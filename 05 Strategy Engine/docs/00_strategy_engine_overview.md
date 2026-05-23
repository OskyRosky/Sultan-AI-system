# 00 Strategy Engine Overview

## Objective

05 Strategy Engine defines the infrastructure layer where governed research outputs are translated into auditable strategy candidates.

This stage exists to formalize strategic intent, signal abstractions, rule framing, regime context, risk constraints, quality gates, and dossier handoff requirements. It does not exist to prove profitability.

## Relationship With 04 Research Layer

04 Research Layer is the upstream evidence and hypothesis governance layer. It may close with no confirmed edge, no validated anomaly, or no tradable finding.

05 Strategy Engine starts after the closure of 04 and may only consume governed artifacts from 04. It must not freely inspect raw data, intermediate exploratory outputs, PostgreSQL tables, Parquet files, or ungoverned notebooks.

## Relationship With 06 Backtesting Engine

06 Backtesting Engine is the downstream validation and simulation layer. It is responsible for historical simulation, PnL calculation, performance statistics, execution assumptions, and validation under market mechanics.

05 Strategy Engine prepares structured candidates for 06. It does not validate profitability.

## What 05 Produces

- Strategy candidate definitions.
- Abstract signal descriptions.
- Rule and invalidation framing.
- Regime context assumptions.
- Risk template constraints.
- Candidate registry requirements.
- Quality gate documentation.
- Strategy closure records.
- Strategy dossier handoff artifacts for 06.

## What 05 Does Not Produce

- Real trading signals.
- Executable orders.
- Real trades.
- Backtests.
- PnL.
- Sharpe, Sortino, Calmar, or similar performance metrics.
- Confirmed edge.
- Production deployment.

## Initial State

Block 1 initializes the Strategy Engine architecture only. No strategy is approved, validated, traded, or backtested in this block.
