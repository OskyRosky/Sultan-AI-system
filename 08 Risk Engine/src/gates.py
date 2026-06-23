from __future__ import annotations

from contracts import Stage08GateResult, Stage08InputPackage


def run_conservative_gates(input_package: Stage08InputPackage) -> tuple[Stage08GateResult, ...]:
    return (
        input_contract_gate(input_package),
        confidence_gate(input_package),
        evidence_completeness_gate(input_package),
        paper_trading_gate(input_package),
        promotion_gate(input_package),
        downstream_restriction_gate(input_package),
    )


def input_contract_gate(input_package: Stage08InputPackage) -> Stage08GateResult:
    reasons = []
    gaps = set(input_package.blocking_gaps)
    if input_package.artifact_type != "RiskHandoffPackage":
        reasons.append("invalid_input_contract")
        gaps.add("stage08_requires_stage07_risk_handoff_package")
    if input_package.risk_handoff_status == "blocked":
        reasons.append("upstream_risk_handoff_blocked")
        gaps.add("upstream_stage07_risk_handoff_blocked")
    return _blocked_gate("input_contract_gate", reasons, gaps, input_package)


def confidence_gate(input_package: Stage08InputPackage) -> Stage08GateResult:
    reasons = []
    gaps = set(input_package.blocking_gaps)
    if input_package.confidence_status == "confidence_not_available":
        reasons.append("confidence_not_available")
        gaps.add("confidence_not_available")
    if input_package.confidence_score is None:
        reasons.append("confidence_score_missing")
        gaps.add("confidence_score_missing")
    if input_package.final_signal_confidence_score is None:
        reasons.append("final_signal_confidence_score_missing")
        gaps.add("final_signal_confidence_score_missing")
    return _blocked_gate("confidence_gate", reasons, gaps, input_package)


def evidence_completeness_gate(input_package: Stage08InputPackage) -> Stage08GateResult:
    reasons = []
    gaps = set(input_package.blocking_gaps)
    if input_package.evidence_completeness_level == "framework_only":
        reasons.append("framework_only_input")
        gaps.add("framework_only_input")
    if input_package.empirical_results_available is False:
        reasons.append("empirical_evidence_not_available")
        gaps.add("empirical_evidence_not_available")
    return _blocked_gate("evidence_completeness_gate", reasons, gaps, input_package)


def paper_trading_gate(input_package: Stage08InputPackage) -> Stage08GateResult:
    reasons = []
    gaps = set(input_package.blocking_gaps)
    if input_package.paper_trading_ready is False:
        reasons.append("paper_trading_blocked")
        gaps.add("paper_trading_blocked")
    return _blocked_gate("paper_trading_gate", reasons, gaps, input_package)


def promotion_gate(input_package: Stage08InputPackage) -> Stage08GateResult:
    reasons = []
    gaps = set(input_package.blocking_gaps)
    if input_package.strategy_promotion_status == "not_promoted":
        reasons.append("strategy_not_promoted")
        gaps.add("strategy_not_promoted")
    return _blocked_gate("promotion_gate", reasons, gaps, input_package)


def downstream_restriction_gate(input_package: Stage08InputPackage) -> Stage08GateResult:
    reasons = ["v1_dry_run_only"]
    gaps = set(input_package.blocking_gaps)
    if input_package.handoff_to_09 == "blocked":
        reasons.append("handoff_to_09_blocked")
        gaps.add("handoff_to_09_blocked")
    if input_package.downstream_operational_eligibility == "blocked":
        reasons.append("downstream_operational_eligibility_blocked")
        gaps.add("downstream_operational_eligibility_blocked")
    if input_package.forbidden_downstream_usage:
        reasons.append("forbidden_downstream_usage_present")
        gaps.add("forbidden_downstream_usage_present")
    return _blocked_gate("downstream_restriction_gate", reasons, gaps, input_package)


def _blocked_gate(
    gate_name: str,
    reason_codes: list[str],
    blocking_gaps: set[str],
    input_package: Stage08InputPackage,
) -> Stage08GateResult:
    preserved = tuple(sorted(input_package.forbidden_downstream_usage))
    return Stage08GateResult(
        gate_name=gate_name,
        gate_status="blocked",
        passed=False,
        reason_codes=tuple(sorted(set(reason_codes or ["conservative_v1_block"]))),
        blocking_gaps=tuple(sorted(blocking_gaps)),
        preserved_restrictions=preserved,
    )
