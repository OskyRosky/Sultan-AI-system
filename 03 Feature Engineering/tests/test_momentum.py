from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from momentum import calculate_momentum_features


def _ohlcv_dataframe() -> pd.DataFrame:
    rows = []
    for symbol, timeframe, base_close in [
        ("BTCUSDT", "1d", 100.0),
        ("ETHUSDT", "4h", 200.0),
    ]:
        for index in range(80):
            close = base_close + index + (0.5 if index % 3 == 0 else -0.25)
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


def test_calculate_momentum_adds_expected_columns() -> None:
    result = calculate_momentum_features(_ohlcv_dataframe())

    assert "rsi_14" in result.columns
    assert "macd" in result.columns
    assert "macd_signal" in result.columns


def test_rsi_14_is_created() -> None:
    result = calculate_momentum_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert pd.notna(btc.loc[14, "rsi_14"])


def test_rsi_14_is_between_0_and_100_after_warmup() -> None:
    result = calculate_momentum_features(_ohlcv_dataframe())
    rsi = result["rsi_14"].dropna()

    assert ((rsi >= 0) & (rsi <= 100)).all()


def test_macd_is_ema12_minus_ema26() -> None:
    df = _ohlcv_dataframe()
    result = calculate_momentum_features(df)
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)
    close = df[df["symbol"] == "BTCUSDT"].reset_index(drop=True)["close"]
    expected = close.ewm(span=12, adjust=False).mean() - close.ewm(
        span=26, adjust=False
    ).mean()

    assert np.isclose(btc.loc[30, "macd"], expected.loc[30])


def test_macd_signal_is_created() -> None:
    result = calculate_momentum_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert pd.notna(btc.loc[0, "macd_signal"])


def test_momentum_is_grouped_by_symbol_and_timeframe() -> None:
    result = calculate_momentum_features(_ohlcv_dataframe())
    eth = result[result["symbol"] == "ETHUSDT"].reset_index(drop=True)

    assert eth.loc[:13, "rsi_14"].isna().all()
    assert pd.notna(eth.loc[14, "rsi_14"])


def test_original_dataframe_is_not_modified() -> None:
    df = _ohlcv_dataframe()
    original_columns = list(df.columns)

    calculate_momentum_features(df)

    assert list(df.columns) == original_columns


def test_no_infinite_values_for_valid_positive_prices() -> None:
    result = calculate_momentum_features(_ohlcv_dataframe())
    values = result[["rsi_14", "macd", "macd_signal"]].to_numpy()

    assert not np.isinf(values[~pd.isna(values)]).any()


def test_rsi_warmup_is_nan() -> None:
    result = calculate_momentum_features(_ohlcv_dataframe())
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert btc.loc[:13, "rsi_14"].isna().all()


def test_auxiliary_ema12_ema26_columns_not_in_output() -> None:
    result = calculate_momentum_features(_ohlcv_dataframe())

    assert "ema_12" not in result.columns
    assert "ema_26" not in result.columns
