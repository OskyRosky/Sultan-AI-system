# 17 Signal Definition Contract

## Purpose

This contract defines the minimum structure and validation rules for abstract signal definitions in Block 03.

It depends on Block 02 Strategy Inputs Contract and must not bypass it.

## Signal Definition Fields

A signal definition must include:

- `signal_id`
- `source_hypothesis_decision`
- `supporting_finding_decisions`
- `orientation`
- `observable_condition`
- `expected_behavior`
- `assumptions`
- `limitations`
- `falsification_references`
- `audit_reference`
- `created_at`

## Orientation Model

Allowed orientations:

- `long_bias`
- `short_bias`
- `neutral`
- `avoid`

These orientations are conceptual labels only. They are not orders, trade directions, execution instructions, position instructions, or backtest signals.

## Origin Rules

1. A signal must originate from an eligible hypothesis decision.
2. The origin decision must have `input_type = hypothesis`.
3. The origin decision must have `eligible_for_strategy_design = True`.
4. A finding decision cannot originate a signal.
5. Eligible finding decisions may be attached only as supporting context.
6. Supporting finding decisions must have `input_type = finding` and `eligible_for_strategy_design = True`.
7. Evidence decisions cannot originate or support signal definitions directly.

## Required Governance Fields

Every valid signal definition must include:

- non-empty assumptions;
- non-empty limitations;
- non-empty falsification references;
- non-empty audit reference;
- non-empty observable condition;
- non-empty expected behavior.

## Explicit Prohibitions

The Signal Definition Layer must not define:

- entry rules;
- exit rules;
- invalidation rules;
- filtering logic;
- thresholds optimized against performance;
- orders;
- trades;
- position sizing;
- portfolio behavior;
- execution logic;
- PnL;
- Sharpe, Sortino, Calmar, or return metrics.

## Traceability

Future Block 04 and later blocks may reference signal definitions, but they must not reinterpret a signal as validated strategy logic.

Future Block 05 Rule Construction may use a signal as conceptual input, but rule construction is not part of Block 03.
