from __future__ import annotations

import importlib.util
from pathlib import Path

import pandas as pd
import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "research" / "feature_profiling.py"
SPEC = importlib.util.spec_from_file_location("feature_profiling", MODULE_PATH)
feature_profiling = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(feature_profiling)


def _features_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "symbol": ["BTCUSDT"] * 6 + ["ETHUSDT"] * 4 + ["BTCUSDT"] * 4,
            "timeframe": ["1h"] * 10 + ["4h"] * 4,
            "timestamp": pd.date_range("2026-01-01", periods=14, freq="1h"),
            "feature_trend": [1, 2, 3, 4, 5, 100, 10, 11, 12, 13, 20, 21, 22, 23],
            "feature_trend_copy": [2, 4, 6, 8, 10, 200, 20, 22, 24, 26, 40, 42, 44, 46],
            "feature_with_nulls": [0, None, 0, 1, None, 1, 2, None, 2, 2, 3, 3, None, 3],
            "feature_constant": [7] * 14,
            "feature_all_nan": [None] * 14,
        }
    )


def _summary_row(result: object, *, symbol: str, timeframe: str, feature: str) -> pd.Series:
    summary = result.summary
    rows = summary[
        summary["symbol"].eq(symbol)
        & summary["timeframe"].eq(timeframe)
        & summary["feature"].eq(feature)
    ]
    assert len(rows) == 1
    return rows.iloc[0]


def test_basic_metrics_are_calculated_per_feature() -> None:
    result = feature_profiling.profile_features(_features_frame())

    row = _summary_row(result, symbol="ETHUSDT", timeframe="1h", feature="feature_trend")

    assert row["count"] == 4
    assert row["null_count"] == 0
    assert row["null_ratio"] == pytest.approx(0.0)
    assert row["mean"] == pytest.approx(11.5)
    assert row["median"] == pytest.approx(11.5)
    assert row["min"] == 10
    assert row["max"] == 13
    assert row["variance"] == pytest.approx(pd.Series([10, 11, 12, 13]).var())
    assert row["unique_values"] == 4


def test_null_handling_and_zero_ratio_are_explicit() -> None:
    result = feature_profiling.profile_features(_features_frame())

    row = _summary_row(result, symbol="BTCUSDT", timeframe="1h", feature="feature_with_nulls")

    assert row["count"] == 4
    assert row["null_count"] == 2
    assert row["null_ratio"] == pytest.approx(2 / 6)
    assert row["zero_ratio"] == pytest.approx(2 / 4)


def test_skewness_and_kurtosis_are_calculated_when_defined() -> None:
    result = feature_profiling.profile_features(_features_frame())

    row = _summary_row(result, symbol="BTCUSDT", timeframe="1h", feature="feature_trend")

    assert pd.notna(row["skewness"])
    assert pd.notna(row["kurtosis"])


def test_iqr_outlier_detection_counts_extreme_values() -> None:
    result = feature_profiling.profile_features(_features_frame())

    row = _summary_row(result, symbol="BTCUSDT", timeframe="1h", feature="feature_trend")

    assert row["outlier_count"] == 1
    assert row["outlier_ratio"] == pytest.approx(1 / 6)


def test_correlation_and_redundancy_are_reported_between_features() -> None:
    result = feature_profiling.profile_features(
        _features_frame(),
        feature_columns=("feature_trend", "feature_trend_copy"),
    )

    pair = result.correlation_matrix[
        result.correlation_matrix["symbol"].eq("BTCUSDT")
        & result.correlation_matrix["timeframe"].eq("1h")
        & result.correlation_matrix["feature_x"].eq("feature_trend")
        & result.correlation_matrix["feature_y"].eq("feature_trend_copy")
    ].iloc[0]
    redundant_pair = result.redundancy[
        result.redundancy["feature_x"].eq("feature_trend")
        & result.redundancy["feature_y"].eq("feature_trend_copy")
    ]

    assert pair["correlation"] == pytest.approx(1.0)
    assert len(redundant_pair) == 3


def test_grouping_by_symbol_does_not_mix_symbols() -> None:
    result = feature_profiling.profile_features(
        _features_frame(),
        feature_columns=("feature_trend",),
        group_by=("symbol",),
    )

    assert set(result.summary["symbol"]) == {"BTCUSDT", "ETHUSDT"}
    btc_row = result.summary[
        result.summary["symbol"].eq("BTCUSDT")
        & result.summary["feature"].eq("feature_trend")
    ].iloc[0]
    eth_row = result.summary[
        result.summary["symbol"].eq("ETHUSDT")
        & result.summary["feature"].eq("feature_trend")
    ].iloc[0]
    assert btc_row["count"] == 10
    assert eth_row["count"] == 4


def test_grouping_by_timeframe_does_not_mix_timeframes() -> None:
    result = feature_profiling.profile_features(
        _features_frame(),
        feature_columns=("feature_trend",),
        group_by=("timeframe",),
    )

    assert set(result.summary["timeframe"]) == {"1h", "4h"}
    one_hour = result.summary[result.summary["timeframe"].eq("1h")].iloc[0]
    four_hour = result.summary[result.summary["timeframe"].eq("4h")].iloc[0]
    assert one_hour["count"] == 10
    assert four_hour["count"] == 4


def test_feature_names_are_preserved() -> None:
    result = feature_profiling.profile_features(_features_frame())

    assert set(result.summary["feature"]) == {
        "feature_trend",
        "feature_trend_copy",
        "feature_with_nulls",
        "feature_constant",
        "feature_all_nan",
    }


def test_missing_required_columns_raise_clear_error() -> None:
    frame = _features_frame().drop(columns=["symbol"])

    with pytest.raises(ValueError, match="features missing required columns"):
        feature_profiling.profile_features(frame)


def test_constant_columns_are_profiled_without_outliers_or_defined_correlation() -> None:
    result = feature_profiling.profile_features(
        _features_frame(),
        feature_columns=("feature_constant", "feature_trend"),
    )

    row = _summary_row(result, symbol="BTCUSDT", timeframe="1h", feature="feature_constant")
    corr_pair = result.correlation_matrix[
        result.correlation_matrix["symbol"].eq("BTCUSDT")
        & result.correlation_matrix["timeframe"].eq("1h")
        & result.correlation_matrix["feature_x"].eq("feature_constant")
        & result.correlation_matrix["feature_y"].eq("feature_trend")
    ].iloc[0]

    assert row["variance"] == pytest.approx(0.0)
    assert row["outlier_count"] == 0
    assert pd.isna(corr_pair["correlation"])


def test_fully_nan_columns_are_profiled_without_fabricated_values() -> None:
    result = feature_profiling.profile_features(
        _features_frame(),
        feature_columns=("feature_all_nan",),
    )

    row = _summary_row(result, symbol="BTCUSDT", timeframe="1h", feature="feature_all_nan")

    assert row["count"] == 0
    assert row["null_count"] == 6
    assert row["null_ratio"] == pytest.approx(1.0)
    assert pd.isna(row["mean"])
    assert pd.isna(row["zero_ratio"])
    assert row["outlier_count"] == 0


def test_forward_return_columns_are_rejected_when_selected_as_features() -> None:
    frame = _features_frame()
    frame["forward_return_1"] = 0.01

    with pytest.raises(ValueError, match="forward return columns are not valid"):
        feature_profiling.profile_features(frame, feature_columns=("forward_return_1",))
