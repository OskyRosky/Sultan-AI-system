"""Fictitious mockups for Strategy Composition.

These mockups are synthetic governance examples only. They are not real
strategy candidates, do not represent edge, and must not be interpreted as
risk-managed systems, registry entries, backtests, orders, or performance
claims.
"""

from __future__ import annotations

from datetime import datetime, timezone

from candidates.strategy_candidate import create_strategy_candidate
from mockups.rule_definition_mockups import FICTITIOUS_RULE_DEFINITION


MOCK_CANDIDATE_CREATED_AT = datetime(2026, 1, 5, tzinfo=timezone.utc)

FICTITIOUS_STRATEGY_CANDIDATE = create_strategy_candidate(
    candidate_id="mock-candidate-001",
    rule_definitions=(FICTITIOUS_RULE_DEFINITION,),
    composition_summary="Synthetic candidate composition; not a real strategy.",
    composition_rationale=(
        "Synthetic rationale for grouping fictitious rule definitions before "
        "future risk-template assignment."
    ),
    assumptions=("Synthetic candidate assumption; not real research.",),
    limitations=("Synthetic candidate limitation; not real edge.",),
    conflict_notes=("Synthetic note: no real conflict analysis performed.",),
    falsification_references=("Synthetic candidate falsification reference.",),
    audit_reference="mock-audit-candidate-001",
    created_at=MOCK_CANDIDATE_CREATED_AT,
)
