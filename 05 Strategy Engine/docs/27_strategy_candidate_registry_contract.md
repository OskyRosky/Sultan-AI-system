# 27 Strategy Candidate Registry Contract

## Purpose

This contract defines the minimum structure and validation rules for Strategy Candidate Registry in Block 08.

It depends on Block 06 Strategy Composition and Block 07 Risk Template Layer. It must not bypass either layer.

## Registry Entry Fields

A registry entry must include:

- `entry_id`
- `strategy_candidate`
- `risk_template`
- `registry_status`
- `source_hypothesis_ids`
- `signal_ids`
- `regime_frame_ids`
- `rule_ids`
- `assumptions`
- `limitations`
- `falsification_references`
- `audit_reference`
- `registered_at`

## Registry Status

Block 08 permits only:

- `registered_pending_quality_gates`

Any quality-approved, closed, dossier-ready, backtest-ready, deployable, live, or trading-approved status is out of scope.

## Origin Rules

1. A registry entry must reference a valid `StrategyCandidate`.
2. A registry entry must reference a valid `RiskTemplate`.
3. The risk template must reference the same strategy candidate.
4. The strategy candidate must validate under Block 06, including V1 rule compatibility.
5. The risk template must validate under Block 07 and remain uncalibrated.
6. A registry entry cannot originate directly from evidence, findings, hypotheses, signals, regime frames, rules, or risk dimensions alone.

## Immutability

Registry entries are immutable audit records. A registry collection must be extended by returning a new collection, not by mutating an existing entry.

## Required Governance Fields

Every valid registry entry must include:

- non-empty audit reference;
- non-empty assumptions;
- non-empty limitations;
- non-empty falsification references;
- traceability identifiers for source hypotheses, signals, regime frames, and rules.

## Explicit Prohibitions

The Strategy Candidate Registry must not define:

- quality gate results;
- closure status;
- dossier readiness;
- backtest authorization;
- PnL;
- drawdown;
- hit rate;
- Sharpe, Sortino, Calmar, or return metrics;
- risk calibration;
- position sizing;
- capital allocation;
- stop loss;
- take profit;
- leverage;
- execution logic;
- trading approval.

## Relationship With Future Blocks

Block 09 may later evaluate quality gates for registered candidates.

Block 10 may later close candidates internally.

Block 11 may later prepare dossier handoff.

06 Backtesting Engine may later evaluate historical behavior after proper handoff.

Block 08 does not perform any of those responsibilities.
