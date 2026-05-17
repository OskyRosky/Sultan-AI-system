"""Storage contract for technical_v1 feature datasets."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

import pandas as pd

from config import FEATURE_SET, FEATURE_VERSION
from feature_quality import (
    BREAKOUT_CONTEXT_FEATURE_COLUMNS,
    CANDLE_STRUCTURE_FEATURE_COLUMNS,
    FORBIDDEN_COLUMNS,
    MOMENTUM_FEATURE_COLUMNS,
    RETURN_FEATURE_COLUMNS,
    TREND_FEATURE_COLUMNS,
    VOLATILITY_FEATURE_COLUMNS,
    VOLUME_FEATURE_COLUMNS,
)


STORAGE_IDENTITY_COLUMNS = [
    "exchange",
    "symbol",
    "timeframe",
    "timestamp",
    "feature_set",
    "feature_version",
    "run_id",
]

STORAGE_METADATA_COLUMNS = [
    "created_at",
    "validated_at",
    "data_quality_score",
]

STORAGE_FEATURE_COLUMNS = (
    RETURN_FEATURE_COLUMNS
    + TREND_FEATURE_COLUMNS
    + VOLATILITY_FEATURE_COLUMNS
    + MOMENTUM_FEATURE_COLUMNS
    + BREAKOUT_CONTEXT_FEATURE_COLUMNS
    + VOLUME_FEATURE_COLUMNS
    + CANDLE_STRUCTURE_FEATURE_COLUMNS
)

STORAGE_COLUMNS = (
    STORAGE_IDENTITY_COLUMNS + STORAGE_METADATA_COLUMNS + STORAGE_FEATURE_COLUMNS
)

RAW_OHLCV_COLUMNS_EXCLUDED_FROM_FEATURE_STORAGE = [
    "open",
    "high",
    "low",
    "close",
    "volume",
]


def get_storage_columns() -> list[str]:
    return list(STORAGE_COLUMNS)


def get_raw_ohlcv_columns_excluded_from_storage() -> list[str]:
    return list(RAW_OHLCV_COLUMNS_EXCLUDED_FROM_FEATURE_STORAGE)


def validate_storage_contract_columns(df: pd.DataFrame) -> dict[str, Any]:
    """Validate the narrow storage contract without running full feature quality."""

    errors: list[str] = []
    warnings: list[str] = []
    missing_columns = [column for column in STORAGE_COLUMNS if column not in df.columns]
    raw_ohlcv_columns = [
        column
        for column in RAW_OHLCV_COLUMNS_EXCLUDED_FROM_FEATURE_STORAGE
        if column in df.columns
    ]
    forbidden_columns = [column for column in FORBIDDEN_COLUMNS if column in df.columns]
    unexpected_columns = sorted(set(df.columns) - set(STORAGE_COLUMNS))

    if missing_columns:
        errors.append(f"missing_storage_columns={missing_columns}")
    if raw_ohlcv_columns:
        errors.append(f"raw_ohlcv_columns_present={raw_ohlcv_columns}")
    if forbidden_columns:
        errors.append(f"forbidden_columns={forbidden_columns}")
    non_blocking_unexpected = sorted(
        set(unexpected_columns) - set(raw_ohlcv_columns) - set(forbidden_columns)
    )
    if non_blocking_unexpected:
        warnings.append(f"unexpected_columns={non_blocking_unexpected}")

    return {
        "status": "passed" if not errors else "failed",
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
    }


def prepare_features_for_storage(
    features_df: pd.DataFrame,
    run_id: str | UUID,
    integrated_quality_result: dict[str, Any],
    validated_at: datetime | None = None,
    created_at: datetime | None = None,
) -> pd.DataFrame:
    """Convert a validated preview feature DataFrame into the storage schema."""

    if not integrated_quality_result.get("ready_for_storage"):
        raise ValueError("integrated_quality_result_not_ready_for_storage")
    if "data_quality_score" not in integrated_quality_result:
        raise ValueError("missing_data_quality_score_in_integrated_quality_result")

    missing_preview_columns = [
        column
        for column in STORAGE_COLUMNS
        if column not in {"run_id", "created_at", "validated_at", "data_quality_score"}
        and column not in features_df.columns
    ]
    if missing_preview_columns:
        raise ValueError(f"missing_required_storage_source_columns={missing_preview_columns}")

    working = features_df.copy()
    _validate_catalog_identity(working)

    timestamp = pd.to_datetime(working["timestamp"], utc=True, errors="coerce")
    if timestamp.isna().any():
        raise ValueError("timestamp_invalid_for_storage")

    now = datetime.now(timezone.utc)
    working["timestamp"] = timestamp
    working["run_id"] = str(run_id)
    working["created_at"] = _as_utc_timestamp(created_at or now)
    working["validated_at"] = _as_utc_timestamp(validated_at or now)
    working["data_quality_score"] = float(
        integrated_quality_result["data_quality_score"]
    )

    storage_df = working.loc[:, STORAGE_COLUMNS].copy()
    contract_result = validate_storage_contract_columns(storage_df)
    if not contract_result["passed"]:
        raise ValueError(f"storage_contract_failed={contract_result['errors']}")

    return storage_df


def _validate_catalog_identity(df: pd.DataFrame) -> None:
    invalid_feature_set = df["feature_set"].dropna().ne(FEATURE_SET)
    if invalid_feature_set.any() or df["feature_set"].isna().any():
        raise ValueError(f"invalid_feature_set_expected_{FEATURE_SET}")

    invalid_feature_version = df["feature_version"].dropna().ne(FEATURE_VERSION)
    if invalid_feature_version.any() or df["feature_version"].isna().any():
        raise ValueError(f"invalid_feature_version_expected_{FEATURE_VERSION}")


def _as_utc_timestamp(value: datetime) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tzinfo is None:
        return timestamp.tz_localize("UTC")
    return timestamp.tz_convert("UTC")
