from __future__ import annotations

from typing import Any

from audit_trace import stable_hash
from contracts import (
    RISK_HANDOFF_ARTIFACT_TYPE,
    STAGE07_ID,
    STAGE08_ID,
    Stage08InputPackage,
)


RAW_ARTIFACT_TYPES = {
    "RawDiagnosticsHandoffContract",
    "MotorAContextMock",
    "MotorBRawDiagnosticsInputForStage07",
    "MotorCEventClassifierMock",
    "NormalizedMotorAInput",
    "NormalizedMotorBInput",
    "NormalizedMotorCInput",
    "LLMOutput",
    "Stage06Artifact",
}
RAW_SOURCE_STAGES = {
    "06 Backtesting Engine",
    "MotorA",
    "MotorB",
    "MotorC",
    "LLM",
}
CRITICAL_FIELDS = (
    "risk_handoff_package_id",
    "target_stage",
    "risk_handoff_status",
    "evidence_completeness_level",
    "empirical_results_available",
    "confidence_status",
    "confidence_score",
    "final_signal_confidence_score",
    "paper_trading_ready",
    "handoff_to_09",
    "downstream_operational_eligibility",
    "strategy_promotion_status",
    "blocking_gaps",
    "forbidden_downstream_usage",
    "non_approval_statement",
)


class Stage08IntakeError(ValueError):
    pass


def validate_stage07_risk_handoff_package(payload: Any) -> Stage08InputPackage:
    data = _to_payload_dict(payload)
    _reject_raw_payload(data)
    _require_risk_handoff_contract(data)

    blocking_gaps = tuple(data["blocking_gaps"])
    forbidden = tuple(data["forbidden_downstream_usage"])
    input_payload = {
        "source_stage": STAGE07_ID,
        "artifact_type": RISK_HANDOFF_ARTIFACT_TYPE,
        "source_risk_handoff_package_id": data["risk_handoff_package_id"],
        "target_stage": data["target_stage"],
        "blocking_gaps": blocking_gaps,
        "forbidden_downstream_usage": forbidden,
    }
    return Stage08InputPackage(
        stage08_input_package_id=stable_hash("stage08-input", input_payload),
        source_stage=STAGE07_ID,
        artifact_type=RISK_HANDOFF_ARTIFACT_TYPE,
        source_risk_handoff_package_id=data["risk_handoff_package_id"],
        intake_status="intake_accepted_for_risk_review",
        target_stage=data["target_stage"],
        risk_handoff_status=data["risk_handoff_status"],
        evidence_completeness_level=data["evidence_completeness_level"],
        empirical_results_available=data["empirical_results_available"],
        confidence_status=data["confidence_status"],
        confidence_score=data["confidence_score"],
        final_signal_confidence_score=data["final_signal_confidence_score"],
        paper_trading_ready=data["paper_trading_ready"],
        handoff_to_09=data["handoff_to_09"],
        downstream_operational_eligibility=data["downstream_operational_eligibility"],
        strategy_promotion_status=data["strategy_promotion_status"],
        blocking_gaps=blocking_gaps,
        forbidden_downstream_usage=forbidden,
        non_approval_statement=data["non_approval_statement"],
    )


def _to_payload_dict(payload: Any) -> dict[str, Any]:
    if hasattr(payload, "to_dict"):
        payload = payload.to_dict()
    if not isinstance(payload, dict):
        raise Stage08IntakeError("stage08_intake_requires_mapping_payload")
    return payload


def _reject_raw_payload(data: dict[str, Any]) -> None:
    artifact_type = data.get("artifact_type") or data.get("source_artifact_type")
    source_stage = data.get("source_stage")
    source_motor = data.get("source_motor")
    if artifact_type in RAW_ARTIFACT_TYPES:
        raise Stage08IntakeError("stage08_rejects_raw_artifact_type")
    if source_stage in RAW_SOURCE_STAGES:
        raise Stage08IntakeError("stage08_rejects_raw_source_stage")
    if source_motor in RAW_SOURCE_STAGES:
        raise Stage08IntakeError("stage08_rejects_raw_motor_input")


def _require_risk_handoff_contract(data: dict[str, Any]) -> None:
    missing = [field for field in CRITICAL_FIELDS if field not in data]
    if missing:
        raise Stage08IntakeError(f"stage08_missing_critical_fields:{','.join(missing)}")
    if data["target_stage"] != STAGE08_ID:
        raise Stage08IntakeError("stage08_target_stage_must_be_08_risk_engine")
    if not str(data["risk_handoff_package_id"]).startswith("risk-handoff-package-"):
        raise Stage08IntakeError("stage08_requires_stage07_risk_handoff_package_id")
    if data.get("artifact_type") not in (None, RISK_HANDOFF_ARTIFACT_TYPE):
        raise Stage08IntakeError("stage08_requires_risk_handoff_package")
