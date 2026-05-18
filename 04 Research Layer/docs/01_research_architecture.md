# Research Architecture

## Formal Definition

04 Research Layer is the auditable quantitative research layer between trusted features and strategy design. Its role is to transform feature data into evidence about future return relationships under controlled methodology, documented assumptions, and explicit anti-overfitting constraints.

The layer must support reproducible research artifacts that can be reviewed before any candidate is allowed to influence 05 Strategy Engine.

## Research Versus Strategy Boundary

Research asks whether a feature appears to have a stable, economically plausible relationship with future returns under defined tests.

Strategy decides how to trade, when to enter or exit, how much to size, how to manage risk, and how to evaluate portfolio-level outcomes. Those decisions are outside 04.

04 is prohibited from creating:

- Trading signals.
- Entry or exit logic.
- Position state.
- PnL.
- Formal backtests.
- Paper trading workflows.
- Live trading workflows.
- Execution logic.

## Conceptual Flow

Trusted features flow through the research process as:

`features confiables -> forward returns -> research datasets -> profiling -> stability -> informativeness -> regime -> hypotheses -> findings -> quality gates -> candidates for strategy`

Each step must preserve lineage, assumptions, and validation status.

## Component Structure

04 Research Layer is organized into 11 conceptual components:

1. Research Architecture.
2. Forward Returns Engine.
3. Research Dataset Builder.
4. Feature Profiling.
5. Temporal Stability Analysis.
6. Feature Informativeness Analysis.
7. Regime Analysis.
8. Hypothesis Registry.
9. Research Findings Registry.
10. Research Quality / Anti-overfitting.
11. Research Closure.

## Main Risks

The architecture must control:

- Lookahead bias in forward returns.
- Multiple testing.
- Low sample size.
- Cherry-picking.
- Overfitting.
- Confusing research with strategy.
- Confusing regime analysis with regime strategy.
- Lack of reproducibility.
- Findings without economic logic.

