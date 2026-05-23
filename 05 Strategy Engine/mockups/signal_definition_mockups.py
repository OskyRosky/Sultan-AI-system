"""Fictitious mockups for the Signal Definition Layer.

These mockups are synthetic governance examples only. They are not real
signals, do not represent edge, and must not be interpreted as rules, strategy
candidates, orders, trades, or performance claims.
"""

from __future__ import annotations

from datetime import datetime, timezone

from mockups.strategy_inputs_contract_mockups import (
    FICTITIOUS_EVIDENCE_INELIGIBLE,
    FICTITIOUS_FINDING_ELIGIBLE,
    FICTITIOUS_FINDING_UNADMISSIBLE_STATUS,
    FICTITIOUS_HYPOTHESIS_ELIGIBLE,
    FICTITIOUS_HYPOTHESIS_NONADMISSIBLE_STATUS,
)
from signals.signal_definition import SignalOrientation, create_signal_definition
from strategy.inputs_contract import decide_strategy_input_eligibility


MOCK_SIGNAL_CREATED_AT = datetime(2026, 1, 2, tzinfo=timezone.utc)

FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION = decide_strategy_input_eligibility(
    FICTITIOUS_HYPOTHESIS_ELIGIBLE,
    decided_at=MOCK_SIGNAL_CREATED_AT,
)

FICTITIOUS_NONELIGIBLE_HYPOTHESIS_DECISION = decide_strategy_input_eligibility(
    FICTITIOUS_HYPOTHESIS_NONADMISSIBLE_STATUS,
    decided_at=MOCK_SIGNAL_CREATED_AT,
)

FICTITIOUS_ELIGIBLE_FINDING_DECISION = decide_strategy_input_eligibility(
    FICTITIOUS_FINDING_ELIGIBLE,
    decided_at=MOCK_SIGNAL_CREATED_AT,
)

FICTITIOUS_NONELIGIBLE_FINDING_DECISION = decide_strategy_input_eligibility(
    FICTITIOUS_FINDING_UNADMISSIBLE_STATUS,
    decided_at=MOCK_SIGNAL_CREATED_AT,
)

FICTITIOUS_EVIDENCE_DECISION = decide_strategy_input_eligibility(
    FICTITIOUS_EVIDENCE_INELIGIBLE,
    decided_at=MOCK_SIGNAL_CREATED_AT,
)

FICTITIOUS_SIGNAL_DEFINITION = create_signal_definition(
    signal_id="mock-signal-001",
    source_hypothesis_decision=FICTITIOUS_ELIGIBLE_HYPOTHESIS_DECISION,
    supporting_finding_decisions=(FICTITIOUS_ELIGIBLE_FINDING_DECISION,),
    orientation=SignalOrientation.LONG_BIAS,
    observable_condition="Synthetic observable condition; not a real trading condition.",
    expected_behavior="Synthetic expected behavior inherited from a fictitious hypothesis.",
    assumptions=("Synthetic assumption; not real research.",),
    limitations=("Synthetic limitation; not real edge.",),
    falsification_references=("Synthetic falsification reference.",),
    audit_reference="mock-audit-signal-001",
    created_at=MOCK_SIGNAL_CREATED_AT,
)
