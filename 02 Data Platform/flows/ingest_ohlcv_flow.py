"""Local Prefect flow for minimal OHLCV ingestion."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from uuid import uuid4

import ccxt
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from prefect import flow, get_run_logger, task

from config import DataPlatformSettings, build_postgres_dsn, load_settings


REQUIRED_COLUMNS = [
    "exchange",
    "symbol",
    "timeframe",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "source",
    "run_id",
    "ingested_at",
    "validated_at",
    "data_quality_score",
]

TIMEFRAME_INTERVALS = {
    "1d": pd.Timedelta(days=1),
    "4h": pd.Timedelta(hours=4),
}


def _ccxt_symbol(symbol: str) -> str:
    if "/" in symbol:
        return symbol
    if symbol.endswith("USDT"):
        return f"{symbol[:-4]}/USDT"
    return symbol


def _safe_symbol(symbol: str) -> str:
    return symbol.replace("/", "")


def _isoformat_timestamp(value: pd.Timestamp) -> str:
    return value.to_pydatetime().isoformat()


def _timestamp_ms(value: str) -> int:
    return int(pd.Timestamp(value).timestamp() * 1000)


def _to_utc_timestamp(value: object) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        return timestamp.tz_localize(UTC)
    return timestamp.tz_convert(UTC)


def _timeframe_interval(timeframe: str) -> pd.Timedelta:
    expected_interval = TIMEFRAME_INTERVALS.get(timeframe)
    if expected_interval is None:
        raise ValueError(f"Unsupported timeframe={timeframe}")
    return expected_interval


def _close_times(timestamps: pd.Series, timeframe: str) -> pd.Series:
    return timestamps + _timeframe_interval(timeframe)


def _latest_closed_expected_timestamp(
    timeframe: str,
    now_utc: pd.Timestamp,
) -> pd.Timestamp:
    interval = _timeframe_interval(timeframe)
    candidate_time = now_utc - interval
    if timeframe == "1d":
        return candidate_time.floor("D")
    if timeframe == "4h":
        return candidate_time.floor("4h")
    raise ValueError(f"Unsupported timeframe={timeframe}")


def _missing_closed_candle_count(
    available_from_timestamp: pd.Timestamp,
    latest_stored_timestamp: pd.Timestamp | None,
    latest_closed_expected_timestamp: pd.Timestamp,
    timeframe: str,
) -> int:
    interval = _timeframe_interval(timeframe)
    if latest_stored_timestamp is None:
        if available_from_timestamp > latest_closed_expected_timestamp:
            return 0
        return int(
            ((latest_closed_expected_timestamp - available_from_timestamp) / interval) + 1
        )
    if latest_stored_timestamp >= latest_closed_expected_timestamp:
        return 0
    return int((latest_closed_expected_timestamp - latest_stored_timestamp) / interval)


def _remaining_gap_bounds(
    available_from_timestamp: pd.Timestamp,
    latest_stored_timestamp: pd.Timestamp | None,
    latest_closed_expected_timestamp: pd.Timestamp,
    timeframe: str,
) -> tuple[pd.Timestamp | None, pd.Timestamp | None, int]:
    missing_count = _missing_closed_candle_count(
        available_from_timestamp,
        latest_stored_timestamp,
        latest_closed_expected_timestamp,
        timeframe,
    )
    if missing_count == 0:
        return None, None, 0

    interval = _timeframe_interval(timeframe)
    if latest_stored_timestamp is None:
        return available_from_timestamp, latest_closed_expected_timestamp, missing_count
    return (
        latest_stored_timestamp + interval,
        latest_closed_expected_timestamp,
        missing_count,
    )


def _reconciliation_health_status(
    is_caught_up_after_run: bool,
    expected_missing_before_run: int,
    rows_closed_eligible: int,
    gaps_found: int,
) -> str:
    if not is_caught_up_after_run:
        return "gap_remaining"
    if rows_closed_eligible == 0 and expected_missing_before_run == 0:
        return "no_new_closed_candles"
    if gaps_found:
        return "caught_up_with_historical_warnings"
    return "caught_up"


def _has_open_candles(df: pd.DataFrame, now_utc: pd.Timestamp) -> bool:
    if df.empty:
        return False
    for timeframe, group in df.groupby("timeframe"):
        close_time = _close_times(group["timestamp"], str(timeframe))
        if (close_time > now_utc).any():
            return True
    return False


def _merge_upsert_metadata(
    fetch_metadata: dict[str, object] | None,
    upsert_result: dict[str, object] | None,
) -> dict[str, object]:
    metadata = json.loads(json.dumps(fetch_metadata or {}))
    dataset_upserts = (upsert_result or {}).get("datasets", {})
    if not isinstance(dataset_upserts, dict):
        return metadata

    datasets = metadata.setdefault("datasets", {})
    if not isinstance(datasets, dict):
        metadata["datasets"] = {}
        datasets = metadata["datasets"]

    for dataset_key, dataset_result in dataset_upserts.items():
        if not isinstance(dataset_result, dict):
            continue
        dataset_metadata = datasets.setdefault(dataset_key, {})
        if not isinstance(dataset_metadata, dict):
            datasets[dataset_key] = {}
            dataset_metadata = datasets[dataset_key]
        dataset_metadata.update(dataset_result)

    return metadata


def _mark_reconciliation_failed_validation(
    fetch_metadata: dict[str, object] | None,
) -> dict[str, object]:
    metadata = json.loads(json.dumps(fetch_metadata or {}))
    datasets = metadata.setdefault("datasets", {})
    if not isinstance(datasets, dict):
        metadata["datasets"] = {}
        datasets = metadata["datasets"]

    for dataset_metadata in datasets.values():
        if not isinstance(dataset_metadata, dict):
            continue
        dataset_metadata["health_status"] = "failed_validation"
        dataset_metadata["is_caught_up_after_run"] = False
        dataset_metadata["reconciliation_health"] = {
            "health_status": "failed_validation",
            "is_caught_up_after_run": False,
            "reason": "curated_validation_failed_before_postgres_upsert",
        }
    return metadata


def _get_latest_ohlcv_timestamp(
    settings: DataPlatformSettings,
    symbol: str,
    timeframe: str,
) -> pd.Timestamp | None:
    with psycopg2.connect(build_postgres_dsn(settings.postgres)) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT MAX(timestamp)
                FROM ohlcv_curated
                WHERE exchange = %s
                  AND symbol = %s
                  AND timeframe = %s;
                """,
                (settings.default_exchange, symbol, timeframe),
            )
            latest_timestamp = cursor.fetchone()[0]

    if latest_timestamp is None:
        return None
    return _to_utc_timestamp(latest_timestamp)


@task
def finalize_reconciliation_health(
    settings: DataPlatformSettings,
    fetch_metadata: dict[str, object] | None,
    upsert_result: dict[str, object] | None,
    validation_result: dict[str, object],
) -> dict[str, object]:
    metadata = _merge_upsert_metadata(fetch_metadata, upsert_result)
    datasets = metadata.setdefault("datasets", {})
    if not isinstance(datasets, dict):
        metadata["datasets"] = {}
        datasets = metadata["datasets"]

    gaps_found = int(validation_result.get("gaps_found") or 0)
    for dataset_key, dataset_metadata in datasets.items():
        if not isinstance(dataset_metadata, dict):
            continue
        try:
            safe_symbol, timeframe = str(dataset_key).split(":", maxsplit=1)
        except ValueError:
            continue

        symbol_start_timestamp = _to_utc_timestamp(
            settings.symbol_start_dates.get(
                safe_symbol,
                "2017-01-01T00:00:00Z",
            )
        )
        expected_raw = dataset_metadata.get("latest_closed_expected_timestamp")
        if expected_raw is None:
            latest_closed_expected_timestamp = _latest_closed_expected_timestamp(
                timeframe,
                pd.Timestamp.now(tz=UTC),
            )
        else:
            latest_closed_expected_timestamp = _to_utc_timestamp(expected_raw)

        latest_stored_after_run = _get_latest_ohlcv_timestamp(
            settings,
            safe_symbol,
            timeframe,
        )
        (
            remaining_gap_start,
            remaining_gap_end,
            missing_closed_candles_after_run,
        ) = _remaining_gap_bounds(
            symbol_start_timestamp,
            latest_stored_after_run,
            latest_closed_expected_timestamp,
            timeframe,
        )
        is_caught_up_after_run = missing_closed_candles_after_run == 0
        rows_closed_eligible = int(dataset_metadata.get("rows_closed_eligible") or 0)
        expected_missing_before_run = int(
            dataset_metadata.get("expected_missing_closed_candles_before_run") or 0
        )
        health_status = _reconciliation_health_status(
            is_caught_up_after_run,
            expected_missing_before_run,
            rows_closed_eligible,
            gaps_found,
        )

        dataset_metadata["latest_stored_after_run"] = (
            latest_stored_after_run.isoformat()
            if latest_stored_after_run is not None
            else None
        )
        dataset_metadata["is_caught_up_after_run"] = is_caught_up_after_run
        dataset_metadata["missing_closed_candles_after_run"] = (
            missing_closed_candles_after_run
        )
        dataset_metadata["remaining_gap_start"] = (
            remaining_gap_start.isoformat()
            if remaining_gap_start is not None
            else None
        )
        dataset_metadata["remaining_gap_end"] = (
            remaining_gap_end.isoformat()
            if remaining_gap_end is not None
            else None
        )
        dataset_metadata["health_status"] = health_status
        dataset_metadata["reconciliation_health"] = {
            "latest_stored_before_run": dataset_metadata.get(
                "latest_stored_before_run"
            ),
            "latest_closed_expected_timestamp": (
                latest_closed_expected_timestamp.isoformat()
            ),
            "latest_stored_after_run": dataset_metadata[
                "latest_stored_after_run"
            ],
            "expected_missing_closed_candles_before_run": (
                expected_missing_before_run
            ),
            "missing_closed_candles_after_run": (
                missing_closed_candles_after_run
            ),
            "remaining_gap_start": dataset_metadata["remaining_gap_start"],
            "remaining_gap_end": dataset_metadata["remaining_gap_end"],
            "is_caught_up_after_run": is_caught_up_after_run,
            "health_status": health_status,
        }

    return metadata


@task
def load_config() -> DataPlatformSettings:
    settings = load_settings()
    get_run_logger().info(
        "Config loaded. exchange=%s symbols=%s timeframes=%s mode=%s limit=%s page_limit=%s overlap_candles=%s",
        settings.default_exchange,
        settings.default_symbols,
        settings.default_timeframes,
        settings.ohlcv_mode,
        settings.ohlcv_fetch_limit,
        settings.ohlcv_page_limit,
        settings.ohlcv_incremental_overlap_candles,
    )
    return settings


@task
def fetch_ohlcv(settings: DataPlatformSettings, run_id: str) -> dict[str, object]:
    logger = get_run_logger()
    exchange = ccxt.binance({"enableRateLimit": True, "timeout": 30000})
    ingested_at = datetime.now(UTC)
    frames: list[pd.DataFrame] = []
    fetch_metadata: dict[str, object] = {
        "mode": settings.ohlcv_mode,
        "page_limit": settings.ohlcv_page_limit,
        "fetch_limit": settings.ohlcv_fetch_limit,
        "symbols": list(settings.default_symbols),
        "timeframes": list(settings.default_timeframes),
        "datasets": {},
    }

    for symbol in settings.default_symbols:
        for timeframe in settings.default_timeframes:
            ccxt_pair = _ccxt_symbol(symbol)
            safe_symbol = _safe_symbol(symbol)
            expected_interval = _timeframe_interval(timeframe)
            interval_ms = int(expected_interval.total_seconds() * 1000)
            dataset_key = f"{safe_symbol}:{timeframe}"
            pages_downloaded = 0
            rows: list[list[float]] = []

            if settings.ohlcv_mode == "recent":
                logger.info(
                    "Fetching recent OHLCV from Binance. symbol=%s timeframe=%s limit=%s",
                    ccxt_pair,
                    timeframe,
                    settings.ohlcv_fetch_limit,
                )
                rows = exchange.fetch_ohlcv(
                    ccxt_pair,
                    timeframe=timeframe,
                    limit=settings.ohlcv_fetch_limit,
                )
                pages_downloaded = 1 if rows else 0
                fetch_metadata["datasets"][dataset_key] = {
                    "mode": settings.ohlcv_mode,
                    "last_existing_timestamp": None,
                    "fetch_since_timestamp": None,
                    "pages_downloaded": pages_downloaded,
                    "rows_fetched": 0,
                    "min_timestamp": None,
                    "max_timestamp": None,
                }
            elif settings.ohlcv_mode == "full_history":
                since_ms = _timestamp_ms(
                    settings.symbol_start_dates.get(safe_symbol, "2017-01-01T00:00:00Z")
                )
                now_ms = exchange.milliseconds()
                last_seen_ts = None
                logger.info(
                    "Fetching full OHLCV history from Binance. symbol=%s timeframe=%s since=%s page_limit=%s",
                    ccxt_pair,
                    timeframe,
                    pd.to_datetime(since_ms, unit="ms", utc=True).isoformat(),
                    settings.ohlcv_page_limit,
                )

                while since_ms <= now_ms:
                    page = exchange.fetch_ohlcv(
                        ccxt_pair,
                        timeframe=timeframe,
                        since=since_ms,
                        limit=settings.ohlcv_page_limit,
                    )
                    if not page:
                        logger.info(
                            "No more OHLCV rows. symbol=%s timeframe=%s pages=%s rows=%s",
                            ccxt_pair,
                            timeframe,
                            pages_downloaded,
                            len(rows),
                        )
                        break

                    first_ts = int(page[0][0])
                    last_ts = int(page[-1][0])
                    if last_seen_ts is not None and last_ts <= last_seen_ts:
                        logger.warning(
                            "Stopping pagination because timestamp did not advance. symbol=%s timeframe=%s last_ts=%s",
                            ccxt_pair,
                            timeframe,
                            last_ts,
                        )
                        break

                    rows.extend(page)
                    pages_downloaded += 1
                    logger.info(
                        "Fetched page=%s symbol=%s timeframe=%s rows=%s first=%s last=%s",
                        pages_downloaded,
                        ccxt_pair,
                        timeframe,
                        len(page),
                        pd.to_datetime(first_ts, unit="ms", utc=True).isoformat(),
                        pd.to_datetime(last_ts, unit="ms", utc=True).isoformat(),
                    )
                    last_seen_ts = last_ts
                    since_ms = last_ts + interval_ms

                    if len(page) < settings.ohlcv_page_limit and since_ms >= now_ms:
                        break
                fetch_metadata["datasets"][dataset_key] = {
                    "mode": settings.ohlcv_mode,
                    "last_existing_timestamp": None,
                    "fetch_since_timestamp": pd.to_datetime(
                        _timestamp_ms(
                            settings.symbol_start_dates.get(
                                safe_symbol, "2017-01-01T00:00:00Z"
                            )
                        ),
                        unit="ms",
                        utc=True,
                    ).isoformat(),
                    "pages_downloaded": pages_downloaded,
                    "rows_fetched": 0,
                    "min_timestamp": None,
                    "max_timestamp": None,
                }
            elif settings.ohlcv_mode == "incremental":
                now_utc = pd.Timestamp.now(tz=UTC)
                symbol_start_timestamp = _to_utc_timestamp(
                    settings.symbol_start_dates.get(
                        safe_symbol,
                        "2017-01-01T00:00:00Z",
                    )
                )
                latest_closed_expected_timestamp = _latest_closed_expected_timestamp(
                    timeframe,
                    now_utc,
                )
                latest_timestamp = _get_latest_ohlcv_timestamp(
                    settings,
                    safe_symbol,
                    timeframe,
                )
                (
                    missing_from_timestamp,
                    missing_to_timestamp,
                    expected_missing_closed_candles,
                ) = _remaining_gap_bounds(
                    symbol_start_timestamp,
                    latest_timestamp,
                    latest_closed_expected_timestamp,
                    timeframe,
                )
                is_already_caught_up_before_run = (
                    expected_missing_closed_candles == 0
                )
                if latest_timestamp is None:
                    fetch_since_timestamp = symbol_start_timestamp
                    overlap_candles = 0
                else:
                    overlap_candles = max(
                        1,
                        int(settings.ohlcv_incremental_overlap_candles),
                    )
                    fetch_since_timestamp = max(
                        latest_timestamp - (expected_interval * overlap_candles),
                        symbol_start_timestamp,
                    )

                since_ms = int(fetch_since_timestamp.timestamp() * 1000)
                target_until_timestamp = min(
                    latest_closed_expected_timestamp + expected_interval,
                    now_utc,
                )
                target_until_ms = int(target_until_timestamp.timestamp() * 1000)
                last_seen_ts = None
                logger.info(
                    "Fetching incremental OHLCV from Binance. symbol=%s timeframe=%s latest_existing=%s expected_latest_closed=%s missing_closed_before=%s fetch_since=%s overlap_candles=%s page_limit=%s",
                    ccxt_pair,
                    timeframe,
                    latest_timestamp.isoformat() if latest_timestamp is not None else None,
                    latest_closed_expected_timestamp.isoformat(),
                    expected_missing_closed_candles,
                    fetch_since_timestamp.isoformat(),
                    overlap_candles,
                    settings.ohlcv_page_limit,
                )

                while since_ms <= target_until_ms:
                    page = exchange.fetch_ohlcv(
                        ccxt_pair,
                        timeframe=timeframe,
                        since=since_ms,
                        limit=settings.ohlcv_page_limit,
                    )
                    if not page:
                        logger.info(
                            "No new OHLCV rows. symbol=%s timeframe=%s latest_existing=%s fetch_since=%s",
                            ccxt_pair,
                            timeframe,
                            latest_timestamp.isoformat()
                            if latest_timestamp is not None
                            else None,
                            fetch_since_timestamp.isoformat(),
                        )
                        break

                    first_ts = int(page[0][0])
                    last_ts = int(page[-1][0])
                    if last_seen_ts is not None and last_ts <= last_seen_ts:
                        logger.warning(
                            "Stopping incremental pagination because timestamp did not advance. symbol=%s timeframe=%s last_ts=%s",
                            ccxt_pair,
                            timeframe,
                            last_ts,
                        )
                        break

                    rows.extend(page)
                    pages_downloaded += 1
                    logger.info(
                        "Fetched incremental page=%s symbol=%s timeframe=%s rows=%s first=%s last=%s",
                        pages_downloaded,
                        ccxt_pair,
                        timeframe,
                        len(page),
                        pd.to_datetime(first_ts, unit="ms", utc=True).isoformat(),
                        pd.to_datetime(last_ts, unit="ms", utc=True).isoformat(),
                    )
                    last_seen_ts = last_ts
                    since_ms = last_ts + interval_ms

                    if (
                        len(page) < settings.ohlcv_page_limit
                        and since_ms >= target_until_ms
                    ):
                        break

                fetch_metadata["datasets"][dataset_key] = {
                    "mode": settings.ohlcv_mode,
                    "last_existing_timestamp": latest_timestamp.isoformat()
                    if latest_timestamp is not None
                    else None,
                    "latest_stored_before_run": latest_timestamp.isoformat()
                    if latest_timestamp is not None
                    else None,
                    "latest_closed_expected_timestamp": (
                        latest_closed_expected_timestamp.isoformat()
                    ),
                    "missing_from_timestamp": missing_from_timestamp.isoformat()
                    if missing_from_timestamp is not None
                    else None,
                    "missing_to_timestamp": missing_to_timestamp.isoformat()
                    if missing_to_timestamp is not None
                    else None,
                    "expected_missing_closed_candles_before_run": (
                        expected_missing_closed_candles
                    ),
                    "is_already_caught_up_before_run": (
                        is_already_caught_up_before_run
                    ),
                    "fetch_since_timestamp": fetch_since_timestamp.isoformat(),
                    "incremental_start_timestamp": fetch_since_timestamp.isoformat(),
                    "incremental_overlap_candles": overlap_candles,
                    "incremental_overlap_interval_seconds": int(
                        expected_interval.total_seconds() * overlap_candles
                    ),
                    "incremental_overlap_policy": (
                        "start_at_max_latest_stored_minus_overlap_or_symbol_start"
                        if latest_timestamp is not None
                        else "start_at_symbol_start_date"
                    ),
                    "pages_downloaded": pages_downloaded,
                    "rows_fetched": 0,
                    "rows_fetched_raw": 0,
                    "rows_closed_eligible": 0,
                    "rows_open_excluded": 0,
                    "closed_candles_only": True,
                    "min_timestamp": None,
                    "max_timestamp": None,
                    "latest_fetched_timestamp": None,
                    "latest_closed_eligible_timestamp": None,
                    "target_fetch_until_timestamp": target_until_timestamp.isoformat(),
                    "reconciliation_plan": {
                        "latest_stored_before_run": latest_timestamp.isoformat()
                        if latest_timestamp is not None
                        else None,
                        "latest_closed_expected_timestamp": (
                            latest_closed_expected_timestamp.isoformat()
                        ),
                        "missing_from_timestamp": missing_from_timestamp.isoformat()
                        if missing_from_timestamp is not None
                        else None,
                        "missing_to_timestamp": missing_to_timestamp.isoformat()
                        if missing_to_timestamp is not None
                        else None,
                        "expected_missing_closed_candles": (
                            expected_missing_closed_candles
                        ),
                        "is_already_caught_up_before_run": (
                            is_already_caught_up_before_run
                        ),
                        "incremental_start_timestamp": (
                            fetch_since_timestamp.isoformat()
                        ),
                    },
                }
            else:
                raise ValueError(f"Unsupported SULTAN_OHLCV_MODE={settings.ohlcv_mode}")

            frame = pd.DataFrame(
                rows,
                columns=["timestamp", "open", "high", "low", "close", "volume"],
            )
            if frame.empty:
                continue
            frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
            frame["exchange"] = settings.default_exchange
            frame["symbol"] = safe_symbol
            frame["timeframe"] = timeframe
            frame["source"] = "ccxt.binance.fetch_ohlcv"
            frame["run_id"] = run_id
            frame["ingested_at"] = ingested_at
            frame["validated_at"] = pd.NaT
            frame["data_quality_score"] = 0.0
            frame = frame.drop_duplicates(
                subset=["exchange", "symbol", "timeframe", "timestamp"],
                keep="last",
            )
            fetch_metadata["datasets"][dataset_key].update(
                {
                    "pages_downloaded": pages_downloaded,
                    "rows_fetched": int(len(frame)),
                    "rows_fetched_raw": int(len(frame)),
                    "min_timestamp": _isoformat_timestamp(frame["timestamp"].min()),
                    "max_timestamp": _isoformat_timestamp(frame["timestamp"].max()),
                    "latest_fetched_timestamp": _isoformat_timestamp(
                        frame["timestamp"].max()
                    ),
                }
            )
            frames.append(frame[REQUIRED_COLUMNS])

    if not frames:
        return {
            "dataframe": pd.DataFrame(columns=REQUIRED_COLUMNS),
            "metadata": fetch_metadata,
        }

    result = pd.concat(frames, ignore_index=True)
    logger.info("Fetched rows=%s", len(result))
    return {
        "dataframe": result,
        "metadata": fetch_metadata,
    }


@task
def filter_closed_candles(
    df: pd.DataFrame,
    fetch_metadata: dict[str, object],
) -> dict[str, object]:
    logger = get_run_logger()
    metadata = json.loads(json.dumps(fetch_metadata))
    metadata["closed_candles_only"] = True
    metadata["rows_fetched_raw"] = int(len(df))

    if df.empty:
        metadata["rows_closed_eligible"] = 0
        metadata["rows_open_excluded"] = 0
        return {
            "dataframe": df.copy(),
            "metadata": metadata,
        }

    now_utc = pd.Timestamp.now(tz=UTC)
    closed_parts: list[pd.DataFrame] = []
    total_closed = 0
    total_open = 0

    for (symbol, timeframe), group in df.groupby(["symbol", "timeframe"]):
        dataset_key = f"{symbol}:{timeframe}"
        expected_interval = _timeframe_interval(str(timeframe))
        close_time = group["timestamp"] + expected_interval
        closed_mask = close_time <= now_utc
        closed_group = group.loc[closed_mask].copy()
        open_count = int((~closed_mask).sum())
        closed_count = int(len(closed_group))
        total_closed += closed_count
        total_open += open_count

        dataset_metadata = metadata.setdefault("datasets", {}).setdefault(
            dataset_key,
            {},
        )
        dataset_metadata["rows_closed_eligible"] = closed_count
        dataset_metadata["rows_open_excluded"] = open_count
        dataset_metadata["closed_candles_only"] = True
        dataset_metadata["latest_closed_eligible_timestamp"] = (
            _isoformat_timestamp(closed_group["timestamp"].max())
            if not closed_group.empty
            else None
        )

        if not closed_group.empty:
            closed_parts.append(closed_group)

    metadata["rows_closed_eligible"] = total_closed
    metadata["rows_open_excluded"] = total_open
    logger.info(
        "Closed candle filter completed. raw_rows=%s closed_rows=%s open_excluded=%s",
        len(df),
        total_closed,
        total_open,
    )

    if not closed_parts:
        closed_df = pd.DataFrame(columns=REQUIRED_COLUMNS)
    else:
        closed_df = pd.concat(closed_parts, ignore_index=True)

    return {
        "dataframe": closed_df[REQUIRED_COLUMNS],
        "metadata": metadata,
    }


@task
def validate_ohlcv(df: pd.DataFrame, settings: DataPlatformSettings) -> dict[str, object]:
    logger = get_run_logger()
    blocking_errors: list[str] = []
    warning_errors: list[str] = []
    rows_checked = len(df)
    gaps_found = 0
    freshness_lag_seconds = None
    freshness_detail: dict[str, dict[str, object]] = {}
    gap_detail: list[dict[str, object]] = []

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        blocking_errors.append(f"missing_columns={missing_columns}")

    if df.empty and settings.ohlcv_mode != "incremental":
        blocking_errors.append("empty_dataset")

    if not missing_columns and not df.empty:
        now_utc = pd.Timestamp.now(tz=UTC)
        if df["timestamp"].isna().any():
            blocking_errors.append("timestamp_nulls")
        if df[["open", "high", "low", "close"]].isna().any().any():
            blocking_errors.append("ohlc_nulls")
        if (df["high"] < df["low"]).any():
            blocking_errors.append("high_lt_low")
        if (df["high"] < df["open"]).any():
            blocking_errors.append("high_lt_open")
        if (df["high"] < df["close"]).any():
            blocking_errors.append("high_lt_close")
        if (df["low"] > df["open"]).any():
            blocking_errors.append("low_gt_open")
        if (df["low"] > df["close"]).any():
            blocking_errors.append("low_gt_close")
        if (df["volume"] < 0).any():
            blocking_errors.append("volume_negative")
        duplicate_count = df.duplicated(
            subset=["exchange", "symbol", "timeframe", "timestamp"]
        ).sum()
        if duplicate_count:
            blocking_errors.append(f"duplicate_bars={int(duplicate_count)}")
        if _has_open_candles(df, now_utc):
            blocking_errors.append("open_candles_in_curated_candidate")

        max_freshness_lag_seconds = 0

        for (exchange, symbol, timeframe), group in df.groupby(
            ["exchange", "symbol", "timeframe"]
        ):
            ordered = group.sort_values("timestamp").reset_index(drop=True)
            expected_interval = TIMEFRAME_INTERVALS.get(str(timeframe))
            detail_key = f"{exchange}:{symbol}:{timeframe}"
            max_timestamp = ordered["timestamp"].max()
            lag_seconds = int((now_utc - max_timestamp).total_seconds())
            max_freshness_lag_seconds = max(max_freshness_lag_seconds, lag_seconds)
            freshness_detail[detail_key] = {
                "max_timestamp": _isoformat_timestamp(max_timestamp),
                "freshness_lag_seconds": lag_seconds,
            }

            if expected_interval is None:
                blocking_errors.append(f"unsupported_timeframe={timeframe}")
                continue

            deltas = ordered["timestamp"].diff()
            gap_deltas = deltas[deltas > expected_interval]
            if not gap_deltas.empty:
                gaps_found += int(len(gap_deltas))
                gap_events = []
                for index, observed_interval in gap_deltas.items():
                    previous_timestamp = ordered.loc[index - 1, "timestamp"]
                    current_timestamp = ordered.loc[index, "timestamp"]
                    gap_events.append(
                        {
                            "previous_timestamp": _isoformat_timestamp(previous_timestamp),
                            "current_timestamp": _isoformat_timestamp(current_timestamp),
                            "observed_interval_seconds": int(
                                observed_interval.total_seconds()
                            ),
                        }
                    )
                gap_detail.append(
                    {
                        "exchange": str(exchange),
                        "symbol": str(symbol),
                        "timeframe": str(timeframe),
                        "gaps_found": int(len(gap_deltas)),
                        "expected_interval_seconds": int(expected_interval.total_seconds()),
                        "events": gap_events,
                    }
                )

        freshness_lag_seconds = max_freshness_lag_seconds
        if gaps_found:
            warning_errors.append(f"gaps_found={gaps_found}")

    is_valid = not blocking_errors
    rows_failed = rows_checked if blocking_errors else 0
    quality_score = 0.0 if blocking_errors else 0.95 if warning_errors else 1.0
    check_status = (
        "failed"
        if blocking_errors
        else "passed_with_warnings"
        if warning_errors
        else "passed"
    )
    logger.info(
        "Validation completed. valid=%s rows_checked=%s gaps_found=%s freshness_lag_seconds=%s blocking_errors=%s warning_errors=%s",
        is_valid,
        rows_checked,
        gaps_found,
        freshness_lag_seconds,
        blocking_errors,
        warning_errors,
    )
    logger.info("Freshness detail: %s", freshness_detail)
    logger.info("Gap detail: %s", gap_detail)
    logger.info("Quality check status=%s data_quality_score=%s", check_status, quality_score)
    logger.info("Pipeline will %s", "continue" if is_valid else "block")
    return {
        "is_valid": is_valid,
        "check_status": check_status,
        "rows_checked": rows_checked,
        "rows_failed": rows_failed,
        "gaps_found": gaps_found,
        "freshness_lag_seconds": freshness_lag_seconds,
        "data_quality_score": quality_score,
        "errors": blocking_errors,
        "blocking_errors": blocking_errors,
        "warning_errors": warning_errors,
        "metadata": {
            "freshness": freshness_detail,
            "gaps": gap_detail,
        },
    }


@task
def save_raw_parquet(settings: DataPlatformSettings, df: pd.DataFrame, run_id: str) -> list[str]:
    logger = get_run_logger()
    written_paths: list[str] = []

    if df.empty:
        logger.info("Raw parquet skipped because dataset is empty.")
        return written_paths

    for (symbol, timeframe, year, month), group in df.assign(
        year=df["timestamp"].dt.year,
        month=df["timestamp"].dt.month,
    ).groupby(["symbol", "timeframe", "year", "month"]):
        target_dir = (
            settings.raw_data_dir
            / "binance"
            / str(symbol)
            / str(timeframe)
            / str(year)
            / f"{int(month):02d}"
        )
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / f"ohlcv_{run_id}.parquet"
        group.drop(columns=["year", "month"]).to_parquet(target_file, index=False)
        written_paths.append(str(target_file))

    logger.info("Raw parquet files written=%s", len(written_paths))
    return written_paths


@task
def transform_to_curated(df: pd.DataFrame, validation_result: dict[str, object]) -> pd.DataFrame:
    if not validation_result["is_valid"]:
        raise ValueError(f"OHLCV validation failed: {validation_result['errors']}")

    curated = df.copy()
    now_utc = pd.Timestamp.now(tz=UTC)
    if _has_open_candles(curated, now_utc):
        raise ValueError("curated_contains_open_candles")
    curated["validated_at"] = datetime.now(UTC)
    curated["data_quality_score"] = float(validation_result["data_quality_score"])
    curated = curated.sort_values(["exchange", "symbol", "timeframe", "timestamp"])
    return curated[REQUIRED_COLUMNS]


@task
def save_curated_parquet(
    settings: DataPlatformSettings,
    df: pd.DataFrame,
    run_id: str,
) -> list[str]:
    logger = get_run_logger()
    written_paths: list[str] = []

    for (symbol, timeframe), group in df.groupby(["symbol", "timeframe"]):
        target_dir = settings.curated_data_dir / "ohlcv" / str(symbol) / str(timeframe)
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / f"ohlcv_{run_id}.parquet"
        group.to_parquet(target_file, index=False)
        written_paths.append(str(target_file))

    logger.info("Curated parquet files written=%s", len(written_paths))
    return written_paths


@task
def write_ingestion_run(
    settings: DataPlatformSettings,
    run_id: str,
    started_at: datetime,
    status: str,
    rows_fetched: int,
    rows_validated: int,
    rows_inserted: int,
    raw_paths: list[str],
    curated_paths: list[str],
    error_message: str | None,
    fetch_metadata: dict[str, object] | None = None,
    upsert_result: dict[str, object] | None = None,
) -> None:
    symbols = list(settings.default_symbols)
    timeframes = list(settings.default_timeframes)
    merged_fetch_metadata = _merge_upsert_metadata(fetch_metadata, upsert_result)
    metadata = json.dumps(
        {
            "raw_paths": raw_paths,
            "curated_paths": curated_paths,
            "fetch": merged_fetch_metadata,
            "upsert_result": upsert_result or {},
        }
    )

    with psycopg2.connect(build_postgres_dsn(settings.postgres)) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO ingestion_runs (
                    run_id, flow_name, source_name, status, started_at, finished_at,
                    symbols, timeframes, rows_fetched, rows_validated, rows_inserted,
                    raw_path, curated_path, error_message, metadata
                )
                VALUES (
                    %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb
                )
                ON CONFLICT (run_id) DO UPDATE SET
                    status = EXCLUDED.status,
                    finished_at = EXCLUDED.finished_at,
                    rows_fetched = EXCLUDED.rows_fetched,
                    rows_validated = EXCLUDED.rows_validated,
                    rows_inserted = EXCLUDED.rows_inserted,
                    raw_path = EXCLUDED.raw_path,
                    curated_path = EXCLUDED.curated_path,
                    error_message = EXCLUDED.error_message,
                    metadata = EXCLUDED.metadata;
                """,
                (
                    str(run_id),
                    "ingest_ohlcv_flow",
                    "binance",
                    status,
                    started_at,
                    symbols,
                    timeframes,
                    rows_fetched,
                    rows_validated,
                    rows_inserted,
                    raw_paths[0] if raw_paths else None,
                    curated_paths[0] if curated_paths else None,
                    error_message,
                    metadata,
                ),
            )
    get_run_logger().info("ingestion_runs registered. status=%s", status)


@task
def upsert_postgres(settings: DataPlatformSettings, df: pd.DataFrame) -> dict[str, object]:
    now_utc = pd.Timestamp.now(tz=UTC)
    if _has_open_candles(df, now_utc):
        raise ValueError("postgres_upsert_rejected_open_candles")
    rows = [
        (
            row.exchange,
            row.symbol,
            row.timeframe,
            row.timestamp.to_pydatetime(),
            row.open,
            row.high,
            row.low,
            row.close,
            row.volume,
            row.source,
            str(row.run_id),
            row.ingested_at.to_pydatetime(),
            row.validated_at.to_pydatetime(),
            row.data_quality_score,
        )
        for row in df.itertuples(index=False)
    ]

    if not rows:
        return {
            "rows_inserted_or_updated": 0,
            "rows_new": 0,
            "rows_existing": 0,
            "datasets": {},
        }

    with psycopg2.connect(build_postgres_dsn(settings.postgres)) as connection:
        with connection.cursor() as cursor:
            key_rows = [(row[0], row[1], row[2], row[3]) for row in rows]
            existing_count_rows = execute_values(
                cursor,
                """
                SELECT COUNT(*)
                FROM (VALUES %s) AS incoming(exchange, symbol, timeframe, timestamp)
                JOIN ohlcv_curated existing
                  ON existing.exchange = incoming.exchange
                 AND existing.symbol = incoming.symbol
                 AND existing.timeframe = incoming.timeframe
                 AND existing.timestamp = incoming.timestamp::timestamptz;
                """,
                key_rows,
                page_size=1000,
                fetch=True,
            )
            existing_count = sum(row[0] for row in existing_count_rows)
            existing_by_dataset_rows = execute_values(
                cursor,
                """
                SELECT incoming.symbol, incoming.timeframe, COUNT(*)
                FROM (VALUES %s) AS incoming(exchange, symbol, timeframe, timestamp)
                JOIN ohlcv_curated existing
                  ON existing.exchange = incoming.exchange
                 AND existing.symbol = incoming.symbol
                 AND existing.timeframe = incoming.timeframe
                 AND existing.timestamp = incoming.timestamp::timestamptz
                GROUP BY incoming.symbol, incoming.timeframe;
                """,
                key_rows,
                page_size=1000,
                fetch=True,
            )
            existing_by_dataset = {
                f"{row[0]}:{row[1]}": int(row[2])
                for row in existing_by_dataset_rows
            }
            execute_values(
                cursor,
                """
                INSERT INTO ohlcv_curated (
                    exchange, symbol, timeframe, timestamp, open, high, low, close,
                    volume, source, run_id, ingested_at, validated_at, data_quality_score
                )
                VALUES %s
                ON CONFLICT (exchange, symbol, timeframe, timestamp) DO UPDATE SET
                    open = EXCLUDED.open,
                    high = EXCLUDED.high,
                    low = EXCLUDED.low,
                    close = EXCLUDED.close,
                    volume = EXCLUDED.volume,
                    source = EXCLUDED.source,
                    run_id = EXCLUDED.run_id,
                    ingested_at = EXCLUDED.ingested_at,
                    validated_at = EXCLUDED.validated_at,
                    data_quality_score = EXCLUDED.data_quality_score,
                    updated_at = NOW();
                """,
                rows,
                page_size=1000,
            )

    rows_by_dataset: dict[str, int] = {}
    for row in rows:
        dataset_key = f"{row[1]}:{row[2]}"
        rows_by_dataset[dataset_key] = rows_by_dataset.get(dataset_key, 0) + 1

    dataset_results = {}
    for dataset_key, rows_inserted_or_updated in rows_by_dataset.items():
        rows_existing = existing_by_dataset.get(dataset_key, 0)
        dataset_results[dataset_key] = {
            "rows_inserted_or_updated": rows_inserted_or_updated,
            "rows_existing": rows_existing,
            "rows_new": rows_inserted_or_updated - rows_existing,
        }

    upsert_result: dict[str, object] = {
        "rows_inserted_or_updated": len(rows),
        "rows_new": len(rows) - int(existing_count),
        "rows_existing": int(existing_count),
        "datasets": dataset_results,
    }
    get_run_logger().info(
        "PostgreSQL ohlcv_curated upserted rows=%s new=%s existing=%s",
        upsert_result["rows_inserted_or_updated"],
        upsert_result["rows_new"],
        upsert_result["rows_existing"],
    )
    return upsert_result


@task
def write_quality_report(
    settings: DataPlatformSettings,
    run_id: str,
    validation_result: dict[str, object],
    fetch_metadata: dict[str, object] | None = None,
) -> None:
    status = str(validation_result["check_status"])
    severity = (
        "error"
        if status == "failed"
        else "warning"
        if status == "passed_with_warnings"
        else "info"
    )
    error_message = None
    if validation_result["blocking_errors"]:
        error_message = "; ".join(validation_result["blocking_errors"])

    with psycopg2.connect(build_postgres_dsn(settings.postgres)) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO data_quality_checks (
                    run_id, dataset_name, check_name, check_status, severity,
                    rows_checked, rows_failed, gaps_found, freshness_lag_seconds,
                    data_quality_score, error_message, metadata
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb);
                """,
                (
                    str(run_id),
                    "ohlcv",
                    "minimal_ohlcv_contract",
                    status,
                    severity,
                    validation_result["rows_checked"],
                    validation_result["rows_failed"],
                    validation_result["gaps_found"],
                    validation_result["freshness_lag_seconds"],
                    validation_result["data_quality_score"],
                    error_message,
                    json.dumps(
                        {
                            "errors": validation_result["blocking_errors"],
                            "warnings": validation_result["warning_errors"],
                            "fetch": fetch_metadata or {},
                            **validation_result["metadata"],
                        }
                    ),
                ),
            )
    get_run_logger().info("data_quality_checks registered. status=%s", status)


@flow(name="ingest_ohlcv_flow")
def ingest_ohlcv_flow() -> dict[str, object]:
    run_id = str(uuid4())
    started_at = datetime.now(UTC)
    settings = load_config()
    fetch_result = fetch_ohlcv(settings, run_id)
    raw_df = fetch_result["dataframe"]
    fetch_metadata = fetch_result["metadata"]
    raw_paths = save_raw_parquet(settings, raw_df, run_id)
    closed_result = filter_closed_candles(raw_df, fetch_metadata)
    df = closed_result["dataframe"]
    fetch_metadata = closed_result["metadata"]
    validation_result = validate_ohlcv(df, settings)

    if not validation_result["is_valid"]:
        fetch_metadata = _mark_reconciliation_failed_validation(fetch_metadata)
        write_ingestion_run(
            settings=settings,
            run_id=run_id,
            started_at=started_at,
            status="failed_validation",
            rows_fetched=len(raw_df),
            rows_validated=0,
            rows_inserted=0,
            raw_paths=raw_paths,
            curated_paths=[],
            error_message="; ".join(validation_result["errors"]),
            fetch_metadata=fetch_metadata,
        )
        write_quality_report(settings, run_id, validation_result, fetch_metadata)
        raise ValueError(f"OHLCV validation failed: {validation_result['errors']}")

    curated_df = transform_to_curated(df, validation_result)
    curated_paths = save_curated_parquet(settings, curated_df, run_id)
    write_ingestion_run(
        settings=settings,
        run_id=run_id,
        started_at=started_at,
        status="running",
        rows_fetched=len(raw_df),
        rows_validated=len(curated_df),
        rows_inserted=0,
        raw_paths=raw_paths,
        curated_paths=curated_paths,
        error_message=None,
        fetch_metadata=fetch_metadata,
    )
    rows_inserted = {
        "rows_inserted_or_updated": 0,
        "rows_new": 0,
        "rows_existing": 0,
    }
    try:
        rows_inserted = upsert_postgres(settings, curated_df)
        fetch_metadata = finalize_reconciliation_health(
            settings,
            fetch_metadata,
            rows_inserted,
            validation_result,
        )
        final_status = (
            "success_with_warnings"
            if validation_result["warning_errors"]
            else "success"
        )
        write_ingestion_run(
            settings=settings,
            run_id=run_id,
            started_at=started_at,
            status=final_status,
            rows_fetched=len(raw_df),
            rows_validated=len(curated_df),
            rows_inserted=rows_inserted["rows_inserted_or_updated"],
            raw_paths=raw_paths,
            curated_paths=curated_paths,
            error_message=None,
            fetch_metadata=fetch_metadata,
            upsert_result=rows_inserted,
        )
        write_quality_report(settings, run_id, validation_result, fetch_metadata)
    except Exception as exc:
        write_ingestion_run(
            settings=settings,
            run_id=run_id,
            started_at=started_at,
            status="failed",
            rows_fetched=len(raw_df),
            rows_validated=len(curated_df),
            rows_inserted=rows_inserted["rows_inserted_or_updated"],
            raw_paths=raw_paths,
            curated_paths=curated_paths,
            error_message=str(exc),
            fetch_metadata=fetch_metadata,
            upsert_result=rows_inserted,
        )
        raise

    return {
        "run_id": run_id,
        "rows_fetched": len(raw_df),
        "rows_closed_eligible": len(curated_df),
        "rows_open_excluded": len(raw_df) - len(curated_df),
        "rows_validated": len(curated_df),
        "rows_inserted": rows_inserted["rows_inserted_or_updated"],
        "rows_new": rows_inserted["rows_new"],
        "rows_existing": rows_inserted["rows_existing"],
        "fetch": fetch_metadata,
        "raw_files": raw_paths,
        "curated_files": curated_paths,
    }


if __name__ == "__main__":
    print("This flow will fetch public Binance OHLCV for BTCUSDT and ETHUSDT.")
    print("Configured timeframes: 1d and 4h unless overridden in .env.")
    print("Default mode: incremental catch-up unless overridden in .env.")
    print("It will write Parquet files under data/raw and data/curated, then upsert PostgreSQL.")
    ingest_ohlcv_flow()
