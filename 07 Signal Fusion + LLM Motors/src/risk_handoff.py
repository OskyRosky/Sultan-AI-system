from __future__ import annotations

from audit_trace import stable_hash
from contracts import (
    CONFIDENCE_SCORE,
    CONFIDENCE_STATUS,
    DOWNSTREAM_OPERATIONAL_ELIGIBILITY,
    EMPIRICAL_RESULTS_AVAILABLE,
    EVIDENCE_COMPLETENESS_LEVEL,
    FINAL_SIGNAL_CONFIDENCE_SCORE,
    FORBIDDEN_DOWNSTREAM_USAGE,
    HANDOFF_TO_09,
    NON_APPROVAL_STATEMENT,
    PAPER_TRADING_READY,
    STRATEGY_PROMOTION_STATUS,
    ConfidenceGovernanceResult,
    FusedSignalCandidate,
    RiskHandoffPackage,
)


def build_risk_handoff_package(
    fused_signal_candidate: FusedSignalCandidate,
    confidence_governance_result: ConfidenceGovernanceResult,
) -> RiskHandoffPackage:
    blocking_gaps = tuple(
        sorted(
            set(fused_signal_candidate.blocking_gaps)
            | set(confidence_governance_result.blocking_gaps)
            | {"stage07_dry_run_only_not_operational"}
        )
    )
    forbidden = tuple(
        sorted(set(FORBIDDEN_DOWNSTREAM_USAGE) | set(fused_signal_candidate.forbidden_downstream_usage))
    )
    payload = {
        "fused_signal_candidate_id": fused_signal_candidate.fused_signal_candidate_id,
        "confidence_governance_result_id": (
            confidence_governance_result.confidence_governance_result_id
        ),
        "blocking_gaps": blocking_gaps,
    }
    return RiskHandoffPackage(
        risk_handoff_package_id=stable_hash("risk-handoff-package", payload),
        target_stage="08 Risk Engine",
        related_fused_signal_candidate_id=fused_signal_candidate.fused_signal_candidate_id,
        related_confidence_governance_result_id=(
            confidence_governance_result.confidence_governance_result_id
        ),
        risk_handoff_status="blocked",
        paper_trading_ready=PAPER_TRADING_READY,
        handoff_to_09=HANDOFF_TO_09,
        downstream_operational_eligibility=DOWNSTREAM_OPERATIONAL_ELIGIBILITY,
        strategy_promotion_status=STRATEGY_PROMOTION_STATUS,
        evidence_completeness_level=EVIDENCE_COMPLETENESS_LEVEL,
        empirical_results_available=EMPIRICAL_RESULTS_AVAILABLE,
        confidence_status=CONFIDENCE_STATUS,
        confidence_score=CONFIDENCE_SCORE,
        final_signal_confidence_score=FINAL_SIGNAL_CONFIDENCE_SCORE,
        blocking_gaps=blocking_gaps,
        forbidden_downstream_usage=forbidden,
        non_approval_statement=NON_APPROVAL_STATEMENT,
    )
