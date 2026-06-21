from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
from datetime import datetime, timezone
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

from adapters.strategy_dossier_adapter import StrategyDossierAdapter  # noqa: E402
from assumptions.execution_assumptions import (  # noqa: E402
    ExecutionAssumptionSet,
    FeeModelType,
    OrderExecutionTiming,
    SlippageModelType,
    create_default_dry_run_execution_assumptions,
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
    TemporalAdmissibilityValidator,
)


MANIFEST_PATH = REPO_ROOT / (
    "03 Feature Engineering/manifests/"
    "feature_snapshot_technical_v1_1_0_0_20260608_163510.json"
)
SCHEMA_PATH = REPO_ROOT / "03 Feature Engineering/schemas/feature_snapshot_manifest_schema.json"
VALIDATION_TIMESTAMP = datetime(2026, 6, 21, tzinfo=timezone.utc)


def _governance_gate_result() -> GovernanceGateResult:
    loaded_snapshot = FeatureSnapshotLoader(MANIFEST_PATH, schema_path=SCHEMA_PATH).load()
    input_package = InputPackageBuilder(loaded_snapshot).build()
    adapted_package = StrategyDossierAdapter(
        input_package,
        FICTITIOUS_STRATEGY_DOSSIER,
    ).adapt()
    temporal_result = TemporalAdmissibilityValidator(
        adapted_package,
        validation_timestamp=VALIDATION_TIMESTAMP,
    ).validate()
    return PreExecutionGovernanceGate(
        adapted_package,
        temporal_result,
        validation_timestamp=VALIDATION_TIMESTAMP,
    ).evaluate()


def _default_assumptions() -> ExecutionAssumptionSet:
    return create_default_dry_run_execution_assumptions(_governance_gate_result())


def test_default_dry_run_assumptions_build_from_valid_governance_gate() -> None:
    gate = _governance_gate_result()
    assumptions = create_default_dry_run_execution_assumptions(gate)

    assert assumptions.assumption_set_id.startswith("exec-assumptions-")
    assert assumptions.governance_gate_status is GovernanceGateStatus.PASSED
    assert assumptions.created_for_package_id == gate.package_id
    assert assumptions.created_for_strategy_id == gate.strategy_id
    assert assumptions.created_for_snapshot_id == gate.snapshot_id
    assert assumptions.fee_model_type is FeeModelType.ZERO_FEE_FOR_DRY_RUN_ONLY
    assert assumptions.slippage_model_type is (
        SlippageModelType.ZERO_SLIPPAGE_FOR_DRY_RUN_ONLY
    )


@pytest.mark.parametrize(
    ("field_name", "value", "expected_error"),
    (
        ("assumption_set_id", "", "assumption_set_id must be a non-empty string"),
        ("assumption_version", "1.0", "assumption_version must follow SemVer"),
        ("created_for_package_id", "", "created_for_package_id must be a non-empty string"),
        ("created_for_strategy_id", "", "created_for_strategy_id must be a non-empty string"),
        ("created_for_snapshot_id", "", "created_for_snapshot_id must be a non-empty string"),
    ),
)
def test_required_identity_fields_are_validated(
    field_name: str,
    value: object,
    expected_error: str,
) -> None:
    with pytest.raises(ValueError, match=expected_error):
        replace(_default_assumptions(), **{field_name: value})


def test_non_passed_governance_gate_rejected() -> None:
    gate = replace(
        _governance_gate_result(),
        gate_status=GovernanceGateStatus.REJECTED,
    )

    with pytest.raises(ValueError, match="governance_gate_status must be passed"):
        create_default_dry_run_execution_assumptions(gate)


@pytest.mark.parametrize(
    "field_name",
    ("maker_fee_bps", "taker_fee_bps", "flat_fee_bps"),
)
def test_negative_fees_rejected(field_name: str) -> None:
    with pytest.raises(ValueError, match="fees cannot be negative"):
        replace(_default_assumptions(), **{field_name: -0.1})


def test_negative_slippage_rejected() -> None:
    with pytest.raises(ValueError, match="slippage cannot be negative"):
        replace(_default_assumptions(), slippage_bps=-0.1)


@pytest.mark.parametrize("starting_capital", (0.0, -1.0))
def test_starting_capital_must_be_positive(starting_capital: float) -> None:
    with pytest.raises(ValueError, match="starting_capital must be positive"):
        replace(_default_assumptions(), starting_capital=starting_capital)


def test_max_position_fraction_greater_than_one_rejected() -> None:
    with pytest.raises(ValueError, match="max_position_fraction"):
        replace(_default_assumptions(), max_position_fraction=1.01)


def test_max_position_fraction_zero_or_less_rejected() -> None:
    with pytest.raises(ValueError, match="max_position_fraction"):
        replace(_default_assumptions(), max_position_fraction=0.0)


def test_leverage_false_requires_max_leverage_one() -> None:
    with pytest.raises(ValueError, match="allow_leverage false"):
        replace(_default_assumptions(), allow_leverage=False, max_leverage=2.0)


def test_leverage_true_requires_max_leverage_greater_than_one() -> None:
    with pytest.raises(ValueError, match="allow_leverage true"):
        replace(_default_assumptions(), allow_leverage=True, max_leverage=1.0)


def test_same_bar_close_forbidden_rejected_as_executable_timing() -> None:
    with pytest.raises(ValueError, match="same_bar_close_forbidden"):
        replace(
            _default_assumptions(),
            order_execution_timing=OrderExecutionTiming.SAME_BAR_CLOSE_FORBIDDEN,
        )


def test_zero_fee_dry_run_warning_present() -> None:
    assumptions = _default_assumptions()

    assert any("zero_fee_for_dry_run_only" in warning for warning in assumptions.warnings)
    assert any("production realism" in warning for warning in assumptions.warnings)


def test_zero_slippage_dry_run_warning_present() -> None:
    assumptions = _default_assumptions()

    assert any(
        "zero_slippage_for_dry_run_only" in warning
        for warning in assumptions.warnings
    )
    assert any("production realism" in warning for warning in assumptions.warnings)


def test_forbidden_usage_contains_required_values() -> None:
    assumptions = _default_assumptions()

    assert {
        "paper_trading",
        "live_trading",
        "capital_allocation",
        "strategy_promotion",
        "confidence_scoring",
    }.issubset(set(assumptions.forbidden_usage))


def test_deterministic_output() -> None:
    gate = _governance_gate_result()
    first = create_default_dry_run_execution_assumptions(gate)
    second = create_default_dry_run_execution_assumptions(gate)

    assert first == second
    assert first.to_dict() == second.to_dict()


def test_frozen_dataclass_enforcement() -> None:
    assumptions = _default_assumptions()

    with pytest.raises(FrozenInstanceError):
        assumptions.starting_capital = 1.0


def test_no_mutation_of_governance_gate_result() -> None:
    gate = _governance_gate_result()
    before = gate.to_dict()

    create_default_dry_run_execution_assumptions(gate)

    assert gate.to_dict() == before


def test_no_parquet_loading(monkeypatch: pytest.MonkeyPatch) -> None:
    gate = _governance_gate_result()

    def fail_read_parquet(*args, **kwargs):
        raise AssertionError("assumption factory must not load parquet")

    monkeypatch.setattr(pd, "read_parquet", fail_read_parquet)

    assert create_default_dry_run_execution_assumptions(gate).governance_gate_status is (
        GovernanceGateStatus.PASSED
    )


def test_no_metrics_trades_signals_labels_or_pnl_fields() -> None:
    assumptions = _default_assumptions()
    field_names = {field.name.lower() for field in fields(ExecutionAssumptionSet)}
    serialized_keys = {key.lower() for key in assumptions.to_dict()}

    for forbidden in ("metrics", "trades", "signals", "labels", "pnl"):
        assert forbidden not in field_names
        assert forbidden not in serialized_keys


def test_no_simulation_backtest_oos_walk_forward_or_robustness_fields() -> None:
    assumptions = _default_assumptions()
    field_names = {field.name.lower() for field in fields(ExecutionAssumptionSet)}
    serialized_keys = {key.lower() for key in assumptions.to_dict()}

    for forbidden in ("simulation", "backtest", "oos", "walk_forward", "robustness"):
        assert forbidden not in field_names
        assert forbidden not in serialized_keys
