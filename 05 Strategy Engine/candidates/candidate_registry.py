"""Immutable strategy candidate registry for 05 Strategy Engine.

Registry entries record valid conceptual candidates and matching uncalibrated
risk templates. They do not approve, validate, backtest, close, hand off, or
authorize trading.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Sequence

from candidates.strategy_candidate import StrategyCandidate, validate_strategy_candidate
from risk_templates.risk_template import RiskTemplate, validate_risk_template


class RegistryStatus(str, Enum):
    """Registry lifecycle state for Block 08."""

    REGISTERED_PENDING_QUALITY_GATES = "registered_pending_quality_gates"


@dataclass(frozen=True)
class StrategyCandidateRegistryEntry:
    """Immutable audit record for one registered conceptual candidate."""

    entry_id: str
    strategy_candidate: StrategyCandidate
    risk_template: RiskTemplate
    registry_status: RegistryStatus
    source_hypothesis_ids: tuple[str, ...]
    signal_ids: tuple[str, ...]
    regime_frame_ids: tuple[str, ...]
    rule_ids: tuple[str, ...]
    assumptions: tuple[str, ...]
    limitations: tuple[str, ...]
    falsification_references: tuple[str, ...]
    audit_reference: str
    registered_at: datetime


@dataclass(frozen=True)
class StrategyCandidateRegistry:
    """Immutable collection of registry entries."""

    entries: tuple[StrategyCandidateRegistryEntry, ...]


def create_registry_entry(
    *,
    entry_id: str,
    strategy_candidate: StrategyCandidate,
    risk_template: RiskTemplate,
    assumptions: Sequence[str],
    limitations: Sequence[str],
    falsification_references: Sequence[str],
    audit_reference: str,
    registry_status: RegistryStatus = RegistryStatus.REGISTERED_PENDING_QUALITY_GATES,
    registered_at: datetime | None = None,
) -> StrategyCandidateRegistryEntry:
    """Create and validate one immutable registry entry."""

    if not isinstance(registry_status, RegistryStatus):
        raise TypeError("registry_status must be a RegistryStatus")
    if not isinstance(strategy_candidate, StrategyCandidate):
        raise ValueError("registry entry must reference a valid strategy candidate")
    if not isinstance(risk_template, RiskTemplate):
        raise ValueError("registry entry must reference a valid risk template")

    entry = StrategyCandidateRegistryEntry(
        entry_id=_require_text(entry_id, "entry_id"),
        strategy_candidate=strategy_candidate,
        risk_template=risk_template,
        registry_status=registry_status,
        source_hypothesis_ids=_source_hypothesis_ids(strategy_candidate),
        signal_ids=_signal_ids(strategy_candidate),
        regime_frame_ids=_regime_frame_ids(strategy_candidate),
        rule_ids=_rule_ids(strategy_candidate),
        assumptions=_normalize_text_sequence(assumptions, "assumptions"),
        limitations=_normalize_text_sequence(limitations, "limitations"),
        falsification_references=_normalize_text_sequence(
            falsification_references,
            "falsification_references",
        ),
        audit_reference=_require_text(audit_reference, "audit_reference"),
        registered_at=registered_at or datetime.now(timezone.utc),
    )
    return validate_registry_entry(entry)


def validate_registry_entry(
    entry: StrategyCandidateRegistryEntry,
) -> StrategyCandidateRegistryEntry:
    """Validate origin artifacts, status, traceability, and governance fields."""

    if not isinstance(entry.strategy_candidate, StrategyCandidate):
        raise ValueError("registry entry must reference a valid strategy candidate")
    validate_strategy_candidate(entry.strategy_candidate)

    if not isinstance(entry.risk_template, RiskTemplate):
        raise ValueError("registry entry must reference a valid risk template")
    validate_risk_template(entry.risk_template)

    if entry.risk_template.strategy_candidate != entry.strategy_candidate:
        raise ValueError("risk template must reference the same strategy candidate")

    if not isinstance(entry.registry_status, RegistryStatus):
        raise TypeError("registry_status must be a RegistryStatus")
    if entry.registry_status is not RegistryStatus.REGISTERED_PENDING_QUALITY_GATES:
        raise ValueError("registry entries must remain registered_pending_quality_gates")

    _require_text(entry.entry_id, "entry_id")
    _normalize_text_sequence(entry.assumptions, "assumptions")
    _normalize_text_sequence(entry.limitations, "limitations")
    _normalize_text_sequence(entry.falsification_references, "falsification_references")
    _require_text(entry.audit_reference, "audit_reference")
    _require_non_empty_tuple(entry.source_hypothesis_ids, "source_hypothesis_ids")
    _require_non_empty_tuple(entry.signal_ids, "signal_ids")
    _require_non_empty_tuple(entry.regime_frame_ids, "regime_frame_ids")
    _require_non_empty_tuple(entry.rule_ids, "rule_ids")

    return entry


def create_registry(
    entries: Sequence[StrategyCandidateRegistryEntry],
) -> StrategyCandidateRegistry:
    """Create an immutable registry from validated entries."""

    validated = tuple(validate_registry_entry(entry) for entry in entries)
    _reject_duplicate_values((entry.entry_id for entry in validated), "entry_id")
    _reject_duplicate_values(
        (entry.strategy_candidate.candidate_id for entry in validated),
        "candidate_id",
    )
    return StrategyCandidateRegistry(entries=validated)


def add_registry_entry(
    registry: StrategyCandidateRegistry,
    entry: StrategyCandidateRegistryEntry,
) -> StrategyCandidateRegistry:
    """Return a new registry with one additional validated entry."""

    if not isinstance(registry, StrategyCandidateRegistry):
        raise TypeError("registry must be a StrategyCandidateRegistry")
    return create_registry((*registry.entries, validate_registry_entry(entry)))


def _source_hypothesis_ids(strategy_candidate: StrategyCandidate) -> tuple[str, ...]:
    ids = (
        rule.signal_definition.source_hypothesis_decision.input_id
        for rule in strategy_candidate.rule_definitions
    )
    return tuple(dict.fromkeys(ids))


def _signal_ids(strategy_candidate: StrategyCandidate) -> tuple[str, ...]:
    ids = (rule.signal_definition.signal_id for rule in strategy_candidate.rule_definitions)
    return tuple(dict.fromkeys(ids))


def _regime_frame_ids(strategy_candidate: StrategyCandidate) -> tuple[str, ...]:
    ids = (rule.regime_context_frame.frame_id for rule in strategy_candidate.rule_definitions)
    return tuple(dict.fromkeys(ids))


def _rule_ids(strategy_candidate: StrategyCandidate) -> tuple[str, ...]:
    ids = (rule.rule_id for rule in strategy_candidate.rule_definitions)
    return tuple(dict.fromkeys(ids))


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


def _require_non_empty_tuple(values: tuple[str, ...], field_name: str) -> None:
    if not values:
        raise ValueError(f"{field_name} must contain at least one item")
    for value in values:
        _require_text(value, field_name)


def _reject_duplicate_values(values: Sequence[str], field_name: str) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    if duplicates:
        raise ValueError(f"duplicate {field_name}: {sorted(duplicates)}")
