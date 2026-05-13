"""Relative strength / breakout context feature calculations."""

from __future__ import annotations

import numpy as np
import pandas as pd

from config import FEATURE_SET, FEATURE_VERSION


BASE_COLUMNS = [
    "exchange",
    "symbol",
    "timeframe",
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume",
]
GROUP_COLUMNS = ["exchange", "symbol", "timeframe"]
BREAKOUT_CONTEXT_COLUMNS = ["close_vs_high_52w", "rolling_max_20", "rolling_min_20"]
HIGH_52W_LOOKBACK_BY_TIMEFRAME = {
    "1d": 365,
    "4h": 2190,
}


def calculate_breakout_context_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate breakout context features without mutating the input DataFrame."""

    missing_columns = [column for column in BASE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"missing_required_columns={missing_columns}")

    result = df.copy()
    result["timestamp"] = pd.to_datetime(result["timestamp"], utc=True)
    for column in ["high", "low", "close"]:
        result[column] = pd.to_numeric(result[column], errors="coerce")

    result = result.sort_values(
        ["exchange", "symbol", "timeframe", "timestamp"]
    ).reset_index(drop=True)

    grouped = result.groupby(GROUP_COLUMNS, sort=False)
    result["rolling_max_20"] = grouped["high"].transform(
        lambda values: values.rolling(window=20, min_periods=20).max()
    )
    result["rolling_min_20"] = grouped["low"].transform(
        lambda values: values.rolling(window=20, min_periods=20).min()
    )

    close_vs_high_52w = pd.Series(np.nan, index=result.index, dtype="float64")
    for (_, _, timeframe), group_index in grouped.groups.items():
        lookback = HIGH_52W_LOOKBACK_BY_TIMEFRAME.get(str(timeframe))
        if lookback is None:
            raise ValueError(f"unsupported_timeframe_for_close_vs_high_52w={timeframe}")

        high_52w = result.loc[group_index, "high"].rolling(
            window=lookback,
            min_periods=lookback,
        ).max()
        close = result.loc[group_index, "close"]
        close_vs_high_52w.loc[group_index] = np.where(
            high_52w > 0,
            close / high_52w,
            np.nan,
        )

    result["close_vs_high_52w"] = close_vs_high_52w
    result[BREAKOUT_CONTEXT_COLUMNS] = result[BREAKOUT_CONTEXT_COLUMNS].replace(
        [np.inf, -np.inf], np.nan
    )
    result["feature_set"] = FEATURE_SET
    result["feature_version"] = FEATURE_VERSION

    return result
