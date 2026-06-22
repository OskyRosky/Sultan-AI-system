from __future__ import annotations

from pathlib import Path
import sys


STAGE07_SRC = Path(__file__).resolve().parents[1] / "src"
if str(STAGE07_SRC) not in sys.path:
    sys.path.insert(0, str(STAGE07_SRC))

from dry_run import default_mock_payload, run_stage07_dry_run  # noqa: E402


def test_stage07_dry_run_produces_expected_artifacts() -> None:
    result = run_stage07_dry_run()

    assert result.normalized_motor_a_input.source_motor == "MotorA"
    assert result.normalized_motor_b_input.source_motor == "MotorB"
    assert result.normalized_motor_c_input.source_motor == "MotorC"
    assert len(result.normalized_signal_candidates) == 3
    assert result.fused_signal_candidate.signal_scope == "dry_run_contract_validation"
    assert result.confidence_governance_result.confidence_reason == (
        "dry_run_contract_validation_only"
    )
    assert result.risk_handoff_package.target_stage == "08 Risk Engine"
    assert result.audit_trace.stage_id == "07 Signal Fusion + LLM Motors"


def test_stage07_dry_run_is_deterministic() -> None:
    first = run_stage07_dry_run()
    second = run_stage07_dry_run()

    assert first == second
    assert first.to_dict() == second.to_dict()


def test_stage07_llm_mock_does_not_create_evidence() -> None:
    payload = default_mock_payload()
    payload["motor_c"] = {
        **payload["motor_c"],
        "classification_confidence_status": "classification_confidence_available",
        "classification_confidence_score": 0.99,
    }

    result = run_stage07_dry_run(payload)

    assert result.normalized_motor_c_input.classification_confidence_score == 0.99
    assert result.confidence_governance_result.empirical_results_available is False
    assert result.confidence_governance_result.confidence_status == "confidence_not_available"
    assert result.confidence_governance_result.confidence_score is None
    assert result.confidence_governance_result.final_signal_confidence_score is None
    assert result.risk_handoff_package.empirical_results_available is False


def test_stage07_risk_handoff_package_targets_stage08_only() -> None:
    result = run_stage07_dry_run()

    assert result.risk_handoff_package.target_stage == "08 Risk Engine"
    assert result.risk_handoff_package.handoff_to_09 == "blocked"
    assert result.risk_handoff_package.risk_handoff_status == "blocked"


def test_stage07_no_strategy_promotion() -> None:
    result = run_stage07_dry_run()

    assert result.fused_signal_candidate.promotion_status == "not_promoted"
    assert result.confidence_governance_result.strategy_promotion_status == "not_promoted"
    assert result.risk_handoff_package.strategy_promotion_status == "not_promoted"

