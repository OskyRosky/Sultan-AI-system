from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import sys

import pytest


BACKTESTING_ROOT = Path(__file__).resolve().parents[1]
if str(BACKTESTING_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKTESTING_ROOT))

from contracts.motor_b_output_contract import (  # noqa: E402
    AllowedDownstreamUsage,
    AvailabilityStatus,
    ConfidenceStatus,
    EvidenceCompletenessLevel,
    ExecutionFrictionStatus,
    ForbiddenDownstreamUsage,
    HistoricalSnapshotStatus,
    OOSValidationStatus,
    OverfittingStatus,
    PaperTradingEligibility,
    SimulationStatus,
    create_framework_only_motor_b_output_contract,
    validate_motor_b_output_contract,
)


def test_framework_only_contract_preserves_blocked_state() -> None:
    contract = create_framework_only_motor_b_output_contract(
        generated_at=datetime(2026, 6, 20, tzinfo=timezone.utc),
    )

    assert contract.evidence_completeness_level is EvidenceCompletenessLevel.FRAMEWORK_ONLY
    assert contract.paper_trading_eligibility is PaperTradingEligibility.BLOCKED
    assert contract.confidence_status is ConfidenceStatus.CONFIDENCE_NOT_AVAILABLE
    assert contract.confidence_score is None
    assert ForbiddenDownstreamUsage.PAPER_TRADING in contract.forbidden_downstream_usage
    assert ForbiddenDownstreamUsage.LIVE_TRADING in contract.forbidden_downstream_usage
    assert ForbiddenDownstreamUsage.CAPITAL_ALLOCATION in contract.forbidden_downstream_usage


def test_framework_only_contract_uses_canonical_allowed_usage() -> None:
    contract = create_framework_only_motor_b_output_contract()

    assert contract.allowed_downstream_usage == (
        AllowedDownstreamUsage.DESIGN_REFERENCE_ONLY,
        AllowedDownstreamUsage.DOCUMENTATION_REVIEW,
        AllowedDownstreamUsage.CONTRACT_VALIDATION,
        AllowedDownstreamUsage.SIMULATION_WITH_MOCK_INPUTS_ONLY,
        AllowedDownstreamUsage.SIGNAL_FUSION_DRY_RUN,
        AllowedDownstreamUsage.OFFLINE_RESEARCH,
        AllowedDownstreamUsage.HUMAN_REVIEW,
    )
    assert AllowedDownstreamUsage.PAPER_TRADING_WITH_FULL_EVIDENCE not in (
        contract.allowed_downstream_usage
    )


def test_framework_only_contract_uses_canonical_missing_evidence() -> None:
    contract = create_framework_only_motor_b_output_contract()

    assert contract.missing_evidence == (
        "research_not_executed",
        "research_output_not_persisted",
        "dossier_not_available",
        "backtest_not_implemented",
        "oos_not_available",
        "walk_forward_not_available",
        "robustness_not_available",
        "confidence_not_available",
    )


def test_framework_only_contract_rejects_status_upgrade() -> None:
    contract = create_framework_only_motor_b_output_contract()
    upgraded = replace(
        contract,
        paper_trading_eligibility=PaperTradingEligibility.ELIGIBLE_FOR_FUTURE_REVIEW,
    )

    with pytest.raises(ValueError, match="framework_only requires paper_trading"):
        validate_motor_b_output_contract(upgraded)


def test_confidence_score_cannot_exist_when_confidence_unavailable() -> None:
    contract = create_framework_only_motor_b_output_contract()
    invalid = replace(contract, confidence_score=0.5)

    with pytest.raises(ValueError, match="confidence_not_available"):
        validate_motor_b_output_contract(invalid)


def test_blocked_contract_cannot_allow_paper_trading_usage() -> None:
    contract = create_framework_only_motor_b_output_contract()
    invalid = replace(
        contract,
        allowed_downstream_usage=(
            *contract.allowed_downstream_usage,
            AllowedDownstreamUsage.PAPER_TRADING_WITH_FULL_EVIDENCE,
        ),
    )

    with pytest.raises(ValueError, match="paper_trading_with_full_evidence"):
        validate_motor_b_output_contract(invalid)


@pytest.mark.parametrize(
    ("field_name", "invalid_value", "expected_status"),
    (
        (
            "historical_snapshot_status",
            "anything_else",
            HistoricalSnapshotStatus.HISTORICAL_SNAPSHOT_NOT_BOUND,
        ),
        (
            "execution_friction_status",
            "anything_else",
            ExecutionFrictionStatus.EXECUTION_FRICTION_NOT_AVAILABLE,
        ),
        (
            "overfitting_status",
            "anything_else",
            OverfittingStatus.OVERFITTING_NOT_EVALUATED,
        ),
    ),
)
def test_factory_statuses_are_controlled_values(
    field_name: str,
    invalid_value: str,
    expected_status: object,
) -> None:
    contract = create_framework_only_motor_b_output_contract()

    assert getattr(contract, field_name) is expected_status
    with pytest.raises(ValueError, match=f"{field_name} must be a controlled"):
        validate_motor_b_output_contract(replace(contract, **{field_name: invalid_value}))


def test_invalid_schema_version_fails() -> None:
    contract = create_framework_only_motor_b_output_contract()

    with pytest.raises(ValueError, match="schema_version must follow SemVer"):
        validate_motor_b_output_contract(replace(contract, schema_version="1.0"))


def test_wrong_owner_stage_fails() -> None:
    contract = create_framework_only_motor_b_output_contract()

    with pytest.raises(ValueError, match="owner_stage must equal 06 Backtesting Engine"):
        validate_motor_b_output_contract(replace(contract, owner_stage="07 Signal Fusion"))


def test_missing_signal_fusion_downstream_consumer_fails() -> None:
    contract = create_framework_only_motor_b_output_contract()

    with pytest.raises(ValueError, match="downstream_consumer_stage must include"):
        validate_motor_b_output_contract(
            replace(contract, downstream_consumer_stage=("08 Risk Engine",))
        )


@pytest.mark.parametrize(
    "field_name",
    ("audit_references", "source_stage_references"),
)
def test_required_reference_sequences_cannot_be_empty(field_name: str) -> None:
    contract = create_framework_only_motor_b_output_contract()

    with pytest.raises(ValueError, match=f"{field_name} must contain"):
        validate_motor_b_output_contract(replace(contract, **{field_name: ()}))


def test_oos_passed_requires_oos_validated_evidence_level() -> None:
    contract = create_framework_only_motor_b_output_contract()

    with pytest.raises(ValueError, match="oos_passed requires oos_validated"):
        validate_motor_b_output_contract(
            replace(contract, oos_validation_status=OOSValidationStatus.OOS_PASSED)
        )


def test_backtest_not_implemented_requires_matching_summary_status() -> None:
    contract = create_framework_only_motor_b_output_contract()

    with pytest.raises(ValueError, match="matching result summary status"):
        validate_motor_b_output_contract(
            replace(contract, backtest_result_summary={"status": "backtest_not_executed"})
        )


def test_metrics_available_fails_when_backtest_not_implemented() -> None:
    contract = create_framework_only_motor_b_output_contract()

    with pytest.raises(ValueError, match="metrics cannot be available"):
        validate_motor_b_output_contract(
            replace(
                contract,
                performance_metrics_status=AvailabilityStatus.METRICS_AVAILABLE.value,
            )
        )


def test_temporal_not_certified_fails_with_simulation_executed() -> None:
    contract = create_framework_only_motor_b_output_contract()

    with pytest.raises(ValueError, match="simulation cannot execute"):
        validate_motor_b_output_contract(
            replace(
                contract,
                simulation_status=SimulationStatus.SIMULATION_EXECUTED,
            )
        )
