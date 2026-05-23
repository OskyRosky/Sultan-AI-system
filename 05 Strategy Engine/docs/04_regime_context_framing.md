# 04 Regime Context Framing

## Purpose

Regime Context Framing defines market context assumptions that must be attached to a valid `SignalDefinition` before future rule construction.

This layer exists because a signal should not be interpreted as universal or context-free. It documents the regime context in which a conceptual signal is expected to be considered later.

## Placement

Regime context comes after Signal Definition and before Rule Construction and Strategy Composition.

The required flow is:

```text
Eligible Hypothesis Decision -> Valid Signal Definition -> Regime Context Frame -> Future Rule Construction
```

## Meaning Of Regime

A regime is a prior context descriptor used to frame future design. It may describe conditions such as trend, volatility, momentum, range, liquidity, macro, or structural market context.

In Block 04, regime context is declared and validated as metadata. It is not calculated from data.

## Required Origin

Every `RegimeContextFrame` must be anchored to one valid `SignalDefinition` from Block 03.

It must not originate directly from:

- research evidence;
- findings;
- hypotheses;
- eligibility decisions without a signal definition.

## Explicit Non-Scope

This layer does not implement:

- regime calculation from data;
- regime classification;
- automatic regime switching;
- automatic market timing;
- dynamic allocation;
- backtested regime filters;
- entry rules;
- exit rules;
- invalidation rules;
- strategy candidates;
- PnL or performance metrics.

## Governance Requirement

Every future regime frame must document:

- frame identifier;
- source signal definition;
- regime type;
- regime label;
- context description;
- applicability rationale;
- assumptions;
- limitations;
- falsification references;
- audit reference.

## Non-Edge Statement

A valid regime context frame does not imply edge, profitability, tradability, market-timing ability, backtest readiness, or execution permission.
