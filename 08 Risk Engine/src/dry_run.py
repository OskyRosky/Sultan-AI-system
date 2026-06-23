from __future__ import annotations

from typing import Any

from audit_trace import create_audit_trace
from contracts import Stage08DryRunResult
from decision_engine import build_risk_decision
from gates import run_conservative_gates
from intake import validate_stage07_risk_handoff_package


def run_stage08_dry_run(stage07_payload: dict[str, Any] | None = None) -> Stage08DryRunResult:
    payload = default_stage07_risk_handoff_payload() if stage07_payload is None else stage07_payload
    input_package = validate_stage07_risk_handoff_package(payload)
    gate_results = run_conservative_gates(input_package)
    risk_decision = build_risk_decision(input_package, gate_results)
    audit_trace = create_audit_trace(input_package, gate_results, risk_decision)
    return Stage08DryRunResult(
        input_package=input_package,
        gate_results=gate_results,
        risk_decision=risk_decision,
        audit_trace=audit_trace,
    )


def default_stage07_risk_handoff_payload() -> dict[str, Any]:
    return {
        "risk_handoff_package_id": "risk-handoff-package-stage07-mock-001",
        "target_stage": "08 Risk Engine",
        "related_fused_signal_candidate_id": "fused-signal-candidate-mock-001",
        "related_confidence_governance_result_id": "confidence-governance-mock-001",
        "risk_handoff_status": "blocked",
        "paper_trading_ready": False,
        "handoff_to_09": "blocked",
        "downstream_operational_eligibility": "blocked",
        "strategy_promotion_status": "not_promoted",
        "evidence_completeness_level": "framework_only",
        "empirical_results_available": False,
        "confidence_status": "confidence_not_available",
        "confidence_score": None,
        "final_signal_confidence_score": None,
        "blocking_gaps": (
            "missing_real_empirical_evidence",
            "oos_not_available",
            "walk_forward_not_available",
            "robustness_not_available",
            "confidence_not_available",
            "paper_trading_blocked",
            "stage07_dry_run_only_not_operational",
        ),
        "forbidden_downstream_usage": (
            "paper_trading",
            "live_trading",
            "capital_allocation",
            "strategy_promotion",
            "confidence_generation",
            "evidence_claims",
            "production_signal_routing",
            "stage_09_unlock",
        ),
        "non_approval_statement": (
            "Stage 07 minimal dry-run is V1 contract validation only: not empirical "
            "evidence, not strategy validation, not confidence, not paper trading "
            "readiness, not production readiness, and not Stage 09 readiness."
        ),
    }
