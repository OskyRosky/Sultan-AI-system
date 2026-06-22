from __future__ import annotations

from typing import Any

from audit_trace import create_audit_trace
from confidence_governance import govern_confidence
from contracts import (
    MotorAContextMock,
    MotorCEventClassifierMock,
    Stage07DryRunResult,
)
from fusion_engine import fuse_candidates
from motor_b_adapter import adapt_motor_b_raw_diagnostics
from normalizer import (
    normalize_motor_a,
    normalize_motor_b,
    normalize_motor_c,
    normalized_inputs_to_candidates,
)
from risk_handoff import build_risk_handoff_package


def run_stage07_dry_run(mock_payload: dict[str, Any] | None = None) -> Stage07DryRunResult:
    payload = default_mock_payload() if mock_payload is None else mock_payload
    motor_a = _motor_a_from_payload(payload.get("motor_a", {}))
    motor_b = adapt_motor_b_raw_diagnostics(payload.get("motor_b", {}))
    motor_c = _motor_c_from_payload(payload.get("motor_c", {}))

    normalized_motor_a = normalize_motor_a(motor_a)
    normalized_motor_b = normalize_motor_b(motor_b)
    normalized_motor_c = normalize_motor_c(motor_c)
    candidates = normalized_inputs_to_candidates(
        normalized_motor_a,
        normalized_motor_b,
        normalized_motor_c,
    )
    fused = fuse_candidates(candidates)
    confidence = govern_confidence(fused)
    risk_handoff = build_risk_handoff_package(fused, confidence)
    audit_trace = create_audit_trace(
        (
            normalized_motor_a,
            normalized_motor_b,
            normalized_motor_c,
            fused,
            confidence,
            risk_handoff,
        )
    )
    return Stage07DryRunResult(
        normalized_motor_a_input=normalized_motor_a,
        normalized_motor_b_input=normalized_motor_b,
        normalized_motor_c_input=normalized_motor_c,
        normalized_signal_candidates=candidates,
        fused_signal_candidate=fused,
        confidence_governance_result=confidence,
        risk_handoff_package=risk_handoff,
        audit_trace=audit_trace,
    )


def default_mock_payload() -> dict[str, Any]:
    return {
        "motor_a": {
            "regime_label": "synthetic_range_regime",
            "regime_source": "stage07_mock_fixture",
            "uncertainty_level": "high",
            "supported_assets": ("BTCUSDT", "ETHUSDT"),
            "supported_timeframes": ("1d", "4h"),
            "synthetic_status": "synthetic_dry_run_only",
            "limitations": ("mock_regime_context_not_operational",),
        },
        "motor_b": {
            "handoff_contract_id": "raw-handoff-mock-001",
            "registry_record_id": "raw-registry-mock-001",
            "diagnostics_id": "raw-diagnostics-mock-001",
            "simulation_id": "sim-mock-001",
            "package_id": "pkg-mock-001",
            "strategy_id": "strategy-mock-001",
            "strategy_version": "1.0.0",
            "snapshot_id": "snapshot-mock-001",
            "output_scope": "raw_execution_scaffold",
            "diagnostics_scope": "raw_scaffold_diagnostics_only",
            "registry_scope": "raw_diagnostics_registry_only",
            "handoff_scope": "raw_diagnostics_handoff_only",
            "simulation_status": "completed_raw_execution",
            "trade_count": 1,
            "ending_capital": 100000.0,
            "return_pct": 0.0,
            "non_approval_statement": (
                "Mock RawDiagnosticsHandoffContract is dry-run only and not evidence."
            ),
        },
        "motor_c": {
            "event_id": "event-mock-001",
            "event_type": "synthetic_event_context",
            "classification_status": "mock_classification_only",
            "classification_confidence_status": "classification_confidence_unavailable",
            "classification_confidence_score": None,
            "synthetic_status": "synthetic_dry_run_only",
            "limitations": ("mock_event_context_not_operational",),
        },
    }


def _motor_a_from_payload(payload: dict[str, Any]) -> MotorAContextMock:
    return MotorAContextMock(
        regime_label=payload.get("regime_label", "missing_regime_context"),
        regime_source=payload.get("regime_source", "stage07_mock_fixture"),
        uncertainty_level=payload.get("uncertainty_level", "unknown"),
        supported_assets=tuple(payload.get("supported_assets", ())),
        supported_timeframes=tuple(payload.get("supported_timeframes", ())),
        synthetic_status=payload.get("synthetic_status", "synthetic_dry_run_only"),
        limitations=tuple(payload.get("limitations", ("motor_a_mock_incomplete",))),
    )


def _motor_c_from_payload(payload: dict[str, Any]) -> MotorCEventClassifierMock:
    return MotorCEventClassifierMock(
        event_id=payload.get("event_id", "missing_event_id"),
        event_type=payload.get("event_type", "missing_event_type"),
        classification_status=payload.get("classification_status", "mock_classification_only"),
        classification_confidence_status=payload.get(
            "classification_confidence_status",
            "classification_confidence_unavailable",
        ),
        classification_confidence_score=payload.get("classification_confidence_score"),
        synthetic_status=payload.get("synthetic_status", "synthetic_dry_run_only"),
        limitations=tuple(payload.get("limitations", ("motor_c_mock_incomplete",))),
    )
