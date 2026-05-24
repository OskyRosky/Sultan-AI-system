"""Conceptual strategy candidate composition for 05 Strategy Engine.

Strategy candidates here compose valid declarative rule definitions. They are
not validated strategies, registry records, risk-managed systems, backtests, or
execution-ready artifacts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Sequence

from rules.rule_definition import RuleDefinition, validate_rule_definition


class CandidateStatus(str, Enum):
    """Pre-registry composition status values."""

    DRAFT = "draft"
    COMPOSED = "composed"
    PENDING_RISK_TEMPLATE = "pending_risk_template"


@dataclass(frozen=True)
class StrategyCandidate:
    """Auditable conceptual strategy candidate composition."""

    candidate_id: str
    rule_definitions: tuple[RuleDefinition, ...]
    composition_summary: str
    composition_rationale: str
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    conflict_notes: tuple[str, ...]
    falsification_references: tuple[str, ...]
    audit_reference: str
    status: CandidateStatus
    created_at: datetime


def create_strategy_candidate(
    *,
    candidate_id: str,
    rule_definitions: Sequence[RuleDefinition],
    composition_summary: str,
    composition_rationale: str,
    assumptions: Sequence[str],
    limitations: Sequence[str],
    falsification_references: Sequence[str],
    audit_reference: str,
    conflict_notes: Sequence[str] = (),
    status: CandidateStatus = CandidateStatus.PENDING_RISK_TEMPLATE,
    created_at: datetime | None = None,
) -> StrategyCandidate:
    """Create and validate one conceptual strategy candidate."""

    if not isinstance(status, CandidateStatus):
        raise TypeError("status must be a CandidateStatus")

    candidate = StrategyCandidate(
        candidate_id=_require_text(candidate_id, "candidate_id"),
        rule_definitions=tuple(rule_definitions),
        composition_summary=_require_text(composition_summary, "composition_summary"),
        composition_rationale=_require_text(composition_rationale, "composition_rationale"),
        assumptions=_normalize_text_sequence(assumptions, "assumptions"),
        limitations=_normalize_text_sequence(limitations, "limitations"),
        conflict_notes=_normalize_optional_text_sequence(conflict_notes, "conflict_notes"),
        falsification_references=_normalize_text_sequence(
            falsification_references,
            "falsification_references",
        ),
        audit_reference=_require_text(audit_reference, "audit_reference"),
        status=status,
        created_at=created_at or datetime.now(timezone.utc),
    )
    return validate_strategy_candidate(candidate)


def validate_strategy_candidate(candidate: StrategyCandidate) -> StrategyCandidate:
    """Validate rule origins, composition status, and governance fields."""

    if not candidate.rule_definitions:
        raise ValueError("strategy candidate must contain at least one rule definition")

    for rule in candidate.rule_definitions:
        if not isinstance(rule, RuleDefinition):
            raise ValueError("strategy candidate rules must be RuleDefinition instances")
        validate_rule_definition(rule)

    if not isinstance(candidate.status, CandidateStatus):
        raise TypeError("status must be a CandidateStatus")
    if candidate.status is not CandidateStatus.PENDING_RISK_TEMPLATE:
        raise ValueError("Block 06 candidates must remain pending_risk_template")

    _require_text(candidate.candidate_id, "candidate_id")
    _require_text(candidate.composition_summary, "composition_summary")
    _require_text(candidate.composition_rationale, "composition_rationale")
    _require_text(candidate.audit_reference, "audit_reference")
    _normalize_text_sequence(candidate.assumptions, "assumptions")
    _normalize_text_sequence(candidate.limitations, "limitations")
    _normalize_optional_text_sequence(candidate.conflict_notes, "conflict_notes")
    _normalize_text_sequence(candidate.falsification_references, "falsification_references")

    return candidate


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


def _normalize_optional_text_sequence(values: Sequence[str], field_name: str) -> tuple[str, ...]:
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
    return tuple(normalized)
