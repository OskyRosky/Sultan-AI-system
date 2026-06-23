from __future__ import annotations

from pathlib import Path
import sys


STAGE08_SRC = Path(__file__).resolve().parents[1] / "src"
if str(STAGE08_SRC) not in sys.path:
    sys.path.insert(0, str(STAGE08_SRC))

from dry_run import run_stage08_dry_run  # noqa: E402


def test_stage08_dry_run_produces_risk_decision() -> None:
    result = run_stage08_dry_run()

    assert result.input_package.artifact_type == "RiskHandoffPackage"
    assert len(result.gate_results) == 6
    assert result.risk_decision.risk_decision_status == "blocked"
    assert result.risk_decision.operational_status == "non_operational"
    assert result.risk_decision.risk_approval is False
    assert result.audit_trace.stage_id == "08 Risk Engine"


def test_stage08_dry_run_is_deterministic() -> None:
    first = run_stage08_dry_run()
    second = run_stage08_dry_run()

    assert first == second
    assert first.to_dict() == second.to_dict()


def test_stage08_blocks_framework_only_input() -> None:
    result = run_stage08_dry_run()

    assert "framework_only_input" in result.risk_decision.reason_codes
    assert "framework_only_input" in result.risk_decision.blocking_gaps


def test_stage08_blocks_confidence_not_available() -> None:
    result = run_stage08_dry_run()

    assert "confidence_not_available" in result.risk_decision.reason_codes
    assert result.risk_decision.risk_approval is False


def test_stage08_blocks_missing_empirical_evidence() -> None:
    result = run_stage08_dry_run()

    assert "empirical_evidence_not_available" in result.risk_decision.reason_codes
    assert "empirical_evidence_not_available" in result.risk_decision.blocking_gaps


def test_stage08_blocks_strategy_not_promoted() -> None:
    result = run_stage08_dry_run()

    assert "strategy_not_promoted" in result.risk_decision.reason_codes
    assert "strategy_not_promoted" in result.risk_decision.blocking_gaps
