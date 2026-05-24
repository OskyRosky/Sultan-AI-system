from __future__ import annotations

from pathlib import Path
import sys

import pytest


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from candidates.strategy_candidate import (  # noqa: E402
    CandidateStatus,
    create_strategy_candidate,
)
from mockups.rule_definition_mockups import (  # noqa: E402
    FICTITIOUS_RULE_DEFINITION,
)
from mockups.signal_definition_mockups import (  # noqa: E402
    FICTITIOUS_SIGNAL_DEFINITION,
)
from mockups.strategy_candidate_mockups import (  # noqa: E402
    FICTITIOUS_STRATEGY_CANDIDATE,
    MOCK_CANDIDATE_CREATED_AT,
)


def test_valid_strategy_candidate_requires_rule_definitions() -> None:
    candidate = create_strategy_candidate(
        candidate_id="mock-candidate-valid",
        rule_definitions=(FICTITIOUS_RULE_DEFINITION,),
        composition_summary="Synthetic composition summary.",
        composition_rationale="Synthetic composition rationale.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        conflict_notes=("Synthetic conflict note.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-candidate-valid",
        created_at=MOCK_CANDIDATE_CREATED_AT,
    )

    assert candidate.candidate_id == "mock-candidate-valid"
    assert candidate.rule_definitions == (FICTITIOUS_RULE_DEFINITION,)
    assert candidate.status is CandidateStatus.PENDING_RISK_TEMPLATE


def test_empty_rule_set_is_rejected() -> None:
    with pytest.raises(ValueError, match="must contain at least one rule definition"):
        create_strategy_candidate(
            candidate_id="mock-candidate-empty",
            rule_definitions=(),
            composition_summary="Synthetic composition summary.",
            composition_rationale="Synthetic composition rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-empty",
        )


def test_non_rule_origin_is_rejected() -> None:
    with pytest.raises(ValueError, match="must be RuleDefinition instances"):
        create_strategy_candidate(
            candidate_id="mock-candidate-bad-origin",
            rule_definitions=(FICTITIOUS_SIGNAL_DEFINITION,),
            composition_summary="Synthetic composition summary.",
            composition_rationale="Synthetic composition rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-bad-origin",
        )


def test_unsupported_candidate_status_is_rejected() -> None:
    with pytest.raises(TypeError, match="status must be a CandidateStatus"):
        create_strategy_candidate(
            candidate_id="mock-candidate-bad-status-type",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION,),
            composition_summary="Synthetic composition summary.",
            composition_rationale="Synthetic composition rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-bad-status-type",
            status="pending_risk_template",
        )


def test_block_06_candidates_must_remain_pending_risk_template() -> None:
    with pytest.raises(ValueError, match="must remain pending_risk_template"):
        create_strategy_candidate(
            candidate_id="mock-candidate-composed-status",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION,),
            composition_summary="Synthetic composition summary.",
            composition_rationale="Synthetic composition rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-composed-status",
            status=CandidateStatus.COMPOSED,
        )


def test_required_governance_fields_are_enforced() -> None:
    with pytest.raises(ValueError, match="composition_summary must be a non-empty string"):
        create_strategy_candidate(
            candidate_id="mock-candidate-missing-summary",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION,),
            composition_summary="",
            composition_rationale="Synthetic rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-missing-summary",
        )

    with pytest.raises(ValueError, match="composition_rationale must be a non-empty string"):
        create_strategy_candidate(
            candidate_id="mock-candidate-missing-rationale",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION,),
            composition_summary="Synthetic summary.",
            composition_rationale="",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-missing-rationale",
        )

    with pytest.raises(ValueError, match="assumptions must contain at least one item"):
        create_strategy_candidate(
            candidate_id="mock-candidate-missing-assumptions",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION,),
            composition_summary="Synthetic summary.",
            composition_rationale="Synthetic rationale.",
            assumptions=(),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-missing-assumptions",
        )

    with pytest.raises(ValueError, match="limitations must contain at least one item"):
        create_strategy_candidate(
            candidate_id="mock-candidate-missing-limitations",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION,),
            composition_summary="Synthetic summary.",
            composition_rationale="Synthetic rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=(),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-missing-limitations",
        )

    with pytest.raises(ValueError, match="falsification_references must contain at least one item"):
        create_strategy_candidate(
            candidate_id="mock-candidate-missing-falsification",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION,),
            composition_summary="Synthetic summary.",
            composition_rationale="Synthetic rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=(),
            audit_reference="mock-audit-candidate-missing-falsification",
        )

    with pytest.raises(ValueError, match="audit_reference must be a non-empty string"):
        create_strategy_candidate(
            candidate_id="mock-candidate-missing-audit",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION,),
            composition_summary="Synthetic summary.",
            composition_rationale="Synthetic rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="",
        )


def test_strategy_candidate_preserves_rule_regime_signal_hypothesis_chain() -> None:
    candidate = FICTITIOUS_STRATEGY_CANDIDATE
    rule = candidate.rule_definitions[0]

    assert rule.regime_context_frame.signal_definition is rule.signal_definition
    assert rule.signal_definition.source_hypothesis_decision.input_type.value == "hypothesis"
    assert rule.signal_definition.source_hypothesis_decision.eligible_for_strategy_design is True
    assert candidate.status is CandidateStatus.PENDING_RISK_TEMPLATE


def test_strategy_candidate_does_not_expose_future_block_or_performance_fields() -> None:
    candidate = FICTITIOUS_STRATEGY_CANDIDATE

    assert not hasattr(candidate, "risk_template")
    assert not hasattr(candidate, "registry_status")
    assert not hasattr(candidate, "quality_gate_status")
    assert not hasattr(candidate, "backtest_result")
    assert not hasattr(candidate, "pnl")
    assert not hasattr(candidate, "drawdown")
    assert not hasattr(candidate, "hit_rate")
    assert not hasattr(candidate, "sharpe")
    assert not hasattr(candidate, "sortino")
    assert not hasattr(candidate, "calmar")
    assert not hasattr(candidate, "position_size")
    assert not hasattr(candidate, "capital_allocation")
    assert not hasattr(candidate, "stop_loss")
    assert not hasattr(candidate, "take_profit")
    assert not hasattr(candidate, "leverage")
    assert not hasattr(candidate, "order")
    assert not hasattr(candidate, "execution")
