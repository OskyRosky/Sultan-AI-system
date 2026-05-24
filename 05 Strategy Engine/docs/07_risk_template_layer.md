# 07 Risk Template Layer

## Purpose

The Risk Template Layer assigns conceptual, auditable, and explicitly uncalibrated risk templates to valid `StrategyCandidate` objects from Block 06.

A risk template defines which dimensions of risk must be considered before a candidate can proceed to future registry, quality gates, and backtesting. It does not quantify or control real risk.

## Required Origin

Every `RiskTemplate` must be assigned to one valid `StrategyCandidate` whose status is:

```text
pending_risk_template
```

The required flow is:

```text
Eligible Hypothesis Decision -> Valid Signal Definition -> Valid Regime Context Frame -> Valid Rule Definition -> Valid Strategy Candidate V1 -> Risk Template Assignment
```

## Risk As Constraint

Risk templates describe intended governance dimensions, exclusions, assumptions, and design boundaries. They exist to prevent unconstrained strategy candidates from advancing without declared risk considerations.

## Calibration Boundary

Risk templates in Block 07 are always uncalibrated. They must not contain real thresholds, capital allocation, position sizing, stop loss, take profit, leverage, or live risk controls.

## Explicit Non-Scope

This layer is not a real Risk Engine. It does not implement:

- calibrated risk models;
- dynamic position sizing;
- capital allocation;
- stop loss rules;
- take profit rules;
- leverage configuration;
- portfolio optimization;
- real-time exposure control;
- drawdown-based trading decisions;
- margin management;
- live kill switches;
- historical risk evaluation;
- backtesting.

## Future Requirement

Every strategy candidate must eventually receive a risk template before it can enter downstream registry and quality review. Block 07 creates the template assignment only; it does not register or approve the candidate.

## Non-Edge Statement

A valid risk template does not imply safety, robustness, profitability, edge, backtest readiness, registry approval, quality approval, or trading authorization.
