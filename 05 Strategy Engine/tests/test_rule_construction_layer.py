from __future__ import annotations

from pathlib import Path
import sys

import pytest


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from mockups.regime_context_mockups import (  # noqa: E402
    FICTITIOUS_REGIME_CONTEXT_FRAME,
)
from mockups.rule_definition_mockups import (  # noqa: E402
    FICTITIOUS_RULE_DEFINITION,
    MOCK_RULE_CREATED_AT,
)
from mockups.signal_definition_mockups import (  # noqa: E402
    FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
    FICTITIOUS_SIGNAL_DEFINITION,
)
from regimes.regime_context import RegimeType, create_regime_context_frame  # noqa: E402
from rules.rule_definition import RuleCategory, create_rule_definition  # noqa: E402
from signals.signal_definition import SignalOrientation, create_signal_definition  # noqa: E402


def test_valid_rule_definition_requires_matching_signal_and_regime_context() -> None:
    rule = create_rule_definition(
        rule_id="mock-rule-valid",
        signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
        regime_context_frame=FICTITIOUS_REGIME_CONTEXT_FRAME,
        rule_category=RuleCategory.ENTRY_CONDITION,
        rule_statement="Synthetic declarative rule statement.",
        interpretation_guidance="Synthetic interpretation guidance.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-rule-valid",
        created_at=MOCK_RULE_CREATED_AT,
    )

    assert rule.rule_id == "mock-rule-valid"
    assert rule.signal_definition is FICTITIOUS_SIGNAL_DEFINITION
    assert rule.regime_context_frame is FICTITIOUS_REGIME_CONTEXT_FRAME
    assert rule.rule_category is RuleCategory.ENTRY_CONDITION


def test_non_signal_origin_is_rejected() -> None:
    with pytest.raises(ValueError, match="must reference a valid signal definition"):
        create_rule_definition(
            rule_id="mock-rule-bad-signal",
            signal_definition=FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
            regime_context_frame=FICTITIOUS_REGIME_CONTEXT_FRAME,
            rule_category=RuleCategory.FILTER_CONDITION,
            rule_statement="Synthetic statement.",
            interpretation_guidance="Synthetic guidance.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-rule-bad-signal",
        )


def test_non_regime_context_origin_is_rejected() -> None:
    with pytest.raises(ValueError, match="must reference a valid regime context frame"):
        create_rule_definition(
            rule_id="mock-rule-bad-regime",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_context_frame=FICTITIOUS_SIGNAL_DEFINITION,
            rule_category=RuleCategory.FILTER_CONDITION,
            rule_statement="Synthetic statement.",
            interpretation_guidance="Synthetic guidance.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-rule-bad-regime",
        )


def test_mismatched_signal_and_regime_context_are_rejected() -> None:
    other_signal = create_signal_definition(
        signal_id="mock-signal-other-for-rule",
        source_hypothesis_decision=FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
        orientation=SignalOrientation.NEUTRAL,
        observable_condition="Synthetic other condition.",
        expected_behavior="Synthetic other behavior.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-signal-other-for-rule",
        created_at=MOCK_RULE_CREATED_AT,
    )

    with pytest.raises(ValueError, match="must reference the same signal definition"):
        create_rule_definition(
            rule_id="mock-rule-mismatched",
            signal_definition=other_signal,
            regime_context_frame=FICTITIOUS_REGIME_CONTEXT_FRAME,
            rule_category=RuleCategory.INVALIDATION_CONDITION,
            rule_statement="Synthetic statement.",
            interpretation_guidance="Synthetic guidance.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-rule-mismatched",
        )


def test_unsupported_rule_category_is_rejected() -> None:
    with pytest.raises(TypeError, match="rule_category must be a RuleCategory"):
        create_rule_definition(
            rule_id="mock-rule-bad-category",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_context_frame=FICTITIOUS_REGIME_CONTEXT_FRAME,
            rule_category="entry_condition",
            rule_statement="Synthetic statement.",
            interpretation_guidance="Synthetic guidance.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-rule-bad-category",
        )


def test_required_governance_fields_are_enforced() -> None:
    with pytest.raises(ValueError, match="rule_statement must be a non-empty string"):
        create_rule_definition(
            rule_id="mock-rule-missing-statement",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_context_frame=FICTITIOUS_REGIME_CONTEXT_FRAME,
            rule_category=RuleCategory.EXIT_CONDITION,
            rule_statement="",
            interpretation_guidance="Synthetic guidance.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-rule-missing-statement",
        )

    with pytest.raises(ValueError, match="interpretation_guidance must be a non-empty string"):
        create_rule_definition(
            rule_id="mock-rule-missing-guidance",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_context_frame=FICTITIOUS_REGIME_CONTEXT_FRAME,
            rule_category=RuleCategory.EXIT_CONDITION,
            rule_statement="Synthetic statement.",
            interpretation_guidance="",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-rule-missing-guidance",
        )

    with pytest.raises(ValueError, match="assumptions must contain at least one item"):
        create_rule_definition(
            rule_id="mock-rule-missing-assumptions",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_context_frame=FICTITIOUS_REGIME_CONTEXT_FRAME,
            rule_category=RuleCategory.EXIT_CONDITION,
            rule_statement="Synthetic statement.",
            interpretation_guidance="Synthetic guidance.",
            assumptions=(),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-rule-missing-assumptions",
        )

    with pytest.raises(ValueError, match="limitations must contain at least one item"):
        create_rule_definition(
            rule_id="mock-rule-missing-limitations",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_context_frame=FICTITIOUS_REGIME_CONTEXT_FRAME,
            rule_category=RuleCategory.EXIT_CONDITION,
            rule_statement="Synthetic statement.",
            interpretation_guidance="Synthetic guidance.",
            assumptions=("Synthetic assumption.",),
            limitations=(),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-rule-missing-limitations",
        )

    with pytest.raises(ValueError, match="falsification_references must contain at least one item"):
        create_rule_definition(
            rule_id="mock-rule-missing-falsification",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_context_frame=FICTITIOUS_REGIME_CONTEXT_FRAME,
            rule_category=RuleCategory.EXIT_CONDITION,
            rule_statement="Synthetic statement.",
            interpretation_guidance="Synthetic guidance.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=(),
            audit_reference="mock-audit-rule-missing-falsification",
        )

    with pytest.raises(ValueError, match="audit_reference must be a non-empty string"):
        create_rule_definition(
            rule_id="mock-rule-missing-audit",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_context_frame=FICTITIOUS_REGIME_CONTEXT_FRAME,
            rule_category=RuleCategory.EXIT_CONDITION,
            rule_statement="Synthetic statement.",
            interpretation_guidance="Synthetic guidance.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="",
        )


def test_rule_definition_preserves_signal_and_regime_context_chain() -> None:
    rule = FICTITIOUS_RULE_DEFINITION

    assert rule.regime_context_frame.signal_definition is rule.signal_definition
    assert rule.signal_definition.source_hypothesis_decision.input_type.value == "hypothesis"
    assert rule.signal_definition.source_hypothesis_decision.eligible_for_strategy_design is True


def test_rule_definition_does_not_expose_strategy_execution_or_performance_fields() -> None:
    rule = FICTITIOUS_RULE_DEFINITION

    assert not hasattr(rule, "strategy_candidate_id")
    assert not hasattr(rule, "order")
    assert not hasattr(rule, "trade")
    assert not hasattr(rule, "position_size")
    assert not hasattr(rule, "stop_loss")
    assert not hasattr(rule, "take_profit")
    assert not hasattr(rule, "leverage")
    assert not hasattr(rule, "pnl")
    assert not hasattr(rule, "drawdown")
    assert not hasattr(rule, "hit_rate")
    assert not hasattr(rule, "sharpe")
    assert not hasattr(rule, "sortino")
    assert not hasattr(rule, "calmar")
