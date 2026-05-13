from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from feature_quality import validate_return_features, validate_trend_features
from returns import calculate_return_features
from trend import calculate_trend_features


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
