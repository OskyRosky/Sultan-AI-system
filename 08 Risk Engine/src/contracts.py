from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


DRY_RUN_TIMESTAMP = "2026-06-22T00:00:00Z"
STAGE07_ID = "07 Signal Fusion + LLM Motors"
STAGE08_ID = "08 Risk Engine"
RISK_HANDOFF_ARTIFACT_TYPE = "RiskHandoffPackage"

RISK_DECISION_STATUS = "blocked"
OPERATIONAL_STATUS = "non_operational"
HANDOFF_TO_09 = "blocked"
DOWNSTREAM_OPERATIONAL_ELIGIBILITY = "blocked"
STAGE_09_OPERATIONAL_START_ALLOWED = False
PAPER_TRADING_READY = False
RISK_APPROVAL = False
CAPITAL_ALLOCATION_READY = False
LIVE_TRADING_READY = False

DEFAULT_REASON_CODES = (
    "framework_only_input",
    "confidence_not_available",
    "empirical_evidence_not_available",
    "strategy_not_promoted",
    "paper_trading_blocked",
    "v1_dry_run_only",
)

NON_APPROVAL_STATEMENT = (
    "Stage 08 minimal dry-run is V1 contract validation only: not real risk "
    "approval, not paper trading readiness, not capital allocation approval, "
    "not live trading approval, and not Stage 09 readiness."
)


@dataclass(frozen=True)
class SerializableContract:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Stage08InputPackage(SerializableContract):
    stage08_input_package_id: str
    source_stage: str
    artifact_type: str
    source_risk_handoff_package_id: str
    intake_status: str
    target_stage: str
    risk_handoff_status: str
    evidence_completeness_level: str
    empirical_results_available: bool
    confidence_status: str
    confidence_score: float | None
    final_signal_confidence_score: float | None
    paper_trading_ready: bool
    handoff_to_09: str
    downstream_operational_eligibility: str
    strategy_promotion_status: str
    blocking_gaps: tuple[str, ...]
    forbidden_downstream_usage: tuple[str, ...]
    non_approval_statement: str


@dataclass(frozen=True)
class Stage08GateResult(SerializableContract):
    gate_name: str
    gate_status: str
    passed: bool
    reason_codes: tuple[str, ...]
    blocking_gaps: tuple[str, ...]
    preserved_restrictions: tuple[str, ...]


@dataclass(frozen=True)
class Stage08RiskDecision(SerializableContract):
    risk_decision_id: str
    related_stage08_input_package_id: str
    risk_decision_status: str
    operational_status: str
    risk_approval: bool
    paper_trading_ready: bool
    handoff_to_09: str
    downstream_operational_eligibility: str
    stage_09_operational_start_allowed: bool
    capital_allocation_ready: bool
    live_trading_ready: bool
    reason_codes: tuple[str, ...]
    blocking_gaps: tuple[str, ...]
    forbidden_downstream_usage: tuple[str, ...]
    non_approval_statement: str


@dataclass(frozen=True)
class Stage08AuditTrace(SerializableContract):
    audit_trace_id: str
    stage_id: str
    dry_run_timestamp: str
    source_artifacts: tuple[str, ...]
    artifact_hashes: tuple[str, ...]
    gate_names: tuple[str, ...]
    decision_hash: str
    blocking_gaps: tuple[str, ...]
    forbidden_downstream_usage: tuple[str, ...]
    non_approval_statement: str


@dataclass(frozen=True)
class Stage08DryRunResult(SerializableContract):
    input_package: Stage08InputPackage
    gate_results: tuple[Stage08GateResult, ...]
    risk_decision: Stage08RiskDecision
    audit_trace: Stage08AuditTrace
