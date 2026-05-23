from __future__ import annotations

from pathlib import Path
import sys

import pytest


STRATEGY_ENGINE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STRATEGY_ENGINE_ROOT))

from mockups.regime_context_mockups import (  # noqa: E402
    FICTITIOUS_REGIME_CONTEXT_FRAME,
    MOCK_REGIME_FRAME_CREATED_AT,
)
from mockups.signal_definition_mockups import (  # noqa: E402
    FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
    FICTITIOUS_SIGNAL_DEFINITION,
)
from regimes.regime_context import RegimeType, create_regime_context_frame  # noqa: E402


def test_valid_regime_context_frame_requires_valid_signal_definition() -> None:
    frame = create_regime_context_frame(
        frame_id="mock-regime-frame-valid",
        signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
        regime_type=RegimeType.TREND,
        regime_label="mock_bullish_context",
        context_description="Synthetic trend context.",
        applicability_rationale="Synthetic rationale for contextual framing.",
        assumptions=("Synthetic assumption.",),
        limitations=("Synthetic limitation.",),
        falsification_references=("Synthetic falsification reference.",),
        audit_reference="mock-audit-regime-frame-valid",
        created_at=MOCK_REGIME_FRAME_CREATED_AT,
    )

    assert frame.frame_id == "mock-regime-frame-valid"
    assert frame.signal_definition is FICTITIOUS_SIGNAL_DEFINITION
    assert frame.regime_type is RegimeType.TREND
    assert frame.regime_label == "mock_bullish_context"


def test_non_signal_origin_is_rejected() -> None:
    with pytest.raises(ValueError, match="must originate from a valid signal definition"):
        create_regime_context_frame(
            frame_id="mock-regime-frame-bad-origin",
            signal_definition=FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
            regime_type=RegimeType.VOLATILITY,
            regime_label="mock_high_vol_context",
            context_description="Synthetic context.",
            applicability_rationale="Synthetic rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-regime-frame-bad-origin",
        )


def test_unsupported_regime_type_is_rejected() -> None:
    with pytest.raises(TypeError, match="regime_type must be a RegimeType"):
        create_regime_context_frame(
            frame_id="mock-regime-frame-bad-type",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_type="volatility",
            regime_label="mock_high_vol_context",
            context_description="Synthetic context.",
            applicability_rationale="Synthetic rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-regime-frame-bad-type",
        )


def test_required_governance_fields_are_enforced() -> None:
    with pytest.raises(ValueError, match="context_description must be a non-empty string"):
        create_regime_context_frame(
            frame_id="mock-regime-frame-missing-context",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_type=RegimeType.RANGE,
            regime_label="mock_range_context",
            context_description="",
            applicability_rationale="Synthetic rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-regime-frame-missing-context",
        )

    with pytest.raises(ValueError, match="applicability_rationale must be a non-empty string"):
        create_regime_context_frame(
            frame_id="mock-regime-frame-missing-rationale",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_type=RegimeType.RANGE,
            regime_label="mock_range_context",
            context_description="Synthetic context.",
            applicability_rationale="",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-regime-frame-missing-rationale",
        )

    with pytest.raises(ValueError, match="assumptions must contain at least one item"):
        create_regime_context_frame(
            frame_id="mock-regime-frame-missing-assumptions",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_type=RegimeType.RANGE,
            regime_label="mock_range_context",
            context_description="Synthetic context.",
            applicability_rationale="Synthetic rationale.",
            assumptions=(),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-regime-frame-missing-assumptions",
        )

    with pytest.raises(ValueError, match="limitations must contain at least one item"):
        create_regime_context_frame(
            frame_id="mock-regime-frame-missing-limitations",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_type=RegimeType.RANGE,
            regime_label="mock_range_context",
            context_description="Synthetic context.",
            applicability_rationale="Synthetic rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=(),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="mock-audit-regime-frame-missing-limitations",
        )

    with pytest.raises(ValueError, match="falsification_references must contain at least one item"):
        create_regime_context_frame(
            frame_id="mock-regime-frame-missing-falsification",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_type=RegimeType.RANGE,
            regime_label="mock_range_context",
            context_description="Synthetic context.",
            applicability_rationale="Synthetic rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=(),
            audit_reference="mock-audit-regime-frame-missing-falsification",
        )

    with pytest.raises(ValueError, match="audit_reference must be a non-empty string"):
        create_regime_context_frame(
            frame_id="mock-regime-frame-missing-audit",
            signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
            regime_type=RegimeType.RANGE,
            regime_label="mock_range_context",
            context_description="Synthetic context.",
            applicability_rationale="Synthetic rationale.",
            assumptions=("Synthetic assumption.",),
            limitations=("Synthetic limitation.",),
            falsification_references=("Synthetic falsification reference.",),
            audit_reference="",
        )


def test_regime_context_preserves_signal_eligibility_chain() -> None:
    frame = FICTITIOUS_REGIME_CONTEXT_FRAME

    signal = frame.signal_definition
    assert signal.source_hypothesis_decision.input_type.value == "hypothesis"
    assert signal.source_hypothesis_decision.eligible_for_strategy_design is True
    assert frame.signal_definition is signal


def test_regime_context_does_not_expose_rules_or_performance_fields() -> None:
    frame = FICTITIOUS_REGIME_CONTEXT_FRAME

    assert not hasattr(frame, "entry_rule")
    assert not hasattr(frame, "exit_rule")
    assert not hasattr(frame, "filter_rule")
    assert not hasattr(frame, "strategy_candidate_id")
    assert not hasattr(frame, "regime_switch")
    assert not hasattr(frame, "position_size")
    assert not hasattr(frame, "pnl")
    assert not hasattr(frame, "sharpe")
    assert not hasattr(frame, "sortino")
    assert not hasattr(frame, "calmar")
