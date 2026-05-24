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
from mockups.regime_context_mockups import (  # noqa: E402
    FICTITIOUS_REGIME_CONTEXT_FRAME,
)
from mockups.signal_definition_mockups import (  # noqa: E402
    FICTITIOUS_ELIGIBLE_FINDING_DECISION,
    FICTITIOUS_SIGNAL_DEFINITION,
)
from mockups.strategy_candidate_mockups import (  # noqa: E402
    FICTITIOUS_STRATEGY_CANDIDATE,
    MOCK_CANDIDATE_CREATED_AT,
)
from regimes.regime_context import RegimeType, create_regime_context_frame  # noqa: E402
from rules.rule_definition import RuleCategory, create_rule_definition  # noqa: E402
from signals.signal_definition import SignalOrientation, create_signal_definition  # noqa: E402
from strategy.inputs_contract import (  # noqa: E402
    HypothesisInput,
    SourceStatus,
    decide_strategy_input_eligibility,
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


def test_multi_rule_candidate_accepts_rules_with_same_signal_regime_and_hypothesis() -> None:
    compatible_rule = create_rule_definition(
        rule_id="mock-rule-compatible",
        signal_definition=FICTITIOUS_RULE_DEFINITION.signal_definition,
        regime_context_frame=FICTITIOUS_RULE_DEFINITION.regime_context_frame,
        rule_category=RuleCategory.FILTER_CONDITION,
        rule_statement="Synthetic compatible rule statement.",
        interpretation_guidance="Synthetic compatible guidance.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-rule-compatible",
        created_at=MOCK_CANDIDATE_CREATED_AT,
    )

    candidate = create_strategy_candidate(
        candidate_id="mock-candidate-compatible-rules",
        rule_definitions=(FICTITIOUS_RULE_DEFINITION, compatible_rule),
        composition_summary="Synthetic compatible multi-rule composition.",
        composition_rationale="Synthetic rationale for compatible rule grouping.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-candidate-compatible-rules",
        created_at=MOCK_CANDIDATE_CREATED_AT,
    )

    assert len(candidate.rule_definitions) == 2
    assert candidate.rule_definitions[0].signal_definition == candidate.rule_definitions[1].signal_definition
    assert (
        candidate.rule_definitions[0].regime_context_frame
        == candidate.rule_definitions[1].regime_context_frame
    )


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


def test_rules_with_different_signal_definitions_are_rejected() -> None:
    other_signal = create_signal_definition(
        signal_id="mock-signal-different-for-candidate",
        source_hypothesis_decision=FICTITIOUS_RULE_DEFINITION.signal_definition.source_hypothesis_decision,
        supporting_finding_decisions=(FICTITIOUS_ELIGIBLE_FINDING_DECISION,),
        orientation=SignalOrientation.NEUTRAL,
        observable_condition="Synthetic different signal condition.",
        expected_behavior="Synthetic different signal behavior.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-signal-different-for-candidate",
        created_at=MOCK_CANDIDATE_CREATED_AT,
    )
    other_regime = create_regime_context_frame(
        frame_id="mock-regime-for-different-signal",
        signal_definition=other_signal,
        regime_type=RegimeType.VOLATILITY,
        regime_label="mock_high_vol_context",
        context_description="Synthetic context.",
        applicability_rationale="Synthetic rationale.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-regime-for-different-signal",
        created_at=MOCK_CANDIDATE_CREATED_AT,
    )
    other_rule = create_rule_definition(
        rule_id="mock-rule-different-signal",
        signal_definition=other_signal,
        regime_context_frame=other_regime,
        rule_category=RuleCategory.FILTER_CONDITION,
        rule_statement="Synthetic statement.",
        interpretation_guidance="Synthetic guidance.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-rule-different-signal",
        created_at=MOCK_CANDIDATE_CREATED_AT,
    )

    with pytest.raises(ValueError, match="same signal definition"):
        create_strategy_candidate(
            candidate_id="mock-candidate-different-signal",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION, other_rule),
            composition_summary="Synthetic composition summary.",
            composition_rationale="Synthetic composition rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-different-signal",
        )


def test_rules_with_different_regime_context_frames_are_rejected() -> None:
    other_regime = create_regime_context_frame(
        frame_id="mock-regime-different-for-candidate",
        signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
        regime_type=RegimeType.RANGE,
        regime_label="mock_range_context",
        context_description="Synthetic different regime context.",
        applicability_rationale="Synthetic rationale.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-regime-different-for-candidate",
        created_at=MOCK_CANDIDATE_CREATED_AT,
    )
    other_rule = create_rule_definition(
        rule_id="mock-rule-different-regime",
        signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
        regime_context_frame=other_regime,
        rule_category=RuleCategory.FILTER_CONDITION,
        rule_statement="Synthetic statement.",
        interpretation_guidance="Synthetic guidance.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-rule-different-regime",
        created_at=MOCK_CANDIDATE_CREATED_AT,
    )

    with pytest.raises(ValueError, match="same regime context frame"):
        create_strategy_candidate(
            candidate_id="mock-candidate-different-regime",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION, other_rule),
            composition_summary="Synthetic composition summary.",
            composition_rationale="Synthetic composition rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-different-regime",
        )


def test_rules_with_different_source_hypotheses_are_rejected() -> None:
    other_hypothesis = HypothesisInput(
        hypothesis_id="mock-hypothesis-different-for-candidate",
        linked_finding_ids=("mock-finding-001",),
        linked_evidence_ids=("mock-evidence-001",),
        hypothesis_statement="Fictitious second hypothesis.",
        expected_behavior="Synthetic behavior.",
        applicable_regime_context="mock_regime_context",
        falsification_criteria=("Synthetic falsification criterion.",),
        limitations=("Synthetic limitation.",),
        source_status=SourceStatus.PROMOTED_FOR_STRATEGY_REVIEW,
        audit_reference="mock-audit-hypothesis-different-for-candidate",
    )
    other_decision = decide_strategy_input_eligibility(
        other_hypothesis,
        decided_at=MOCK_CANDIDATE_CREATED_AT,
    )
    other_signal = create_signal_definition(
        signal_id=FICTITIOUS_SIGNAL_DEFINITION.signal_id,
        source_hypothesis_decision=other_decision,
        supporting_finding_decisions=(FICTITIOUS_ELIGIBLE_FINDING_DECISION,),
        orientation=FICTITIOUS_SIGNAL_DEFINITION.orientation,
        observable_condition=FICTITIOUS_SIGNAL_DEFINITION.observable_condition,
        expected_behavior=FICTITIOUS_SIGNAL_DEFINITION.expected_behavior,
        assumptions=FICTITIOUS_SIGNAL_DEFINITION.assumptions,
        limitations=FICTITIOUS_SIGNAL_DEFINITION.limitations,
        falsification_references=FICTITIOUS_SIGNAL_DEFINITION.falsification_references,
        audit_reference=FICTITIOUS_SIGNAL_DEFINITION.audit_reference,
        created_at=FICTITIOUS_SIGNAL_DEFINITION.created_at,
    )
    other_regime = create_regime_context_frame(
        frame_id=FICTITIOUS_REGIME_CONTEXT_FRAME.frame_id,
        signal_definition=other_signal,
        regime_type=FICTITIOUS_REGIME_CONTEXT_FRAME.regime_type,
        regime_label=FICTITIOUS_REGIME_CONTEXT_FRAME.regime_label,
        context_description=FICTITIOUS_REGIME_CONTEXT_FRAME.context_description,
        applicability_rationale=FICTITIOUS_REGIME_CONTEXT_FRAME.applicability_rationale,
        assumptions=FICTITIOUS_REGIME_CONTEXT_FRAME.assumptions,
        limitations=FICTITIOUS_REGIME_CONTEXT_FRAME.limitations,
        falsification_references=FICTITIOUS_REGIME_CONTEXT_FRAME.falsification_references,
        audit_reference=FICTITIOUS_REGIME_CONTEXT_FRAME.audit_reference,
        created_at=FICTITIOUS_REGIME_CONTEXT_FRAME.created_at,
    )
    other_rule = create_rule_definition(
        rule_id=FICTITIOUS_RULE_DEFINITION.rule_id,
        signal_definition=other_signal,
        regime_context_frame=other_regime,
        rule_category=FICTITIOUS_RULE_DEFINITION.rule_category,
        rule_statement=FICTITIOUS_RULE_DEFINITION.rule_statement,
        interpretation_guidance=FICTITIOUS_RULE_DEFINITION.interpretation_guidance,
        assumptions=FICTITIOUS_RULE_DEFINITION.assumptions,
        limitations=FICTITIOUS_RULE_DEFINITION.limitations,
        falsification_references=FICTITIOUS_RULE_DEFINITION.falsification_references,
        audit_reference=FICTITIOUS_RULE_DEFINITION.audit_reference,
        created_at=FICTITIOUS_RULE_DEFINITION.created_at,
    )

    with pytest.raises(ValueError, match="same source hypothesis"):
        create_strategy_candidate(
            candidate_id="mock-candidate-different-hypothesis",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION, other_rule),
            composition_summary="Synthetic composition summary.",
            composition_rationale="Synthetic composition rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-different-hypothesis",
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

    with pytest.raises(ValueError, match="must remain pending_risk_template"):
        create_strategy_candidate(
            candidate_id="mock-candidate-draft-status",
            rule_definitions=(FICTITIOUS_RULE_DEFINITION,),
            composition_summary="Synthetic composition summary.",
            composition_rationale="Synthetic composition rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-candidate-draft-status",
            status=CandidateStatus.DRAFT,
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
