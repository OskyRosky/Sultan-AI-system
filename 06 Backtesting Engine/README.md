# 06 Backtesting Engine

## Purpose

06 Backtesting Engine is the historical evaluation layer for governed StrategyDossiers produced by 05 Strategy Engine.

Its purpose is to determine whether a governed strategy candidate can be translated into an honest, reproducible, temporally correct, and auditable historical evaluation. In later blocks, this stage will define how controlled simulations, assumptions, frictions, risk exposure, metrics, robustness checks, and feedback handoff are governed.

## Current Stage Status

Block 01 initialized the Backtesting Architecture.

Block 02 adds the Backtest Inputs & Eligibility Contract as documentation.

Block 03 adds the Historical Data & Feature Snapshot Contract as documentation.

Block 04 adds the Temporal Data Admissibility & Leakage Baseline Controls as documentation.

Block 05 adds the Strategy Operationalization & Simulation Specification as documentation.

Block 06 adds the Experiment & Evaluation Protocol as documentation.

Block 07 adds the Execution & Market Friction Simulation contract as documentation.

Block 08 adds the Risk & Exposure Simulation contract as documentation.

The current scope is documentation only. It does not implement a backtesting engine, trade simulator, PnL calculation, metrics engine, data loader, risk model, exchange integration, paper trading, live trading, deployment path, or notebook workflow.

## Relationship With 05 Strategy Engine

05 Strategy Engine produces a governed StrategyDossier with status such as `dossier_prepared_pending_final_audit`, subject to future input contracts.

06 Backtesting Engine treats the StrategyDossier as the upstream governed input. The dossier is not proof of edge, not trading approval, not performance validation, and not automatic authorization to run a backtest.

If 06 requires operational details that 05 deliberately does not calibrate, such as thresholds, sizing, stops, holding periods, leverage, capital allocation, execution assumptions, or friction assumptions, those details must be modeled as explicit, versioned, auditable experimental assumptions owned by 06 and kept separate from 05 content.

## What 06 Evaluates

06 may evaluate governed StrategyDossiers historically once future blocks define eligibility, data snapshots, temporal admissibility, operationalization, experiment protocol, frictions, risk simulation, simulation execution, metrics, robustness, closure, and feedback rules.

It does not authorize trading, paper trading, deployment, capital allocation, or live execution. Positive historical results do not confirm edge by themselves and do not guarantee future performance.

## 12-Block Map

1. Backtesting Architecture.
2. Backtest Inputs & Eligibility Contract.
3. Historical Data & Feature Snapshot Contract.
4. Temporal Data Admissibility & Leakage Baseline Controls. This is a blocking prerequisite before operationalization or simulation.
5. Strategy Operationalization & Simulation Specification.
6. Experiment & Evaluation Protocol.
7. Execution & Market Friction Simulation.
8. Risk & Exposure Simulation.
9. Backtest Simulation Engine.
10. Performance Metrics & Diagnostics Engine.
11. Robustness, Falsification & Anti-Overfitting.
12. Results Registry, Closure & Feedback Handoff.

## Core Warning

Historical evaluation is evidence generation under explicit assumptions. It is not confirmation of edge, not permission to trade, not permission to paper trade, and not deployment approval.

Snapshot certification does not imply temporal certification. Event time alone is insufficient without availability-at-decision-time evidence.
