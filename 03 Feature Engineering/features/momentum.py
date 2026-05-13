"""Momentum feature calculations for validated OHLCV data."""

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
MOMENTUM_COLUMNS = ["rsi_14", "macd", "macd_signal"]


def calculate_momentum_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate momentum features without mutating the input DataFrame."""

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
    result["rsi_14"] = grouped_close.transform(_calculate_rsi_14)

    ema_12 = grouped_close.transform(lambda values: values.ewm(span=12, adjust=False).mean())
    ema_26 = grouped_close.transform(lambda values: values.ewm(span=26, adjust=False).mean())
    result["macd"] = ema_12 - ema_26
    result["macd_signal"] = result.groupby(GROUP_COLUMNS, sort=False)["macd"].transform(
        lambda values: values.ewm(span=9, adjust=False).mean()
    )

    result[MOMENTUM_COLUMNS] = result[MOMENTUM_COLUMNS].replace(
        [np.inf, -np.inf], np.nan
    )
    result["feature_set"] = FEATURE_SET
    result["feature_version"] = FEATURE_VERSION

    return result


def _calculate_rsi_14(close: pd.Series) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = (-delta.clip(upper=0)).abs()

    avg_gain = gain.ewm(alpha=1 / 14, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / 14, adjust=False).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    rsi = rsi.where(avg_loss != 0, 100.0)
    rsi = rsi.where(avg_gain != 0, 0.0)
    rsi = rsi.where(close.notna())
    rsi.iloc[:14] = np.nan
    return rsi.clip(lower=0, upper=100)
