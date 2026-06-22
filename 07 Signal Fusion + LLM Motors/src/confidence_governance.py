from __future__ import annotations

from audit_trace import stable_hash
from contracts import (
    CONFIDENCE_SCORE,
    CONFIDENCE_STATUS,
    EMPIRICAL_RESULTS_AVAILABLE,
    EVIDENCE_COMPLETENESS_LEVEL,
    FINAL_SIGNAL_CONFIDENCE_SCORE,
    HANDOFF_TO_09,
    NON_APPROVAL_STATEMENT,
    PAPER_TRADING_READY,
    STRATEGY_PROMOTION_STATUS,
    ConfidenceGovernanceResult,
    FusedSignalCandidate,
)


def govern_confidence(
    fused_signal_candidate: FusedSignalCandidate,
) -> ConfidenceGovernanceResult:
    payload = {
        "fused_signal_candidate_id": fused_signal_candidate.fused_signal_candidate_id,
        "confidence_status": CONFIDENCE_STATUS,
        "confidence_reason": "dry_run_contract_validation_only",
    }
    return ConfidenceGovernanceResult(
        confidence_governance_result_id=stable_hash("confidence-governance", payload),
        related_fused_signal_candidate_id=fused_signal_candidate.fused_signal_candidate_id,
        evidence_completeness_level=EVIDENCE_COMPLETENESS_LEVEL,
        empirical_results_available=EMPIRICAL_RESULTS_AVAILABLE,
        confidence_status=CONFIDENCE_STATUS,
        confidence_score=CONFIDENCE_SCORE,
        final_signal_confidence_score=FINAL_SIGNAL_CONFIDENCE_SCORE,
        confidence_reason="dry_run_contract_validation_only",
        paper_trading_ready=PAPER_TRADING_READY,
        handoff_to_09=HANDOFF_TO_09,
        strategy_promotion_status=STRATEGY_PROMOTION_STATUS,
        blocking_gaps=fused_signal_candidate.blocking_gaps,
        non_approval_statement=NON_APPROVAL_STATEMENT,
    )
