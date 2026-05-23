# 03 Signal Definition Layer

## Purpose

The Signal Definition Layer defines abstract, auditable signal definitions that can be traced to eligible inputs from Block 02.

A signal definition is a conceptual expression of an eligible hypothesis. It is not an order, not a rule, not a trade, not a strategy candidate, and not evidence of profitability.

## Required Origin

Every `SignalDefinition` must be anchored to at least one Block 02 eligibility decision where:

- `input_type = hypothesis`
- `eligible_for_strategy_design = True`

Eligible findings may be referenced only as supporting context. A finding cannot originate a signal by itself.

## Signal Meaning

A signal may define:

- conceptual orientation, such as `long_bias`, `short_bias`, `neutral`, or `avoid`;
- an observable conceptual condition;
- expected behavior inherited from the eligible hypothesis;
- assumptions;
- limitations;
- audit references.

## Explicit Non-Scope

The Signal Definition Layer does not create:

- BUY or SELL instructions.
- Orders.
- Trades.
- Entry rules.
- Exit rules.
- Invalidation rules.
- Filtering rules.
- Position sizes.
- Live alerts.
- Backtest-ready alpha code.
- Strategy candidates.
- PnL or performance metrics.

## Governance Requirement

Every signal must preserve:

- signal identifier;
- source hypothesis eligibility decision;
- optional supporting finding eligibility decisions;
- conceptual orientation;
- observable condition description;
- expected behavior;
- assumptions;
- limitations;
- falsification references;
- audit reference.

## Non-Edge Statement

A valid signal definition means only that an eligible hypothesis has been expressed as a conceptual signal candidate for later 05 design work. It does not imply edge, profitability, tradability, backtest readiness, deployment readiness, or execution permission.
