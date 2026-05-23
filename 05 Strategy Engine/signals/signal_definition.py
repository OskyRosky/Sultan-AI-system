"""Abstract signal definitions for 05 Strategy Engine.

Signals here are conceptual and auditable. They must originate from eligible
hypothesis decisions produced by the Block 02 input contract. They do not
represent orders, trades, rules, strategy candidates, or performance claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Sequence

from strategy.inputs_contract import (
    InputType,
    StrategyInputEligibilityDecision,
)


class SignalOrientation(str, Enum):
    """Conceptual orientation labels for signal definitions."""

    LONG_BIAS = "long_bias"
    SHORT_BIAS = "short_bias"
    NEUTRAL = "neutral"
    AVOID = "avoid"


@dataclass(frozen=True)
class SignalDefinition:
    """Auditable conceptual signal definition."""

    signal_id: str
    source_hypothesis_decision: StrategyInputEligibilityDecision
    supporting_finding_decisions: tuple[StrategyInputEligibilityDecision, ...]
    orientation: SignalOrientation
    observable_condition: str
    expected_behavior: str
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    falsification_references: tuple[str, ...]
    audit_reference: str
    created_at: datetime


def create_signal_definition(
    *,
    signal_id: str,
    source_hypothesis_decision: StrategyInputEligibilityDecision,
    orientation: SignalOrientation,
    observable_condition: str,
    expected_behavior: str,
    assumptions: Sequence[str],
    limitations: Sequence[str],
    falsification_references: Sequence[str],
    audit_reference: str,
    supporting_finding_decisions: Sequence[StrategyInputEligibilityDecision] = (),
    created_at: datetime | None = None,
) -> SignalDefinition:
    """Create and validate one abstract signal definition."""

    signal = SignalDefinition(
        signal_id=_require_text(signal_id, "signal_id"),
        source_hypothesis_decision=source_hypothesis_decision,
        supporting_finding_decisions=tuple(supporting_finding_decisions),
        orientation=orientation,
        observable_condition=_require_text(observable_condition, "observable_condition"),
        expected_behavior=_require_text(expected_behavior, "expected_behavior"),
        assumptions=_normalize_text_sequence(assumptions, "assumptions"),
        limitations=_normalize_text_sequence(limitations, "limitations"),
        falsification_references=_normalize_text_sequence(
            falsification_references,
            "falsification_references",
        ),
        audit_reference=_require_text(audit_reference, "audit_reference"),
        created_at=created_at or datetime.now(timezone.utc),
    )
    return validate_signal_definition(signal)


def validate_signal_definition(signal: SignalDefinition) -> SignalDefinition:
    """Validate signal origin, supporting context, and governance fields."""

    if signal.source_hypothesis_decision.input_type is not InputType.HYPOTHESIS:
        raise ValueError("signal origin must be an eligible hypothesis decision")
    if not signal.source_hypothesis_decision.eligible_for_strategy_design:
        raise ValueError("source hypothesis decision is not eligible for strategy design")

    for decision in signal.supporting_finding_decisions:
        if decision.input_type is not InputType.FINDING:
            raise ValueError("supporting context must contain finding decisions only")
        if not decision.eligible_for_strategy_design:
            raise ValueError("supporting finding decision is not eligible for strategy design")

    _require_text(signal.signal_id, "signal_id")
    _require_text(signal.observable_condition, "observable_condition")
    _require_text(signal.expected_behavior, "expected_behavior")
    _require_text(signal.audit_reference, "audit_reference")
    _normalize_text_sequence(signal.assumptions, "assumptions")
    _normalize_text_sequence(signal.limitations, "limitations")
    _normalize_text_sequence(signal.falsification_references, "falsification_references")

    return signal


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
