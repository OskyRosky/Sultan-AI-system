"""Pure in-memory regime analysis for Research Layer.

This module labels simple auditable regimes and evaluates feature
informativeness conditionally by regime. It does not create strategies,
signals, switching logic, forecasts, or economic interpretations.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
import sys

import pandas as pd

RESEARCH_DIR = Path(__file__).resolve().parent
if str(RESEARCH_DIR) not in sys.path:
    sys.path.insert(0, str(RESEARCH_DIR))

from _common import (
    group_key_values,
    is_numeric_or_all_null,
    require_columns,
    safe_correlation,
    validate_group_by,
)


DEFAULT_GROUP_BY: tuple[str, str] = ("symbol", "timeframe")
DEFAULT_KEY_COLUMNS: tuple[str, str, str] = ("symbol", "timeframe", "timestamp")
DEFAULT_FORWARD_RETURN_PREFIX = "forward_return_"

REGIME_LABELS: dict[str, tuple[str, ...]] = {
    "trend": ("bearish", "neutral", "bullish"),
    "volatility": ("low_vol", "medium_vol", "high_vol"),
    "momentum": ("negative", "flat", "positive"),
    "range": ("compressed", "expanded"),
}


@dataclass(frozen=True)
class RegimeAnalysisResult:
    """Structured in-memory output for regime analysis."""

    labeled_data: pd.DataFrame
    regime_metrics: pd.DataFrame
    regime_counts: pd.DataFrame


def analyze_regimes(
    research_dataset: pd.DataFrame,
    *,
    feature_columns: Sequence[str] | None = None,
    forward_return_columns: Sequence[str] | None = None,
    trend_column: str | None = None,
    volatility_column: str | None = None,
    momentum_column: str | None = None,
    range_column: str | None = None,
    group_by: Sequence[str] = DEFAULT_GROUP_BY,
    key_columns: Sequence[str] = DEFAULT_KEY_COLUMNS,
    forward_return_prefix: str = DEFAULT_FORWARD_RETURN_PREFIX,
    positive_threshold: float = 0.0,
    negative_threshold: float = 0.0,
) -> RegimeAnalysisResult:
    """Label regimes and calculate conditional informativeness metrics."""

    groups = tuple(group_by)
    keys = tuple(key_columns)
    validate_group_by(groups, keys)
    require_columns(research_dataset, keys, frame_name="research_dataset")
    require_columns(research_dataset, groups, frame_name="research_dataset")
    _validate_thresholds(positive_threshold, negative_threshold)

    context_columns = _context_columns(
        trend_column=trend_column,
        volatility_column=volatility_column,
        momentum_column=momentum_column,
        range_column=range_column,
    )
    if not context_columns:
        raise ValueError("at least one regime context column is required")
    require_columns(research_dataset, tuple(context_columns.values()), frame_name="research_dataset")

    selected_features = _select_feature_columns(
        research_dataset,
        columns=feature_columns,
        excluded_columns=(*keys, *groups, *context_columns.values()),
        forward_return_prefix=forward_return_prefix,
    )
    _reject_feature_context_overlap(selected_features, context_columns.values())
    selected_returns = _select_forward_return_columns(
        research_dataset,
        columns=forward_return_columns,
        forward_return_prefix=forward_return_prefix,
    )

    frame = research_dataset.copy(deep=True)
    for column in (*selected_features, *selected_returns, *context_columns.values()):
        frame[column] = pd.to_numeric(frame[column])
    frame = frame.sort_values([*groups, *[key for key in keys if key not in groups]], kind="mergesort")

    labeled_data = add_regime_labels(
        frame,
        trend_column=trend_column,
        volatility_column=volatility_column,
        momentum_column=momentum_column,
        range_column=range_column,
        group_by=groups,
        key_columns=keys,
        positive_threshold=positive_threshold,
        negative_threshold=negative_threshold,
    )
    regime_columns = _regime_columns_from_context(context_columns)
    regime_metrics = _build_regime_metrics(
        labeled_data,
        feature_columns=selected_features,
        forward_return_columns=selected_returns,
        regime_columns=regime_columns,
        group_by=groups,
    )
    regime_counts = _build_regime_counts(
        labeled_data,
        regime_columns=regime_columns,
        group_by=groups,
    )

    return RegimeAnalysisResult(
        labeled_data=labeled_data,
        regime_metrics=regime_metrics,
        regime_counts=regime_counts,
    )


def add_regime_labels(
    research_dataset: pd.DataFrame,
    *,
    trend_column: str | None = None,
    volatility_column: str | None = None,
    momentum_column: str | None = None,
    range_column: str | None = None,
    group_by: Sequence[str] = DEFAULT_GROUP_BY,
    key_columns: Sequence[str] = DEFAULT_KEY_COLUMNS,
    positive_threshold: float = 0.0,
    negative_threshold: float = 0.0,
) -> pd.DataFrame:
    """Return a copy of `research_dataset` with simple regime label columns."""

    groups = tuple(group_by)
    keys = tuple(key_columns)
    validate_group_by(groups, keys)
    require_columns(research_dataset, keys, frame_name="research_dataset")
    require_columns(research_dataset, groups, frame_name="research_dataset")
    _validate_thresholds(positive_threshold, negative_threshold)

    context_columns = _context_columns(
        trend_column=trend_column,
        volatility_column=volatility_column,
        momentum_column=momentum_column,
        range_column=range_column,
    )
    if not context_columns:
        raise ValueError("at least one regime context column is required")
    require_columns(research_dataset, tuple(context_columns.values()), frame_name="research_dataset")

    labeled = research_dataset.copy(deep=True)
    for column in context_columns.values():
        labeled[column] = pd.to_numeric(labeled[column])
    labeled = labeled.sort_values([*groups, *[key for key in keys if key not in groups]], kind="mergesort")

    if trend_column is not None:
        labeled["trend_regime"] = _label_signed_regime(
            labeled[trend_column],
            positive_label="bullish",
            negative_label="bearish",
            neutral_label="neutral",
            positive_threshold=positive_threshold,
            negative_threshold=negative_threshold,
        )

    if momentum_column is not None:
        labeled["momentum_regime"] = _label_signed_regime(
            labeled[momentum_column],
            positive_label="positive",
            negative_label="negative",
            neutral_label="flat",
            positive_threshold=positive_threshold,
            negative_threshold=negative_threshold,
        )

    if volatility_column is not None:
        labeled["volatility_regime"] = _label_volatility_regime(
            labeled,
            volatility_column=volatility_column,
            group_by=groups,
        )

    if range_column is not None:
        labeled["range_regime"] = _label_range_regime(
            labeled,
            range_column=range_column,
            group_by=groups,
        )

    return labeled.reset_index(drop=True)


def _build_regime_metrics(
    frame: pd.DataFrame,
    *,
    feature_columns: Sequence[str],
    forward_return_columns: Sequence[str],
    regime_columns: dict[str, str],
    group_by: Sequence[str],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for group_key, group in frame.groupby(list(group_by), sort=True, dropna=False):
        group_values = group_key_values(group_key, group_by)

        for regime_type, regime_column in regime_columns.items():
            for regime_label in REGIME_LABELS[regime_type]:
                regime_frame = group.loc[group[regime_column].eq(regime_label)]
                for feature in feature_columns:
                    for forward_return in forward_return_columns:
                        pair = regime_frame.loc[:, [feature, forward_return]].dropna()
                        feature_series = pair[feature]
                        return_series = pair[forward_return]
                        pearson_ic = safe_correlation(feature_series, return_series, method="pearson")
                        spearman_ic = safe_correlation(feature_series, return_series, method="spearman")

                        rows.append(
                            {
                                **group_values,
                                "regime_type": regime_type,
                                "regime": regime_label,
                                "feature": feature,
                                "forward_return": forward_return,
                                "sample_count": int(len(pair)),
                                "mean_forward_return": return_series.mean(),
                                "median_forward_return": return_series.median(),
                                "hit_rate": return_series.gt(0).mean() if len(pair) else pd.NA,
                                "avg_abs_forward_return": return_series.abs().mean(),
                                "pearson_ic": pearson_ic,
                                "spearman_ic": spearman_ic,
                            }
                        )

    return pd.DataFrame(rows)


def _build_regime_counts(
    frame: pd.DataFrame,
    *,
    regime_columns: dict[str, str],
    group_by: Sequence[str],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for group_key, group in frame.groupby(list(group_by), sort=True, dropna=False):
        group_values = group_key_values(group_key, group_by)
        for regime_type, regime_column in regime_columns.items():
            for regime_label in REGIME_LABELS[regime_type]:
                rows.append(
                    {
                        **group_values,
                        "regime_type": regime_type,
                        "regime": regime_label,
                        "row_count": int(group[regime_column].eq(regime_label).sum()),
                    }
                )

    return pd.DataFrame(rows)


def _label_signed_regime(
    series: pd.Series,
    *,
    positive_label: str,
    negative_label: str,
    neutral_label: str,
    positive_threshold: float,
    negative_threshold: float,
) -> pd.Series:
    labels = pd.Series(neutral_label, index=series.index, dtype="object")
    labels.loc[series.gt(positive_threshold)] = positive_label
    labels.loc[series.lt(negative_threshold)] = negative_label
    labels.loc[series.isna()] = pd.NA
    return labels


def _label_volatility_regime(
    frame: pd.DataFrame,
    *,
    volatility_column: str,
    group_by: Sequence[str],
) -> pd.Series:
    labels = pd.Series(pd.NA, index=frame.index, dtype="object")

    for _, group in frame.groupby(list(group_by), sort=True, dropna=False):
        values = group[volatility_column]
        valid = values.dropna()
        if valid.empty:
            continue
        if valid.nunique(dropna=True) <= 1:
            labels.loc[valid.index] = "medium_vol"
            continue

        try:
            bucket = pd.qcut(valid, q=3, labels=False, duplicates="drop")
        except ValueError:
            labels.loc[valid.index] = "medium_vol"
            continue

        max_bucket = int(bucket.max()) if pd.notna(bucket.max()) else 0
        if max_bucket <= 0:
            labels.loc[valid.index] = "medium_vol"
            continue

        mapped = bucket.map(_volatility_bucket_label)
        labels.loc[valid.index] = mapped

    return labels


def _volatility_bucket_label(bucket: int) -> str:
    if bucket <= 0:
        return "low_vol"
    if bucket == 1:
        return "medium_vol"
    return "high_vol"


def _label_range_regime(
    frame: pd.DataFrame,
    *,
    range_column: str,
    group_by: Sequence[str],
) -> pd.Series:
    labels = pd.Series(pd.NA, index=frame.index, dtype="object")

    for _, group in frame.groupby(list(group_by), sort=True, dropna=False):
        values = group[range_column]
        valid = values.dropna()
        if valid.empty:
            continue
        median = valid.median()
        labels.loc[valid.index] = "compressed"
        labels.loc[valid.gt(median).loc[lambda mask: mask].index] = "expanded"

    return labels


def _context_columns(
    *,
    trend_column: str | None,
    volatility_column: str | None,
    momentum_column: str | None,
    range_column: str | None,
) -> dict[str, str]:
    columns: dict[str, str] = {}
    if trend_column is not None:
        columns["trend"] = trend_column
    if volatility_column is not None:
        columns["volatility"] = volatility_column
    if momentum_column is not None:
        columns["momentum"] = momentum_column
    if range_column is not None:
        columns["range"] = range_column
    return columns


def _regime_columns_from_context(context_columns: dict[str, str]) -> dict[str, str]:
    return {regime_type: f"{regime_type}_regime" for regime_type in context_columns}


def _reject_feature_context_overlap(
    feature_columns: Sequence[str],
    context_columns: Sequence[str],
) -> None:
    overlap = sorted(set(feature_columns).intersection(context_columns))
    if overlap:
        raise ValueError(
            "regime context columns cannot also be analyzed as features; "
            "this creates circular regime evidence: "
            f"{overlap}"
        )


def _select_feature_columns(
    frame: pd.DataFrame,
    *,
    columns: Sequence[str] | None,
    excluded_columns: Sequence[str],
    forward_return_prefix: str,
) -> tuple[str, ...]:
    if columns is not None:
        selected = tuple(columns)
        require_columns(frame, selected, frame_name="research_dataset")
    else:
        excluded = set(excluded_columns)
        selected = tuple(
            column
            for column in frame.columns
            if column not in excluded
            and not column.startswith(forward_return_prefix)
            and is_numeric_or_all_null(frame[column])
        )

    if not selected:
        raise ValueError("research_dataset must contain at least one numeric feature column")

    invalid = [column for column in selected if column.startswith(forward_return_prefix)]
    if invalid:
        raise ValueError(f"feature columns must not include forward returns: {invalid}")

    non_numeric = [column for column in selected if not is_numeric_or_all_null(frame[column])]
    if non_numeric:
        raise ValueError(f"feature columns must be numeric: {non_numeric}")

    return selected


def _select_forward_return_columns(
    frame: pd.DataFrame,
    *,
    columns: Sequence[str] | None,
    forward_return_prefix: str,
) -> tuple[str, ...]:
    if columns is not None:
        selected = tuple(columns)
        require_columns(frame, selected, frame_name="research_dataset")
    else:
        selected = tuple(
            column
            for column in frame.columns
            if column.startswith(forward_return_prefix) and is_numeric_or_all_null(frame[column])
        )

    if not selected:
        raise ValueError("research_dataset must contain at least one forward return column")

    invalid = [column for column in selected if not column.startswith(forward_return_prefix)]
    if invalid:
        raise ValueError(f"forward return columns must start with '{forward_return_prefix}': {invalid}")

    non_numeric = [column for column in selected if not is_numeric_or_all_null(frame[column])]
    if non_numeric:
        raise ValueError(f"forward return columns must be numeric: {non_numeric}")

    return selected


def _validate_thresholds(positive_threshold: float, negative_threshold: float) -> None:
    if positive_threshold < negative_threshold:
        raise ValueError("positive_threshold must be greater than or equal to negative_threshold")
