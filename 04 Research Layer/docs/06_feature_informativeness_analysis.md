# Feature Informativeness Analysis

## Concept

Feature Informativeness Analysis evaluates whether feature values contain measurable information about future returns under predefined research metrics.

Informativeness is statistical research. It estimates whether a feature at timestamp `t` has a measurable relationship with forward returns already aligned at the same timestamp `t`.

Feature Informativeness is not a strategy, does not generate signals, does not define entry or exit rules, and does not prove profitability.

In Block 6, the analysis is a pure in-memory component. It accepts a research dataset already built in memory, feature columns, and forward return columns. It returns structured metrics in memory. It does not read PostgreSQL, read Parquet, write Parquet, write PostgreSQL, execute SQL, orchestrate pipelines, download data, or call external services.

## Initial Methods

The component includes:

- Bucket / quantile analysis.
- Mean forward return by bucket.
- Median forward return by bucket.
- Hit rate by bucket.
- Average absolute forward return by bucket.
- Information Coefficient using Pearson correlation.
- Information Coefficient using Spearman correlation.
- Preliminary technical ranking metadata.

## Relationship With Forward Returns

Forward returns are labels calculated before this block. Block 6 does not calculate forward returns, create new labels, shift rows, or change timestamp alignment.

The alignment contract is:

```text
feature[t] compared with forward_return_h[t]
```

Where `forward_return_h[t]` was produced by the Forward Returns Engine. Any additional shifting inside this block would risk lookahead contamination and is out of scope.

## Bucket / Quantile Analysis

Bucket analysis divides feature values into quantile buckets within each `symbol`, `timeframe`, `feature`, and `forward_return` scope.

For each bucket, Block 6 calculates:

- `count`
- `mean_forward_return`
- `median_forward_return`
- `hit_rate`
- `avg_abs_forward_return`

`hit_rate` is the fraction of non-null forward returns greater than zero inside the bucket. It is descriptive research metadata, not a trading win rate and not a backtest.

Repeated feature values may reduce the number of realized buckets. Constant features produce a single bucket. Missing feature or return values are excluded from bucket calculations.

## Information Coefficient

Information Coefficient is calculated as simple correlation between feature values and forward returns within each group:

- Pearson IC.
- Spearman IC.

The IC calculation drops rows where either the feature or the forward return is null. If there are too few observations, or either side is constant, the IC is null.

IC is not causality, not alpha, not profitability, and not a signal.

## Preliminary Technical Ranking

Block 6 creates a preliminary technical ranking table ordered within each `symbol`, `timeframe`, and `forward_return` by:

1. absolute Pearson IC;
2. absolute Spearman IC;
3. sample count.

This ranking is research metadata only. It must not be used as a BUY/SELL signal, feature selection decision, strategy rule, or automatic promotion mechanism.

## Output

The expected output is research evidence and feature rankings. Rankings are not trading signals and must not imply direct entry or exit decisions.

The in-memory output contains:

- bucket-level metrics;
- IC metrics;
- technical ranking metadata.

## Strategy Boundary

This analysis does not define thresholds for trading, positions, sizing, portfolio construction, optimization, backtests, or strategy performance metrics.

It also does not create `strategy_return`, positions, signals, BUY/SELL labels, trading rules, ML pipelines, model training, portfolio simulation, or economic narratives.

## Methodological Risks

Main risks:

- multiple testing across many features, horizons, assets, and timeframes;
- cherry-picking favorable buckets or horizons;
- interpreting correlation as causality;
- mistaking hit rate for tradable edge;
- treating a preliminary ranking as a strategy;
- ignoring temporal instability already surfaced by Block 5.

Block 6 does not solve all multiple testing risk. Block 10 must define formal correction and anti-overfitting controls before broad scans can be interpreted as evidence.

## Status

Specified and implemented in Block 6 as a pure in-memory feature informativeness engine with synthetic tests.
