# 07 Signal Fusion + LLM Motors - Stage Charter, Boundaries, and Non-Authority Rules

## 1. Purpose

`07 Signal Fusion + LLM Motors` is the governed bridge between `06 Backtesting Engine` and `08 Risk Engine`.

The purpose of this stage is to define an audit-first, risk-aware, deterministic-first layer that can consume evidence and context from parallel motors, normalize candidate inputs, and produce a traceable fused signal candidate for downstream review.

The output of 07 is a `fused signal candidate`.

The output of 07 is no trade approval.

The output of 07 is no paper trading approval, no live trading approval, no execution instruction, no capital allocation decision, and no Risk Engine override.

## 2. Position In The System

The official stage sequence around 07 is:

```text
04 Research Layer
-> 05 Strategy Engine
-> 06 Backtesting Engine
-> 07 Signal Fusion + LLM Motors
-> 08 Risk Engine
-> 09 Paper Trading
```

07 consumes upstream contracts and evidence states. It does not rewrite upstream records, invent missing evidence, upgrade research status, approve strategies, or declare historical validation.

The formal Motor B handoff consumed by 07 is:

```text
06 Backtesting Engine/docs/18_motor_b_output_contract.md
```

That contract belongs to `06 Backtesting Engine`. Stage 07 consumes it, validates it for downstream use, and preserves its restrictions. Stage 07 does not redefine the Motor B Output Contract.

## 3. What 07 Is

07 is:

- a signal candidate normalization stage;
- a deterministic-first fusion stage;
- a governed LLM-assisted classification and evidence-structuring stage;
- a traceability and replay metadata stage;
- a dry-run and contract-validation surface before Risk Engine review;
- a bridge from Motor A, Motor B, and Motor C into a fused signal candidate.

07 may classify, structure, compare, normalize, and debate candidate evidence under explicit rules.

07 must preserve upstream evidence state, missing evidence state, forbidden downstream usage, non-approval statements, and audit references.

## 4. What 07 Is Not

07 is not:

- a trading engine;
- a paper trading engine;
- a live trading engine;
- an execution engine;
- a broker integration layer;
- a capital allocation engine;
- a Risk Engine;
- a backtesting engine;
- an OOS validation engine;
- a walk-forward engine;
- a robustness engine;
- an ML ensemble;
- a strategy approval committee;
- a replacement for human review where human review is required.

07 must not create execution logic, position sizing, stop loss logic, take profit logic, leverage policy, portfolio allocation, exchange routing, or capital deployment logic.

## 5. Conceptual Inputs Allowed

07 may consume the following conceptual inputs when available and explicitly versioned:

- Motor A context outputs, including regime context derived from prior research where allowed;
- Motor B Output Contract from `06 Backtesting Engine`;
- Motor C event or LLM classifier outputs after their contracts exist;
- documented absence-of-evidence states;
- audit references;
- upstream limitations;
- forbidden downstream usage values;
- non-approval statements;
- dry-run fixtures for interface validation.

Current Motor B input state must be treated as:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

07 may use this state for design reference, documentation review, contract validation, dry-run simulation, offline research, and interface validation only.

## 6. Conceptual Outputs Allowed

07 may produce:

- normalized signal candidate records;
- fused signal candidate records;
- evidence availability summaries;
- motor contribution summaries;
- deterministic fusion decisions for dry-run or review;
- disagreement records;
- Bull/Bear debate records when the later block exists;
- confidence status records that preserve upstream confidence limitations;
- downstream eligibility metadata for `08 Risk Engine`;
- audit and replay metadata.

Any `fused signal candidate` produced by 07 must carry explicit downstream restrictions and must preserve upstream `forbidden_downstream_usage`.

No 07 output may be interpreted as:

- trade approval;
- paper trading approval;
- live trading approval;
- capital allocation approval;
- order authorization;
- Risk Engine approval;
- confirmed edge;
- historical validation;
- production readiness.

## 7. Non-Authority Rules

07 has no authority to:

- approve trades;
- authorize paper trading;
- authorize live trading;
- allocate capital;
- bypass `08 Risk Engine`;
- relax risk limits;
- override `paper_trading_eligibility = blocked`;
- create or modify upstream evidence;
- convert mockups into real evidence;
- convert documentation into empirical validation;
- create missing backtest results;
- create missing OOS validation;
- create missing walk-forward results;
- create missing robustness results;
- invent `confidence_score`;
- upgrade `confidence_status = confidence_not_available`;
- remove upstream forbidden usage restrictions.

If upstream evidence is missing, 07 must preserve the absence explicitly.

If upstream Motor B is `framework_only`, 07 must not produce an operational signal or any paper trading eligible artifact.

## 8. LLM Authority Boundaries

LLMs in 07 may:

- classify text and event context under a documented contract;
- summarize upstream evidence and limitations;
- structure unstructured inputs into reviewable fields;
- generate Bull/Bear arguments for later governed debate;
- identify missing evidence;
- propose review questions;
- assist with audit explanations.

LLMs in 07 must not:

- execute trades;
- approve trades;
- approve paper trading;
- approve live trading;
- allocate capital;
- alter Risk Engine decisions;
- invent backtest evidence;
- invent OOS evidence;
- invent robustness evidence;
- invent confidence;
- promote strategies;
- treat generated text as empirical evidence;
- hide uncertainty or missing evidence.

LLMs do not approve trades.

Any LLM-generated classification must be traceable to source input, prompt or instruction version where applicable, model identifier where applicable, timestamp, limitations, and replay metadata.

## 9. Motor A / Motor B / Motor C Parallel Input Principle

Motor A, Motor B, and Motor C are parallel conceptual inputs into Signal Candidate Normalization and Signal Fusion.

They are not hierarchical dependencies.

They must remain separately traceable:

- Motor A: market/regime/context layer;
- Motor B: research/strategy/backtesting evidence state through the Motor B Output Contract;
- Motor C: event/LLM classifier layer.

Motor A and Motor C are independent from each other.

Motor A may be constructed earlier for pragmatic reasons because `04 Research Layer` already contains Regime Detection v1 / regime analysis as partial input. That sequencing does not create a technical dependency between Motor A and Motor C.

Motor B is consumed through the Motor B Output Contract owned by 06. Stage 07 must not redefine Motor B evidence semantics.

## 10. Current Motor B Evidence State

The current Motor B evidence state entering 07 is:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

This means:

- 04 has framework tools, but no real persisted research output;
- 05 has conceptual strategy framework and mockups, but no real approved strategy derived from real research;
- 06 has documentation and contracts, but no Python backtesting engine, simulation, OOS validation, walk-forward execution, robustness result, or historical performance evidence.

07 must preserve this state until a later Motor B Output Contract instance provides real evidence under governed validation.

## 11. Relationship With 08 Risk Engine

`08 Risk Engine` has final authority over veto, risk review, promotion eligibility, risk limits, and downstream eligibility.

07 must hand off fused signal candidates to 08 with:

- evidence completeness level;
- confidence status;
- confidence score or explicit null;
- paper trading eligibility status;
- forbidden downstream usage;
- missing evidence;
- blocking gaps;
- non-approval statements;
- audit references;
- replay metadata.

08 may veto any 07 output.

08 must be able to block any output with incomplete evidence, `framework_only` evidence, missing OOS validation, missing robustness review, missing temporal admissibility, explicit forbidden downstream usage, or unresolved blocking gaps.

Paper Trading remains blocked unless a later 08 Risk Engine process explicitly permits downstream eligibility after sufficient evidence and review.

## 12. Explicit Prohibited Actions

07 must not:

- implement trading logic;
- implement Paper Trading;
- implement Live Trading;
- implement execution logic;
- create capital allocation;
- create broker routing;
- create production signal routing;
- create Risk Engine logic;
- redefine the Motor B Output Contract;
- invent backtesting results;
- invent OOS validation;
- invent walk-forward results;
- invent robustness results;
- invent historical performance;
- invent `confidence_score`;
- convert mocks or examples into evidence;
- create an ML ensemble;
- build Motor A in this block;
- build Motor B Adapter in this block;
- build Motor C in this block;
- build Bull/Bear Debate in this block;
- build Signal Fusion Engine in this block;
- start Block 01 work inside Block 00.

## 13. Audit-First Requirements

Every future 07 artifact must preserve:

- source contract references;
- source stage references;
- schema versions;
- evidence completeness level;
- missing evidence status;
- confidence status;
- forbidden downstream usage;
- non-approval statements;
- deterministic rule versions where applicable;
- LLM prompt and model metadata where applicable;
- timestamps;
- replay metadata;
- human review status where applicable.

07 must make it possible to replay why a fused signal candidate exists and why it was or was not eligible for downstream review.

## 14. Deterministic-First Requirement

When evidence is incomplete, unavailable, or `framework_only`, 07 must prefer deterministic rules over probabilistic or generative behavior.

The first version of 07 must be deterministic-first:

- no hidden model weighting;
- no inferred confidence;
- no ML ensemble;
- no opaque promotion;
- no stochastic decision as authority;
- no LLM-generated approval.

LLM outputs may assist classification or explanation, but deterministic governance decides allowed downstream usage.

## 15. Evidence Preservation Rules

07 must preserve upstream evidence restrictions exactly.

If an upstream contract includes `forbidden_downstream_usage`, 07 must carry it forward unless a later owner stage formally supersedes it with stronger evidence and audit references.

07 must not weaken:

- `paper_trading_eligibility = blocked`;
- `confidence_status = confidence_not_available`;
- `confidence_score = null`;
- `approval_status = not_approved`;
- `evidence_completeness_level = framework_only`;
- missing evidence declarations;
- blocking gaps;
- non-approval statements.

Any absence of evidence must remain explicit. A null value without an explicit status is not acceptable for downstream use.

## 16. Block 00 Closure Criteria

Block 00 is closed when this document establishes:

- the purpose of 07;
- what 07 is and is not;
- allowed conceptual inputs;
- allowed conceptual outputs;
- non-authority rules;
- LLM authority boundaries;
- Motor A / Motor B / Motor C parallel input principle;
- current Motor B evidence state;
- Paper Trading blocked statement;
- relationship with `08 Risk Engine`;
- explicit prohibited actions;
- audit-first requirements;
- deterministic-first requirements;
- evidence preservation rules.

Closing Block 00 does not create Block 01, Motor A, Motor B Adapter, Motor C, Bull/Bear Debate, Signal Fusion Engine, Risk Engine integration, Paper Trading, Live Trading, or any executable trading behavior.
