# 04 Research Layer Overview

## Objective

04 Research Layer converts reliable feature outputs from 03 Feature Engineering into quantitative evidence, investigable hypotheses, structured findings, and candidates for 05 Strategy Engine.

The layer is data-first, risk-first, and audit-first. It must preserve reproducibility and separate quantitative research from strategy design, backtesting, paper trading, live trading, and execution.

## Relationship with 03 Feature Engineering

03 Feature Engineering is the upstream source of trusted features. The initial feature set is `technical_v1`, feature version `1.0.0`, produced and validated before this layer starts.

04 Research Layer consumes those features from approved storage surfaces, such as PostgreSQL or Parquet, without changing feature definitions, calculation logic, quality gates, or orchestration owned by 03.

## Exchange Assumption

The current 04 Research Layer grouping key is `symbol` + `timeframe`, with `timestamp` used as the observation key where needed. Upstream 03 Feature Engineering may use `exchange`, `symbol`, `timeframe`, and `timestamp`.

Until multi-exchange support is explicitly designed, 04 assumes the caller provides single-exchange series or prefilters to one exchange before calling in-memory research functions. Mixing the same `symbol/timeframe/timestamp` from multiple exchanges would contaminate research observations and can create misleading feature, return, stability, informativeness, and regime metrics.

Multi-exchange research support is out of scope for the current framework.

## Relationship with 05 Strategy Engine

05 Strategy Engine is the downstream consumer of research outputs. 04 may provide ranked feature evidence, hypothesis candidates, caveats, and structured findings for consideration.

04 does not define entry rules, exit rules, position logic, sizing logic, portfolio logic, backtests, or strategy performance metrics.

## Outputs

04 Research Layer produces:

- Forward return definitions and validated outputs.
- Research datasets that join features with forward returns.
- Feature profiling results.
- Temporal stability analysis.
- Feature informativeness analysis.
- Regime-conditioned research analysis.
- Hypothesis registry entries.
- Structured findings registry entries.
- Research quality and anti-overfitting checks.
- Final research dossier inputs for 05 Strategy Engine.

## Non-Outputs

04 Research Layer does not produce:

- BUY or SELL signals.
- Entry or exit rules.
- Positions.
- Strategy returns.
- PnL.
- Formal backtests.
- Paper trading.
- Live trading.
- Order execution.
- Parameter optimization.
- Strategy performance metrics such as Sharpe, Sortino, Calmar, or expectancy.

## Initial State

This block creates the initial folder structure, conceptual documentation, initial backlog, and decision log for 04 Research Layer. It does not read real data, write research datasets, calculate forward returns, execute SQL, or generate findings.
