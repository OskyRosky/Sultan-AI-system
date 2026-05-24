"""Fictitious mockups for Risk Template Layer.

These mockups are synthetic governance examples only. They are not calibrated
risk models, do not represent safety or edge, and must not be interpreted as
capital policy, sizing, stops, leverage, backtests, or trading approval.
"""

from __future__ import annotations

from datetime import datetime, timezone

from mockups.strategy_candidate_mockups import FICTITIOUS_STRATEGY_CANDIDATE
from risk_templates.risk_template import RiskDimension, create_risk_template


MOCK_RISK_TEMPLATE_CREATED_AT = datetime(2026, 1, 6, tzinfo=timezone.utc)

FICTITIOUS_RISK_TEMPLATE = create_risk_template(
    template_id="mock-risk-template-001",
    strategy_candidate=FICTITIOUS_STRATEGY_CANDIDATE,
    risk_dimensions=(
        RiskDimension.MARKET_EXPOSURE,
        RiskDimension.LIQUIDITY,
        RiskDimension.REGIME_DEPENDENCY,
    ),
    constraint_intent=(
        "Synthetic risk intent; identifies future risk review dimensions only."
    ),
    exclusion_criteria=("Synthetic exclusion criterion; not an operational control.",),
    assumptions=("Synthetic risk assumption; not calibrated.",),
    limitations=("Synthetic risk limitation; no real protection implied.",),
    non_calibrated_rationale=(
        "Synthetic template is uncalibrated because no real data or backtesting is used."
    ),
    audit_reference="mock-audit-risk-template-001",
    created_at=MOCK_RISK_TEMPLATE_CREATED_AT,
)
