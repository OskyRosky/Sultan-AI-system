# 06 Strategy Composition Layer

## Purpose

The Strategy Composition Layer composes one or more valid `RuleDefinition` records into a conceptual and auditable `StrategyCandidate`.

A strategy candidate in this block is a structured composition artifact. It is not a validated strategy, not a profitable strategy, not a trading recommendation, and not ready for operation.

## Required Origin

Every `StrategyCandidate` must originate from one or more valid rule definitions from Block 05.

For V1 composition, all rules inside the same candidate must share:

- the same source hypothesis;
- the same `SignalDefinition`;
- the same `RegimeContextFrame`.

The required flow is:

```text
Eligible Hypothesis Decision -> Valid Signal Definition -> Valid Regime Context Frame -> Valid Rule Definition -> Strategy Candidate Composition
```

## Composition Inputs

Composition may reference:

- valid rule definitions;
- their underlying signal definitions;
- their underlying regime context frames;
- shared hypothesis lineage;
- assumptions;
- limitations;
- conflict notes;
- falsification references;
- audit references.

## Pending Future Blocks

The output of Block 06 is explicitly pending:

- Risk Template assignment in Block 07.
- Candidate Registry in Block 08.
- Quality Gates in Block 09.
- Closure in Block 10.
- Dossier Handoff in Block 11.

## Explicit Non-Scope

Strategy composition does not:

- assign risk templates;
- register candidates in a registry;
- run quality gates;
- perform backtesting;
- validate profitability;
- calculate PnL;
- calculate drawdown, hit rate, Sharpe, Sortino, Calmar, or returns;
- perform live simulation;
- define position sizing;
- define capital allocation;
- define stop loss, take profit, or leverage;
- execute orders.

## Output

The output is a structured `StrategyCandidate` ready for future risk-template assignment, not a validated trading strategy.

## Non-Edge Statement

A valid strategy candidate composition does not imply edge, profitability, robustness, tradability, backtest readiness, deployment readiness, or execution permission.
