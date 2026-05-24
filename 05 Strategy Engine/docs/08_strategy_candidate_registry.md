# 08 Strategy Candidate Registry

## Purpose

The Strategy Candidate Registry is the governed inventory of conceptual strategy candidates created by 05 Strategy Engine.

Registry entries are immutable audit records. They state that a candidate and its uncalibrated risk template have been received with sufficient traceability for future quality-gate review.

## Required Origin

Every registry entry must originate from:

1. one valid `StrategyCandidate` from Block 06;
2. one valid uncalibrated `RiskTemplate` from Block 07;
3. the risk template must reference the same strategy candidate.

The required flow is:

```text
Eligible Hypothesis Decision -> SignalDefinition -> RegimeContextFrame -> RuleDefinition -> StrategyCandidate -> RiskTemplate -> Registry Entry
```

## Registry Status

Block 08 may create only:

- `registered_pending_quality_gates`

This status means the candidate is registered as a conceptual artifact and awaits Block 09. It does not mean quality approval, closure, dossier readiness, backtest authorization, deployment approval, or trading authorization.

## Required Fields

Registry entries include:

- registry entry identifier;
- strategy candidate;
- risk template;
- registry status;
- source hypothesis identifiers;
- signal identifiers;
- regime frame identifiers;
- rule identifiers;
- assumptions;
- limitations;
- falsification references;
- audit reference;
- registration timestamp.

## Falsification Criteria

Falsification references remain mandatory. A candidate must preserve what evidence would weaken, reject, or retire the conceptual idea before downstream validation work begins.

## Explicit Non-Scope

The registry does not:

- validate profitability;
- approve deployment;
- authorize trading;
- run quality gates;
- close candidates;
- prepare dossier handoff;
- authorize backtesting;
- calculate PnL or performance metrics;
- assign risk parameters;
- execute orders.
