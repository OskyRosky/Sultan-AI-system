from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "research" / "hypothesis_registry.py"
SPEC = importlib.util.spec_from_file_location("hypothesis_registry", MODULE_PATH)
hypothesis_registry = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = hypothesis_registry
SPEC.loader.exec_module(hypothesis_registry)


def _valid_hypothesis(**overrides: object) -> dict[str, object]:
    record: dict[str, object] = {
        "hypothesis_id": "HYP-001",
        "title": "RSI dispersion may relate to short horizon returns",
        "description": "Human-authored candidate hypothesis for registry validation.",
        "rationale": "Observed research metrics suggest a relationship worth human review.",
        "related_features": ["rsi_14", "rsi_zscore_20"],
        "related_horizons": ["forward_return_1", "forward_return_3"],
        "related_regimes": ["trend:bullish"],
        "evidence_summary": "Synthetic evidence summary for schema validation only.",
        "evidence_source": {
            "artifact": "synthetic_test_fixture",
            "block": "block_8",
            "methodology": "manual_candidate",
        },
        "assumptions": ["Feature definitions are stable.", "Forward returns are aligned."],
        "falsification_conditions": [
            "Relationship disappears under temporal validation.",
            "Effect is concentrated in one small regime segment.",
        ],
        "status": "draft",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
        "notes": "No real hypothesis; synthetic registry test.",
    }
    record.update(overrides)
    return record


def test_create_valid_hypothesis() -> None:
    hypothesis = hypothesis_registry.create_hypothesis(**_valid_hypothesis())

    assert hypothesis.hypothesis_id == "HYP-001"
    assert hypothesis.status == "draft"
    assert hypothesis.related_features == ("rsi_14", "rsi_zscore_20")
    assert hypothesis.evidence_source["artifact"] == "synthetic_test_fixture"


def test_registry_validates_schema_and_returns_dataframe() -> None:
    registry = hypothesis_registry.create_registry([_valid_hypothesis()])

    assert registry.shape[0] == 1
    assert registry.iloc[0]["hypothesis_id"] == "HYP-001"
    assert registry.iloc[0]["falsification_conditions"] == [
        "Relationship disappears under temporal validation.",
        "Effect is concentrated in one small regime segment.",
    ]


def test_duplicate_hypothesis_id_is_rejected() -> None:
    with pytest.raises(ValueError, match="duplicate hypothesis_id"):
        hypothesis_registry.create_registry([_valid_hypothesis(), _valid_hypothesis()])


def test_invalid_status_is_rejected() -> None:
    with pytest.raises(ValueError, match="invalid hypothesis status"):
        hypothesis_registry.validate_hypothesis(
            _valid_hypothesis(status="approved_for_trading")
        )


def test_missing_required_fields_are_rejected() -> None:
    record = _valid_hypothesis()
    del record["rationale"]

    with pytest.raises(ValueError, match="missing required fields"):
        hypothesis_registry.validate_hypothesis(record)


def test_lifecycle_status_update_is_validated() -> None:
    registry = hypothesis_registry.create_registry([_valid_hypothesis()])

    updated = hypothesis_registry.update_hypothesis_status(
        registry,
        hypothesis_id="HYP-001",
        status="proposed",
        updated_at="2026-01-02T00:00:00Z",
        notes="Moved to human review queue.",
    )

    assert updated.iloc[0]["status"] == "proposed"
    assert updated.iloc[0]["notes"] == "Moved to human review queue."
    assert updated.iloc[0]["updated_at"] == pd.Timestamp("2026-01-02T00:00:00Z")


def test_update_preserves_schema_and_rejects_unknown_hypothesis_id() -> None:
    registry = hypothesis_registry.create_registry([_valid_hypothesis()])

    with pytest.raises(ValueError, match="hypothesis_id not found"):
        hypothesis_registry.update_hypothesis(
            registry,
            hypothesis_id="HYP-404",
            updates={"status": "rejected", "updated_at": "2026-01-02T00:00:00Z"},
        )


def test_falsification_conditions_are_required() -> None:
    with pytest.raises(ValueError, match="falsification_conditions"):
        hypothesis_registry.validate_hypothesis(
            _valid_hypothesis(falsification_conditions=[])
        )


def test_evidence_metadata_must_be_consistent_mapping() -> None:
    with pytest.raises(TypeError, match="evidence_source"):
        hypothesis_registry.validate_hypothesis(
            _valid_hypothesis(evidence_source="not-structured")
        )

    with pytest.raises(ValueError, match="evidence_source must not be empty"):
        hypothesis_registry.validate_hypothesis(_valid_hypothesis(evidence_source={}))


def test_empty_hypothesis_text_is_rejected() -> None:
    with pytest.raises(ValueError, match="title must be non-empty text"):
        hypothesis_registry.validate_hypothesis(_valid_hypothesis(title=" "))


def test_list_fields_must_contain_non_empty_strings() -> None:
    with pytest.raises(ValueError, match="related_features"):
        hypothesis_registry.validate_hypothesis(
            _valid_hypothesis(related_features=["rsi_14", " "])
        )


def test_updated_at_cannot_precede_created_at() -> None:
    with pytest.raises(ValueError, match="updated_at must be greater than or equal"):
        hypothesis_registry.validate_hypothesis(
            _valid_hypothesis(
                created_at="2026-01-02T00:00:00Z",
                updated_at="2026-01-01T00:00:00Z",
            )
        )


def test_add_hypothesis_returns_new_registry_without_mutating_input() -> None:
    registry = hypothesis_registry.create_registry([_valid_hypothesis()])
    second = _valid_hypothesis(
        hypothesis_id="HYP-002",
        title="Second synthetic hypothesis",
        created_at="2026-01-03T00:00:00Z",
        updated_at="2026-01-03T00:00:00Z",
    )

    updated = hypothesis_registry.add_hypothesis(registry, second)

    assert registry.shape[0] == 1
    assert updated.shape[0] == 2
    assert set(updated["hypothesis_id"]) == {"HYP-001", "HYP-002"}
