from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from returns import calculate_return_features
from volatility import calculate_volatility_features


def _ohlcv_dataframe() -> pd.DataFrame:
    rows = []
    for symbol, timeframe, base_close in [
        ("BTCUSDT", "1d", 100.0),
        ("ETHUSDT", "4h", 200.0),
    ]:
        for index in range(60):
            close = base_close + index + (0.5 if index % 2 == 0 else -0.25)
            rows.append(
                {
                    "exchange": "binance",
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "timestamp": pd.Timestamp("2026-01-01T00:00:00Z")
                    + pd.Timedelta(hours=index if timeframe == "4h" else index * 24),
                    "open": close - 0.5,
                    "high": close + 2.0,
                    "low": close - 1.0,
                    "close": close,
                    "volume": 10.0 + index,
                }
            )
    return pd.DataFrame(rows)


def test_calculate_volatility_adds_expected_columns() -> None:
    result = calculate_volatility_features(calculate_return_features(_ohlcv_dataframe()))

    assert "rolling_std_20" in result.columns
    assert "volatility_20" in result.columns
    assert "atr_14" in result.columns


def test_rolling_std_20_is_created() -> None:
    result = calculate_volatility_features(calculate_return_features(_ohlcv_dataframe()))
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert pd.notna(btc.loc[20, "rolling_std_20"])


def test_volatility_20_equals_rolling_std_20() -> None:
    result = calculate_volatility_features(calculate_return_features(_ohlcv_dataframe()))
    comparable = result[["rolling_std_20", "volatility_20"]].dropna()

    assert np.isclose(comparable["rolling_std_20"], comparable["volatility_20"]).all()


def test_atr_14_is_created() -> None:
    result = calculate_volatility_features(calculate_return_features(_ohlcv_dataframe()))
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert pd.notna(btc.loc[13, "atr_14"])


def test_atr_14_uses_previous_close_without_lookahead() -> None:
    df = _ohlcv_dataframe()
    result = calculate_volatility_features(calculate_return_features(df))
    btc_source = df[df["symbol"] == "BTCUSDT"].reset_index(drop=True)
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    true_ranges = []
    for index in range(14):
        high_low = btc_source.loc[index, "high"] - btc_source.loc[index, "low"]
        if index == 0:
            true_ranges.append(high_low)
            continue
        previous_close = btc_source.loc[index - 1, "close"]
        true_ranges.append(
            max(
                high_low,
                abs(btc_source.loc[index, "high"] - previous_close),
                abs(btc_source.loc[index, "low"] - previous_close),
            )
        )

    assert np.isclose(btc.loc[13, "atr_14"], np.mean(true_ranges))


def test_volatility_is_grouped_by_symbol_and_timeframe() -> None:
    result = calculate_volatility_features(calculate_return_features(_ohlcv_dataframe()))
    eth = result[result["symbol"] == "ETHUSDT"].reset_index(drop=True)

    assert eth.loc[:19, "rolling_std_20"].isna().all()
    assert pd.notna(eth.loc[20, "rolling_std_20"])


def test_original_dataframe_is_not_modified() -> None:
    df = _ohlcv_dataframe()
    original_columns = list(df.columns)

    calculate_volatility_features(df)

    assert list(df.columns) == original_columns


def test_no_infinite_values_for_valid_positive_prices() -> None:
    result = calculate_volatility_features(calculate_return_features(_ohlcv_dataframe()))
    values = result[["rolling_std_20", "volatility_20", "atr_14"]].to_numpy()

    assert not np.isinf(values[~pd.isna(values)]).any()


def test_warmup_periods_are_nan_for_rolling_std() -> None:
    result = calculate_volatility_features(calculate_return_features(_ohlcv_dataframe()))
    btc = result[result["symbol"] == "BTCUSDT"].reset_index(drop=True)

    assert btc.loc[:19, "rolling_std_20"].isna().all()
    assert btc.loc[:19, "volatility_20"].isna().all()


def test_atr_14_is_non_negative_after_warmup() -> None:
    result = calculate_volatility_features(calculate_return_features(_ohlcv_dataframe()))
    atr = result["atr_14"].dropna()

    assert (atr >= 0).all()
