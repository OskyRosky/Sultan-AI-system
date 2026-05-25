"""Conceptual Strategy Dossier & Handoff preparation for 05 Strategy Engine.

Strategy dossiers package closed conceptual strategy artifacts for future
review. They do not execute handoff, authorize backtesting, validate edge,
calculate performance, or approve trading.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Iterable, Sequence

from reports.strategy_closure import (
    StrategyClosureRecord,
    StrategyClosureStatus,
    validate_strategy_closure_record,
)


class DossierSectionType(str, Enum):
    """Required conceptual dossier sections for Block 11."""

    CANDIDATE_IDENTITY = "candidate_identity"
    SOURCE_TRACEABILITY = "source_traceability"
    SIGNAL_REGIME_RULE_SUMMARY = "signal_regime_rule_summary"
    RISK_TEMPLATE_SUMMARY = "risk_template_summary"
    QUALITY_AND_CLOSURE_SUMMARY = "quality_and_closure_summary"
    FALSIFICATION_REFERENCES = "falsification_references"
    ASSUMPTIONS_AND_LIMITATIONS = "assumptions_and_limitations"
    DOWNSTREAM_REVIEW_QUESTIONS = "downstream_review_questions"
    NON_APPROVAL_SCOPE = "non_approval_scope"


class DossierHandoffStatus(str, Enum):
    """Documentation handoff preparation state for Block 11."""

    DOSSIER_PREPARED_PENDING_FINAL_AUDIT = "dossier_prepared_pending_final_audit"


REQUIRED_DOSSIER_SECTION_TYPES: frozenset[DossierSectionType] = frozenset(
    DossierSectionType,
)


@dataclass(frozen=True)
class DossierSection:
    """One immutable conceptual dossier section."""

    section_id: str
    section_type: DossierSectionType
    title: str
    content_summary: str
    audit_reference: str


@dataclass(frozen=True)
class StrategyDossier:
    """Immutable conceptual dossier prepared from one closure record."""

    dossier_id: str
    closure_record: StrategyClosureRecord
    handoff_status: DossierHandoffStatus
    candidate_id: str
    closure_id: str
    quality_assessment_id: str
    registry_entry_id: str
    source_hypothesis_ids: tuple[str, ...]
    signal_ids: tuple[str, ...]
    regime_frame_ids: tuple[str, ...]
    rule_ids: tuple[str, ...]
    upstream_falsification_references: tuple[str, ...]
    sections: tuple[DossierSection, ...]
    downstream_review_questions: tuple[str, ...]
    pending_requirements: tuple[str, ...]
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    non_approval_statement: str
    audit_reference: str
    prepared_at: datetime


def create_dossier_section(
    *,
    section_id: str,
    section_type: DossierSectionType,
    title: str,
    content_summary: str,
    audit_reference: str,
) -> DossierSection:
    """Create and validate one dossier section."""

    if not isinstance(section_type, DossierSectionType):
        raise TypeError("section_type must be a DossierSectionType")

    section = DossierSection(
        section_id=_require_text(section_id, "section_id"),
        section_type=section_type,
        title=_require_text(title, "title"),
        content_summary=_require_text(content_summary, "content_summary"),
        audit_reference=_require_text(audit_reference, "audit_reference"),
    )
    return validate_dossier_section(section)


def validate_dossier_section(section: DossierSection) -> DossierSection:
    """Validate one dossier section."""

    if not isinstance(section.section_type, DossierSectionType):
        raise TypeError("section_type must be a DossierSectionType")

    _require_text(section.section_id, "section_id")
    _require_text(section.title, "title")
    _require_text(section.content_summary, "content_summary")
    _require_text(section.audit_reference, "audit_reference")

    return section


def create_strategy_dossier(
    *,
    dossier_id: str,
    closure_record: StrategyClosureRecord,
    sections: Sequence[DossierSection],
    downstream_review_questions: Sequence[str],
    pending_requirements: Sequence[str],
    assumptions: Sequence[str],
    limitations: Sequence[str],
    non_approval_statement: str,
    audit_reference: str,
    handoff_status: DossierHandoffStatus = (
        DossierHandoffStatus.DOSSIER_PREPARED_PENDING_FINAL_AUDIT
    ),
    prepared_at: datetime | None = None,
) -> StrategyDossier:
    """Create and validate one immutable Strategy Dossier."""

    if not isinstance(handoff_status, DossierHandoffStatus):
        raise TypeError("handoff_status must be a DossierHandoffStatus")
    if not isinstance(closure_record, StrategyClosureRecord):
        raise ValueError("strategy dossier must reference a valid closure record")

    dossier = StrategyDossier(
        dossier_id=_require_text(dossier_id, "dossier_id"),
        closure_record=closure_record,
        handoff_status=handoff_status,
        candidate_id=closure_record.candidate_id,
        closure_id=closure_record.closure_id,
        quality_assessment_id=closure_record.quality_assessment_id,
        registry_entry_id=closure_record.registry_entry_id,
        source_hypothesis_ids=closure_record.source_hypothesis_ids,
        signal_ids=closure_record.signal_ids,
        regime_frame_ids=closure_record.regime_frame_ids,
        rule_ids=closure_record.rule_ids,
        upstream_falsification_references=closure_record.upstream_falsification_references,
        sections=tuple(validate_dossier_section(section) for section in sections),
        downstream_review_questions=_normalize_text_sequence(
            downstream_review_questions,
            "downstream_review_questions",
        ),
        pending_requirements=_normalize_text_sequence(
            pending_requirements,
            "pending_requirements",
        ),
        assumptions=_normalize_text_sequence(assumptions, "assumptions"),
        limitations=_normalize_text_sequence(limitations, "limitations"),
        non_approval_statement=_require_text(
            non_approval_statement,
            "non_approval_statement",
        ),
        audit_reference=_require_text(audit_reference, "audit_reference"),
        prepared_at=prepared_at or datetime.now(timezone.utc),
    )
    return validate_strategy_dossier(dossier)


def validate_strategy_dossier(dossier: StrategyDossier) -> StrategyDossier:
    """Validate closure origin, dossier status, sections, and traceability."""

    if not isinstance(dossier.closure_record, StrategyClosureRecord):
        raise ValueError("strategy dossier must reference a valid closure record")
    validate_strategy_closure_record(dossier.closure_record)

    if (
        dossier.closure_record.closure_status
        is not StrategyClosureStatus.CLOSED_PENDING_DOSSIER_HANDOFF
    ):
        raise ValueError("closure record must be closed_pending_dossier_handoff")

    if not isinstance(dossier.handoff_status, DossierHandoffStatus):
        raise TypeError("handoff_status must be a DossierHandoffStatus")
    if (
        dossier.handoff_status
        is not DossierHandoffStatus.DOSSIER_PREPARED_PENDING_FINAL_AUDIT
    ):
        raise ValueError("dossier handoff status must remain prepared pending final audit")

    closure_record = dossier.closure_record
    if dossier.candidate_id != closure_record.candidate_id:
        raise ValueError("candidate_id must match the closure record")
    if dossier.closure_id != closure_record.closure_id:
        raise ValueError("closure_id must match the closure record")
    if dossier.quality_assessment_id != closure_record.quality_assessment_id:
        raise ValueError("quality_assessment_id must match the closure record")
    if dossier.registry_entry_id != closure_record.registry_entry_id:
        raise ValueError("registry_entry_id must match the closure record")
    if dossier.source_hypothesis_ids != closure_record.source_hypothesis_ids:
        raise ValueError("source_hypothesis_ids must match the closure record")
    if dossier.signal_ids != closure_record.signal_ids:
        raise ValueError("signal_ids must match the closure record")
    if dossier.regime_frame_ids != closure_record.regime_frame_ids:
        raise ValueError("regime_frame_ids must match the closure record")
    if dossier.rule_ids != closure_record.rule_ids:
        raise ValueError("rule_ids must match the closure record")
    if (
        dossier.upstream_falsification_references
        != closure_record.upstream_falsification_references
    ):
        raise ValueError("upstream_falsification_references must match the closure record")

    _require_text(dossier.dossier_id, "dossier_id")
    _validate_required_sections(dossier.sections)
    _normalize_text_sequence(
        dossier.downstream_review_questions,
        "downstream_review_questions",
    )
    _normalize_text_sequence(dossier.pending_requirements, "pending_requirements")
    _normalize_text_sequence(dossier.assumptions, "assumptions")
    _normalize_text_sequence(dossier.limitations, "limitations")
    _require_text(dossier.non_approval_statement, "non_approval_statement")
    _require_text(dossier.audit_reference, "audit_reference")

    return dossier


def _validate_required_sections(sections: Sequence[DossierSection]) -> None:
    if isinstance(sections, (str, bytes)):
        raise TypeError("sections must be a sequence of DossierSection values")
    validated = tuple(validate_dossier_section(section) for section in sections)
    if not validated:
        raise ValueError("sections must contain at least one item")

    section_types = {section.section_type for section in validated}
    missing = REQUIRED_DOSSIER_SECTION_TYPES - section_types
    if missing:
        missing_values = sorted(section_type.value for section_type in missing)
        raise ValueError(f"missing required dossier section types: {missing_values}")

    _reject_duplicate_values((section.section_id for section in validated), "section_id")
    _reject_duplicate_values((section.section_type.value for section in validated), "section_type")


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


def _reject_duplicate_values(values: Iterable[str], field_name: str) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    if duplicates:
        raise ValueError(f"duplicate {field_name}: {sorted(duplicates)}")

