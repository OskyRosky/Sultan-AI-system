"""Executable Motor B Output Contract models.

These models implement the non-empirical contract surface documented in
``docs/18_motor_b_output_contract.md``. They validate evidence state and
downstream blocking semantics only; they do not run backtests or produce
historical evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
import re
from typing import Any, Mapping, Sequence


SEMVER_PATTERN = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


class EvidenceCompletenessLevel(str, Enum):
    FRAMEWORK_ONLY = "framework_only"
    PARTIAL_EMPIRICAL = "partial_empirical"
    BACKTEST_VALIDATED = "backtest_validated"
    OOS_VALIDATED = "oos_validated"


class ConfidenceStatus(str, Enum):
    CONFIDENCE_NOT_AVAILABLE = "confidence_not_available"
    CONFIDENCE_NOT_COMPUTABLE = "confidence_not_computable"
    CONFIDENCE_COMPUTED_FROM_BACKTEST = "confidence_computed_from_backtest"
    CONFIDENCE_COMPUTED_FROM_OOS = "confidence_computed_from_oos"
    CONFIDENCE_REJECTED_DUE_TO_INCOMPLETE_EVIDENCE = (
        "confidence_rejected_due_to_incomplete_evidence"
    )


class ApprovalStatus(str, Enum):
    NOT_APPROVED = "not_approved"
    NOT_EVALUATED = "not_evaluated"
    DOCUMENTATION_ONLY = "documentation_only"
    PENDING_HUMAN_REVIEW = "pending_human_review"
    REJECTED = "rejected"
    APPROVED_FOR_RESEARCH_ONLY = "approved_for_research_only"


class BacktestEligibilityStatus(str, Enum):
    NOT_EVALUATED = "not_evaluated"
    ELIGIBLE_FOR_BACKTEST_EVALUATION = "eligible_for_backtest_evaluation"
    NOT_ELIGIBLE_MISSING_INFORMATION = "not_eligible_missing_information"
    NOT_ELIGIBLE_MISSING_TRACEABILITY = "not_eligible_missing_traceability"
    NOT_ELIGIBLE_GOVERNANCE_FAILURE = "not_eligible_governance_failure"
    NOT_ELIGIBLE_CANDIDATE_AMBIGUITY = "not_eligible_candidate_ambiguity"
    NOT_ELIGIBLE_INTERNAL_INCONSISTENCY = "not_eligible_internal_inconsistency"
    NOT_ELIGIBLE_OTHER = "not_eligible_other"


class SimulationStatus(str, Enum):
    BACKTEST_NOT_IMPLEMENTED = "backtest_not_implemented"
    BACKTEST_NOT_EXECUTED = "backtest_not_executed"
    SIMULATION_BLOCKED = "simulation_blocked"
    SIMULATION_FAILED = "simulation_failed"
    SIMULATION_EXECUTED = "simulation_executed"
    SIMULATION_RESULT_INVALID = "simulation_result_invalid"


class OOSValidationStatus(str, Enum):
    OOS_NOT_AVAILABLE = "oos_not_available"
    OOS_NOT_EXECUTED = "oos_not_executed"
    OOS_PASSED = "oos_passed"
    OOS_FAILED = "oos_failed"
    OOS_INCONCLUSIVE = "oos_inconclusive"
    OOS_INVALID = "oos_invalid"


class RobustnessStatus(str, Enum):
    ROBUSTNESS_NOT_AVAILABLE = "robustness_not_available"
    ROBUSTNESS_NOT_EXECUTED = "robustness_not_executed"
    ROBUST_RESULT = "robust_result"
    FRAGILE_RESULT = "fragile_result"
    FALSIFIED_RESULT = "falsified_result"
    OVERFIT_RESULT = "overfit_result"
    INCONCLUSIVE_RESULT = "inconclusive_result"
    ROBUSTNESS_REVIEW_FAILED = "robustness_review_failed"


class PaperTradingEligibility(str, Enum):
    BLOCKED = "blocked"
    NOT_EVALUATED = "not_evaluated"
    REQUIRES_RISK_ENGINE_REVIEW = "requires_risk_engine_review"
    REQUIRES_HUMAN_REVIEW = "requires_human_review"
    ELIGIBLE_FOR_FUTURE_REVIEW = "eligible_for_future_review"


class AllowedDownstreamUsage(str, Enum):
    DESIGN_REFERENCE_ONLY = "design_reference_only"
    DOCUMENTATION_REVIEW = "documentation_review"
    CONTRACT_VALIDATION = "contract_validation"
    SIMULATION_WITH_MOCK_INPUTS_ONLY = "simulation_with_mock_inputs_only"
    SIGNAL_FUSION_DRY_RUN = "signal_fusion_dry_run"
    OFFLINE_RESEARCH = "offline_research"
    HUMAN_REVIEW = "human_review"
    PAPER_TRADING_WITH_FULL_EVIDENCE = "paper_trading_with_full_evidence"


class ForbiddenDownstreamUsage(str, Enum):
    PAPER_TRADING = "paper_trading"
    PAPER_TRADING_WITHOUT_OOS = "paper_trading_without_oos"
    LIVE_TRADING = "live_trading"
    CAPITAL_ALLOCATION = "capital_allocation"
    AUTONOMOUS_EXECUTION = "autonomous_execution"
    PRODUCTION_SIGNAL_ROUTING = "production_signal_routing"
    RISK_LIMIT_RELAXATION = "risk_limit_relaxation"
    RISK_BYPASS = "risk_bypass"
    CONFIDENCE_GENERATION = "confidence_generation"
    STRATEGY_PROMOTION = "strategy_promotion"
    EXECUTION_SIGNAL_GENERATION = "execution_signal_generation"
    PERFORMANCE_CLAIMS = "performance_claims"


class HumanReviewStatus(str, Enum):
    HUMAN_REVIEW_NOT_REQUESTED = "human_review_not_requested"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    HUMAN_REVIEW_IN_PROGRESS = "human_review_in_progress"
    HUMAN_REVIEW_PASSED = "human_review_passed"
    HUMAN_REVIEW_REJECTED = "human_review_rejected"


class SchemaValidationStatus(str, Enum):
    SCHEMA_VALID = "schema_valid"
    SCHEMA_INVALID = "schema_invalid"
    SCHEMA_VALID_GOVERNANCE_BLOCKED = "schema_valid_governance_blocked"


class ContractGenerationMode(str, Enum):
    CONTRACT_GENERATED_FROM_DOCUMENTATION = "contract_generated_from_documentation"
    CONTRACT_GENERATED_FROM_MOCKUPS = "contract_generated_from_mockups"
    CONTRACT_GENERATED_FROM_REAL_ARTIFACTS = "contract_generated_from_real_artifacts"
    CONTRACT_GENERATED_FROM_MIXED_SOURCES = "contract_generated_from_mixed_sources"


class AvailabilityStatus(str, Enum):
    DOSSIER_NOT_AVAILABLE = "dossier_not_available"
    DOSSIER_MOCK_ONLY = "dossier_mock_only"
    DOSSIER_PREPARED_PENDING_FINAL_AUDIT = "dossier_prepared_pending_final_audit"
    CANDIDATE_NOT_AVAILABLE = "candidate_not_available"
    CANDIDATE_MOCK_ONLY = "candidate_mock_only"
    CANDIDATE_CONCEPTUAL_ONLY = "candidate_conceptual_only"
    CANDIDATE_AVAILABLE = "candidate_available"
    REGIME_CONTEXT_NOT_AVAILABLE = "regime_context_not_available"
    REGIME_CONTEXT_FRAMEWORK_ONLY = "regime_context_framework_only"
    REGIME_CONTEXT_AVAILABLE = "regime_context_available"
    REGIME_CONTEXT_REAL_EMPIRICAL = "regime_context_real_empirical"
    RESEARCH_NOT_EXECUTED = "research_not_executed"
    RESEARCH_EXECUTED_PARTIAL = "research_executed_partial"
    RESEARCH_OUTPUT_NOT_PERSISTED = "research_output_not_persisted"
    DOCUMENTATION_ONLY = "documentation_only"
    TEMPORAL_ADMISSIBILITY_NOT_CERTIFIED = "temporal_admissibility_not_certified"
    FALSIFICATION_NOT_EXECUTED = "falsification_not_executed"
    WALK_FORWARD_NOT_AVAILABLE = "walk_forward_not_available"
    ROBUSTNESS_NOT_AVAILABLE = "robustness_not_available"
    CONFIDENCE_NOT_AVAILABLE = "confidence_not_available"
    METRICS_NOT_AVAILABLE = "metrics_not_available"
    METRICS_AVAILABLE = "metrics_available"
    NOT_APPROVED = "not_approved"


class HistoricalSnapshotStatus(str, Enum):
    HISTORICAL_SNAPSHOT_NOT_BOUND = "historical_snapshot_not_bound"
    HISTORICAL_SNAPSHOT_BOUND = "historical_snapshot_bound"


class ExecutionFrictionStatus(str, Enum):
    EXECUTION_FRICTION_NOT_AVAILABLE = "execution_friction_not_available"
    EXECUTION_FRICTION_AVAILABLE = "execution_friction_available"


class OverfittingStatus(str, Enum):
    OVERFITTING_NOT_EVALUATED = "overfitting_not_evaluated"
    OVERFITTING_EVALUATED = "overfitting_evaluated"


@dataclass(frozen=True)
class MotorBOutputContract:
    """Minimum executable Motor B contract consumed by stages 07 and 08."""

    motor_b_output_id: str
    schema_version: str
    generated_at: datetime
    owner_stage: str
    downstream_consumer_stage: tuple[str, ...]
    source_stage_references: tuple[str, ...]
    strategy_dossier_id: str | None
    strategy_handoff_status: str
    candidate_id: str | None
    candidate_status: str
    regime_context: Mapping[str, Any] | None
    regime_context_status: str
    research_execution_status: str
    backtest_eligibility_status: BacktestEligibilityStatus
    temporal_admissibility_status: str
    historical_snapshot_status: HistoricalSnapshotStatus
    simulation_status: SimulationStatus
    execution_friction_status: ExecutionFrictionStatus
    performance_metrics_status: str
    backtest_result_summary: Mapping[str, Any]
    oos_validation_status: OOSValidationStatus
    oos_validation_report: Mapping[str, Any] | None
    walk_forward_status: str
    walk_forward_summary: Mapping[str, Any] | None
    robustness_status: RobustnessStatus
    overfitting_status: OverfittingStatus
    falsification_status: str
    confidence_status: ConfidenceStatus
    confidence_score: float | None
    approval_status: ApprovalStatus
    non_approval_statement: str
    risk_engine_required_action: tuple[str, ...]
    paper_trading_eligibility: PaperTradingEligibility
    evidence_completeness_level: EvidenceCompletenessLevel
    missing_evidence: tuple[str, ...]
    blocking_gaps: tuple[str, ...]
    allowed_downstream_usage: tuple[AllowedDownstreamUsage, ...]
    forbidden_downstream_usage: tuple[ForbiddenDownstreamUsage, ...]
    audit_references: tuple[str, ...]
    schema_validation_status: SchemaValidationStatus
    contract_generation_mode: ContractGenerationMode
    human_review_status: HumanReviewStatus


def validate_motor_b_output_contract(contract: MotorBOutputContract) -> MotorBOutputContract:
    """Validate documented Motor B invariants without changing any status."""

    _require_text(contract.motor_b_output_id, "motor_b_output_id")
    _require_semver(contract.schema_version, "schema_version")
    if contract.owner_stage != "06 Backtesting Engine":
        raise ValueError("owner_stage must equal 06 Backtesting Engine")
    if "07 Signal Fusion + LLM Motors" not in contract.downstream_consumer_stage:
        raise ValueError("downstream_consumer_stage must include 07 Signal Fusion + LLM Motors")
    _require_non_empty_sequence(contract.source_stage_references, "source_stage_references")
    _require_non_empty_sequence(contract.audit_references, "audit_references")
    _require_text(contract.non_approval_statement, "non_approval_statement")
    _require_enum(
        contract.historical_snapshot_status,
        HistoricalSnapshotStatus,
        "historical_snapshot_status",
    )
    _require_enum(
        contract.execution_friction_status,
        ExecutionFrictionStatus,
        "execution_friction_status",
    )
    _require_enum(contract.overfitting_status, OverfittingStatus, "overfitting_status")

    if (
        contract.strategy_dossier_id is None
        and contract.strategy_handoff_status != AvailabilityStatus.DOSSIER_NOT_AVAILABLE.value
    ):
        raise ValueError("strategy_dossier_id null requires dossier_not_available status")
    if (
        contract.candidate_id is None
        and contract.candidate_status != AvailabilityStatus.CANDIDATE_NOT_AVAILABLE.value
    ):
        raise ValueError("candidate_id null requires candidate_not_available status")
    if (
        contract.regime_context is None
        and contract.regime_context_status
        != AvailabilityStatus.REGIME_CONTEXT_NOT_AVAILABLE.value
    ):
        raise ValueError("regime_context null requires regime_context_not_available status")

    if (
        contract.confidence_status is ConfidenceStatus.CONFIDENCE_NOT_AVAILABLE
        and contract.confidence_score is not None
    ):
        raise ValueError("confidence_not_available requires confidence_score null")
    if contract.confidence_score is not None:
        if not 0.0 <= contract.confidence_score <= 1.0:
            raise ValueError("confidence_score must be between 0.0 and 1.0")
        if contract.confidence_status is ConfidenceStatus.CONFIDENCE_NOT_AVAILABLE:
            raise ValueError("confidence_score cannot exist when confidence is unavailable")

    if contract.evidence_completeness_level is EvidenceCompletenessLevel.FRAMEWORK_ONLY:
        if contract.paper_trading_eligibility is not PaperTradingEligibility.BLOCKED:
            raise ValueError("framework_only requires paper_trading_eligibility blocked")
        if contract.confidence_status is not ConfidenceStatus.CONFIDENCE_NOT_AVAILABLE:
            raise ValueError("framework_only requires confidence_not_available")
        _require_forbidden_usage(
            contract.forbidden_downstream_usage,
            (
                ForbiddenDownstreamUsage.PAPER_TRADING,
                ForbiddenDownstreamUsage.LIVE_TRADING,
                ForbiddenDownstreamUsage.CAPITAL_ALLOCATION,
                ForbiddenDownstreamUsage.PERFORMANCE_CLAIMS,
            ),
        )

    if contract.oos_validation_status is OOSValidationStatus.OOS_PASSED:
        if contract.evidence_completeness_level not in {
            EvidenceCompletenessLevel.OOS_VALIDATED,
        }:
            raise ValueError("oos_passed requires oos_validated evidence completeness")
    if contract.simulation_status is SimulationStatus.BACKTEST_NOT_IMPLEMENTED:
        if contract.backtest_result_summary.get("status") != (
            SimulationStatus.BACKTEST_NOT_IMPLEMENTED.value
        ):
            raise ValueError("backtest_not_implemented requires matching result summary status")
    if contract.simulation_status in {
        SimulationStatus.BACKTEST_NOT_IMPLEMENTED,
        SimulationStatus.BACKTEST_NOT_EXECUTED,
    } and contract.performance_metrics_status == AvailabilityStatus.METRICS_AVAILABLE.value:
        raise ValueError("metrics cannot be available without implemented/executed backtest")
    if (
        contract.temporal_admissibility_status
        == AvailabilityStatus.TEMPORAL_ADMISSIBILITY_NOT_CERTIFIED.value
        and contract.simulation_status is SimulationStatus.SIMULATION_EXECUTED
    ):
        raise ValueError("simulation cannot execute without temporal certification")
    if (
        contract.strategy_handoff_status == AvailabilityStatus.DOSSIER_MOCK_ONLY.value
        and contract.approval_status is ApprovalStatus.APPROVED_FOR_RESEARCH_ONLY
    ):
        raise ValueError("dossier_mock_only cannot be approved_for_research_only")
    if contract.robustness_status is RobustnessStatus.ROBUSTNESS_NOT_AVAILABLE:
        if "block_or_require_review" not in contract.risk_engine_required_action:
            raise ValueError("robustness_not_available requires block_or_require_review action")
    if contract.paper_trading_eligibility is PaperTradingEligibility.BLOCKED:
        if (
            AllowedDownstreamUsage.PAPER_TRADING_WITH_FULL_EVIDENCE
            in contract.allowed_downstream_usage
        ):
            raise ValueError("blocked paper trading forbids paper_trading_with_full_evidence")
    if contract.evidence_completeness_level in {
        EvidenceCompletenessLevel.FRAMEWORK_ONLY,
        EvidenceCompletenessLevel.PARTIAL_EMPIRICAL,
    }:
        _require_forbidden_usage(
            contract.forbidden_downstream_usage,
            (
                ForbiddenDownstreamUsage.PAPER_TRADING,
                ForbiddenDownstreamUsage.LIVE_TRADING,
                ForbiddenDownstreamUsage.CAPITAL_ALLOCATION,
            ),
        )

    return contract


def create_framework_only_motor_b_output_contract(
    *,
    motor_b_output_id: str = "motor-b-framework-only-001",
    generated_at: datetime | None = None,
) -> MotorBOutputContract:
    """Create the current governance-blocked framework-only contract."""

    contract = MotorBOutputContract(
        motor_b_output_id=motor_b_output_id,
        schema_version="1.0.0",
        generated_at=generated_at or datetime.now(timezone.utc),
        owner_stage="06 Backtesting Engine",
        downstream_consumer_stage=(
            "07 Signal Fusion + LLM Motors",
            "08 Risk Engine",
        ),
        source_stage_references=(
            "04 Research Layer",
            "05 Strategy Engine",
            "06 Backtesting Engine",
        ),
        strategy_dossier_id=None,
        strategy_handoff_status=AvailabilityStatus.DOSSIER_NOT_AVAILABLE.value,
        candidate_id=None,
        candidate_status=AvailabilityStatus.CANDIDATE_NOT_AVAILABLE.value,
        regime_context=None,
        regime_context_status=AvailabilityStatus.REGIME_CONTEXT_NOT_AVAILABLE.value,
        research_execution_status=AvailabilityStatus.RESEARCH_NOT_EXECUTED.value,
        backtest_eligibility_status=BacktestEligibilityStatus.NOT_EVALUATED,
        temporal_admissibility_status=(
            AvailabilityStatus.TEMPORAL_ADMISSIBILITY_NOT_CERTIFIED.value
        ),
        historical_snapshot_status=(
            HistoricalSnapshotStatus.HISTORICAL_SNAPSHOT_NOT_BOUND
        ),
        simulation_status=SimulationStatus.BACKTEST_NOT_IMPLEMENTED,
        execution_friction_status=(
            ExecutionFrictionStatus.EXECUTION_FRICTION_NOT_AVAILABLE
        ),
        performance_metrics_status=AvailabilityStatus.METRICS_NOT_AVAILABLE.value,
        backtest_result_summary={
            "status": SimulationStatus.BACKTEST_NOT_IMPLEMENTED.value,
        },
        oos_validation_status=OOSValidationStatus.OOS_NOT_AVAILABLE,
        oos_validation_report=None,
        walk_forward_status=AvailabilityStatus.WALK_FORWARD_NOT_AVAILABLE.value,
        walk_forward_summary=None,
        robustness_status=RobustnessStatus.ROBUSTNESS_NOT_AVAILABLE,
        overfitting_status=OverfittingStatus.OVERFITTING_NOT_EVALUATED,
        falsification_status=AvailabilityStatus.FALSIFICATION_NOT_EXECUTED.value,
        confidence_status=ConfidenceStatus.CONFIDENCE_NOT_AVAILABLE,
        confidence_score=None,
        approval_status=ApprovalStatus.NOT_APPROVED,
        non_approval_statement=(
            "This contract is framework-only and blocks paper trading, live trading, "
            "capital allocation, confidence generation, and performance claims."
        ),
        risk_engine_required_action=("block_or_require_review",),
        paper_trading_eligibility=PaperTradingEligibility.BLOCKED,
        evidence_completeness_level=EvidenceCompletenessLevel.FRAMEWORK_ONLY,
        missing_evidence=(
            "research_not_executed",
            "research_output_not_persisted",
            "dossier_not_available",
            "backtest_not_implemented",
            "oos_not_available",
            "walk_forward_not_available",
            "robustness_not_available",
            "confidence_not_available",
        ),
        blocking_gaps=(
            "empirical_results_unavailable",
            "paper_trading_blocked",
            "stage_09_blocked",
        ),
        allowed_downstream_usage=(
            AllowedDownstreamUsage.DESIGN_REFERENCE_ONLY,
            AllowedDownstreamUsage.DOCUMENTATION_REVIEW,
            AllowedDownstreamUsage.CONTRACT_VALIDATION,
            AllowedDownstreamUsage.SIMULATION_WITH_MOCK_INPUTS_ONLY,
            AllowedDownstreamUsage.SIGNAL_FUSION_DRY_RUN,
            AllowedDownstreamUsage.OFFLINE_RESEARCH,
            AllowedDownstreamUsage.HUMAN_REVIEW,
        ),
        forbidden_downstream_usage=(
            ForbiddenDownstreamUsage.PAPER_TRADING,
            ForbiddenDownstreamUsage.PAPER_TRADING_WITHOUT_OOS,
            ForbiddenDownstreamUsage.LIVE_TRADING,
            ForbiddenDownstreamUsage.CAPITAL_ALLOCATION,
            ForbiddenDownstreamUsage.AUTONOMOUS_EXECUTION,
            ForbiddenDownstreamUsage.PRODUCTION_SIGNAL_ROUTING,
            ForbiddenDownstreamUsage.RISK_LIMIT_RELAXATION,
            ForbiddenDownstreamUsage.RISK_BYPASS,
            ForbiddenDownstreamUsage.CONFIDENCE_GENERATION,
            ForbiddenDownstreamUsage.STRATEGY_PROMOTION,
            ForbiddenDownstreamUsage.EXECUTION_SIGNAL_GENERATION,
            ForbiddenDownstreamUsage.PERFORMANCE_CLAIMS,
        ),
        audit_references=(
            "06 Backtesting Engine/docs/18_motor_b_output_contract.md",
            "04 Research Layer/docs/11_research_closure.md",
            "05 Strategy Engine/docs/35_strategy_engine_framework_closure.md",
        ),
        schema_validation_status=SchemaValidationStatus.SCHEMA_VALID_GOVERNANCE_BLOCKED,
        contract_generation_mode=(
            ContractGenerationMode.CONTRACT_GENERATED_FROM_DOCUMENTATION
        ),
        human_review_status=HumanReviewStatus.HUMAN_REVIEW_NOT_REQUESTED,
    )
    return validate_motor_b_output_contract(contract)


def _require_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_semver(value: object, field_name: str) -> str:
    text = _require_text(value, field_name)
    if not SEMVER_PATTERN.fullmatch(text):
        raise ValueError(f"{field_name} must follow SemVer MAJOR.MINOR.PATCH")
    return text


def _require_non_empty_sequence(values: Sequence[str], field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be a sequence")
    normalized = tuple(_require_text(value, field_name) for value in values)
    if not normalized:
        raise ValueError(f"{field_name} must contain at least one item")
    return normalized


def _require_enum(value: object, enum_type: type[Enum], field_name: str) -> None:
    if not isinstance(value, enum_type):
        raise ValueError(
            f"{field_name} must be a controlled {enum_type.__name__} value"
        )


def _require_forbidden_usage(
    actual: Sequence[ForbiddenDownstreamUsage],
    required: Sequence[ForbiddenDownstreamUsage],
) -> None:
    missing = [usage.value for usage in required if usage not in actual]
    if missing:
        raise ValueError(f"missing forbidden_downstream_usage values: {missing}")
