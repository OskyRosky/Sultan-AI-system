"""Manual controlled smoke test for Feature Storage PostgreSQL write path.

This is an operator tool, not a pytest test. It writes real Parquet under
data/features/ and writes real rows to local PostgreSQL. Use it only for a
small smoke test after DDL is ready. It reads existing OHLCV from PostgreSQL
and does not download data, call Binance, or use CCXT.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import psycopg2

FEATURE_ENGINEERING_DIR = Path(__file__).resolve().parents[1]
PROJECT_ROOT = FEATURE_ENGINEERING_DIR.parent
FEATURES_DIR = FEATURE_ENGINEERING_DIR / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from breakout_context import calculate_breakout_context_features  # noqa: E402
from candle_structure import calculate_candle_structure_features  # noqa: E402
from config import DATA_FEATURES_DIR, build_postgres_dsn, load_feature_settings  # noqa: E402
from feature_quality import (  # noqa: E402
    validate_breakout_context_features,
    validate_candle_structure_features,
    validate_momentum_features,
    validate_return_features,
    validate_trend_features,
    validate_volatility_features,
    validate_volume_features,
)
from feature_storage_contract import prepare_features_for_storage  # noqa: E402
from feature_storage_db import (  # noqa: E402
    build_insert_feature_run_payload,
    store_features_postgres,
)
from feature_storage_parquet import write_features_parquet  # noqa: E402
from integrated_feature_quality import validate_integrated_feature_dataset  # noqa: E402
from momentum import calculate_momentum_features  # noqa: E402
from ohlcv_loader import load_ohlcv_batch_read_only  # noqa: E402
from ohlcv_validation import validate_ohlcv_dataframe  # noqa: E402
from returns import calculate_return_features  # noqa: E402
from trend import calculate_trend_features  # noqa: E402
from volatility import calculate_volatility_features  # noqa: E402
from volume import calculate_volume_features  # noqa: E402


SMOKE_SYMBOLS = ["BTCUSDT"]
SMOKE_TIMEFRAMES = ["1d"]
SMOKE_LIMIT = 200


def main() -> None:
    settings = load_feature_settings()
    run_id = str(uuid4())
    started_at = datetime.now(timezone.utc)

    ohlcv_df = load_ohlcv_batch_read_only(
        symbols=SMOKE_SYMBOLS,
        timeframes=SMOKE_TIMEFRAMES,
        limit=SMOKE_LIMIT,
        settings=settings,
    )
    validation_result = validate_ohlcv_dataframe(ohlcv_df).to_dict()
    if not validation_result["passed"]:
        raise RuntimeError(f"ohlcv_validation_failed={validation_result}")

    features_df = calculate_return_features(ohlcv_df)
    returns_quality = validate_return_features(features_df)
    features_df = calculate_trend_features(features_df)
    trend_quality = validate_trend_features(features_df)
    features_df = calculate_volatility_features(features_df)
    volatility_quality = validate_volatility_features(features_df)
    features_df = calculate_momentum_features(features_df)
    momentum_quality = validate_momentum_features(features_df)
    features_df = calculate_breakout_context_features(features_df)
    breakout_quality = validate_breakout_context_features(features_df)
    features_df = calculate_volume_features(features_df)
    volume_quality = validate_volume_features(features_df)
    features_df = calculate_candle_structure_features(features_df)
    candle_quality = validate_candle_structure_features(features_df)
    integrated_quality = validate_integrated_feature_dataset(features_df)

    if not integrated_quality["ready_for_storage"]:
        raise RuntimeError(f"integrated_quality_not_ready={integrated_quality}")

    storage_df = prepare_features_for_storage(
        features_df=features_df,
        run_id=run_id,
        integrated_quality_result=integrated_quality,
        validated_at=datetime.now(timezone.utc),
        created_at=started_at,
    )
    parquet_paths = write_features_parquet(
        storage_df=storage_df,
        base_dir=DATA_FEATURES_DIR,
        run_id=run_id,
    )

    run_payload = build_insert_feature_run_payload(
        run_id=run_id,
        flow_name="smoke_test_feature_storage_postgres",
        status="running",
        started_at=started_at,
        feature_set=settings.feature_set,
        feature_version=settings.feature_version,
        symbols=SMOKE_SYMBOLS,
        timeframes=SMOKE_TIMEFRAMES,
        rows_loaded=len(ohlcv_df),
        rows_generated=len(features_df),
        rows_validated=len(storage_df),
        rows_inserted=0,
        metadata={
            "smoke_test": True,
            "limit": SMOKE_LIMIT,
        },
    )
    family_quality_results = {
        "returns": returns_quality,
        "trend": trend_quality,
        "volatility": volatility_quality,
        "momentum": momentum_quality,
        "breakout_context": breakout_quality,
        "volume": volume_quality,
        "candle_structure": candle_quality,
    }

    with psycopg2.connect(build_postgres_dsn(settings.postgres), connect_timeout=5) as conn:
        summary = store_features_postgres(
            conn=conn,
            storage_df=storage_df,
            run_payload=run_payload,
            integrated_quality_result=integrated_quality,
            family_quality_results=family_quality_results,
            parquet_paths=parquet_paths,
        )

    result = {
        "run_id": run_id,
        "rows_loaded": int(len(ohlcv_df)),
        "rows_generated": int(len(features_df)),
        "rows_validated": int(len(storage_df)),
        "rows_inserted": int(summary["rows_inserted"]),
        "data_quality_score": float(integrated_quality["data_quality_score"]),
        "ready_for_storage": bool(integrated_quality["ready_for_storage"]),
        "parquet_paths": [str(path) for path in parquet_paths],
        "postgres_summary": summary,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
