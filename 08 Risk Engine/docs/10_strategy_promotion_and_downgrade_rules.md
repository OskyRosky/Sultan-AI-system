# 08 Risk Engine — Block 10: Strategy Promotion and Downgrade Rules

## Purpose

Block 10 defines documentary rules for strategy promotion, downgrade, suspension, review, and blocking inside Stage 08 Risk Engine.

Under the current `framework_only` state, no strategy promotion is possible.

This block does not promote strategies. It does not approve Paper Trading. It does not approve Live Trading. It does not assign capital. It does not enable execution, order generation, exchange connection, productive position sizing, risk budget activation, or strategy deployment. It does not create `confidence_score` or `final_signal_confidence_score`.

Block 10 may define future promotion prerequisites and conservative downgrade paths. Under the current state, promotion remains blocked and only risk-reducing transitions such as blocked, review-required, suspended, degraded, rejected, or not-promoted are permitted.

## Promotion and Downgrade Authority

Stage 08 / Block 10 may:

- preserve `not_promoted`;
- block strategy promotion;
- downgrade to blocked;
- downgrade to review;
- downgrade to suspended;
- require human review;
- require Risk Engine review;
- require more evidence;
- mark promotion evidence missing;
- mark promotion evidence insufficient;
- reject promotion claims;
- block promotion under `framework_only`;
- define future promotion prerequisites.

Stage 08 can downgrade conservatively, but cannot promote under `framework_only`.

Downgrade, suspension, review, rejection, or continued blocking are valid because they reduce or preserve risk posture. Promotion is not valid under the current evidence state.

## Current Framework-Only Promotion Baseline

The current promotion baseline is:

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

No promotion, downgrade, suspension, review, or blocking outcome may contradict this baseline.

Any artifact that attempts to upgrade `promotion_status`, infer promotion eligibility, or reinterpret `framework_only` as empirical support must be rejected, blocked, downgraded, or escalated to Risk Engine review according to severity.

## No Promotion Under Framework-Only Rule

Under `framework_only`:

- no strategy promotion is allowed;
- no conditional promotion is allowed;
- no provisional promotion is allowed;
- no Paper Trading promotion is allowed;
- no Live Trading promotion is allowed;
- no execution promotion is allowed;
- no capital allocation promotion is allowed;
- no confidence-based promotion is allowed;
- no human-review-only promotion is allowed;
- no LLM-assisted promotion is allowed;
- no documentation-only promotion is allowed;
- no mock-result promotion is allowed;
- no synthetic-test promotion is allowed.

Promotion remains blocked until empirical evidence, governance, and Risk Engine review exist in a future stage.

Listing future prerequisites does not imply that promotion can be approved now.

## Conservative Downgrade Rule

Conservative downgrades are allowed because they reduce risk.

Permitted conservative strategy states include:

- `strategy_status_blocked`;
- `strategy_status_review_required`;
- `strategy_status_suspended`;
- `strategy_status_degraded`;
- `strategy_status_rejected`;
- `strategy_status_not_promoted`;
- `strategy_status_evidence_missing`;
- `strategy_status_confidence_unavailable`;
- `strategy_status_framework_only_blocked`.

Downgrade, review, rejection, suspension, degradation, or continued not-promoted status does not approve operational use.

A conservative downgrade may be applied even when an artifact is structurally valid if evidence, confidence, audit trace, risk policy compliance, or source consistency is missing or insufficient.

## Promotion Blockers

Promotion blockers include:

- `framework_only`;
- missing backtesting;
- missing OOS validation;
- missing walk-forward validation;
- missing robustness testing;
- missing empirical historical results;
- missing confidence;
- `confidence_score = null`;
- `final_signal_confidence_score = null`;
- missing audit trace;
- missing reproducibility metadata;
- missing strategy version;
- missing data version;
- missing feature version;
- unresolved blocking gaps;
- active hard veto;
- Kill Switch review required;
- event critical;
- source conflict;
- contract violation;
- missing `non_approval_statement`;
- forbidden downstream usage missing;
- insufficient risk policy compliance;
- capital allocation blocked;
- position sizing blocked;
- `handoff_to_09` blocked.

Any one material blocker is sufficient to prevent promotion. Multiple blockers may coexist and must be preserved for audit traceability.

## Future Promotion Prerequisites

Future promotion review would require, at minimum:

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
- risk policy compliance;
- exposure/position/capital constraints reviewed;
- event/regime/market risk reviewed;
- confidence availability, if required by governance;
- quality gate results;
- audit trace;
- no blocking gaps;
- no active hard veto;
- no Kill Switch review required;
- human review if required;
- Risk Engine review.

These requirements do not exist currently and do not imply approval.

Future promotion review must be versioned, reproducible, auditable, empirically supported, and governed by later Stage 08 controls.

## Strategy State Taxonomy

Documentary strategy state values include:

- `strategy_status_not_promoted`;
- `strategy_status_blocked`;
- `strategy_status_framework_only_blocked`;
- `strategy_status_missing_evidence`;
- `strategy_status_confidence_unavailable`;
- `strategy_status_review_required`;
- `strategy_status_risk_engine_review_required`;
- `strategy_status_human_review_required`;
- `strategy_status_degraded`;
- `strategy_status_suspended`;
- `strategy_status_rejected`;
- `strategy_status_future_review_candidate_only_after_empirical_evidence`.

Under `framework_only`, the following states are prohibited:

- `strategy_status_promoted`;
- `strategy_status_paper_trading_ready`;
- `strategy_status_live_trading_ready`;
- `strategy_status_execution_ready`;
- `strategy_status_capital_allocated`;
- `strategy_status_confidence_approved`.

No strategy state may be interpreted as operational approval under the current state.

## Promotion Eligibility Taxonomy

Promotion eligibility values include:

- `promotion_eligibility_blocked_framework_only`;
- `promotion_eligibility_blocked_missing_backtest`;
- `promotion_eligibility_blocked_missing_oos`;
- `promotion_eligibility_blocked_missing_walk_forward`;
- `promotion_eligibility_blocked_missing_robustness`;
- `promotion_eligibility_blocked_missing_empirical_results`;
- `promotion_eligibility_blocked_confidence_unavailable`;
- `promotion_eligibility_blocked_audit_missing`;
- `promotion_eligibility_blocked_risk_policy_missing`;
- `promotion_eligibility_blocked_hard_veto`;
- `promotion_eligibility_blocked_kill_switch_review`;
- `promotion_eligibility_blocked_event_critical`;
- `promotion_eligibility_blocked_capital_allocation`;
- `promotion_eligibility_blocked_position_sizing`;
- `promotion_eligibility_blocked_handoff_to_09`;
- `promotion_eligibility_future_review_candidate_only`.

There is no approved promotion eligibility under the current state.

`promotion_eligibility_future_review_candidate_only` is not approval. It means only that future review could be considered after empirical evidence and governance exist.

## Downgrade Trigger Taxonomy

Conservative downgrade triggers include:

- `downgrade_trigger_framework_only`;
- `downgrade_trigger_missing_evidence`;
- `downgrade_trigger_confidence_unavailable`;
- `downgrade_trigger_confidence_invention`;
- `downgrade_trigger_source_conflict`;
- `downgrade_trigger_contract_violation`;
- `downgrade_trigger_event_critical`;
- `downgrade_trigger_market_risk_high`;
- `downgrade_trigger_regime_uncertainty`;
- `downgrade_trigger_audit_trace_missing`;
- `downgrade_trigger_policy_non_compliance`;
- `downgrade_trigger_hard_veto`;
- `downgrade_trigger_kill_switch_review`;
- `downgrade_trigger_human_override_violation`;
- `downgrade_trigger_synthetic_evidence_as_real`;
- `downgrade_trigger_forbidden_downstream_usage_violation`.

Downgrade triggers are conservative and may only reduce, block, suspend, reject, degrade, or escalate status.

No downgrade trigger may be reinterpreted as a promotion trigger.

## Promotion Prohibited Substitutes

The following cannot substitute for promotion evidence:

- `StrategyDossier` completeness;
- strategy registry presence;
- strategy candidate status;
- Stage 05 mock examples;
- Stage 07 fused candidates;
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

These elements may provide context, traceability, or review surfaces. They are not promotion evidence and cannot create operational readiness.

## StrategyDossier and Stage 05 Boundary

Stage 05 Strategy Engine defines `StrategyDossier`, registry, candidates, quality gates, and risk templates as a framework.

Stage 05 boundaries:

- `StrategyDossier` is not promotion;
- strategy candidate is not promotion;
- registry presence is not promotion;
- quality gate documentation is not promotion;
- risk template presence is not capital approval;
- mock examples are not empirical evidence;
- Stage 05 does not approve operational trading under the current state.

Stage 05 artifacts may be consumed as review context only. They cannot replace Motor B empirical evidence, Stage 06 backtesting, OOS validation, walk-forward validation, robustness testing, confidence availability, or Risk Engine approval.

## Stage 07 Fusion Boundary

Stage 07 fusion outputs cannot promote a strategy.

Stage 07 boundaries:

- `FusedSignalCandidate` is not promotion;
- `ConfidenceGovernanceResult` is not promotion;
- Bull/Bear agreement is not promotion;
- `review_package_only` is not promotion;
- signal fusion alignment is not promotion;
- LLM ensemble agreement is not promotion.

Stage 07 outputs remain non-operational review artifacts under the current state.

## Human Review Boundary

Human review can require review, block, reject, suspend, or request evidence.

Human review cannot promote under `framework_only` without empirical evidence and formal future governance.

This block prohibits:

- human-review-only promotion;
- human override promotion under `framework_only`;
- manual approval without audit trace;
- manual approval without empirical evidence;
- manual approval without Risk Engine review.

Human review metadata is audit context. It is not a substitute for backtesting, OOS validation, walk-forward validation, robustness testing, or confidence availability.

## Promotion/Downgrade Output Record

Stage 08 may document a promotion/downgrade assessment with fields such as:

- `strategy_transition_record_id`;
- `strategy_id`;
- `strategy_name`;
- `source_stage`;
- `source_block`;
- `source_document_ref`;
- `source_strategy_ref`;
- `assessed_at`;
- `current_strategy_status`;
- `requested_transition`;
- `transition_allowed`;
- `transition_blocked_reason`;
- `promotion_status`;
- `promotion_eligibility`;
- `downgrade_trigger`;
- `downgrade_outcome`;
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
- `handoff_to_09`;
- `required_future_evidence`;
- `required_review`;
- `audit_trace_ref`;
- `final_note_non_operational`.

This block does not create a database, storage layer, promotion engine, downgrade engine, strategy selector, signal generator, or executable transition system. This structure is documentary only.

## Current Gate Conclusion

Under the current state:

```text
promotion_status = not_promoted
promotion_eligibility = blocked
strategy_status = strategy_status_framework_only_blocked
paper_trading_eligibility = blocked
live_trading_status = blocked
execution_eligibility = blocked
order_generation_eligibility = blocked
exchange_connection_eligibility = blocked
capital_allocation_eligibility = blocked
productive_position_sizing_eligibility = blocked
risk_budget_activation = blocked
handoff_to_09 = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

There is no strategy promotion under `framework_only`.

Only conservative downgrade, review, suspension, rejection, degradation, or continued blocking states are valid under the current state.

## Relationship With Stage 05

Stage 05 Strategy Engine defines strategy candidates and `StrategyDossier`.

Block 10 consumes those artifacts as review context only.

Block 10 cannot convert Stage 05 artifacts into promotion without empirical evidence and future governance.

Stage 05 mockups, registry entries, risk templates, quality gates, closure records, or dossiers are not operational approvals.

## Relationship With Block 03

Block 03 blocks downstream eligibility due to Motor B `framework_only`.

Block 10 cannot promote a strategy while Block 03 remains blocked.

Motor B must provide sufficient empirical evidence in a future governed path before promotion review can even be considered.

## Relationship With Block 07

Block 07 preserves `confidence_not_available`.

Block 10 cannot promote without confidence availability if future governance requires confidence.

Block 10 cannot create confidence.

LLM confidence, Bull/Bear agreement, Stage 07 fusion alignment, human optimism, or documentation completeness cannot become promotion confidence.

## Relationship With Block 09

Block 09 documents exposure, position, and capital constraints.

Block 10 cannot promote a strategy into capital allocation or position sizing while Block 09 remains documentary and blocked.

Documented constraints, templates, or risk budgets do not constitute promotion prerequisites unless future empirical evidence and governance make them applicable.

## Relationship With Block 11

Block 11 — Paper Trading Eligibility Gate will define Paper Trading eligibility.

Block 10 cannot declare Paper Trading eligibility. It can only define promotion/downgrade rules and preserve blocking.

A strategy cannot become Paper Trading ready through promotion language under `framework_only`.

## Relationship With Block 12

Block 12 — Risk Decision Engine will produce the formal `RiskDecision`.

Block 10 produces transition and gate outcomes, but not the final `RiskDecision`.

A promotion/downgrade record may become input to Block 12, but it must not be converted into trade execution, Paper Trading readiness, Live Trading readiness, capital allocation, strategy promotion, confidence assignment, or `handoff_to_09` approval under the current state.

## Explicit Non-Goals

This block does not:

- promote strategies;
- approve Paper Trading;
- approve Live Trading;
- approve execution;
- approve capital allocation;
- approve position sizing;
- approve risk budget activation;
- approve `handoff_to_09`;
- create `confidence_score`;
- create `final_signal_confidence_score`;
- create empirical evidence;
- run backtesting;
- run OOS validation;
- run walk-forward;
- run robustness;
- implement strategy selector;
- implement signal generator;
- implement execution engine;
- implement capital allocator;
- implement portfolio optimizer;
- create Paper Trading eligibility gate;
- create RiskDecision final;
- create human override policy;
- create audit replay.
