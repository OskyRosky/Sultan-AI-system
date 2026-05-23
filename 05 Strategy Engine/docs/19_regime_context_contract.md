# 19 Regime Context Contract

## Purpose

This contract defines the minimum structure and validation rules for Regime Context Framing in Block 04.

It depends on Block 03 Signal Definition Layer and must not bypass it.

## Regime Context Frame Fields

A regime context frame must include:

- `frame_id`
- `signal_definition`
- `regime_type`
- `regime_label`
- `context_description`
- `applicability_rationale`
- `assumptions`
- `limitations`
- `falsification_references`
- `audit_reference`
- `created_at`

## Supported Regime Types

Initial conceptual regime types:

- `trend`
- `volatility`
- `momentum`
- `range`
- `liquidity`
- `macro`
- `structural`

These are context descriptors only. They are not classifiers, switches, filters, rules, or trading states.

## Origin Rules

1. A regime context frame must originate from a valid `SignalDefinition`.
2. A regime context frame cannot originate from evidence.
3. A regime context frame cannot originate from findings.
4. A regime context frame cannot originate from hypotheses directly.
5. A regime context frame cannot modify signal origin, hypothesis eligibility, or Block 02 decisions.

## Required Governance Fields

Every valid regime context frame must include:

- non-empty context description;
- non-empty applicability rationale;
- non-empty assumptions;
- non-empty limitations;
- non-empty falsification references;
- non-empty audit reference.

## Explicit Prohibitions

The Regime Context Framing Layer must not define:

- regime labels calculated from real data;
- online or rolling regime detection;
- entry rules;
- exit rules;
- invalidation rules;
- filters;
- automatic regime switching;
- market timing;
- position sizing;
- portfolio behavior;
- execution logic;
- strategy candidates;
- PnL;
- Sharpe, Sortino, Calmar, or return metrics.

## Relationship With 04 Research Layer

04 Research Layer may produce regime analysis as conditional research evidence. Block 04 of 05 does not reuse that engine directly, does not read its data, and does not calculate regimes.

Any future real regime reference must arrive through governed artifacts and the contracts already defined by Blocks 02 and 03.
