# 05 Block Map

## 12 Blocks

| Block | Name | Responsibility | Depends On |
| --- | --- | --- | --- |
| 01 | Backtesting Architecture | Define scope, principles, boundaries, prohibitions, lifecycle, and relationship with 05 and future layers. | Closed 05 framework context. |
| 02 | Backtest Inputs & Eligibility Contract | Define which StrategyDossiers may enter 06, required statuses, traceability, and formal eligibility decisions. | Block 01. |
| 03 | Historical Data & Feature Snapshot Contract | Define exact historical data, features, versions, universe, time range, timestamps, gaps, availability, and reproducibility requirements. | Block 02. |
| 04 | Temporal Data Admissibility & Leakage Baseline Controls | Certify that snapshots and features are temporally usable before operationalization. Prevent lookahead, leakage, and availability errors. | Blocks 02-03. |
| 05 | Strategy Operationalization & Simulation Specification | Convert the conceptual dossier into an evaluable specification, documenting every added condition as a 06 experimental assumption. | Block 04. |
| 06 | Experiment & Evaluation Protocol | Define splits, in-sample, out-of-sample, walk-forward, benchmarks, seeds, versions, and comparison rules before results are inspected. | Block 05. |
| 07 | Execution & Market Friction Simulation | Define simulated fills, fees, slippage, latency assumptions, liquidity constraints, and market realism. | Block 06. |
| 08 | Risk & Exposure Simulation | Define simulated sizing, exposure, and risk controls while preserving 05 risk template boundaries. | Block 07. |
| 09 | Backtest Simulation Engine | Execute reproducible historical simulation and produce simulated trades, positions, events, equity curve, and audit logs. | Blocks 02-08. |
| 10 | Performance Metrics & Diagnostics Engine | Calculate PnL, returns, Sharpe, Sortino, drawdown, hit rate, turnover, exposure, and diagnostic summaries. | Block 09. |
| 11 | Robustness, Falsification & Anti-Overfitting | Evaluate sensitivity, costs, stability, out-of-sample, walk-forward, regimes, falsification, and overfitting risk. | Block 10. |
| 12 | Results Registry, Closure & Feedback Handoff | Register results, close the evaluation, and produce governed feedback to 04 and 05 without upstream mutation or trading authorization. | Block 11. |

## Critical Blocks

Block 04 is critical because no operationalization should occur until data and features are temporally admissible.

Block 05 is critical because it defines the boundary between 05 conceptual strategy content and 06 experimental simulation assumptions.

Block 06 is critical because the protocol must be frozen before results are observed.

Blocks 07 and 08 are critical because frictions, market mechanics, sizing, exposure, and risk simulation materially affect historical results and must not be invented after the fact.

Block 11 is critical because positive performance metrics are insufficient without robustness, falsification, and anti-overfitting review.

## Recommended Claude Code Audits

Run an external Claude Code audit after Block 05 to review the operationalization boundary and separation between 05 content and 06 assumptions.

Run an external Claude Code audit after Block 08 to review friction simulation, risk simulation, and whether assumptions remain controlled before execution.

Run an external Claude Code audit after Block 12 to review the complete historical evaluation lifecycle, result registry, closure, feedback handoff, and non-authorization boundaries.

## Non-Advancement Rule

Block 01 creates architecture documentation only. It does not advance to Block 02 and does not implement contracts, schemas, simulation logic, metrics, robustness checks, or registries.
