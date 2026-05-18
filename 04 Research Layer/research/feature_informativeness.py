"""Pure in-memory feature informativeness diagnostics for Research Layer.

This module estimates statistical relationships between features at t and
precomputed forward returns aligned at t. It does not create signals,
strategies, backtests, positions, or economic interpretations.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import pandas as pd
from pandas.api.types import is_numeric_dtype


DEFAULT_GROUP_BY: tuple[str, str] = ("symbol", "timeframe")
DEFAULT_KEY_COLUMNS: tuple[str, str, str] = ("symbol", "timeframe", "timestamp")
DEFAULT_FORWARD_RETURN_PREFIX = "forward_return_"
DEFAULT_N_BUCKETS = 5
MIN_CORRELATION_PAIRS = 2


@dataclass(frozen=True)
class FeatureInformativenessResult:
    """Structured in-memory output for feature informativeness analysis."""

    bucket_metrics: pd.DataFrame
    ic_metrics: pd.DataFrame
    ranking: pd.DataFrame


def analyze_feature_informativeness(
    research_dataset: pd.DataFrame,
    *,
    feature_columns: Sequence[str] | None = None,
    forward_return_columns: Sequence[str] | None = None,
    group_by: Sequence[str] = DEFAULT_GROUP_BY,
    key_columns: Sequence[str] = DEFAULT_KEY_COLUMNS,
    n_buckets: int = DEFAULT_N_BUCKETS,
    forward_return_prefix: str = DEFAULT_FORWARD_RETURN_PREFIX,
) -> FeatureInformativenessResult:
    """Analyze feature-to-forward-return informativeness in memory."""

    groups = tuple(group_by)
    keys = tuple(key_columns)
    _validate_group_by(groups, keys)
    _validate_n_buckets(n_buckets)
    _require_columns(research_dataset, keys, frame_name="research_dataset")
    _require_columns(research_dataset, groups, frame_name="research_dataset")

    selected_features = _select_feature_columns(
        research_dataset,
        columns=feature_columns,
        excluded_columns=(*keys, *groups),
        forward_return_prefix=forward_return_prefix,
    )
    selected_returns = _select_forward_return_columns(
        research_dataset,
        columns=forward_return_columns,
        forward_return_prefix=forward_return_prefix,
    )

    frame = research_dataset.copy(deep=True)
    for column in (*selected_features, *selected_returns):
        frame[column] = pd.to_numeric(frame[column])
    frame = frame.sort_values([*groups, *[key for key in keys if key not in groups]], kind="mergesort")

    bucket_metrics = _build_bucket_metrics(
        frame,
        feature_columns=selected_features,
        forward_return_columns=selected_returns,
        group_by=groups,
        n_buckets=n_buckets,
    )
    ic_metrics = _build_ic_metrics(
        frame,
        feature_columns=selected_features,
        forward_return_columns=selected_returns,
        group_by=groups,
    )
    ranking = _build_ranking(ic_metrics, groups)

    return FeatureInformativenessResult(
        bucket_metrics=bucket_metrics,
        ic_metrics=ic_metrics,
        ranking=ranking,
    )


def _build_bucket_metrics(
    frame: pd.DataFrame,
    *,
    feature_columns: Sequence[str],
    forward_return_columns: Sequence[str],
    group_by: Sequence[str],
    n_buckets: int,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for group_key, group in frame.groupby(list(group_by), sort=True, dropna=False):
        group_values = _group_key_values(group_key, group_by)

        for feature in feature_columns:
            for forward_return in forward_return_columns:
                pair = group.loc[:, [feature, forward_return]].dropna()
                if pair.empty:
                    rows.append(
                        {
                            **group_values,
                            "feature": feature,
                            "forward_return": forward_return,
                            "bucket": pd.NA,
                            "bucket_min": pd.NA,
                            "bucket_max": pd.NA,
                            "count": 0,
                            "mean_forward_return": pd.NA,
                            "median_forward_return": pd.NA,
                            "hit_rate": pd.NA,
                            "avg_abs_forward_return": pd.NA,
                        }
                    )
                    continue

                bucketed = pair.copy(deep=True)
                bucketed["bucket"] = _assign_quantile_buckets(bucketed[feature], n_buckets)

                for bucket, bucket_frame in bucketed.groupby("bucket", sort=True, dropna=False):
                    returns = bucket_frame[forward_return]
                    rows.append(
                        {
                            **group_values,
                            "feature": feature,
                            "forward_return": forward_return,
                            "bucket": int(bucket) if pd.notna(bucket) else pd.NA,
                            "bucket_min": bucket_frame[feature].min(),
                            "bucket_max": bucket_frame[feature].max(),
                            "count": int(len(bucket_frame)),
                            "mean_forward_return": returns.mean(),
                            "median_forward_return": returns.median(),
                            "hit_rate": returns.gt(0).mean(),
                            "avg_abs_forward_return": returns.abs().mean(),
                        }
                    )

    return pd.DataFrame(rows)


def _build_ic_metrics(
    frame: pd.DataFrame,
    *,
    feature_columns: Sequence[str],
    forward_return_columns: Sequence[str],
    group_by: Sequence[str],
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for group_key, group in frame.groupby(list(group_by), sort=True, dropna=False):
        group_values = _group_key_values(group_key, group_by)

        for feature in feature_columns:
            for forward_return in forward_return_columns:
                pair = group.loc[:, [feature, forward_return]].dropna()
                feature_series = pair[feature]
                return_series = pair[forward_return]
                pearson_ic = _safe_correlation(feature_series, return_series, method="pearson")
                spearman_ic = _safe_correlation(feature_series, return_series, method="spearman")

                rows.append(
                    {
                        **group_values,
                        "feature": feature,
                        "forward_return": forward_return,
                        "sample_count": int(len(pair)),
                        "pearson_ic": pearson_ic,
                        "spearman_ic": spearman_ic,
                        "abs_pearson_ic": abs(pearson_ic) if pd.notna(pearson_ic) else pd.NA,
                        "abs_spearman_ic": abs(spearman_ic) if pd.notna(spearman_ic) else pd.NA,
                        "avg_abs_forward_return": return_series.abs().mean(),
                    }
                )

    return pd.DataFrame(rows)


def _build_ranking(ic_metrics: pd.DataFrame, group_by: Sequence[str]) -> pd.DataFrame:
    if ic_metrics.empty:
        return ic_metrics.copy()

    rank_groups = [*group_by, "forward_return"]
    ranked_parts: list[pd.DataFrame] = []

    for _, group in ic_metrics.groupby(rank_groups, sort=True, dropna=False):
        ranked = group.copy(deep=True)
        ranked["_sort_abs_pearson"] = ranked["abs_pearson_ic"].fillna(-1)
        ranked["_sort_abs_spearman"] = ranked["abs_spearman_ic"].fillna(-1)
        ranked = ranked.sort_values(
            ["_sort_abs_pearson", "_sort_abs_spearman", "sample_count", "feature"],
            ascending=[False, False, False, True],
            kind="mergesort",
        )
        ranked["technical_rank"] = range(1, len(ranked) + 1)
        ranked_parts.append(ranked.drop(columns=["_sort_abs_pearson", "_sort_abs_spearman"]))

    return pd.concat(ranked_parts, ignore_index=True)


def _assign_quantile_buckets(series: pd.Series, n_buckets: int) -> pd.Series:
    if series.empty:
        return pd.Series(dtype="Int64", index=series.index)

    unique_count = int(series.nunique(dropna=True))
    if unique_count <= 1:
        return pd.Series(1, index=series.index, dtype="Int64")

    requested_buckets = min(n_buckets, unique_count, len(series))
    try:
        buckets = pd.qcut(series, q=requested_buckets, labels=False, duplicates="drop")
    except ValueError:
        return pd.Series(1, index=series.index, dtype="Int64")

    if buckets.isna().all():
        return pd.Series(1, index=series.index, dtype="Int64")

    return (buckets.astype("Int64") + 1).astype("Int64")


def _safe_correlation(feature: pd.Series, forward_return: pd.Series, *, method: str) -> float | pd.NA:
    if len(feature) < MIN_CORRELATION_PAIRS:
        return pd.NA
    if feature.nunique(dropna=True) <= 1 or forward_return.nunique(dropna=True) <= 1:
        return pd.NA
    if method == "spearman":
        return feature.rank(method="average").corr(
            forward_return.rank(method="average"),
            method="pearson",
        )
    return feature.corr(forward_return, method=method)


def _select_feature_columns(
    frame: pd.DataFrame,
    *,
    columns: Sequence[str] | None,
    excluded_columns: Sequence[str],
    forward_return_prefix: str,
) -> tuple[str, ...]:
    if columns is not None:
        selected = tuple(columns)
        _require_columns(frame, selected, frame_name="research_dataset")
    else:
        excluded = set(excluded_columns)
        selected = tuple(
            column
            for column in frame.columns
            if column not in excluded
            and not column.startswith(forward_return_prefix)
            and _is_numeric_or_all_null(frame[column])
        )

    if not selected:
        raise ValueError("research_dataset must contain at least one numeric feature column")

    invalid = [column for column in selected if column.startswith(forward_return_prefix)]
    if invalid:
        raise ValueError(f"feature columns must not include forward returns: {invalid}")

    non_numeric = [column for column in selected if not _is_numeric_or_all_null(frame[column])]
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
        _require_columns(frame, selected, frame_name="research_dataset")
    else:
        selected = tuple(
            column
            for column in frame.columns
            if column.startswith(forward_return_prefix) and _is_numeric_or_all_null(frame[column])
        )

    if not selected:
        raise ValueError("research_dataset must contain at least one forward return column")

    invalid = [column for column in selected if not column.startswith(forward_return_prefix)]
    if invalid:
        raise ValueError(f"forward return columns must start with '{forward_return_prefix}': {invalid}")

    non_numeric = [column for column in selected if not _is_numeric_or_all_null(frame[column])]
    if non_numeric:
        raise ValueError(f"forward return columns must be numeric: {non_numeric}")

    return selected


def _group_key_values(group_key: object, group_by: Sequence[str]) -> dict[str, object]:
    if len(group_by) == 1:
        values = group_key if isinstance(group_key, tuple) else (group_key,)
    else:
        values = tuple(group_key)
    return dict(zip(group_by, values, strict=True))


def _is_numeric_or_all_null(series: pd.Series) -> bool:
    return is_numeric_dtype(series) or series.dropna().empty


def _validate_group_by(group_by: Sequence[str], key_columns: Sequence[str]) -> None:
    allowed_groups = {"symbol", "timeframe"}
    groups = tuple(group_by)

    if not groups:
        raise ValueError("group_by must include 'symbol', 'timeframe', or both")

    unknown = [group for group in groups if group not in allowed_groups]
    if unknown:
        raise ValueError(f"group_by contains unsupported columns: {unknown}")

    missing_from_keys = [group for group in groups if group not in key_columns]
    if missing_from_keys:
        raise ValueError(f"group_by columns must also be key columns: {missing_from_keys}")


def _validate_n_buckets(n_buckets: int) -> None:
    if not isinstance(n_buckets, int):
        raise TypeError("n_buckets must be an integer")
    if n_buckets <= 0:
        raise ValueError("n_buckets must be greater than zero")


def _require_columns(frame: pd.DataFrame, columns: Sequence[str], *, frame_name: str) -> None:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ValueError(f"{frame_name} missing required columns: {missing}")
