"""Candle structure feature calculations for validated OHLCV data."""

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
CANDLE_STRUCTURE_COLUMNS = [
    "high_low_range",
    "body_size",
    "upper_wick",
    "lower_wick",
    "body_to_range_ratio",
]


def calculate_candle_structure_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate candle structure features without mutating the input DataFrame."""

    missing_columns = [column for column in BASE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"missing_required_columns={missing_columns}")

    result = df.copy()
    result["timestamp"] = pd.to_datetime(result["timestamp"], utc=True)
    for column in ["open", "high", "low", "close"]:
        result[column] = pd.to_numeric(result[column], errors="coerce")

    result = result.sort_values(
        ["exchange", "symbol", "timeframe", "timestamp"]
    ).reset_index(drop=True)

    open_close_max = result[["open", "close"]].max(axis=1)
    open_close_min = result[["open", "close"]].min(axis=1)

    result["high_low_range"] = result["high"] - result["low"]
    result["body_size"] = (result["close"] - result["open"]).abs()
    result["upper_wick"] = result["high"] - open_close_max
    result["lower_wick"] = open_close_min - result["low"]
    result["body_to_range_ratio"] = np.where(
        result["high_low_range"] > 0,
        result["body_size"] / result["high_low_range"],
        np.nan,
    )

    result[CANDLE_STRUCTURE_COLUMNS] = result[CANDLE_STRUCTURE_COLUMNS].replace(
        [np.inf, -np.inf], np.nan
    )
    result["feature_set"] = FEATURE_SET
    result["feature_version"] = FEATURE_VERSION

    return result
