from __future__ import annotations

from pathlib import Path
import sys

import pytest


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from mockups.signal_definition_mockups import (  # noqa: E402
    FICTITIOUS_ELIGIBLE_FINDING_DECISION,
    FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
    FICTITIOUS_EVIDENCE_DECISION,
    FICTITIOUS_NONELIGIBLE_FINDING_DECISION,
    FICTITIOUS_NONELIGIBLE_HYPOTHESIS_DECISION,
    FICTITIOUS_SIGNAL_DEFINITION,
    MOCK_SIGNAL_CREATED_AT,
)
from signals.signal_definition import (  # noqa: E402
    SignalOrientation,
    create_signal_definition,
)


def test_valid_signal_definition_requires_eligible_hypothesis_origin() -> None:
    signal = create_signal_definition(
        signal_id="mock-signal-valid",
        source_hypothesis_decision=FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
        supporting_finding_decisions=(FICTITIOUS_ELIGIBLE_FINDING_DECISION,),
        orientation=SignalOrientation.LONG_BIAS,
        observable_condition="Synthetic observable condition.",
        expected_behavior="Synthetic expected behavior.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-signal-valid",
        created_at=MOCK_SIGNAL_CREATED_AT,
    )

    assert signal.signal_id == "mock-signal-valid"
    assert signal.source_hypothesis_decision.eligible_for_strategy_design is True
    assert signal.source_hypothesis_decision.input_type.value == "hypothesis"
    assert signal.orientation is SignalOrientation.LONG_BIAS


def test_noneligible_hypothesis_cannot_originate_signal() -> None:
    with pytest.raises(ValueError, match="source hypothesis decision is not eligible"):
        create_signal_definition(
            signal_id="mock-signal-rejected-origin",
            source_hypothesis_decision=FICTITIOUS_NONELIGIBLE_HYPOTHESIS_DECISION,
            orientation=SignalOrientation.NEUTRAL,
            observable_condition="Synthetic condition.",
            expected_behavior="Synthetic behavior.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-signal-rejected-origin",
        )


def test_eligible_finding_cannot_originate_signal() -> None:
    with pytest.raises(ValueError, match="signal origin must be an eligible hypothesis decision"):
        create_signal_definition(
            signal_id="mock-signal-finding-origin",
            source_hypothesis_decision=FICTITIOUS_ELIGIBLE_FINDING_DECISION,
            orientation=SignalOrientation.AVOID,
            observable_condition="Synthetic condition.",
            expected_behavior="Synthetic behavior.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-signal-finding-origin",
        )


def test_eligible_finding_can_support_signal_context() -> None:
    signal = FICTITIOUS_SIGNAL_DEFINITION

    assert len(signal.supporting_finding_decisions) == 1
    assert signal.supporting_finding_decisions[0].input_type.value == "finding"
    assert signal.supporting_finding_decisions[0].eligible_for_strategy_design is True


def test_noneligible_supporting_finding_is_rejected() -> None:
    with pytest.raises(ValueError, match="supporting finding decision is not eligible"):
        create_signal_definition(
            signal_id="mock-signal-bad-support",
            source_hypothesis_decision=FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
            supporting_finding_decisions=(FICTITIOUS_NONELIGIBLE_FINDING_DECISION,),
            orientation=SignalOrientation.SHORT_BIAS,
            observable_condition="Synthetic condition.",
            expected_behavior="Synthetic behavior.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-signal-bad-support",
        )


def test_evidence_decision_cannot_support_signal_context_directly() -> None:
    with pytest.raises(ValueError, match="supporting context must contain finding decisions only"):
        create_signal_definition(
            signal_id="mock-signal-evidence-support",
            source_hypothesis_decision=FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
            supporting_finding_decisions=(FICTITIOUS_EVIDENCE_DECISION,),
            orientation=SignalOrientation.NEUTRAL,
            observable_condition="Synthetic condition.",
            expected_behavior="Synthetic behavior.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-signal-evidence-support",
        )


def test_required_governance_fields_are_enforced() -> None:
    with pytest.raises(ValueError, match="assumptions must contain at least one item"):
        create_signal_definition(
            signal_id="mock-signal-missing-assumptions",
            source_hypothesis_decision=FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
            orientation=SignalOrientation.LONG_BIAS,
            observable_condition="Synthetic condition.",
            expected_behavior="Synthetic behavior.",
            assumptions=(),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-signal-missing-assumptions",
        )

    with pytest.raises(ValueError, match="limitations must contain at least one item"):
        create_signal_definition(
            signal_id="mock-signal-missing-limitations",
            source_hypothesis_decision=FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
            orientation=SignalOrientation.LONG_BIAS,
            observable_condition="Synthetic condition.",
            expected_behavior="Synthetic behavior.",
            assumptions=("Synthetic assumption.",),
            limitations=(),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-signal-missing-limitations",
        )

    with pytest.raises(ValueError, match="falsification_references must contain at least one item"):
        create_signal_definition(
            signal_id="mock-signal-missing-falsification",
            source_hypothesis_decision=FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
            orientation=SignalOrientation.LONG_BIAS,
            observable_condition="Synthetic condition.",
            expected_behavior="Synthetic behavior.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=(),
            audit_reference="mock-audit-signal-missing-falsification",
        )

    with pytest.raises(ValueError, match="audit_reference must be a non-empty string"):
        create_signal_definition(
            signal_id="mock-signal-missing-audit",
            source_hypothesis_decision=FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
            orientation=SignalOrientation.LONG_BIAS,
            observable_condition="Synthetic condition.",
            expected_behavior="Synthetic behavior.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="",
        )


def test_signal_definition_does_not_expose_trading_or_performance_fields() -> None:
    signal = FICTITIOUS_SIGNAL_DEFINITION

    assert not hasattr(signal, "order")
    assert not hasattr(signal, "trade")
    assert not hasattr(signal, "entry_rule")
    assert not hasattr(signal, "exit_rule")
    assert not hasattr(signal, "strategy_candidate_id")
    assert not hasattr(signal, "pnl")
    assert not hasattr(signal, "sharpe")
    assert not hasattr(signal, "sortino")
    assert not hasattr(signal, "calmar")
