"""Pure in-memory forward return calculations for Research Layer.

This module does not read or write storage. It expects OHLCV rows that are
already loaded in memory and returns a new DataFrame with label columns.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import pandas as pd


DEFAULT_HORIZONS: tuple[int, ...] = (1, 3, 5, 10)
DEFAULT_GROUP_COLUMNS: tuple[str, str] = ("symbol", "timeframe")
DEFAULT_TIMESTAMP_COLUMN = "timestamp"
DEFAULT_CLOSE_COLUMN = "close"


def add_forward_returns(
    ohlcv: pd.DataFrame,
    horizons: Sequence[int] = DEFAULT_HORIZONS,
    *,
    group_columns: Sequence[str] = DEFAULT_GROUP_COLUMNS,
    timestamp_column: str = DEFAULT_TIMESTAMP_COLUMN,
    close_column: str = DEFAULT_CLOSE_COLUMN,
    output_prefix: str = "forward_return",
) -> pd.DataFrame:
    """Return a copy of `ohlcv` with arithmetic forward return labels.

    For each horizon `h`, the label is:

        close[t + h] / close[t] - 1

    Calculation is isolated within each `(symbol, timeframe)` group by default.
    Duplicate group/timestamp keys are rejected because they make `close[t]`
    ambiguous. Missing future rows naturally produce NaN labels and are not
    filled.
    """

    normalized_horizons = _normalize_horizons(horizons)
    grouping = tuple(group_columns)
    required_columns = (*grouping, timestamp_column, close_column)
    _require_columns(ohlcv, required_columns)
    _reject_duplicate_timestamps(ohlcv, grouping, timestamp_column)

    result = ohlcv.copy(deep=True)
    result = result.sort_values([*grouping, timestamp_column], kind="mergesort")

    grouped_close = result.groupby(list(grouping), sort=False, observed=True)[close_column]

    for horizon in normalized_horizons:
        output_column = f"{output_prefix}_{horizon}"
        future_close = grouped_close.shift(-horizon)
        result[output_column] = future_close / result[close_column] - 1

    return result


def forward_return_columns(
    horizons: Sequence[int] = DEFAULT_HORIZONS,
    *,
    output_prefix: str = "forward_return",
) -> list[str]:
    """Return the expected forward return column names for `horizons`."""

    return [f"{output_prefix}_{horizon}" for horizon in _normalize_horizons(horizons)]


def _normalize_horizons(horizons: Sequence[int]) -> tuple[int, ...]:
    if isinstance(horizons, (str, bytes)) or not isinstance(horizons, Iterable):
        raise TypeError("horizons must be a sequence of positive integers")

    normalized: list[int] = []
    for horizon in horizons:
        if not isinstance(horizon, int):
            raise TypeError("each horizon must be an integer")
        if horizon <= 0:
            raise ValueError("each horizon must be greater than zero")
        normalized.append(horizon)

    if not normalized:
        raise ValueError("at least one horizon is required")

    return tuple(dict.fromkeys(normalized))


def _require_columns(frame: pd.DataFrame, columns: Sequence[str]) -> None:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")


def _reject_duplicate_timestamps(
    frame: pd.DataFrame,
    group_columns: Sequence[str],
    timestamp_column: str,
) -> None:
    key_columns = [*group_columns, timestamp_column]
    duplicate_mask = frame.duplicated(subset=key_columns, keep=False)
    if duplicate_mask.any():
        duplicate_keys = frame.loc[duplicate_mask, key_columns].drop_duplicates()
        raise ValueError(
            "duplicate rows found for group/timestamp keys: "
            f"{duplicate_keys.to_dict(orient='records')}"
        )
