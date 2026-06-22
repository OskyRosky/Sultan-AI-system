from __future__ import annotations

from audit_trace import stable_hash
from contracts import (
    CONFIDENCE_SCORE,
    CONFIDENCE_STATUS,
    DOWNSTREAM_OPERATIONAL_ELIGIBILITY,
    EMPIRICAL_RESULTS_AVAILABLE,
    EVIDENCE_COMPLETENESS_LEVEL,
    FORBIDDEN_DOWNSTREAM_USAGE,
    HANDOFF_TO_09,
    NON_APPROVAL_STATEMENT,
    PAPER_TRADING_READY,
    STRATEGY_PROMOTION_STATUS,
    MotorAContextMock,
    MotorBRawDiagnosticsInputForStage07,
    MotorCEventClassifierMock,
    NormalizedMotorAInput,
    NormalizedMotorBInput,
    NormalizedMotorCInput,
    NormalizedSignalCandidate,
)


def normalize_motor_a(motor_a: MotorAContextMock) -> NormalizedMotorAInput:
    blocking_gaps = ("motor_a_context_is_synthetic_dry_run_only",)
    payload = motor_a.to_dict() | {"blocking_gaps": blocking_gaps}
    return NormalizedMotorAInput(
        normalized_input_id=stable_hash("normalized-motor-a", payload),
        source_motor="MotorA",
        regime_label=motor_a.regime_label,
        uncertainty_level=motor_a.uncertainty_level,
        synthetic_status=motor_a.synthetic_status,
        normalization_status="accepted_for_dry_run_only",
        blocking_gaps=blocking_gaps,
    )


def normalize_motor_b(
    motor_b: MotorBRawDiagnosticsInputForStage07,
) -> NormalizedMotorBInput:
    return NormalizedMotorBInput(
        normalized_input_id=stable_hash("normalized-motor-b", motor_b.to_dict()),
        source_motor="MotorB",
        source_artifact_type=motor_b.source_artifact_type,
        source_artifact_id=motor_b.handoff_contract_id,
        strategy_id=motor_b.strategy_id,
        evidence_completeness_level=motor_b.evidence_completeness_level,
        empirical_results_available=motor_b.empirical_results_available,
        confidence_status=motor_b.confidence_status,
        confidence_score=motor_b.confidence_score,
        paper_trading_ready=motor_b.paper_trading_ready,
        handoff_to_09=motor_b.handoff_to_09,
        downstream_operational_eligibility=motor_b.downstream_operational_eligibility,
        strategy_promotion_status=motor_b.strategy_promotion_status,
        normalization_status=motor_b.adapter_status,
        blocking_gaps=motor_b.blocking_gaps,
        forbidden_downstream_usage=motor_b.forbidden_downstream_usage,
        non_approval_statement=motor_b.non_approval_statement,
    )


def normalize_motor_c(motor_c: MotorCEventClassifierMock) -> NormalizedMotorCInput:
    blocking_gaps = ("motor_c_event_classifier_is_mock_only",)
    payload = motor_c.to_dict() | {"blocking_gaps": blocking_gaps}
    return NormalizedMotorCInput(
        normalized_input_id=stable_hash("normalized-motor-c", payload),
        source_motor="MotorC",
        event_id=motor_c.event_id,
        event_type=motor_c.event_type,
        classification_confidence_status=motor_c.classification_confidence_status,
        classification_confidence_score=motor_c.classification_confidence_score,
        synthetic_status=motor_c.synthetic_status,
        normalization_status="accepted_for_dry_run_only",
        blocking_gaps=blocking_gaps,
    )


def normalized_inputs_to_candidates(
    motor_a: NormalizedMotorAInput,
    motor_b: NormalizedMotorBInput,
    motor_c: NormalizedMotorCInput,
) -> tuple[NormalizedSignalCandidate, ...]:
    return (
        _candidate_from_motor_a(motor_a),
        _candidate_from_motor_b(motor_b),
        _candidate_from_motor_c(motor_c),
    )


def _candidate_from_motor_a(motor_a: NormalizedMotorAInput) -> NormalizedSignalCandidate:
    return _candidate(
        source_motor="MotorA",
        source_input_id=motor_a.normalized_input_id,
        normalization_status=motor_a.normalization_status,
        blocking_gaps=motor_a.blocking_gaps,
    )


def _candidate_from_motor_b(motor_b: NormalizedMotorBInput) -> NormalizedSignalCandidate:
    return _candidate(
        source_motor="MotorB",
        source_input_id=motor_b.normalized_input_id,
        normalization_status=motor_b.normalization_status,
        blocking_gaps=motor_b.blocking_gaps,
        forbidden_downstream_usage=motor_b.forbidden_downstream_usage,
        non_approval_statement=motor_b.non_approval_statement,
    )


def _candidate_from_motor_c(motor_c: NormalizedMotorCInput) -> NormalizedSignalCandidate:
    return _candidate(
        source_motor="MotorC",
        source_input_id=motor_c.normalized_input_id,
        normalization_status=motor_c.normalization_status,
        blocking_gaps=motor_c.blocking_gaps,
    )


def _candidate(
    *,
    source_motor: str,
    source_input_id: str,
    normalization_status: str,
    blocking_gaps: tuple[str, ...],
    forbidden_downstream_usage: tuple[str, ...] = FORBIDDEN_DOWNSTREAM_USAGE,
    non_approval_statement: str = NON_APPROVAL_STATEMENT,
) -> NormalizedSignalCandidate:
    payload = {
        "source_motor": source_motor,
        "source_input_id": source_input_id,
        "normalization_status": normalization_status,
        "blocking_gaps": blocking_gaps,
    }
    return NormalizedSignalCandidate(
        normalized_signal_candidate_id=stable_hash("normalized-signal-candidate", payload),
        source_motor=source_motor,
        source_input_id=source_input_id,
        signal_direction="no_operational_signal",
        signal_scope="dry_run_contract_validation",
        evidence_completeness_level=EVIDENCE_COMPLETENESS_LEVEL,
        empirical_results_available=EMPIRICAL_RESULTS_AVAILABLE,
        confidence_status=CONFIDENCE_STATUS,
        confidence_score=CONFIDENCE_SCORE,
        paper_trading_ready=PAPER_TRADING_READY,
        handoff_to_09=HANDOFF_TO_09,
        downstream_operational_eligibility=DOWNSTREAM_OPERATIONAL_ELIGIBILITY,
        strategy_promotion_status=STRATEGY_PROMOTION_STATUS,
        normalization_status=normalization_status,
        blocking_gaps=blocking_gaps,
        forbidden_downstream_usage=forbidden_downstream_usage,
        non_approval_statement=non_approval_statement,
    )
