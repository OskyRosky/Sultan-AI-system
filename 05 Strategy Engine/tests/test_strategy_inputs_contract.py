from __future__ import annotations

from pathlib import Path
import sys


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from mockups.strategy_inputs_contract_mockups import (  # noqa: E402
    FICTITIOUS_EVIDENCE_INELIGIBLE,
    FICTITIOUS_FINDING_ELIGIBLE,
    FICTITIOUS_FINDING_INCOMPLETE_TRACEABILITY,
    FICTITIOUS_FINDING_MISSING_LIMITATIONS,
    FICTITIOUS_FINDING_UNADMISSIBLE_STATUS,
    FICTITIOUS_HYPOTHESIS_ELIGIBLE,
    FICTITIOUS_HYPOTHESIS_INCOMPLETE_TRACEABILITY,
    FICTITIOUS_HYPOTHESIS_MISSING_FALSIFICATION,
    FICTITIOUS_HYPOTHESIS_NONADMISSIBLE_STATUS,
)
from strategy.inputs_contract import (  # noqa: E402
    EligibilityStatus,
    InputType,
    decide_strategy_input_eligibility,
)


def test_hypothesis_without_admissible_source_status_is_rejected() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_HYPOTHESIS_NONADMISSIBLE_STATUS)

    assert decision.input_type is InputType.HYPOTHESIS
    assert decision.eligibility_status is EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.eligible_for_strategy_design is False
    assert decision.source_status_admissible is False
    assert "source status is not admissible for 05: proposed" in decision.decision_reason


def test_promoted_hypothesis_without_falsification_is_rejected() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_HYPOTHESIS_MISSING_FALSIFICATION)

    assert decision.eligibility_status is EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.falsification_criteria_present is False
    assert "falsification criteria are missing" in decision.decision_reason


def test_hypothesis_with_incomplete_traceability_is_rejected() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_HYPOTHESIS_INCOMPLETE_TRACEABILITY)

    assert decision.eligibility_status is EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.traceability_complete is False
    assert "traceability is incomplete" in decision.decision_reason


def test_eligible_hypothesis_requires_status_traceability_limitations_and_falsification() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_HYPOTHESIS_ELIGIBLE)

    assert decision.eligibility_status is EligibilityStatus.ELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.eligible_for_strategy_design is True
    assert decision.source_status == "promoted_for_strategy_review"
    assert decision.source_status_admissible is True
    assert decision.traceability_complete is True
    assert decision.limitations_acknowledged is True
    assert decision.falsification_criteria_present is True
    assert decision.decision_reason == "eligible for conceptual strategy design only"


def test_evidence_alone_is_not_eligible_for_strategy_design() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_EVIDENCE_INELIGIBLE)

    assert decision.input_type is InputType.RESEARCH_EVIDENCE
    assert decision.eligibility_status is EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.eligible_for_strategy_design is False
    assert decision.source_status_admissible is False
    assert "evidence alone cannot feed strategy design" in decision.decision_reason


def test_finding_with_unadmissible_source_status_is_rejected() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_FINDING_UNADMISSIBLE_STATUS)

    assert decision.input_type is InputType.FINDING
    assert decision.eligibility_status is EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.eligible_for_strategy_design is False
    assert decision.source_status == "under_review"
    assert decision.source_status_admissible is False
    assert "source status is not admissible for 05: under_review" in decision.decision_reason


def test_finding_with_incomplete_traceability_is_rejected() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_FINDING_INCOMPLETE_TRACEABILITY)

    assert decision.input_type is InputType.FINDING
    assert decision.eligibility_status is EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.source_status_admissible is True
    assert decision.traceability_complete is False
    assert "traceability is incomplete" in decision.decision_reason


def test_finding_without_limitations_is_rejected() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_FINDING_MISSING_LIMITATIONS)

    assert decision.input_type is InputType.FINDING
    assert decision.eligibility_status is EligibilityStatus.INELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.limitations_acknowledged is False
    assert "limitations are missing" in decision.decision_reason


def test_well_formed_finding_is_eligible_without_hypothesis_falsification_requirements() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_FINDING_ELIGIBLE)

    assert decision.input_type is InputType.FINDING
    assert decision.eligibility_status is EligibilityStatus.ELIGIBLE_FOR_STRATEGY_DESIGN
    assert decision.eligible_for_strategy_design is True
    assert decision.source_status == "promoted_to_quality_review"
    assert decision.source_status_admissible is True
    assert decision.traceability_complete is True
    assert decision.limitations_acknowledged is True
    assert decision.falsification_criteria_present is None
    assert decision.decision_reason == "eligible for conceptual strategy design only"


def test_findings_and_hypotheses_are_evaluated_as_distinct_input_types() -> None:
    finding_decision = decide_strategy_input_eligibility(FICTITIOUS_FINDING_ELIGIBLE)
    hypothesis_decision = decide_strategy_input_eligibility(FICTITIOUS_HYPOTHESIS_ELIGIBLE)

    assert finding_decision.input_type is InputType.FINDING
    assert hypothesis_decision.input_type is InputType.HYPOTHESIS
    assert finding_decision.falsification_criteria_present is None
    assert hypothesis_decision.falsification_criteria_present is True


def test_contract_outputs_are_only_eligibility_decisions() -> None:
    decision = decide_strategy_input_eligibility(FICTITIOUS_HYPOTHESIS_ELIGIBLE)

    assert decision.__class__.__name__ == "StrategyInputEligibilityDecision"
    assert not hasattr(decision, "signal_id")
    assert not hasattr(decision, "rule_id")
    assert not hasattr(decision, "strategy_candidate_id")
    assert not hasattr(decision, "pnl")
    assert not hasattr(decision, "sharpe")
    assert not hasattr(decision, "order")
