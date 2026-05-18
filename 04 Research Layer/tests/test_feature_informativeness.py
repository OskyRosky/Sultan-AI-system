from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "research" / "feature_informativeness.py"
SPEC = importlib.util.spec_from_file_location("feature_informativeness", MODULE_PATH)
feature_informativeness = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = feature_informativeness
SPEC.loader.exec_module(feature_informativeness)


def _research_dataset() -> pd.DataFrame:
    rows = []

    btc_one_hour = [
        (1, 0.01, 0.02),
        (2, 0.02, 0.04),
        (3, 0.03, 0.06),
        (4, 0.04, 0.08),
        (5, 0.05, 0.10),
        (6, 0.06, 0.12),
    ]
    for idx, (feature, return_1, return_3) in enumerate(btc_one_hour):
        rows.append(
            {
                "symbol": "BTCUSDT",
                "timeframe": "1h",
                "timestamp": pd.Timestamp("2026-01-01") + pd.Timedelta(hours=idx),
                "feature_signal": feature,
                "feature_inverse": -feature,
                "feature_repeated": [1, 1, 1, 2, 2, 3][idx],
                "feature_constant": 7,
                "forward_return_1": return_1,
                "forward_return_3": return_3,
            }
        )

    eth_one_hour = [(10, -0.10), (11, -0.11), (12, -0.12), (13, -0.13), (14, -0.14)]
    for idx, (feature, return_1) in enumerate(eth_one_hour):
        rows.append(
            {
                "symbol": "ETHUSDT",
                "timeframe": "1h",
                "timestamp": pd.Timestamp("2026-01-01") + pd.Timedelta(hours=idx),
                "feature_signal": feature,
                "feature_inverse": -feature,
                "feature_repeated": 1,
                "feature_constant": 7,
                "forward_return_1": return_1,
                "forward_return_3": return_1 * 2,
            }
        )

    btc_four_hour = [(20, 0.20), (21, 0.21), (22, 0.22), (23, 0.23), (24, 0.24)]
    for idx, (feature, return_1) in enumerate(btc_four_hour):
        rows.append(
            {
                "symbol": "BTCUSDT",
                "timeframe": "4h",
                "timestamp": pd.Timestamp("2026-01-01") + pd.Timedelta(hours=idx * 4),
                "feature_signal": feature,
                "feature_inverse": -feature,
                "feature_repeated": 2,
                "feature_constant": 7,
                "forward_return_1": return_1,
                "forward_return_3": return_1 * 2,
            }
        )

    return pd.DataFrame(rows)


def _bucket_rows(result: object, *, feature: str = "feature_signal") -> pd.DataFrame:
    return result.bucket_metrics[
        result.bucket_metrics["symbol"].eq("BTCUSDT")
        & result.bucket_metrics["timeframe"].eq("1h")
        & result.bucket_metrics["feature"].eq(feature)
        & result.bucket_metrics["forward_return"].eq("forward_return_1")
    ]


def _ic_row(
    result: object,
    *,
    symbol: str = "BTCUSDT",
    timeframe: str = "1h",
    feature: str = "feature_signal",
    forward_return: str = "forward_return_1",
) -> pd.Series:
    rows = result.ic_metrics[
        result.ic_metrics["symbol"].eq(symbol)
        & result.ic_metrics["timeframe"].eq(timeframe)
        & result.ic_metrics["feature"].eq(feature)
        & result.ic_metrics["forward_return"].eq(forward_return)
    ]
    assert len(rows) == 1
    return rows.iloc[0]


def test_bucket_analysis_calculates_return_statistics() -> None:
    result = feature_informativeness.analyze_feature_informativeness(
        _research_dataset(),
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1",),
        n_buckets=3,
    )

    buckets = _bucket_rows(result)
    first_bucket = buckets[buckets["bucket"].eq(1)].iloc[0]
    last_bucket = buckets[buckets["bucket"].eq(3)].iloc[0]

    assert buckets["count"].sum() == 6
    assert first_bucket["count"] == 2
    assert first_bucket["mean_forward_return"] == pytest.approx(0.015)
    assert first_bucket["median_forward_return"] == pytest.approx(0.015)
    assert first_bucket["hit_rate"] == pytest.approx(1.0)
    assert last_bucket["avg_abs_forward_return"] == pytest.approx(0.055)


def test_quantiles_with_repeated_feature_values_do_not_drop_observations() -> None:
    result = feature_informativeness.analyze_feature_informativeness(
        _research_dataset(),
        feature_columns=("feature_repeated",),
        forward_return_columns=("forward_return_1",),
        n_buckets=5,
    )

    buckets = _bucket_rows(result, feature="feature_repeated")

    assert buckets["count"].sum() == 6
    assert buckets["bucket"].notna().all()
    assert buckets["bucket"].nunique() <= 3


def test_nan_pairs_are_excluded_from_bucket_and_ic_metrics() -> None:
    frame = _research_dataset()
    mask = frame["symbol"].eq("BTCUSDT") & frame["timeframe"].eq("1h")
    frame.loc[mask & frame["feature_signal"].eq(2), "feature_signal"] = None
    frame.loc[mask & frame["feature_signal"].eq(4), "forward_return_1"] = None

    result = feature_informativeness.analyze_feature_informativeness(
        frame,
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1",),
        n_buckets=3,
    )

    buckets = _bucket_rows(result)
    ic = _ic_row(result)
    assert buckets["count"].sum() == 4
    assert ic["sample_count"] == 4


def test_information_coefficient_pearson_is_calculated() -> None:
    result = feature_informativeness.analyze_feature_informativeness(
        _research_dataset(),
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1",),
    )

    ic = _ic_row(result)

    assert ic["pearson_ic"] == pytest.approx(1.0)
    assert ic["abs_pearson_ic"] == pytest.approx(1.0)


def test_information_coefficient_spearman_is_calculated() -> None:
    result = feature_informativeness.analyze_feature_informativeness(
        _research_dataset(),
        feature_columns=("feature_inverse",),
        forward_return_columns=("forward_return_1",),
    )

    ic = _ic_row(result, feature="feature_inverse")

    assert ic["spearman_ic"] == pytest.approx(-1.0)
    assert ic["abs_spearman_ic"] == pytest.approx(1.0)


def test_hit_rate_counts_positive_forward_returns() -> None:
    frame = _research_dataset()
    mask = frame["symbol"].eq("BTCUSDT") & frame["timeframe"].eq("1h")
    frame.loc[mask, "forward_return_1"] = [-0.03, -0.02, 0.01, 0.02, 0.03, 0.04]

    result = feature_informativeness.analyze_feature_informativeness(
        frame,
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1",),
        n_buckets=3,
    )

    first_bucket = _bucket_rows(result).query("bucket == 1").iloc[0]
    last_bucket = _bucket_rows(result).query("bucket == 3").iloc[0]

    assert first_bucket["hit_rate"] == pytest.approx(0.0)
    assert last_bucket["hit_rate"] == pytest.approx(1.0)


def test_multi_horizon_forward_returns_are_supported() -> None:
    result = feature_informativeness.analyze_feature_informativeness(
        _research_dataset(),
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1", "forward_return_3"),
    )

    horizons = set(result.ic_metrics["forward_return"])
    assert horizons == {"forward_return_1", "forward_return_3"}


def test_analysis_is_separated_by_symbol() -> None:
    result = feature_informativeness.analyze_feature_informativeness(
        _research_dataset(),
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1",),
    )

    btc = _ic_row(result, symbol="BTCUSDT", timeframe="1h")
    eth = _ic_row(result, symbol="ETHUSDT", timeframe="1h")
    assert btc["sample_count"] == 6
    assert eth["sample_count"] == 5
    assert eth["pearson_ic"] == pytest.approx(-1.0)


def test_analysis_is_separated_by_timeframe() -> None:
    result = feature_informativeness.analyze_feature_informativeness(
        _research_dataset(),
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1",),
    )

    one_hour = _ic_row(result, symbol="BTCUSDT", timeframe="1h")
    four_hour = _ic_row(result, symbol="BTCUSDT", timeframe="4h")
    assert one_hour["sample_count"] == 6
    assert four_hour["sample_count"] == 5
    assert four_hour["pearson_ic"] == pytest.approx(1.0)


def test_preliminary_ranking_orders_by_absolute_ic_metadata() -> None:
    result = feature_informativeness.analyze_feature_informativeness(
        _research_dataset(),
        feature_columns=("feature_constant", "feature_signal", "feature_repeated"),
        forward_return_columns=("forward_return_1",),
    )

    ranking = result.ranking[
        result.ranking["symbol"].eq("BTCUSDT")
        & result.ranking["timeframe"].eq("1h")
        & result.ranking["forward_return"].eq("forward_return_1")
    ].sort_values("technical_rank")

    assert ranking.iloc[0]["feature"] == "feature_signal"
    assert ranking.iloc[0]["technical_rank"] == 1
    assert ranking.iloc[-1]["feature"] == "feature_constant"


def test_missing_required_columns_raise_clear_error() -> None:
    frame = _research_dataset().drop(columns=["symbol"])

    with pytest.raises(ValueError, match="research_dataset missing required columns"):
        feature_informativeness.analyze_feature_informativeness(frame)


def test_constant_features_have_null_ic_and_single_bucket() -> None:
    result = feature_informativeness.analyze_feature_informativeness(
        _research_dataset(),
        feature_columns=("feature_constant",),
        forward_return_columns=("forward_return_1",),
    )

    ic = _ic_row(result, feature="feature_constant")
    buckets = _bucket_rows(result, feature="feature_constant")
    assert pd.isna(ic["pearson_ic"])
    assert pd.isna(ic["spearman_ic"])
    assert buckets["bucket"].tolist() == [1]
    assert buckets.iloc[0]["count"] == 6


def test_constant_forward_returns_have_null_ic() -> None:
    frame = _research_dataset()
    frame["forward_return_1"] = 0.01

    result = feature_informativeness.analyze_feature_informativeness(
        frame,
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1",),
    )

    ic = _ic_row(result)
    assert pd.isna(ic["pearson_ic"])
    assert pd.isna(ic["spearman_ic"])


def test_small_datasets_keep_metrics_without_fabricating_correlation() -> None:
    frame = _research_dataset().head(1)

    result = feature_informativeness.analyze_feature_informativeness(
        frame,
        feature_columns=("feature_signal",),
        forward_return_columns=("forward_return_1",),
        n_buckets=3,
    )

    ic = _ic_row(result)
    buckets = _bucket_rows(result)
    assert ic["sample_count"] == 1
    assert pd.isna(ic["pearson_ic"])
    assert buckets.iloc[0]["count"] == 1


def test_non_forward_return_label_selection_raises_clear_error() -> None:
    with pytest.raises(ValueError, match="forward return columns must start"):
        feature_informativeness.analyze_feature_informativeness(
            _research_dataset(),
            feature_columns=("feature_signal",),
            forward_return_columns=("feature_inverse",),
        )
