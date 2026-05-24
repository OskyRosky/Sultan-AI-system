from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import sys

import pytest


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from candidates.candidate_registry import (  # noqa: E402
    RegistryStatus,
    add_registry_entry,
    create_registry,
    create_registry_entry,
)
from mockups.candidate_registry_mockups import (  # noqa: E402
    FICTITIOUS_REGISTRY,
    FICTITIOUS_REGISTRY_ENTRY,
    MOCK_REGISTRY_CREATED_AT,
)
from mockups.risk_template_mockups import FICTITIOUS_RISK_TEMPLATE  # noqa: E402
from mockups.signal_definition_mockups import FICTITIOUS_SIGNAL_DEFINITION  # noqa: E402
from mockups.strategy_candidate_mockups import FICTITIOUS_STRATEGY_CANDIDATE  # noqa: E402


def test_valid_registry_entry_requires_candidate_and_matching_risk_template() -> None:
    entry = create_registry_entry(
        entry_id="mock-registry-entry-valid",
        strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
        risk_template=FICTITIOUS_RISK_TEMPLATE,
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-registry-entry-valid",
        registered_at=MOCK_REGISTRY_CREATED_AT,
    )

    assert entry.entry_id == "mock-registry-entry-valid"
    assert entry.strategy_candidate is FICTITIOUS_STRATEGY_CANDIDATE
    assert entry.risk_template is FICTITIOUS_RISK_TEMPLATE
    assert entry.registry_status is RegistryStatus.REGISTERED_PENDING_QUALITY_GATES


def test_non_candidate_origin_is_rejected() -> None:
    with pytest.raises(ValueError, match="valid strategy candidate"):
        create_registry_entry(
            entry_id="mock-registry-entry-bad-candidate",
            strategy_candidate=FICTITIOUS_SIGNAL_DEFINITION,
            risk_template=FICTITIOUS_RISK_TEMPLATE,
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-registry-entry-bad-candidate",
        )


def test_non_risk_template_origin_is_rejected() -> None:
    with pytest.raises(ValueError, match="valid risk template"):
        create_registry_entry(
            entry_id="mock-registry-entry-bad-template",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_template=FICTITIOUS_STRATEGY_CANDIDATE,
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-registry-entry-bad-template",
        )


def test_mismatched_candidate_and_risk_template_are_rejected() -> None:
    other_candidate = replace(
        FICTITIOUS_STRATEGY_CANDIDATE,
        candidate_id="mock-candidate-mismatched-registry",
    )

    with pytest.raises(ValueError, match="same strategy candidate"):
        create_registry_entry(
            entry_id="mock-registry-entry-mismatch",
            strategy_candidate=other_candidate,
            risk_template=FICTITIOUS_RISK_TEMPLATE,
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-registry-entry-mismatch",
        )


def test_unsupported_registry_status_is_rejected() -> None:
    with pytest.raises(TypeError, match="registry_status must be a RegistryStatus"):
        create_registry_entry(
            entry_id="mock-registry-entry-bad-status",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_template=FICTITIOUS_RISK_TEMPLATE,
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-registry-entry-bad-status",
            registry_status="registered_pending_quality_gates",
        )


def test_required_governance_fields_are_enforced() -> None:
    with pytest.raises(ValueError, match="assumptions must contain at least one item"):
        create_registry_entry(
            entry_id="mock-registry-entry-missing-assumptions",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_template=FICTITIOUS_RISK_TEMPLATE,
            assumptions=(),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-registry-entry-missing-assumptions",
        )

    with pytest.raises(ValueError, match="limitations must contain at least one item"):
        create_registry_entry(
            entry_id="mock-registry-entry-missing-limitations",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_template=FICTITIOUS_RISK_TEMPLATE,
            assumptions=("Synthetic assumption.",),
            limitations=(),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-registry-entry-missing-limitations",
        )

    with pytest.raises(ValueError, match="falsification_references must contain at least one item"):
        create_registry_entry(
            entry_id="mock-registry-entry-missing-falsification",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_template=FICTITIOUS_RISK_TEMPLATE,
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=(),
            audit_reference="mock-audit-registry-entry-missing-falsification",
        )

    with pytest.raises(ValueError, match="audit_reference must be a non-empty string"):
        create_registry_entry(
            entry_id="mock-registry-entry-missing-audit",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_template=FICTITIOUS_RISK_TEMPLATE,
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="",
        )


def test_registry_entry_preserves_traceability_identifiers() -> None:
    entry = FICTITIOUS_REGISTRY_ENTRY
    rule = entry.strategy_candidate.rule_definitions[0]

    assert entry.source_hypothesis_ids == (
        rule.signal_definition.source_hypothesis_decision.input_id,
    )
    assert entry.signal_ids == (rule.signal_definition.signal_id,)
    assert entry.regime_frame_ids == (rule.regime_context_frame.frame_id,)
    assert entry.rule_ids == (rule.rule_id,)


def test_registry_entry_is_immutable() -> None:
    with pytest.raises(FrozenInstanceError):
        FICTITIOUS_REGISTRY_ENTRY.registry_status = RegistryStatus.REGISTERED_PENDING_QUALITY_GATES


def test_registry_collection_rejects_duplicate_entry_ids_and_candidate_ids() -> None:
    duplicate_entry_id = create_registry_entry(
        entry_id=FICTITIOUS_REGISTRY_ENTRY.entry_id,
        strategy_candidate=replace(
            FICTITIOUS_STRATEGY_CANDIDATE,
            candidate_id="mock-candidate-distinct-for-entry-duplicate",
        ),
        risk_template=replace(
            FICTITIOUS_RISK_TEMPLATE,
            strategy_candidate=replace(
                FICTITIOUS_STRATEGY_CANDIDATE,
                candidate_id="mock-candidate-distinct-for-entry-duplicate",
            ),
        ),
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-duplicate-entry-id",
    )

    with pytest.raises(ValueError, match="duplicate entry_id"):
        create_registry((FICTITIOUS_REGISTRY_ENTRY, duplicate_entry_id))

    duplicate_candidate_id = create_registry_entry(
        entry_id="mock-registry-entry-distinct",
        strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
        risk_template=FICTITIOUS_RISK_TEMPLATE,
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-duplicate-candidate-id",
    )

    with pytest.raises(ValueError, match="duplicate candidate_id"):
        create_registry((FICTITIOUS_REGISTRY_ENTRY, duplicate_candidate_id))


def test_add_registry_entry_returns_new_registry_without_mutating_existing() -> None:
    other_candidate = replace(FICTITIOUS_STRATEGY_CANDIDATE, candidate_id="mock-candidate-new")
    other_template = replace(FICTITIOUS_RISK_TEMPLATE, strategy_candidate=other_candidate)
    other_entry = create_registry_entry(
        entry_id="mock-registry-entry-new",
        strategy_candidate=other_candidate,
        risk_template=other_template,
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-registry-entry-new",
    )

    updated = add_registry_entry(FICTITIOUS_REGISTRY, other_entry)

    assert len(FICTITIOUS_REGISTRY.entries) == 1
    assert len(updated.entries) == 2


def test_registry_entry_does_not_expose_future_block_or_performance_fields() -> None:
    entry = FICTITIOUS_REGISTRY_ENTRY

    assert not hasattr(entry, "quality_gate_status")
    assert not hasattr(entry, "closure_status")
    assert not hasattr(entry, "dossier_ready")
    assert not hasattr(entry, "backtest_result")
    assert not hasattr(entry, "pnl")
    assert not hasattr(entry, "drawdown")
    assert not hasattr(entry, "hit_rate")
    assert not hasattr(entry, "sharpe")
    assert not hasattr(entry, "sortino")
    assert not hasattr(entry, "calmar")
    assert not hasattr(entry, "position_size")
    assert not hasattr(entry, "order")
    assert not hasattr(entry, "execution")
