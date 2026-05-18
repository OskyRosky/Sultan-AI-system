from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "research" / "regime_analysis.py"
SPEC = importlib.util.spec_from_file_location("regime_analysis", MODULE_PATH)
regime_analysis = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = regime_analysis
SPEC.loader.exec_module(regime_analysis)


def _research_dataset() -> pd.DataFrame:
    rows = []
    btc_one_hour = [
        (-2, 1, 10, 1, -0.02, -0.04),
        (-1, 2, 20, 1, -0.01, -0.02),
        (0, 3, 30, 2, 0.00, 0.00),
        (1, 4, 40, 2, 0.01, 0.02),
        (2, 5, 50, 3, 0.02, 0.04),
        (3, 6, 60, 3, 0.03, 0.06),
        (4, 7, 70, 4, 0.04, 0.08),
        (5, 8, 80, 4, 0.05, 0.10),
    ]
    for idx, (trend, volatility, momentum, range_value, return_1, return_3) in enumerate(
        btc_one_hour
    ):
        rows.append(
            {
                "symbol": "BTCUSDT",
                "timeframe": "1h",
                "timestamp": pd.Timestamp("2026-01-01") + pd.Timedelta(hours=idx),
                "feature_signal": trend,
                "feature_constant": 7,
                "trend_context": trend,
                "volatility_context": volatility,
                "momentum_context": momentum - 35,
                "range_context": range_value,
                "forward_return_1": return_1,
                "forward_return_3": return_3,
            }
        )

    eth_one_hour = [(-1, -0.10), (0, 0.00), (1, 0.10), (2, 0.20)]
    for idx, (feature, return_1) in enumerate(eth_one_hour):
        rows.append(
            {
                "symbol": "ETHUSDT",
                "timeframe": "1h",
                "timestamp": pd.Timestamp("2026-01-01") + pd.Timedelta(hours=idx),
                "feature_signal": feature,
                "feature_constant": 7,
                "trend_context": feature,
                "volatility_context": 5,
                "momentum_context": feature,
                "range_context": 1,
                "forward_return_1": return_1,
                "forward_return_3": return_1 * 2,
            }
        )

    btc_four_hour = [(10, 0.10), (11, 0.11), (12, 0.12), (13, 0.13)]
    for idx, (feature, return_1) in enumerate(btc_four_hour):
        rows.append(
            {
                "symbol": "BTCUSDT",
                "timeframe": "4h",
                "timestamp": pd.Timestamp("2026-01-01") + pd.Timedelta(hours=idx * 4),
                "feature_signal": feature,
                "feature_constant": 7,
                "trend_context": feature,
                "volatility_context": idx + 1,
                "momentum_context": feature,
                "range_context": idx + 1,
                "forward_return_1": return_1,
                "forward_return_3": return_1 * 2,
            }
        )

    return pd.DataFrame(rows)


def _analyze(frame: pd.DataFrame | None = None) -> object:
    return regime_analysis.analyze_regimes(
        _research_dataset() if frame is None else frame,
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1",),
        trend_column="trend_context",
        volatility_column="volatility_context",
        momentum_column="momentum_context",
        range_column="range_context",
    )


def _metric_row(
    result: object,
    *,
    symbol: str = "BTCUSDT",
    timeframe: str = "1h",
    regime_type: str,
    regime: str,
    forward_return: str = "forward_return_1",
    feature: str = "feature_signal",
) -> pd.Series:
    rows = result.regime_metrics[
        result.regime_metrics["symbol"].eq(symbol)
        & result.regime_metrics["timeframe"].eq(timeframe)
        & result.regime_metrics["regime_type"].eq(regime_type)
        & result.regime_metrics["regime"].eq(regime)
        & result.regime_metrics["forward_return"].eq(forward_return)
        & result.regime_metrics["feature"].eq(feature)
    ]
    assert len(rows) == 1
    return rows.iloc[0]


def test_regime_labeling_is_correct_for_all_supported_types() -> None:
    result = _analyze()
    labeled = result.labeled_data[
        result.labeled_data["symbol"].eq("BTCUSDT")
        & result.labeled_data["timeframe"].eq("1h")
    ]

    assert labeled["trend_regime"].tolist() == [
        "bearish",
        "bearish",
        "neutral",
        "bullish",
        "bullish",
        "bullish",
        "bullish",
        "bullish",
    ]
    assert set(labeled["volatility_regime"]) == {"low_vol", "medium_vol", "high_vol"}
    assert labeled["momentum_regime"].tolist() == [
        "negative",
        "negative",
        "negative",
        "positive",
        "positive",
        "positive",
        "positive",
        "positive",
    ]
    assert labeled["range_regime"].tolist() == [
        "compressed",
        "compressed",
        "compressed",
        "compressed",
        "expanded",
        "expanded",
        "expanded",
        "expanded",
    ]


def test_analysis_is_separated_by_symbol() -> None:
    result = _analyze()

    btc = _metric_row(result, symbol="BTCUSDT", timeframe="1h", regime_type="trend", regime="bullish")
    eth = _metric_row(result, symbol="ETHUSDT", timeframe="1h", regime_type="trend", regime="bullish")

    assert btc["sample_count"] == 5
    assert eth["sample_count"] == 2


def test_analysis_is_separated_by_timeframe() -> None:
    result = _analyze()

    one_hour = _metric_row(result, symbol="BTCUSDT", timeframe="1h", regime_type="trend", regime="bullish")
    four_hour = _metric_row(result, symbol="BTCUSDT", timeframe="4h", regime_type="trend", regime="bullish")

    assert one_hour["mean_forward_return"] == pytest.approx(0.03)
    assert four_hour["mean_forward_return"] == pytest.approx(0.115)


def test_analysis_is_separated_by_horizon() -> None:
    result = regime_analysis.analyze_regimes(
        _research_dataset(),
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1", "forward_return_3"),
        trend_column="trend_context",
    )

    horizons = set(result.regime_metrics["forward_return"])
    assert horizons == {"forward_return_1", "forward_return_3"}


def test_conditional_ic_is_calculated_by_regime() -> None:
    result = _analyze()

    bullish = _metric_row(result, regime_type="trend", regime="bullish")

    assert bullish["pearson_ic"] == pytest.approx(1.0)
    assert bullish["spearman_ic"] == pytest.approx(1.0)


def test_regime_context_columns_cannot_also_be_analyzed_as_features() -> None:
    with pytest.raises(ValueError, match="cannot also be analyzed as features"):
        regime_analysis.analyze_regimes(
            _research_dataset(),
            feature_columns=("trend_context",),
            forward_return_columns=("forward_return_1",),
            trend_column="trend_context",
        )


def test_conditional_hit_rate_is_calculated_by_regime() -> None:
    result = _analyze()

    bearish = _metric_row(result, regime_type="trend", regime="bearish")
    bullish = _metric_row(result, regime_type="trend", regime="bullish")

    assert bearish["hit_rate"] == pytest.approx(0.0)
    assert bullish["hit_rate"] == pytest.approx(1.0)


def test_nan_pairs_are_excluded_without_losing_regime_count_traceability() -> None:
    frame = _research_dataset()
    mask = (
        frame["symbol"].eq("BTCUSDT")
        & frame["timeframe"].eq("1h")
        & frame["trend_context"].gt(0)
    )
    frame.loc[mask & frame["feature_signal"].eq(2), "forward_return_1"] = None

    result = _analyze(frame)
    bullish = _metric_row(result, regime_type="trend", regime="bullish")
    count = result.regime_counts[
        result.regime_counts["symbol"].eq("BTCUSDT")
        & result.regime_counts["timeframe"].eq("1h")
        & result.regime_counts["regime_type"].eq("trend")
        & result.regime_counts["regime"].eq("bullish")
    ].iloc[0]

    assert bullish["sample_count"] == 4
    assert count["row_count"] == 5


def test_small_datasets_keep_metrics_without_fabricating_correlation() -> None:
    frame = _research_dataset().head(1)

    result = regime_analysis.analyze_regimes(
        frame,
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1",),
        trend_column="trend_context",
    )

    bearish = _metric_row(result, regime_type="trend", regime="bearish")
    assert bearish["sample_count"] == 1
    assert pd.isna(bearish["pearson_ic"])


def test_empty_expected_regimes_are_retained_with_zero_sample_count() -> None:
    frame = _research_dataset()
    frame = frame[frame["symbol"].eq("BTCUSDT") & frame["timeframe"].eq("1h")].copy()
    frame["trend_context"] = 1

    result = regime_analysis.analyze_regimes(
        frame,
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1",),
        trend_column="trend_context",
    )

    bearish = _metric_row(result, regime_type="trend", regime="bearish")
    neutral = _metric_row(result, regime_type="trend", regime="neutral")
    assert bearish["sample_count"] == 0
    assert neutral["sample_count"] == 0
    assert pd.isna(bearish["mean_forward_return"])


def test_constant_features_have_null_conditional_ic() -> None:
    result = regime_analysis.analyze_regimes(
        _research_dataset(),
        feature_columns=("feature_constant",),
        forward_return_columns=("forward_return_1",),
        trend_column="trend_context",
    )

    bullish = _metric_row(result, regime_type="trend", regime="bullish", feature="feature_constant")
    assert pd.isna(bullish["pearson_ic"])
    assert pd.isna(bullish["spearman_ic"])


def test_constant_forward_returns_have_null_conditional_ic() -> None:
    frame = _research_dataset()
    frame["forward_return_1"] = 0.01

    result = _analyze(frame)
    bullish = _metric_row(result, regime_type="trend", regime="bullish")

    assert pd.isna(bullish["pearson_ic"])
    assert pd.isna(bullish["spearman_ic"])


def test_missing_required_columns_raise_clear_error() -> None:
    frame = _research_dataset().drop(columns=["trend_context"])

    with pytest.raises(ValueError, match="research_dataset missing required columns"):
        regime_analysis.analyze_regimes(
            frame,
            feature_columns=("feature_signal",),
            forward_return_columns=("forward_return_1",),
            trend_column="trend_context",
        )


def test_missing_context_columns_raise_clear_error() -> None:
    with pytest.raises(ValueError, match="at least one regime context column is required"):
        regime_analysis.analyze_regimes(
            _research_dataset(),
            feature_columns=("feature_signal",),
            forward_return_columns=("forward_return_1"),
        )
