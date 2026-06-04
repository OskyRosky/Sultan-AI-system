# 08 Risk Engine — Block 12: Risk Decision Engine

## Purpose

Block 12 defines the documentary Risk Decision Engine for Stage 08 Risk Engine.

This block consolidates documentary inputs and gate outcomes from Blocks 01-11 to produce a formal conceptual `RiskDecision`.

`RiskDecision` is a risk-state decision. It is not trade execution, not order generation, not exchange connection, not capital allocation, not productive position sizing, not automatic Paper Trading approval, and not Live Trading approval.

Under the current `framework_only` state, this block must preserve blocking, null confidence, no promotion, no operational handoff, and no downstream operational eligibility.

## Risk Decision Authority

Stage 08 / Block 12 may:

- produce `RiskDecision`;
- veto;
- block;
- preserve `framework_only` blocking;
- preserve `paper_trading_eligibility = blocked`;
- preserve `downstream_operational_eligibility = blocked`;
- preserve `handoff_to_09 = blocked`;
- preserve `confidence_status = confidence_not_available`;
- require more evidence;
- require human review;
- require Risk Engine review;
- classify missing evidence;
- classify insufficient evidence;
- classify confidence unavailable;
- classify event risk blocking;
- classify contract violation;
- classify hard veto candidate;
- classify Kill Switch review required.

`RiskDecision` can reduce risk, preserve risk blocks, require review, require future evidence, or veto. It cannot execute or approve operational activity under `framework_only`.

## Current Framework-Only Risk Decision Baseline

The current RiskDecision baseline is:

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
risk_decision_operational_effect = non_operational_blocking_only
```

No RiskDecision outcome may contradict this baseline under `framework_only`.

If an artifact requests or implies an upgrade from this baseline, Block 12 must preserve blocking and route the issue to rejection, veto, required review, or future-evidence-required handling according to severity.

## RiskDecision Is Not Execution Rule

RiskDecision is not trade execution.

RiskDecision is not order generation.

RiskDecision is not exchange connection.

RiskDecision is not order routing.

RiskDecision is not capital allocation.

RiskDecision is not productive position sizing.

RiskDecision is not risk budget activation.

RiskDecision is not Paper Trading runtime.

RiskDecision is not Paper Trading simulator.

RiskDecision is not Live Trading readiness.

RiskDecision cannot send orders.

RiskDecision cannot allocate capital.

RiskDecision cannot activate strategies.

Any artifact that treats a RiskDecision as an executable command, trading instruction, exchange permission, order-routing instruction, capital allocation instruction, strategy activation, or Paper Trading runtime permission must be blocked or vetoed.

## Paper Trading Non-Approval Rule

RiskDecision does not automatically approve Paper Trading.

RiskDecision cannot approve Paper Trading under `framework_only`.

RiskDecision cannot convert `paper_trading_review_candidate_future_only` into Paper Trading ready.

RiskDecision cannot convert `paper_trading_eligibility_requires_more_evidence_future_only` into conditional approval.

RiskDecision cannot convert human review into Paper Trading approval under `framework_only`.

RiskDecision cannot convert `StrategyDossier` into Paper Trading approval.

RiskDecision cannot convert Stage 07 fusion into Paper Trading approval.

RiskDecision cannot override Block 11 while `paper_trading_eligibility = blocked`.

Under the current state:

```text
paper_trading_eligibility = blocked
handoff_to_09 = blocked
```

Paper Trading remains unavailable until future empirical evidence, governance, Risk Engine review, and later eligibility controls exist. This block does not create that future path.

## blocked_missing_evidence vs requires_more_evidence

`blocked_missing_evidence` means:

Required evidence does not exist, was not produced, is not versioned, or is not auditable.

`requires_more_evidence` means:

Some evidence exists, but it is insufficient in quality, coverage, robustness, OOS validation, stability, sample size, regime coverage, or traceability.

`blocked_missing_evidence` is stronger than `requires_more_evidence`.

`blocked_missing_evidence` blocks downstream eligibility.

`requires_more_evidence` also does not approve anything.

`requires_more_evidence` is not conditional approval.

`requires_more_evidence` is not Paper Trading readiness.

`requires_more_evidence` is not `handoff_to_09`.

`requires_more_evidence` cannot be used as approval language.

Under the current Sultan state, because Motor B is `framework_only`, missing backtesting, missing OOS validation, missing walk-forward validation, missing robustness, and missing empirical historical results must map to `blocked_missing_evidence`, not merely `requires_more_evidence`.

## RiskDecision State Taxonomy

Documentary RiskDecision states include:

- `risk_vetoed`;
- `blocked_framework_only`;
- `blocked_missing_evidence`;
- `requires_more_evidence`;
- `blocked_confidence_unavailable`;
- `blocked_event_risk`;
- `blocked_contract_violation`;
- `blocked_hard_veto`;
- `blocked_kill_switch_review_required`;
- `blocked_paper_trading_not_eligible`;
- `blocked_live_trading_not_eligible`;
- `blocked_execution_not_eligible`;
- `blocked_capital_allocation_not_eligible`;
- `blocked_position_sizing_not_eligible`;
- `blocked_strategy_promotion_not_eligible`;
- `requires_human_review`;
- `requires_risk_engine_review`;
- `paper_trading_not_eligible`;
- `paper_trading_review_candidate_future_only`;
- `no_downstream_operational_eligibility`.

Under `framework_only`, the following values are prohibited:

- `risk_approved`;
- `trading_approved`;
- `paper_trading_approved`;
- `paper_trading_ready`;
- `live_trading_approved`;
- `execution_approved`;
- `capital_allocation_approved`;
- `position_sizing_approved`;
- `strategy_promoted`;
- `confidence_approved`.

`paper_trading_review_candidate_future_only` is not approval and cannot be used currently under `framework_only` as operational readiness.

## RiskDecision Precedence Rules

RiskDecision precedence is conservative:

- hard veto overrides all non-veto states;
- Kill Switch review required overrides favorable context;
- `framework_only` blocks downstream eligibility;
- missing evidence blocks downstream eligibility;
- confidence unavailable blocks confidence-based eligibility;
- event critical can block or escalate;
- contract violation blocks downstream eligibility;
- source conflict requires review or blocks;
- Paper Trading blocked remains blocked unless future empirical evidence and governance exist;
- favorable events cannot override missing evidence;
- stable regime cannot override missing evidence;
- normal market context cannot override missing evidence;
- human review cannot override `framework_only` without future governance and empirical evidence.

Precedence can harden, veto, require review, or preserve blocking. It cannot approve operational use under the current state.

## RiskDecision Input Sources

Block 12 may consume documentary inputs from:

- Intake status from Block 01 — Input Contract and Handoff Intake Layer;
- RiskHandoffPackage validation outcome from Block 02 — RiskHandoffPackage Validator;
- Motor B evidence gate outcome from Block 03 — Motor B Evidence and Eligibility Gate;
- Risk policy registry status from Block 04 — Risk Policy Registry;
- hard veto / Kill Switch outcome from Block 05 — Hard Veto Rules and Kill Switch Triggers;
- missing evidence assessment from Block 06 — Missing Evidence and Blocking Gap Assessment;
- confidence/evidence sufficiency gate outcome from Block 07 — Confidence and Evidence Sufficiency Gate;
- event/regime/market risk gate outcome from Block 08 — Event, Regime and Market Risk Gate;
- exposure/position/capital constraint record from Block 09 — Exposure, Position and Capital Constraint Framework;
- strategy promotion/downgrade outcome from Block 10 — Strategy Promotion and Downgrade Rules;
- Paper Trading eligibility outcome from Block 11 — Paper Trading Eligibility Gate.

These inputs are documentary gate outcomes, not operational commands.

## RiskDecision Output Record

Stage 08 may document a RiskDecision with fields such as:

- `risk_decision_id`;
- `risk_decision_version`;
- `assessed_at`;
- `source_artifact_id`;
- `source_stage`;
- `source_block`;
- `source_document_ref`;
- `risk_handoff_package_ref`;
- `intake_status`;
- `validation_status`;
- `evidence_completeness_level`;
- `simulation_status`;
- `oos_validation_status`;
- `walk_forward_status`;
- `robustness_status`;
- `missing_evidence_status`;
- `blocking_gap_status`;
- `confidence_status`;
- `confidence_score`;
- `final_signal_confidence_score`;
- `event_risk_status`;
- `regime_risk_status`;
- `market_risk_status`;
- `risk_policy_status`;
- `hard_veto_status`;
- `kill_switch_review_status`;
- `exposure_constraint_status`;
- `capital_allocation_eligibility`;
- `productive_position_sizing_eligibility`;
- `risk_budget_activation`;
- `promotion_status`;
- `promotion_eligibility`;
- `paper_trading_eligibility`;
- `live_trading_status`;
- `execution_eligibility`;
- `order_generation_eligibility`;
- `exchange_connection_eligibility`;
- `downstream_operational_eligibility`;
- `handoff_to_09`;
- `risk_decision_status`;
- `risk_decision_reason`;
- `risk_decision_precedence_applied`;
- `required_future_evidence`;
- `required_review`;
- `human_review_required`;
- `risk_engine_review_required`;
- `audit_trace_ref`;
- `final_note_non_operational`.

This block does not create a database, storage layer, executable RiskDecision engine, productive schema, or runtime service. The record is documentary only.

## Framework-Only Decision Rule

Under `framework_only`, RiskDecision must preserve blocking:

- if `evidence_completeness_level = framework_only`, then `downstream_operational_eligibility = blocked`;
- if `simulation_status = backtest_not_implemented`, then Paper Trading remains blocked;
- if `oos_validation_status = oos_not_available`, then Paper Trading remains blocked;
- if `walk_forward_status = walk_forward_not_available`, then Paper Trading remains blocked;
- if `robustness_status = robustness_not_available`, then Paper Trading remains blocked;
- if `confidence_status = confidence_not_available`, then confidence remains unavailable;
- if `paper_trading_eligibility = blocked`, then `handoff_to_09 = blocked`;
- if `promotion_status = not_promoted`, then strategy cannot advance to Paper Trading.

`framework_only` can never produce approval.

## Missing Evidence Decision Rule

Missing backtesting, missing OOS validation, missing walk-forward validation, missing robustness, and missing empirical historical results produce `blocked_missing_evidence`.

Under the current Sultan state, this is not merely `requires_more_evidence` because the required evidence does not exist yet as auditable empirical evidence.

Missing evidence must remain explicit in the RiskDecision record and must preserve downstream blocking until future evidence exists, is versioned, is auditable, and passes later governance.

## Requires More Evidence Non-Approval Rule

`requires_more_evidence` is not approval.

`requires_more_evidence` is not conditional approval.

`requires_more_evidence` is not provisional approval.

`requires_more_evidence` is not Paper Trading readiness.

`requires_more_evidence` is not `handoff_to_09`.

`requires_more_evidence` cannot activate execution.

`requires_more_evidence` cannot activate capital allocation.

`requires_more_evidence` cannot promote a strategy.

`requires_more_evidence` cannot create confidence.

`requires_more_evidence` only records that additional evidence is needed for a future review.

## Human Review Non-Override Rule

Human review can require review, block, reject, suspend, escalate, request evidence, or preserve blocking.

Human review cannot approve Paper Trading, Live Trading, execution, capital allocation, or promotion under `framework_only` without future empirical evidence and governance.

This block prohibits:

- human-review-only approval;
- human override of `framework_only`;
- manual approval without audit trace;
- manual approval without empirical evidence;
- manual approval without Risk Engine review.

Human review metadata may become an input to later governance, but it cannot replace missing empirical evidence or RiskDecision precedence.

## Confidence Preservation Rule

RiskDecision cannot create confidence.

Under the current state, RiskDecision must preserve:

```text
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

RiskDecision prohibits confidence from:

- LLM agreement;
- LLM textual confidence;
- Bull/Bear agreement;
- Stage 07 fusion;
- Motor A context;
- Motor C context;
- favorable events;
- stable regimes;
- normal market context;
- human optimism;
- documentation completeness;
- synthetic tests;
- mock scenarios.

No confidence field may be upgraded unless future empirical evidence and formal governance define an auditable path.

## Downstream Blocking Rule

Under the current state, RiskDecision must preserve:

```text
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
```

No downstream route can be opened by favorable events, stable regimes, normal market context, StrategyDossier completeness, Stage 07 fusion, human optimism, review metadata, documentation completeness, or the absence of a hard veto.

## Current RiskDecision Conclusion

Under the current state:

```text
risk_decision_engine_status = non_operational_documentary
risk_decision_status = blocked_framework_only
secondary_risk_decision_status = blocked_missing_evidence
evidence_completeness_level = framework_only
simulation_status = backtest_not_implemented
oos_validation_status = oos_not_available
walk_forward_status = walk_forward_not_available
robustness_status = robustness_not_available
paper_trading_eligibility = blocked
paper_trading_ready = false
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
final_note = RiskDecision is non-operational and does not approve trading, Paper Trading, execution, capital allocation, promotion or confidence.
```

There is no Paper Trading eligibility, Live Trading eligibility, execution eligibility, order generation eligibility, exchange connection eligibility, capital allocation eligibility, productive position sizing eligibility, risk budget activation, strategy promotion, confidence assignment, downstream operational eligibility, or `handoff_to_09` under `framework_only`.

## Relationship With Blocks 01–11

Block 12 consumes, without reopening or softening, the outcomes of:

- Block 01 — Input Contract and Handoff Intake Layer: provides intake status and preserves upstream non-operational restrictions.
- Block 02 — RiskHandoffPackage Validator: provides structural validation, rejection, degradation, or review outcomes without approving operational usage.
- Block 03 — Motor B Evidence and Eligibility Gate: establishes Motor B `framework_only` and downstream blocking.
- Block 04 — Risk Policy Registry: provides documentary risk policy categories without activating policy enforcement.
- Block 05 — Hard Veto Rules and Kill Switch Triggers: provides hard veto and Kill Switch review classifications.
- Block 06 — Missing Evidence and Blocking Gap Assessment: provides missing evidence and blocking gap classifications.
- Block 07 — Confidence and Evidence Sufficiency Gate: preserves `confidence_not_available`, null confidence scores, and evidence insufficiency.
- Block 08 — Event, Regime and Market Risk Gate: provides event, regime, and market risk outcomes that can harden, block, or escalate but cannot approve.
- Block 09 — Exposure, Position and Capital Constraint Framework: provides documentary constraint records while capital allocation, position sizing, and risk budgets remain blocked.
- Block 10 — Strategy Promotion and Downgrade Rules: provides promotion blocking, downgrade, suspension, or review outcomes while promotion remains unavailable.
- Block 11 — Paper Trading Eligibility Gate: provides Paper Trading blocked or future-evidence-required outcomes while Paper Trading remains not eligible.

Block 12 consolidates and decides risk state, but does not execute.

## Relationship With Block 13

Block 13 will define Human Review, Override and Escalation Policy.

Block 12 may mark `requires_human_review`, but it does not define the complete override policy.

Any human review routing produced here remains non-operational under `framework_only` and cannot approve Paper Trading, Live Trading, execution, capital allocation, promotion, confidence assignment, or `handoff_to_09`.

## Relationship With Block 14

Block 14 will define Audit, Traceability and Risk Decision Replay.

Block 12 prepares auditable fields such as decision id, source references, precedence applied, required future evidence, required review, and audit trace references. It does not build full replay, storage, executable audit infrastructure, or production traceability services.

## Relationship With Block 17

Block 17 will close Stage 08 and formalize handoff to Stage 09 Paper Trading.

Block 12 cannot unblock `handoff_to_09` under the current `framework_only` state.

Any future handoff would require empirical evidence, no blocking gaps, Paper Trading eligibility review, auditability, governance, and later Stage 08 closure. This block does not create that handoff.

## Explicit Non-Goals

This block does not do:

- execute trades;
- generate orders;
- connect to exchanges;
- route orders;
- allocate capital;
- calculate productive position sizing;
- activate risk budgets;
- approve Paper Trading;
- activate Paper Trading;
- create Paper Trading runtime;
- create Paper Trading simulator;
- approve Live Trading;
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
- create human override policy;
- create audit replay;
- close Stage 08;
- hand off to Stage 09.

Block 12 is a non-operational documentary RiskDecision contract. It consolidates risk state and preserves blocking; it does not create any trading, Paper Trading, execution, capital, promotion, confidence, or handoff capability.
