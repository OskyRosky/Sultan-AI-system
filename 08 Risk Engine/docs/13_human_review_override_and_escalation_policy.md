# 08 Risk Engine — Block 13: Human Review, Override and Escalation Policy

## Purpose

Block 13 defines the documentary policy for human review, override boundaries, and escalation inside Stage 08 Risk Engine.

Human review may block, request evidence, escalate, suspend, reject, require Risk Engine review, require emergency review, preserve `not_promoted`, preserve Paper Trading blocked, and preserve `handoff_to_09` blocked.

Human review cannot convert `framework_only` into operational approval.

This block does not create a productive workflow, does not approve Paper Trading, does not approve Live Trading, does not enable execution, and does not substitute empirical evidence.

## Human Review Authority

Stage 08 / Block 13 may:

- require human review;
- require Risk Engine review;
- require emergency review;
- require evidence review;
- require audit review;
- preserve blocking;
- block;
- reject;
- suspend;
- escalate;
- request more evidence;
- request missing evidence;
- flag override attempts;
- classify override attempt severity;
- preserve no downstream eligibility.

Human review can reduce risk or preserve blocking, but cannot approve operational activity under `framework_only`.

## Current Framework-Only Human Review Baseline

The current human review baseline is:

```text
evidence_completeness_level = framework_only
simulation_status = backtest_not_implemented
oos_validation_status = oos_not_available
walk_forward_status = walk_forward_not_available
robustness_status = robustness_not_available
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
handoff_to_09 = blocked
live_trading_status = blocked
execution_eligibility = blocked
order_generation_eligibility = blocked
exchange_connection_eligibility = blocked
capital_allocation_eligibility = blocked
productive_position_sizing_eligibility = blocked
risk_budget_activation = blocked
promotion_status = not_promoted
promotion_eligibility = blocked
risk_decision_status = blocked_framework_only
secondary_risk_decision_status = blocked_missing_evidence
```

No human review outcome may contradict this baseline under `framework_only`.

Any review note, override request, escalation statement, or manual instruction that attempts to weaken this baseline must be logged, classified, and routed conservatively.

## Human Review Non-Approval Rule

Human review is not approval under `framework_only`.

Human review cannot approve Paper Trading under `framework_only`.

Human review cannot approve Live Trading under `framework_only`.

Human review cannot approve execution under `framework_only`.

Human review cannot approve order generation under `framework_only`.

Human review cannot approve exchange connection under `framework_only`.

Human review cannot approve capital allocation under `framework_only`.

Human review cannot approve productive position sizing under `framework_only`.

Human review cannot activate risk budgets under `framework_only`.

Human review cannot promote strategies under `framework_only`.

Human review cannot create confidence_score.

Human review cannot create final_signal_confidence_score.

Human review cannot override missing empirical evidence.

Human review cannot override Motor B `framework_only`.

Human review cannot override hard veto or Kill Switch review without future formal governance.

Human review can produce conservative outcomes, not approval outcomes.

## Allowed Human Review Outcomes

Permitted conservative human review outcomes include:

- `human_review_required`;
- `human_review_completed_blocking_preserved`;
- `human_review_completed_rejected`;
- `human_review_completed_suspended`;
- `human_review_completed_more_evidence_required`;
- `human_review_completed_missing_evidence_required`;
- `human_review_completed_risk_engine_review_required`;
- `human_review_completed_emergency_review_required`;
- `human_review_completed_hard_veto_review_required`;
- `human_review_completed_kill_switch_review_required`;
- `human_review_completed_no_downstream_eligibility`;
- `human_review_completed_not_promoted`;
- `human_review_completed_paper_trading_blocked`.

None of these outcomes is operational approval.

These outcomes may preserve blocking, increase review requirements, reject a request, suspend a path, require additional evidence, or escalate. They cannot unlock downstream eligibility.

## Prohibited Human Review Outcomes

Under `framework_only`, the following outcomes are prohibited:

- `human_review_approved`;
- `human_review_paper_trading_approved`;
- `human_review_live_trading_approved`;
- `human_review_execution_approved`;
- `human_review_order_generation_approved`;
- `human_review_exchange_connection_approved`;
- `human_review_capital_allocation_approved`;
- `human_review_position_sizing_approved`;
- `human_review_risk_budget_approved`;
- `human_review_strategy_promoted`;
- `human_review_confidence_approved`;
- `human_review_handoff_to_09_approved`;
- `human_review_framework_only_override_approved`.

These outcomes are not valid in the current state.

If any artifact uses one of these outcomes under `framework_only`, Block 13 must classify it as an override attempt, preserve downstream blocking, and escalate according to severity.

## Override Boundary Rule

Overrides cannot bypass `framework_only`.

Overrides cannot bypass missing empirical evidence.

Overrides cannot bypass missing backtesting.

Overrides cannot bypass missing OOS validation.

Overrides cannot bypass missing walk-forward validation.

Overrides cannot bypass missing robustness testing.

Overrides cannot bypass `confidence_not_available`.

Overrides cannot bypass hard veto.

Overrides cannot bypass Kill Switch review.

Overrides cannot bypass Paper Trading blocked.

Overrides cannot bypass `promotion_status = not_promoted`.

Overrides cannot bypass `handoff_to_09` blocked.

Override attempts must be logged, classified, and escalated.

## Override Attempt Taxonomy

Documentary override attempt types include:

- `override_attempt_framework_only_bypass`;
- `override_attempt_paper_trading_bypass`;
- `override_attempt_live_trading_bypass`;
- `override_attempt_execution_bypass`;
- `override_attempt_order_generation_bypass`;
- `override_attempt_exchange_connection_bypass`;
- `override_attempt_capital_allocation_bypass`;
- `override_attempt_position_sizing_bypass`;
- `override_attempt_risk_budget_bypass`;
- `override_attempt_strategy_promotion_bypass`;
- `override_attempt_confidence_creation`;
- `override_attempt_missing_evidence_bypass`;
- `override_attempt_hard_veto_bypass`;
- `override_attempt_kill_switch_bypass`;
- `override_attempt_handoff_to_09_bypass`;
- `override_attempt_audit_trace_bypass`.

Override attempts may trigger Risk Engine review, human review escalation, emergency review, hard veto candidate, or Kill Switch review candidate.

Override attempts do not create approval, readiness, eligibility, confidence, or operational authority.

## Escalation Trigger Taxonomy

Escalation triggers include:

- `escalation_trigger_framework_only_with_approval_request`;
- `escalation_trigger_paper_trading_request_under_blocked_state`;
- `escalation_trigger_live_trading_request_under_blocked_state`;
- `escalation_trigger_execution_request_under_blocked_state`;
- `escalation_trigger_capital_allocation_request_under_blocked_state`;
- `escalation_trigger_strategy_promotion_request_under_blocked_state`;
- `escalation_trigger_confidence_invention`;
- `escalation_trigger_missing_evidence_bypass_attempt`;
- `escalation_trigger_contract_violation`;
- `escalation_trigger_source_conflict`;
- `escalation_trigger_event_critical`;
- `escalation_trigger_hard_veto_candidate`;
- `escalation_trigger_kill_switch_review_required`;
- `escalation_trigger_manual_override_attempt`;
- `escalation_trigger_audit_gap`;
- `escalation_trigger_unversioned_evidence_claim`.

Escalation trigger classification is documentary and non-operational. It routes review and preserves blocking.

## Escalation Outcome Taxonomy

Escalation outcomes include:

- `escalation_outcome_blocking_preserved`;
- `escalation_outcome_review_required`;
- `escalation_outcome_risk_engine_review_required`;
- `escalation_outcome_emergency_review_required`;
- `escalation_outcome_hard_veto_review_required`;
- `escalation_outcome_kill_switch_review_required`;
- `escalation_outcome_rejected`;
- `escalation_outcome_suspended`;
- `escalation_outcome_more_evidence_required`;
- `escalation_outcome_missing_evidence_required`;
- `escalation_outcome_audit_trace_required`;
- `escalation_outcome_no_downstream_eligibility`;
- `escalation_outcome_handoff_to_09_blocked`.

`escalation_outcome_approved` is prohibited under `framework_only`.

Escalation can harden, preserve blocking, reject, suspend, or require review. It cannot approve operational use.

## Human Review Required Conditions

Human review is required when there is:

- `framework_only` with favorable signal;
- `framework_only` with Paper Trading request;
- event critical;
- conflicting sources;
- prohibited inference flags;
- prompt injection or instruction override attempt;
- human override attempt;
- missing evidence;
- audit gaps;
- source conflict;
- contract violation;
- Kill Switch review required;
- hard veto candidate;
- confidence invention attempt;
- strategy promotion request under `framework_only`;
- paper trading request under `framework_only`;
- capital allocation request under `framework_only`;
- execution request under `framework_only`.

Human review under these conditions is a conservative review route. It does not create approval.

## Human Review Cannot Substitute Evidence Rule

Human review metadata cannot substitute:

- real backtesting;
- OOS validation;
- walk-forward validation;
- robustness testing;
- empirical historical results;
- versioned data references;
- versioned feature references;
- versioned strategy references;
- audit trace;
- confidence evidence;
- risk policy compliance;
- Paper Trading eligibility.

Human review cannot substitute empirical evidence.

Human review can request evidence, but cannot create it.

Human review can document a concern, classification, rejection, escalation, or future requirement, but cannot convert missing evidence into sufficient evidence.

## Human Review Record

Stage 08 may document a human review with fields such as:

- `human_review_record_id`;
- `review_type`;
- `review_requested_at`;
- `review_completed_at`;
- `reviewer_role`;
- `reviewer_identifier_optional`;
- `source_artifact_id`;
- `source_stage`;
- `source_block`;
- `source_document_ref`;
- `risk_decision_ref`;
- `review_trigger`;
- `override_attempt_detected`;
- `override_attempt_type`;
- `escalation_trigger`;
- `human_review_outcome`;
- `escalation_outcome`;
- `evidence_completeness_level`;
- `simulation_status`;
- `oos_validation_status`;
- `walk_forward_status`;
- `robustness_status`;
- `confidence_status`;
- `confidence_score`;
- `final_signal_confidence_score`;
- `paper_trading_eligibility`;
- `live_trading_status`;
- `execution_eligibility`;
- `order_generation_eligibility`;
- `exchange_connection_eligibility`;
- `capital_allocation_eligibility`;
- `productive_position_sizing_eligibility`;
- `risk_budget_activation`;
- `promotion_status`;
- `promotion_eligibility`;
- `downstream_operational_eligibility`;
- `handoff_to_09`;
- `blocking_preserved`;
- `required_future_evidence`;
- `required_review`;
- `audit_trace_ref`;
- `final_note_non_operational`.

This block does not create a database, storage layer, productive approval workflow, override runtime, escalation runtime, or executable review service. The record is documentary only.

## Current Human Review Conclusion

Under the current state:

```text
human_review_policy_status = non_operational_documentary
human_review_can_approve_operational_use = false
human_review_can_override_framework_only = false
human_review_can_create_confidence = false
human_review_can_create_empirical_evidence = false
human_review_can_unblock_paper_trading = false
human_review_can_unblock_handoff_to_09 = false
paper_trading_eligibility = blocked
live_trading_status = blocked
execution_eligibility = blocked
order_generation_eligibility = blocked
exchange_connection_eligibility = blocked
capital_allocation_eligibility = blocked
productive_position_sizing_eligibility = blocked
risk_budget_activation = blocked
promotion_status = not_promoted
promotion_eligibility = blocked
downstream_operational_eligibility = blocked
handoff_to_09 = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

Human review cannot approve operational use, cannot override Motor B `framework_only`, cannot create confidence, cannot create empirical evidence, and cannot unblock Paper Trading or `handoff_to_09` under the current state.

## Relationship With Block 05

Block 05 defines hard veto and Kill Switch triggers.

Block 13 can require hard veto review or Kill Switch review, but cannot override them under `framework_only`.

Human review may escalate to hard veto review or Kill Switch review when override attempts, prompt injection, direct operational requests, confidence invention, source conflicts, critical events, or missing evidence bypass attempts are detected.

## Relationship With Block 12

Block 12 produces `RiskDecision`.

Block 13 can consume RiskDecision outcomes such as `requires_human_review` or `requires_risk_engine_review`, but cannot convert them into approval under `framework_only`.

Human review routing produced by RiskDecision remains non-operational and must preserve Paper Trading blocked, `handoff_to_09` blocked, null confidence, no promotion, and no downstream operational eligibility.

## Relationship With Block 14

Block 14 will define Audit, Traceability and Risk Decision Replay.

Block 13 prepares human review record fields, override attempt fields, escalation fields, review outcome fields, and audit references. It does not build full replay.

## Relationship With Block 17

Block 17 closes Stage 08 and formalizes handoff to Stage 09.

Block 13 cannot unblock `handoff_to_09` under the current `framework_only` state.

Human review cannot convert Stage 08 closure or any future handoff language into Stage 09 readiness unless future empirical evidence, governance, auditability, and eligibility gates support it.

## Explicit Non-Goals

This block does not do:

- approve Paper Trading;
- approve Live Trading;
- approve execution;
- approve order generation;
- approve exchange connection;
- approve capital allocation;
- approve productive position sizing;
- activate risk budgets;
- promote strategies;
- create `confidence_score`;
- create `final_signal_confidence_score`;
- create empirical evidence;
- run backtesting;
- run OOS validation;
- run walk-forward;
- run robustness;
- implement human approval workflow;
- implement override runtime;
- implement escalation runtime;
- execute Kill Switch;
- override hard veto;
- create Paper Trading runtime;
- create Paper Trading simulator;
- create execution engine;
- create capital allocator;
- create audit replay;
- close Stage 08;
- hand off to Stage 09.

Block 13 is a non-operational documentary policy. It defines conservative review, override, and escalation boundaries; it does not create any approval, execution, capital, confidence, promotion, or handoff capability.
