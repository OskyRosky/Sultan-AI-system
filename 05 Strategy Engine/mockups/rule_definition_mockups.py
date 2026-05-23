"""Fictitious mockups for Rule Construction.

These mockups are synthetic governance examples only. They are not real rules,
do not represent edge, and must not be interpreted as strategy candidates,
orders, trades, execution logic, risk controls, or performance claims.
"""

from __future__ import annotations

from datetime import datetime, timezone

from mockups.regime_context_mockups import FICTITIOUS_REGIME_CONTEXT_FRAME
from rules.rule_definition import RuleCategory, create_rule_definition


MOCK_RULE_CREATED_AT = datetime(2026, 1, 4, tzinfo=timezone.utc)

FICTITIOUS_RULE_DEFINITION = create_rule_definition(
    rule_id="mock-rule-001",
    signal_definition=FICTITIOUS_REGIME_CONTEXT_FRAME.signal_definition,
    regime_context_frame=FICTITIOUS_REGIME_CONTEXT_FRAME,
    rule_category=RuleCategory.ENTRY_CONDITION,
    rule_statement="Synthetic declarative interpretation; not an executable entry rule.",
    interpretation_guidance=(
        "Synthetic guidance for future design review only; not trading logic."
    ),
    assumptions=("Synthetic rule assumption; not real research.",),
    limitations=("Synthetic rule limitation; not real edge.",),
    falsification_references=("Synthetic rule falsification reference.",),
    audit_reference="mock-audit-rule-001",
    created_at=MOCK_RULE_CREATED_AT,
)
