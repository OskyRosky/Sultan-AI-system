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


@task
def load_config() -> DataPlatformSettings:
    settings = load_settings()
    get_run_logger().info(
        "Config loaded. exchange=%s symbols=%s timeframes=%s limit=%s",
        settings.default_exchange,
        settings.default_symbols,
        settings.default_timeframes,
        settings.ohlcv_fetch_limit,
    )
    return settings


@task
def fetch_ohlcv(settings: DataPlatformSettings, run_id: str) -> pd.DataFrame:
    logger = get_run_logger()
    exchange = ccxt.binance({"enableRateLimit": True})
    ingested_at = datetime.now(UTC)
    frames: list[pd.DataFrame] = []

    for symbol in settings.default_symbols:
        for timeframe in settings.default_timeframes:
            ccxt_pair = _ccxt_symbol(symbol)
            logger.info(
                "Fetching OHLCV from Binance. symbol=%s timeframe=%s limit=%s",
                ccxt_pair,
                timeframe,
                settings.ohlcv_fetch_limit,
            )
            rows = exchange.fetch_ohlcv(
                ccxt_pair,
                timeframe=timeframe,
                limit=settings.ohlcv_fetch_limit,
            )
            frame = pd.DataFrame(
                rows,
                columns=["timestamp", "open", "high", "low", "close", "volume"],
            )
            if frame.empty:
                continue
            frame["timestamp"] = pd.to_datetime(frame["timestamp"], unit="ms", utc=True)
            frame["exchange"] = settings.default_exchange
            frame["symbol"] = _safe_symbol(symbol)
            frame["timeframe"] = timeframe
            frame["source"] = "ccxt.binance.fetch_ohlcv"
            frame["run_id"] = run_id
            frame["ingested_at"] = ingested_at
            frame["validated_at"] = pd.NaT
            frame["data_quality_score"] = 0.0
            frames.append(frame[REQUIRED_COLUMNS])

    if not frames:
        return pd.DataFrame(columns=REQUIRED_COLUMNS)

    result = pd.concat(frames, ignore_index=True)
    logger.info("Fetched rows=%s", len(result))
    return result


@task
def validate_ohlcv(df: pd.DataFrame) -> dict[str, object]:
    logger = get_run_logger()
    errors: list[str] = []
    rows_checked = len(df)
    gaps_found = 0
    freshness_lag_seconds = None
    freshness_detail: dict[str, dict[str, object]] = {}
    gap_detail: list[dict[str, object]] = []

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        errors.append(f"missing_columns={missing_columns}")

    if df.empty:
        errors.append("empty_dataset")

    if not missing_columns and not df.empty:
        if df["timestamp"].isna().any():
            errors.append("timestamp_nulls")
        if df[["open", "high", "low", "close"]].isna().any().any():
            errors.append("ohlc_nulls")
        if (df["high"] < df["low"]).any():
            errors.append("high_lt_low")
        if (df["high"] < df["open"]).any():
            errors.append("high_lt_open")
        if (df["high"] < df["close"]).any():
            errors.append("high_lt_close")
        if (df["low"] > df["open"]).any():
            errors.append("low_gt_open")
        if (df["low"] > df["close"]).any():
            errors.append("low_gt_close")
        if (df["volume"] < 0).any():
            errors.append("volume_negative")
        duplicate_count = df.duplicated(
            subset=["exchange", "symbol", "timeframe", "timestamp"]
        ).sum()
        if duplicate_count:
            errors.append(f"duplicate_bars={int(duplicate_count)}")

        now_utc = pd.Timestamp.now(tz=UTC)
        max_freshness_lag_seconds = 0

        for (exchange, symbol, timeframe), group in df.groupby(
            ["exchange", "symbol", "timeframe"]
        ):
            ordered = group.sort_values("timestamp")
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
                errors.append(f"unsupported_timeframe={timeframe}")
                continue

            deltas = ordered["timestamp"].diff()
            gap_deltas = deltas[deltas > expected_interval]
            if not gap_deltas.empty:
                gaps_found += int(len(gap_deltas))
                gap_detail.append(
                    {
                        "exchange": str(exchange),
                        "symbol": str(symbol),
                        "timeframe": str(timeframe),
                        "gaps_found": int(len(gap_deltas)),
                        "expected_interval_seconds": int(expected_interval.total_seconds()),
                    }
                )

        freshness_lag_seconds = max_freshness_lag_seconds
        if gaps_found:
            errors.append(f"gaps_found={gaps_found}")

    is_valid = not errors
    rows_failed = rows_checked if errors else 0
    quality_score = 1.0 if is_valid else 0.0
    logger.info(
        "Validation completed. valid=%s rows_checked=%s gaps_found=%s freshness_lag_seconds=%s errors=%s",
        is_valid,
        rows_checked,
        gaps_found,
        freshness_lag_seconds,
        errors,
    )
    logger.info("Freshness detail: %s", freshness_detail)
    logger.info("Gap detail: %s", gap_detail)
    logger.info("Quality check status=%s", "passed" if is_valid else "failed")
    return {
        "is_valid": is_valid,
        "rows_checked": rows_checked,
        "rows_failed": rows_failed,
        "gaps_found": gaps_found,
        "freshness_lag_seconds": freshness_lag_seconds,
        "data_quality_score": quality_score,
        "errors": errors,
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
    upsert_result: dict[str, int] | None = None,
) -> None:
    symbols = list(settings.default_symbols)
    timeframes = list(settings.default_timeframes)
    metadata = json.dumps(
        {
            "raw_paths": raw_paths,
            "curated_paths": curated_paths,
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
) -> None:
    status = "passed" if validation_result["is_valid"] else "failed"
    error_message = None
    if validation_result["errors"]:
        error_message = "; ".join(validation_result["errors"])

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
                            "errors": validation_result["errors"],
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
    df = fetch_ohlcv(settings, run_id)
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
        )
        write_quality_report(settings, run_id, validation_result)
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
    )
    rows_inserted = upsert_postgres(settings, curated_df)
    write_ingestion_run(
        settings=settings,
        run_id=run_id,
        started_at=started_at,
        status="success",
        rows_fetched=len(df),
        rows_validated=len(curated_df),
        rows_inserted=rows_inserted["rows_inserted_or_updated"],
        raw_paths=raw_paths,
        curated_paths=curated_paths,
        error_message=None,
        upsert_result=rows_inserted,
    )
    write_quality_report(settings, run_id, validation_result)

    return {
        "run_id": run_id,
        "rows_fetched": len(df),
        "rows_validated": len(curated_df),
        "rows_inserted": rows_inserted["rows_inserted_or_updated"],
        "rows_new": rows_inserted["rows_new"],
        "rows_existing": rows_inserted["rows_existing"],
        "raw_files": raw_paths,
        "curated_files": curated_paths,
    }


if __name__ == "__main__":
    print("This flow will fetch public Binance OHLCV for BTCUSDT and ETHUSDT.")
    print("Configured timeframes: 1d and 4h unless overridden in .env.")
    print("Default limit: 500 candles per symbol/timeframe unless overridden in .env.")
    print("It will write Parquet files under data/raw and data/curated, then upsert PostgreSQL.")
    ingest_ohlcv_flow()
