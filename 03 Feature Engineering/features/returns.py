"""Return feature calculations for validated OHLCV data."""

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
RETURN_COLUMNS = ["simple_return", "log_return", "close_open_return"]


def calculate_return_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate return features without mutating the input DataFrame."""

    missing_columns = [column for column in BASE_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError(f"missing_required_columns={missing_columns}")

    result = df[BASE_COLUMNS].copy()
    result["timestamp"] = pd.to_datetime(result["timestamp"], utc=True)
    for column in ["open", "close"]:
        result[column] = pd.to_numeric(result[column], errors="coerce")

    result = result.sort_values(
        ["exchange", "symbol", "timeframe", "timestamp"]
    ).reset_index(drop=True)

    previous_close = result.groupby(GROUP_COLUMNS, sort=False)["close"].shift(1)
    close = result["close"]
    open_ = result["open"]

    valid_previous_close = previous_close > 0
    valid_current_close = close > 0
    valid_open = open_ > 0

    result["simple_return"] = np.where(
        valid_previous_close & valid_current_close,
        close / previous_close - 1.0,
        np.nan,
    )
    result["log_return"] = np.where(
        valid_previous_close & valid_current_close,
        np.log(close / previous_close),
        np.nan,
    )
    result["close_open_return"] = np.where(
        valid_open & valid_current_close,
        close / open_ - 1.0,
        np.nan,
    )

    result[RETURN_COLUMNS] = result[RETURN_COLUMNS].replace([np.inf, -np.inf], np.nan)
    result["feature_set"] = FEATURE_SET
    result["feature_version"] = FEATURE_VERSION

    return result
