from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from feature_quality import (
    validate_return_features,
    validate_trend_features,
    validate_volatility_features,
    validate_momentum_features,
    validate_breakout_context_features,
    validate_volume_features,
    validate_candle_structure_features,
)
from returns import calculate_return_features
from trend import calculate_trend_features
from volatility import calculate_volatility_features
from momentum import calculate_momentum_features
from breakout_context import calculate_breakout_context_features
from volume import calculate_volume_features
from candle_structure import calculate_candle_structure_features


def _feature_dataframe() -> pd.DataFrame:
    ohlcv = pd.DataFrame(
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
        ]
    )
    return calculate_return_features(ohlcv)


def test_valid_returns_features_pass_quality() -> None:
    result = validate_return_features(_feature_dataframe())

    assert result["passed"] is True
    assert result["status"] == "passed"
    assert result["errors"] == []


def test_missing_return_column_fails_quality() -> None:
    df = _feature_dataframe().drop(columns=["log_return"])

    result = validate_return_features(df)

    assert result["passed"] is False
    assert "missing_return_columns=['log_return']" in result["errors"]


def test_infinite_return_fails_quality() -> None:
    df = _feature_dataframe()
    df.loc[1, "simple_return"] = np.inf

    result = validate_return_features(df)

    assert result["passed"] is False
    assert "simple_return_contains_infinite" in result["errors"]


def test_duplicate_feature_row_fails_quality() -> None:
    df = pd.concat([_feature_dataframe(), _feature_dataframe().iloc[[0]]])

    result = validate_return_features(df)

    assert result["passed"] is False
    assert "duplicate_feature_rows=1" in result["errors"]


def test_forbidden_signal_column_fails_quality() -> None:
    df = _feature_dataframe()
    df["buy_signal"] = False

    result = validate_return_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['buy_signal']" in result["errors"]


def test_missing_feature_set_or_version_fails_quality() -> None:
    df = _feature_dataframe()
    df.loc[0, "feature_set"] = None
    df.loc[1, "feature_version"] = ""

    result = validate_return_features(df)

    assert result["passed"] is False
    assert "feature_set_null_or_empty" in result["errors"]
    assert "feature_version_null_or_empty" in result["errors"]


def _trend_feature_dataframe() -> pd.DataFrame:
    rows = []
    for index in range(60):
        close = 100.0 + index
        rows.append(
            {
                "exchange": "binance",
                "symbol": "BTCUSDT",
                "timeframe": "1d",
                "timestamp": pd.Timestamp("2026-01-01T00:00:00Z")
                + pd.Timedelta(days=index),
                "open": close - 0.5,
                "high": close + 1.0,
                "low": close - 1.0,
                "close": close,
                "volume": 10.0 + index,
            }
        )
    return calculate_trend_features(calculate_return_features(pd.DataFrame(rows)))


def test_valid_trend_features_pass_quality() -> None:
    result = validate_trend_features(_trend_feature_dataframe())

    assert result["passed"] is True
    assert result["status"] == "passed"
    assert result["errors"] == []


def test_missing_trend_column_fails_quality_when_required() -> None:
    df = _trend_feature_dataframe().drop(columns=["sma_20"])

    result = validate_trend_features(df)

    assert result["passed"] is False
    assert "missing_trend_columns=['sma_20']" in result["errors"]


def test_infinite_trend_value_fails_quality() -> None:
    df = _trend_feature_dataframe()
    df.loc[50, "ema_20"] = np.inf

    result = validate_trend_features(df)

    assert result["passed"] is False
    assert "ema_20_contains_infinite" in result["errors"]


def test_invalid_price_above_sma20_state_fails_quality() -> None:
    df = _trend_feature_dataframe()
    df["price_above_sma20"] = df["price_above_sma20"].astype("object")
    df.loc[50, "price_above_sma20"] = "BUY"

    result = validate_trend_features(df)

    assert result["passed"] is False
    assert "price_above_sma20_invalid_state_values=1" in result["errors"]


def test_invalid_ema20_above_ema50_state_fails_quality() -> None:
    df = _trend_feature_dataframe()
    df["ema20_above_ema50"] = df["ema20_above_ema50"].astype("object")
    df.loc[50, "ema20_above_ema50"] = "BULLISH"

    result = validate_trend_features(df)

    assert result["passed"] is False
    assert "ema20_above_ema50_invalid_state_values=1" in result["errors"]


def test_ema_nan_is_reported_only_when_close_is_available() -> None:
    df = _trend_feature_dataframe()
    df.loc[10, "close"] = np.nan
    df.loc[10, "ema_20"] = np.nan
    df.loc[11, "ema_50"] = np.nan

    result = validate_trend_features(df)

    assert "ema_20_unexpected_nan=1" not in result["errors"]
    assert "ema_50_unexpected_nan=1" in result["errors"]


def test_forbidden_cross_column_fails_quality() -> None:
    df = _trend_feature_dataframe()
    df["cross"] = False

    result = validate_trend_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['cross']" in result["errors"]


def test_forbidden_crossover_column_fails_quality() -> None:
    df = _trend_feature_dataframe()
    df["crossover"] = False

    result = validate_trend_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['crossover']" in result["errors"]


def _volatility_feature_dataframe() -> pd.DataFrame:
    rows = []
    for index in range(60):
        close = 100.0 + index + (0.5 if index % 2 == 0 else -0.25)
        rows.append(
            {
                "exchange": "binance",
                "symbol": "BTCUSDT",
                "timeframe": "1d",
                "timestamp": pd.Timestamp("2026-01-01T00:00:00Z")
                + pd.Timedelta(days=index),
                "open": close - 0.5,
                "high": close + 2.0,
                "low": close - 1.0,
                "close": close,
                "volume": 10.0 + index,
            }
        )
    return calculate_volatility_features(
        calculate_trend_features(calculate_return_features(pd.DataFrame(rows)))
    )


def test_valid_volatility_features_pass_quality() -> None:
    result = validate_volatility_features(_volatility_feature_dataframe())

    assert result["passed"] is True
    assert result["status"] == "passed"
    assert result["errors"] == []


def test_missing_volatility_column_fails_quality_when_required() -> None:
    df = _volatility_feature_dataframe().drop(columns=["atr_14"])

    result = validate_volatility_features(df)

    assert result["passed"] is False
    assert "missing_volatility_columns=['atr_14']" in result["errors"]


def test_infinite_volatility_value_fails_quality() -> None:
    df = _volatility_feature_dataframe()
    df.loc[30, "rolling_std_20"] = np.inf

    result = validate_volatility_features(df)

    assert result["passed"] is False
    assert "rolling_std_20_contains_infinite" in result["errors"]


def test_negative_rolling_std_fails_quality() -> None:
    df = _volatility_feature_dataframe()
    df.loc[30, "rolling_std_20"] = -0.01

    result = validate_volatility_features(df)

    assert result["passed"] is False
    assert "rolling_std_20_contains_negative" in result["errors"]


def test_negative_volatility_20_fails_quality() -> None:
    df = _volatility_feature_dataframe()
    df.loc[30, "volatility_20"] = -0.01

    result = validate_volatility_features(df)

    assert result["passed"] is False
    assert "volatility_20_contains_negative" in result["errors"]


def test_negative_atr_14_fails_quality() -> None:
    df = _volatility_feature_dataframe()
    df.loc[30, "atr_14"] = -0.01

    result = validate_volatility_features(df)

    assert result["passed"] is False
    assert "atr_14_contains_negative" in result["errors"]


def test_volatility_20_not_equal_rolling_std_20_fails_quality() -> None:
    df = _volatility_feature_dataframe()
    df.loc[30, "volatility_20"] = df.loc[30, "rolling_std_20"] + 0.01

    result = validate_volatility_features(df)

    assert result["passed"] is False
    assert "volatility_20_not_equal_rolling_std_20" in result["errors"]


def _momentum_feature_dataframe() -> pd.DataFrame:
    rows = []
    for index in range(80):
        close = 100.0 + index + (0.5 if index % 3 == 0 else -0.25)
        rows.append(
            {
                "exchange": "binance",
                "symbol": "BTCUSDT",
                "timeframe": "1d",
                "timestamp": pd.Timestamp("2026-01-01T00:00:00Z")
                + pd.Timedelta(days=index),
                "open": close - 0.5,
                "high": close + 1.0,
                "low": close - 1.0,
                "close": close,
                "volume": 10.0 + index,
            }
        )
    return calculate_momentum_features(
        calculate_volatility_features(
            calculate_trend_features(calculate_return_features(pd.DataFrame(rows)))
        )
    )


def test_valid_momentum_features_pass_quality() -> None:
    result = validate_momentum_features(_momentum_feature_dataframe())

    assert result["passed"] is True
    assert result["status"] == "passed"
    assert result["errors"] == []


def test_missing_momentum_column_fails_quality_when_required() -> None:
    df = _momentum_feature_dataframe().drop(columns=["rsi_14"])

    result = validate_momentum_features(df)

    assert result["passed"] is False
    assert "missing_momentum_columns=['rsi_14']" in result["errors"]


def test_infinite_momentum_value_fails_quality() -> None:
    df = _momentum_feature_dataframe()
    df.loc[30, "macd"] = np.inf

    result = validate_momentum_features(df)

    assert result["passed"] is False
    assert "macd_contains_infinite" in result["errors"]


def test_rsi_below_0_fails_quality() -> None:
    df = _momentum_feature_dataframe()
    df.loc[30, "rsi_14"] = -1.0

    result = validate_momentum_features(df)

    assert result["passed"] is False
    assert "rsi_14_out_of_range" in result["errors"]


def test_rsi_above_100_fails_quality() -> None:
    df = _momentum_feature_dataframe()
    df.loc[30, "rsi_14"] = 101.0

    result = validate_momentum_features(df)

    assert result["passed"] is False
    assert "rsi_14_out_of_range" in result["errors"]


def test_forbidden_rsi_signal_column_fails_quality() -> None:
    df = _momentum_feature_dataframe()
    df["rsi_signal"] = 0

    result = validate_momentum_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['rsi_signal']" in result["errors"]


def test_forbidden_macd_cross_column_fails_quality() -> None:
    df = _momentum_feature_dataframe()
    df["macd_cross"] = False

    result = validate_momentum_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['macd_cross']" in result["errors"]


def test_forbidden_macd_signal_cross_column_fails_quality() -> None:
    df = _momentum_feature_dataframe()
    df["macd_signal_cross"] = False

    result = validate_momentum_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['macd_signal_cross']" in result["errors"]


def test_macd_nan_is_reported_only_when_close_is_available() -> None:
    df = _momentum_feature_dataframe()
    df.loc[10, "close"] = np.nan
    df.loc[10, "macd"] = np.nan
    df.loc[11, "macd_signal"] = np.nan

    result = validate_momentum_features(df)

    assert "macd_unexpected_nan=1" not in result["errors"]
    assert "macd_signal_unexpected_nan=1" in result["errors"]


def _breakout_context_feature_dataframe() -> pd.DataFrame:
    rows = []
    for index in range(365):
        close = 100.0 + index
        rows.append(
            {
                "exchange": "binance",
                "symbol": "BTCUSDT",
                "timeframe": "1d",
                "timestamp": pd.Timestamp("2025-01-01T00:00:00Z")
                + pd.Timedelta(days=index),
                "open": close - 0.5,
                "high": close + 2.0,
                "low": close - 2.0,
                "close": close,
                "volume": 10.0 + index,
            }
        )
    return calculate_breakout_context_features(pd.DataFrame(rows))


def test_valid_breakout_context_features_pass_quality() -> None:
    result = validate_breakout_context_features(_breakout_context_feature_dataframe())

    assert result["passed"] is True
    assert result["status"] == "passed"
    assert result["errors"] == []


def test_missing_breakout_context_column_fails_quality_when_required() -> None:
    df = _breakout_context_feature_dataframe().drop(columns=["rolling_min_20"])

    result = validate_breakout_context_features(df)

    assert result["passed"] is False
    assert "missing_breakout_context_columns=['rolling_min_20']" in result["errors"]


def test_infinite_breakout_context_value_fails_quality() -> None:
    df = _breakout_context_feature_dataframe()
    df.loc[30, "rolling_max_20"] = np.inf

    result = validate_breakout_context_features(df)

    assert result["passed"] is False
    assert "rolling_max_20_contains_infinite" in result["errors"]


def test_negative_close_vs_high_52w_fails_quality() -> None:
    df = _breakout_context_feature_dataframe()
    df.loc[364, "close_vs_high_52w"] = -0.1

    result = validate_breakout_context_features(df)

    assert result["passed"] is False
    assert "close_vs_high_52w_contains_negative" in result["errors"]


def test_negative_rolling_max_20_fails_quality() -> None:
    df = _breakout_context_feature_dataframe()
    df.loc[30, "rolling_max_20"] = -1.0

    result = validate_breakout_context_features(df)

    assert result["passed"] is False
    assert "rolling_max_20_contains_negative" in result["errors"]


def test_negative_rolling_min_20_fails_quality() -> None:
    df = _breakout_context_feature_dataframe()
    df.loc[30, "rolling_min_20"] = -1.0

    result = validate_breakout_context_features(df)

    assert result["passed"] is False
    assert "rolling_min_20_contains_negative" in result["errors"]


def test_forbidden_breakout_signal_column_fails_quality() -> None:
    df = _breakout_context_feature_dataframe()
    df["breakout_signal"] = False

    result = validate_breakout_context_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['breakout_signal']" in result["errors"]


def test_forbidden_support_resistance_columns_fail_quality() -> None:
    df = _breakout_context_feature_dataframe()
    df["support"] = 100.0
    df["resistance"] = 200.0

    result = validate_breakout_context_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['support', 'resistance']" in result["errors"]


def _volume_feature_dataframe() -> pd.DataFrame:
    rows = []
    for index in range(60):
        close = 100.0 + index
        rows.append(
            {
                "exchange": "binance",
                "symbol": "BTCUSDT",
                "timeframe": "1d",
                "timestamp": pd.Timestamp("2026-01-01T00:00:00Z")
                + pd.Timedelta(days=index),
                "open": close - 0.5,
                "high": close + 1.0,
                "low": close - 1.0,
                "close": close,
                "volume": 1000.0 + index * 10.0,
            }
        )
    return calculate_volume_features(pd.DataFrame(rows))


def test_valid_volume_features_pass_quality() -> None:
    result = validate_volume_features(_volume_feature_dataframe())

    assert result["passed"] is True
    assert result["status"] == "passed"
    assert result["errors"] == []


def test_missing_volume_column_fails_quality_when_required() -> None:
    df = _volume_feature_dataframe().drop(columns=["volume_ratio_20"])

    result = validate_volume_features(df)

    assert result["passed"] is False
    assert "missing_volume_columns=['volume_ratio_20']" in result["errors"]


def test_infinite_volume_value_fails_quality() -> None:
    df = _volume_feature_dataframe()
    df.loc[20, "volume_change"] = np.inf

    result = validate_volume_features(df)

    assert result["passed"] is False
    assert "volume_change_contains_infinite" in result["errors"]


def test_negative_volume_sma_20_fails_quality() -> None:
    df = _volume_feature_dataframe()
    df.loc[20, "volume_sma_20"] = -1.0

    result = validate_volume_features(df)

    assert result["passed"] is False
    assert "volume_sma_20_contains_negative" in result["errors"]


def test_negative_volume_ratio_20_fails_quality() -> None:
    df = _volume_feature_dataframe()
    df.loc[20, "volume_ratio_20"] = -1.0

    result = validate_volume_features(df)

    assert result["passed"] is False
    assert "volume_ratio_20_contains_negative" in result["errors"]


def test_forbidden_volume_signal_column_fails_quality() -> None:
    df = _volume_feature_dataframe()
    df["volume_signal"] = False

    result = validate_volume_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['volume_signal']" in result["errors"]


def test_forbidden_volume_spike_signal_column_fails_quality() -> None:
    df = _volume_feature_dataframe()
    df["volume_spike_signal"] = False

    result = validate_volume_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['volume_spike_signal']" in result["errors"]


def _candle_structure_feature_dataframe() -> pd.DataFrame:
    ohlcv = pd.DataFrame(
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
    return calculate_candle_structure_features(ohlcv)


def test_valid_candle_structure_features_pass_quality() -> None:
    result = validate_candle_structure_features(_candle_structure_feature_dataframe())

    assert result["passed"] is True
    assert result["status"] == "passed"
    assert result["errors"] == []


def test_missing_candle_structure_column_fails_quality_when_required() -> None:
    df = _candle_structure_feature_dataframe().drop(columns=["upper_wick"])

    result = validate_candle_structure_features(df)

    assert result["passed"] is False
    assert "missing_candle_structure_columns=['upper_wick']" in result["errors"]


def test_infinite_candle_structure_value_fails_quality() -> None:
    df = _candle_structure_feature_dataframe()
    df.loc[0, "body_size"] = np.inf

    result = validate_candle_structure_features(df)

    assert result["passed"] is False
    assert "body_size_contains_infinite" in result["errors"]


def test_negative_high_low_range_fails_quality() -> None:
    df = _candle_structure_feature_dataframe()
    df.loc[0, "high_low_range"] = -1.0

    result = validate_candle_structure_features(df)

    assert result["passed"] is False
    assert "high_low_range_contains_negative" in result["errors"]


def test_negative_body_size_fails_quality() -> None:
    df = _candle_structure_feature_dataframe()
    df.loc[0, "body_size"] = -1.0

    result = validate_candle_structure_features(df)

    assert result["passed"] is False
    assert "body_size_contains_negative" in result["errors"]


def test_negative_upper_wick_fails_quality() -> None:
    df = _candle_structure_feature_dataframe()
    df.loc[0, "upper_wick"] = -1.0

    result = validate_candle_structure_features(df)

    assert result["passed"] is False
    assert "upper_wick_contains_negative" in result["errors"]


def test_negative_lower_wick_fails_quality() -> None:
    df = _candle_structure_feature_dataframe()
    df.loc[0, "lower_wick"] = -1.0

    result = validate_candle_structure_features(df)

    assert result["passed"] is False
    assert "lower_wick_contains_negative" in result["errors"]


def test_body_to_range_ratio_above_1_fails_quality() -> None:
    df = _candle_structure_feature_dataframe()
    df.loc[0, "body_to_range_ratio"] = 1.1

    result = validate_candle_structure_features(df)

    assert result["passed"] is False
    assert "body_to_range_ratio_out_of_range" in result["errors"]


def test_forbidden_candle_signal_column_fails_quality() -> None:
    df = _candle_structure_feature_dataframe()
    df["candle_signal"] = False

    result = validate_candle_structure_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['candle_signal']" in result["errors"]


def test_forbidden_hammer_signal_column_fails_quality() -> None:
    df = _candle_structure_feature_dataframe()
    df["hammer_signal"] = False

    result = validate_candle_structure_features(df)

    assert result["passed"] is False
    assert "forbidden_columns=['hammer_signal']" in result["errors"]
