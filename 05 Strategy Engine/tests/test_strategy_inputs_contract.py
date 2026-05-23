from __future__ import annotations

from pathlib import Path
import sys


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from mockups.strategy_inputs_contract_mockups import (  # noqa: E402
    FICTITIOUS_EVIDENCE_INELIGIBLE,
    FICTITIOUS_HYPOTHESIS_ELIGIBLE,
    FICTITIOUS_HYPOTHESIS_INCOMPLETE_TRACEABILITY,
    FICTITIOUS_HYPOTHESIS_MISSING_FALSIFICATION,
    FICTITIOUS_HYPOTHESIS_UNAPPROVED,
)
from strategy.inputs_contract import (  # noqa: E402
    EligibilityStatus,
    InputType,
    decide_strategy_input_eligibility,
)


def test_unapproved_hypothesis_is_rejected_for_strategy_design() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_HYPOTHESIS_UNAPPROVED)

    assert decision.input_type is InputType.HYPOTHESIS
    assert decision.eligibility_status is EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.required_approvals_present is False
    assert "approval status is not approved" in decision.decision_reason


def test_approved_hypothesis_without_falsification_is_rejected() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_HYPOTHESIS_MISSING_FALSIFICATION)

    assert decision.eligibility_status is EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.falsification_criteria_present is False
    assert "falsification criteria are missing" in decision.decision_reason


def test_hypothesis_with_incomplete_traceability_is_rejected() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_HYPOTHESIS_INCOMPLETE_TRACEABILITY)

    assert decision.eligibility_status is EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.traceability_complete is False
    assert "traceability is incomplete" in decision.decision_reason


def test_eligible_hypothesis_requires_approval_traceability_limitations_and_falsification() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_HYPOTHESIS_ELIGIBLE)

    assert decision.eligibility_status is EligibilityStatus.ELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.required_approvals_present is True
    assert decision.traceability_complete is True
    assert decision.limitations_acknowledged is True
    assert decision.falsification_criteria_present is True
    assert decision.decision_reason == "eligible for conceptual strategy design only"


def test_evidence_alone_is_not_eligible_for_strategy_design() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_EVIDENCE_INELIGIBLE)

    assert decision.input_type is InputType.RESEARCH_EVIDENCE
    assert decision.eligibility_status is EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.required_approvals_present is True
    assert "evidence alone cannot feed strategy design" in decision.decision_reason


def test_contract_outputs_are_only_eligibility_decisions() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_HYPOTHESIS_ELIGIBLE)

    assert decision.__class__.__name__ == "StrategyInputEligibilityDecision"
    assert not hasattr(decision, "signal_id")
    assert not hasattr(decision, "rule_id")
    assert not hasattr(decision, "strategy_candidate_id")
    assert not hasattr(decision, "pnl")
    assert not hasattr(decision, "sharpe")
    assert not hasattr(decision, "order")
