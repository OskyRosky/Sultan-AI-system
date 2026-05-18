"""Pure in-memory research dataset construction.

This module joins trusted feature rows with precomputed forward return labels.
It performs validation only; it does not calculate features, calculate forward
returns, read storage, write storage, create signals, or interpret results.
"""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd


DEFAULT_KEY_COLUMNS: tuple[str, str, str] = ("symbol", "timeframe", "timestamp")
DEFAULT_FORWARD_RETURN_PREFIX = "forward_return_"


def build_research_dataset(
    features: pd.DataFrame,
    forward_returns: pd.DataFrame,
    *,
    key_columns: Sequence[str] = DEFAULT_KEY_COLUMNS,
    forward_return_prefix: str = DEFAULT_FORWARD_RETURN_PREFIX,
) -> pd.DataFrame:
    """Join trusted features with precomputed forward return labels in memory.

    The output contains only keys present in both inputs. Duplicate join keys
    are rejected before the merge so each output row remains one unambiguous
    research observation.
    """

    keys = tuple(key_columns)
    _require_columns(features, keys, frame_name="features")
    _require_columns(forward_returns, keys, frame_name="forward_returns")
    _reject_duplicate_keys(features, keys, frame_name="features")
    _reject_duplicate_keys(forward_returns, keys, frame_name="forward_returns")

    feature_columns = _non_key_columns(features, keys)
    forward_return_columns = _forward_return_columns(forward_returns, keys, forward_return_prefix)

    if not feature_columns:
        raise ValueError("features must contain at least one non-key feature column")
    if not forward_return_columns:
        raise ValueError(
            f"forward_returns must contain at least one '{forward_return_prefix}' column"
        )

    feature_side = features.loc[:, [*keys, *feature_columns]].copy(deep=True)
    label_side = forward_returns.loc[:, [*keys, *forward_return_columns]].copy(deep=True)

    result = feature_side.merge(
        label_side,
        on=list(keys),
        how="inner",
        validate="one_to_one",
        sort=False,
    )

    return result.sort_values(list(keys), kind="mergesort").reset_index(drop=True)


def research_dataset_columns(
    features: pd.DataFrame,
    forward_returns: pd.DataFrame,
    *,
    key_columns: Sequence[str] = DEFAULT_KEY_COLUMNS,
    forward_return_prefix: str = DEFAULT_FORWARD_RETURN_PREFIX,
) -> list[str]:
    """Return the expected output columns after validation."""

    keys = tuple(key_columns)
    _require_columns(features, keys, frame_name="features")
    _require_columns(forward_returns, keys, frame_name="forward_returns")

    feature_columns = _non_key_columns(features, keys)
    forward_return_columns = _forward_return_columns(forward_returns, keys, forward_return_prefix)
    return [*keys, *feature_columns, *forward_return_columns]


def _require_columns(frame: pd.DataFrame, columns: Sequence[str], *, frame_name: str) -> None:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ValueError(f"{frame_name} missing required columns: {missing}")


def _reject_duplicate_keys(
    frame: pd.DataFrame,
    key_columns: Sequence[str],
    *,
    frame_name: str,
) -> None:
    duplicate_mask = frame.duplicated(subset=list(key_columns), keep=False)
    if duplicate_mask.any():
        duplicate_keys = frame.loc[duplicate_mask, list(key_columns)].drop_duplicates()
        raise ValueError(
            f"{frame_name} duplicate rows found for research dataset keys: "
            f"{duplicate_keys.to_dict(orient='records')}"
        )


def _non_key_columns(frame: pd.DataFrame, key_columns: Sequence[str]) -> list[str]:
    key_set = set(key_columns)
    return [column for column in frame.columns if column not in key_set]


def _forward_return_columns(
    frame: pd.DataFrame,
    key_columns: Sequence[str],
    forward_return_prefix: str,
) -> list[str]:
    key_set = set(key_columns)
    return [
        column
        for column in frame.columns
        if column not in key_set and column.startswith(forward_return_prefix)
    ]
