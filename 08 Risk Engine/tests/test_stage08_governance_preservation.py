from __future__ import annotations

from pathlib import Path
import sys


STAGE08_SRC = Path(__file__).resolve().parents[1] / "src"
if str(STAGE08_SRC) not in sys.path:
    sys.path.insert(0, str(STAGE08_SRC))

from dry_run import run_stage08_dry_run  # noqa: E402


def test_stage08_preserves_paper_trading_blocked() -> None:
    result = run_stage08_dry_run()

    assert result.input_package.paper_trading_ready is False
    assert result.risk_decision.paper_trading_ready is False
    assert "paper_trading_blocked" in result.risk_decision.reason_codes


def test_stage08_preserves_handoff_to_09_blocked() -> None:
    result = run_stage08_dry_run()

    assert result.input_package.handoff_to_09 == "blocked"
    assert result.risk_decision.handoff_to_09 == "blocked"
    assert result.risk_decision.stage_09_operational_start_allowed is False


def test_stage08_forbidden_downstream_usage_present() -> None:
    result = run_stage08_dry_run()

    assert "paper_trading" in result.risk_decision.forbidden_downstream_usage
    assert "stage_09_unlock" in result.risk_decision.forbidden_downstream_usage
    assert "forbidden_downstream_usage_present" in result.risk_decision.blocking_gaps


def test_stage08_non_approval_statement_present() -> None:
    result = run_stage08_dry_run()

    assert "not real risk approval" in result.risk_decision.non_approval_statement
    assert "not Stage 09 readiness" in result.risk_decision.non_approval_statement


def test_stage08_no_capital_allocation_ready() -> None:
    result = run_stage08_dry_run()

    assert result.risk_decision.capital_allocation_ready is False
    assert result.risk_decision.risk_approval is False


def test_stage08_no_live_trading_ready() -> None:
    result = run_stage08_dry_run()

    assert result.risk_decision.live_trading_ready is False
    assert result.risk_decision.downstream_operational_eligibility == "blocked"
