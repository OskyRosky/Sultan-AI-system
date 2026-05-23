# 21 Rule Construction Contract

## Purpose

This contract defines the minimum structure and validation rules for Rule Construction in Block 05.

It depends on Block 03 Signal Definition Layer and Block 04 Regime Context Framing. It must not bypass either layer.

## Rule Definition Fields

A rule definition must include:

- `rule_id`
- `signal_definition`
- `regime_context_frame`
- `rule_category`
- `rule_statement`
- `interpretation_guidance`
- `assumptions`
- `limitations`
- `falsification_references`
- `audit_reference`
- `created_at`

## Supported Rule Categories

Initial conceptual rule categories:

- `entry_condition`
- `exit_condition`
- `invalidation_condition`
- `filter_condition`
- `conflict_resolution`

These are declarative categories only. They do not trigger trades or create executable strategy behavior.

## Origin Rules

1. A rule definition must reference a valid `SignalDefinition`.
2. A rule definition must reference a valid `RegimeContextFrame`.
3. The regime context frame must reference the same signal definition.
4. A rule definition cannot originate from evidence, findings, hypotheses, eligibility decisions, or regime context alone.
5. A rule definition cannot modify hypothesis eligibility, signal origin, or regime context.

## Required Governance Fields

Every valid rule definition must include:

- non-empty rule statement;
- non-empty interpretation guidance;
- non-empty assumptions;
- non-empty limitations;
- non-empty falsification references;
- non-empty audit reference.

## Explicit Prohibitions

The Rule Construction Layer must not define:

- executable orders;
- trade instructions;
- position sizing;
- stop loss;
- take profit;
- leverage;
- portfolio behavior;
- exchange connectivity;
- strategy candidates;
- backtests;
- PnL;
- drawdown;
- hit rate;
- Sharpe, Sortino, Calmar, or return metrics;
- parameter optimization.

## Relationship With Block 06

Block 06 Strategy Composition may later combine signals, regime frames, and rule definitions into strategy candidates. Block 05 does not perform that composition.
