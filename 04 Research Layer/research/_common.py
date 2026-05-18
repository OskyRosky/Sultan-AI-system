"""Small shared helpers for pure in-memory Research Layer modules."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
from pandas.api.types import is_numeric_dtype


# Correlation over 2 observations is always mechanically perfect when both
# series vary. Five pairs is still a small-sample diagnostic, but avoids the
# most misleading degenerate case while keeping synthetic tests lightweight.
MIN_CORRELATION_PAIRS = 5


def require_columns(frame: pd.DataFrame, columns: Sequence[str], *, frame_name: str) -> None:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ValueError(f"{frame_name} missing required columns: {missing}")


def group_key_values(group_key: object, group_by: Sequence[str]) -> dict[str, object]:
    if len(group_by) == 1:
        values = group_key if isinstance(group_key, tuple) else (group_key,)
    else:
        values = tuple(group_key)
    return dict(zip(group_by, values, strict=True))


def is_numeric_or_all_null(series: pd.Series) -> bool:
    return is_numeric_dtype(series) or series.dropna().empty


def validate_group_by(group_by: Sequence[str], key_columns: Sequence[str]) -> None:
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


def safe_correlation(
    feature: pd.Series,
    forward_return: pd.Series,
    *,
    method: str = "pearson",
) -> float | pd.NA:
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
