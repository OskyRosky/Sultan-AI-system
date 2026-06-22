from __future__ import annotations

from audit_trace import stable_hash
from contracts import (
    DOWNSTREAM_OPERATIONAL_ELIGIBILITY,
    EMPIRICAL_RESULTS_AVAILABLE,
    EVIDENCE_COMPLETENESS_LEVEL,
    FORBIDDEN_DOWNSTREAM_USAGE,
    HANDOFF_TO_09,
    NON_APPROVAL_STATEMENT,
    PAPER_TRADING_READY,
    STRATEGY_PROMOTION_STATUS,
    FusedSignalCandidate,
    NormalizedSignalCandidate,
)


def fuse_candidates(
    candidates: tuple[NormalizedSignalCandidate, ...],
) -> FusedSignalCandidate:
    candidate_ids = tuple(candidate.normalized_signal_candidate_id for candidate in candidates)
    blocking_gaps = tuple(
        sorted({gap for candidate in candidates for gap in candidate.blocking_gaps})
    )
    forbidden = tuple(
        sorted(
            set(FORBIDDEN_DOWNSTREAM_USAGE)
            | {item for candidate in candidates for item in candidate.forbidden_downstream_usage}
        )
    )
    payload = {
        "candidate_ids": candidate_ids,
        "blocking_gaps": blocking_gaps,
        "signal_scope": "dry_run_contract_validation",
    }
    return FusedSignalCandidate(
        fused_signal_candidate_id=stable_hash("fused-signal-candidate", payload),
        input_candidate_ids=candidate_ids,
        signal_scope="dry_run_contract_validation",
        fused_direction="diagnostic_only",
        operational_status="non_operational",
        evidence_completeness_level=EVIDENCE_COMPLETENESS_LEVEL,
        empirical_results_available=EMPIRICAL_RESULTS_AVAILABLE,
        promotion_status=STRATEGY_PROMOTION_STATUS,
        paper_trading_ready=PAPER_TRADING_READY,
        handoff_to_09=HANDOFF_TO_09,
        downstream_operational_eligibility=DOWNSTREAM_OPERATIONAL_ELIGIBILITY,
        blocking_gaps=blocking_gaps,
        forbidden_downstream_usage=forbidden,
        non_approval_statement=NON_APPROVAL_STATEMENT,
    )
