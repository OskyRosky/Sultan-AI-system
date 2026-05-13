from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from returns import calculate_return_features


def _ohlcv_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "exchange": "binance",
                "symbol": "BTCUSDT",
                "timeframe": "1d",
                "timestamp": "2026-05-10T00:00:00Z",
                "open": 100.0,
                "high": 105.0,
                "low": 95.0,
                "close": 100.0,
                "volume": 10.0,
            },
            {
                "exchange": "binance",
                "symbol": "BTCUSDT",
                "timeframe": "1d",
                "timestamp": "2026-05-11T00:00:00Z",
                "open": 100.0,
                "high": 112.0,
                "low": 99.0,
                "close": 110.0,
                "volume": 11.0,
            },
            {
                "exchange": "binance",
                "symbol": "ETHUSDT",
                "timeframe": "4h",
                "timestamp": "2026-05-10T00:00:00Z",
                "open": 200.0,
                "high": 205.0,
                "low": 195.0,
                "close": 200.0,
                "volume": 20.0,
            },
            {
                "exchange": "binance",
                "symbol": "ETHUSDT",
                "timeframe": "4h",
                "timestamp": "2026-05-10T04:00:00Z",
                "open": 200.0,
                "high": 212.0,
                "low": 198.0,
                "close": 210.0,
                "volume": 21.0,
            },
        ]
    )


def test_calculate_returns_adds_expected_columns() -> None:
    result = calculate_return_features(_ohlcv_dataframe())

    assert "simple_return" in result.columns
    assert "log_return" in result.columns
    assert "close_open_return" in result.columns
    assert "feature_set" in result.columns
    assert "feature_version" in result.columns


def test_simple_return_is_correct() -> None:
    result = calculate_return_features(_ohlcv_dataframe())
    btc_second_row = result[(result["symbol"] == "BTCUSDT")].iloc[1]

    assert np.isclose(btc_second_row["simple_return"], 0.10)


def test_log_return_is_correct() -> None:
    result = calculate_return_features(_ohlcv_dataframe())
    btc_second_row = result[(result["symbol"] == "BTCUSDT")].iloc[1]

    assert np.isclose(btc_second_row["log_return"], np.log(1.10))


def test_close_open_return_is_correct() -> None:
    result = calculate_return_features(_ohlcv_dataframe())
    btc_second_row = result[(result["symbol"] == "BTCUSDT")].iloc[1]

    assert np.isclose(btc_second_row["close_open_return"], 0.10)


def test_first_row_group_returns_are_nan() -> None:
    result = calculate_return_features(_ohlcv_dataframe())
    first_rows = result.groupby(["exchange", "symbol", "timeframe"]).head(1)

    assert first_rows["simple_return"].isna().all()
    assert first_rows["log_return"].isna().all()


def test_returns_are_grouped_by_symbol_and_timeframe() -> None:
    result = calculate_return_features(_ohlcv_dataframe())
    eth_first_row = result[result["symbol"] == "ETHUSDT"].iloc[0]
    eth_second_row = result[result["symbol"] == "ETHUSDT"].iloc[1]

    assert pd.isna(eth_first_row["simple_return"])
    assert np.isclose(eth_second_row["simple_return"], 0.05)


def test_original_dataframe_is_not_modified() -> None:
    df = _ohlcv_dataframe()
    original_columns = list(df.columns)

    calculate_return_features(df)

    assert list(df.columns) == original_columns


def test_no_infinite_values_for_valid_positive_prices() -> None:
    result = calculate_return_features(_ohlcv_dataframe())
    values = result[["simple_return", "log_return", "close_open_return"]].to_numpy()

    assert not np.isinf(values[~pd.isna(values)]).any()
