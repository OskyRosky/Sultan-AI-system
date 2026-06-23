from __future__ import annotations

from audit_trace import stable_hash
from contracts import (
    CAPITAL_ALLOCATION_READY,
    DEFAULT_REASON_CODES,
    DOWNSTREAM_OPERATIONAL_ELIGIBILITY,
    HANDOFF_TO_09,
    LIVE_TRADING_READY,
    NON_APPROVAL_STATEMENT,
    OPERATIONAL_STATUS,
    PAPER_TRADING_READY,
    RISK_APPROVAL,
    RISK_DECISION_STATUS,
    STAGE_09_OPERATIONAL_START_ALLOWED,
    Stage08GateResult,
    Stage08InputPackage,
    Stage08RiskDecision,
)


def build_risk_decision(
    input_package: Stage08InputPackage,
    gate_results: tuple[Stage08GateResult, ...],
) -> Stage08RiskDecision:
    reason_codes = tuple(
        sorted(
            set(DEFAULT_REASON_CODES)
            | {
                reason
                for gate in gate_results
                for reason in gate.reason_codes
            }
        )
    )
    blocking_gaps = tuple(
        sorted(
            set(input_package.blocking_gaps)
            | {
                gap
                for gate in gate_results
                for gap in gate.blocking_gaps
            }
        )
    )
    forbidden = tuple(sorted(input_package.forbidden_downstream_usage))
    payload = {
        "stage08_input_package_id": input_package.stage08_input_package_id,
        "reason_codes": reason_codes,
        "blocking_gaps": blocking_gaps,
        "forbidden_downstream_usage": forbidden,
        "risk_decision_status": RISK_DECISION_STATUS,
    }
    return Stage08RiskDecision(
        risk_decision_id=stable_hash("stage08-risk-decision", payload),
        related_stage08_input_package_id=input_package.stage08_input_package_id,
        risk_decision_status=RISK_DECISION_STATUS,
        operational_status=OPERATIONAL_STATUS,
        risk_approval=RISK_APPROVAL,
        paper_trading_ready=PAPER_TRADING_READY,
        handoff_to_09=HANDOFF_TO_09,
        downstream_operational_eligibility=DOWNSTREAM_OPERATIONAL_ELIGIBILITY,
        stage_09_operational_start_allowed=STAGE_09_OPERATIONAL_START_ALLOWED,
        capital_allocation_ready=CAPITAL_ALLOCATION_READY,
        live_trading_ready=LIVE_TRADING_READY,
        reason_codes=reason_codes,
        blocking_gaps=blocking_gaps,
        forbidden_downstream_usage=forbidden,
        non_approval_statement=NON_APPROVAL_STATEMENT,
    )
