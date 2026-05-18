# Temporal Stability Analysis

## Concept

Temporal Stability Analysis evaluates whether the relationship between a feature and future returns is consistent across time windows.

The purpose is to reduce the risk of accepting patterns that exist only in one isolated period.

Temporal stability is still statistical research, not strategy research. A feature can appear useful in one period and fail completely in another. Block 5 exists to expose that cross-period behavior before later informativeness analysis makes stronger claims.

In Block 5, the analysis is a pure in-memory component. It accepts a research dataset already built in memory, feature columns, forward return columns, and timestamp columns. It returns structured stability metrics in memory. It does not read PostgreSQL, read Parquet, write Parquet, write PostgreSQL, execute SQL, orchestrate pipelines, download data, or call external services.

## Scope

This component evaluates:

- Explicit temporal segmentation.
- Window-level feature behavior.
- Window-level feature-to-forward-return correlation.
- Sign consistency.
- Degradation across time.
- Variance drift.
- Correlation drift.
- Basic feature behavior consistency.
- Stability by `symbol`.
- Stability by `timeframe`.

The initial implementation uses simple, explicit windows. It does not do rolling optimization, parameter search, forecasting, ML, ensemble scoring, automatic feature selection, or feature ranking.

## Methodological Rationale

Feature-to-return relationships are vulnerable to temporal overfitting. A relationship observed in one sample may be caused by a single market period, one asset-specific episode, or a small number of unusual observations.

Temporal Stability Analysis helps separate:

- relationships that are directionally consistent across windows;
- relationships that reverse sign across windows;
- relationships that appear only in one period;
- feature behavior that drifts materially across periods.

This evidence is preparatory. It does not prove causality, alpha, profitability, or tradability.

## Boundary with Profiling

Profiling describes feature distributions without forward returns. Temporal Stability Analysis studies the time-varying relationship between feature values and future returns.

Profiling asks how a feature behaves by itself. Temporal Stability asks whether feature behavior and feature-to-forward-return relationships change across windows.

## Boundary with Informativeness

Temporal Stability Analysis is not the full informativeness layer. It may calculate simple window-level Pearson correlation as a stability diagnostic, but it does not rank features, calculate a final information coefficient package, define hit rates, create composite scores, or decide whether a feature should be used by a strategy.

## Boundary with Strategy

Temporal stability evidence may inform whether a feature is a candidate for later strategy research, but it does not create trading rules, signals, or backtests.

## Window Contract

Block 5 supports two simple window modes:

- Explicit windows supplied by the caller with a label, start timestamp, and end timestamp.
- Equal-count chronological windows created independently inside each `symbol/timeframe` group.

Explicit windows are preferred when a research review needs fixed calendar boundaries. Equal-count windows are useful for synthetic tests and early methodology checks.

Windows must not mix `symbol` values or `timeframe` values. Every metric keeps traceability through:

```text
symbol, timeframe, window
```

Empty explicit windows are represented with `sample_count = 0` and null metrics. This makes missing coverage visible instead of silently dropping periods.

## Minimum Metrics

Per `symbol`, `timeframe`, `window`, `feature`, and `forward_return` pair, Block 5 calculates:

- `sample_count` for non-null feature/return pairs;
- `feature_mean`;
- `feature_std`;
- `feature_variance`;
- `return_mean`;
- `return_std`;
- `return_variance`;
- `correlation`;
- `correlation_sign`;
- `window_start`;
- `window_end`.

Correlation is calculated only when at least 5 non-null feature/return pairs are available. This avoids mechanically perfect correlations from two-point samples while still allowing lightweight synthetic validation. Correlations from small samples remain descriptive and should not be treated as inferential evidence.

Across windows, Block 5 calculates:

- `windows_observed`;
- `correlation_min`;
- `correlation_max`;
- `correlation_range`;
- `correlation_std`;
- `feature_mean_min`;
- `feature_mean_max`;
- `feature_mean_range`;
- `feature_mean_std`;
- `sign_consistency_ratio`.

These are diagnostics only. They must not be interpreted as edge, profitability, or automatic usefulness.

## Risks

Main risks controlled by this block:

- temporal overfitting;
- cherry-picking a favorable period;
- mistaking one-period behavior for robust evidence;
- mixing assets or timeframes silently;
- interpreting stable correlation as causality or profitability;
- rejecting a feature automatically because one diagnostic is unstable.

## Status

Specified and implemented in Block 5 as a pure in-memory temporal stability engine with synthetic tests.
