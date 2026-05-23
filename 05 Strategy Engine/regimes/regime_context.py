"""Regime context framing for 05 Strategy Engine.

Regime context frames attach conceptual market context to valid signal
definitions. They do not calculate regimes, switch strategies, create rules,
build candidates, backtest, or make performance claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Sequence

from signals.signal_definition import SignalDefinition, validate_signal_definition


class RegimeType(str, Enum):
    """Conceptual regime context categories."""

    TREND = "trend"
    VOLATILITY = "volatility"
    MOMENTUM = "momentum"
    RANGE = "range"
    LIQUIDITY = "liquidity"
    MACRO = "macro"
    STRUCTURAL = "structural"


@dataclass(frozen=True)
class RegimeContextFrame:
    """Auditable context frame attached to one signal definition."""

    frame_id: str
    signal_definition: SignalDefinition
    regime_type: RegimeType
    regime_label: str
    context_description: str
    applicability_rationale: str
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    falsification_references: tuple[str, ...]
    audit_reference: str
    created_at: datetime


def create_regime_context_frame(
    *,
    frame_id: str,
    signal_definition: SignalDefinition,
    regime_type: RegimeType,
    regime_label: str,
    context_description: str,
    applicability_rationale: str,
    assumptions: Sequence[str],
    limitations: Sequence[str],
    falsification_references: Sequence[str],
    audit_reference: str,
    created_at: datetime | None = None,
) -> RegimeContextFrame:
    """Create and validate one conceptual regime context frame."""

    if not isinstance(regime_type, RegimeType):
        raise TypeError("regime_type must be a RegimeType")

    frame = RegimeContextFrame(
        frame_id=_require_text(frame_id, "frame_id"),
        signal_definition=signal_definition,
        regime_type=regime_type,
        regime_label=_require_text(regime_label, "regime_label"),
        context_description=_require_text(context_description, "context_description"),
        applicability_rationale=_require_text(
            applicability_rationale,
            "applicability_rationale",
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
    return validate_regime_context_frame(frame)


def validate_regime_context_frame(frame: RegimeContextFrame) -> RegimeContextFrame:
    """Validate source signal and required governance fields."""

    if not isinstance(frame.signal_definition, SignalDefinition):
        raise ValueError("regime context frame must originate from a valid signal definition")
    validate_signal_definition(frame.signal_definition)

    if not isinstance(frame.regime_type, RegimeType):
        raise TypeError("regime_type must be a RegimeType")

    _require_text(frame.frame_id, "frame_id")
    _require_text(frame.regime_label, "regime_label")
    _require_text(frame.context_description, "context_description")
    _require_text(frame.applicability_rationale, "applicability_rationale")
    _require_text(frame.audit_reference, "audit_reference")
    _normalize_text_sequence(frame.assumptions, "assumptions")
    _normalize_text_sequence(frame.limitations, "limitations")
    _normalize_text_sequence(frame.falsification_references, "falsification_references")

    return frame


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
