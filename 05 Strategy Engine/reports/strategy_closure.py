"""Conceptual Strategy Closure records for 05 Strategy Engine.

Strategy Closure records confirm that a conceptual strategy package completed
05 governance checks. They do not create a dossier, authorize backtesting,
validate edge, calculate performance, or approve trading.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Sequence

from quality.quality_gates import (
    QualityAssessmentStatus,
    StrategyQualityGateAssessment,
    validate_quality_gate_assessment,
)


class StrategyClosureStatus(str, Enum):
    """Internal closure status for Block 10."""

    CLOSED_PENDING_DOSSIER_HANDOFF = "closed_pending_dossier_handoff"


@dataclass(frozen=True)
class StrategyClosureRecord:
    """Immutable internal closure record for one quality-assessed package."""

    closure_id: str
    quality_assessment: StrategyQualityGateAssessment
    closure_status: StrategyClosureStatus
    candidate_id: str
    registry_entry_id: str
    quality_assessment_id: str
    source_hypothesis_ids: tuple[str, ...]
    signal_ids: tuple[str, ...]
    regime_frame_ids: tuple[str, ...]
    rule_ids: tuple[str, ...]
    upstream_falsification_references: tuple[str, ...]
    closure_summary: str
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    non_approval_statement: str
    audit_reference: str
    closed_at: datetime


def create_strategy_closure_record(
    *,
    closure_id: str,
    quality_assessment: StrategyQualityGateAssessment,
    closure_summary: str,
    assumptions: Sequence[str],
    limitations: Sequence[str],
    non_approval_statement: str,
    audit_reference: str,
    closure_status: StrategyClosureStatus = StrategyClosureStatus.CLOSED_PENDING_DOSSIER_HANDOFF,
    closed_at: datetime | None = None,
) -> StrategyClosureRecord:
    """Create and validate one immutable Strategy Closure record."""

    if not isinstance(closure_status, StrategyClosureStatus):
        raise TypeError("closure_status must be a StrategyClosureStatus")
    if not isinstance(quality_assessment, StrategyQualityGateAssessment):
        raise ValueError("strategy closure must reference a valid quality assessment")

    registry_entry = quality_assessment.registry_entry
    candidate = registry_entry.strategy_candidate

    record = StrategyClosureRecord(
        closure_id=_require_text(closure_id, "closure_id"),
        quality_assessment=quality_assessment,
        closure_status=closure_status,
        candidate_id=candidate.candidate_id,
        registry_entry_id=registry_entry.entry_id,
        quality_assessment_id=quality_assessment.assessment_id,
        source_hypothesis_ids=registry_entry.source_hypothesis_ids,
        signal_ids=registry_entry.signal_ids,
        regime_frame_ids=registry_entry.regime_frame_ids,
        rule_ids=registry_entry.rule_ids,
        upstream_falsification_references=_upstream_falsification_references(
            quality_assessment,
        ),
        closure_summary=_require_text(closure_summary, "closure_summary"),
        assumptions=_normalize_text_sequence(assumptions, "assumptions"),
        limitations=_normalize_text_sequence(limitations, "limitations"),
        non_approval_statement=_require_text(
            non_approval_statement,
            "non_approval_statement",
        ),
        audit_reference=_require_text(audit_reference, "audit_reference"),
        closed_at=closed_at or datetime.now(timezone.utc),
    )
    return validate_strategy_closure_record(record)


def validate_strategy_closure_record(record: StrategyClosureRecord) -> StrategyClosureRecord:
    """Validate quality-assessment origin, closure status, and traceability."""

    if not isinstance(record.quality_assessment, StrategyQualityGateAssessment):
        raise ValueError("strategy closure must reference a valid quality assessment")
    validate_quality_gate_assessment(record.quality_assessment)

    if (
        record.quality_assessment.assessment_status
        is not QualityAssessmentStatus.PASSED_PENDING_STRATEGY_CLOSURE
    ):
        raise ValueError("quality assessment must be passed_pending_strategy_closure")

    if not isinstance(record.closure_status, StrategyClosureStatus):
        raise TypeError("closure_status must be a StrategyClosureStatus")
    if record.closure_status is not StrategyClosureStatus.CLOSED_PENDING_DOSSIER_HANDOFF:
        raise ValueError("strategy closure must remain closed_pending_dossier_handoff")

    registry_entry = record.quality_assessment.registry_entry
    candidate = registry_entry.strategy_candidate

    if record.candidate_id != candidate.candidate_id:
        raise ValueError("candidate_id must match the quality assessment registry entry")
    if record.registry_entry_id != registry_entry.entry_id:
        raise ValueError("registry_entry_id must match the quality assessment registry entry")
    if record.quality_assessment_id != record.quality_assessment.assessment_id:
        raise ValueError("quality_assessment_id must match the quality assessment")
    if record.source_hypothesis_ids != registry_entry.source_hypothesis_ids:
        raise ValueError("source_hypothesis_ids must match the registry entry")
    if record.signal_ids != registry_entry.signal_ids:
        raise ValueError("signal_ids must match the registry entry")
    if record.regime_frame_ids != registry_entry.regime_frame_ids:
        raise ValueError("regime_frame_ids must match the registry entry")
    if record.rule_ids != registry_entry.rule_ids:
        raise ValueError("rule_ids must match the registry entry")

    _require_text(record.closure_id, "closure_id")
    _require_text(record.closure_summary, "closure_summary")
    _normalize_text_sequence(record.assumptions, "assumptions")
    _normalize_text_sequence(record.limitations, "limitations")
    _normalize_text_sequence(
        record.upstream_falsification_references,
        "upstream_falsification_references",
    )
    _require_text(record.non_approval_statement, "non_approval_statement")
    _require_text(record.audit_reference, "audit_reference")

    return record


def _upstream_falsification_references(
    quality_assessment: StrategyQualityGateAssessment,
) -> tuple[str, ...]:
    registry_entry = quality_assessment.registry_entry
    values = (
        *registry_entry.falsification_references,
        *registry_entry.strategy_candidate.falsification_references,
        *registry_entry.risk_template.falsification_references,
    )
    return tuple(dict.fromkeys(values))


def _require_text(value: object, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _normalize_text_sequence(values: Sequence[str], field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError(f"{field_name} must be a sequence of strings")
    normalized: list[str] = []
    for value in values:
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must contain only strings")
        stripped = value.strip()
        if not stripped:
            raise ValueError(f"{field_name} must not contain empty strings")
        normalized.append(stripped)
    if not normalized:
        raise ValueError(f"{field_name} must contain at least one item")
    return tuple(normalized)

