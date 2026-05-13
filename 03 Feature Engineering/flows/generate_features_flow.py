"""Mock Prefect flow for 03 Feature Engineering.

This file defines the intended orchestration shape only. It does not connect to
PostgreSQL, calculate real features, write Parquet, or upsert rows.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

try:
    from prefect import flow, task
except ImportError:

    def task(func=None, **_kwargs):
        def decorator(inner):
            return inner

        return decorator(func) if func is not None else decorator

    def flow(func=None, **_kwargs):
        def decorator(inner):
            return inner

        return decorator(func) if func is not None else decorator


FEATURE_SET = "technical_v1"
FEATURE_VERSION = "1.0.0"


@task
def load_feature_config() -> dict[str, Any]:
    return {
        "run_id": str(uuid4()),
        "flow_name": "generate_features_flow",
        "feature_set": FEATURE_SET,
        "feature_version": FEATURE_VERSION,
        "symbols": ["BTCUSDT", "ETHUSDT"],
        "timeframes": ["1d", "4h"],
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "mock_noop",
    }


@task
def check_ohlcv_freshness_mock(config: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": config["run_id"],
        "check_name": "check_ohlcv_freshness_mock",
        "check_status": "passed",
        "severity": "info",
        "message": "Mock freshness check only. No PostgreSQL query executed.",
    }


@task
def load_ohlcv_data_mock(config: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": config["run_id"],
        "rows_loaded": 0,
        "symbols": config["symbols"],
        "timeframes": config["timeframes"],
        "message": "Mock OHLCV load only. No data read.",
    }


@task
def calculate_features_mock(ohlcv_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": ohlcv_payload["run_id"],
        "rows_generated": 0,
        "feature_columns": [
            "simple_return",
            "log_return",
            "close_open_return",
            "rolling_std_20",
            "volatility_20",
            "atr_14",
            "sma_20",
            "sma_50",
            "ema_20",
            "ema_50",
            "price_above_sma20",
            "sma20_slope",
            "ema20_above_ema50",
            "rsi_14",
            "macd",
            "macd_signal",
            "close_vs_high_52w",
            "rolling_max_20",
            "rolling_min_20",
            "volume_change",
            "volume_sma_20",
            "volume_ratio_20",
            "high_low_range",
            "body_size",
            "upper_wick",
            "lower_wick",
            "body_to_range_ratio",
        ],
        "message": "Mock feature calculation only. No indicators calculated.",
    }


@task
def validate_features_mock(features_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "run_id": features_payload["run_id"],
        "rows_validated": 0,
        "data_quality_score": 1.0,
        "checks": [
            "no_duplicates",
            "no_infinities",
            "required_fields_present",
            "warmup_nulls_only",
            "no_lookahead",
        ],
        "message": "Mock validation only. No feature rows inspected.",
    }


@task
def save_features_parquet_mock(
    config: dict[str, Any], validation_payload: dict[str, Any]
) -> dict[str, Any]:
    return {
        "run_id": config["run_id"],
        "rows_saved": 0,
        "target_root": "data/features/technical/",
        "data_quality_score": validation_payload["data_quality_score"],
        "message": "Mock Parquet save only. No files written.",
    }


@task
def upsert_features_postgres_mock(
    config: dict[str, Any], validation_payload: dict[str, Any]
) -> dict[str, Any]:
    return {
        "run_id": config["run_id"],
        "rows_inserted": 0,
        "target_table": "public.ohlcv_features",
        "data_quality_score": validation_payload["data_quality_score"],
        "message": "Mock PostgreSQL upsert only. No database connection opened.",
    }


@task
def write_feature_run_mock(
    config: dict[str, Any],
    ohlcv_payload: dict[str, Any],
    features_payload: dict[str, Any],
    validation_payload: dict[str, Any],
    upsert_payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "run_id": config["run_id"],
        "flow_name": config["flow_name"],
        "status": "mock_success",
        "feature_set": config["feature_set"],
        "feature_version": config["feature_version"],
        "rows_loaded": ohlcv_payload["rows_loaded"],
        "rows_generated": features_payload["rows_generated"],
        "rows_validated": validation_payload["rows_validated"],
        "rows_inserted": upsert_payload["rows_inserted"],
        "message": "Mock feature run record only. No audit row written.",
    }


@task
def write_feature_quality_report_mock(
    config: dict[str, Any], validation_payload: dict[str, Any]
) -> dict[str, Any]:
    return {
        "run_id": config["run_id"],
        "feature_set": config["feature_set"],
        "feature_version": config["feature_version"],
        "data_quality_score": validation_payload["data_quality_score"],
        "checks": validation_payload["checks"],
        "message": "Mock quality report only. No report file written.",
    }


@flow(name="generate_features_flow")
def generate_features_flow() -> dict[str, Any]:
    config = load_feature_config()
    freshness = check_ohlcv_freshness_mock(config)
    ohlcv_payload = load_ohlcv_data_mock(config)
    features_payload = calculate_features_mock(ohlcv_payload)
    validation_payload = validate_features_mock(features_payload)
    parquet_payload = save_features_parquet_mock(config, validation_payload)
    upsert_payload = upsert_features_postgres_mock(config, validation_payload)
    run_payload = write_feature_run_mock(
        config,
        ohlcv_payload,
        features_payload,
        validation_payload,
        upsert_payload,
    )
    quality_payload = write_feature_quality_report_mock(config, validation_payload)

    return {
        "config": config,
        "freshness": freshness,
        "parquet": parquet_payload,
        "upsert": upsert_payload,
        "run": run_payload,
        "quality": quality_payload,
    }


if __name__ == "__main__":
    result = generate_features_flow()
    print(result)
