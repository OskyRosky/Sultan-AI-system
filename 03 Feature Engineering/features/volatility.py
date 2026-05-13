"""Volatility feature calculations for validated OHLCV data."""

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
VOLATILITY_COLUMNS = ["rolling_std_20", "volatility_20", "atr_14"]


def calculate_volatility_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate volatility features without mutating the input DataFrame."""

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

    if "simple_return" in result.columns:
        simple_return = pd.to_numeric(result["simple_return"], errors="coerce")
    else:
        previous_close = result.groupby(GROUP_COLUMNS, sort=False)["close"].shift(1)
        valid_close = (result["close"] > 0) & (previous_close > 0)
        simple_return = pd.Series(
            np.where(valid_close, result["close"] / previous_close - 1.0, np.nan),
            index=result.index,
        )

    result["rolling_std_20"] = simple_return.groupby(
        [result[column] for column in GROUP_COLUMNS], sort=False
    ).transform(lambda values: values.rolling(window=20, min_periods=20).std())
    result["volatility_20"] = result["rolling_std_20"]

    previous_close = result.groupby(GROUP_COLUMNS, sort=False)["close"].shift(1)
    high_low = result["high"] - result["low"]
    high_previous_close = (result["high"] - previous_close).abs()
    low_previous_close = (result["low"] - previous_close).abs()
    true_range = pd.concat(
        [high_low, high_previous_close, low_previous_close], axis=1
    ).max(axis=1, skipna=True)

    result["atr_14"] = true_range.groupby(
        [result[column] for column in GROUP_COLUMNS], sort=False
    ).transform(lambda values: values.rolling(window=14, min_periods=14).mean())

    result[VOLATILITY_COLUMNS] = result[VOLATILITY_COLUMNS].replace(
        [np.inf, -np.inf], np.nan
    )
    result["feature_set"] = FEATURE_SET
    result["feature_version"] = FEATURE_VERSION

    return result
