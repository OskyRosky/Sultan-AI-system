# 25 Risk Template Contract

## Purpose

This contract defines the minimum structure and validation rules for Risk Template assignment in Block 07.

It depends on Block 06 Strategy Composition and must not bypass it.

## Risk Template Fields

A risk template must include:

- `template_id`
- `strategy_candidate`
- `risk_dimensions`
- `constraint_intent`
- `exclusion_criteria`
- `assumptions`
- `limitations`
- `calibration_status`
- `non_calibrated_rationale`
- `audit_reference`
- `created_at`

## Risk Dimensions

Initial conceptual risk dimensions:

- `market_exposure`
- `liquidity`
- `volatility`
- `concentration`
- `regime_dependency`
- `model_risk`
- `execution_dependency`
- `operational`

These dimensions are governance labels only. They are not calibrated risk factors or executable controls.

## Calibration Status

Block 07 permits only:

- `uncalibrated`

Any calibrated, production, live, or deployment-ready status is out of scope.

## Origin Rules

1. A risk template must reference a valid `StrategyCandidate`.
2. The referenced candidate must have status `pending_risk_template`.
3. The referenced candidate must validate under Block 06, including V1 rule compatibility.
4. A risk template cannot originate directly from evidence, findings, hypotheses, signals, regime frames, or rules.
5. A risk template cannot register, quality-approve, close, or hand off a candidate.

## Required Governance Fields

Every valid risk template must include:

- at least one risk dimension;
- non-empty constraint intent;
- non-empty assumptions;
- non-empty limitations;
- non-empty non-calibrated rationale;
- non-empty audit reference.

## Explicit Prohibitions

The Risk Template Layer must not define:

- real risk parameters;
- capital allocation;
- position sizing;
- stop loss;
- take profit;
- leverage;
- drawdown limits;
- PnL limits;
- margin rules;
- portfolio optimization;
- live kill switches;
- backtests;
- Sharpe, Sortino, Calmar, drawdown, hit rate, or return metrics;
- candidate registry entries;
- quality gate results.

## Relationship With Future Blocks

Block 08 may later register candidates with risk templates.

Block 09 may later evaluate quality gates.

06 Backtesting Engine may later evaluate historical behavior.

Block 07 does not perform those responsibilities.
