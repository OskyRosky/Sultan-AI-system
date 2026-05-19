from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pandas as pd


MODULE_PATH = Path(__file__).resolve().parents[1] / "research" / "research_quality.py"
SPEC = importlib.util.spec_from_file_location("research_quality", MODULE_PATH)
research_quality = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = research_quality
SPEC.loader.exec_module(research_quality)


def _finding(**overrides: object) -> dict[str, object]:
    record: dict[str, object] = {
        "finding_id": "FIND-001",
        "title": "Synthetic finding",
        "description": "Synthetic finding for quality tests.",
        "linked_hypothesis_id": "HYP-001",
        "evidence_summary": "Structured synthetic evidence.",
        "supporting_metrics": {
            "sample_count": "120",
            "pearson_ic": "0.08",
            "nan_ratio": "0.05",
            "regime_concentration": "0.50",
            "period_concentration": "0.40",
            "min_regime_sample_count": "25",
            "temporal_stability": "stable",
            "ic_type": "time_series",
            "multiple_testing_control": "documented",
        },
        "sample_scope": {"symbol": "BTCUSDT", "timeframe": "1h", "period": "synthetic"},
        "limitations": ["Synthetic fixture only."],
        "caveats": ["No causal claim."],
        "status": "under_review",
    }
    record.update(overrides)
    return record


def _hypothesis(**overrides: object) -> dict[str, object]:
    record: dict[str, object] = {
        "hypothesis_id": "HYP-001",
        "status": "proposed",
        "assumptions": ["Feature definitions are stable."],
        "falsification_conditions": ["Fails temporal validation."],
    }
    record.update(overrides)
    return record


def test_sample_insufficiency_returns_insufficient_evidence() -> None:
    finding = _finding(supporting_metrics={**_finding()["supporting_metrics"], "sample_count": "12"})

    result = research_quality.evaluate_finding_quality(finding)

    assert result.quality_status == "insufficient_evidence"
    assert "insufficient_sample_count" in result.failed_checks


def test_weak_ic_warning() -> None:
    finding = _finding(supporting_metrics={**_finding()["supporting_metrics"], "pearson_ic": "0.01"})

    result = research_quality.evaluate_finding_quality(finding)

    assert result.quality_status == "warning"
    assert "weak_ic" in result.warnings


def test_missing_caveats_fail_governance() -> None:
    result = research_quality.evaluate_finding_quality(_finding(caveats=[]))

    assert result.quality_status == "fail"
    assert "missing_caveats" in result.failed_checks


def test_missing_limitations_fail_governance() -> None:
    result = research_quality.evaluate_finding_quality(_finding(limitations=[]))

    assert result.quality_status == "fail"
    assert "missing_limitations" in result.failed_checks


def test_regime_concentration_warning() -> None:
    finding = _finding(
        supporting_metrics={**_finding()["supporting_metrics"], "regime_concentration": "0.95"}
    )

    result = research_quality.evaluate_finding_quality(finding)

    assert result.quality_status == "warning"
    assert "regime_concentration" in result.warnings


def test_temporal_instability_warning() -> None:
    finding = _finding(
        supporting_metrics={
            **_finding()["supporting_metrics"],
            "temporal_stability": "unstable",
            "period_concentration": "0.90",
        }
    )

    result = research_quality.evaluate_finding_quality(finding)

    assert "temporal_instability" in result.warnings
    assert "period_concentration" in result.warnings


def test_missing_temporal_stability_assessment_warning() -> None:
    metrics = dict(_finding()["supporting_metrics"])
    del metrics["temporal_stability"]

    result = research_quality.evaluate_finding_quality(_finding(supporting_metrics=metrics))

    assert "missing_temporal_stability_assessment" in result.warnings


def test_missing_regime_concentration_warning() -> None:
    metrics = dict(_finding()["supporting_metrics"])
    del metrics["regime_concentration"]

    result = research_quality.evaluate_finding_quality(_finding(supporting_metrics=metrics))

    assert "missing_regime_concentration" in result.warnings


def test_missing_period_concentration_warning() -> None:
    metrics = dict(_finding()["supporting_metrics"])
    del metrics["period_concentration"]

    result = research_quality.evaluate_finding_quality(_finding(supporting_metrics=metrics))

    assert "missing_period_concentration" in result.warnings


def test_invalid_finding_status_fails() -> None:
    result = research_quality.evaluate_finding_quality(_finding(status="alpha_confirmed"))

    assert result.quality_status == "fail"
    assert "invalid_finding_status" in result.failed_checks


def test_pass_warning_fail_transitions() -> None:
    passing = research_quality.evaluate_finding_quality(_finding())
    warning = research_quality.evaluate_finding_quality(
        _finding(supporting_metrics={**_finding()["supporting_metrics"], "nan_ratio": "0.40"})
    )
    failing = research_quality.evaluate_finding_quality(_finding(sample_scope={}))

    assert passing.quality_status == "pass"
    assert warning.quality_status == "warning"
    assert "excessive_nan_ratio" in warning.warnings
    assert failing.quality_status == "fail"
    assert "missing_sample_scope" in failing.failed_checks


def test_empty_finding_fails_required_checks() -> None:
    result = research_quality.evaluate_finding_quality({})

    assert result.quality_status == "fail"
    assert "missing_finding_id" in result.failed_checks
    assert "missing_supporting_metrics" in result.failed_checks


def test_hypothesis_governance_failures() -> None:
    result = research_quality.evaluate_hypothesis_quality(
        _hypothesis(status="approved_for_trading", falsification_conditions=[])
    )

    assert result.quality_status == "fail"
    assert "invalid_hypothesis_status" in result.failed_checks
    assert "missing_falsification_conditions" in result.failed_checks


def test_pooled_only_warning() -> None:
    finding = _finding(supporting_metrics={**_finding()["supporting_metrics"], "ic_type": "pooled"})

    result = research_quality.evaluate_finding_quality(finding)

    assert result.quality_status == "warning"
    assert "pooled_only_ic" in result.warnings


def test_nan_heavy_evidence_warning() -> None:
    finding = _finding(supporting_metrics={**_finding()["supporting_metrics"], "nan_ratio": "0.85"})

    result = research_quality.evaluate_finding_quality(finding)

    assert "excessive_nan_ratio" in result.warnings


def test_sparse_regime_evidence_warning() -> None:
    finding = _finding(
        supporting_metrics={**_finding()["supporting_metrics"], "min_regime_sample_count": "3"}
    )

    result = research_quality.evaluate_finding_quality(finding)

    assert "sparse_regime_evidence" in result.warnings


def test_missing_metrics_warning() -> None:
    metrics = {"sample_count": "120", "nan_ratio": "0.01"}
    result = research_quality.evaluate_finding_quality(_finding(supporting_metrics=metrics))

    assert "missing_ic_metric" in result.warnings
    assert "missing_multiple_testing_control" in result.warnings
    assert "missing_temporal_stability_assessment" in result.warnings
    assert "missing_regime_concentration" in result.warnings
    assert "missing_period_concentration" in result.warnings


def test_results_to_frame_preserves_audit_fields() -> None:
    result = research_quality.evaluate_finding_quality(
        _finding(),
        reviewer_notes="Manual review required before future promotion.",
        evaluated_at="2026-03-01T00:00:00Z",
    )

    frame = research_quality.results_to_frame([result])

    assert frame.iloc[0]["quality_status"] == "pass"
    assert frame.iloc[0]["reviewer_notes"] == "Manual review required before future promotion."
    assert frame.iloc[0]["evaluated_at"] == pd.Timestamp("2026-03-01T00:00:00Z")
