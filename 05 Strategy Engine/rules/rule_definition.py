"""Conceptual rule definitions for 05 Strategy Engine.

Rule definitions here are declarative and auditable. They require a valid
signal definition and a matching valid regime context frame. They do not
represent executable trading rules, strategy candidates, backtests, PnL, or
performance claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Sequence

from regimes.regime_context import RegimeContextFrame, validate_regime_context_frame
from signals.signal_definition import SignalDefinition, validate_signal_definition


class RuleCategory(str, Enum):
    """Conceptual rule definition categories."""

    ENTRY_CONDITION = "entry_condition"
    EXIT_CONDITION = "exit_condition"
    INVALIDATION_CONDITION = "invalidation_condition"
    FILTER_CONDITION = "filter_condition"
    CONFLICT_RESOLUTION = "conflict_resolution"


@dataclass(frozen=True)
class RuleDefinition:
    """Auditable conceptual rule definition."""

    rule_id: str
    signal_definition: SignalDefinition
    regime_context_frame: RegimeContextFrame
    rule_category: RuleCategory
    rule_statement: str
    interpretation_guidance: str
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    falsification_references: tuple[str, ...]
    audit_reference: str
    created_at: datetime


def create_rule_definition(
    *,
    rule_id: str,
    signal_definition: SignalDefinition,
    regime_context_frame: RegimeContextFrame,
    rule_category: RuleCategory,
    rule_statement: str,
    interpretation_guidance: str,
    assumptions: Sequence[str],
    limitations: Sequence[str],
    falsification_references: Sequence[str],
    audit_reference: str,
    created_at: datetime | None = None,
) -> RuleDefinition:
    """Create and validate one conceptual rule definition."""

    if not isinstance(rule_category, RuleCategory):
        raise TypeError("rule_category must be a RuleCategory")

    rule = RuleDefinition(
        rule_id=_require_text(rule_id, "rule_id"),
        signal_definition=signal_definition,
        regime_context_frame=regime_context_frame,
        rule_category=rule_category,
        rule_statement=_require_text(rule_statement, "rule_statement"),
        interpretation_guidance=_require_text(
            interpretation_guidance,
            "interpretation_guidance",
        ),
        assumptions=_normalize_text_sequence(assumptions, "assumptions"),
        limitations=_normalize_text_sequence(limitations, "limitations"),
        falsification_references=_normalize_text_sequence(
            falsification_references,
            "falsification_references",
        ),
        audit_reference=_require_text(audit_reference, "audit_reference"),
        created_at=created_at or datetime.now(timezone.utc),
    )
    return validate_rule_definition(rule)


def validate_rule_definition(rule: RuleDefinition) -> RuleDefinition:
    """Validate source signal, regime context, and governance fields."""

    if not isinstance(rule.signal_definition, SignalDefinition):
        raise ValueError("rule definition must reference a valid signal definition")
    validate_signal_definition(rule.signal_definition)

    if not isinstance(rule.regime_context_frame, RegimeContextFrame):
        raise ValueError("rule definition must reference a valid regime context frame")
    validate_regime_context_frame(rule.regime_context_frame)

    if rule.regime_context_frame.signal_definition != rule.signal_definition:
        raise ValueError("regime context frame must reference the same signal definition")

    if not isinstance(rule.rule_category, RuleCategory):
        raise TypeError("rule_category must be a RuleCategory")

    _require_text(rule.rule_id, "rule_id")
    _require_text(rule.rule_statement, "rule_statement")
    _require_text(rule.interpretation_guidance, "interpretation_guidance")
    _require_text(rule.audit_reference, "audit_reference")
    _normalize_text_sequence(rule.assumptions, "assumptions")
    _normalize_text_sequence(rule.limitations, "limitations")
    _normalize_text_sequence(rule.falsification_references, "falsification_references")

    return rule


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
