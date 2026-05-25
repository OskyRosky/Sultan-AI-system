"""Fictitious mockups for Strategy Dossier & Handoff.

These mockups are synthetic documentation examples only. They are not real
dossiers, do not execute handoff, do not represent edge, and must not be
interpreted as backtest authorization, deployment, or trading approval.
"""

from __future__ import annotations

from datetime import datetime, timezone

from mockups.strategy_closure_mockups import FICTITIOUS_STRATEGY_CLOSURE_RECORD
from reports.strategy_dossier import (
    DossierSectionType,
    create_dossier_section,
    create_strategy_dossier,
)


MOCK_STRATEGY_DOSSIER_PREPARED_AT = datetime(2026, 1, 10, tzinfo=timezone.utc)

FICTITIOUS_DOSSIER_SECTIONS = tuple(
    create_dossier_section(
        section_id=f"mock-dossier-section-{section_type.value}",
        section_type=section_type,
        title=f"Synthetic {section_type.value.replace('_', ' ').title()}",
        content_summary=(
            "Synthetic dossier section; documentation packaging only."
        ),
        audit_reference=f"mock-audit-dossier-section-{section_type.value}",
    )
    for section_type in DossierSectionType
)

FICTITIOUS_STRATEGY_DOSSIER = create_strategy_dossier(
    dossier_id="mock-strategy-dossier-001",
    closure_record=FICTITIOUS_STRATEGY_CLOSURE_RECORD,
    sections=FICTITIOUS_DOSSIER_SECTIONS,
    downstream_review_questions=(
        "Synthetic downstream question; no backtest has been authorized.",
    ),
    pending_requirements=(
        "Synthetic pending requirement; final audit required before any downstream use.",
    ),
    assumptions=("Synthetic dossier assumption; no real candidate approval.",),
    limitations=("Synthetic dossier limitation; no empirical validation.",),
    non_approval_statement=(
        "Synthetic dossier does not authorize trading, backtesting, deployment, "
        "capital allocation, edge, profitability, or strategy validation."
    ),
    audit_reference="mock-audit-strategy-dossier-001",
    prepared_at=MOCK_STRATEGY_DOSSIER_PREPARED_AT,
)

