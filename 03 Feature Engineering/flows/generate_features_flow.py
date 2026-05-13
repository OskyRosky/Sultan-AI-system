"""Preview flow for 03 Feature Engineering read-only OHLCV readiness.

Default execution is safe: read_from_db=False uses mock OHLCV rows. Setting
read_from_db=True performs SELECT-only reads and freshness checks.
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import pandas as pd

FEATURE_ENGINEERING_DIR = Path(__file__).resolve().parents[1]
FEATURES_DIR = FEATURE_ENGINEERING_DIR / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from config import (  # noqa: E402
    DEFAULT_SYMBOLS,
    DEFAULT_TIMEFRAMES,
    FEATURE_SET,
    FEATURE_VERSION,
    load_feature_settings,
)
from freshness_gate import evaluate_freshness_timestamp, check_ohlcv_freshness as db_freshness_gate  # noqa: E402
from ohlcv_loader import load_ohlcv_batch_read_only  # noqa: E402
from ohlcv_validation import validate_ohlcv_dataframe  # noqa: E402

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


@task
def load_feature_config(read_from_db: bool = False, limit: int = 1000) -> dict[str, Any]:
    settings = load_feature_settings()
    return {
        "run_id": str(uuid4()),
        "flow_name": "generate_features_flow",
        "feature_set": FEATURE_SET,
        "feature_version": FEATURE_VERSION,
        "symbols": list(settings.default_symbols or DEFAULT_SYMBOLS),
        "timeframes": list(settings.default_timeframes or DEFAULT_TIMEFRAMES),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "read_only_preview",
        "read_from_db": read_from_db,
        "limit": limit,
        "ohlcv_table": settings.ohlcv_table,
    }


@task
def check_ohlcv_freshness(config: dict[str, Any]) -> list[dict[str, Any]]:
    if config["read_from_db"]:
        return [
            db_freshness_gate(symbol=symbol, timeframe=timeframe).to_dict()
            for symbol in config["symbols"]
            for timeframe in config["timeframes"]
        ]

    mock_now = pd.Timestamp.now(tz="UTC")
    return [
        evaluate_freshness_timestamp(
            symbol=symbol,
            timeframe=timeframe,
            latest_timestamp=mock_now,
            current_time=mock_now,
        ).to_dict()
        for symbol in config["symbols"]
        for timeframe in config["timeframes"]
    ]


@task
def load_ohlcv_data_read_only(config: dict[str, Any]) -> pd.DataFrame:
    if config["read_from_db"]:
        return load_ohlcv_batch_read_only(
            symbols=config["symbols"],
            timeframes=config["timeframes"],
            limit=config["limit"],
        )
    return _build_mock_ohlcv_dataframe(config)


@task
def validate_ohlcv_data(df: pd.DataFrame) -> dict[str, Any]:
    return validate_ohlcv_dataframe(df).to_dict()


@task
def summarize_ohlcv_for_feature_readiness(
    df: pd.DataFrame,
    validation_result: dict[str, Any],
    freshness_results: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "rows_loaded": int(len(df)),
        "symbols": sorted(df["symbol"].dropna().unique().tolist()) if not df.empty else [],
        "timeframes": sorted(df["timeframe"].dropna().unique().tolist())
        if not df.empty
        else [],
        "validation_passed": validation_result["passed"],
        "freshness_passed": all(item["passed"] for item in freshness_results),
        "ready_for_future_feature_calculation": validation_result["passed"]
        and all(item["passed"] for item in freshness_results),
        "note": "Readiness summary only. No real features calculated.",
    }


@task
def stop_before_feature_calculation(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "stopped_before_feature_calculation",
        "features_calculated": False,
        "parquet_written": False,
        "postgres_inserted": False,
        "summary": summary,
    }


@flow(name="generate_features_flow")
def generate_features_flow(
    read_from_db: bool = False,
    limit: int = 1000,
) -> dict[str, Any]:
    config = load_feature_config(read_from_db=read_from_db, limit=limit)
    freshness_results = check_ohlcv_freshness(config)
    ohlcv_df = load_ohlcv_data_read_only(config)
    validation_result = validate_ohlcv_data(ohlcv_df)
    summary = summarize_ohlcv_for_feature_readiness(
        ohlcv_df,
        validation_result,
        freshness_results,
    )
    stop_result = stop_before_feature_calculation(summary)

    return {
        "config": config,
        "freshness": freshness_results,
        "validation": validation_result,
        "summary": summary,
        "stop": stop_result,
    }


def _build_mock_ohlcv_dataframe(config: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    base_timestamp = pd.Timestamp.now(tz="UTC").floor("h")
    for symbol in config["symbols"]:
        for timeframe in config["timeframes"]:
            rows.append(
                {
                    "exchange": "binance",
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "timestamp": base_timestamp,
                    "open": 100.0,
                    "high": 101.0,
                    "low": 99.0,
                    "close": 100.5,
                    "volume": 10.0,
                }
            )
    return pd.DataFrame(rows).sort_values(["symbol", "timeframe", "timestamp"])


if __name__ == "__main__":
    result = generate_features_flow(read_from_db=False, limit=1000)
    print(result)
