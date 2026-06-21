from __future__ import annotations

from dataclasses import fields, replace
from pathlib import Path
import sys

import pytest


BACKTESTING_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKTESTING_ROOT.parents[0]
STRATEGY_ENGINE_ROOT = REPO_ROOT / "05 Strategy Engine"
if str(BACKTESTING_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKTESTING_ROOT))
if str(STRATEGY_ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from adapters.strategy_dossier_adapter import (  # noqa: E402
    AdaptedBacktestPackage,
    AdaptedSeriesReference,
    StrategyDossierAdapter,
)
from loaders.feature_snapshot_loader import FeatureSnapshotLoader  # noqa: E402
from mockups.strategy_dossier_mockups import FICTITIOUS_STRATEGY_DOSSIER  # noqa: E402
from packages.input_package_builder import (  # noqa: E402
    BacktestInputPackage,
    InputPackageBuilder,
)


MANIFEST_PATH = REPO_ROOT / (
    "03 Feature Engineering/manifests/"
    "feature_snapshot_technical_v1_1_0_0_20260608_163510.json"
)
SCHEMA_PATH = REPO_ROOT / "03 Feature Engineering/schemas/feature_snapshot_manifest_schema.json"


def _input_package() -> BacktestInputPackage:
    loaded_snapshot = FeatureSnapshotLoader(MANIFEST_PATH, schema_path=SCHEMA_PATH).load()
    return InputPackageBuilder(loaded_snapshot).build()


def _adapted_package() -> AdaptedBacktestPackage:
    return StrategyDossierAdapter(
        _input_package(),
        FICTITIOUS_STRATEGY_DOSSIER,
    ).adapt()


def _dossier_with_attr(name: str, value: object):
    dossier = replace(FICTITIOUS_STRATEGY_DOSSIER)
    object.__setattr__(dossier, name, value)
    return dossier


def test_adapter_builds_from_valid_package_and_dossier() -> None:
    adapted = _adapted_package()

    assert adapted.adapted_package_id.startswith("adapted-backtest-")
    assert adapted.strategy_id == FICTITIOUS_STRATEGY_DOSSIER.dossier_id
    assert adapted.input_package_id == _input_package().input_package_id


def test_adapted_package_preserves_lineage_metadata() -> None:
    input_package = _input_package()
    adapted = StrategyDossierAdapter(input_package, FICTITIOUS_STRATEGY_DOSSIER).adapt()

    assert adapted.input_package_id == input_package.input_package_id
    assert adapted.snapshot_id == input_package.snapshot_id
    assert adapted.feature_set == input_package.feature_set
    assert adapted.feature_version == input_package.feature_version
    assert adapted.code_commit == input_package.code_commit
    assert adapted.manifest_path == input_package.manifest_path
    assert adapted.schema_path == input_package.schema_path
    assert adapted.gap_report_reference == input_package.gap_report_reference
    assert adapted.quality_report_reference == input_package.quality_report_reference
    assert adapted.warmup_policy == input_package.warmup_policy


def test_adapted_package_preserves_governance_restrictions() -> None:
    adapted = _adapted_package()
    governance = adapted.governance_state

    assert governance.temporal_admissibility_status == (
        "temporal_admissibility_not_certified"
    )
    assert governance.simulation_status == "backtest_not_implemented"
    assert governance.oos_validation_status == "oos_not_available"
    assert governance.walk_forward_status == "walk_forward_not_available"
    assert governance.robustness_status == "robustness_not_available"
    assert governance.confidence_status == "confidence_not_available"
    assert governance.confidence_score is None
    assert governance.paper_trading_eligibility == "blocked"
    assert governance.stage_09_readiness == "blocked"
    assert governance.handoff_to_09 == "blocked"


def test_deterministic_adapted_package_id_is_stable() -> None:
    input_package = _input_package()

    first = StrategyDossierAdapter(input_package, FICTITIOUS_STRATEGY_DOSSIER).adapt()
    second = StrategyDossierAdapter(input_package, FICTITIOUS_STRATEGY_DOSSIER).adapt()

    assert first.adapted_package_id == second.adapted_package_id


def test_adapter_rejects_missing_dossier() -> None:
    with pytest.raises(ValueError, match="StrategyDossier is required"):
        StrategyDossierAdapter(_input_package(), None).adapt()


def test_adapter_rejects_empty_strategy_id() -> None:
    dossier = replace(FICTITIOUS_STRATEGY_DOSSIER, dossier_id="")

    with pytest.raises(ValueError, match="strategy_id must be a non-empty string"):
        StrategyDossierAdapter(_input_package(), dossier).adapt()


def test_adapter_rejects_empty_strategy_name() -> None:
    closure_record = replace(
        FICTITIOUS_STRATEGY_DOSSIER.closure_record,
        closure_summary="",
    )
    dossier = replace(FICTITIOUS_STRATEGY_DOSSIER, closure_record=closure_record)

    with pytest.raises(ValueError, match="strategy_name must be a non-empty string"):
        StrategyDossierAdapter(_input_package(), dossier).adapt()


def test_adapter_rejects_empty_strategy_version() -> None:
    closure_record = replace(
        FICTITIOUS_STRATEGY_DOSSIER.closure_record,
        closure_id="",
    )
    dossier = replace(FICTITIOUS_STRATEGY_DOSSIER, closure_record=closure_record)

    with pytest.raises(ValueError, match="strategy_version must be a non-empty string"):
        StrategyDossierAdapter(_input_package(), dossier).adapt()


def test_adapter_rejects_deprecated_dossier() -> None:
    dossier = _dossier_with_attr("status", "deprecated")

    with pytest.raises(ValueError, match="deprecated"):
        StrategyDossierAdapter(_input_package(), dossier).adapt()


def test_adapter_rejects_archived_dossier() -> None:
    dossier = _dossier_with_attr("status", "archived")

    with pytest.raises(ValueError, match="archived"):
        StrategyDossierAdapter(_input_package(), dossier).adapt()


def test_adapter_rejects_incompatible_feature_set() -> None:
    dossier = _dossier_with_attr("required_feature_set", "different_feature_set")

    with pytest.raises(ValueError, match="feature_set requirements"):
        StrategyDossierAdapter(_input_package(), dossier).adapt()


def test_adapter_rejects_unavailable_symbol() -> None:
    dossier = _dossier_with_attr("required_symbols", ("SOLUSDT",))

    with pytest.raises(ValueError, match="unavailable symbols"):
        StrategyDossierAdapter(_input_package(), dossier).adapt()


def test_adapter_rejects_unavailable_timeframe() -> None:
    dossier = _dossier_with_attr("required_timeframes", ("1h",))

    with pytest.raises(ValueError, match="unavailable timeframes"):
        StrategyDossierAdapter(_input_package(), dossier).adapt()


def test_serialized_object_excludes_dataframes() -> None:
    serialized = _adapted_package().to_dict()
    text = repr(serialized).lower()

    assert "frame" not in serialized
    assert "dataframe" not in text


@pytest.mark.parametrize(
    "forbidden_term",
    ("metrics", "signals", "labels", "trades", "pnl", "evidence"),
)
def test_serialized_object_excludes_empirical_fields(forbidden_term: str) -> None:
    serialized = _adapted_package().to_dict()
    serialized_text = repr(serialized).lower()
    adapted_fields = {field.name.lower() for field in fields(AdaptedBacktestPackage)}
    series_fields = {field.name.lower() for field in fields(AdaptedSeriesReference)}

    assert forbidden_term not in serialized_text
    assert forbidden_term not in adapted_fields
    assert forbidden_term not in series_fields


def test_adapter_does_not_mutate_backtest_input_package() -> None:
    input_package = _input_package()
    series_ids_before = {key: id(value) for key, value in input_package.series.items()}
    serialized_before = input_package.to_dict()

    StrategyDossierAdapter(input_package, FICTITIOUS_STRATEGY_DOSSIER).adapt()

    assert input_package.to_dict() == serialized_before
    assert {key: id(value) for key, value in input_package.series.items()} == (
        series_ids_before
    )
