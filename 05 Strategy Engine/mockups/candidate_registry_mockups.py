"""Fictitious mockups for Strategy Candidate Registry.

These mockups are synthetic governance examples only. They are not real
registered candidates, do not represent edge, and must not be interpreted as
quality approval, closure, backtest authorization, deployment, or trading
approval.
"""

from __future__ import annotations

from datetime import datetime, timezone

from candidates.candidate_registry import create_registry, create_registry_entry
from mockups.risk_template_mockups import FICTITIOUS_RISK_TEMPLATE
from mockups.strategy_candidate_mockups import FICTITIOUS_STRATEGY_CANDIDATE


MOCK_REGISTRY_CREATED_AT = datetime(2026, 1, 7, tzinfo=timezone.utc)

FICTITIOUS_REGISTRY_ENTRY = create_registry_entry(
    entry_id="mock-registry-entry-001",
    strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
    risk_template=FICTITIOUS_RISK_TEMPLATE,
    assumptions=("Synthetic registry assumption; not real approval.",),
    limitations=("Synthetic registry limitation; no validation implied.",),
    falsification_references=("Synthetic registry falsification reference.",),
    audit_reference="mock-audit-registry-entry-001",
    registered_at=MOCK_REGISTRY_CREATED_AT,
)

FICTITIOUS_REGISTRY = create_registry((FICTITIOUS_REGISTRY_ENTRY,))
