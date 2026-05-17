"""Integrated cross-family quality checks for technical_v1 feature previews."""

from __future__ import annotations

import ast
from typing import Any, Callable

import numpy as np
import pandas as pd

from config import FEATURE_SET, FEATURE_VERSION
from feature_quality import (
    BREAKOUT_CONTEXT_FEATURE_COLUMNS,
    CANDLE_STRUCTURE_FEATURE_COLUMNS,
    FEATURE_KEY_COLUMNS,
    FORBIDDEN_COLUMNS,
    MOMENTUM_FEATURE_COLUMNS,
    RETURN_FEATURE_COLUMNS,
    TREND_FEATURE_COLUMNS,
    VOLATILITY_FEATURE_COLUMNS,
    VOLUME_FEATURE_COLUMNS,
    validate_breakout_context_features,
    validate_candle_structure_features,
    validate_momentum_features,
    validate_return_features,
    validate_trend_features,
    validate_volatility_features,
    validate_volume_features,
)


BASE_METADATA_COLUMNS = [
    "exchange",
    "symbol",
    "timeframe",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "feature_set",
    "feature_version",
]

EXPECTED_FEATURE_COLUMNS_BY_FAMILY = {
    "returns": RETURN_FEATURE_COLUMNS,
    "trend": TREND_FEATURE_COLUMNS,
    "volatility": VOLATILITY_FEATURE_COLUMNS,
    "momentum": MOMENTUM_FEATURE_COLUMNS,
    "breakout_context": BREAKOUT_CONTEXT_FEATURE_COLUMNS,
    "volume": VOLUME_FEATURE_COLUMNS,
    "candle_structure": CANDLE_STRUCTURE_FEATURE_COLUMNS,
}

EXPECTED_FEATURE_COLUMNS = [
    column
    for family_columns in EXPECTED_FEATURE_COLUMNS_BY_FAMILY.values()
    for column in family_columns
]

EXPECTED_COLUMNS = BASE_METADATA_COLUMNS + EXPECTED_FEATURE_COLUMNS

STRUCTURAL_WARMUP_ALL_NULL_COLUMNS = {
    "simple_return",
    "log_return",
    "sma_20",
    "sma_50",
    "price_above_sma20",
    "sma20_slope",
    "rolling_std_20",
    "volatility_20",
    "atr_14",
    "rsi_14",
    "close_vs_high_52w",
    "rolling_max_20",
    "rolling_min_20",
    "volume_change",
    "volume_sma_20",
    "volume_ratio_20",
}

STRUCTURAL_WARMUP_WARNING_PREFIXES = (
    "trend_warmup_rows=",
    "volatility_warmup_rows=",
    "momentum_warmup_rows=",
    "breakout_context_warmup_rows=",
    "volume_warmup_rows=",
)

FAMILY_VALIDATORS: dict[str, Callable[[pd.DataFrame], dict[str, Any]]] = {
    "returns": validate_return_features,
    "trend": validate_trend_features,
    "volatility": validate_volatility_features,
    "momentum": validate_momentum_features,
    "breakout_context": validate_breakout_context_features,
    "volume": validate_volume_features,
    "candle_structure": validate_candle_structure_features,
}


def validate_integrated_feature_dataset(df: pd.DataFrame) -> dict[str, Any]:
    """Validate the complete technical_v1 feature dataset before storage."""

    blocking_errors: list[str] = []
    warnings: list[str] = []
    rows_checked = int(len(df))

    if df.empty:
        blocking_errors.append("empty_feature_dataset")

    missing_columns = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    if missing_columns:
        blocking_errors.append(f"missing_expected_columns={missing_columns}")

    forbidden_columns_found = [column for column in FORBIDDEN_COLUMNS if column in df.columns]
    if forbidden_columns_found:
        blocking_errors.append(f"forbidden_columns={forbidden_columns_found}")

    unexpected_columns = sorted(
        set(df.columns) - set(EXPECTED_COLUMNS) - set(FORBIDDEN_COLUMNS)
    )
    if unexpected_columns:
        warnings.append(f"unexpected_columns={unexpected_columns}")

    working = df.copy()
    _validate_metadata(working, blocking_errors)
    _validate_identity(working, blocking_errors)

    duplicate_count = _duplicate_count(working)
    if duplicate_count:
        blocking_errors.append(f"duplicate_feature_rows={duplicate_count}")

    infinite_count = _infinite_count(working)
    if infinite_count:
        blocking_errors.append(f"infinite_feature_values={infinite_count}")

    null_counts_by_family = _null_counts_by_family(working)
    _add_null_warnings(null_counts_by_family, rows_checked, warnings)

    family_summary = _family_summary(working)
    for family_name, family_result in family_summary.items():
        if not family_result["passed"]:
            blocking_errors.append(
                f"{family_name}_quality_failed={family_result['errors']}"
            )

    symbol_timeframe_summary = _symbol_timeframe_summary(working)
    data_quality_score = _calculate_data_quality_score(
        blocking_errors=blocking_errors,
        warnings=warnings,
        missing_columns=missing_columns,
        duplicate_count=duplicate_count,
        infinite_count=infinite_count,
    )

    status = "passed" if not blocking_errors else "failed"
    ready_for_storage = (
        status == "passed"
        and not missing_columns
        and not forbidden_columns_found
        and duplicate_count == 0
        and infinite_count == 0
    )

    return {
        "status": status,
        "ready_for_storage": ready_for_storage,
        "data_quality_score": data_quality_score,
        "rows_checked": rows_checked,
        "blocking_errors": blocking_errors,
        "warnings": warnings,
        "expected_columns": EXPECTED_COLUMNS,
        "missing_columns": missing_columns,
        "unexpected_columns": unexpected_columns,
        "forbidden_columns_found": forbidden_columns_found,
        "duplicate_count": duplicate_count,
        "infinite_count": infinite_count,
        "null_counts_by_family": null_counts_by_family,
        "family_summary": family_summary,
        "symbol_timeframe_summary": symbol_timeframe_summary,
    }


def _validate_metadata(df: pd.DataFrame, blocking_errors: list[str]) -> None:
    for column in ["feature_set", "feature_version"]:
        if column not in df.columns:
            return
        if df[column].isna().any() or (df[column] == "").any():
            blocking_errors.append(f"{column}_null_or_empty")

    if "feature_set" in df.columns:
        invalid_feature_set = df["feature_set"].dropna().ne(FEATURE_SET)
        if invalid_feature_set.any():
            blocking_errors.append(f"invalid_feature_set_expected_{FEATURE_SET}")

    if "feature_version" in df.columns:
        invalid_feature_version = df["feature_version"].dropna().ne(FEATURE_VERSION)
        if invalid_feature_version.any():
            blocking_errors.append(
                f"invalid_feature_version_expected_{FEATURE_VERSION}"
            )


def _validate_identity(df: pd.DataFrame, blocking_errors: list[str]) -> None:
    for column in ["exchange", "symbol", "timeframe", "timestamp"]:
        if column not in df.columns:
            continue
        if df[column].isna().any() or (df[column] == "").any():
            blocking_errors.append(f"{column}_null_or_empty")

    if "timestamp" in df.columns:
        timestamps = pd.to_datetime(df["timestamp"], utc=True, errors="coerce")
        if timestamps.isna().any():
            blocking_errors.append("timestamp_invalid")


def _duplicate_count(df: pd.DataFrame) -> int:
    if any(column not in df.columns for column in FEATURE_KEY_COLUMNS):
        return 0
    return int(df.duplicated(subset=FEATURE_KEY_COLUMNS).sum())


def _infinite_count(df: pd.DataFrame) -> int:
    infinite_count = 0
    for column in EXPECTED_FEATURE_COLUMNS:
        if column not in df.columns:
            continue
        values = pd.to_numeric(df[column], errors="coerce")
        infinite_count += int(np.isinf(values).sum())
    return infinite_count


def _null_counts_by_family(df: pd.DataFrame) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for family_name, columns in EXPECTED_FEATURE_COLUMNS_BY_FAMILY.items():
        result[family_name] = {}
        for column in columns:
            if column in df.columns:
                result[family_name][column] = int(df[column].isna().sum())
    return result


def _add_null_warnings(
    null_counts_by_family: dict[str, dict[str, int]],
    rows_checked: int,
    warnings: list[str],
) -> None:
    if rows_checked == 0:
        return

    all_null_columns = [
        column
        for family_counts in null_counts_by_family.values()
        for column, null_count in family_counts.items()
        if null_count == rows_checked
    ]
    if all_null_columns:
        warnings.append(f"all_null_feature_columns={all_null_columns}")


def _family_summary(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    summary: dict[str, dict[str, Any]] = {}
    for family_name, validator in FAMILY_VALIDATORS.items():
        result = validator(df)
        summary[family_name] = {
            "status": result["status"],
            "passed": bool(result["passed"]),
            "rows_checked": int(result["rows_checked"]),
            "errors": list(result["errors"]),
            "warnings": list(result["warnings"]),
        }
    return summary


def _symbol_timeframe_summary(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    required_columns = {"symbol", "timeframe", "timestamp"}
    if df.empty or not required_columns.issubset(df.columns):
        return {}

    working = df.copy()
    working["timestamp"] = pd.to_datetime(working["timestamp"], utc=True, errors="coerce")
    feature_columns = [column for column in EXPECTED_FEATURE_COLUMNS if column in df.columns]

    summary: dict[str, dict[str, Any]] = {}
    for (symbol, timeframe), group in working.groupby(["symbol", "timeframe"], sort=True):
        key = f"{symbol}|{timeframe}"
        null_feature_values = (
            int(group[feature_columns].isna().sum().sum()) if feature_columns else 0
        )
        min_timestamp = group["timestamp"].min()
        max_timestamp = group["timestamp"].max()
        summary[key] = {
            "symbol": symbol,
            "timeframe": timeframe,
            "row_count": int(len(group)),
            "min_timestamp": min_timestamp.isoformat() if pd.notna(min_timestamp) else None,
            "max_timestamp": max_timestamp.isoformat() if pd.notna(max_timestamp) else None,
            "null_feature_values": null_feature_values,
        }
    return summary


def _calculate_data_quality_score(
    *,
    blocking_errors: list[str],
    warnings: list[str],
    missing_columns: list[str],
    duplicate_count: int,
    infinite_count: int,
) -> float:
    penalized_warnings = [
        warning for warning in warnings if not _is_structural_warmup_warning(warning)
    ]
    score = 1.0
    score -= min(0.30, 0.03 * len(missing_columns))
    score -= 0.10 if duplicate_count else 0.0
    score -= 0.10 if infinite_count else 0.0
    score -= min(0.30, 0.03 * len(penalized_warnings))
    if blocking_errors:
        score = min(score, 0.50)
    return round(float(max(0.0, min(1.0, score))), 4)


def _is_structural_warmup_warning(warning: str) -> bool:
    if warning.startswith(STRUCTURAL_WARMUP_WARNING_PREFIXES):
        return True

    prefix = "all_null_feature_columns="
    if not warning.startswith(prefix):
        return False

    try:
        columns = ast.literal_eval(warning.removeprefix(prefix))
    except (SyntaxError, ValueError):
        return False

    if not isinstance(columns, list):
        return False

    return bool(columns) and all(
        column in STRUCTURAL_WARMUP_ALL_NULL_COLUMNS for column in columns
    )
