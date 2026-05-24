"""Fictitious mockups for Strategy Closure.

These mockups are synthetic internal closure examples only. They are not real
closed strategies, do not represent edge, and must not be interpreted as
dossier handoff, backtest authorization, deployment, or trading approval.
"""

from __future__ import annotations

from datetime import datetime, timezone

from mockups.quality_gate_mockups import FICTITIOUS_QUALITY_GATE_ASSESSMENT
from reports.strategy_closure import create_strategy_closure_record


MOCK_STRATEGY_CLOSURE_CLOSED_AT = datetime(2026, 1, 9, tzinfo=timezone.utc)

FICTITIOUS_STRATEGY_CLOSURE_RECORD = create_strategy_closure_record(
    closure_id="mock-strategy-closure-001",
    quality_assessment=FICTITIOUS_QUALITY_GATE_ASSESSMENT,
    closure_summary=(
        "Synthetic closure summary; internal governance completion only."
    ),
    assumptions=("Synthetic closure assumption; no real approval.",),
    limitations=("Synthetic closure limitation; no dossier or backtest authorization.",),
    non_approval_statement=(
        "Synthetic closure does not authorize trading, backtesting, deployment, "
        "capital allocation, edge, profitability, or strategy validation."
    ),
    audit_reference="mock-audit-strategy-closure-001",
    closed_at=MOCK_STRATEGY_CLOSURE_CLOSED_AT,
)

