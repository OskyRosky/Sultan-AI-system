from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

FEATURES_DIR = Path(__file__).resolve().parents[1] / "features"
if str(FEATURES_DIR) not in sys.path:
    sys.path.insert(0, str(FEATURES_DIR))

from breakout_context import calculate_breakout_context_features
from candle_structure import calculate_candle_structure_features
from integrated_feature_quality import (
    EXPECTED_FEATURE_COLUMNS,
    EXPECTED_FEATURE_COLUMNS_BY_FAMILY,
    validate_integrated_feature_dataset,
)
from momentum import calculate_momentum_features
from returns import calculate_return_features
from trend import calculate_trend_features
from volatility import calculate_volatility_features
from volume import calculate_volume_features


def _ohlcv_dataframe() -> pd.DataFrame:
    rows = []
    for symbol in ["BTCUSDT", "ETHUSDT"]:
        for index in range(80):
            open_price = 100.0 + index
            close = open_price + (0.5 if index % 2 == 0 else -0.25)
            rows.append(
                {
                    "exchange": "binance",
                    "symbol": symbol,
                    "timeframe": "1d",
                    "timestamp": pd.Timestamp("2026-01-01T00:00:00Z")
                    + pd.Timedelta(days=index),
                    "open": open_price,
                    "high": max(open_price, close) + 1.0,
                    "low": min(open_price, close) - 1.0,
                    "close": close,
                    "volume": 10.0 + index,
                }
            )
    return pd.DataFrame(rows)


def _integrated_feature_dataframe() -> pd.DataFrame:
    features = calculate_return_features(_ohlcv_dataframe())
    features = calculate_trend_features(features)
    features = calculate_volatility_features(features)
    features = calculate_momentum_features(features)
    features = calculate_breakout_context_features(features)
    features = calculate_volume_features(features)
    return calculate_candle_structure_features(features)


def test_valid_integrated_feature_dataset_passes() -> None:
    result = validate_integrated_feature_dataset(_integrated_feature_dataframe())

    assert result["status"] == "passed"
    assert result["ready_for_storage"] is True
    assert result["blocking_errors"] == []


def test_missing_expected_feature_column_fails() -> None:
    df = _integrated_feature_dataframe().drop(columns=["simple_return"])

    result = validate_integrated_feature_dataset(df)

    assert result["status"] == "failed"
    assert "simple_return" in result["missing_columns"]


def test_forbidden_signal_column_fails() -> None:
    df = _integrated_feature_dataframe()
    df["signal"] = False

    result = validate_integrated_feature_dataset(df)

    assert result["status"] == "failed"
    assert result["forbidden_columns_found"] == ["signal"]


def test_duplicate_feature_row_fails() -> None:
    df = _integrated_feature_dataframe()
    duplicated = pd.concat([df, df.iloc[[0]]], ignore_index=True)

    result = validate_integrated_feature_dataset(duplicated)

    assert result["status"] == "failed"
    assert result["duplicate_count"] == 1


def test_infinite_feature_value_fails() -> None:
    df = _integrated_feature_dataframe()
    df.loc[10, "simple_return"] = np.inf

    result = validate_integrated_feature_dataset(df)

    assert result["status"] == "failed"
    assert result["infinite_count"] == 1


def test_missing_feature_set_fails() -> None:
    df = _integrated_feature_dataframe().drop(columns=["feature_set"])

    result = validate_integrated_feature_dataset(df)

    assert result["status"] == "failed"
    assert "feature_set" in result["missing_columns"]


def test_invalid_feature_set_fails() -> None:
    df = _integrated_feature_dataframe()
    df["feature_set"] = "technical_v2"

    result = validate_integrated_feature_dataset(df)

    assert result["status"] == "failed"
    assert "invalid_feature_set_expected_technical_v1" in result["blocking_errors"]


def test_missing_feature_version_fails() -> None:
    df = _integrated_feature_dataframe().drop(columns=["feature_version"])

    result = validate_integrated_feature_dataset(df)

    assert result["status"] == "failed"
    assert "feature_version" in result["missing_columns"]


def test_invalid_feature_version_fails() -> None:
    df = _integrated_feature_dataframe()
    df["feature_version"] = "1.1.0"

    result = validate_integrated_feature_dataset(df)

    assert result["status"] == "failed"
    assert "invalid_feature_version_expected_1.0.0" in result["blocking_errors"]


def test_ready_for_storage_true_when_clean() -> None:
    result = validate_integrated_feature_dataset(_integrated_feature_dataframe())

    assert result["ready_for_storage"] is True


def test_ready_for_storage_false_when_blocking_errors() -> None:
    df = _integrated_feature_dataframe().drop(columns=["macd"])

    result = validate_integrated_feature_dataset(df)

    assert result["ready_for_storage"] is False


def test_data_quality_score_between_0_and_1() -> None:
    result = validate_integrated_feature_dataset(_integrated_feature_dataframe())

    assert 0.0 <= result["data_quality_score"] <= 1.0


def test_family_summary_contains_all_families() -> None:
    result = validate_integrated_feature_dataset(_integrated_feature_dataframe())

    assert set(result["family_summary"]) == set(EXPECTED_FEATURE_COLUMNS_BY_FAMILY)
    assert len(EXPECTED_FEATURE_COLUMNS) == 27


def test_symbol_timeframe_summary_is_created() -> None:
    result = validate_integrated_feature_dataset(_integrated_feature_dataframe())

    assert "BTCUSDT|1d" in result["symbol_timeframe_summary"]
    assert result["symbol_timeframe_summary"]["BTCUSDT|1d"]["row_count"] == 80
