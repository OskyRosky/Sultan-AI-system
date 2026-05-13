from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from trend import calculate_trend_features


def _ohlcv_dataframe() -> pd.DataFrame:
    rows = []
    for symbol, timeframe, base_close in [
        ("BTCUSDT", "1d", 100.0),
        ("ETHUSDT", "4h", 200.0),
    ]:
        for index in range(60):
            close = base_close + index
            rows.append(
                {
                    "exchange": "binance",
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "timestamp": pd.Timestamp("2026-01-01T00:00:00Z")
                    + pd.Timedelta(hours=index if timeframe == "4h" else index * 24),
                    "open": close - 0.5,
                    "high": close + 1.0,
                    "low": close - 1.0,
                    "close": close,
                    "volume": 10.0 + index,
                }
            )
    return pd.DataFrame(rows)


def test_calculate_trend_adds_expected_columns() -> None:
    result = calculate_trend_features(_ohlcv_dataframe())

    for column in [
        "sma_20",
        "sma_50",
        "ema_20",
        "ema_50",
        "price_above_sma20",
        "sma20_slope",
        "ema20_above_ema50",
    ]:
        assert column in result.columns


def test_sma_20_is_correct() -> None:
    result = calculate_trend_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert np.isclose(btc.loc[19, "sma_20"], np.mean(np.arange(100.0, 120.0)))


def test_sma_50_is_correct() -> None:
    result = calculate_trend_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert np.isclose(btc.loc[49, "sma_50"], np.mean(np.arange(100.0, 150.0)))


def test_ema_columns_are_created_without_infinite_values() -> None:
    result = calculate_trend_features(_ohlcv_dataframe())
    values = result[["ema_20", "ema_50"]].to_numpy()

    assert not np.isinf(values[~pd.isna(values)]).any()


def test_price_above_sma20_is_correct_after_warmup() -> None:
    result = calculate_trend_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert btc.loc[19, "price_above_sma20"] == True


def test_sma20_slope_is_correct() -> None:
    result = calculate_trend_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert np.isclose(btc.loc[20, "sma20_slope"], 1.0)


def test_ema20_above_ema50_is_neutral_state_not_signal() -> None:
    result = calculate_trend_features(_ohlcv_dataframe())

    assert "ema20_above_ema50" in result.columns
    assert "signal" not in result.columns
    assert "cross" not in result.columns
    assert result["ema20_above_ema50"].dropna().isin([True, False]).all()


def test_trend_is_grouped_by_symbol_and_timeframe() -> None:
    result = calculate_trend_features(_ohlcv_dataframe())
    eth = result[result["symbol"] == "ETHUSDT"].reset_index(drop=True)

    assert pd.isna(eth.loc[18, "sma_20"])
    assert np.isclose(eth.loc[19, "sma_20"], np.mean(np.arange(200.0, 220.0)))


def test_original_dataframe_is_not_modified() -> None:
    df = _ohlcv_dataframe()
    original_columns = list(df.columns)

    calculate_trend_features(df)

    assert list(df.columns) == original_columns


def test_warmup_periods_are_nan_for_sma_features() -> None:
    result = calculate_trend_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert btc.loc[:18, "sma_20"].isna().all()
    assert btc.loc[:48, "sma_50"].isna().all()
    assert pd.isna(btc.loc[19, "sma20_slope"])
