"""Pure in-memory hypothesis registry for Research Layer.

This module validates and manages human-authored research hypotheses. It does
not generate hypotheses, score them, promote them automatically, or convert
them into strategy logic.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass

import pandas as pd


VALID_STATUSES: tuple[str, ...] = (
    "draft",
    "proposed",
    "rejected",
    "archived",
    "promoted_for_strategy_review",
)

REQUIRED_TEXT_FIELDS: tuple[str, ...] = (
    "hypothesis_id",
    "title",
    "description",
    "rationale",
    "evidence_summary",
)

LIST_FIELDS: tuple[str, ...] = (
    "related_features",
    "related_horizons",
    "related_regimes",
    "assumptions",
    "falsification_conditions",
)


@dataclass(frozen=True)
class ResearchHypothesis:
    """Structured, auditable research hypothesis record."""

    hypothesis_id: str
    title: str
    description: str
    rationale: str
    related_features: tuple[str, ...]
    related_horizons: tuple[str, ...]
    related_regimes: tuple[str, ...]
    evidence_summary: str
    evidence_source: dict[str, str]
    assumptions: tuple[str, ...]
    falsification_conditions: tuple[str, ...]
    status: str
    created_at: pd.Timestamp
    updated_at: pd.Timestamp
    notes: str = ""


def create_hypothesis(
    *,
    hypothesis_id: str,
    title: str,
    description: str,
    rationale: str,
    related_features: Sequence[str],
    related_horizons: Sequence[str],
    related_regimes: Sequence[str],
    evidence_summary: str,
    evidence_source: Mapping[str, str],
    assumptions: Sequence[str],
    falsification_conditions: Sequence[str],
    status: str = "draft",
    created_at: object | None = None,
    updated_at: object | None = None,
    notes: str = "",
) -> ResearchHypothesis:
    """Create and validate one human-authored research hypothesis."""

    created_timestamp = _timestamp_or_now(created_at)
    updated_timestamp = _timestamp_or_now(updated_at) if updated_at is not None else created_timestamp

    hypothesis = ResearchHypothesis(
        hypothesis_id=hypothesis_id,
        title=title,
        description=description,
        rationale=rationale,
        related_features=_normalize_string_list(related_features, field_name="related_features"),
        related_horizons=_normalize_string_list(related_horizons, field_name="related_horizons"),
        related_regimes=_normalize_string_list(related_regimes, field_name="related_regimes"),
        evidence_summary=evidence_summary,
        evidence_source=_normalize_evidence_source(evidence_source),
        assumptions=_normalize_string_list(assumptions, field_name="assumptions"),
        falsification_conditions=_normalize_string_list(
            falsification_conditions,
            field_name="falsification_conditions",
        ),
        status=status,
        created_at=created_timestamp,
        updated_at=updated_timestamp,
        notes=notes,
    )
    return validate_hypothesis(hypothesis)


def validate_hypothesis(hypothesis: ResearchHypothesis | Mapping[str, object]) -> ResearchHypothesis:
    """Validate and normalize a hypothesis record."""

    record = _as_record(hypothesis)

    missing = [field for field in _schema_fields() if field not in record]
    if missing:
        raise ValueError(f"hypothesis missing required fields: {missing}")

    for field in REQUIRED_TEXT_FIELDS:
        _require_non_empty_text(record[field], field_name=field)

    status = str(record["status"])
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid hypothesis status: {status}")

    notes = record["notes"]
    if not isinstance(notes, str):
        raise TypeError("notes must be a string")

    created_at = pd.Timestamp(record["created_at"])
    updated_at = pd.Timestamp(record["updated_at"])
    if pd.isna(created_at) or pd.isna(updated_at):
        raise ValueError("created_at and updated_at must be valid timestamps")
    if updated_at < created_at:
        raise ValueError("updated_at must be greater than or equal to created_at")

    evidence_source = _normalize_evidence_source(record["evidence_source"])
    normalized_lists = {
        field: _normalize_string_list(record[field], field_name=field) for field in LIST_FIELDS
    }
    if not normalized_lists["falsification_conditions"]:
        raise ValueError("falsification_conditions must contain at least one condition")

    return ResearchHypothesis(
        hypothesis_id=str(record["hypothesis_id"]).strip(),
        title=str(record["title"]).strip(),
        description=str(record["description"]).strip(),
        rationale=str(record["rationale"]).strip(),
        related_features=normalized_lists["related_features"],
        related_horizons=normalized_lists["related_horizons"],
        related_regimes=normalized_lists["related_regimes"],
        evidence_summary=str(record["evidence_summary"]).strip(),
        evidence_source=evidence_source,
        assumptions=normalized_lists["assumptions"],
        falsification_conditions=normalized_lists["falsification_conditions"],
        status=status,
        created_at=created_at,
        updated_at=updated_at,
        notes=notes.strip(),
    )


def create_registry(hypotheses: Sequence[ResearchHypothesis | Mapping[str, object]]) -> pd.DataFrame:
    """Create a validated in-memory hypothesis registry DataFrame."""

    validated = [validate_hypothesis(hypothesis) for hypothesis in hypotheses]
    _reject_duplicate_ids(validated)
    return pd.DataFrame([hypothesis_to_record(hypothesis) for hypothesis in validated])


def add_hypothesis(
    registry: pd.DataFrame,
    hypothesis: ResearchHypothesis | Mapping[str, object],
) -> pd.DataFrame:
    """Return a new registry with one validated hypothesis appended."""

    existing = [validate_hypothesis(record) for record in registry.to_dict(orient="records")]
    candidate = validate_hypothesis(hypothesis)
    return create_registry([*existing, candidate])


def update_hypothesis(
    registry: pd.DataFrame,
    *,
    hypothesis_id: str,
    updates: Mapping[str, object],
) -> pd.DataFrame:
    """Return a new registry with validated updates applied to one hypothesis."""

    if not updates:
        raise ValueError("updates must contain at least one field")
    if "hypothesis_id" in updates and updates["hypothesis_id"] != hypothesis_id:
        raise ValueError("hypothesis_id cannot be changed by update_hypothesis")

    records = registry.to_dict(orient="records")
    match_indexes = [
        index for index, record in enumerate(records) if record.get("hypothesis_id") == hypothesis_id
    ]
    if not match_indexes:
        raise ValueError(f"hypothesis_id not found: {hypothesis_id}")
    if len(match_indexes) > 1:
        raise ValueError(f"duplicate hypothesis_id in registry: {hypothesis_id}")

    index = match_indexes[0]
    updated_record = {**records[index], **dict(updates)}
    if "updated_at" not in updated_record:
        updated_record["updated_at"] = _timestamp_or_now(None)
    records[index] = hypothesis_to_record(validate_hypothesis(updated_record))
    return create_registry(records)


def update_hypothesis_status(
    registry: pd.DataFrame,
    *,
    hypothesis_id: str,
    status: str,
    updated_at: object | None = None,
    notes: str | None = None,
) -> pd.DataFrame:
    """Return a new registry with status updated for one hypothesis."""

    updates: dict[str, object] = {
        "status": status,
        "updated_at": _timestamp_or_now(updated_at),
    }
    if notes is not None:
        updates["notes"] = notes
    return update_hypothesis(registry, hypothesis_id=hypothesis_id, updates=updates)


def hypothesis_to_record(hypothesis: ResearchHypothesis) -> dict[str, object]:
    """Convert a validated hypothesis to a registry record."""

    record = asdict(hypothesis)
    for field in LIST_FIELDS:
        record[field] = list(record[field])
    return record


def _as_record(hypothesis: ResearchHypothesis | Mapping[str, object]) -> dict[str, object]:
    if isinstance(hypothesis, ResearchHypothesis):
        return hypothesis_to_record(hypothesis)
    if isinstance(hypothesis, Mapping):
        return dict(hypothesis)
    raise TypeError("hypothesis must be ResearchHypothesis or mapping")


def _schema_fields() -> tuple[str, ...]:
    return (
        "hypothesis_id",
        "title",
        "description",
        "rationale",
        "related_features",
        "related_horizons",
        "related_regimes",
        "evidence_summary",
        "evidence_source",
        "assumptions",
        "falsification_conditions",
        "status",
        "created_at",
        "updated_at",
        "notes",
    )


def _normalize_string_list(values: object, *, field_name: str) -> tuple[str, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
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


def _normalize_evidence_source(value: object) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise TypeError("evidence_source must be structured mapping metadata")
    if not value:
        raise ValueError("evidence_source must not be empty")

    normalized: dict[str, str] = {}
    for key, raw_value in value.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError("evidence_source keys must be non-empty strings")
        if raw_value is None:
            raise ValueError("evidence_source values must not be null")
        normalized_value = str(raw_value).strip()
        if not normalized_value:
            raise ValueError("evidence_source values must be non-empty")
        normalized[key.strip()] = normalized_value

    return normalized


def _require_non_empty_text(value: object, *, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be non-empty text")


def _timestamp_or_now(value: object | None) -> pd.Timestamp:
    if value is None:
        return pd.Timestamp.now(tz="UTC")
    timestamp = pd.Timestamp(value)
    if pd.isna(timestamp):
        raise ValueError("timestamp values must be valid")
    return timestamp


def _reject_duplicate_ids(hypotheses: Sequence[ResearchHypothesis]) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for hypothesis in hypotheses:
        if hypothesis.hypothesis_id in seen:
            duplicates.add(hypothesis.hypothesis_id)
        seen.add(hypothesis.hypothesis_id)
    if duplicates:
        raise ValueError(f"duplicate hypothesis_id values: {sorted(duplicates)}")
