from __future__ import annotations

from pathlib import Path
import sys


STAGE07_SRC = Path(__file__).resolve().parents[1] / "src"
if str(STAGE07_SRC) not in sys.path:
    sys.path.insert(0, str(STAGE07_SRC))

from dry_run import default_mock_payload, run_stage07_dry_run  # noqa: E402


def test_stage07_preserves_paper_trading_blocked() -> None:
    result = run_stage07_dry_run()

    assert result.normalized_motor_b_input.paper_trading_ready is False
    assert result.fused_signal_candidate.paper_trading_ready is False
    assert result.confidence_governance_result.paper_trading_ready is False
    assert result.risk_handoff_package.paper_trading_ready is False


def test_stage07_handoff_to_09_never_approved() -> None:
    result = run_stage07_dry_run()

    assert result.normalized_motor_b_input.handoff_to_09 == "blocked"
    assert result.fused_signal_candidate.handoff_to_09 == "blocked"
    assert result.confidence_governance_result.handoff_to_09 == "blocked"
    assert result.risk_handoff_package.handoff_to_09 == "blocked"


def test_stage07_confidence_not_invented() -> None:
    result = run_stage07_dry_run()

    assert result.confidence_governance_result.confidence_status == "confidence_not_available"
    assert result.confidence_governance_result.confidence_score is None
    assert result.confidence_governance_result.final_signal_confidence_score is None
    assert result.risk_handoff_package.confidence_score is None
    assert result.risk_handoff_package.final_signal_confidence_score is None


def test_stage07_blocking_gaps_present_through_risk_handoff() -> None:
    result = run_stage07_dry_run()

    assert result.risk_handoff_package.blocking_gaps
    assert "confidence_not_available" in result.risk_handoff_package.blocking_gaps
    assert "stage07_dry_run_only_not_operational" in (
        result.risk_handoff_package.blocking_gaps
    )


def test_stage07_missing_null_fields_remain_blocked() -> None:
    payload = default_mock_payload()
    payload["motor_b"]["strategy_id"] = None

    result = run_stage07_dry_run(payload)

    assert result.normalized_motor_b_input.normalization_status == (
        "rejected_missing_required_fields_fail_closed"
    )
    assert "missing_strategy_id" in result.risk_handoff_package.blocking_gaps
    assert result.risk_handoff_package.paper_trading_ready is False
    assert result.risk_handoff_package.handoff_to_09 == "blocked"

