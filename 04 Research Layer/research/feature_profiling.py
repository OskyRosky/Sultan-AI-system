"""Pure in-memory feature profiling for Research Layer.

This module describes standalone feature behavior. It does not use forward
returns, calculate predictive metrics, create rankings, or interpret alpha.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
import sys

import pandas as pd
from pandas.api.types import is_numeric_dtype

RESEARCH_DIR = Path(__file__).resolve().parent
if str(RESEARCH_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_DIR))

from _common import group_key_values, require_columns, validate_group_by


DEFAULT_KEY_COLUMNS: tuple[str, str, str] = ("symbol", "timeframe", "timestamp")
DEFAULT_GROUP_BY: tuple[str, str] = ("symbol", "timeframe")
DEFAULT_FORWARD_RETURN_PREFIX = "forward_return_"
DEFAULT_REDUNDANCY_THRESHOLD = 0.95
IQR_MULTIPLIER = 1.5


@dataclass(frozen=True)
class FeatureProfileResult:
    """Structured in-memory output for feature profiling."""

    summary: pd.DataFrame
    correlation_matrix: pd.DataFrame
    redundancy: pd.DataFrame


def profile_features(
    features: pd.DataFrame,
    *,
    feature_columns: Sequence[str] | None = None,
    group_by: Sequence[str] = DEFAULT_GROUP_BY,
    key_columns: Sequence[str] = DEFAULT_KEY_COLUMNS,
    forward_return_prefix: str = DEFAULT_FORWARD_RETURN_PREFIX,
    redundancy_threshold: float = DEFAULT_REDUNDANCY_THRESHOLD,
) -> FeatureProfileResult:
    """Profile numeric features in memory and return structured diagnostics."""

    groups = tuple(group_by)
    keys = tuple(key_columns)
    validate_group_by(groups, keys)
    require_columns(features, keys, frame_name="features")
    require_columns(features, groups, frame_name="features")
    _validate_redundancy_threshold(redundancy_threshold)

    selected_features = _select_feature_columns(
        features,
        feature_columns=feature_columns,
        key_columns=keys,
        forward_return_prefix=forward_return_prefix,
    )

    sorted_features = features.copy(deep=True)
    for feature in selected_features:
        sorted_features[feature] = pd.to_numeric(sorted_features[feature])
    sorted_features = sorted_features.sort_values([*groups, "timestamp"], kind="mergesort")
    summary = _build_summary(sorted_features, selected_features, groups)
    correlation_matrix = _build_correlation_matrix(sorted_features, selected_features, groups)
    redundancy = _build_redundancy(correlation_matrix, redundancy_threshold)

    return FeatureProfileResult(
        summary=summary,
        correlation_matrix=correlation_matrix,
        redundancy=redundancy,
    )


def _build_summary(
    frame: pd.DataFrame,
    feature_columns: Sequence[str],
    group_by: Sequence[str],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for group_key, group in frame.groupby(list(group_by), sort=True, dropna=False):
        group_values = group_key_values(group_key, group_by)
        total_rows = len(group)

        for feature in feature_columns:
            series = group[feature]
            non_null = series.dropna()
            null_count = int(series.isna().sum())
            count = int(non_null.count())
            zero_count = int(non_null.eq(0).sum())
            outlier_count = _iqr_outlier_count(non_null)

            rows.append(
                {
                    **group_values,
                    "feature": feature,
                    "count": count,
                    "null_count": null_count,
                    "null_ratio": null_count / total_rows if total_rows else pd.NA,
                    "mean": non_null.mean(),
                    "median": non_null.median(),
                    "std": non_null.std(),
                    "min": non_null.min(),
                    "max": non_null.max(),
                    "skewness": non_null.skew(),
                    "kurtosis": non_null.kurt(),
                    "variance": non_null.var(),
                    "unique_values": int(non_null.nunique(dropna=True)),
                    "zero_ratio": zero_count / count if count else pd.NA,
                    "outlier_count": outlier_count,
                    "outlier_ratio": outlier_count / count if count else pd.NA,
                }
            )

    return pd.DataFrame(rows)


def _build_correlation_matrix(
    frame: pd.DataFrame,
    feature_columns: Sequence[str],
    group_by: Sequence[str],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for group_key, group in frame.groupby(list(group_by), sort=True, dropna=False):
        group_values = group_key_values(group_key, group_by)
        correlations = group.loc[:, list(feature_columns)].corr(method="pearson")

        for feature_x in feature_columns:
            for feature_y in feature_columns:
                correlation = correlations.loc[feature_x, feature_y]
                rows.append(
                    {
                        **group_values,
                        "feature_x": feature_x,
                        "feature_y": feature_y,
                        "correlation": correlation,
                        "abs_correlation": abs(correlation) if pd.notna(correlation) else pd.NA,
                    }
                )

    return pd.DataFrame(rows)


def _build_redundancy(correlation_matrix: pd.DataFrame, threshold: float) -> pd.DataFrame:
    if correlation_matrix.empty:
        return correlation_matrix.copy()

    pair_mask = correlation_matrix["feature_x"] < correlation_matrix["feature_y"]
    threshold_mask = correlation_matrix["abs_correlation"].ge(threshold).fillna(False)
    return correlation_matrix.loc[pair_mask & threshold_mask].reset_index(drop=True)


def _select_feature_columns(
    frame: pd.DataFrame,
    *,
    feature_columns: Sequence[str] | None,
    key_columns: Sequence[str],
    forward_return_prefix: str,
) -> tuple[str, ...]:
    if feature_columns is not None:
        selected = tuple(feature_columns)
        require_columns(frame, selected, frame_name="features")
    else:
        excluded = set(key_columns)
        selected = tuple(
            column
            for column in frame.columns
            if column not in excluded
            and not column.startswith(forward_return_prefix)
            and _is_profileable_numeric(frame[column])
        )

    if not selected:
        raise ValueError("features must contain at least one numeric feature column")

    non_numeric = [column for column in selected if not _is_profileable_numeric(frame[column])]
    if non_numeric:
        raise ValueError(f"feature columns must be numeric: {non_numeric}")

    forward_return_columns = [
        column for column in selected if column.startswith(forward_return_prefix)
    ]
    if forward_return_columns:
        raise ValueError(
            "forward return columns are not valid Feature Profiling inputs: "
            f"{forward_return_columns}"
        )

    return selected


def _iqr_outlier_count(series: pd.Series) -> int:
    if series.empty:
        return 0

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    if pd.isna(iqr) or iqr == 0:
        return 0

    lower_bound = q1 - IQR_MULTIPLIER * iqr
    upper_bound = q3 + IQR_MULTIPLIER * iqr
    return int(series.lt(lower_bound).sum() + series.gt(upper_bound).sum())


def _is_profileable_numeric(series: pd.Series) -> bool:
    return is_numeric_dtype(series) or series.dropna().empty


def _validate_redundancy_threshold(threshold: float) -> None:
    if threshold <= 0 or threshold > 1:
        raise ValueError("redundancy_threshold must be greater than 0 and less than or equal to 1")
