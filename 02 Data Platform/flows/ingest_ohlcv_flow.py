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


@task
def load_config() -> DataPlatformSettings:
    settings = load_settings()
    get_run_logger().info(
        "Config loaded. exchange=%s symbols=%s timeframes=%s mode=%s limit=%s page_limit=%s",
        settings.default_exchange,
        settings.default_symbols,
        settings.default_timeframes,
        settings.ohlcv_mode,
        settings.ohlcv_fetch_limit,
        settings.ohlcv_page_limit,
    )
    return settings


@task
def fetch_ohlcv(settings: DataPlatformSettings, run_id: str) -> dict[str, object]:
    logger = get_run_logger()
    exchange = ccxt.binance({"enableRateLimit": True})
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
            expected_interval = TIMEFRAME_INTERVALS[timeframe]
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
            else:
                raise ValueError(f"Unsupported SULTAN_OHLCV_MODE={settings.ohlcv_mode}")

            frame = pd.DataFrame(
                rows,
                columns=["timestamp", "open", "high", "low", "close", "volume"],
            )
            if frame.empty:
                fetch_metadata["datasets"][dataset_key] = {
                    "pages_downloaded": pages_downloaded,
                    "rows_fetched": 0,
                    "min_timestamp": None,
                    "max_timestamp": None,
                }
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
            fetch_metadata["datasets"][dataset_key] = {
                "pages_downloaded": pages_downloaded,
                "rows_fetched": int(len(frame)),
                "min_timestamp": _isoformat_timestamp(frame["timestamp"].min()),
                "max_timestamp": _isoformat_timestamp(frame["timestamp"].max()),
            }
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
def validate_ohlcv(df: pd.DataFrame) -> dict[str, object]:
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

    if df.empty:
        blocking_errors.append("empty_dataset")

    if not missing_columns and not df.empty:
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

        now_utc = pd.Timestamp.now(tz=UTC)
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
    upsert_result: dict[str, int] | None = None,
) -> None:
    symbols = list(settings.default_symbols)
    timeframes = list(settings.default_timeframes)
    metadata = json.dumps(
        {
            "raw_paths": raw_paths,
            "curated_paths": curated_paths,
            "fetch": fetch_metadata or {},
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
def upsert_postgres(settings: DataPlatformSettings, df: pd.DataFrame) -> dict[str, int]:
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

    upsert_result = {
        "rows_inserted_or_updated": len(rows),
        "rows_new": len(rows) - int(existing_count),
        "rows_existing": int(existing_count),
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
                    "error",
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
    df = fetch_result["dataframe"]
    fetch_metadata = fetch_result["metadata"]
    validation_result = validate_ohlcv(df)
    raw_paths = save_raw_parquet(settings, df, run_id)

    if not validation_result["is_valid"]:
        write_ingestion_run(
            settings=settings,
            run_id=run_id,
            started_at=started_at,
            status="failed_validation",
            rows_fetched=len(df),
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
        rows_fetched=len(df),
        rows_validated=len(curated_df),
        rows_inserted=0,
        raw_paths=raw_paths,
        curated_paths=curated_paths,
        error_message=None,
        fetch_metadata=fetch_metadata,
    )
    rows_inserted = upsert_postgres(settings, curated_df)
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
        rows_fetched=len(df),
        rows_validated=len(curated_df),
        rows_inserted=rows_inserted["rows_inserted_or_updated"],
        raw_paths=raw_paths,
        curated_paths=curated_paths,
        error_message=None,
        fetch_metadata=fetch_metadata,
        upsert_result=rows_inserted,
    )
    write_quality_report(settings, run_id, validation_result, fetch_metadata)

    return {
        "run_id": run_id,
        "rows_fetched": len(df),
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
    print("Default mode: full_history with paginated OHLCV unless overridden in .env.")
    print("It will write Parquet files under data/raw and data/curated, then upsert PostgreSQL.")
    ingest_ohlcv_flow()
