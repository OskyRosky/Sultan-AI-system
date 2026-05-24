"""Fictitious mockups for Strategy Quality Gates.

These mockups are synthetic governance examples only. They are not real
quality approvals, do not represent edge, and must not be interpreted as
closure, dossier readiness, backtest authorization, deployment, or trading
approval.
"""

from __future__ import annotations

from datetime import datetime, timezone

from mockups.candidate_registry_mockups import FICTITIOUS_REGISTRY_ENTRY
from quality.quality_gates import (
    QualityGateType,
    create_quality_gate_assessment,
    create_quality_gate_result,
)


MOCK_QUALITY_ASSESSED_AT = datetime(2026, 1, 8, tzinfo=timezone.utc)

FICTITIOUS_PASSING_GATE_RESULTS = tuple(
    create_quality_gate_result(
        gate_id=f"mock-quality-gate-{gate_type.value}",
        gate_type=gate_type,
        passed=True,
        assessment_summary=(
            "Synthetic quality gate result; structural governance only."
        ),
        limitations=("Synthetic limitation; no empirical validation implied.",),
        audit_reference=f"mock-audit-quality-gate-{gate_type.value}",
    )
    for gate_type in QualityGateType
)

FICTITIOUS_QUALITY_GATE_ASSESSMENT = create_quality_gate_assessment(
    assessment_id="mock-quality-assessment-001",
    registry_entry=FICTITIOUS_REGISTRY_ENTRY,
    gate_results=FICTITIOUS_PASSING_GATE_RESULTS,
    assumptions=("Synthetic quality assumption; no real candidate approval.",),
    limitations=("Synthetic quality limitation; no performance validation.",),
    non_approval_statement=(
        "Synthetic assessment does not approve trading, backtesting, deployment, "
        "capital allocation, edge, profitability, or strategy validation."
    ),
    audit_reference="mock-audit-quality-assessment-001",
    assessed_at=MOCK_QUALITY_ASSESSED_AT,
)

