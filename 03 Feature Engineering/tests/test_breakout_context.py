from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from breakout_context import calculate_breakout_context_features


def _ohlcv_dataframe(periods: int = 365, timeframe: str = "1d") -> pd.DataFrame:
    rows = []
    for symbol, base_close in [("BTCUSDT", 100.0), ("ETHUSDT", 200.0)]:
        for index in range(periods):
            close = base_close + index
            rows.append(
                {
                    "exchange": "binance",
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "timestamp": pd.Timestamp("2025-01-01T00:00:00Z")
                    + pd.Timedelta(hours=index * 4 if timeframe == "4h" else index * 24),
                    "open": close - 0.5,
                    "high": close + 2.0,
                    "low": close - 2.0,
                    "close": close,
                    "volume": 10.0 + index,
                }
            )
    return pd.DataFrame(rows)


def test_calculate_breakout_context_adds_expected_columns() -> None:
    result = calculate_breakout_context_features(_ohlcv_dataframe(periods=40))

    assert "close_vs_high_52w" in result.columns
    assert "rolling_max_20" in result.columns
    assert "rolling_min_20" in result.columns


def test_rolling_max_20_uses_high_and_is_correct() -> None:
    result = calculate_breakout_context_features(_ohlcv_dataframe(periods=40))
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert np.isclose(btc.loc[19, "rolling_max_20"], 121.0)


def test_rolling_min_20_uses_low_and_is_correct() -> None:
    result = calculate_breakout_context_features(_ohlcv_dataframe(periods=40))
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert np.isclose(btc.loc[19, "rolling_min_20"], 98.0)


def test_close_vs_high_52w_for_1d_is_correct_with_365_periods() -> None:
    result = calculate_breakout_context_features(_ohlcv_dataframe(periods=365))
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert np.isclose(btc.loc[364, "close_vs_high_52w"], 464.0 / 466.0)


def test_close_vs_high_52w_for_4h_uses_2190_periods() -> None:
    result = calculate_breakout_context_features(
        _ohlcv_dataframe(periods=2190, timeframe="4h")
    )
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert pd.isna(btc.loc[2188, "close_vs_high_52w"])
    assert np.isclose(btc.loc[2189, "close_vs_high_52w"], 2289.0 / 2291.0)


def test_breakout_context_is_grouped_by_symbol_and_timeframe() -> None:
    result = calculate_breakout_context_features(_ohlcv_dataframe(periods=40))
    eth = result[result["symbol"] == "ETHUSDT"].reset_index(drop=True)

    assert pd.isna(eth.loc[18, "rolling_max_20"])
    assert np.isclose(eth.loc[19, "rolling_max_20"], 221.0)


def test_original_dataframe_is_not_modified() -> None:
    df = _ohlcv_dataframe(periods=40)
    original_columns = list(df.columns)

    calculate_breakout_context_features(df)

    assert list(df.columns) == original_columns


def test_no_infinite_values_for_valid_positive_prices() -> None:
    result = calculate_breakout_context_features(_ohlcv_dataframe(periods=365))
    values = result[
        ["close_vs_high_52w", "rolling_max_20", "rolling_min_20"]
    ].to_numpy()

    assert not np.isinf(values[~pd.isna(values)]).any()


def test_warmup_periods_are_nan() -> None:
    result = calculate_breakout_context_features(_ohlcv_dataframe(periods=365))
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert btc.loc[:18, "rolling_max_20"].isna().all()
    assert btc.loc[:18, "rolling_min_20"].isna().all()
    assert btc.loc[:363, "close_vs_high_52w"].isna().all()


def test_auxiliary_rolling_high_52w_not_in_output() -> None:
    result = calculate_breakout_context_features(_ohlcv_dataframe(periods=365))

    assert "rolling_high_52w" not in result.columns
