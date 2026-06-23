# 09 Paper Trading — Block 09.2: Motor D Portfolio Construction Contract

## Purpose

Block 09.2 defines the non-operational V1 contract for Motor D — Portfolio Construction inside `09 Paper Trading`.

This block documents Motor D's Blueprint role, V1 boundary, Stage 08 dependency, future V2 inputs and outputs, blocking rules, relationship to Motor E, and schema gaps.

Block 09.2 produces a contract only. It does not implement portfolio construction, sizing, rebalancing, allocation logic, correlation logic, candidate order generation, broker/exchange integration, CCXT integration, execution runtime, fills, slippage, fees, or any operational paper trading code.

## Blueprint Role Of Motor D

Motor D belongs to `09 Paper Trading`.

In the full V2 system, Motor D is responsible for:

- strategy-level sizing;
- asset-level diversification;
- correlation-aware exposure constraints;
- rebalance logic;
- portfolio construction;
- per-strategy limits;
- per-asset limits;
- candidate order preparation;
- downstream handoff to Motor E only after Risk Engine approval.

Motor D must remain downstream of `08 Risk Engine`. Candidate order preparation, when it exists in V2, must remain subject to Risk Engine approval and paper environment safety controls.

## V1 Non-Operational Boundary

Stage 09 V1 does not implement:

- real sizing;
- real portfolio optimization;
- real diversification calculations;
- real correlation estimation;
- real rebalance execution;
- candidate order creation;
- paper account allocation;
- capital allocation;
- exposure updates;
- PnL attribution;
- execution planning.

V1 Motor D is a future contract boundary only.

No V1 document may convert this contract into executable portfolio decisions, candidate orders, allocations, position sizes, exposure changes, capital deployment, paper account changes, or execution instructions.

## Required Upstream Dependency

Motor D may only operate downstream of `08 Risk Engine`.

In V1, Stage 08 remains blocked and non-operational for approval purposes. Therefore Motor D remains blocked and non-operational.

Motor D must not consume:

- raw Stage 06 diagnostics;
- raw Stage 06 backtesting artifacts;
- direct Stage 07 signals;
- Stage 07 `RiskHandoffPackage` directly;
- raw signal motor outputs;
- raw Motor A outputs;
- raw Motor B outputs;
- raw Motor C outputs;
- raw LLM outputs;
- manually selected strategies;
- manually promoted readiness claims;
- any bypass around Stage 08.

The valid future path is:

```text
Stage 08 approved, non-blocked Risk Engine output
-> Stage 09 input contract
-> Motor D portfolio construction
-> Motor E execution contract
```

This path does not exist operationally in V1.

## Current V1 Dependency State

The current Stage 08 decision object documented in Block 09.1 is:

```text
Stage08DryRunResult.risk_decision: Stage08RiskDecision
```

Current observed Stage 08 V1 values include:

```text
risk_decision_status = blocked
operational_status = non_operational
risk_approval = false
paper_trading_ready = false
handoff_to_09 = blocked
downstream_operational_eligibility = blocked
stage_09_operational_start_allowed = false
capital_allocation_ready = false
live_trading_ready = false
```

These values block Motor D.

They are expected and correct in V1.

## Conceptual V2 Inputs

Future V2 Motor D will eventually require inputs such as:

- risk-approved strategy candidates from Stage 08;
- strategy identifiers;
- approved risk budget;
- allowed assets/universe;
- account or paper capital;
- maximum exposure per strategy;
- maximum exposure per asset;
- correlation matrix or exposure clustering data;
- current simulated positions;
- pending orders;
- rebalance timestamp;
- paper environment identifier;
- kill-switch status;
- schema version and artifact references.

These are V2 requirements only.

They do not exist as a Motor D runtime input contract today unless a future block creates them explicitly.

No V1 document may imply that these inputs are currently available, approved, complete, or operational.

## Conceptual V2 Outputs

Future V2 Motor D may eventually produce:

- proposed portfolio allocation;
- target weights;
- target notional exposure;
- target quantity;
- rebalance plan;
- candidate order intents;
- blocked allocation reasons;
- risk budget usage;
- exposure summary;
- correlation constraint summary;
- downstream execution eligibility state.

In V1, all of these are documentary-only future concepts.

No V1 code produces them.

No V1 document may treat them as existing artifacts, paper trading instructions, or execution-ready outputs.

## V1 Required State Preservation

Motor D V1 must preserve:

```text
motor_d_operational = false
portfolio_construction_ready = false
sizing_ready = false
rebalance_ready = false
candidate_orders_ready = false
capital_allocation_ready = false
paper_trading_ready = false
stage_09_operational_start_allowed = false
risk_approval = false
handoff_to_09 = blocked
live_trading_ready = false
strategy_promotion_status = not_promoted
confidence_status = confidence_not_available
confidence_score = null
```

These states are blocking states.

They must not be reinterpreted as partial readiness.

They must not be upgraded by documentation, mock examples, manual claims, or future design notes.

## Motor D Blocking Rules

Motor D remains blocked if:

- Stage 08 does not produce an approved, non-blocked risk decision;
- `risk_approval = false`;
- `handoff_to_09 = blocked`;
- `capital_allocation_ready = false`;
- `paper_trading_ready = false`;
- kill-switch status is missing;
- paper environment identity is missing;
- strategy promotion status is not valid;
- confidence score is unavailable;
- confidence score is unsupported by real V2 evidence;
- schema traceability is missing;
- artifact traceability is missing.

For V1, these blocked states are expected and correct.

Motor D must not attempt to repair missing evidence, infer confidence, infer promotion, infer risk approval, infer capital readiness, or infer paper trading readiness.

## Explicit Non-Claims

Motor D V1 explicitly does not claim:

- Motor D has produced portfolio allocations;
- Motor D has produced position sizes;
- Motor D has produced candidate orders;
- capital has been allocated;
- a rebalance has been run;
- a paper portfolio exists;
- exposure limits have been operationally enforced;
- a correlation model has been run;
- readiness is claimed;
- paper trading has started;
- Motor E handoff is permitted.

No Motor D V1 artifact is empirical evidence.

No Motor D V1 artifact is a trading instruction.

No Motor D V1 artifact is portfolio approval.

## Relationship To Motor E

Motor D may only hand off to Motor E in V2 after:

- Stage 08 has produced valid approval;
- Stage 09 input contract has accepted the handoff;
- Motor D has valid V2 inputs;
- Motor D has produced risk-approved candidate order intents;
- paper environment safety controls are satisfied;
- kill-switch status allows continuation;
- all schema and audit references are traceable.

In V1, no handoff to Motor E is permitted except documentary-only design continuity.

Motor D V1 must not create candidate order intents for Motor E.

Motor E must not treat Motor D V1 documentation as execution authorization.

## V2 Schema Gaps

Known V2 schema gaps include:

- no machine-readable Motor D input artifact yet;
- no portfolio allocation schema yet;
- no candidate order intent schema yet;
- no risk budget schema from Stage 08 yet;
- no paper account state schema yet;
- no current position schema yet;
- no pending order schema yet;
- no correlation/exposure model artifact yet;
- no rebalance policy artifact yet;
- no paper environment identity artifact yet;
- no kill-switch status artifact for Stage 09 yet;
- no Motor D to Motor E handoff artifact yet.

Block 09.2 does not resolve these gaps.

Future V2 work must define them before Motor D can become operational.

## Exit Criteria For 09.2

Block 09.2 is complete only when:

- Motor D's Blueprint role is documented;
- V1 non-operational boundary is explicit;
- dependency on Stage 08 is explicit;
- direct Stage 06 bypass is prohibited;
- direct Stage 07 bypass is prohibited;
- raw motor bypass is prohibited;
- conceptual V2 inputs are documented as future-only;
- conceptual V2 outputs are documented as future-only;
- blocked state preservation is explicit;
- Motor E relationship is documented but not implemented;
- no operational code is introduced.

## Block 09.2 Closure Statement

Block 09.2 establishes Motor D as a future portfolio construction contract within `09 Paper Trading`.

In V1, Motor D is non-operational, blocked by Stage 08's current non-approval state, and unable to produce allocations, sizing, rebalances, candidate orders, or Motor E execution handoff.

Stage 09 remains non-operational and blocked.
