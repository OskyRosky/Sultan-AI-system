# 09 Paper Trading — Block 09.5: Promotion Criteria and V2 Roadmap

## Purpose

Block 09.5 documents the future V2 promotion criteria and roadmap for Paper Trading and eventual live-small eligibility.

This is a V1 documentary artifact only.

Block 09.5 does not evaluate promotion, satisfy promotion, run paper trading, calculate metrics, calculate PnL, calculate drawdown, calculate backtest/paper gap, allocate capital, or approve live-small.

## Blueprint Promotion Context

Stage 09 Paper Trading is part of the Blueprint path toward:

- paper trading validation;
- measurement of backtest/paper gap;
- paper trading evidence collection;
- eventual live-small eligibility only if strict criteria are satisfied.

Under V1, Stage 09 does not produce paper trading evidence.

Under V1, Stage 09 does not create live-small eligibility.

## Phase 4 Exit Criteria From Blueprint

Future V2 Phase 4 exit requirements include:

- minimum 4 weeks of documented paper trading;
- daily PnL traced;
- Risk Engine operational;
- backtest/paper gap less than 20%;
- kill-switch tested and functioning;
- minimum 20 trades executed.

None of these are satisfied in V1.

In V1:

- no paper trading campaign exists;
- no daily PnL exists;
- Risk Engine is not operationally approving Stage 09;
- no backtest/paper gap exists;
- no kill-switch test has passed;
- no paper trades exist.

## Paper To Live-Small Promotion Criteria

Future Paper -> Live-Small promotion requires all of the following simultaneously:

- 4 weeks with positive PnL;
- minimum 20 trades;
- MDD in paper less than 15%;
- backtest/paper gap less than 20%;
- kill-switch tested and functioning.

V1 does not satisfy any promotion condition.

No single condition is sufficient.

No partial evidence may be treated as promotion readiness.

## V1 Non-Operational Boundary

Stage 09 V1 does not implement:

- paper trading campaign;
- paper runtime;
- trade execution;
- simulated trades;
- real trades;
- daily PnL calculation;
- MDD calculation;
- backtest/paper gap calculation;
- kill-switch test execution;
- 20-trade evidence;
- 4-week evidence;
- live-small evaluation;
- promotion engine;
- readiness scoring;
- capital allocation;
- operational approval.

V1 Block 09.5 is a future promotion criteria and roadmap contract only.

No V1 document may convert this criteria catalog into a promotion evaluation, live-small review, paper readiness claim, capital allocation approval, or operational approval.

## Required Future V2 Evidence

Future V2 must collect evidence before any promotion decision, including:

- paper session start/end dates;
- trade ledger;
- order ledger;
- fill ledger;
- daily PnL records;
- cumulative PnL;
- drawdown series;
- maximum drawdown;
- backtest reference period;
- paper reference period;
- backtest/paper comparison methodology;
- slippage and fee records;
- kill-switch test record;
- Risk Engine approval record;
- paper/live separation validation record;
- audit trail references;
- schema version and artifact paths.

These are V2 requirements only.

They are not present as satisfied Stage 09 V1 evidence.

No V1 document may imply that these evidence artifacts exist, are complete, or are valid for promotion.

## Promotion Evaluation Rules

Future V2 promotion evaluation must obey these conceptual rules:

- no single criterion is sufficient;
- all criteria must pass simultaneously;
- missing evidence means blocked;
- unverified evidence means blocked;
- manual override is prohibited;
- positive PnL without 20 trades is insufficient;
- 20 trades without 4 weeks is insufficient;
- positive PnL with MDD >= 15% is insufficient;
- positive PnL with backtest/paper gap >= 20% is insufficient;
- kill-switch not tested means blocked;
- non-operational Risk Engine means blocked;
- any live credential ambiguity means blocked;
- any paper/live separation failure means blocked.

Block 09.5 does not implement evaluator code.

Block 09.5 does not produce evaluation output.

## V1 Required State Preservation

Block 09.5 V1 must preserve:

```text
promotion_evaluation_ready = false
paper_to_live_small_ready = false
live_small_candidate = false
live_trading_ready = false
paper_trading_ready = false
stage_09_operational_start_allowed = false
risk_engine_operational = false
risk_approval = false
capital_allocation_ready = false
paper_runtime_ready = false
paper_account_initialized = false
notional_capital_configured = false
notional_capital_usd = null
kill_switch_ready = false
kill_switch_tested = false
daily_pnl_available = false
paper_trade_count = 0
paper_trading_duration_weeks = 0
positive_pnl_4_weeks = false
mdd_available = false
mdd_threshold_passed = false
backtest_paper_gap_available = false
backtest_paper_gap_threshold_passed = false
handoff_to_09 = blocked
handoff_to_10 = blocked
strategy_promotion_status = not_promoted
confidence_status = confidence_not_available
confidence_score = null
```

These states are blocking states.

They must not be reinterpreted as partial readiness.

They must not be upgraded by documentation, mock examples, manual claims, future design notes, or planned roadmap items.

## Explicit Non-Claims

Block 09.5 V1 explicitly does not claim:

- a paper campaign has started;
- paper trades exist;
- the 20-trade minimum has been met;
- a 4-week paper trading period exists;
- daily PnL exists;
- positive 4-week PnL exists;
- MDD has been calculated;
- MDD threshold has passed;
- backtest/paper gap has been calculated;
- backtest/paper gap threshold has passed;
- kill-switch has been tested;
- Risk Engine operational approval exists;
- promotion evaluation has been run;
- a live-small candidate exists;
- live-small approval exists;
- capital allocation is allowed.

No Block 09.5 V1 artifact is empirical evidence.

No Block 09.5 V1 artifact is a promotion evaluation.

No Block 09.5 V1 artifact is live-small authorization.

## Relationship To Prior Stage 09 Blocks

Block 09.1 defines the input/risk handoff boundary.

Block 09.2 defines the future Motor D portfolio construction contract.

Block 09.3 defines the future Motor E execution contract.

Block 09.4 defines the future Paper Environment and Safety Controls.

Block 09.5 only documents future promotion criteria and V2 roadmap.

Block 09.5 must not override or relax any prior block.

Block 09.5 must not reinterpret a blocked Stage 08 decision, absent Motor D output, absent Motor E runtime, or absent Paper Environment as readiness.

## Relationship To 09.6 And 09.7

Block 09.6 will define Stage 09 V1 Quality Gates.

Block 09.7 will define Stage 09 V1 Closure + Handoff to Stage 10.

Block 09.5 does not close the stage by itself.

Block 09.5 does not authorize handoff to Stage 10 except as future documentary context.

Final closure remains reserved for Block 09.7.

## V2 Roadmap

A conservative V2 roadmap may include:

- persisted Stage 08 risk decision / handoff artifact;
- operational Risk Engine approval;
- Motor D operational portfolio construction;
- Motor E operational execution contract;
- paper environment initialization;
- paper-only/sandbox credentials;
- kill-switch implementation and test;
- paper account state;
- paper trade ledger;
- order/fill/reconciliation ledger;
- daily PnL pipeline;
- drawdown calculation;
- backtest/paper gap methodology;
- 4-week paper campaign;
- 20-trade minimum;
- promotion evaluation report;
- live-small readiness review.

These roadmap items are future-only.

None of these roadmap items are implemented in V1.

## V2 Schema Gaps

Known V2 schema gaps include:

- no promotion evidence schema;
- no paper trade ledger schema;
- no daily PnL schema;
- no drawdown schema;
- no backtest/paper comparison schema;
- no kill-switch test evidence schema;
- no Risk Engine operational approval artifact;
- no promotion evaluation report schema;
- no live-small readiness review artifact;
- no handoff-to-10 readiness artifact.

Block 09.5 does not resolve these gaps.

Future V2 work must define them before promotion evaluation or live-small readiness review can occur.

## Exit Criteria For 09.5

Block 09.5 is complete only when:

- Blueprint Phase 4 exit criteria are documented;
- Paper -> Live-Small promotion criteria are documented;
- V1 non-operational boundary is explicit;
- all promotion criteria are explicitly marked unsatisfied in V1;
- required future V2 evidence is documented;
- V2 roadmap is documented as future-only;
- V2 schema gaps are documented honestly;
- all readiness/promotion/risk/capital/live states remain false/blocked/null;
- no operational code, evaluator code, metrics code, PnL code, MDD code, backtest/paper gap code, or runtime code has been introduced.

## Block 09.5 Closure Statement

Block 09.5 establishes the future promotion criteria and V2 roadmap within `09 Paper Trading`.

In V1, no criteria are satisfied, no promotion evaluation exists, no paper campaign exists, no PnL exists, no MDD exists, no backtest/paper gap exists, no kill-switch test exists, no live-small candidate exists, and no capital allocation is allowed.

Stage 09 remains non-operational and blocked.
