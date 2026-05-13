from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from ohlcv_validation import validate_ohlcv_dataframe


def _valid_ohlcv_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "exchange": "binance",
                "symbol": "BTCUSDT",
                "timeframe": "1d",
                "timestamp": pd.Timestamp("2026-05-10T00:00:00Z"),
                "open": 100.0,
                "high": 110.0,
                "low": 95.0,
                "close": 105.0,
                "volume": 10.0,
            },
            {
                "exchange": "binance",
                "symbol": "BTCUSDT",
                "timeframe": "1d",
                "timestamp": pd.Timestamp("2026-05-11T00:00:00Z"),
                "open": 105.0,
                "high": 112.0,
                "low": 101.0,
                "close": 108.0,
                "volume": 12.0,
            },
        ]
    )


def test_valid_ohlcv_dataframe_passes() -> None:
    result = validate_ohlcv_dataframe(_valid_ohlcv_dataframe())

    assert result.passed is True
    assert result.status == "passed"
    assert result.errors == []


def test_missing_required_column_fails() -> None:
    df = _valid_ohlcv_dataframe().drop(columns=["volume"])

    result = validate_ohlcv_dataframe(df)

    assert result.passed is False
    assert "missing_required_columns=['volume']" in result.errors


def test_duplicate_timestamp_fails() -> None:
    df = pd.concat([_valid_ohlcv_dataframe(), _valid_ohlcv_dataframe().iloc[[0]]])
    df = df.sort_values(["symbol", "timeframe", "timestamp"]).reset_index(drop=True)

    result = validate_ohlcv_dataframe(df)

    assert result.passed is False
    assert "duplicate_bars=1" in result.errors


def test_invalid_ohlc_relationship_fails() -> None:
    df = _valid_ohlcv_dataframe()
    df.loc[0, "high"] = 90.0

    result = validate_ohlcv_dataframe(df)

    assert result.passed is False
    assert "high_lt_low" in result.errors
    assert "high_lt_open" in result.errors
    assert "high_lt_close" in result.errors


def test_negative_volume_fails() -> None:
    df = _valid_ohlcv_dataframe()
    df.loc[0, "volume"] = -1.0

    result = validate_ohlcv_dataframe(df)

    assert result.passed is False
    assert "volume_negative" in result.errors
