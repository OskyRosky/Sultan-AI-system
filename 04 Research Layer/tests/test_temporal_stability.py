from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "research" / "temporal_stability.py"
SPEC = importlib.util.spec_from_file_location("temporal_stability", MODULE_PATH)
temporal_stability = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = temporal_stability
SPEC.loader.exec_module(temporal_stability)


def _research_dataset() -> pd.DataFrame:
    rows = []

    btc_values = [
        (1, 0.01),
        (2, 0.02),
        (3, 0.03),
        (4, 0.04),
        (1, -0.01),
        (2, -0.02),
        (3, -0.03),
        (4, -0.04),
    ]
    for idx, (feature, forward_return) in enumerate(btc_values):
        rows.append(
            {
                "symbol": "BTCUSDT",
                "timeframe": "1h",
                "timestamp": pd.Timestamp("2026-01-01") + pd.Timedelta(hours=idx),
                "feature_trend": feature,
                "feature_constant": 7,
                "forward_return_1": forward_return,
            }
        )

    eth_values = [(10, 0.10), (11, 0.11), (12, 0.12), (13, 0.13)]
    for idx, (feature, forward_return) in enumerate(eth_values):
        rows.append(
            {
                "symbol": "ETHUSDT",
                "timeframe": "1h",
                "timestamp": pd.Timestamp("2026-01-01") + pd.Timedelta(hours=idx),
                "feature_trend": feature,
                "feature_constant": 7,
                "forward_return_1": forward_return,
            }
        )

    four_hour_values = [(20, 0.20), (21, 0.21), (22, 0.22), (23, 0.23)]
    for idx, (feature, forward_return) in enumerate(four_hour_values):
        rows.append(
            {
                "symbol": "BTCUSDT",
                "timeframe": "4h",
                "timestamp": pd.Timestamp("2026-01-01") + pd.Timedelta(hours=idx * 4),
                "feature_trend": feature,
                "feature_constant": 7,
                "forward_return_1": forward_return,
            }
        )

    return pd.DataFrame(rows)


def _window_row(
    result: object,
    *,
    symbol: str = "BTCUSDT",
    timeframe: str = "1h",
    window: str,
    feature: str = "feature_trend",
) -> pd.Series:
    rows = result.window_metrics[
        result.window_metrics["symbol"].eq(symbol)
        & result.window_metrics["timeframe"].eq(timeframe)
        & result.window_metrics["window"].eq(window)
        & result.window_metrics["feature"].eq(feature)
        & result.window_metrics["forward_return"].eq("forward_return_1")
    ]
    assert len(rows) == 1
    return rows.iloc[0]


def test_equal_count_temporal_segmentation_is_chronological_per_group() -> None:
    result = temporal_stability.analyze_temporal_stability(
        _research_dataset(),
        feature_columns=("feature_trend",),
        forward_return_columns=("forward_return_1",),
        n_windows=2,
    )

    first = _window_row(result, window="window_1")
    second = _window_row(result, window="window_2")

    assert first["sample_count"] == 4
    assert second["sample_count"] == 4
    assert first["window_start"] == pd.Timestamp("2026-01-01 00:00:00")
    assert first["window_end"] == pd.Timestamp("2026-01-01 03:00:00")
    assert second["window_start"] == pd.Timestamp("2026-01-01 04:00:00")
    assert second["window_end"] == pd.Timestamp("2026-01-01 07:00:00")


def test_window_stability_metrics_capture_positive_and_negative_periods() -> None:
    result = temporal_stability.analyze_temporal_stability(
        _research_dataset(),
        feature_columns=("feature_trend",),
        forward_return_columns=("forward_return_1",),
        n_windows=2,
    )

    first = _window_row(result, window="window_1")
    second = _window_row(result, window="window_2")

    assert first["correlation"] == pytest.approx(1.0)
    assert first["correlation_sign"] == 1
    assert second["correlation"] == pytest.approx(-1.0)
    assert second["correlation_sign"] == -1


def test_drift_metrics_detect_correlation_and_feature_mean_drift() -> None:
    result = temporal_stability.analyze_temporal_stability(
        _research_dataset(),
        feature_columns=("feature_trend",),
        forward_return_columns=("forward_return_1",),
        n_windows=2,
    )

    drift = result.drift_metrics[
        result.drift_metrics["symbol"].eq("BTCUSDT")
        & result.drift_metrics["timeframe"].eq("1h")
        & result.drift_metrics["feature"].eq("feature_trend")
    ].iloc[0]

    assert drift["windows_observed"] == 2
    assert drift["correlation_min"] == pytest.approx(-1.0)
    assert drift["correlation_max"] == pytest.approx(1.0)
    assert drift["correlation_range"] == pytest.approx(2.0)
    assert drift["feature_mean_range"] == pytest.approx(0.0)
    assert drift["sign_consistency_ratio"] == pytest.approx(0.5)


def test_analysis_is_separated_by_symbol() -> None:
    result = temporal_stability.analyze_temporal_stability(
        _research_dataset(),
        feature_columns=("feature_trend",),
        forward_return_columns=("forward_return_1",),
        n_windows=2,
    )

    assert set(result.window_metrics["symbol"]) == {"BTCUSDT", "ETHUSDT"}
    eth_first = _window_row(result, symbol="ETHUSDT", timeframe="1h", window="window_1")
    assert eth_first["sample_count"] == 2
    assert eth_first["feature_mean"] == pytest.approx(10.5)


def test_analysis_is_separated_by_timeframe() -> None:
    result = temporal_stability.analyze_temporal_stability(
        _research_dataset(),
        feature_columns=("feature_trend",),
        forward_return_columns=("forward_return_1",),
        n_windows=2,
    )

    one_hour = _window_row(result, symbol="BTCUSDT", timeframe="1h", window="window_1")
    four_hour = _window_row(result, symbol="BTCUSDT", timeframe="4h", window="window_1")
    assert one_hour["feature_mean"] == pytest.approx(2.5)
    assert four_hour["feature_mean"] == pytest.approx(20.5)


def test_nan_pairs_are_ignored_without_dropping_window_traceability() -> None:
    frame = _research_dataset()
    frame.loc[
        frame["symbol"].eq("BTCUSDT") & frame["timeframe"].eq("1h") & frame.index.isin([1, 2]),
        "forward_return_1",
    ] = None

    result = temporal_stability.analyze_temporal_stability(
        frame,
        feature_columns=("feature_trend",),
        forward_return_columns=("forward_return_1",),
        n_windows=2,
    )

    first = _window_row(result, window="window_1")
    assert first["sample_count"] == 2
    assert pd.notna(first["window_start"])
    assert pd.notna(first["window_end"])


def test_explicit_empty_windows_are_retained_with_null_metrics() -> None:
    result = temporal_stability.analyze_temporal_stability(
        _research_dataset(),
        feature_columns=("feature_trend",),
        forward_return_columns=("forward_return_1",),
        windows=(
            ("observed", "2026-01-01 00:00:00", "2026-01-01 02:00:00"),
            ("empty", "2027-01-01 00:00:00", "2027-01-01 02:00:00"),
        ),
    )

    empty = _window_row(result, window="empty")
    assert empty["sample_count"] == 0
    assert empty["window_start"] == pd.Timestamp("2027-01-01 00:00:00")
    assert empty["window_end"] == pd.Timestamp("2027-01-01 02:00:00")
    assert pd.isna(empty["correlation"])


def test_timestamps_are_preserved_as_window_boundaries() -> None:
    result = temporal_stability.analyze_temporal_stability(
        _research_dataset(),
        feature_columns=("feature_trend",),
        forward_return_columns=("forward_return_1",),
        windows=(("first_two", "2026-01-01 00:00:00", "2026-01-01 01:00:00"),),
    )

    row = _window_row(result, window="first_two")
    assert row["window_start"] == pd.Timestamp("2026-01-01 00:00:00")
    assert row["window_end"] == pd.Timestamp("2026-01-01 01:00:00")


def test_constant_features_have_null_correlation_without_crashing() -> None:
    result = temporal_stability.analyze_temporal_stability(
        _research_dataset(),
        feature_columns=("feature_constant",),
        forward_return_columns=("forward_return_1",),
        n_windows=2,
    )

    row = _window_row(result, window="window_1", feature="feature_constant")
    assert row["feature_variance"] == pytest.approx(0.0)
    assert pd.isna(row["correlation"])


def test_small_datasets_keep_empty_equal_count_windows_visible() -> None:
    frame = _research_dataset().head(1)

    result = temporal_stability.analyze_temporal_stability(
        frame,
        feature_columns=("feature_trend",),
        forward_return_columns=("forward_return_1",),
        n_windows=3,
    )

    assert result.window_metrics["window"].tolist() == ["window_1", "window_2", "window_3"]
    assert result.window_metrics["sample_count"].tolist() == [1, 0, 0]
    assert pd.isna(result.window_metrics.iloc[1]["window_start"])


def test_missing_required_columns_raise_clear_error() -> None:
    frame = _research_dataset().drop(columns=["timestamp"])

    with pytest.raises(ValueError, match="research_dataset missing required columns"):
        temporal_stability.analyze_temporal_stability(frame)


def test_missing_forward_return_columns_raise_clear_error() -> None:
    frame = _research_dataset().drop(columns=["forward_return_1"])

    with pytest.raises(ValueError, match="at least one forward return column"):
        temporal_stability.analyze_temporal_stability(frame)
