"""Volume feature calculations for validated OHLCV data."""

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
VOLUME_COLUMNS = ["volume_change", "volume_sma_20", "volume_ratio_20"]


def calculate_volume_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate volume features without mutating the input DataFrame."""

    missing_columns = [column for column in BASE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"missing_required_columns={missing_columns}")

    result = df.copy()
    result["timestamp"] = pd.to_datetime(result["timestamp"], utc=True)
    result["volume"] = pd.to_numeric(result["volume"], errors="coerce")
    result = result.sort_values(
        ["exchange", "symbol", "timeframe", "timestamp"]
    ).reset_index(drop=True)

    grouped_volume = result.groupby(GROUP_COLUMNS, sort=False)["volume"]
    previous_volume = grouped_volume.shift(1)
    valid_previous_volume = previous_volume > 0
    result["volume_change"] = np.where(
        valid_previous_volume,
        result["volume"] / previous_volume - 1.0,
        np.nan,
    )
    result["volume_sma_20"] = grouped_volume.transform(
        lambda values: values.rolling(window=20, min_periods=20).mean()
    )
    result["volume_ratio_20"] = np.where(
        result["volume_sma_20"] > 0,
        result["volume"] / result["volume_sma_20"],
        np.nan,
    )

    result[VOLUME_COLUMNS] = result[VOLUME_COLUMNS].replace([np.inf, -np.inf], np.nan)
    result["feature_set"] = FEATURE_SET
    result["feature_version"] = FEATURE_VERSION

    return result
