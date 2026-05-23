# 01 Strategy Architecture

## Formal Definition

Strategy Engine is the governed design layer that converts approved research context into auditable strategy candidates. It defines how strategic ideas are described, constrained, composed, challenged, closed, and handed off.

Strategy Engine is not a research discovery engine, not a backtesting engine, not a risk engine, and not an execution system.

## Strategy Candidate vs Strategy Validated

A strategy candidate is a structured proposal with traceable inputs, explicit assumptions, rule framing, risk constraints, falsification criteria, and quality gate status.

A validated strategy is outside the authority of 05 Strategy Engine. Validation belongs to downstream stages, starting with 06 Backtesting Engine and later risk, paper trading, and live governance layers.

## Research vs Strategy vs Backtesting

Research defines whether there is governed evidence worth translating.

Strategy defines what a candidate would be, how it should be constrained, and what must be tested later.

Backtesting evaluates candidate behavior under historical simulation and market assumptions.

## Architecture Of 11 Blocks

1. Strategy Architecture.
2. Strategy Inputs Contract.
3. Signal Definition Layer.
4. Regime Context Framing.
5. Rule Construction Layer.
6. Strategy Composition Layer.
7. Risk Template Layer.
8. Strategy Candidate Registry.
9. Strategy Quality Gates.
10. Strategy Closure.
11. Strategy Dossier Handoff.

## Explicit Prohibitions

05 Strategy Engine must not:

- Run backtests.
- Calculate PnL.
- Calculate Sharpe, Sortino, Calmar, drawdown statistics, or return metrics.
- Read PostgreSQL.
- Read Parquet.
- Consume raw market data directly.
- Execute orders.
- Approve live trading.

## Design Principles

Risk-first: every candidate is designed under constraints before performance is considered.

Audit-first: every assumption, input, rule, and decision must be traceable.

Governance-first: candidates move forward only through documented contracts, gates, and closure records.
