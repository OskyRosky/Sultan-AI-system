from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd
import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "research" / "findings_registry.py"
SPEC = importlib.util.spec_from_file_location("findings_registry", MODULE_PATH)
findings_registry = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = findings_registry
SPEC.loader.exec_module(findings_registry)


def _valid_finding(**overrides: object) -> dict[str, object]:
    record: dict[str, object] = {
        "finding_id": "FIND-001",
        "title": "RSI bucket behavior differs in synthetic fixture",
        "description": "Human-reviewed synthetic finding for registry validation.",
        "linked_hypothesis_id": "HYP-001",
        "evidence_summary": "Synthetic evidence summary for schema validation only.",
        "supporting_metrics": {
            "metric_family": "bucket_analysis",
            "sample_count": "120",
            "horizon": "forward_return_1",
        },
        "sample_scope": {
            "symbol": "BTCUSDT",
            "timeframe": "1h",
            "start": "2026-01-01",
            "end": "2026-01-31",
        },
        "related_features": ["rsi_14"],
        "related_horizons": ["forward_return_1"],
        "related_regimes": ["trend:bullish"],
        "limitations": ["Synthetic fixture only.", "No multiple testing correction."],
        "caveats": ["No causal claim.", "No strategy implication."],
        "decision": "defer",
        "status": "draft",
        "created_at": "2026-02-01T00:00:00Z",
        "updated_at": "2026-02-01T00:00:00Z",
        "notes": "No real finding; synthetic registry test.",
    }
    record.update(overrides)
    return record


def test_create_valid_finding() -> None:
    finding = findings_registry.create_finding(**_valid_finding())

    assert finding.finding_id == "FIND-001"
    assert finding.linked_hypothesis_id == "HYP-001"
    assert finding.decision == "defer"
    assert finding.status == "draft"


def test_registry_validates_schema_and_returns_dataframe() -> None:
    registry = findings_registry.create_registry([_valid_finding()])

    assert registry.shape[0] == 1
    assert registry.iloc[0]["finding_id"] == "FIND-001"
    assert registry.iloc[0]["limitations"] == [
        "Synthetic fixture only.",
        "No multiple testing correction.",
    ]


def test_duplicate_finding_id_is_rejected() -> None:
    with pytest.raises(ValueError, match="duplicate finding_id"):
        findings_registry.create_registry([_valid_finding(), _valid_finding()])


def test_invalid_status_is_rejected() -> None:
    with pytest.raises(ValueError, match="invalid finding status"):
        findings_registry.validate_finding(_valid_finding(status="alpha_confirmed"))


def test_invalid_decision_is_rejected() -> None:
    with pytest.raises(ValueError, match="invalid finding decision"):
        findings_registry.validate_finding(_valid_finding(decision="trade"))


def test_missing_required_fields_are_rejected() -> None:
    record = _valid_finding()
    del record["evidence_summary"]

    with pytest.raises(ValueError, match="missing required fields"):
        findings_registry.validate_finding(record)


def test_lifecycle_status_and_decision_update_is_validated() -> None:
    registry = findings_registry.create_registry([_valid_finding()])

    updated = findings_registry.update_finding_status(
        registry,
        finding_id="FIND-001",
        status="promoted_to_quality_review",
        decision="advance_to_quality_review",
        updated_at="2026-02-02T00:00:00Z",
        notes="Ready for quality gate review.",
    )

    assert updated.iloc[0]["status"] == "promoted_to_quality_review"
    assert updated.iloc[0]["decision"] == "advance_to_quality_review"
    assert updated.iloc[0]["notes"] == "Ready for quality gate review."
    assert updated.iloc[0]["updated_at"] == pd.Timestamp("2026-02-02T00:00:00Z")


def test_update_rejects_unknown_finding_id() -> None:
    registry = findings_registry.create_registry([_valid_finding()])

    with pytest.raises(ValueError, match="finding_id not found"):
        findings_registry.update_finding(
            registry,
            finding_id="FIND-404",
            updates={"status": "rejected", "updated_at": "2026-02-02T00:00:00Z"},
        )


def test_supporting_metrics_must_be_structured_metadata() -> None:
    with pytest.raises(TypeError, match="supporting_metrics"):
        findings_registry.validate_finding(
            _valid_finding(supporting_metrics="not-structured")
        )

    with pytest.raises(ValueError, match="supporting_metrics must not be empty"):
        findings_registry.validate_finding(_valid_finding(supporting_metrics={}))


def test_sample_scope_is_required_structured_metadata() -> None:
    with pytest.raises(ValueError, match="sample_scope must not be empty"):
        findings_registry.validate_finding(_valid_finding(sample_scope={}))


def test_limitations_are_required() -> None:
    with pytest.raises(ValueError, match="limitations"):
        findings_registry.validate_finding(_valid_finding(limitations=[]))


def test_caveats_are_required() -> None:
    with pytest.raises(ValueError, match="caveats"):
        findings_registry.validate_finding(_valid_finding(caveats=[]))


def test_empty_finding_text_is_rejected() -> None:
    with pytest.raises(ValueError, match="title must be non-empty text"):
        findings_registry.validate_finding(_valid_finding(title=" "))


def test_decisions_that_imply_trading_are_rejected() -> None:
    for decision in ("buy", "sell", "deploy", "live", "production_ready"):
        with pytest.raises(ValueError, match="invalid finding decision"):
            findings_registry.validate_finding(_valid_finding(decision=decision))


def test_updated_at_cannot_precede_created_at() -> None:
    with pytest.raises(ValueError, match="updated_at must be greater than or equal"):
        findings_registry.validate_finding(
            _valid_finding(
                created_at="2026-02-02T00:00:00Z",
                updated_at="2026-02-01T00:00:00Z",
            )
        )


def test_add_finding_returns_new_registry_without_mutating_input() -> None:
    registry = findings_registry.create_registry([_valid_finding()])
    second = _valid_finding(
        finding_id="FIND-002",
        title="Second synthetic finding",
        created_at="2026-02-03T00:00:00Z",
        updated_at="2026-02-03T00:00:00Z",
    )

    updated = findings_registry.add_finding(registry, second)

    assert registry.shape[0] == 1
    assert updated.shape[0] == 2
    assert set(updated["finding_id"]) == {"FIND-001", "FIND-002"}
