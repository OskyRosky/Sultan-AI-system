# 01 Backtesting Architecture

## Formal Definition

Backtesting Engine is the governed historical evaluation layer that converts a valid StrategyDossier into an auditable historical evaluation, when and only when the dossier can be operationalized honestly under explicit assumptions.

It is not a strategy design layer, not a research discovery layer, not a live execution layer, not a paper trading system, and not a deployment approval process.

## Conceptual Flow

1. Receive a governed StrategyDossier from 05 Strategy Engine.
2. Decide whether the dossier is eligible for 06 review.
3. Bind the evaluation to a historical data and feature snapshot.
4. Certify temporal admissibility before operationalization.
5. Convert the conceptual dossier into a simulation specification, adding only explicit 06-owned experimental assumptions where justified.
6. Freeze the experiment and evaluation protocol before observing results.
7. Define simulated execution frictions and market constraints.
8. Define simulated risk and exposure assumptions.
9. Execute a reproducible historical simulation.
10. Calculate performance metrics and diagnostics.
11. Evaluate robustness, falsification, and overfitting risk.
12. Close the result and hand governed feedback to 04 and 05.

## Architectural Separation

Input governance determines whether a StrategyDossier can enter 06.

Data snapshot governance determines exactly which historical data, features, versions, timestamps, universe, time range, gaps, and availability assumptions are bound to the evaluation.

Temporal admissibility determines whether the bound snapshot and feature set can be used without lookahead, leakage, or availability violations.

Operationalization converts conceptual strategy material into a historically evaluable specification. It must keep 05 content separate from 06 experimental assumptions.

Experiment protocol defines splits, walk-forward logic, benchmarks, seeds, comparison rules, and evaluation order before results are observed.

Friction simulation defines fills, fees, slippage, latency assumptions, liquidity constraints, and market realism for historical simulation only.

Risk simulation defines sizing, exposure, and risk-control assumptions for historical simulation only. It does not calibrate a live Risk Engine.

Simulation execution produces simulated trades, positions, events, equity curve, and logs under approved contracts.

Metrics and diagnostics calculate historical performance and behavior summaries.

Robustness and falsification determine whether results are falsified, inconclusive, not robust, or robust pending review.

Closure and feedback record the outcome without mutating upstream artifacts or authorizing trading.

## Why Block 04 Comes Before Block 05

Temporal Data Admissibility must occur before Strategy Operationalization because operational rules can only be evaluated honestly if their required data and features were available at the simulated decision time.

If 06 operationalizes first, it may accidentally define rules around data that are not temporally admissible, creating lookahead bias or hidden leakage. Block 04 is therefore a blocking control before converting the dossier into a simulation specification.

## Why Block 06 Freezes The Protocol Before Results

The Experiment & Evaluation Protocol must be frozen before observing simulation results to prevent outcome-driven edits, uncontrolled comparison changes, parameter mining, benchmark switching, and selective reporting.

`protocol_frozen` means the evaluation plan was defined before result inspection. It does not mean that the strategy is approved, profitable, robust, or authorized for paper trading, live trading, deployment, or capital allocation.

## Boundary With Future Layers

06 produces historical evaluation evidence and governed feedback. It does not authorize paper trading, live trading, deployment, capital allocation, exchange connectivity, order routing, or production risk controls.
