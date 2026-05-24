"""Conceptual risk template assignment for 05 Strategy Engine.

Risk templates here attach uncalibrated risk governance dimensions to valid
strategy candidates. They are not risk engines, calibrated risk models,
position sizing policies, stop rules, leverage settings, or trading approval.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Sequence

from candidates.strategy_candidate import (
    CandidateStatus,
    StrategyCandidate,
    validate_strategy_candidate,
)


class RiskDimension(str, Enum):
    """Conceptual risk dimensions for future governance review."""

    MARKET_EXPOSURE = "market_exposure"
    LIQUIDITY = "liquidity"
    VOLATILITY = "volatility"
    CONCENTRATION = "concentration"
    REGIME_DEPENDENCY = "regime_dependency"
    MODEL_RISK = "model_risk"
    EXECUTION_DEPENDENCY = "execution_dependency"
    OPERATIONAL = "operational"


class CalibrationStatus(str, Enum):
    """Risk template calibration state."""

    UNCALIBRATED = "uncalibrated"


@dataclass(frozen=True)
class RiskTemplate:
    """Auditable uncalibrated risk template assignment."""

    template_id: str
    strategy_candidate: StrategyCandidate
    risk_dimensions: tuple[RiskDimension, ...]
    constraint_intent: str
    exclusion_criteria: tuple[str, ...]
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    calibration_status: CalibrationStatus
    non_calibrated_rationale: str
    audit_reference: str
    created_at: datetime


def create_risk_template(
    *,
    template_id: str,
    strategy_candidate: StrategyCandidate,
    risk_dimensions: Sequence[RiskDimension],
    constraint_intent: str,
    assumptions: Sequence[str],
    limitations: Sequence[str],
    non_calibrated_rationale: str,
    audit_reference: str,
    exclusion_criteria: Sequence[str] = (),
    calibration_status: CalibrationStatus = CalibrationStatus.UNCALIBRATED,
    created_at: datetime | None = None,
) -> RiskTemplate:
    """Create and validate one conceptual uncalibrated risk template."""

    if not isinstance(calibration_status, CalibrationStatus):
        raise TypeError("calibration_status must be a CalibrationStatus")

    template = RiskTemplate(
        template_id=_require_text(template_id, "template_id"),
        strategy_candidate=strategy_candidate,
        risk_dimensions=_normalize_risk_dimensions(risk_dimensions),
        constraint_intent=_require_text(constraint_intent, "constraint_intent"),
        exclusion_criteria=_normalize_optional_text_sequence(
            exclusion_criteria,
            "exclusion_criteria",
        ),
        assumptions=_normalize_text_sequence(assumptions, "assumptions"),
        limitations=_normalize_text_sequence(limitations, "limitations"),
        calibration_status=calibration_status,
        non_calibrated_rationale=_require_text(
            non_calibrated_rationale,
            "non_calibrated_rationale",
        ),
        audit_reference=_require_text(audit_reference, "audit_reference"),
        created_at=created_at or datetime.now(timezone.utc),
    )
    return validate_risk_template(template)


def validate_risk_template(template: RiskTemplate) -> RiskTemplate:
    """Validate candidate origin, uncalibrated status, and governance fields."""

    if not isinstance(template.strategy_candidate, StrategyCandidate):
        raise ValueError("risk template must reference a valid strategy candidate")
    if template.strategy_candidate.status is not CandidateStatus.PENDING_RISK_TEMPLATE:
        raise ValueError("strategy candidate must be pending_risk_template")
    validate_strategy_candidate(template.strategy_candidate)

    if not isinstance(template.calibration_status, CalibrationStatus):
        raise TypeError("calibration_status must be a CalibrationStatus")
    if template.calibration_status is not CalibrationStatus.UNCALIBRATED:
        raise ValueError("risk templates in Block 07 must remain uncalibrated")

    _require_text(template.template_id, "template_id")
    _normalize_risk_dimensions(template.risk_dimensions)
    _require_text(template.constraint_intent, "constraint_intent")
    _normalize_optional_text_sequence(template.exclusion_criteria, "exclusion_criteria")
    _normalize_text_sequence(template.assumptions, "assumptions")
    _normalize_text_sequence(template.limitations, "limitations")
    _require_text(template.non_calibrated_rationale, "non_calibrated_rationale")
    _require_text(template.audit_reference, "audit_reference")

    return template


def _normalize_risk_dimensions(values: Sequence[RiskDimension]) -> tuple[RiskDimension, ...]:
    if isinstance(values, (str, bytes)):
        raise TypeError("risk_dimensions must be a sequence of RiskDimension values")
    normalized: list[RiskDimension] = []
    for value in values:
        if not isinstance(value, RiskDimension):
            raise TypeError("risk_dimensions must contain only RiskDimension values")
        if value not in normalized:
            normalized.append(value)
    if not normalized:
        raise ValueError("risk_dimensions must contain at least one dimension")
    return tuple(normalized)


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
