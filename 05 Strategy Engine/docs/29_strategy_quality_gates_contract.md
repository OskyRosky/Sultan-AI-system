# 29 Strategy Quality Gates Contract

## Purpose

This contract defines the Block 09 quality-gate assessment layer.

It evaluates structural governance quality for a valid `StrategyCandidateRegistryEntry`. It does not validate performance, approve trading, close a candidate, or hand off to 06 Backtesting Engine.

## Required Input

A quality-gate assessment must reference:

- one valid `StrategyCandidateRegistryEntry`;
- registry status `registered_pending_quality_gates`;
- complete registry traceability to source hypothesis, signal, regime frame, and rules.

## Quality Gate Result Fields

Each gate result must include:

- `gate_id`
- `gate_type`
- `passed`
- `assessment_summary`
- `limitations`
- `audit_reference`

## Required Gate Types

Every assessment must include exactly one result for each gate type:

- `traceability`
- `governance_fields`
- `structural_complexity`
- `evidence_governance_readiness`
- `risk_template_completeness`
- `falsification_readiness`
- `non_performance_scope`

## Assessment Fields

A quality-gate assessment must include:

- `assessment_id`
- `registry_entry`
- `gate_results`
- `assessment_status`
- `assumptions`
- `limitations`
- `non_approval_statement`
- `audit_reference`
- `assessed_at`

## Assessment Status

Assessment status is derived from gate results:

- all required gates pass: `passed_pending_strategy_closure`;
- any required gate fails: `failed_requires_revision`.

No manual override is allowed in Block 09.

## Falsification References

`StrategyQualityGateAssessment` is procedural. It verifies and preserves the upstream falsification references carried by the registry entry and its source artifacts.

The assessment itself does not need to create a new `falsification_references` field, because Block 09 evaluates governance readiness rather than proposing a new strategic hypothesis, signal, rule, candidate, or risk template.

## Explicit Prohibitions

Quality Gates must not define:

- strategy closure;
- dossier readiness;
- backtest authorization;
- edge confirmation;
- profitability validation;
- robustness validation;
- PnL;
- drawdown;
- hit rate;
- Sharpe, Sortino, Calmar, or return metrics;
- capital allocation;
- position sizing;
- stop loss;
- take profit;
- leverage;
- execution logic;
- trading approval.

## Relationship With Future Blocks

Block 10 may later use a passing quality-gate assessment as an input to Strategy Closure.

Block 11 may later use closed candidates for dossier handoff.

06 Backtesting Engine may later evaluate historical behavior only after proper handoff.

Block 09 does not perform those responsibilities.
