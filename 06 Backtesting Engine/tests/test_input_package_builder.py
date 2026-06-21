from __future__ import annotations

from dataclasses import fields
from datetime import datetime, timezone
from pathlib import Path
import sys


BACKTESTING_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKTESTING_ROOT.parents[0]
if str(BACKTESTING_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKTESTING_ROOT))

from contracts.motor_b_output_contract import (  # noqa: E402
    AvailabilityStatus,
    ConfidenceStatus,
    OOSValidationStatus,
    PaperTradingEligibility,
    RobustnessStatus,
    SimulationStatus,
)
from loaders.feature_snapshot_loader import FeatureSnapshotLoader  # noqa: E402
from packages.input_package_builder import (  # noqa: E402
    BacktestInputPackage,
    InputPackageBuilder,
    InputPackageSeriesReference,
)


MANIFEST_PATH = REPO_ROOT / (
    "03 Feature Engineering/manifests/"
    "feature_snapshot_technical_v1_1_0_0_20260608_163510.json"
)
SCHEMA_PATH = REPO_ROOT / "03 Feature Engineering/schemas/feature_snapshot_manifest_schema.json"
GAP_REPORT_REFERENCE = "03 Feature Engineering/docs/gap_report_4h_historical.md"
EXPECTED_SERIES_KEYS = {
    ("BTCUSDT", "1d"),
    ("BTCUSDT", "4h"),
    ("ETHUSDT", "1d"),
    ("ETHUSDT", "4h"),
}


def _loaded_snapshot():
    return FeatureSnapshotLoader(MANIFEST_PATH, schema_path=SCHEMA_PATH).load()


def _input_package() -> BacktestInputPackage:
    return InputPackageBuilder(_loaded_snapshot()).build(
        created_at=datetime(2026, 6, 21, tzinfo=timezone.utc)
    )


def test_input_package_builds_from_official_loaded_snapshot() -> None:
    package = _input_package()

    assert package.input_package_id.startswith("backtest-input-")
    assert package.created_at == datetime(2026, 6, 21, tzinfo=timezone.utc)
    assert package.governance_state.empirical_results_available is False


def test_package_preserves_snapshot_feature_version_and_commit() -> None:
    loaded_snapshot = _loaded_snapshot()
    package = InputPackageBuilder(loaded_snapshot).build()

    assert package.snapshot_id == loaded_snapshot.snapshot_id
    assert package.feature_set == loaded_snapshot.feature_set
    assert package.feature_version == loaded_snapshot.feature_version
    assert package.code_commit == loaded_snapshot.code_commit
    assert package.generated_at == loaded_snapshot.generated_at


def test_package_preserves_manifest_path_and_schema_path() -> None:
    package = _input_package()

    assert package.manifest_path == MANIFEST_PATH
    assert package.schema_path == SCHEMA_PATH


def test_package_preserves_gap_and_quality_report_references() -> None:
    loaded_snapshot = _loaded_snapshot()
    package = InputPackageBuilder(loaded_snapshot).build()

    assert package.gap_report_reference == GAP_REPORT_REFERENCE
    assert package.gap_report_reference == loaded_snapshot.gap_report_reference
    assert package.quality_report_reference == loaded_snapshot.quality_report_reference


def test_serialized_package_includes_generated_at() -> None:
    package = _input_package()
    serialized = package.to_dict()

    assert serialized["lineage"]["generated_at"] == package.generated_at.isoformat()


def test_package_includes_all_four_expected_series_references() -> None:
    package = _input_package()

    assert set(package.series) == EXPECTED_SERIES_KEYS


def test_package_series_row_counts_match_loaded_snapshot() -> None:
    loaded_snapshot = _loaded_snapshot()
    package = InputPackageBuilder(loaded_snapshot).build()

    for key, loaded_series in loaded_snapshot.series.items():
        assert package.series[key].row_count == loaded_series.row_count


def test_package_series_run_ids_match_loaded_snapshot() -> None:
    loaded_snapshot = _loaded_snapshot()
    package = InputPackageBuilder(loaded_snapshot).build()

    for key, loaded_series in loaded_snapshot.series.items():
        assert package.series[key].run_id == loaded_series.run_id


def test_governance_state_preserves_blocked_statuses() -> None:
    governance = _input_package().governance_state

    assert governance.stage_09_readiness == "blocked"
    assert governance.handoff_to_09 == "blocked"
    assert governance.empirical_results_available is False
    assert governance.oos_validation_status is OOSValidationStatus.OOS_NOT_AVAILABLE
    assert governance.walk_forward_status == (
        AvailabilityStatus.WALK_FORWARD_NOT_AVAILABLE.value
    )
    assert governance.robustness_status is RobustnessStatus.ROBUSTNESS_NOT_AVAILABLE
    assert governance.confidence_status is ConfidenceStatus.CONFIDENCE_NOT_AVAILABLE
    assert governance.confidence_score is None


def test_strategy_dossier_remains_unbound() -> None:
    governance = _input_package().governance_state

    assert governance.strategy_dossier_bound is False
    assert governance.strategy_dossier_id is None


def test_temporal_admissibility_status_remains_not_certified() -> None:
    governance = _input_package().governance_state

    assert governance.temporal_admissibility_status == (
        AvailabilityStatus.TEMPORAL_ADMISSIBILITY_NOT_CERTIFIED.value
    )


def test_simulation_status_remains_backtest_not_implemented() -> None:
    governance = _input_package().governance_state

    assert governance.simulation_status is SimulationStatus.BACKTEST_NOT_IMPLEMENTED


def test_paper_trading_eligibility_remains_blocked() -> None:
    governance = _input_package().governance_state

    assert governance.paper_trading_eligibility is PaperTradingEligibility.BLOCKED


def test_serialized_package_does_not_include_dataframe_contents() -> None:
    serialized = _input_package().to_dict()
    text = repr(serialized).lower()

    assert "frame" not in serialized
    assert "dataframe" not in text
    assert "simple_return" not in text
    assert "timestamp" not in serialized["series"]["BTCUSDT|1d"]


def test_serialized_package_omits_empirical_output_fields() -> None:
    serialized = _input_package().to_dict()
    forbidden_terms = {
        "metrics",
        "trades",
        "signals",
        "labels",
        "pnl",
        "evidence",
    }
    serialized_text = repr(serialized).lower()
    package_fields = {field.name.lower() for field in fields(BacktestInputPackage)}
    series_fields = {field.name.lower() for field in fields(InputPackageSeriesReference)}

    assert package_fields.isdisjoint(forbidden_terms)
    assert series_fields.isdisjoint(forbidden_terms)
    assert all(term not in serialized_text for term in forbidden_terms)


def test_deterministic_input_package_id_is_stable_across_repeated_builds() -> None:
    loaded_snapshot = _loaded_snapshot()
    first = InputPackageBuilder(loaded_snapshot).build(
        created_at=datetime(2026, 6, 21, tzinfo=timezone.utc)
    )
    second = InputPackageBuilder(loaded_snapshot).build(
        created_at=datetime(2027, 1, 1, tzinfo=timezone.utc)
    )

    assert first.input_package_id == second.input_package_id


def test_builder_does_not_mutate_loaded_snapshot() -> None:
    loaded_snapshot = _loaded_snapshot()
    series_ids_before = {
        key: id(series.frame) for key, series in loaded_snapshot.series.items()
    }
    series_shapes_before = {
        key: series.frame.shape for key, series in loaded_snapshot.series.items()
    }

    InputPackageBuilder(loaded_snapshot).build()

    assert loaded_snapshot.snapshot_id == "feature_snapshot_technical_v1_1_0_0_20260608_163510"
    assert {
        key: id(series.frame) for key, series in loaded_snapshot.series.items()
    } == series_ids_before
    assert {
        key: series.frame.shape for key, series in loaded_snapshot.series.items()
    } == series_shapes_before
