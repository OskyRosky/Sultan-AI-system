"""Trend feature calculations for validated OHLCV data."""

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
TREND_COLUMNS = [
    "sma_20",
    "sma_50",
    "ema_20",
    "ema_50",
    "price_above_sma20",
    "sma20_slope",
    "ema20_above_ema50",
]


def calculate_trend_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate trend features without mutating the input DataFrame."""

    missing_columns = [column for column in BASE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"missing_required_columns={missing_columns}")

    result = df.copy()
    result["timestamp"] = pd.to_datetime(result["timestamp"], utc=True)
    result["close"] = pd.to_numeric(result["close"], errors="coerce")
    result = result.sort_values(
        ["exchange", "symbol", "timeframe", "timestamp"]
    ).reset_index(drop=True)

    grouped_close = result.groupby(GROUP_COLUMNS, sort=False)["close"]
    result["sma_20"] = grouped_close.transform(
        lambda values: values.rolling(window=20, min_periods=20).mean()
    )
    result["sma_50"] = grouped_close.transform(
        lambda values: values.rolling(window=50, min_periods=50).mean()
    )
    result["ema_20"] = grouped_close.transform(
        lambda values: values.ewm(span=20, adjust=False).mean()
    )
    result["ema_50"] = grouped_close.transform(
        lambda values: values.ewm(span=50, adjust=False).mean()
    )
    result["sma20_slope"] = result.groupby(GROUP_COLUMNS, sort=False)["sma_20"].diff()

    result["price_above_sma20"] = np.where(
        result["sma_20"].notna(),
        result["close"] > result["sma_20"],
        np.nan,
    )
    result["ema20_above_ema50"] = np.where(
        result["ema_20"].notna() & result["ema_50"].notna(),
        result["ema_20"] > result["ema_50"],
        np.nan,
    )

    result[TREND_COLUMNS] = result[TREND_COLUMNS].replace([np.inf, -np.inf], np.nan)
    result["feature_set"] = FEATURE_SET
    result["feature_version"] = FEATURE_VERSION

    return result
