from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from feature_quality import validate_return_features
from returns import calculate_return_features


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
