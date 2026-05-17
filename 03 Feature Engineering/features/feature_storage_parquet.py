"""Local Parquet writer for prepared technical_v1 feature storage datasets."""

from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import UUID

import pandas as pd

from feature_storage_contract import (
    RAW_OHLCV_COLUMNS_EXCLUDED_FROM_FEATURE_STORAGE,
    validate_storage_contract_columns,
)


def build_feature_parquet_path(
    base_dir: Path,
    feature_set: str,
    feature_version: str,
    symbol: str,
    timeframe: str,
    run_id: str | UUID,
) -> Path:
    return (
        Path(base_dir)
        / feature_set
        / feature_version
        / symbol
        / timeframe
        / f"features_{run_id}.parquet"
    )


def write_features_parquet(
    storage_df: pd.DataFrame,
    base_dir: Path,
    run_id: str | UUID,
) -> list[Path]:
    """Write one Parquet file per symbol/timeframe for a prepared storage DataFrame."""

    if storage_df.empty:
        return []

    raw_columns = [
        column
        for column in RAW_OHLCV_COLUMNS_EXCLUDED_FROM_FEATURE_STORAGE
        if column in storage_df.columns
    ]
    if raw_columns:
        raise ValueError(f"raw_ohlcv_columns_present={raw_columns}")

    contract_result = validate_storage_contract_columns(storage_df)
    if not contract_result["passed"]:
        raise ValueError(f"storage_contract_failed={contract_result['errors']}")

    written_paths: list[Path] = []
    for (symbol, timeframe), group in storage_df.groupby(
        ["symbol", "timeframe"], sort=True
    ):
        feature_sets = group["feature_set"].dropna().unique()
        feature_versions = group["feature_version"].dropna().unique()
        if len(feature_sets) != 1 or len(feature_versions) != 1:
            raise ValueError("mixed_feature_set_or_version_in_parquet_group")

        output_path = build_feature_parquet_path(
            base_dir=Path(base_dir),
            feature_set=str(feature_sets[0]),
            feature_version=str(feature_versions[0]),
            symbol=str(symbol),
            timeframe=str(timeframe),
            run_id=run_id,
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        _to_parquet_with_snappy_fallback(group, output_path)
        written_paths.append(output_path)

    return written_paths


def _to_parquet_with_snappy_fallback(df: pd.DataFrame, output_path: Path) -> None:
    try:
        df.to_parquet(output_path, index=False, compression="snappy")
    except Exception as exc:
        if not _looks_like_snappy_unavailable(exc):
            raise
        df.to_parquet(output_path, index=False)


def _looks_like_snappy_unavailable(exc: Exception) -> bool:
    message = str(exc).lower()
    return "snappy" in message or ("codec" in message and "compression" in message)
