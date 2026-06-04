# 08 Risk Engine — Block 11: Paper Trading Eligibility Gate

## Purpose

Block 11 defines the documentary Paper Trading eligibility gate for Stage 08 Risk Engine.

This gate defines minimum future conditions for considering Paper Trading review. It does not approve Paper Trading in the current state.

Under `framework_only`, the mandatory conclusion is:

```text
paper_trading_eligibility = blocked
```

Paper Trading Eligibility Gate does not mean Paper Trading ready. It is a governance boundary that preserves blocking until empirical evidence, auditability, risk controls, promotion review, and Risk Engine review exist in a future governed path.

## Paper Trading Gate Authority

Stage 08 / Block 11 may:

- declare Paper Trading blocked;
- declare Paper Trading not eligible;
- define future Paper Trading prerequisites;
- reject Paper Trading requests;
- require empirical evidence;
- require real backtesting;
- require OOS validation;
- require walk-forward validation;
- require robustness testing;
- require risk policy compliance;
- require exposure/position/capital constraints review;
- require event/regime/market risk review;
- require confidence availability, if governance requires it;
- require human review, if needed;
- require Risk Engine review;
- preserve downstream blocking.

Block 11 cannot approve Paper Trading under `framework_only`.

Any Paper Trading request under the current state must be routed to blocked, not eligible, rejected, or future-evidence-required handling.

## Current Framework-Only Paper Trading Baseline

The current Paper Trading baseline is:

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
```

No Paper Trading eligibility outcome may contradict this baseline.

If an artifact, package, request, review note, or downstream consumer attempts to contradict this baseline, Block 11 must preserve blocking and route the issue to rejection, degradation, hard veto candidate, Kill Switch review candidate, human review, or Risk Engine review according to severity.

## Mandatory Blocked Conclusion Under Framework-Only

Under `framework_only`:

- `paper_trading_eligibility = blocked`;
- Paper Trading is not ready;
- Paper Trading is not approved;
- Paper Trading is not provisionally approved;
- Paper Trading is not conditionally approved;
- Paper Trading is not review-approved;
- Paper Trading is not human-review-approved;
- Paper Trading is not LLM-assisted-approved;
- Paper Trading is not strategy-promoted;
- Paper Trading is not downstream eligible;
- `handoff_to_09 = blocked`.

Any request for Paper Trading under `framework_only` must produce blocked, not eligible, or requires future evidence. It must never produce approval.

Internal review inside Stage 08 is not Paper Trading readiness.

## Minimum Future Paper Trading Prerequisites

Future Paper Trading review would require, at minimum:

- real backtesting results;
- versioned backtest configuration;
- reproducible backtest run;
- OOS validation;
- walk-forward validation;
- robustness testing;
- empirical historical results;
- transaction cost assumptions;
- slippage assumptions;
- drawdown analysis;
- data version references;
- feature version references;
- strategy version references;
- risk policy compliance;
- exposure/position/capital constraint review;
- event/regime/market risk review;
- strategy promotion review;
- confidence availability, if required by governance;
- audit trace;
- quality gate results;
- no blocking gaps;
- no active hard veto;
- no Kill Switch review required;
- human review, if required;
- Risk Engine review.

Listing these requirements does not mean they exist currently.

Future review must be versioned, reproducible, auditable, empirically supported, and governed by later Stage 08 controls.

## Paper Trading Blockers

Current Paper Trading blockers include:

- `framework_only`;
- `simulation_status = backtest_not_implemented`;
- `oos_validation_status = oos_not_available`;
- `walk_forward_status = walk_forward_not_available`;
- `robustness_status = robustness_not_available`;
- empirical historical results missing;
- `confidence_status = confidence_not_available`;
- `confidence_score = null`;
- `final_signal_confidence_score = null`;
- missing evidence;
- blocking gaps;
- audit trace missing or insufficient;
- risk policy not active;
- exposure constraints documentary only;
- capital allocation blocked;
- productive position sizing blocked;
- risk budget activation blocked;
- `promotion_status = not_promoted`;
- hard veto candidate;
- Kill Switch review required;
- event critical;
- source conflict;
- contract violation;
- `handoff_to_09 = blocked`.

Any material blocker is sufficient to keep Paper Trading ineligible.

Blockers must remain explicit for audit traceability and must not be resolved by inference, documentation completeness, LLM output, human optimism, or favorable context.

## Paper Trading Eligibility Taxonomy

Documentary Paper Trading eligibility values include:

- `paper_trading_eligibility_blocked_framework_only`;
- `paper_trading_eligibility_blocked_missing_backtest`;
- `paper_trading_eligibility_blocked_missing_oos`;
- `paper_trading_eligibility_blocked_missing_walk_forward`;
- `paper_trading_eligibility_blocked_missing_robustness`;
- `paper_trading_eligibility_blocked_missing_empirical_results`;
- `paper_trading_eligibility_blocked_confidence_unavailable`;
- `paper_trading_eligibility_blocked_audit_missing`;
- `paper_trading_eligibility_blocked_risk_policy_missing`;
- `paper_trading_eligibility_blocked_constraints_not_active`;
- `paper_trading_eligibility_blocked_capital_allocation`;
- `paper_trading_eligibility_blocked_position_sizing`;
- `paper_trading_eligibility_blocked_promotion_not_available`;
- `paper_trading_eligibility_blocked_hard_veto`;
- `paper_trading_eligibility_blocked_kill_switch_review`;
- `paper_trading_eligibility_blocked_event_risk`;
- `paper_trading_eligibility_blocked_handoff_to_09`;
- `paper_trading_eligibility_requires_more_evidence_future_only`;
- `paper_trading_eligibility_future_review_candidate_only_after_empirical_evidence`.

Under `framework_only`, the following values are prohibited:

- `paper_trading_eligibility_approved`;
- `paper_trading_eligibility_ready`;
- `paper_trading_eligibility_conditionally_approved`;
- `paper_trading_eligibility_provisionally_approved`;
- `paper_trading_eligibility_human_review_approved`.

`paper_trading_eligibility_requires_more_evidence_future_only` is not approval, is not readiness, is not conditional approval, and does not allow Paper Trading. It only records that more empirical evidence would be required for a future review.

`paper_trading_eligibility_future_review_candidate_only_after_empirical_evidence` is not approval. It means only that a future review could be considered after empirical evidence and governance exist.

## Paper Trading Request Rejection Rules

Any direct request for Paper Trading under `framework_only` must be rejected, blocked, or marked as future evidence required.

Rejected or blocked request types include:

- direct Paper Trading activation request;
- strategy-to-paper request;
- fused-signal-to-paper request;
- human-review-to-paper request;
- LLM-assisted Paper Trading request;
- documentation-only Paper Trading request;
- mock-result Paper Trading request;
- synthetic-test Paper Trading request;
- confidence-null Paper Trading request;
- backtest-missing Paper Trading request.

None of these requests can become approval.

If a request attempts to bypass Motor B evidence, confidence availability, risk policy compliance, promotion status, or Stage 08 blocking, the request must be preserved as a prohibited inference or boundary violation for audit review.

## Non-Substitution Rule for Paper Trading

Paper Trading eligibility cannot be substituted by:

- `StrategyDossier` completeness;
- strategy registry presence;
- strategy candidate status;
- Stage 05 mock examples;
- Stage 07 fused candidates;
- `ConfidenceGovernanceResult`;
- Bull/Bear agreement;
- LLM agreement;
- LLM textual confidence;
- Motor A context;
- Motor C context;
- event favorable context;
- stable regime context;
- normal market context;
- policy registry entries;
- constraints documented;
- `hard_veto_not_triggered`;
- `kill_switch_not_required`;
- human review metadata;
- human optimism;
- documentation completeness;
- synthetic tests;
- mock scenarios.

These elements may provide context, traceability, review surfaces, or audit metadata. They are not Paper Trading eligibility evidence.

## Relationship With Block 03

Block 03 blocks downstream eligibility because Motor B is `framework_only`.

Block 11 cannot approve Paper Trading while Block 03 remains blocked or `framework_only`.

Motor B must provide sufficient empirical evidence in a future governed path before Paper Trading review can even be considered.

## Relationship With Block 06

Block 06 classifies missing evidence and blocking gaps.

Block 11 uses those gaps as Paper Trading blockers and does not resolve them.

Missing evidence, incomplete evidence, unauditable evidence, insufficient evidence, and blocking gaps must remain explicit until resolved by proper future artifacts and review.

## Relationship With Block 07

Block 07 preserves `confidence_not_available`.

Block 11 cannot approve Paper Trading with confidence unavailable or `confidence_score = null` if governance requires confidence.

Block 11 does not create confidence.

LLM confidence, Bull/Bear agreement, Stage 07 fusion alignment, human optimism, or documentation completeness cannot become Paper Trading confidence.

## Relationship With Block 08

Block 08 handles event, regime, and market risk.

Block 11 cannot use favorable events, stable regime, or normal market context to approve Paper Trading.

Negative or critical events may block, harden, suspend, require review, or escalate Paper Trading handling.

## Relationship With Block 09

Block 09 documents exposure, position, and capital constraints.

Block 11 cannot approve Paper Trading while constraints are documentary, capital allocation is blocked, productive position sizing is blocked, and risk budgets are blocked.

Documented constraints are not active operational safeguards under the current state.

## Relationship With Block 10

Block 10 defines strategy promotion and downgrade rules.

Block 11 cannot approve Paper Trading while:

- `promotion_status = not_promoted`;
- `promotion_eligibility = blocked`.

A strategy cannot become Paper Trading ready through promotion language under `framework_only`.

## Relationship With Block 12

Block 12 will produce the formal `RiskDecision`.

Block 11 produces Paper Trading eligibility outcomes, but not the final `RiskDecision`.

A Paper Trading eligibility assessment may become input to Block 12, but it must not be converted into Paper Trading activation, execution, order generation, exchange connection, capital allocation, position sizing, confidence assignment, or `handoff_to_09` approval under the current state.

## Paper Trading Eligibility Assessment Record

Stage 08 may document a Paper Trading eligibility assessment with fields such as:

- `paper_trading_gate_record_id`;
- `strategy_id`;
- `source_stage`;
- `source_block`;
- `source_document_ref`;
- `assessed_at`;
- `requested_transition`;
- `paper_trading_request_type`;
- `paper_trading_eligibility`;
- `paper_trading_blocked_reason`;
- `evidence_completeness_level`;
- `simulation_status`;
- `oos_validation_status`;
- `walk_forward_status`;
- `robustness_status`;
- `empirical_results_status`;
- `confidence_status`;
- `confidence_score`;
- `final_signal_confidence_score`;
- `missing_evidence_flags`;
- `blocking_gap_flags`;
- `hard_veto_status`;
- `kill_switch_review_status`;
- `event_risk_status`;
- `exposure_constraint_status`;
- `capital_allocation_eligibility`;
- `productive_position_sizing_eligibility`;
- `risk_budget_activation`;
- `promotion_status`;
- `promotion_eligibility`;
- `downstream_operational_eligibility`;
- `handoff_to_09`;
- `required_future_evidence`;
- `required_review`;
- `audit_trace_ref`;
- `final_note_non_operational`.

This block does not create a database, storage layer, Paper Trading runtime, Paper Trading simulator, execution simulator, or executable eligibility engine. This structure is documentary only.

## Current Gate Conclusion

Under the current state:

```text
paper_trading_gate_status = non_operational
paper_trading_eligibility = blocked
paper_trading_ready = false
paper_trading_review_candidate_currently = false
paper_trading_review_candidate_future_only_after_empirical_evidence = true
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
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

There is no Paper Trading eligibility under `framework_only`.

Paper Trading Gate does not mean Paper Trading ready.

## Explicit Non-Goals

This block does not:

- approve Paper Trading;
- activate Paper Trading;
- declare Paper Trading ready;
- create Paper Trading runtime;
- create Paper Trading execution simulator;
- create order generation;
- create exchange connection;
- create execution engine;
- approve Live Trading;
- approve capital allocation;
- calculate productive position sizing;
- activate risk budgets;
- promote strategies;
- create `confidence_score`;
- create `final_signal_confidence_score`;
- create empirical evidence;
- run backtesting;
- run OOS validation;
- run walk-forward;
- run robustness;
- implement strategy selector;
- implement signal generator;
- create RiskDecision final;
- create human override policy;
- create audit replay.
