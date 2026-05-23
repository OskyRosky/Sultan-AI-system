"""Governed input contract for 05 Strategy Engine.

The module represents admissible 04 Research Layer inputs and makes an explicit
eligibility decision for later conceptual strategy design. It is intentionally
small, in-memory, and free of trading, backtesting, PnL, and data integration
logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Protocol


class ApprovalStatus(str, Enum):
    """Research governance approval state."""

    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    CLOSED = "closed"


class EligibilityStatus(str, Enum):
    """Strategy design eligibility state."""

    INELIGIBLE_FOR_STRATEGY_DESIGN = "ineligible_for_strategy_design"
    ELIGIBLE_FOR_STRATEGY_DESIGN = "eligible_for_strategy_design"


class InputType(str, Enum):
    """Accepted conceptual input classes from 04 Research Layer."""

    RESEARCH_EVIDENCE = "research_evidence"
    FINDING = "finding"
    HYPOTHESIS = "hypothesis"


@dataclass(frozen=True)
class ResearchEvidenceInput:
    """Governed evidence metadata from 04 Research Layer.

    Evidence is context only. Evidence alone is never eligible for strategy
    design.
    """

    evidence_id: str
    source_layer: str
    source_component: str
    evidence_type: str
    feature_reference: str
    target_reference: str | None
    regime_reference: str | None
    temporal_scope: str
    asset_scope: str
    timeframe_scope: str
    evidence_status: str
    approval_status: ApprovalStatus
    created_at: datetime
    limitations: tuple[str, ...]
    audit_reference: str


@dataclass(frozen=True)
class FindingInput:
    """Governed finding metadata from 04 Research Layer."""

    finding_id: str
    linked_evidence_ids: tuple[str, ...]
    finding_summary: str
    finding_type: str
    regime_scope: str | None
    stability_assessment: str
    informativeness_assessment: str
    falsification_reference: str | None
    finding_status: str
    approval_status: ApprovalStatus
    closure_reference: str
    audit_reference: str
    limitations: tuple[str, ...]


@dataclass(frozen=True)
class HypothesisInput:
    """Governed hypothesis metadata from 04 Research Layer."""

    hypothesis_id: str
    linked_finding_ids: tuple[str, ...]
    linked_evidence_ids: tuple[str, ...]
    hypothesis_statement: str
    expected_behavior: str
    applicable_regime_context: str | None
    falsification_criteria: tuple[str, ...]
    limitations: tuple[str, ...]
    approval_status: ApprovalStatus
    eligible_for_strategy_design: bool
    audit_reference: str


class StrategyInput(Protocol):
    """Shared fields required for eligibility evaluation."""

    approval_status: ApprovalStatus
    limitations: tuple[str, ...]
    audit_reference: str


@dataclass(frozen=True)
class StrategyInputEligibilityDecision:
    """Explicit eligibility decision for future 05 conceptual design."""

    input_id: str
    input_type: InputType
    eligibility_status: EligibilityStatus
    decision_reason: str
    required_approvals_present: bool
    falsification_criteria_present: bool | None
    traceability_complete: bool
    limitations_acknowledged: bool
    decided_at: datetime
    audit_reference: str


def decide_strategy_input_eligibility(
    strategy_input: ResearchEvidenceInput | FindingInput | HypothesisInput,
    *,
    decided_at: datetime | None = None,
) -> StrategyInputEligibilityDecision:
    """Return an auditable eligibility decision for one governed input."""

    input_type = _input_type(strategy_input)
    input_id = _input_id(strategy_input)
    required_approvals_present = strategy_input.approval_status is ApprovalStatus.APPROVED
    traceability_complete = _traceability_complete(strategy_input)
    limitations_acknowledged = bool(strategy_input.limitations)
    falsification_criteria_present = _falsification_criteria_present(strategy_input)
    audit_reference_present = bool(strategy_input.audit_reference.strip())

    failures: list[str] = []
    if not audit_reference_present:
        failures.append("missing audit reference")
    if not required_approvals_present:
        failures.append("approval status is not approved")
    if not traceability_complete:
        failures.append("traceability is incomplete")
    if not limitations_acknowledged:
        failures.append("limitations are missing")
    if input_type is InputType.RESEARCH_EVIDENCE:
        failures.append("evidence alone cannot feed strategy design")
    if input_type is InputType.HYPOTHESIS and not falsification_criteria_present:
        failures.append("hypothesis falsification criteria are missing")
    if input_type is InputType.HYPOTHESIS and not strategy_input.eligible_for_strategy_design:
        failures.append("hypothesis is not marked eligible by source governance")

    eligibility_status = (
        EligibilityStatus.ELIGIBLE_FOR_STRATEGY_DESIGN
        if not failures
        else EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    )
    reason = "eligible for conceptual strategy design only" if not failures else "; ".join(failures)

    return StrategyInputEligibilityDecision(
        input_id=input_id,
        input_type=input_type,
        eligibility_status=eligibility_status,
        decision_reason=reason,
        required_approvals_present=required_approvals_present,
        falsification_criteria_present=falsification_criteria_present,
        traceability_complete=traceability_complete,
        limitations_acknowledged=limitations_acknowledged,
        decided_at=decided_at or datetime.now(timezone.utc),
        audit_reference=strategy_input.audit_reference,
    )


def _input_type(
    strategy_input: ResearchEvidenceInput | FindingInput | HypothesisInput,
) -> InputType:
    if isinstance(strategy_input, ResearchEvidenceInput):
        return InputType.RESEARCH_EVIDENCE
    if isinstance(strategy_input, FindingInput):
        return InputType.FINDING
    if isinstance(strategy_input, HypothesisInput):
        return InputType.HYPOTHESIS
    raise TypeError("unsupported strategy input type")


def _input_id(strategy_input: ResearchEvidenceInput | FindingInput | HypothesisInput) -> str:
    if isinstance(strategy_input, ResearchEvidenceInput):
        return strategy_input.evidence_id
    if isinstance(strategy_input, FindingInput):
        return strategy_input.finding_id
    return strategy_input.hypothesis_id


def _traceability_complete(
    strategy_input: ResearchEvidenceInput | FindingInput | HypothesisInput,
) -> bool:
    if isinstance(strategy_input, ResearchEvidenceInput):
        return all(
            (
                strategy_input.source_layer == "04 Research Layer",
                bool(strategy_input.source_component.strip()),
                bool(strategy_input.evidence_id.strip()),
                bool(strategy_input.feature_reference.strip()),
                bool(strategy_input.temporal_scope.strip()),
                bool(strategy_input.asset_scope.strip()),
                bool(strategy_input.timeframe_scope.strip()),
            )
        )
    if isinstance(strategy_input, FindingInput):
        return all(
            (
                bool(strategy_input.finding_id.strip()),
                bool(strategy_input.linked_evidence_ids),
                bool(strategy_input.closure_reference.strip()),
                bool(strategy_input.audit_reference.strip()),
            )
        )
    return all(
        (
            bool(strategy_input.hypothesis_id.strip()),
            bool(strategy_input.linked_evidence_ids),
            bool(strategy_input.audit_reference.strip()),
        )
    )


def _falsification_criteria_present(
    strategy_input: ResearchEvidenceInput | FindingInput | HypothesisInput,
) -> bool | None:
    if isinstance(strategy_input, HypothesisInput):
        return bool(strategy_input.falsification_criteria)
    if isinstance(strategy_input, FindingInput):
        return bool(strategy_input.falsification_reference or strategy_input.limitations)
    return None
