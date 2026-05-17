"""Controlled flow for 03 Feature Engineering feature generation.

Default execution is safe: read_from_db=True calculates and validates features,
but enable_storage=False prevents Parquet and PostgreSQL writes.
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
    DATA_FEATURES_DIR,
    DEFAULT_SYMBOLS,
    DEFAULT_TIMEFRAMES,
    FEATURE_SET,
    FEATURE_VERSION,
    build_postgres_dsn,
    load_feature_settings,
)
from freshness_gate import evaluate_freshness_timestamp, check_ohlcv_freshness as db_freshness_gate  # noqa: E402
from feature_quality import (  # noqa: E402
    validate_return_features,
    validate_trend_features,
    validate_volatility_features,
    validate_momentum_features,
    validate_breakout_context_features,
    validate_volume_features,
    validate_candle_structure_features,
)
from ohlcv_loader import load_ohlcv_batch_read_only  # noqa: E402
from ohlcv_validation import validate_ohlcv_dataframe  # noqa: E402
from returns import calculate_return_features  # noqa: E402
from trend import calculate_trend_features  # noqa: E402
from volatility import calculate_volatility_features  # noqa: E402
from momentum import calculate_momentum_features  # noqa: E402
from breakout_context import calculate_breakout_context_features  # noqa: E402
from volume import calculate_volume_features  # noqa: E402
from candle_structure import calculate_candle_structure_features  # noqa: E402
from integrated_feature_quality import validate_integrated_feature_dataset  # noqa: E402
from feature_storage_contract import prepare_features_for_storage  # noqa: E402
from feature_storage_db import build_insert_feature_run_payload, store_features_postgres  # noqa: E402
from feature_storage_parquet import write_features_parquet  # noqa: E402

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
def load_feature_config(
    symbols: list[str] | None = None,
    timeframes: list[str] | None = None,
    limit: int | None = 1000,
    read_from_db: bool = True,
    enable_storage: bool = False,
    enable_parquet: bool = True,
    enable_postgres: bool = True,
    require_freshness: bool = True,
    allow_full_history: bool = False,
) -> dict[str, Any]:
    settings = load_feature_settings()
    selected_symbols = list(symbols or settings.default_symbols or DEFAULT_SYMBOLS)
    selected_timeframes = list(
        timeframes or settings.default_timeframes or DEFAULT_TIMEFRAMES
    )
    _validate_flow_controls(
        read_from_db=read_from_db,
        enable_storage=enable_storage,
        limit=limit,
        allow_full_history=allow_full_history,
    )
    return {
        "run_id": str(uuid4()),
        "flow_name": "generate_features_flow",
        "feature_set": FEATURE_SET,
        "feature_version": FEATURE_VERSION,
        "symbols": selected_symbols,
        "timeframes": selected_timeframes,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "mode": "controlled_storage" if enable_storage else "controlled_preview",
        "read_from_db": read_from_db,
        "limit": limit,
        "enable_storage": enable_storage,
        "enable_parquet": enable_parquet,
        "enable_postgres": enable_postgres,
        "require_freshness": require_freshness,
        "allow_full_history": allow_full_history,
        "ohlcv_table": settings.ohlcv_table,
    }


@task
def check_ohlcv_freshness(config: dict[str, Any]) -> list[dict[str, Any]]:
    if not config["require_freshness"]:
        return []
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
def calculate_returns_features_preview(df: pd.DataFrame) -> pd.DataFrame:
    return calculate_return_features(df)


@task
def validate_returns_features_preview(features_df: pd.DataFrame) -> dict[str, Any]:
    return validate_return_features(features_df)


@task
def calculate_trend_features_preview(features_df: pd.DataFrame) -> pd.DataFrame:
    return calculate_trend_features(features_df)


@task
def validate_trend_features_preview(features_df: pd.DataFrame) -> dict[str, Any]:
    return validate_trend_features(features_df)


@task
def calculate_volatility_features_preview(features_df: pd.DataFrame) -> pd.DataFrame:
    return calculate_volatility_features(features_df)


@task
def validate_volatility_features_preview(features_df: pd.DataFrame) -> dict[str, Any]:
    return validate_volatility_features(features_df)


@task
def calculate_momentum_features_preview(features_df: pd.DataFrame) -> pd.DataFrame:
    return calculate_momentum_features(features_df)


@task
def validate_momentum_features_preview(features_df: pd.DataFrame) -> dict[str, Any]:
    return validate_momentum_features(features_df)


@task
def calculate_breakout_context_features_preview(features_df: pd.DataFrame) -> pd.DataFrame:
    return calculate_breakout_context_features(features_df)


@task
def validate_breakout_context_features_preview(features_df: pd.DataFrame) -> dict[str, Any]:
    return validate_breakout_context_features(features_df)


@task
def calculate_volume_features_preview(features_df: pd.DataFrame) -> pd.DataFrame:
    return calculate_volume_features(features_df)


@task
def validate_volume_features_preview(features_df: pd.DataFrame) -> dict[str, Any]:
    return validate_volume_features(features_df)


@task
def calculate_candle_structure_features_preview(features_df: pd.DataFrame) -> pd.DataFrame:
    return calculate_candle_structure_features(features_df)


@task
def validate_candle_structure_features_preview(features_df: pd.DataFrame) -> dict[str, Any]:
    return validate_candle_structure_features(features_df)


@task
def validate_integrated_feature_dataset_preview(
    features_df: pd.DataFrame,
) -> dict[str, Any]:
    return validate_integrated_feature_dataset(features_df)


@task
def summarize_feature_preview(
    df: pd.DataFrame,
    features_df: pd.DataFrame,
    validation_result: dict[str, Any],
    returns_quality_result: dict[str, Any],
    trend_quality_result: dict[str, Any],
    volatility_quality_result: dict[str, Any],
    momentum_quality_result: dict[str, Any],
    breakout_context_quality_result: dict[str, Any],
    volume_quality_result: dict[str, Any],
    candle_structure_quality_result: dict[str, Any],
    integrated_quality_result: dict[str, Any],
    freshness_results: list[dict[str, Any]],
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    freshness_passed = (
        all(item["passed"] for item in freshness_results)
        if freshness_results
        else True
    )
    return {
        "rows_loaded": int(len(df)),
        "rows_with_return_features": int(len(features_df)),
        "symbols": sorted(df["symbol"].dropna().unique().tolist()) if not df.empty else [],
        "timeframes": sorted(df["timeframe"].dropna().unique().tolist())
        if not df.empty
        else [],
        "validation_passed": validation_result["passed"],
        "returns_quality_passed": returns_quality_result["passed"],
        "trend_quality_passed": trend_quality_result["passed"],
        "volatility_quality_passed": volatility_quality_result["passed"],
        "momentum_quality_passed": momentum_quality_result["passed"],
        "breakout_context_quality_passed": breakout_context_quality_result["passed"],
        "volume_quality_passed": volume_quality_result["passed"],
        "candle_structure_quality_passed": candle_structure_quality_result["passed"],
        "integrated_quality_status": integrated_quality_result["status"],
        "integrated_ready_for_storage": integrated_quality_result[
            "ready_for_storage"
        ],
        "integrated_data_quality_score": integrated_quality_result[
            "data_quality_score"
        ],
        "freshness_passed": freshness_passed,
        "enable_storage": bool(config.get("enable_storage")) if config else False,
        "enable_parquet": bool(config.get("enable_parquet")) if config else False,
        "enable_postgres": bool(config.get("enable_postgres")) if config else False,
        "return_features_calculated": [
            "simple_return",
            "log_return",
            "close_open_return",
        ],
        "trend_features_calculated": [
            "sma_20",
            "sma_50",
            "ema_20",
            "ema_50",
            "price_above_sma20",
            "sma20_slope",
            "ema20_above_ema50",
        ],
        "volatility_features_calculated": [
            "rolling_std_20",
            "volatility_20",
            "atr_14",
        ],
        "momentum_features_calculated": [
            "rsi_14",
            "macd",
            "macd_signal",
        ],
        "breakout_context_features_calculated": [
            "close_vs_high_52w",
            "rolling_max_20",
            "rolling_min_20",
        ],
        "volume_features_calculated": [
            "volume_change",
            "volume_sma_20",
            "volume_ratio_20",
        ],
        "candle_structure_features_calculated": [
            "high_low_range",
            "body_size",
            "upper_wick",
            "lower_wick",
            "body_to_range_ratio",
        ],
        "ready_for_future_persistence": validation_result["passed"]
        and returns_quality_result["passed"]
        and trend_quality_result["passed"]
        and volatility_quality_result["passed"]
        and momentum_quality_result["passed"]
        and breakout_context_quality_result["passed"]
        and volume_quality_result["passed"]
        and candle_structure_quality_result["passed"]
        and integrated_quality_result["ready_for_storage"]
        and freshness_passed,
        "note": (
            "Storage enabled only if requested."
            if config and config.get("enable_storage")
            else "Feature preview only. No Parquet or PostgreSQL persistence executed."
        ),
    }


@task
def stop_before_persistence(summary: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "stopped_before_persistence",
        "features_calculated": True,
        "feature_families": [
            "returns",
            "trend",
            "volatility",
            "momentum",
            "breakout_context",
            "volume",
            "candle_structure",
        ],
        "parquet_written": False,
        "postgres_inserted": False,
        "summary": summary,
    }


@task
def prepare_features_for_storage_task(
    features_df: pd.DataFrame,
    config: dict[str, Any],
    integrated_quality_result: dict[str, Any],
) -> pd.DataFrame:
    return prepare_features_for_storage(
        features_df=features_df,
        run_id=config["run_id"],
        integrated_quality_result=integrated_quality_result,
        validated_at=datetime.now(timezone.utc),
        created_at=datetime.fromisoformat(config["created_at"]),
    )


@task
def write_features_parquet_task(
    storage_df: pd.DataFrame,
    config: dict[str, Any],
) -> list[str]:
    if not config["enable_parquet"]:
        return []
    return [
        str(path)
        for path in write_features_parquet(
            storage_df=storage_df,
            base_dir=DATA_FEATURES_DIR,
            run_id=config["run_id"],
        )
    ]


@task
def store_features_postgres_task(
    storage_df: pd.DataFrame,
    config: dict[str, Any],
    validation_result: dict[str, Any],
    integrated_quality_result: dict[str, Any],
    family_quality_results: dict[str, dict[str, Any]],
    parquet_paths: list[str],
) -> dict[str, Any]:
    if not config["enable_postgres"]:
        return {
            "enabled": False,
            "status": "skipped",
            "rows_inserted": 0,
            "features_upserted": False,
        }

    import psycopg2

    settings = load_feature_settings()
    run_payload = build_insert_feature_run_payload(
        run_id=config["run_id"],
        flow_name=config["flow_name"],
        status="running",
        started_at=datetime.fromisoformat(config["created_at"]),
        feature_set=config["feature_set"],
        feature_version=config["feature_version"],
        symbols=config["symbols"],
        timeframes=config["timeframes"],
        rows_loaded=int(validation_result.get("rows_checked", len(storage_df))),
        rows_generated=len(storage_df),
        rows_validated=len(storage_df),
        rows_inserted=0,
        metadata={
            "limit": config["limit"],
            "allow_full_history": config["allow_full_history"],
            "enable_parquet": config["enable_parquet"],
            "enable_postgres": config["enable_postgres"],
        },
    )
    with psycopg2.connect(build_postgres_dsn(settings.postgres), connect_timeout=5) as conn:
        return store_features_postgres(
            conn=conn,
            storage_df=storage_df,
            run_payload=run_payload,
            integrated_quality_result=integrated_quality_result,
            family_quality_results=family_quality_results,
            parquet_paths=parquet_paths,
        )


@task
def summarize_storage_result(
    config: dict[str, Any],
    storage_df: pd.DataFrame,
    parquet_paths: list[str],
    postgres_result: dict[str, Any],
) -> dict[str, Any]:
    return {
        "enabled": True,
        "run_id": config["run_id"],
        "rows_prepared": int(len(storage_df)),
        "parquet_enabled": config["enable_parquet"],
        "postgres_enabled": config["enable_postgres"],
        "parquet_paths": parquet_paths,
        "postgres": postgres_result,
    }


@flow(name="generate_features_flow")
def generate_features_flow(
    symbols: list[str] | None = None,
    timeframes: list[str] | None = None,
    limit: int | None = 1000,
    read_from_db: bool = True,
    enable_storage: bool = False,
    enable_parquet: bool = True,
    enable_postgres: bool = True,
    require_freshness: bool = True,
    allow_full_history: bool = False,
) -> dict[str, Any]:
    config = load_feature_config(
        symbols=symbols,
        timeframes=timeframes,
        limit=limit,
        read_from_db=read_from_db,
        enable_storage=enable_storage,
        enable_parquet=enable_parquet,
        enable_postgres=enable_postgres,
        require_freshness=require_freshness,
        allow_full_history=allow_full_history,
    )
    freshness_results = check_ohlcv_freshness(config)
    ohlcv_df = load_ohlcv_data_read_only(config)
    validation_result = validate_ohlcv_data(ohlcv_df)
    return_features_df = calculate_returns_features_preview(ohlcv_df)
    returns_quality_result = validate_returns_features_preview(return_features_df)
    trend_features_df = calculate_trend_features_preview(return_features_df)
    trend_quality_result = validate_trend_features_preview(trend_features_df)
    volatility_features_df = calculate_volatility_features_preview(trend_features_df)
    volatility_quality_result = validate_volatility_features_preview(
        volatility_features_df
    )
    momentum_features_df = calculate_momentum_features_preview(volatility_features_df)
    momentum_quality_result = validate_momentum_features_preview(momentum_features_df)
    breakout_context_features_df = calculate_breakout_context_features_preview(
        momentum_features_df
    )
    breakout_context_quality_result = validate_breakout_context_features_preview(
        breakout_context_features_df
    )
    volume_features_df = calculate_volume_features_preview(breakout_context_features_df)
    volume_quality_result = validate_volume_features_preview(volume_features_df)
    candle_structure_features_df = calculate_candle_structure_features_preview(
        volume_features_df
    )
    candle_structure_quality_result = validate_candle_structure_features_preview(
        candle_structure_features_df
    )
    integrated_quality_result = validate_integrated_feature_dataset_preview(
        candle_structure_features_df
    )
    summary = summarize_feature_preview(
        ohlcv_df,
        candle_structure_features_df,
        validation_result,
        returns_quality_result,
        trend_quality_result,
        volatility_quality_result,
        momentum_quality_result,
        breakout_context_quality_result,
        volume_quality_result,
        candle_structure_quality_result,
        integrated_quality_result,
        freshness_results,
        config,
    )
    storage_result: dict[str, Any] | None = None
    stop_result: dict[str, Any] | None = None

    if not config["enable_storage"]:
        stop_result = stop_before_persistence(summary)
    elif not integrated_quality_result["ready_for_storage"]:
        stop_result = {
            "status": "storage_blocked_by_quality_gate",
            "features_calculated": True,
            "parquet_written": False,
            "postgres_inserted": False,
            "summary": summary,
        }
    else:
        storage_df = prepare_features_for_storage_task(
            candle_structure_features_df,
            config,
            integrated_quality_result,
        )
        parquet_paths = write_features_parquet_task(storage_df, config)
        postgres_result = store_features_postgres_task(
            storage_df,
            config,
            validation_result,
            integrated_quality_result,
            {
                "returns": returns_quality_result,
                "trend": trend_quality_result,
                "volatility": volatility_quality_result,
                "momentum": momentum_quality_result,
                "breakout_context": breakout_context_quality_result,
                "volume": volume_quality_result,
                "candle_structure": candle_structure_quality_result,
            },
            parquet_paths,
        )
        storage_result = summarize_storage_result(
            config,
            storage_df,
            parquet_paths,
            postgres_result,
        )

    return {
        "config": config,
        "freshness": freshness_results,
        "validation": validation_result,
        "returns_quality": returns_quality_result,
        "trend_quality": trend_quality_result,
        "volatility_quality": volatility_quality_result,
        "momentum_quality": momentum_quality_result,
        "breakout_context_quality": breakout_context_quality_result,
        "volume_quality": volume_quality_result,
        "candle_structure_quality": candle_structure_quality_result,
        "integrated_quality": integrated_quality_result,
        "summary": summary,
        "stop": stop_result,
        "storage": storage_result,
    }


def _validate_flow_controls(
    *,
    read_from_db: bool,
    enable_storage: bool,
    limit: int | None,
    allow_full_history: bool,
) -> None:
    if limit is None and not allow_full_history:
        raise ValueError("limit_none_requires_allow_full_history_true")
    if enable_storage and not read_from_db:
        raise ValueError("enable_storage_requires_read_from_db_true")


def _build_mock_ohlcv_dataframe(config: dict[str, Any]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    base_timestamp = pd.Timestamp.now(tz="UTC").floor("h")
    for symbol in config["symbols"]:
        for timeframe in config["timeframes"]:
            timeframe_delta = _mock_timeframe_delta(timeframe)
            for offset in range(80):
                open_price = 100.0 + offset
                close = open_price + (0.5 if offset % 2 == 0 else -0.25)
                rows.append(
                    {
                        "exchange": "binance",
                        "symbol": symbol,
                        "timeframe": timeframe,
                        "timestamp": base_timestamp + offset * timeframe_delta,
                        "open": open_price,
                        "high": max(open_price, close) + 1.0,
                        "low": min(open_price, close) - 1.0,
                        "close": close,
                        "volume": 10.0 + offset,
                    }
                )
    return pd.DataFrame(rows).sort_values(["symbol", "timeframe", "timestamp"])


def _mock_timeframe_delta(timeframe: str) -> pd.Timedelta:
    if timeframe == "1d":
        return pd.Timedelta(days=1)
    if timeframe == "4h":
        return pd.Timedelta(hours=4)
    raise ValueError(f"Unsupported mock OHLCV timeframe: {timeframe}")


if __name__ == "__main__":
    result = generate_features_flow(read_from_db=False, limit=1000)
    print(result)
