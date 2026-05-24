from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys

import pytest


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from candidates.candidate_registry import RegistryStatus  # noqa: E402
from mockups.candidate_registry_mockups import FICTITIOUS_REGISTRY_ENTRY  # noqa: E402
from mockups.quality_gate_mockups import (  # noqa: E402
    FICTITIOUS_PASSING_GATE_RESULTS,
    FICTITIOUS_QUALITY_GATE_ASSESSMENT,
    MOCK_QUALITY_ASSESSED_AT,
)
from mockups.strategy_candidate_mockups import FICTITIOUS_STRATEGY_CANDIDATE  # noqa: E402
from quality.quality_gates import (  # noqa: E402
    QualityAssessmentStatus,
    QualityGateType,
    create_quality_gate_assessment,
    create_quality_gate_result,
    validate_quality_gate_assessment,
)


def test_valid_quality_gate_assessment_requires_registered_registry_entry() -> None:
    assessment = create_quality_gate_assessment(
        assessment_id="mock-quality-assessment-valid",
        registry_entry=FICTITIOUS_REGISTRY_ENTRY,
        gate_results=FICTITIOUS_PASSING_GATE_RESULTS,
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        non_approval_statement="Synthetic non-approval statement.",
        audit_reference="mock-audit-quality-assessment-valid",
        assessed_at=MOCK_QUALITY_ASSESSED_AT,
    )

    assert assessment.registry_entry is FICTITIOUS_REGISTRY_ENTRY
    assert (
        assessment.assessment_status
        is QualityAssessmentStatus.PASSED_PENDING_STRATEGY_CLOSURE
    )


def test_non_registry_entry_origin_is_rejected() -> None:
    with pytest.raises(ValueError, match="valid registry entry"):
        create_quality_gate_assessment(
            assessment_id="mock-quality-assessment-bad-origin",
            registry_entry=FICTITIOUS_STRATEGY_CANDIDATE,
            gate_results=FICTITIOUS_PASSING_GATE_RESULTS,
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-quality-assessment-bad-origin",
        )


def test_registry_entry_must_be_pending_quality_gates() -> None:
    invalid_entry = replace(
        FICTITIOUS_REGISTRY_ENTRY,
        registry_status="registered_pending_quality_gates",
    )

    with pytest.raises(TypeError, match="registry_status must be a RegistryStatus"):
        create_quality_gate_assessment(
            assessment_id="mock-quality-assessment-bad-status",
            registry_entry=invalid_entry,
            gate_results=FICTITIOUS_PASSING_GATE_RESULTS,
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-quality-assessment-bad-status",
        )


def test_all_required_quality_gate_types_are_required() -> None:
    missing_one_gate = tuple(
        result
        for result in FICTITIOUS_PASSING_GATE_RESULTS
        if result.gate_type is not QualityGateType.FALSIFICATION_READINESS
    )

    with pytest.raises(ValueError, match="missing required quality gate types"):
        create_quality_gate_assessment(
            assessment_id="mock-quality-assessment-missing-gate",
            registry_entry=FICTITIOUS_REGISTRY_ENTRY,
            gate_results=missing_one_gate,
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-quality-assessment-missing-gate",
        )


def test_failed_gate_derives_revision_status() -> None:
    failed_gate = create_quality_gate_result(
        gate_id="mock-quality-gate-failed-traceability",
        gate_type=QualityGateType.TRACEABILITY,
        passed=False,
        assessment_summary="Synthetic failure; traceability needs revision.",
        limitations=("Synthetic limitation.",),
        audit_reference="mock-audit-quality-gate-failed-traceability",
    )
    gate_results = (
        failed_gate,
        *(
            result
            for result in FICTITIOUS_PASSING_GATE_RESULTS
            if result.gate_type is not QualityGateType.TRACEABILITY
        ),
    )

    assessment = create_quality_gate_assessment(
        assessment_id="mock-quality-assessment-failed",
        registry_entry=FICTITIOUS_REGISTRY_ENTRY,
        gate_results=gate_results,
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        non_approval_statement="Synthetic non-approval statement.",
        audit_reference="mock-audit-quality-assessment-failed",
    )

    assert assessment.assessment_status is QualityAssessmentStatus.FAILED_REQUIRES_REVISION


def test_manual_assessment_status_override_is_rejected() -> None:
    manipulated_assessment = replace(
        FICTITIOUS_QUALITY_GATE_ASSESSMENT,
        assessment_status=QualityAssessmentStatus.FAILED_REQUIRES_REVISION,
    )

    with pytest.raises(ValueError, match="assessment_status must be derived from gate_results"):
        validate_quality_gate_assessment(manipulated_assessment)


def test_quality_gate_result_rejects_non_quality_gate_type() -> None:
    with pytest.raises(TypeError, match="gate_type must be a QualityGateType"):
        create_quality_gate_result(
            gate_id="mock-quality-gate-bad-type",
            gate_type="performance",
            passed=True,
            assessment_summary="Synthetic bad gate type.",
            limitations=("Synthetic limitation.",),
            audit_reference="mock-audit-quality-gate-bad-type",
        )


def test_quality_assessment_required_governance_fields_are_enforced() -> None:
    with pytest.raises(ValueError, match="assumptions must contain at least one item"):
        create_quality_gate_assessment(
            assessment_id="mock-quality-assessment-missing-assumptions",
            registry_entry=FICTITIOUS_REGISTRY_ENTRY,
            gate_results=FICTITIOUS_PASSING_GATE_RESULTS,
            assumptions=(),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-quality-assessment-missing-assumptions",
        )

    with pytest.raises(ValueError, match="limitations must contain at least one item"):
        create_quality_gate_assessment(
            assessment_id="mock-quality-assessment-missing-limitations",
            registry_entry=FICTITIOUS_REGISTRY_ENTRY,
            gate_results=FICTITIOUS_PASSING_GATE_RESULTS,
            assumptions=("Synthetic assumption.",),
            limitations=(),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-quality-assessment-missing-limitations",
        )

    with pytest.raises(ValueError, match="non_approval_statement must be a non-empty string"):
        create_quality_gate_assessment(
            assessment_id="mock-quality-assessment-missing-non-approval",
            registry_entry=FICTITIOUS_REGISTRY_ENTRY,
            gate_results=FICTITIOUS_PASSING_GATE_RESULTS,
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="",
            audit_reference="mock-audit-quality-assessment-missing-non-approval",
        )


def test_quality_gate_assessment_is_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        FICTITIOUS_QUALITY_GATE_ASSESSMENT.assessment_status = (
            QualityAssessmentStatus.FAILED_REQUIRES_REVISION
        )


def test_quality_gate_assessment_preserves_registry_traceability() -> None:
    assessment = FICTITIOUS_QUALITY_GATE_ASSESSMENT

    assert assessment.registry_entry.source_hypothesis_ids
    assert assessment.registry_entry.signal_ids
    assert assessment.registry_entry.regime_frame_ids
    assert assessment.registry_entry.rule_ids
    assert (
        assessment.registry_entry.registry_status
        is RegistryStatus.REGISTERED_PENDING_QUALITY_GATES
    )


def test_quality_gate_assessment_does_not_expose_closure_handoff_or_performance_fields() -> None:
    assessment = FICTITIOUS_QUALITY_GATE_ASSESSMENT

    assert not hasattr(assessment, "closure_status")
    assert not hasattr(assessment, "dossier_ready")
    assert not hasattr(assessment, "backtest_result")
    assert not hasattr(assessment, "pnl")
    assert not hasattr(assessment, "drawdown")
    assert not hasattr(assessment, "hit_rate")
    assert not hasattr(assessment, "sharpe")
    assert not hasattr(assessment, "sortino")
    assert not hasattr(assessment, "calmar")
    assert not hasattr(assessment, "position_size")
    assert not hasattr(assessment, "order")
    assert not hasattr(assessment, "execution")
