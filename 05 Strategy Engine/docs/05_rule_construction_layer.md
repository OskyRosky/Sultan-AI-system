# 05 Rule Construction Layer

## Purpose

The Rule Construction Layer defines conceptual, declarative, and auditable rule definitions from valid regime-contextualized signals.

A rule in this block describes how a signal framed by a regime context may be interpreted by future strategy design. It is not an order, not execution logic, not a strategy candidate, not backtested behavior, and not evidence of profitability.

## Required Origin

Every `RuleDefinition` must originate from:

1. one valid `SignalDefinition` from Block 03;
2. one valid `RegimeContextFrame` from Block 04;
3. the regime context frame must reference the same signal definition.

The required flow is:

```text
Eligible Hypothesis Decision -> Valid Signal Definition -> Valid Regime Context Frame -> Rule Definition
```

## Rule Classes

Allowed conceptual rule categories:

- `entry_condition`
- `exit_condition`
- `invalidation_condition`
- `filter_condition`
- `conflict_resolution`

These categories are descriptive. They are not executable rules.

## Required Governance Fields

Every future rule definition must document:

- rule identifier;
- source signal definition;
- source regime context frame;
- rule category;
- rule statement;
- interpretation guidance;
- assumptions;
- limitations;
- falsification references;
- audit reference.

## Optimization Warning

Rule construction must not become disguised optimization. Rules should be justified by governed signal and regime context, not tuned to maximize historical performance inside 05.

## Explicit Non-Scope

This layer does not:

- Create strategy candidates.
- Run parameter searches.
- Tune thresholds against PnL.
- Calculate performance.
- Calculate hit rate, drawdown, Sharpe, Sortino, Calmar, or returns.
- Select rules based on historical profitability.
- Assign capital.
- Define position sizing.
- Define stop loss or take profit.
- Define leverage.
- Trigger trades.
- Execute orders.

## Non-Edge Statement

A valid rule definition means only that a signal and regime context have been expressed as a conceptual rule candidate for future composition. It does not imply edge, profitability, tradability, backtest readiness, deployment readiness, or execution permission.
