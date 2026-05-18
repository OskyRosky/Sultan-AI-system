from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "research" / "research_dataset_builder.py"
SPEC = importlib.util.spec_from_file_location("research_dataset_builder", MODULE_PATH)
research_dataset_builder = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(research_dataset_builder)


def _features_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "symbol": ["BTCUSDT", "BTCUSDT", "ETHUSDT", "BTCUSDT"],
            "timeframe": ["1h", "1h", "1h", "4h"],
            "timestamp": pd.to_datetime(
                [
                    "2026-01-01 00:00:00",
                    "2026-01-01 01:00:00",
                    "2026-01-01 00:00:00",
                    "2026-01-01 00:00:00",
                ]
            ),
            "feature_rsi_14": [45.0, 55.0, 35.0, 65.0],
            "feature_atr_14": [10.0, 11.0, 12.0, 13.0],
        }
    )


def _forward_returns_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "symbol": ["BTCUSDT", "BTCUSDT", "ETHUSDT", "BTCUSDT"],
            "timeframe": ["1h", "1h", "1h", "4h"],
            "timestamp": pd.to_datetime(
                [
                    "2026-01-01 00:00:00",
                    "2026-01-01 01:00:00",
                    "2026-01-01 00:00:00",
                    "2026-01-01 00:00:00",
                ]
            ),
            "forward_return_1": [0.01, None, -0.02, 0.04],
            "forward_return_3": [0.03, None, -0.01, 0.08],
            "close": [100.0, 101.0, 200.0, 105.0],
        }
    )


def test_build_research_dataset_joins_by_symbol_timeframe_timestamp() -> None:
    result = research_dataset_builder.build_research_dataset(
        _features_frame(),
        _forward_returns_frame(),
    )

    assert result.columns.tolist() == [
        "symbol",
        "timeframe",
        "timestamp",
        "feature_rsi_14",
        "feature_atr_14",
        "forward_return_1",
        "forward_return_3",
    ]
    assert len(result) == 4
    btc_1h_first = result[
        result["symbol"].eq("BTCUSDT")
        & result["timeframe"].eq("1h")
        & result["timestamp"].eq(pd.Timestamp("2026-01-01 00:00:00"))
    ].iloc[0]
    assert btc_1h_first["feature_rsi_14"] == pytest.approx(45.0)
    assert btc_1h_first["forward_return_1"] == pytest.approx(0.01)


def test_duplicate_feature_keys_are_rejected() -> None:
    features = _features_frame()
    features = pd.concat([features, features.iloc[[0]]], ignore_index=True)

    with pytest.raises(ValueError, match="features duplicate rows"):
        research_dataset_builder.build_research_dataset(features, _forward_returns_frame())


def test_duplicate_forward_return_keys_are_rejected() -> None:
    labels = _forward_returns_frame()
    labels = pd.concat([labels, labels.iloc[[0]]], ignore_index=True)

    with pytest.raises(ValueError, match="forward_returns duplicate rows"):
        research_dataset_builder.build_research_dataset(_features_frame(), labels)


def test_symbols_are_not_mixed_when_timestamps_match() -> None:
    result = research_dataset_builder.build_research_dataset(
        _features_frame(),
        _forward_returns_frame(),
    )

    eth_row = result[result["symbol"].eq("ETHUSDT")].iloc[0]
    assert eth_row["feature_rsi_14"] == pytest.approx(35.0)
    assert eth_row["forward_return_1"] == pytest.approx(-0.02)


def test_timeframes_are_not_mixed_when_symbol_and_timestamp_match() -> None:
    result = research_dataset_builder.build_research_dataset(
        _features_frame(),
        _forward_returns_frame(),
    )

    four_hour_row = result[result["timeframe"].eq("4h")].iloc[0]
    assert four_hour_row["feature_rsi_14"] == pytest.approx(65.0)
    assert four_hour_row["forward_return_1"] == pytest.approx(0.04)


def test_feature_and_forward_return_columns_are_preserved_without_extra_label_inputs() -> None:
    result = research_dataset_builder.build_research_dataset(
        _features_frame(),
        _forward_returns_frame(),
    )

    assert "feature_rsi_14" in result.columns
    assert "feature_atr_14" in result.columns
    assert "forward_return_1" in result.columns
    assert "forward_return_3" in result.columns
    assert "close" not in result.columns


def test_terminal_nan_forward_returns_are_preserved() -> None:
    result = research_dataset_builder.build_research_dataset(
        _features_frame(),
        _forward_returns_frame(),
    )

    terminal_row = result[
        result["symbol"].eq("BTCUSDT")
        & result["timeframe"].eq("1h")
        & result["timestamp"].eq(pd.Timestamp("2026-01-01 01:00:00"))
    ].iloc[0]
    assert pd.isna(terminal_row["forward_return_1"])
    assert pd.isna(terminal_row["forward_return_3"])


def test_missing_required_feature_columns_raise_clear_error() -> None:
    features = _features_frame().drop(columns=["timeframe"])

    with pytest.raises(ValueError, match="features missing required columns"):
        research_dataset_builder.build_research_dataset(features, _forward_returns_frame())


def test_missing_required_forward_return_columns_raise_clear_error() -> None:
    labels = _forward_returns_frame().drop(columns=["timestamp"])

    with pytest.raises(ValueError, match="forward_returns missing required columns"):
        research_dataset_builder.build_research_dataset(_features_frame(), labels)


def test_missing_forward_return_label_columns_raise_clear_error() -> None:
    labels = _forward_returns_frame().drop(columns=["forward_return_1", "forward_return_3"])

    with pytest.raises(ValueError, match="at least one 'forward_return_' column"):
        research_dataset_builder.build_research_dataset(_features_frame(), labels)


def test_research_dataset_columns_are_predictable() -> None:
    assert research_dataset_builder.research_dataset_columns(
        _features_frame(),
        _forward_returns_frame(),
    ) == [
        "symbol",
        "timeframe",
        "timestamp",
        "feature_rsi_14",
        "feature_atr_14",
        "forward_return_1",
        "forward_return_3",
    ]
