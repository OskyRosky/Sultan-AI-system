"""Fictitious mockups for Regime Context Framing.

These mockups are synthetic governance examples only. They are not real
regimes, do not represent edge, and must not be interpreted as rules, strategy
candidates, filters, market timing, or performance claims.
"""

from __future__ import annotations

from datetime import datetime, timezone

from mockups.signal_definition_mockups import FICTITIOUS_SIGNAL_DEFINITION
from regimes.regime_context import RegimeType, create_regime_context_frame


MOCK_REGIME_FRAME_CREATED_AT = datetime(2026, 1, 3, tzinfo=timezone.utc)

FICTITIOUS_REGIME_CONTEXT_FRAME = create_regime_context_frame(
    frame_id="mock-regime-frame-001",
    signal_definition=FICTITIOUS_SIGNAL_DEFINITION,
    regime_type=RegimeType.VOLATILITY,
    regime_label="mock_high_vol_context",
    context_description="Synthetic volatility context; not calculated from real data.",
    applicability_rationale=(
        "Synthetic rationale explaining why this fictitious signal should be "
        "framed with a volatility context."
    ),
    assumptions=("Synthetic regime assumption; not real market evidence.",),
    limitations=("Synthetic regime limitation; not real edge.",),
    falsification_references=("Synthetic regime falsification reference.",),
    audit_reference="mock-audit-regime-frame-001",
    created_at=MOCK_REGIME_FRAME_CREATED_AT,
)
