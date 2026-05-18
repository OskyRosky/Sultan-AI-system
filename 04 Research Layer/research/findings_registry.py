"""Pure in-memory research findings registry for Research Layer.

This module validates and manages structured human-reviewed findings. It does
not generate findings, score them, approve trading logic, or convert findings
into strategy behavior.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, dataclass

import pandas as pd


VALID_DECISIONS: tuple[str, ...] = (
    "advance_to_quality_review",
    "defer",
    "reject",
    "needs_more_data",
    "archive",
)

VALID_STATUSES: tuple[str, ...] = (
    "draft",
    "observed",
    "under_review",
    "rejected",
    "archived",
    "promoted_to_quality_review",
)

REQUIRED_TEXT_FIELDS: tuple[str, ...] = (
    "finding_id",
    "title",
    "description",
    "evidence_summary",
)

LIST_FIELDS: tuple[str, ...] = (
    "related_features",
    "related_horizons",
    "related_regimes",
    "limitations",
    "caveats",
)


@dataclass(frozen=True)
class ResearchFinding:
    """Structured, auditable research finding record."""

    finding_id: str
    title: str
    description: str
    linked_hypothesis_id: str
    evidence_summary: str
    supporting_metrics: dict[str, str]
    sample_scope: dict[str, str]
    related_features: tuple[str, ...]
    related_horizons: tuple[str, ...]
    related_regimes: tuple[str, ...]
    limitations: tuple[str, ...]
    caveats: tuple[str, ...]
    decision: str
    status: str
    created_at: pd.Timestamp
    updated_at: pd.Timestamp
    notes: str = ""


def create_finding(
    *,
    finding_id: str,
    title: str,
    description: str,
    linked_hypothesis_id: str = "",
    evidence_summary: str,
    supporting_metrics: Mapping[str, object],
    sample_scope: Mapping[str, object],
    related_features: Sequence[str],
    related_horizons: Sequence[str],
    related_regimes: Sequence[str],
    limitations: Sequence[str],
    caveats: Sequence[str],
    decision: str = "defer",
    status: str = "draft",
    created_at: object | None = None,
    updated_at: object | None = None,
    notes: str = "",
) -> ResearchFinding:
    """Create and validate one structured research finding."""

    created_timestamp = _timestamp_or_now(created_at)
    updated_timestamp = _timestamp_or_now(updated_at) if updated_at is not None else created_timestamp

    finding = ResearchFinding(
        finding_id=finding_id,
        title=title,
        description=description,
        linked_hypothesis_id=linked_hypothesis_id,
        evidence_summary=evidence_summary,
        supporting_metrics=_normalize_metadata(supporting_metrics, field_name="supporting_metrics"),
        sample_scope=_normalize_metadata(sample_scope, field_name="sample_scope"),
        related_features=_normalize_string_list(related_features, field_name="related_features"),
        related_horizons=_normalize_string_list(related_horizons, field_name="related_horizons"),
        related_regimes=_normalize_string_list(related_regimes, field_name="related_regimes"),
        limitations=_normalize_string_list(limitations, field_name="limitations"),
        caveats=_normalize_string_list(caveats, field_name="caveats"),
        decision=decision,
        status=status,
        created_at=created_timestamp,
        updated_at=updated_timestamp,
        notes=notes,
    )
    return validate_finding(finding)


def validate_finding(finding: ResearchFinding | Mapping[str, object]) -> ResearchFinding:
    """Validate and normalize a finding record."""

    record = _as_record(finding)
    missing = [field for field in _schema_fields() if field not in record]
    if missing:
        raise ValueError(f"finding missing required fields: {missing}")

    for field in REQUIRED_TEXT_FIELDS:
        _require_non_empty_text(record[field], field_name=field)

    linked_hypothesis_id = record["linked_hypothesis_id"]
    if not isinstance(linked_hypothesis_id, str):
        raise TypeError("linked_hypothesis_id must be a string")

    decision = str(record["decision"])
    if decision not in VALID_DECISIONS:
        raise ValueError(f"invalid finding decision: {decision}")

    status = str(record["status"])
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid finding status: {status}")

    notes = record["notes"]
    if not isinstance(notes, str):
        raise TypeError("notes must be a string")

    created_at = pd.Timestamp(record["created_at"])
    updated_at = pd.Timestamp(record["updated_at"])
    if pd.isna(created_at) or pd.isna(updated_at):
        raise ValueError("created_at and updated_at must be valid timestamps")
    if updated_at < created_at:
        raise ValueError("updated_at must be greater than or equal to created_at")

    normalized_lists = {
        field: _normalize_string_list(record[field], field_name=field) for field in LIST_FIELDS
    }
    if not normalized_lists["limitations"]:
        raise ValueError("limitations must contain at least one limitation")
    if not normalized_lists["caveats"]:
        raise ValueError("caveats must contain at least one caveat")

    return ResearchFinding(
        finding_id=str(record["finding_id"]).strip(),
        title=str(record["title"]).strip(),
        description=str(record["description"]).strip(),
        linked_hypothesis_id=linked_hypothesis_id.strip(),
        evidence_summary=str(record["evidence_summary"]).strip(),
        supporting_metrics=_normalize_metadata(
            record["supporting_metrics"],
            field_name="supporting_metrics",
        ),
        sample_scope=_normalize_metadata(record["sample_scope"], field_name="sample_scope"),
        related_features=normalized_lists["related_features"],
        related_horizons=normalized_lists["related_horizons"],
        related_regimes=normalized_lists["related_regimes"],
        limitations=normalized_lists["limitations"],
        caveats=normalized_lists["caveats"],
        decision=decision,
        status=status,
        created_at=created_at,
        updated_at=updated_at,
        notes=notes.strip(),
    )


def create_registry(findings: Sequence[ResearchFinding | Mapping[str, object]]) -> pd.DataFrame:
    """Create a validated in-memory findings registry DataFrame."""

    validated = [validate_finding(finding) for finding in findings]
    _reject_duplicate_ids(validated)
    return pd.DataFrame([finding_to_record(finding) for finding in validated])


def add_finding(
    registry: pd.DataFrame,
    finding: ResearchFinding | Mapping[str, object],
) -> pd.DataFrame:
    """Return a new registry with one validated finding appended."""

    existing = [validate_finding(record) for record in registry.to_dict(orient="records")]
    candidate = validate_finding(finding)
    return create_registry([*existing, candidate])


def update_finding(
    registry: pd.DataFrame,
    *,
    finding_id: str,
    updates: Mapping[str, object],
) -> pd.DataFrame:
    """Return a new registry with validated updates applied to one finding."""

    if not updates:
        raise ValueError("updates must contain at least one field")
    if "finding_id" in updates and updates["finding_id"] != finding_id:
        raise ValueError("finding_id cannot be changed by update_finding")

    records = registry.to_dict(orient="records")
    match_indexes = [
        index for index, record in enumerate(records) if record.get("finding_id") == finding_id
    ]
    if not match_indexes:
        raise ValueError(f"finding_id not found: {finding_id}")
    if len(match_indexes) > 1:
        raise ValueError(f"duplicate finding_id in registry: {finding_id}")

    index = match_indexes[0]
    updated_record = {**records[index], **dict(updates)}
    if "updated_at" not in updated_record:
        updated_record["updated_at"] = _timestamp_or_now(None)
    records[index] = finding_to_record(validate_finding(updated_record))
    return create_registry(records)


def update_finding_status(
    registry: pd.DataFrame,
    *,
    finding_id: str,
    status: str,
    decision: str | None = None,
    updated_at: object | None = None,
    notes: str | None = None,
) -> pd.DataFrame:
    """Return a new registry with status and optional decision updated."""

    updates: dict[str, object] = {
        "status": status,
        "updated_at": _timestamp_or_now(updated_at),
    }
    if decision is not None:
        updates["decision"] = decision
    if notes is not None:
        updates["notes"] = notes
    return update_finding(registry, finding_id=finding_id, updates=updates)


def finding_to_record(finding: ResearchFinding) -> dict[str, object]:
    """Convert a validated finding to a registry record."""

    record = asdict(finding)
    for field in LIST_FIELDS:
        record[field] = list(record[field])
    return record


def _as_record(finding: ResearchFinding | Mapping[str, object]) -> dict[str, object]:
    if isinstance(finding, ResearchFinding):
        return finding_to_record(finding)
    if isinstance(finding, Mapping):
        return dict(finding)
    raise TypeError("finding must be ResearchFinding or mapping")


def _schema_fields() -> tuple[str, ...]:
    return (
        "finding_id",
        "title",
        "description",
        "linked_hypothesis_id",
        "evidence_summary",
        "supporting_metrics",
        "sample_scope",
        "related_features",
        "related_horizons",
        "related_regimes",
        "limitations",
        "caveats",
        "decision",
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


def _normalize_metadata(value: object, *, field_name: str) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise TypeError(f"{field_name} must be structured mapping metadata")
    if not value:
        raise ValueError(f"{field_name} must not be empty")

    normalized: dict[str, str] = {}
    for key, raw_value in value.items():
        if not isinstance(key, str) or not key.strip():
            raise ValueError(f"{field_name} keys must be non-empty strings")
        if raw_value is None:
            raise ValueError(f"{field_name} values must not be null")
        normalized_value = str(raw_value).strip()
        if not normalized_value:
            raise ValueError(f"{field_name} values must be non-empty")
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


def _reject_duplicate_ids(findings: Sequence[ResearchFinding]) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for finding in findings:
        if finding.finding_id in seen:
            duplicates.add(finding.finding_id)
        seen.add(finding.finding_id)
    if duplicates:
        raise ValueError(f"duplicate finding_id values: {sorted(duplicates)}")
