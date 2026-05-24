from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import pytest


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from candidates.strategy_candidate import CandidateStatus  # noqa: E402
from mockups.risk_template_mockups import (  # noqa: E402
    FICTITIOUS_RISK_TEMPLATE,
    MOCK_RISK_TEMPLATE_CREATED_AT,
)
from mockups.signal_definition_mockups import FICTITIOUS_SIGNAL_DEFINITION  # noqa: E402
from mockups.strategy_candidate_mockups import FICTITIOUS_STRATEGY_CANDIDATE  # noqa: E402
from risk_templates.risk_template import (  # noqa: E402
    CalibrationStatus,
    RiskDimension,
    create_risk_template,
)


def test_valid_risk_template_requires_pending_strategy_candidate() -> None:
    template = create_risk_template(
        template_id="mock-risk-template-valid",
        strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
        risk_dimensions=(RiskDimension.MARKET_EXPOSURE, RiskDimension.VOLATILITY),
        constraint_intent="Synthetic constraint intent.",
        exclusion_criteria=("Synthetic exclusion criterion.",),
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        non_calibrated_rationale="Synthetic rationale for uncalibrated status.",
        audit_reference="mock-audit-risk-template-valid",
        created_at=MOCK_RISK_TEMPLATE_CREATED_AT,
    )

    assert template.template_id == "mock-risk-template-valid"
    assert template.strategy_candidate is FICTITIOUS_STRATEGY_CANDIDATE
    assert template.calibration_status is CalibrationStatus.UNCALIBRATED
    assert template.strategy_candidate.status is CandidateStatus.PENDING_RISK_TEMPLATE


def test_non_candidate_origin_is_rejected() -> None:
    with pytest.raises(ValueError, match="must reference a valid strategy candidate"):
        create_risk_template(
            template_id="mock-risk-template-bad-origin",
            strategy_candidate=FICTITIOUS_SIGNAL_DEFINITION,
            risk_dimensions=(RiskDimension.MARKET_EXPOSURE,),
            constraint_intent="Synthetic constraint intent.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            non_calibrated_rationale="Synthetic rationale.",
            audit_reference="mock-audit-risk-template-bad-origin",
        )


def test_candidate_not_pending_risk_template_is_rejected() -> None:
    candidate = replace(FICTITIOUS_STRATEGY_CANDIDATE, status=CandidateStatus.COMPOSED)

    with pytest.raises(ValueError, match="must be pending_risk_template"):
        create_risk_template(
            template_id="mock-risk-template-bad-candidate-status",
            strategy_candidate=candidate,
            risk_dimensions=(RiskDimension.MARKET_EXPOSURE,),
            constraint_intent="Synthetic constraint intent.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            non_calibrated_rationale="Synthetic rationale.",
            audit_reference="mock-audit-risk-template-bad-candidate-status",
        )


def test_empty_risk_dimensions_are_rejected() -> None:
    with pytest.raises(ValueError, match="risk_dimensions must contain at least one dimension"):
        create_risk_template(
            template_id="mock-risk-template-empty-dimensions",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_dimensions=(),
            constraint_intent="Synthetic constraint intent.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            non_calibrated_rationale="Synthetic rationale.",
            audit_reference="mock-audit-risk-template-empty-dimensions",
        )


def test_invalid_risk_dimensions_are_rejected() -> None:
    with pytest.raises(TypeError, match="RiskDimension"):
        create_risk_template(
            template_id="mock-risk-template-invalid-dimension",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_dimensions=("market_exposure",),
            constraint_intent="Synthetic constraint intent.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            non_calibrated_rationale="Synthetic rationale.",
            audit_reference="mock-audit-risk-template-invalid-dimension",
        )


def test_unsupported_calibration_status_is_rejected() -> None:
    with pytest.raises(TypeError, match="calibration_status must be a CalibrationStatus"):
        create_risk_template(
            template_id="mock-risk-template-bad-calibration",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_dimensions=(RiskDimension.MARKET_EXPOSURE,),
            constraint_intent="Synthetic constraint intent.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            non_calibrated_rationale="Synthetic rationale.",
            audit_reference="mock-audit-risk-template-bad-calibration",
            calibration_status="calibrated",
        )


def test_required_governance_fields_are_enforced() -> None:
    with pytest.raises(ValueError, match="constraint_intent must be a non-empty string"):
        create_risk_template(
            template_id="mock-risk-template-missing-intent",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_dimensions=(RiskDimension.MARKET_EXPOSURE,),
            constraint_intent="",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            non_calibrated_rationale="Synthetic rationale.",
            audit_reference="mock-audit-risk-template-missing-intent",
        )

    with pytest.raises(ValueError, match="assumptions must contain at least one item"):
        create_risk_template(
            template_id="mock-risk-template-missing-assumptions",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_dimensions=(RiskDimension.MARKET_EXPOSURE,),
            constraint_intent="Synthetic constraint intent.",
            assumptions=(),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            non_calibrated_rationale="Synthetic rationale.",
            audit_reference="mock-audit-risk-template-missing-assumptions",
        )

    with pytest.raises(ValueError, match="limitations must contain at least one item"):
        create_risk_template(
            template_id="mock-risk-template-missing-limitations",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_dimensions=(RiskDimension.MARKET_EXPOSURE,),
            constraint_intent="Synthetic constraint intent.",
            assumptions=("Synthetic assumption.",),
            limitations=(),
            falsification_references=("Synthetic falsification reference.",),
            non_calibrated_rationale="Synthetic rationale.",
            audit_reference="mock-audit-risk-template-missing-limitations",
        )

    with pytest.raises(ValueError, match="falsification_references must contain at least one item"):
        create_risk_template(
            template_id="mock-risk-template-missing-falsification",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_dimensions=(RiskDimension.MARKET_EXPOSURE,),
            constraint_intent="Synthetic constraint intent.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=(),
            non_calibrated_rationale="Synthetic rationale.",
            audit_reference="mock-audit-risk-template-missing-falsification",
        )

    with pytest.raises(ValueError, match="non_calibrated_rationale must be a non-empty string"):
        create_risk_template(
            template_id="mock-risk-template-missing-rationale",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_dimensions=(RiskDimension.MARKET_EXPOSURE,),
            constraint_intent="Synthetic constraint intent.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            non_calibrated_rationale="",
            audit_reference="mock-audit-risk-template-missing-rationale",
        )

    with pytest.raises(ValueError, match="audit_reference must be a non-empty string"):
        create_risk_template(
            template_id="mock-risk-template-missing-audit",
            strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
            risk_dimensions=(RiskDimension.MARKET_EXPOSURE,),
            constraint_intent="Synthetic constraint intent.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            non_calibrated_rationale="Synthetic rationale.",
            audit_reference="",
        )


def test_risk_template_preserves_candidate_rule_regime_signal_hypothesis_chain() -> None:
    template = FICTITIOUS_RISK_TEMPLATE
    candidate = template.strategy_candidate
    rule = candidate.rule_definitions[0]

    assert candidate.status is CandidateStatus.PENDING_RISK_TEMPLATE
    assert rule.regime_context_frame.signal_definition is rule.signal_definition
    assert rule.signal_definition.source_hypothesis_decision.input_type.value == "hypothesis"
    assert rule.signal_definition.source_hypothesis_decision.eligible_for_strategy_design is True


def test_risk_template_does_not_expose_future_block_operational_or_performance_fields() -> None:
    template = FICTITIOUS_RISK_TEMPLATE

    assert not hasattr(template, "registry_status")
    assert not hasattr(template, "quality_gate_status")
    assert not hasattr(template, "backtest_result")
    assert not hasattr(template, "pnl")
    assert not hasattr(template, "drawdown")
    assert not hasattr(template, "hit_rate")
    assert not hasattr(template, "sharpe")
    assert not hasattr(template, "sortino")
    assert not hasattr(template, "calmar")
    assert not hasattr(template, "position_size")
    assert not hasattr(template, "capital_allocation")
    assert not hasattr(template, "stop_loss")
    assert not hasattr(template, "take_profit")
    assert not hasattr(template, "leverage")
    assert not hasattr(template, "order")
    assert not hasattr(template, "execution")
