from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


DRY_RUN_TIMESTAMP = "2026-06-21T00:00:00Z"
EVIDENCE_COMPLETENESS_LEVEL = "framework_only"
CONFIDENCE_STATUS = "confidence_not_available"
PAPER_TRADING_READY = False
HANDOFF_TO_09 = "blocked"
DOWNSTREAM_OPERATIONAL_ELIGIBILITY = "blocked"
STRATEGY_PROMOTION_STATUS = "not_promoted"
EMPIRICAL_RESULTS_AVAILABLE = False
FINAL_SIGNAL_CONFIDENCE_SCORE = None
CONFIDENCE_SCORE = None
NON_APPROVAL_STATEMENT = (
    "Stage 07 minimal dry-run is V1 contract validation only: not empirical "
    "evidence, not strategy validation, not confidence, not paper trading "
    "readiness, not production readiness, and not Stage 09 readiness."
)
FORBIDDEN_DOWNSTREAM_USAGE = (
    "paper_trading",
    "live_trading",
    "capital_allocation",
    "strategy_promotion",
    "confidence_generation",
    "evidence_claims",
    "production_signal_routing",
    "stage_09_unlock",
)
DEFAULT_BLOCKING_GAPS = (
    "missing_real_empirical_evidence",
    "oos_not_available",
    "walk_forward_not_available",
    "robustness_not_available",
    "confidence_not_available",
    "paper_trading_blocked",
)


@dataclass(frozen=True)
class SerializableContract:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MotorAContextMock(SerializableContract):
    regime_label: str
    regime_source: str
    uncertainty_level: str
    supported_assets: tuple[str, ...]
    supported_timeframes: tuple[str, ...]
    synthetic_status: str
    limitations: tuple[str, ...]


@dataclass(frozen=True)
class MotorBRawDiagnosticsInputForStage07(SerializableContract):
    motor_b_input_id: str
    source_stage: str
    source_artifact_type: str
    handoff_contract_id: str | None
    registry_record_id: str | None
    diagnostics_id: str | None
    simulation_id: str | None
    package_id: str | None
    strategy_id: str | None
    strategy_version: str | None
    snapshot_id: str | None
    output_scope: str | None
    diagnostics_scope: str | None
    registry_scope: str | None
    handoff_scope: str | None
    simulation_status: str | None
    trade_count: int | None
    ending_capital: float | None
    return_pct: float | None
    evidence_completeness_level: str
    empirical_results_available: bool
    confidence_status: str
    confidence_score: float | None
    final_signal_confidence_score: float | None
    paper_trading_ready: bool
    paper_trading_eligibility: str
    handoff_to_09: str
    downstream_operational_eligibility: str
    strategy_promotion_status: str
    adapter_status: str
    missing_evidence: tuple[str, ...]
    blocking_gaps: tuple[str, ...]
    forbidden_downstream_usage: tuple[str, ...]
    non_approval_statement: str
    audit_references: tuple[str, ...]


@dataclass(frozen=True)
class MotorCEventClassifierMock(SerializableContract):
    event_id: str
    event_type: str
    classification_status: str
    classification_confidence_status: str
    classification_confidence_score: float | None
    synthetic_status: str
    limitations: tuple[str, ...]


@dataclass(frozen=True)
class NormalizedMotorAInput(SerializableContract):
    normalized_input_id: str
    source_motor: str
    regime_label: str
    uncertainty_level: str
    synthetic_status: str
    normalization_status: str
    blocking_gaps: tuple[str, ...]


@dataclass(frozen=True)
class NormalizedMotorBInput(SerializableContract):
    normalized_input_id: str
    source_motor: str
    source_artifact_type: str
    source_artifact_id: str | None
    strategy_id: str | None
    evidence_completeness_level: str
    empirical_results_available: bool
    confidence_status: str
    confidence_score: float | None
    paper_trading_ready: bool
    handoff_to_09: str
    downstream_operational_eligibility: str
    strategy_promotion_status: str
    normalization_status: str
    blocking_gaps: tuple[str, ...]
    forbidden_downstream_usage: tuple[str, ...]
    non_approval_statement: str


@dataclass(frozen=True)
class NormalizedMotorCInput(SerializableContract):
    normalized_input_id: str
    source_motor: str
    event_id: str
    event_type: str
    classification_confidence_status: str
    classification_confidence_score: float | None
    synthetic_status: str
    normalization_status: str
    blocking_gaps: tuple[str, ...]


@dataclass(frozen=True)
class NormalizedSignalCandidate(SerializableContract):
    normalized_signal_candidate_id: str
    source_motor: str
    source_input_id: str
    signal_direction: str
    signal_scope: str
    evidence_completeness_level: str
    empirical_results_available: bool
    confidence_status: str
    confidence_score: float | None
    paper_trading_ready: bool
    handoff_to_09: str
    downstream_operational_eligibility: str
    strategy_promotion_status: str
    normalization_status: str
    blocking_gaps: tuple[str, ...]
    forbidden_downstream_usage: tuple[str, ...]
    non_approval_statement: str


@dataclass(frozen=True)
class FusedSignalCandidate(SerializableContract):
    fused_signal_candidate_id: str
    input_candidate_ids: tuple[str, ...]
    signal_scope: str
    fused_direction: str
    operational_status: str
    evidence_completeness_level: str
    empirical_results_available: bool
    promotion_status: str
    paper_trading_ready: bool
    handoff_to_09: str
    downstream_operational_eligibility: str
    blocking_gaps: tuple[str, ...]
    forbidden_downstream_usage: tuple[str, ...]
    non_approval_statement: str


@dataclass(frozen=True)
class ConfidenceGovernanceResult(SerializableContract):
    confidence_governance_result_id: str
    related_fused_signal_candidate_id: str
    evidence_completeness_level: str
    empirical_results_available: bool
    confidence_status: str
    confidence_score: float | None
    final_signal_confidence_score: float | None
    confidence_reason: str
    paper_trading_ready: bool
    handoff_to_09: str
    strategy_promotion_status: str
    blocking_gaps: tuple[str, ...]
    non_approval_statement: str


@dataclass(frozen=True)
class RiskHandoffPackage(SerializableContract):
    risk_handoff_package_id: str
    target_stage: str
    related_fused_signal_candidate_id: str
    related_confidence_governance_result_id: str
    risk_handoff_status: str
    paper_trading_ready: bool
    handoff_to_09: str
    downstream_operational_eligibility: str
    strategy_promotion_status: str
    evidence_completeness_level: str
    empirical_results_available: bool
    confidence_status: str
    confidence_score: float | None
    final_signal_confidence_score: float | None
    blocking_gaps: tuple[str, ...]
    forbidden_downstream_usage: tuple[str, ...]
    non_approval_statement: str


@dataclass(frozen=True)
class Stage07AuditTrace(SerializableContract):
    audit_trace_id: str
    stage_id: str
    dry_run_timestamp: str
    source_artifacts: tuple[str, ...]
    artifact_hashes: tuple[str, ...]
    blocking_gaps: tuple[str, ...]
    forbidden_downstream_usage: tuple[str, ...]
    non_approval_statement: str


@dataclass(frozen=True)
class Stage07DryRunResult(SerializableContract):
    normalized_motor_a_input: NormalizedMotorAInput
    normalized_motor_b_input: NormalizedMotorBInput
    normalized_motor_c_input: NormalizedMotorCInput
    normalized_signal_candidates: tuple[NormalizedSignalCandidate, ...]
    fused_signal_candidate: FusedSignalCandidate
    confidence_governance_result: ConfidenceGovernanceResult
    risk_handoff_package: RiskHandoffPackage
    audit_trace: Stage07AuditTrace
