from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys

import pytest


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from mockups.quality_gate_mockups import (  # noqa: E402
    FICTITIOUS_PASSING_GATE_RESULTS,
    FICTITIOUS_QUALITY_GATE_ASSESSMENT,
)
from mockups.strategy_candidate_mockups import FICTITIOUS_STRATEGY_CANDIDATE  # noqa: E402
from mockups.strategy_closure_mockups import (  # noqa: E402
    FICTITIOUS_STRATEGY_CLOSURE_RECORD,
    MOCK_STRATEGY_CLOSURE_CLOSED_AT,
)
from quality.quality_gates import (  # noqa: E402
    QualityAssessmentStatus,
    QualityGateType,
    create_quality_gate_assessment,
    create_quality_gate_result,
)
from reports.strategy_closure import (  # noqa: E402
    StrategyClosureStatus,
    create_strategy_closure_record,
    validate_strategy_closure_record,
)


def test_valid_strategy_closure_requires_passing_quality_assessment() -> None:
    record = create_strategy_closure_record(
        closure_id="mock-strategy-closure-valid",
        quality_assessment=FICTITIOUS_QUALITY_GATE_ASSESSMENT,
        closure_summary="Synthetic closure summary.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        non_approval_statement="Synthetic non-approval statement.",
        audit_reference="mock-audit-strategy-closure-valid",
        closed_at=MOCK_STRATEGY_CLOSURE_CLOSED_AT,
    )

    assert record.quality_assessment is FICTITIOUS_QUALITY_GATE_ASSESSMENT
    assert record.closure_status is StrategyClosureStatus.CLOSED_PENDING_DOSSIER_HANDOFF
    assert record.candidate_id == (
        FICTITIOUS_QUALITY_GATE_ASSESSMENT
        .registry_entry
        .strategy_candidate
        .candidate_id
    )


def test_non_quality_assessment_origin_is_rejected() -> None:
    with pytest.raises(ValueError, match="valid quality assessment"):
        create_strategy_closure_record(
            closure_id="mock-strategy-closure-bad-origin",
            quality_assessment=FICTITIOUS_STRATEGY_CANDIDATE,
            closure_summary="Synthetic closure summary.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-strategy-closure-bad-origin",
        )


def test_failed_quality_assessment_is_rejected_for_closure() -> None:
    failed_gate = create_quality_gate_result(
        gate_id="mock-closure-failed-quality-gate",
        gate_type=QualityGateType.TRACEABILITY,
        passed=False,
        assessment_summary="Synthetic failed gate.",
        limitations=("Synthetic limitation.",),
        audit_reference="mock-audit-closure-failed-quality-gate",
    )
    failed_assessment = create_quality_gate_assessment(
        assessment_id="mock-quality-assessment-for-rejected-closure",
        registry_entry=FICTITIOUS_QUALITY_GATE_ASSESSMENT.registry_entry,
        gate_results=(
            failed_gate,
            *(
                result
                for result in FICTITIOUS_PASSING_GATE_RESULTS
                if result.gate_type is not QualityGateType.TRACEABILITY
            ),
        ),
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        non_approval_statement="Synthetic non-approval statement.",
        audit_reference="mock-audit-quality-assessment-for-rejected-closure",
    )

    assert failed_assessment.assessment_status is QualityAssessmentStatus.FAILED_REQUIRES_REVISION
    with pytest.raises(ValueError, match="passed_pending_strategy_closure"):
        create_strategy_closure_record(
            closure_id="mock-strategy-closure-failed-assessment",
            quality_assessment=failed_assessment,
            closure_summary="Synthetic closure summary.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-strategy-closure-failed-assessment",
        )


def test_strategy_closure_rejects_manual_traceability_mismatch() -> None:
    manipulated_record = replace(
        FICTITIOUS_STRATEGY_CLOSURE_RECORD,
        candidate_id="mock-wrong-candidate",
    )

    with pytest.raises(ValueError, match="candidate_id must match"):
        validate_strategy_closure_record(manipulated_record)


def test_strategy_closure_required_governance_fields_are_enforced() -> None:
    with pytest.raises(ValueError, match="assumptions must contain at least one item"):
        create_strategy_closure_record(
            closure_id="mock-strategy-closure-missing-assumptions",
            quality_assessment=FICTITIOUS_QUALITY_GATE_ASSESSMENT,
            closure_summary="Synthetic closure summary.",
            assumptions=(),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-strategy-closure-missing-assumptions",
        )

    with pytest.raises(ValueError, match="limitations must contain at least one item"):
        create_strategy_closure_record(
            closure_id="mock-strategy-closure-missing-limitations",
            quality_assessment=FICTITIOUS_QUALITY_GATE_ASSESSMENT,
            closure_summary="Synthetic closure summary.",
            assumptions=("Synthetic assumption.",),
            limitations=(),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-strategy-closure-missing-limitations",
        )

    with pytest.raises(ValueError, match="non_approval_statement must be a non-empty string"):
        create_strategy_closure_record(
            closure_id="mock-strategy-closure-missing-non-approval",
            quality_assessment=FICTITIOUS_QUALITY_GATE_ASSESSMENT,
            closure_summary="Synthetic closure summary.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="",
            audit_reference="mock-audit-strategy-closure-missing-non-approval",
        )


def test_strategy_closure_preserves_upstream_traceability_and_falsification() -> None:
    record = FICTITIOUS_STRATEGY_CLOSURE_RECORD
    registry_entry = record.quality_assessment.registry_entry
    rule = registry_entry.strategy_candidate.rule_definitions[0]

    assert record.registry_entry_id == registry_entry.entry_id
    assert record.quality_assessment_id == record.quality_assessment.assessment_id
    assert record.source_hypothesis_ids == registry_entry.source_hypothesis_ids
    assert record.signal_ids == registry_entry.signal_ids
    assert record.regime_frame_ids == registry_entry.regime_frame_ids
    assert record.rule_ids == registry_entry.rule_ids
    assert rule.signal_definition.falsification_references[0] in record.upstream_falsification_references
    assert rule.regime_context_frame.falsification_references[0] in record.upstream_falsification_references
    assert rule.falsification_references[0] in record.upstream_falsification_references
    assert registry_entry.falsification_references[0] in record.upstream_falsification_references
    assert (
        registry_entry.strategy_candidate.falsification_references[0]
        in record.upstream_falsification_references
    )
    assert (
        registry_entry.risk_template.falsification_references[0]
        in record.upstream_falsification_references
    )


def test_strategy_closure_record_is_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        FICTITIOUS_STRATEGY_CLOSURE_RECORD.closure_status = (
            StrategyClosureStatus.CLOSED_PENDING_DOSSIER_HANDOFF
        )


def test_unsupported_closure_status_is_rejected() -> None:
    with pytest.raises(TypeError, match="closure_status must be a StrategyClosureStatus"):
        create_strategy_closure_record(
            closure_id="mock-strategy-closure-bad-status",
            quality_assessment=FICTITIOUS_QUALITY_GATE_ASSESSMENT,
            closure_summary="Synthetic closure summary.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-strategy-closure-bad-status",
            closure_status="closed_pending_dossier_handoff",
        )


def test_strategy_closure_does_not_expose_handoff_backtest_or_performance_fields() -> None:
    record = FICTITIOUS_STRATEGY_CLOSURE_RECORD

    assert not hasattr(record, "dossier")
    assert not hasattr(record, "dossier_ready")
    assert not hasattr(record, "handoff_status")
    assert not hasattr(record, "backtest_result")
    assert not hasattr(record, "pnl")
    assert not hasattr(record, "drawdown")
    assert not hasattr(record, "hit_rate")
    assert not hasattr(record, "sharpe")
    assert not hasattr(record, "sortino")
    assert not hasattr(record, "calmar")
    assert not hasattr(record, "position_size")
    assert not hasattr(record, "order")
    assert not hasattr(record, "execution")
