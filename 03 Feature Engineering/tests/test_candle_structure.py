from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from candle_structure import calculate_candle_structure_features


def _ohlcv_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "exchange": "binance",
                "symbol": "BTCUSDT",
                "timeframe": "1d",
                "timestamp": "2026-01-01T00:00:00Z",
                "open": 100.0,
                "high": 112.0,
                "low": 95.0,
                "close": 108.0,
                "volume": 1000.0,
            },
            {
                "exchange": "binance",
                "symbol": "BTCUSDT",
                "timeframe": "1d",
                "timestamp": "2026-01-02T00:00:00Z",
                "open": 108.0,
                "high": 110.0,
                "low": 101.0,
                "close": 103.0,
                "volume": 1010.0,
            },
        ]
    )


def test_calculate_candle_structure_adds_expected_columns() -> None:
    result = calculate_candle_structure_features(_ohlcv_dataframe())

    for column in [
        "high_low_range",
        "body_size",
        "upper_wick",
        "lower_wick",
        "body_to_range_ratio",
    ]:
        assert column in result.columns


def test_high_low_range_is_correct() -> None:
    result = calculate_candle_structure_features(_ohlcv_dataframe())

    assert result.loc[0, "high_low_range"] == 17.0


def test_body_size_is_correct() -> None:
    result = calculate_candle_structure_features(_ohlcv_dataframe())

    assert result.loc[0, "body_size"] == 8.0


def test_upper_wick_is_correct() -> None:
    result = calculate_candle_structure_features(_ohlcv_dataframe())

    assert result.loc[0, "upper_wick"] == 4.0


def test_lower_wick_is_correct() -> None:
    result = calculate_candle_structure_features(_ohlcv_dataframe())

    assert result.loc[0, "lower_wick"] == 5.0


def test_body_to_range_ratio_is_correct() -> None:
    result = calculate_candle_structure_features(_ohlcv_dataframe())

    assert np.isclose(result.loc[0, "body_to_range_ratio"], 8.0 / 17.0)


def test_body_to_range_ratio_nan_when_range_zero() -> None:
    df = _ohlcv_dataframe()
    df.loc[0, ["high", "low", "open", "close"]] = 100.0

    result = calculate_candle_structure_features(df)

    assert pd.isna(result.loc[0, "body_to_range_ratio"])


def test_original_dataframe_is_not_modified() -> None:
    df = _ohlcv_dataframe()
    original_columns = list(df.columns)

    calculate_candle_structure_features(df)

    assert list(df.columns) == original_columns


def test_no_infinite_values_for_valid_ohlcv() -> None:
    result = calculate_candle_structure_features(_ohlcv_dataframe())
    values = result[
        [
            "high_low_range",
            "body_size",
            "upper_wick",
            "lower_wick",
            "body_to_range_ratio",
        ]
    ].to_numpy()

    assert not np.isinf(values[~pd.isna(values)]).any()


def test_no_auxiliary_columns_in_output() -> None:
    result = calculate_candle_structure_features(_ohlcv_dataframe())

    assert "open_close_max" not in result.columns
    assert "open_close_min" not in result.columns
