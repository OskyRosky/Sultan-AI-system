from __future__ import annotations

from typing import Any

from audit_trace import stable_hash
from contracts import (
    CONFIDENCE_SCORE,
    CONFIDENCE_STATUS,
    DEFAULT_BLOCKING_GAPS,
    DOWNSTREAM_OPERATIONAL_ELIGIBILITY,
    EMPIRICAL_RESULTS_AVAILABLE,
    EVIDENCE_COMPLETENESS_LEVEL,
    FINAL_SIGNAL_CONFIDENCE_SCORE,
    FORBIDDEN_DOWNSTREAM_USAGE,
    HANDOFF_TO_09,
    NON_APPROVAL_STATEMENT,
    PAPER_TRADING_READY,
    STRATEGY_PROMOTION_STATUS,
    MotorBRawDiagnosticsInputForStage07,
)


REQUIRED_HANDOFF_FIELDS = (
    "handoff_contract_id",
    "registry_record_id",
    "diagnostics_id",
    "simulation_id",
    "package_id",
    "strategy_id",
    "strategy_version",
    "snapshot_id",
    "output_scope",
    "diagnostics_scope",
    "registry_scope",
    "simulation_status",
    "handoff_scope",
    "non_approval_statement",
)


EXPECTED_SCOPE_VALUES = {
    "output_scope": "raw_execution_scaffold",
    "diagnostics_scope": "raw_scaffold_diagnostics_only",
    "registry_scope": "raw_diagnostics_registry_only",
    "handoff_scope": "raw_diagnostics_handoff_only",
    "simulation_status": "completed_raw_execution",
}


def adapt_motor_b_raw_diagnostics(
    raw_handoff: dict[str, Any] | MotorBRawDiagnosticsInputForStage07,
) -> MotorBRawDiagnosticsInputForStage07:
    if isinstance(raw_handoff, MotorBRawDiagnosticsInputForStage07):
        return raw_handoff
    if not isinstance(raw_handoff, dict):
        raise TypeError("Motor B raw diagnostics handoff must be a dict or adapter object")

    missing = tuple(field for field in REQUIRED_HANDOFF_FIELDS if raw_handoff.get(field) in (None, ""))
    scope_gaps = tuple(
        f"{field}_invalid"
        for field, expected in EXPECTED_SCOPE_VALUES.items()
        if raw_handoff.get(field) not in (None, expected)
    )
    blocking_gaps = tuple(
        sorted(
            set(DEFAULT_BLOCKING_GAPS)
            | {f"missing_{field}" for field in missing}
            | set(scope_gaps)
        )
    )
    adapter_status = (
        "accepted_for_dry_run_only"
        if not missing and not scope_gaps
        else "rejected_missing_required_fields_fail_closed"
    )
    payload = {
        "source_artifact": raw_handoff,
        "blocking_gaps": blocking_gaps,
        "adapter_status": adapter_status,
    }
    return MotorBRawDiagnosticsInputForStage07(
        motor_b_input_id=stable_hash("motor-b-raw-diagnostics-input", payload),
        source_stage="06 Backtesting Engine",
        source_artifact_type="RawDiagnosticsHandoffContract",
        handoff_contract_id=raw_handoff.get("handoff_contract_id"),
        registry_record_id=raw_handoff.get("registry_record_id"),
        diagnostics_id=raw_handoff.get("diagnostics_id"),
        simulation_id=raw_handoff.get("simulation_id"),
        package_id=raw_handoff.get("package_id"),
        strategy_id=raw_handoff.get("strategy_id"),
        strategy_version=raw_handoff.get("strategy_version"),
        snapshot_id=raw_handoff.get("snapshot_id"),
        output_scope=raw_handoff.get("output_scope"),
        diagnostics_scope=raw_handoff.get("diagnostics_scope"),
        registry_scope=raw_handoff.get("registry_scope"),
        handoff_scope=raw_handoff.get("handoff_scope"),
        simulation_status=raw_handoff.get("simulation_status"),
        trade_count=raw_handoff.get("trade_count"),
        ending_capital=raw_handoff.get("ending_capital"),
        return_pct=raw_handoff.get("return_pct"),
        evidence_completeness_level=EVIDENCE_COMPLETENESS_LEVEL,
        empirical_results_available=EMPIRICAL_RESULTS_AVAILABLE,
        confidence_status=CONFIDENCE_STATUS,
        confidence_score=CONFIDENCE_SCORE,
        final_signal_confidence_score=FINAL_SIGNAL_CONFIDENCE_SCORE,
        paper_trading_ready=PAPER_TRADING_READY,
        paper_trading_eligibility="blocked",
        handoff_to_09=HANDOFF_TO_09,
        downstream_operational_eligibility=DOWNSTREAM_OPERATIONAL_ELIGIBILITY,
        strategy_promotion_status=STRATEGY_PROMOTION_STATUS,
        adapter_status=adapter_status,
        missing_evidence=DEFAULT_BLOCKING_GAPS,
        blocking_gaps=blocking_gaps,
        forbidden_downstream_usage=FORBIDDEN_DOWNSTREAM_USAGE,
        non_approval_statement=raw_handoff.get("non_approval_statement")
        or NON_APPROVAL_STATEMENT,
        audit_references=(
            "06 Backtesting Engine/handoff/raw_diagnostics_handoff_contract.py",
            "07 Signal Fusion + LLM Motors/docs/14_motor_b_raw_diagnostics_adapter_contract.md",
        ),
    )
