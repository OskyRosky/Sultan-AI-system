from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from breakout_context import calculate_breakout_context_features
from returns import calculate_return_features
from trend import calculate_trend_features


def _ohlcv_dataframe(periods: int = 90) -> pd.DataFrame:
    rows = []
    for symbol, base_close in [("BTCUSDT", 100.0), ("ETHUSDT", 200.0)]:
        for index in range(periods):
            close = base_close + index + (0.5 if index % 5 == 0 else -0.25)
            rows.append(
                {
                    "exchange": "binance",
                    "symbol": symbol,
                    "timeframe": "1d",
                    "timestamp": pd.Timestamp("2026-01-01T00:00:00Z")
                    + pd.Timedelta(days=index),
                    "open": close - 0.25,
                    "high": close + 1.0,
                    "low": close - 1.0,
                    "close": close,
                    "volume": 10.0 + index,
                }
            )
    return pd.DataFrame(rows)


def _past_slice(df: pd.DataFrame, symbol: str, through_index: int, columns: list[str]) -> pd.DataFrame:
    timestamps = sorted(df.loc[df["symbol"] == symbol, "timestamp"].unique())
    through_timestamp = timestamps[through_index]
    return (
        df[(df["symbol"] == symbol) & (df["timestamp"] <= through_timestamp)]
        .sort_values("timestamp")
        .reset_index(drop=True)
        .loc[:, columns]
    )


def test_returns_do_not_change_when_future_rows_change() -> None:
    base = _ohlcv_dataframe()
    mutated = base.copy()
    mutated.loc[mutated["timestamp"] > pd.Timestamp("2026-02-15T00:00:00Z"), "close"] *= 10

    columns = ["simple_return", "log_return", "close_open_return"]
    expected = _past_slice(calculate_return_features(base), "BTCUSDT", 45, columns)
    actual = _past_slice(calculate_return_features(mutated), "BTCUSDT", 45, columns)

    pd.testing.assert_frame_equal(actual, expected)


def test_trend_features_do_not_change_when_future_rows_change() -> None:
    base = _ohlcv_dataframe()
    mutated = base.copy()
    future_mask = mutated["timestamp"] > pd.Timestamp("2026-02-20T00:00:00Z")
    mutated.loc[future_mask, ["close", "high", "low"]] *= 5

    columns = ["sma_20", "sma_50", "ema_20", "ema_50", "sma20_slope"]
    expected = _past_slice(calculate_trend_features(base), "BTCUSDT", 50, columns)
    actual = _past_slice(calculate_trend_features(mutated), "BTCUSDT", 50, columns)

    pd.testing.assert_frame_equal(actual, expected)


def test_breakout_context_does_not_change_when_future_rows_change() -> None:
    base = _ohlcv_dataframe()
    mutated = base.copy()
    future_mask = mutated["timestamp"] > pd.Timestamp("2026-02-15T00:00:00Z")
    mutated.loc[future_mask, ["high", "low", "close"]] *= 20

    columns = ["close_vs_high_52w", "rolling_max_20", "rolling_min_20"]
    expected = _past_slice(calculate_breakout_context_features(base), "BTCUSDT", 45, columns)
    actual = _past_slice(calculate_breakout_context_features(mutated), "BTCUSDT", 45, columns)

    pd.testing.assert_frame_equal(actual, expected)


def test_group_isolation_when_other_symbol_future_rows_change() -> None:
    base = _ohlcv_dataframe()
    mutated = base.copy()
    eth_future_mask = (mutated["symbol"] == "ETHUSDT") & (
        mutated["timestamp"] > pd.Timestamp("2026-02-01T00:00:00Z")
    )
    mutated.loc[eth_future_mask, ["high", "low", "close", "volume"]] *= 50

    columns = ["sma_20", "sma_50", "ema_20", "ema_50", "sma20_slope"]
    expected = _past_slice(calculate_trend_features(base), "BTCUSDT", 60, columns)
    actual = _past_slice(calculate_trend_features(mutated), "BTCUSDT", 60, columns)

    pd.testing.assert_frame_equal(actual, expected)
