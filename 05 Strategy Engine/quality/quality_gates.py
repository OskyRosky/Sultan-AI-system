"""Conceptual strategy quality gates for 05 Strategy Engine.

Quality gates evaluate structural governance readiness for registered
conceptual candidates. They do not evaluate edge, profitability, historical
robustness, backtest readiness, deployment readiness, or trading approval.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Sequence

from candidates.candidate_registry import (
    RegistryStatus,
    StrategyCandidateRegistryEntry,
    validate_registry_entry,
)


class QualityGateType(str, Enum):
    """Conceptual quality dimensions for Block 09."""

    TRACEABILITY = "traceability"
    GOVERNANCE_FIELDS = "governance_fields"
    STRUCTURAL_COMPLEXITY = "structural_complexity"
    EVIDENCE_GOVERNANCE_READINESS = "evidence_governance_readiness"
    RISK_TEMPLATE_COMPLETENESS = "risk_template_completeness"
    FALSIFICATION_READINESS = "falsification_readiness"
    NON_PERFORMANCE_SCOPE = "non_performance_scope"


class QualityAssessmentStatus(str, Enum):
    """Derived quality assessment state for Block 09."""

    PASSED_PENDING_STRATEGY_CLOSURE = "passed_pending_strategy_closure"
    FAILED_REQUIRES_REVISION = "failed_requires_revision"


REQUIRED_GATE_TYPES: frozenset[QualityGateType] = frozenset(QualityGateType)


@dataclass(frozen=True)
class QualityGateResult:
    """Result for one conceptual quality gate."""

    gate_id: str
    gate_type: QualityGateType
    passed: bool
    assessment_summary: str
    limitations: tuple[str, ...]
    audit_reference: str


@dataclass(frozen=True)
class StrategyQualityGateAssessment:
    """Immutable quality-gate assessment for one registry entry."""

    assessment_id: str
    registry_entry: StrategyCandidateRegistryEntry
    gate_results: tuple[QualityGateResult, ...]
    assessment_status: QualityAssessmentStatus
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    non_approval_statement: str
    audit_reference: str
    assessed_at: datetime


def create_quality_gate_result(
    *,
    gate_id: str,
    gate_type: QualityGateType,
    passed: bool,
    assessment_summary: str,
    limitations: Sequence[str],
    audit_reference: str,
) -> QualityGateResult:
    """Create and validate one conceptual quality gate result."""

    if not isinstance(gate_type, QualityGateType):
        raise TypeError("gate_type must be a QualityGateType")
    if not isinstance(passed, bool):
        raise TypeError("passed must be a bool")

    result = QualityGateResult(
        gate_id=_require_text(gate_id, "gate_id"),
        gate_type=gate_type,
        passed=passed,
        assessment_summary=_require_text(assessment_summary, "assessment_summary"),
        limitations=_normalize_text_sequence(limitations, "limitations"),
        audit_reference=_require_text(audit_reference, "audit_reference"),
    )
    return validate_quality_gate_result(result)


def validate_quality_gate_result(result: QualityGateResult) -> QualityGateResult:
    """Validate one quality gate result."""

    if not isinstance(result.gate_type, QualityGateType):
        raise TypeError("gate_type must be a QualityGateType")
    if not isinstance(result.passed, bool):
        raise TypeError("passed must be a bool")

    _require_text(result.gate_id, "gate_id")
    _require_text(result.assessment_summary, "assessment_summary")
    _normalize_text_sequence(result.limitations, "limitations")
    _require_text(result.audit_reference, "audit_reference")

    return result


def create_quality_gate_assessment(
    *,
    assessment_id: str,
    registry_entry: StrategyCandidateRegistryEntry,
    gate_results: Sequence[QualityGateResult],
    assumptions: Sequence[str],
    limitations: Sequence[str],
    non_approval_statement: str,
    audit_reference: str,
    assessed_at: datetime | None = None,
) -> StrategyQualityGateAssessment:
    """Create and validate one quality gate assessment."""

    assessment = StrategyQualityGateAssessment(
        assessment_id=_require_text(assessment_id, "assessment_id"),
        registry_entry=registry_entry,
        gate_results=tuple(validate_quality_gate_result(result) for result in gate_results),
        assessment_status=_derive_assessment_status(gate_results),
        assumptions=_normalize_text_sequence(assumptions, "assumptions"),
        limitations=_normalize_text_sequence(limitations, "limitations"),
        non_approval_statement=_require_text(
            non_approval_statement,
            "non_approval_statement",
        ),
        audit_reference=_require_text(audit_reference, "audit_reference"),
        assessed_at=assessed_at or datetime.now(timezone.utc),
    )
    return validate_quality_gate_assessment(assessment)


def validate_quality_gate_assessment(
    assessment: StrategyQualityGateAssessment,
) -> StrategyQualityGateAssessment:
    """Validate registry origin, required gates, and governance fields."""

    if not isinstance(assessment.registry_entry, StrategyCandidateRegistryEntry):
        raise ValueError("quality gate assessment must reference a valid registry entry")
    validate_registry_entry(assessment.registry_entry)

    if assessment.registry_entry.registry_status is not RegistryStatus.REGISTERED_PENDING_QUALITY_GATES:
        raise ValueError("registry entry must be registered_pending_quality_gates")

    _require_text(assessment.assessment_id, "assessment_id")
    _normalize_text_sequence(assessment.assumptions, "assumptions")
    _normalize_text_sequence(assessment.limitations, "limitations")
    _require_text(assessment.non_approval_statement, "non_approval_statement")
    _require_text(assessment.audit_reference, "audit_reference")
    _validate_required_gate_results(assessment.gate_results)

    derived_status = _derive_assessment_status(assessment.gate_results)
    if assessment.assessment_status is not derived_status:
        raise ValueError("assessment_status must be derived from gate_results")

    return assessment


def _derive_assessment_status(
    gate_results: Sequence[QualityGateResult],
) -> QualityAssessmentStatus:
    if not gate_results:
        raise ValueError("gate_results must contain at least one item")
    validated = tuple(validate_quality_gate_result(result) for result in gate_results)
    if all(result.passed for result in validated):
        return QualityAssessmentStatus.PASSED_PENDING_STRATEGY_CLOSURE
    return QualityAssessmentStatus.FAILED_REQUIRES_REVISION


def _validate_required_gate_results(gate_results: Sequence[QualityGateResult]) -> None:
    if isinstance(gate_results, (str, bytes)):
        raise TypeError("gate_results must be a sequence of QualityGateResult values")
    validated = tuple(validate_quality_gate_result(result) for result in gate_results)
    if not validated:
        raise ValueError("gate_results must contain at least one item")

    gate_types = {result.gate_type for result in validated}
    missing = REQUIRED_GATE_TYPES - gate_types
    if missing:
        missing_values = sorted(gate_type.value for gate_type in missing)
        raise ValueError(f"missing required quality gate types: {missing_values}")

    _reject_duplicate_values((result.gate_id for result in validated), "gate_id")
    _reject_duplicate_values((result.gate_type.value for result in validated), "gate_type")


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


def _reject_duplicate_values(values: Sequence[str], field_name: str) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    if duplicates:
        raise ValueError(f"duplicate {field_name}: {sorted(duplicates)}")

