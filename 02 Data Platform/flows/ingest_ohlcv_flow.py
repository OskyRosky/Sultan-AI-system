"""Mock Prefect flow skeleton for future OHLCV ingestion.

This module intentionally performs no external API calls, stores no market data,
and writes nothing to PostgreSQL. It only validates the local orchestration shape.
"""

from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from prefect import flow, get_run_logger, task

from config import DataPlatformSettings, load_settings


@task
def load_config() -> DataPlatformSettings:
    settings = load_settings()
    logger = get_run_logger()
    logger.info("Loaded config for project_root=%s", settings.project_root)
    return settings


@task
def fetch_ohlcv_mock(settings: DataPlatformSettings) -> list[dict[str, object]]:
    logger = get_run_logger()
    logger.info(
        "Mock fetch only. No Binance, CCXT, or external calls. exchange=%s symbols=%s timeframes=%s",
        settings.default_exchange,
        settings.default_symbols,
        settings.default_timeframes,
    )
    return [
        {
            "exchange": settings.default_exchange,
            "symbol": symbol,
            "timeframe": timeframe,
            "rows_fetched": 0,
            "mock": True,
        }
        for symbol in settings.default_symbols
        for timeframe in settings.default_timeframes
    ]


@task
def validate_ohlcv_mock(records: list[dict[str, object]]) -> dict[str, object]:
    logger = get_run_logger()
    logger.info("Mock validation only. records=%s", len(records))
    return {
        "is_valid": True,
        "records_checked": len(records),
        "rows_failed": 0,
        "gaps_found": 0,
        "data_quality_score": 1.0,
    }


@task
def save_raw_parquet_mock(
    settings: DataPlatformSettings,
    records: list[dict[str, object]],
    run_id: str,
) -> str:
    raw_path = settings.raw_data_dir / "binance" / "_mock_no_data_written" / run_id
    get_run_logger().info(
        "Mock raw parquet save skipped. records=%s target_path=%s",
        len(records),
        raw_path,
    )
    return str(raw_path)


@task
def transform_to_curated_mock(records: list[dict[str, object]]) -> list[dict[str, object]]:
    get_run_logger().info("Mock transform to curated. records=%s", len(records))
    return records


@task
def save_curated_parquet_mock(
    settings: DataPlatformSettings,
    records: list[dict[str, object]],
    run_id: str,
) -> str:
    curated_path = settings.curated_data_dir / "ohlcv" / "_mock_no_data_written" / run_id
    get_run_logger().info(
        "Mock curated parquet save skipped. records=%s target_path=%s",
        len(records),
        curated_path,
    )
    return str(curated_path)


@task
def upsert_postgres_mock(records: list[dict[str, object]]) -> int:
    get_run_logger().info(
        "Mock PostgreSQL upsert skipped. No database writes. records=%s",
        len(records),
    )
    return 0


@task
def write_ingestion_run_mock(
    run_id: str,
    raw_path: str,
    curated_path: str,
    rows_inserted: int,
) -> dict[str, object]:
    run_record = {
        "run_id": run_id,
        "flow_name": "ingest_ohlcv_flow",
        "status": "mock_success",
        "raw_path": raw_path,
        "curated_path": curated_path,
        "rows_inserted": rows_inserted,
        "finished_at": datetime.now(UTC).isoformat(),
    }
    get_run_logger().info("Mock ingestion run record prepared: %s", run_record)
    return run_record


@task
def write_quality_report_mock(
    run_id: str,
    validation_result: dict[str, object],
) -> dict[str, object]:
    quality_report = {
        "run_id": run_id,
        "dataset_name": "ohlcv",
        "check_status": "mock_passed",
        **validation_result,
    }
    get_run_logger().info("Mock quality report prepared: %s", quality_report)
    return quality_report


@flow(name="ingest_ohlcv_flow")
def ingest_ohlcv_flow() -> dict[str, object]:
    run_id = str(uuid4())
    settings = load_config()
    records = fetch_ohlcv_mock(settings)
    validation_result = validate_ohlcv_mock(records)
    raw_path = save_raw_parquet_mock(settings, records, run_id)
    curated_records = transform_to_curated_mock(records)
    curated_path = save_curated_parquet_mock(settings, curated_records, run_id)
    rows_inserted = upsert_postgres_mock(curated_records)
    ingestion_run = write_ingestion_run_mock(run_id, raw_path, curated_path, rows_inserted)
    quality_report = write_quality_report_mock(run_id, validation_result)
    return {
        "run_id": run_id,
        "ingestion_run": ingestion_run,
        "quality_report": quality_report,
    }


if __name__ == "__main__":
    ingest_ohlcv_flow()

