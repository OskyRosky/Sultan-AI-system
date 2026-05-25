# 31 Strategy Closure Contract

## Purpose

This contract defines the Block 10 Strategy Closure layer.

Strategy Closure creates an immutable internal record that a conceptual strategy package completed the 05 Strategy Engine governance chain through Quality Gates.

It does not create a dossier, execute handoff, authorize backtesting, validate performance, confirm edge, or approve trading.

## Required Input

A closure record must reference:

- one valid `StrategyQualityGateAssessment`;
- assessment status `passed_pending_strategy_closure`;
- complete upstream traceability through registry entry, candidate, risk template, rules, regime frame, signal, and source hypothesis.

## Closure Record Fields

A closure record must include:

- `closure_id`
- `quality_assessment`
- `closure_status`
- `candidate_id`
- `registry_entry_id`
- `quality_assessment_id`
- `source_hypothesis_ids`
- `signal_ids`
- `regime_frame_ids`
- `rule_ids`
- `upstream_falsification_references`
- `closure_summary`
- `assumptions`
- `limitations`
- `non_approval_statement`
- `audit_reference`
- `closed_at`

## Closure Status

Block 10 permits only:

- `closed_pending_dossier_handoff`

No backtest-ready, dossier-ready, deployment-ready, live, trading-approved, profitable, robust, or validated status is permitted.

## Falsification References

Strategy Closure preserves upstream falsification references from every upstream conceptual layer that carries explicit `falsification_references`:

- `SignalDefinition`;
- `RegimeContextFrame`;
- `RuleDefinition`;
- `StrategyCandidate`;
- `RiskTemplate`;
- `StrategyCandidateRegistryEntry`.

Closure does not create a new strategic claim and does not create new falsification criteria of its own.

## Explicit Prohibitions

Strategy Closure must not define:

- dossier content;
- handoff execution;
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

## Relationship With Block 11

Block 11 may later use a closed package to create a Strategy Dossier & Handoff artifact.

Block 10 does not perform that handoff and does not package a final dossier.
