"""Pure in-memory temporal stability diagnostics for Research Layer.

This module evaluates simple windowed stability of feature-to-forward-return
relationships. It does not create signals, rankings, strategies, backtests, or
economic interpretations.
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
DEFAULT_TIMESTAMP_COLUMN = "timestamp"
DEFAULT_FORWARD_RETURN_PREFIX = "forward_return_"
DEFAULT_N_WINDOWS = 3


@dataclass(frozen=True)
class WindowSpec:
    """Explicit temporal window definition."""

    label: str
    start: pd.Timestamp | str
    end: pd.Timestamp | str


@dataclass(frozen=True)
class TemporalStabilityResult:
    """Structured in-memory output for temporal stability analysis."""

    window_metrics: pd.DataFrame
    drift_metrics: pd.DataFrame


def analyze_temporal_stability(
    research_dataset: pd.DataFrame,
    *,
    feature_columns: Sequence[str] | None = None,
    forward_return_columns: Sequence[str] | None = None,
    group_by: Sequence[str] = DEFAULT_GROUP_BY,
    key_columns: Sequence[str] = DEFAULT_KEY_COLUMNS,
    timestamp_column: str = DEFAULT_TIMESTAMP_COLUMN,
    windows: Sequence[WindowSpec | tuple[str, object, object]] | None = None,
    n_windows: int = DEFAULT_N_WINDOWS,
    forward_return_prefix: str = DEFAULT_FORWARD_RETURN_PREFIX,
) -> TemporalStabilityResult:
    """Analyze temporal stability with simple non-overlapping windows."""

    groups = tuple(group_by)
    keys = tuple(key_columns)
    validate_group_by(groups, keys)
    require_columns(research_dataset, keys, frame_name="research_dataset")
    require_columns(research_dataset, groups, frame_name="research_dataset")
    require_columns(research_dataset, (timestamp_column,), frame_name="research_dataset")
    _validate_n_windows(n_windows)

    selected_features = _select_numeric_columns(
        research_dataset,
        columns=feature_columns,
        excluded_columns=(*keys, *groups),
        prefix_to_exclude=forward_return_prefix,
        error_label="feature",
    )
    selected_returns = _select_forward_return_columns(
        research_dataset,
        columns=forward_return_columns,
        forward_return_prefix=forward_return_prefix,
    )

    frame = research_dataset.copy(deep=True)
    frame[timestamp_column] = pd.to_datetime(frame[timestamp_column])
    for column in (*selected_features, *selected_returns):
        frame[column] = pd.to_numeric(frame[column])
    frame = frame.sort_values([*groups, timestamp_column], kind="mergesort")

    explicit_windows = _normalize_windows(windows)
    window_metrics = _build_window_metrics(
        frame,
        feature_columns=selected_features,
        forward_return_columns=selected_returns,
        group_by=groups,
        timestamp_column=timestamp_column,
        windows=explicit_windows,
        n_windows=n_windows,
    )
    drift_metrics = _build_drift_metrics(window_metrics, groups)

    return TemporalStabilityResult(window_metrics=window_metrics, drift_metrics=drift_metrics)


def _build_window_metrics(
    frame: pd.DataFrame,
    *,
    feature_columns: Sequence[str],
    forward_return_columns: Sequence[str],
    group_by: Sequence[str],
    timestamp_column: str,
    windows: tuple[WindowSpec, ...] | None,
    n_windows: int,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for group_key, group in frame.groupby(list(group_by), sort=True, dropna=False):
        group_values = group_key_values(group_key, group_by)
        grouped_windows = (
            _explicit_window_slices(group, windows, timestamp_column)
            if windows is not None
            else _equal_count_window_slices(group, n_windows, timestamp_column)
        )

        for window_label, window_start, window_end, window_frame in grouped_windows:
            for feature in feature_columns:
                for forward_return in forward_return_columns:
                    pair = window_frame.loc[:, [feature, forward_return]].dropna()
                    sample_count = int(len(pair))
                    feature_series = pair[feature]
                    return_series = pair[forward_return]
                    correlation = safe_correlation(feature_series, return_series)

                    rows.append(
                        {
                            **group_values,
                            "window": window_label,
                            "window_start": window_start,
                            "window_end": window_end,
                            "feature": feature,
                            "forward_return": forward_return,
                            "sample_count": sample_count,
                            "feature_mean": feature_series.mean(),
                            "feature_std": feature_series.std(),
                            "feature_variance": feature_series.var(),
                            "return_mean": return_series.mean(),
                            "return_std": return_series.std(),
                            "return_variance": return_series.var(),
                            "correlation": correlation,
                            "correlation_sign": _correlation_sign(correlation),
                        }
                    )

    return pd.DataFrame(rows)


def _build_drift_metrics(window_metrics: pd.DataFrame, group_by: Sequence[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    metric_groups = [*group_by, "feature", "forward_return"]

    for group_key, group in window_metrics.groupby(metric_groups, sort=True, dropna=False):
        group_values = dict(zip(metric_groups, tuple(group_key), strict=True))
        valid_correlation = group["correlation"].dropna()
        valid_feature_mean = group["feature_mean"].dropna()
        nonzero_signs = group["correlation_sign"].dropna()
        nonzero_signs = nonzero_signs[nonzero_signs.ne(0)]

        rows.append(
            {
                **group_values,
                "windows_observed": int(group["sample_count"].gt(0).sum()),
                "correlation_min": valid_correlation.min(),
                "correlation_max": valid_correlation.max(),
                "correlation_range": _range(valid_correlation),
                "correlation_std": valid_correlation.std(),
                "feature_mean_min": valid_feature_mean.min(),
                "feature_mean_max": valid_feature_mean.max(),
                "feature_mean_range": _range(valid_feature_mean),
                "feature_mean_std": valid_feature_mean.std(),
                "sign_consistency_ratio": _sign_consistency_ratio(nonzero_signs),
            }
        )

    return pd.DataFrame(rows)


def _explicit_window_slices(
    group: pd.DataFrame,
    windows: tuple[WindowSpec, ...],
    timestamp_column: str,
) -> list[tuple[str, pd.Timestamp, pd.Timestamp, pd.DataFrame]]:
    slices: list[tuple[str, pd.Timestamp, pd.Timestamp, pd.DataFrame]] = []

    for window in windows:
        start = pd.Timestamp(window.start)
        end = pd.Timestamp(window.end)
        mask = group[timestamp_column].ge(start) & group[timestamp_column].le(end)
        slices.append((window.label, start, end, group.loc[mask]))

    return slices


def _equal_count_window_slices(
    group: pd.DataFrame,
    n_windows: int,
    timestamp_column: str,
) -> list[tuple[str, pd.Timestamp | pd.NaT, pd.Timestamp | pd.NaT, pd.DataFrame]]:
    if group.empty:
        return [
            (f"window_{window_number}", pd.NaT, pd.NaT, group)
            for window_number in range(1, n_windows + 1)
        ]

    assigned = group.copy(deep=True).reset_index(drop=True)
    row_count = len(assigned)
    assigned["_window_number"] = [
        min((row_index * n_windows) // row_count + 1, n_windows)
        for row_index in range(row_count)
    ]

    slices: list[tuple[str, pd.Timestamp | pd.NaT, pd.Timestamp | pd.NaT, pd.DataFrame]] = []
    for window_number in range(1, n_windows + 1):
        window_frame = assigned.loc[assigned["_window_number"].eq(window_number)].drop(
            columns=["_window_number"]
        )
        if window_frame.empty:
            slices.append((f"window_{window_number}", pd.NaT, pd.NaT, window_frame))
        else:
            slices.append(
                (
                    f"window_{window_number}",
                    window_frame[timestamp_column].min(),
                    window_frame[timestamp_column].max(),
                    window_frame,
                )
            )

    return slices


def _normalize_windows(
    windows: Sequence[WindowSpec | tuple[str, object, object]] | None,
) -> tuple[WindowSpec, ...] | None:
    if windows is None:
        return None

    normalized: list[WindowSpec] = []
    for window in windows:
        if isinstance(window, WindowSpec):
            spec = window
        else:
            label, start, end = window
            spec = WindowSpec(label=str(label), start=pd.Timestamp(start), end=pd.Timestamp(end))

        start_timestamp = pd.Timestamp(spec.start)
        end_timestamp = pd.Timestamp(spec.end)
        if end_timestamp < start_timestamp:
            raise ValueError(f"window '{spec.label}' end must be greater than or equal to start")
        normalized.append(WindowSpec(spec.label, start_timestamp, end_timestamp))

    if not normalized:
        raise ValueError("windows must contain at least one window when provided")

    return tuple(normalized)


def _select_numeric_columns(
    frame: pd.DataFrame,
    *,
    columns: Sequence[str] | None,
    excluded_columns: Sequence[str],
    prefix_to_exclude: str,
    error_label: str,
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
            and not column.startswith(prefix_to_exclude)
            and is_numeric_or_all_null(frame[column])
        )

    if not selected:
        raise ValueError(f"research_dataset must contain at least one numeric {error_label} column")

    non_numeric = [column for column in selected if not is_numeric_or_all_null(frame[column])]
    if non_numeric:
        raise ValueError(f"{error_label} columns must be numeric: {non_numeric}")

    invalid_prefixed = [column for column in selected if column.startswith(prefix_to_exclude)]
    if invalid_prefixed:
        raise ValueError(f"{error_label} columns must not include forward returns: {invalid_prefixed}")

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


def _correlation_sign(correlation: object) -> int | pd.NA:
    if pd.isna(correlation):
        return pd.NA
    if correlation > 0:
        return 1
    if correlation < 0:
        return -1
    return 0


def _range(series: pd.Series) -> float | pd.NA:
    if series.empty:
        return pd.NA
    return series.max() - series.min()


def _sign_consistency_ratio(signs: pd.Series) -> float | pd.NA:
    if signs.empty:
        return pd.NA
    return signs.value_counts().max() / len(signs)


def _validate_n_windows(n_windows: int) -> None:
    if not isinstance(n_windows, int):
        raise TypeError("n_windows must be an integer")
    if n_windows <= 0:
        raise ValueError("n_windows must be greater than zero")
