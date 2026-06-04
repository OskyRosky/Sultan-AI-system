# 08 Risk Engine — Block 08: Event, Regime and Market Risk Gate

## Purpose

Block 08 defines the formal event risk, regime risk, and market risk gate inside Stage 08 Risk Engine.

This block consumes Stage 07 event precedence outputs and related event metadata. It does not redefine Stage 07 event precedence from scratch.

The gate may harden, block, degrade, suspend, require review, or escalate event/regime/market risk handling. It cannot unlock Paper Trading, Live Trading, execution, order generation, exchange connection, capital allocation, productive position sizing, strategy promotion, confidence, or `handoff_to_09`.

Block 08 is documentary and non-operational. It does not implement an event engine, regime engine, market risk engine, trading logic, execution logic, capital allocation logic, or confidence scoring.

## Notation and Reference Convention

This document uses explicit notation because `08` can refer to both Stage 08 Risk Engine and Block 08 Event, Regime and Market Risk Gate.

The official convention is:

```text
stage_id = "08"
stage_name = "Risk Engine"
block_number = "08"
block_id = "08.08"
block_ref = "stage_08.block_08"
```

This convention avoids ambiguity between the stage number and the block number.

All schemas, audit logs, gate outcomes, replay artifacts, quality gates, assessment records, and downstream documents must use this convention when ambiguity could exist.

Block 08 is not renamed to `08A`. Stage 08 preserves the standard block numbering sequence from `00` through `17`.

## Gate Authority

Stage 08 / Block 08 may:

- consume Stage 07 event precedence outputs;
- consume `event_risk_status`;
- consume Motor C severity;
- consume `event_precedence_hint`;
- consume `event_modulation_hook_reference`;
- classify event risk;
- classify regime risk;
- classify market risk;
- harden risk posture;
- block downstream handling;
- degrade a package;
- suspend downstream eligibility;
- escalate to human review;
- escalate to Risk Engine review;
- mark event metadata unavailable;
- mark event metadata degraded;
- trigger hard veto candidate;
- trigger Kill Switch review candidate.

Block 08 cannot use event, regime, or market context to approve trading. It cannot convert a favorable event, stable regime, normal market context, or aligned Stage 07 fusion artifact into operational approval.

## Stage 07 Event Precedence Consumption Rule

Block 08 consumes, references, and respects Stage 07 event precedence outputs.

Block 08 must consume or reference:

- `event_precedence_outcome` from Stage 07 Block 08, if present;
- `event_risk_status` from `RiskHandoffPackage`, if present;
- Motor C severity from Stage 07 Block 04, if present;
- `event_precedence_hint` from Stage 07 Block 04, if present;
- `event_modulation_hook_reference` from Stage 07 Block 06, if present.

Block 08 does not redefine Stage 07 event precedence from scratch.

Missing event precedence metadata must be marked `unavailable`, `degraded`, or `review-required`.

Missing metadata cannot be inferred from LLM text, favorable interpretation, regime context, market context, Bull/Bear agreement, or human optimism.

Stage 08 can harden, veto, escalate, or maintain blocking based on event/regime/market risk. Stage 08 cannot relax event risk declared by Stage 07 without formal replayable evidence and later governance. Stage 08 cannot convert a favorable event into approval.

Stage 07 documents that allowed `event_precedence_outcome` values include:

```text
no_event_precedence
monitor_only
constrain_direction
degrade_candidate
require_human_review
risk_suspend_candidate
reject_candidate_due_to_event_risk
unavailable_event_context
```

These outcomes are consumed as non-operational risk metadata. They are not trading authorization.

## Event Asymmetry Rule

The event asymmetry rule is mandatory:

- favorable events unlock nothing;
- favorable events cannot approve Paper Trading;
- favorable events cannot approve Live Trading;
- favorable events cannot approve execution;
- favorable events cannot approve order generation;
- favorable events cannot approve exchange connection;
- favorable events cannot approve capital allocation;
- favorable events cannot create confidence;
- favorable events cannot promote a strategy;
- favorable events cannot unblock `handoff_to_09`;
- negative events may block, degrade, suspend, escalate, or trigger hard veto review;
- critical events may trigger hard veto or Kill Switch review;
- critical events cannot be relaxed by favorable regime, LLM agreement, Bull/Bear agreement, fused signal alignment, Motor A, human optimism, or documentation completeness.

Favorable context may be recorded for audit. It must not change downstream eligibility.

## Current Event/Regime/Market Risk Baseline

Block 08 inherits the current Stage 08 baseline:

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
```

No event, regime, or market outcome may contradict this baseline.

Event/regime/market context may only preserve blocking, harden handling, escalate review, or record context under the current state.

## Event Risk Input Metadata

Expected event risk metadata includes:

- `event_risk_status`;
- `event_precedence_outcome`;
- `event_precedence_source_ref`;
- `event_precedence_hint`;
- `event_modulation_hook_reference`;
- `motor_c_severity`;
- `motor_c_source_ref`;
- `event_timestamp` or `event_window`;
- `event_scope`;
- `event_classification`;
- `event_directionality`;
- `event_source_artifact_ref`;
- `event_audit_trace_ref`;
- `event_metadata_status`;
- `event_metadata_quality`;
- `event_review_status`.

Absence of event metadata must not be resolved by inference. Missing or ambiguous event metadata must be marked unavailable, degraded, or review-required according to severity.

## Regime Risk Input Metadata

Expected regime risk metadata includes:

- `regime_status`;
- `regime_source_ref`;
- `regime_detection_method_ref`;
- `regime_as_of`;
- `regime_scope`;
- `regime_stability_status`;
- `regime_conflict_status`;
- `regime_metadata_status`;
- `regime_audit_trace_ref`.

Regime analysis may provide context. It cannot substitute Motor B empirical validation, create confidence, relax event risk, unlock Paper Trading, unlock Live Trading, justify execution, justify capital allocation, promote a strategy, or unblock `handoff_to_09`.

## Market Risk Input Metadata

Expected market risk metadata includes:

- `market_risk_status`;
- `market_risk_source_ref`;
- `volatility_context`;
- `liquidity_context`;
- `spread_context`, if available;
- `market_dislocation_flag`, if available;
- `exchange_risk_context`, if available;
- `asset_risk_context`, if available;
- `market_metadata_status`;
- `market_audit_trace_ref`.

Favorable or normal market context does not unlock anything. Elevated, high, extreme, conflicting, or unauditable market context may harden, degrade, block, suspend, escalate, or require review.

## Event Risk Classification Taxonomy

Documentary event risk classifications include:

- `event_risk_unavailable`;
- `event_risk_missing_metadata`;
- `event_risk_degraded_metadata`;
- `event_risk_neutral_context_only`;
- `event_risk_favorable_context_only`;
- `event_risk_negative_context`;
- `event_risk_high_negative_context`;
- `event_risk_critical`;
- `event_risk_conflicting_sources`;
- `event_risk_requires_human_review`;
- `event_risk_requires_risk_engine_review`;
- `event_risk_hard_veto_candidate`;
- `event_risk_kill_switch_candidate`.

`event_risk_favorable_context_only` cannot approve anything. It is context only and must preserve all downstream blocks.

## Regime Risk Classification Taxonomy

Documentary regime risk classifications include:

- `regime_risk_unavailable`;
- `regime_risk_missing_metadata`;
- `regime_risk_degraded_metadata`;
- `regime_risk_stable_context_only`;
- `regime_risk_unstable`;
- `regime_risk_conflicting_sources`;
- `regime_risk_high_uncertainty`;
- `regime_risk_requires_human_review`;
- `regime_risk_requires_risk_engine_review`;
- `regime_risk_hardening_required`.

A stable regime cannot approve anything. It is context only and cannot relax missing evidence, unavailable confidence, Motor B `framework_only`, or event risk constraints.

## Market Risk Classification Taxonomy

Documentary market risk classifications include:

- `market_risk_unavailable`;
- `market_risk_missing_metadata`;
- `market_risk_degraded_metadata`;
- `market_risk_normal_context_only`;
- `market_risk_elevated`;
- `market_risk_high`;
- `market_risk_extreme`;
- `market_risk_liquidity_concern`;
- `market_risk_volatility_concern`;
- `market_risk_exchange_concern`;
- `market_risk_asset_concern`;
- `market_risk_requires_human_review`;
- `market_risk_requires_risk_engine_review`;
- `market_risk_hardening_required`;
- `market_risk_kill_switch_candidate`.

`market_risk_normal_context_only` cannot approve anything. It is context only and must not change downstream eligibility.

## Event Precedence Override Boundary

Block 08 cannot relax event precedence from Stage 07.

Rules:

- if Stage 07 marks event critical, Stage 08 cannot downgrade it to favorable;
- if Stage 07 marks event negative, Stage 08 cannot convert it to approval;
- if Stage 07 event precedence metadata is missing, Stage 08 must mark it unavailable, degraded, or review-required;
- if event sources conflict, Stage 08 must preserve downstream blocking;
- if event is favorable, Stage 08 may record context but must preserve blocking;
- if event is critical, Stage 08 may escalate to hard veto or Kill Switch review.

Any relaxation would require formal replayable evidence, source reconciliation, and later governance. This block does not provide that relaxation path.

## Event/Regime/Market Non-Substitution Rule

Event, regime, and market context cannot substitute:

- Motor B empirical validation;
- real backtesting;
- OOS validation;
- walk-forward validation;
- robustness testing;
- empirical historical results;
- confidence evidence;
- auditability;
- risk policy compliance;
- Paper Trading eligibility gate.

Specifically:

- favorable event cannot substitute evidence;
- stable regime cannot substitute evidence;
- normal market context cannot substitute evidence;
- Motor C event context cannot substitute Motor B evidence;
- Motor A regime context cannot substitute Motor B evidence.

These elements may be audit context, risk context, or review context. They are not empirical evidence and cannot create confidence.

## Event Critical Escalation Rule

Critical events may produce:

- `event_risk_hard_veto_candidate`;
- `event_risk_kill_switch_candidate`;
- `all_downstream_blocked`;
- `paper_trading_blocked`;
- `live_trading_blocked`;
- `execution_blocked`;
- `capital_allocation_blocked`;
- `promotion_blocked`;
- `confidence_assignment_blocked`;
- `human_review_required`;
- `risk_engine_review_required`;
- `emergency_review_required`.

Escalation does not create the final `RiskDecision`. Block 12 will define and produce the formal `RiskDecision` later.

Block 08 escalation is a conservative gate outcome only. It cannot execute a Kill Switch, execute trades, route orders, allocate capital, or activate Paper Trading.

## Favorable Event Non-Approval Rule

Favorable events cannot produce:

- `confidence_score`;
- `final_signal_confidence_score`;
- `paper_trading_eligibility`;
- Live Trading approval through `live_trading_status`;
- `execution_eligibility`;
- `order_generation_eligibility`;
- `exchange_connection_eligibility`;
- `capital_allocation_eligibility`;
- strategy promotion;
- `handoff_to_09`;
- `downstream_operational_eligibility`.

A favorable event may only be recorded as context.

If an artifact attempts to convert a favorable event into approval, Block 08 must mark the attempt as a prohibited inference, downstream restriction violation, or hard veto candidate according to severity.

## Event/Regime/Market Gate Outcomes

Possible gate outcomes include:

- `event_market_gate_blocked_framework_only`;
- `event_market_gate_event_metadata_unavailable`;
- `event_market_gate_event_metadata_degraded`;
- `event_market_gate_favorable_context_recorded_only`;
- `event_market_gate_negative_event_blocking`;
- `event_market_gate_critical_event_escalation`;
- `event_market_gate_regime_context_recorded_only`;
- `event_market_gate_regime_uncertainty_hardening`;
- `event_market_gate_market_context_recorded_only`;
- `event_market_gate_market_risk_hardening`;
- `event_market_gate_requires_human_review`;
- `event_market_gate_requires_risk_engine_review`;
- `event_market_gate_hard_veto_candidate`;
- `event_market_gate_kill_switch_candidate`;
- `event_market_gate_no_downstream_eligibility`.

These outcomes are not the final `RiskDecision` of Block 12.

No outcome can approve Paper Trading, Live Trading, execution, order generation, exchange connection, capital allocation, productive position sizing, strategy promotion, confidence assignment, or `handoff_to_09` under the current state.

## Event/Regime/Market Risk Assessment Record

Stage 08 may document an Event/Regime/Market Risk Gate assessment with fields such as:

- `event_market_gate_record_id`;
- `stage_id`;
- `block_id`;
- `block_ref`;
- `assessed_at`;
- `source_artifact_id`;
- `source_stage`;
- `source_block`;
- `source_document_ref`;
- `event_precedence_outcome`;
- `event_risk_status`;
- `motor_c_severity`;
- `event_precedence_hint`;
- `event_modulation_hook_reference`;
- `event_metadata_status`;
- `event_risk_classification`;
- `regime_status`;
- `regime_risk_classification`;
- `market_risk_status`;
- `market_risk_classification`;
- `event_asymmetry_applied`;
- `favorable_event_unlock_attempt_detected`;
- `critical_event_relaxation_attempt_detected`;
- `non_substitution_confirmed`;
- `downstream_blocking_status`;
- `paper_trading_eligibility`;
- `live_trading_status`;
- `execution_eligibility`;
- `order_generation_eligibility`;
- `exchange_connection_eligibility`;
- `capital_allocation_eligibility`;
- `promotion_status`;
- `handoff_to_09`;
- `confidence_status`;
- `confidence_score`;
- `final_signal_confidence_score`;
- `gate_outcome`;
- `required_review`;
- `required_evidence`;
- `audit_trace_ref`;
- `final_note_non_operational`.

This block does not create a database, storage layer, event engine, regime engine, market risk engine, productive gate, or executable assessment implementation. This record is documentary only.

## Current Gate Conclusion

Under the current state:

```text
event_gate_status = non_operational
event_precedence_consumption_status = documentary_only
event_metadata_status = unavailable_or_framework_only_unless_provided_by_07
event_risk_cannot_unlock_downstream = true
favorable_events_unlock_nothing = true
critical_events_can_escalate = true
evidence_completeness_level = framework_only
simulation_status = backtest_not_implemented
oos_validation_status = oos_not_available
walk_forward_status = walk_forward_not_available
robustness_status = robustness_not_available
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
live_trading_status = blocked
execution_eligibility = blocked
order_generation_eligibility = blocked
exchange_connection_eligibility = blocked
capital_allocation_eligibility = blocked
productive_position_sizing_eligibility = blocked
risk_budget_activation = blocked
promotion_status = not_promoted
promotion_eligibility = blocked
handoff_to_09 = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

There is no downstream operational eligibility.

## Relationship With Stage 07

Block 08 consumes Stage 07 event precedence and related event metadata.

The controlling Stage 07 reference is:

`07 Signal Fusion + LLM Motors/docs/99_signal_fusion_llm_motors_closure.md`

Relevant Stage 07 event references include:

- `event_precedence_outcome` from Stage 07 Block 08, if present;
- `event_risk_status` from `RiskHandoffPackage`, if present;
- Motor C severity from Stage 07 Block 04, if present;
- `event_precedence_hint` from Stage 07 Block 04, if present;
- `event_modulation_hook_reference` from Stage 07 Block 06, if present.

Stage 07 outputs cannot be used as operational approval. Stage 07 did not approve Paper Trading, Live Trading, execution, capital allocation, strategy promotion, confidence, or runtime LLM operations.

Block 08 consumes Stage 07 event precedence only as governed, non-operational risk metadata.

## Relationship With Block 03

Block 03 preserves Motor B `framework_only` and blocks downstream eligibility.

Block 08 cannot use event, regime, or market context to override Block 03.

Even if event context is favorable, regime context is stable, or market context is normal, Motor B remains `framework_only`, evidence remains insufficient, confidence remains unavailable, and downstream eligibility remains blocked.

## Relationship With Block 05

Block 05 defines hard veto and Kill Switch triggers.

Block 08 may identify event, regime, or market conditions as hard veto candidates or Kill Switch review candidates.

Block 08 does not execute Kill Switch, does not produce a final hard veto decision, and does not produce the final `RiskDecision`.

Critical event escalation from Block 08 may become an input to Block 05-style veto/Kill Switch handling and later Block 12 RiskDecision handling.

## Relationship With Block 07

Block 07 preserves `confidence_not_available` and evidence insufficiency.

Block 08 cannot use event, regime, or market context to create confidence or evidence sufficiency.

Event precedence, Motor C severity, regime status, market context, favorable events, stable regimes, or normal market conditions cannot create `confidence_score`, `final_signal_confidence_score`, empirical support, or eligibility confidence.

## Relationship With Block 11

Block 11 — Paper Trading Eligibility Gate will define complete Paper Trading eligibility conditions.

Block 08 cannot approve Paper Trading. It can only block, harden, degrade, suspend, escalate, require review, or record event/regime/market context.

Under `framework_only`, Paper Trading remains blocked regardless of event, regime, or market context.

## Relationship With Block 12

Block 12 — Risk Decision Engine will produce the formal `RiskDecision`.

Block 08 produces gate outcomes and documentary assessment records. It does not produce the final `RiskDecision`.

An event/regime/market gate outcome may become input to Block 12, but it must not be converted into trade execution, Paper Trading readiness, Live Trading readiness, capital allocation, strategy promotion, confidence assignment, or `handoff_to_09` approval.

## Explicit Non-Goals

This block does not:

- redefine Stage 07 event precedence from scratch;
- approve Paper Trading;
- approve Live Trading;
- approve execution;
- approve order generation;
- approve exchange connection;
- approve capital allocation;
- approve strategy promotion;
- approve `handoff_to_09`;
- create `confidence_score`;
- create `final_signal_confidence_score`;
- create empirical evidence;
- substitute Motor B evidence;
- run backtesting;
- run OOS validation;
- run walk-forward;
- run robustness;
- implement event engine;
- implement regime engine;
- implement market risk engine;
- execute Kill Switch;
- create hard veto final decision;
- create RiskDecision final;
- create Paper Trading eligibility gate;
- create productive exposure templates;
- create human override policy;
- create audit replay.
