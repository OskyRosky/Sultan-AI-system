from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

import pandas as pd
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
    StrategyDossierAdapter,
)
from governance.pre_execution_governance_gate import (  # noqa: E402
    GovernanceGateResult,
    GovernanceGateStatus,
    PreExecutionGovernanceGate,
)
from loaders.feature_snapshot_loader import FeatureSnapshotLoader  # noqa: E402
from mockups.strategy_dossier_mockups import FICTITIOUS_STRATEGY_DOSSIER  # noqa: E402
from packages.input_package_builder import InputPackageBuilder  # noqa: E402
from validators.temporal_admissibility_validator import (  # noqa: E402
    TemporalAdmissibilityResult,
    TemporalAdmissibilityStatus,
    TemporalAdmissibilityValidator,
)


MANIFEST_PATH = REPO_ROOT / (
    "03 Feature Engineering/manifests/"
    "feature_snapshot_technical_v1_1_0_0_20260608_163510.json"
)
SCHEMA_PATH = REPO_ROOT / "03 Feature Engineering/schemas/feature_snapshot_manifest_schema.json"
VALIDATION_TIMESTAMP = datetime(2026, 6, 21, tzinfo=timezone.utc)


def _adapted_package() -> AdaptedBacktestPackage:
    loaded_snapshot = FeatureSnapshotLoader(MANIFEST_PATH, schema_path=SCHEMA_PATH).load()
    input_package = InputPackageBuilder(loaded_snapshot).build()
    return StrategyDossierAdapter(input_package, FICTITIOUS_STRATEGY_DOSSIER).adapt()


def _temporal_result(
    package: AdaptedBacktestPackage,
) -> TemporalAdmissibilityResult:
    return TemporalAdmissibilityValidator(
        package,
        validation_timestamp=VALIDATION_TIMESTAMP,
    ).validate()


def _gate_result(
    package: AdaptedBacktestPackage,
    temporal_result: TemporalAdmissibilityResult,
) -> GovernanceGateResult:
    return PreExecutionGovernanceGate(
        package,
        temporal_result,
        validation_timestamp=VALIDATION_TIMESTAMP,
    ).evaluate()


def test_valid_package_passes() -> None:
    package = _adapted_package()
    result = _gate_result(package, _temporal_result(package))

    assert result.gate_status is GovernanceGateStatus.PASSED
    assert result.blocking_failures == ()
    assert "future empirical execution stage" in result.gate_reason
    assert "strategy profitable" in result.gate_reason


@pytest.mark.parametrize(
    ("field_name", "expected_failure"),
    (
        ("adapted_package_id", "package_id must be present"),
        ("strategy_id", "strategy_id must be present"),
        ("strategy_version", "strategy_version must be present"),
        ("snapshot_id", "snapshot_id must be present"),
    ),
)
def test_missing_package_identity_rejected(
    field_name: str,
    expected_failure: str,
) -> None:
    package = replace(_adapted_package(), **{field_name: ""})
    result = _gate_result(package, _temporal_result(_adapted_package()))

    assert result.gate_status is GovernanceGateStatus.REJECTED
    assert expected_failure in result.blocking_failures


def test_temporal_certification_rejected() -> None:
    package = _adapted_package()
    temporal = replace(
        _temporal_result(package),
        admissible=False,
        certification_status=TemporalAdmissibilityStatus.REJECTED,
    )

    result = _gate_result(package, temporal)

    assert result.gate_status is GovernanceGateStatus.REJECTED
    assert "temporal certification is rejected" in result.blocking_failures


def test_temporal_certification_insufficient_information() -> None:
    package = _adapted_package()
    temporal = replace(
        _temporal_result(package),
        admissible=False,
        certification_status=TemporalAdmissibilityStatus.INSUFFICIENT_INFORMATION,
    )

    result = _gate_result(package, temporal)

    assert result.gate_status is GovernanceGateStatus.INSUFFICIENT_INFORMATION
    assert "temporal certification has insufficient information" in (
        result.blocking_failures
    )


def test_wrong_certification_scope_rejected() -> None:
    package = _adapted_package()
    temporal = replace(_temporal_result(package), certification_scope="strategy_level")

    result = _gate_result(package, temporal)

    assert result.gate_status is GovernanceGateStatus.REJECTED
    assert "certification_scope must be package_metadata_only" in result.blocking_failures


def test_missing_handoff_required_rejected() -> None:
    package = _adapted_package()
    temporal = replace(_temporal_result(package), handoff_required=False)

    result = _gate_result(package, temporal)

    assert result.gate_status is GovernanceGateStatus.REJECTED
    assert "handoff_required must be true" in result.blocking_failures


def test_wrong_handoff_target_rejected() -> None:
    package = _adapted_package()
    temporal = replace(_temporal_result(package), handoff_target="Block 08")

    result = _gate_result(package, temporal)

    assert result.gate_status is GovernanceGateStatus.REJECTED
    assert "handoff_target must be Block 07" in result.blocking_failures


@pytest.mark.parametrize(
    ("field_name", "value", "expected_failure"),
    (
        ("manifest_path", Path("missing-manifest.json"), "manifest_path must reference"),
        ("schema_path", Path("missing-schema.json"), "schema_path must reference"),
        ("gap_report_reference", "", "gap_report_reference must be present"),
        (
            "quality_report_reference",
            "",
            "quality_report_reference must be present",
        ),
    ),
)
def test_missing_lineage_rejected(
    field_name: str,
    value: object,
    expected_failure: str,
) -> None:
    package = replace(_adapted_package(), **{field_name: value})
    result = _gate_result(package, _temporal_result(_adapted_package()))

    assert result.gate_status is GovernanceGateStatus.REJECTED
    assert any(expected_failure in failure for failure in result.blocking_failures)


def test_duplicate_series_rejected() -> None:
    package = _adapted_package()
    first_key = next(iter(package.series))
    first_series = package.series[first_key]
    series = dict(package.series)
    series[("DUPLICATE", "1d")] = first_series

    result = _gate_result(
        replace(package, series=series),
        _temporal_result(package),
    )

    assert result.gate_status is GovernanceGateStatus.REJECTED
    assert any("duplicate symbol/timeframe" in failure for failure in result.blocking_failures)


def test_invalid_timestamps_rejected() -> None:
    package = _adapted_package()
    first_key = next(iter(package.series))
    first_series = package.series[first_key]
    series = dict(package.series)
    series[first_key] = replace(
        first_series,
        min_timestamp=first_series.max_timestamp + timedelta(days=1),
    )

    result = _gate_result(
        replace(package, series=series),
        _temporal_result(package),
    )

    assert result.gate_status is GovernanceGateStatus.REJECTED
    assert any("min_timestamp must be <=" in failure for failure in result.blocking_failures)


def test_deterministic_output() -> None:
    package = _adapted_package()
    temporal = _temporal_result(package)

    first = _gate_result(package, temporal)
    second = _gate_result(package, temporal)

    assert first == second
    assert first.to_dict() == second.to_dict()


def test_frozen_dataclass_enforcement() -> None:
    package = _adapted_package()
    result = _gate_result(package, _temporal_result(package))

    with pytest.raises(FrozenInstanceError):
        result.gate_status = GovernanceGateStatus.REJECTED


def test_no_mutation_of_inputs() -> None:
    package = _adapted_package()
    temporal = _temporal_result(package)
    package_before = package.to_dict()
    temporal_before = temporal.to_dict()

    _gate_result(package, temporal)

    assert package.to_dict() == package_before
    assert temporal.to_dict() == temporal_before


def test_no_parquet_loading(monkeypatch: pytest.MonkeyPatch) -> None:
    package = _adapted_package()
    temporal = _temporal_result(package)

    def fail_read_parquet(*args, **kwargs):
        raise AssertionError("governance gate must not load parquet")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    assert _gate_result(package, temporal).gate_status is GovernanceGateStatus.PASSED


def test_no_metrics_trades_signals_labels_or_pnl_fields() -> None:
    package = _adapted_package()
    result = _gate_result(package, _temporal_result(package))
    field_names = {field.name.lower() for field in fields(GovernanceGateResult)}
    serialized = repr(result.to_dict()).lower()

    for forbidden in ("metrics", "trades", "signals", "labels", "pnl"):
        assert forbidden not in field_names
        assert forbidden not in serialized


def test_governance_consistency_blocks_readiness_upgrades() -> None:
    package = _adapted_package()
    governance = replace(package.governance_state, stage_09_readiness="ready")
    package = replace(package, governance_state=governance)

    result = _gate_result(package, _temporal_result(_adapted_package()))

    assert result.gate_status is GovernanceGateStatus.REJECTED
    assert "Stage 09 readiness must remain blocked" in result.blocking_failures
