from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys

import pytest


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from mockups.strategy_candidate_mockups import FICTITIOUS_STRATEGY_CANDIDATE  # noqa: E402
from mockups.strategy_closure_mockups import FICTITIOUS_STRATEGY_CLOSURE_RECORD  # noqa: E402
from mockups.strategy_dossier_mockups import (  # noqa: E402
    FICTITIOUS_DOSSIER_SECTIONS,
    FICTITIOUS_STRATEGY_DOSSIER,
    MOCK_STRATEGY_DOSSIER_PREPARED_AT,
)
from reports.strategy_dossier import (  # noqa: E402
    DossierHandoffStatus,
    DossierSectionType,
    create_dossier_section,
    create_strategy_dossier,
    validate_strategy_dossier,
)


def test_valid_strategy_dossier_requires_closure_record() -> None:
    dossier = create_strategy_dossier(
        dossier_id="mock-strategy-dossier-valid",
        closure_record=FICTITIOUS_STRATEGY_CLOSURE_RECORD,
        sections=FICTITIOUS_DOSSIER_SECTIONS,
        downstream_review_questions=("Synthetic downstream question.",),
        pending_requirements=("Synthetic pending requirement.",),
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        non_approval_statement="Synthetic non-approval statement.",
        audit_reference="mock-audit-strategy-dossier-valid",
        prepared_at=MOCK_STRATEGY_DOSSIER_PREPARED_AT,
    )

    assert dossier.closure_record is FICTITIOUS_STRATEGY_CLOSURE_RECORD
    assert (
        dossier.handoff_status
        is DossierHandoffStatus.DOSSIER_PREPARED_PENDING_FINAL_AUDIT
    )
    assert dossier.candidate_id == FICTITIOUS_STRATEGY_CLOSURE_RECORD.candidate_id


def test_non_closure_origin_is_rejected() -> None:
    with pytest.raises(ValueError, match="valid closure record"):
        create_strategy_dossier(
            dossier_id="mock-strategy-dossier-bad-origin",
            closure_record=FICTITIOUS_STRATEGY_CANDIDATE,
            sections=FICTITIOUS_DOSSIER_SECTIONS,
            downstream_review_questions=("Synthetic downstream question.",),
            pending_requirements=("Synthetic pending requirement.",),
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-strategy-dossier-bad-origin",
        )


def test_all_required_dossier_sections_are_required() -> None:
    missing_one_section = tuple(
        section
        for section in FICTITIOUS_DOSSIER_SECTIONS
        if section.section_type is not DossierSectionType.NON_APPROVAL_SCOPE
    )

    with pytest.raises(ValueError, match="missing required dossier section types"):
        create_strategy_dossier(
            dossier_id="mock-strategy-dossier-missing-section",
            closure_record=FICTITIOUS_STRATEGY_CLOSURE_RECORD,
            sections=missing_one_section,
            downstream_review_questions=("Synthetic downstream question.",),
            pending_requirements=("Synthetic pending requirement.",),
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-strategy-dossier-missing-section",
        )


def test_duplicate_dossier_section_types_are_rejected() -> None:
    duplicate_section = create_dossier_section(
        section_id="mock-dossier-section-duplicate",
        section_type=FICTITIOUS_DOSSIER_SECTIONS[0].section_type,
        title="Synthetic Duplicate Section",
        content_summary="Synthetic duplicate section.",
        audit_reference="mock-audit-dossier-section-duplicate",
    )

    with pytest.raises(ValueError, match="duplicate section_type"):
        create_strategy_dossier(
            dossier_id="mock-strategy-dossier-duplicate-section",
            closure_record=FICTITIOUS_STRATEGY_CLOSURE_RECORD,
            sections=(*FICTITIOUS_DOSSIER_SECTIONS, duplicate_section),
            downstream_review_questions=("Synthetic downstream question.",),
            pending_requirements=("Synthetic pending requirement.",),
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-strategy-dossier-duplicate-section",
        )


def test_strategy_dossier_rejects_manual_traceability_mismatch() -> None:
    manipulated_dossier = replace(
        FICTITIOUS_STRATEGY_DOSSIER,
        candidate_id="mock-wrong-candidate",
    )

    with pytest.raises(ValueError, match="candidate_id must match"):
        validate_strategy_dossier(manipulated_dossier)


def test_unsupported_handoff_status_is_rejected() -> None:
    with pytest.raises(TypeError, match="handoff_status must be a DossierHandoffStatus"):
        create_strategy_dossier(
            dossier_id="mock-strategy-dossier-bad-status",
            closure_record=FICTITIOUS_STRATEGY_CLOSURE_RECORD,
            sections=FICTITIOUS_DOSSIER_SECTIONS,
            downstream_review_questions=("Synthetic downstream question.",),
            pending_requirements=("Synthetic pending requirement.",),
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-strategy-dossier-bad-status",
            handoff_status="dossier_prepared_pending_final_audit",
        )


def test_strategy_dossier_required_governance_fields_are_enforced() -> None:
    with pytest.raises(ValueError, match="downstream_review_questions must contain at least one item"):
        create_strategy_dossier(
            dossier_id="mock-strategy-dossier-missing-questions",
            closure_record=FICTITIOUS_STRATEGY_CLOSURE_RECORD,
            sections=FICTITIOUS_DOSSIER_SECTIONS,
            downstream_review_questions=(),
            pending_requirements=("Synthetic pending requirement.",),
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-strategy-dossier-missing-questions",
        )

    with pytest.raises(ValueError, match="pending_requirements must contain at least one item"):
        create_strategy_dossier(
            dossier_id="mock-strategy-dossier-missing-requirements",
            closure_record=FICTITIOUS_STRATEGY_CLOSURE_RECORD,
            sections=FICTITIOUS_DOSSIER_SECTIONS,
            downstream_review_questions=("Synthetic downstream question.",),
            pending_requirements=(),
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="Synthetic non-approval statement.",
            audit_reference="mock-audit-strategy-dossier-missing-requirements",
        )

    with pytest.raises(ValueError, match="non_approval_statement must be a non-empty string"):
        create_strategy_dossier(
            dossier_id="mock-strategy-dossier-missing-non-approval",
            closure_record=FICTITIOUS_STRATEGY_CLOSURE_RECORD,
            sections=FICTITIOUS_DOSSIER_SECTIONS,
            downstream_review_questions=("Synthetic downstream question.",),
            pending_requirements=("Synthetic pending requirement.",),
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            non_approval_statement="",
            audit_reference="mock-audit-strategy-dossier-missing-non-approval",
        )


def test_strategy_dossier_preserves_closure_traceability_and_falsification() -> None:
    dossier = FICTITIOUS_STRATEGY_DOSSIER
    closure = dossier.closure_record

    assert dossier.closure_id == closure.closure_id
    assert dossier.quality_assessment_id == closure.quality_assessment_id
    assert dossier.registry_entry_id == closure.registry_entry_id
    assert dossier.source_hypothesis_ids == closure.source_hypothesis_ids
    assert dossier.signal_ids == closure.signal_ids
    assert dossier.regime_frame_ids == closure.regime_frame_ids
    assert dossier.rule_ids == closure.rule_ids
    assert (
        dossier.upstream_falsification_references
        == closure.upstream_falsification_references
    )


def test_strategy_dossier_is_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        FICTITIOUS_STRATEGY_DOSSIER.handoff_status = (
            DossierHandoffStatus.DOSSIER_PREPARED_PENDING_FINAL_AUDIT
        )


def test_strategy_dossier_does_not_expose_backtest_performance_or_execution_fields() -> None:
    dossier = FICTITIOUS_STRATEGY_DOSSIER

    assert not hasattr(dossier, "handoff_executed")
    assert not hasattr(dossier, "backtest_result")
    assert not hasattr(dossier, "pnl")
    assert not hasattr(dossier, "drawdown")
    assert not hasattr(dossier, "hit_rate")
    assert not hasattr(dossier, "sharpe")
    assert not hasattr(dossier, "sortino")
    assert not hasattr(dossier, "calmar")
    assert not hasattr(dossier, "position_size")
    assert not hasattr(dossier, "order")
    assert not hasattr(dossier, "execution")

