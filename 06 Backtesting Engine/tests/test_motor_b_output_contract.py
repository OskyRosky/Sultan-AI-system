from __future__ import annotations

from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
import sys

import pytest


BACKTESTING_ROOT = Path(__file__).resolve().parents[1]
if str(BACKTESTING_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKTESTING_ROOT))

from contracts.motor_b_output_contract import (  # noqa: E402
    AllowedDownstreamUsage,
    ConfidenceStatus,
    EvidenceCompletenessLevel,
    ForbiddenDownstreamUsage,
    PaperTradingEligibility,
    create_framework_only_motor_b_output_contract,
    validate_motor_b_output_contract,
)


def test_framework_only_contract_preserves_blocked_state() -> None:
    contract = create_framework_only_motor_b_output_contract(
        generated_at=datetime(2026, 6, 20, tzinfo=timezone.utc),
    )

    assert contract.evidence_completeness_level is EvidenceCompletenessLevel.FRAMEWORK_ONLY
    assert contract.paper_trading_eligibility is PaperTradingEligibility.BLOCKED
    assert contract.confidence_status is ConfidenceStatus.CONFIDENCE_NOT_AVAILABLE
    assert contract.confidence_score is None
    assert ForbiddenDownstreamUsage.PAPER_TRADING in contract.forbidden_downstream_usage
    assert ForbiddenDownstreamUsage.LIVE_TRADING in contract.forbidden_downstream_usage
    assert ForbiddenDownstreamUsage.CAPITAL_ALLOCATION in contract.forbidden_downstream_usage


def test_framework_only_contract_rejects_status_upgrade() -> None:
    contract = create_framework_only_motor_b_output_contract()
    upgraded = replace(
        contract,
        paper_trading_eligibility=PaperTradingEligibility.ELIGIBLE_FOR_FUTURE_REVIEW,
    )

    with pytest.raises(ValueError, match="framework_only requires paper_trading"):
        validate_motor_b_output_contract(upgraded)


def test_confidence_score_cannot_exist_when_confidence_unavailable() -> None:
    contract = create_framework_only_motor_b_output_contract()
    invalid = replace(contract, confidence_score=0.5)

    with pytest.raises(ValueError, match="confidence_not_available"):
        validate_motor_b_output_contract(invalid)


def test_blocked_contract_cannot_allow_paper_trading_usage() -> None:
    contract = create_framework_only_motor_b_output_contract()
    invalid = replace(
        contract,
        allowed_downstream_usage=(
            *contract.allowed_downstream_usage,
            AllowedDownstreamUsage.PAPER_TRADING_WITH_FULL_EVIDENCE,
        ),
    )

    with pytest.raises(ValueError, match="paper_trading_with_full_evidence"):
        validate_motor_b_output_contract(invalid)
