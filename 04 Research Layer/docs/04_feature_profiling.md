# Feature Profiling

## Concept

Feature Profiling analyzes the standalone behavior of each feature by asset and timeframe before evaluating relationship with forward returns.

Feature Profiling describes features. It does not evaluate whether a feature predicts future returns, and it does not produce alpha evidence.

In Block 4, profiling is a pure in-memory component. It accepts feature rows already loaded into a `pandas.DataFrame` and returns structured statistics in memory. It does not read PostgreSQL, read Parquet, write Parquet, write PostgreSQL, execute SQL, orchestrate pipelines, download data, or call external services.

## Scope

Profiling should cover:

- Distribution shape.
- Null rates.
- Infinite values.
- Outliers.
- Skewness.
- Kurtosis.
- Variance.
- Degenerate or constant features.
- Fully null features.
- Correlation and redundancy between features.
- Asset-level and timeframe-level coverage.

## Profiling Versus Informativeness

Feature Profiling is descriptive quality analysis. It answers questions such as:

- Is this feature mostly null?
- Is this feature constant or near-degenerate?
- Does this feature have extreme outliers?
- Is the distribution heavily skewed?
- Is this feature redundant with another feature?
- Does the behavior differ by `symbol` or `timeframe`?

Feature Informativeness Analysis is predictive research. It asks whether a feature has a stable relationship with forward returns. That is out of scope for Block 4.

Profiling must not use forward returns, calculate information coefficient, calculate hit rate, rank features by predictive value, create findings, create hypotheses, create signals, define strategies, or run backtests.

## Minimum Metrics

For each numeric feature, the profiler must calculate:

- `count`
- `null_count`
- `null_ratio`
- `mean`
- `median`
- `std`
- `min`
- `max`
- `skewness`
- `kurtosis`
- `variance`
- `unique_values`
- `zero_ratio`
- `outlier_count`
- `outlier_ratio`

`count` is the number of non-null observations. `null_ratio` is calculated against total rows in the profiling group. `zero_ratio` is calculated against non-null observations.

## Outlier Method

Block 4 uses a simple interquartile range rule:

```text
lower_bound = q1 - 1.5 * IQR
upper_bound = q3 + 1.5 * IQR
IQR = q3 - q1
```

Values below `lower_bound` or above `upper_bound` are counted as outliers. The profiler does not remove, cap, winsorize, normalize, scale, or otherwise modify outlier values.

If a feature has no non-null values or has `IQR = 0`, the outlier count is `0` for that group.

## Correlation And Redundancy

Block 4 calculates pairwise Pearson correlation between numeric features within each profiling group. This is a redundancy and quality diagnostic only.

Extreme redundancy is identified when:

```text
abs(correlation) >= 0.95
```

This threshold marks candidate redundancy for review. It does not imply causality, predictive power, alpha, or an automatic decision to remove a feature.

## Stationarity Limitation

Stationarity testing is not implemented in Block 4. Feature profiling describes distributions, nulls, outliers, variance, and redundancy, but it does not test whether feature series are stationary.

Non-stationary features can produce spurious correlations when they share a trend with another variable. This is especially relevant in crypto markets, where long trending periods can make unrelated time series appear informative. Stationarity analysis is deferred.

## Grouping Contract

Profiling must be executable by:

- `symbol`
- `timeframe`
- `symbol` + `timeframe`

The default grouping is `symbol` + `timeframe`. Grouping is explicit so assets and timeframes are not mixed silently.

Input rows must include:

- `symbol`
- `timeframe`
- `timestamp`
- at least one numeric feature column

Forward return columns are not feature inputs for Block 4 and are excluded from profiling by default.

## Explicit Exclusion

Feature Profiling does not use forward returns. It describes feature quality and behavior only. Any relationship between a feature and future returns belongs to Temporal Stability Analysis or Feature Informativeness Analysis.

Block 4 also excludes feature ranking, predictive analysis, feature-to-return analysis, BUY/SELL signals, strategies, backtesting, PnL, Sharpe, Sortino, Calmar, expectancy, PostgreSQL, Parquet, real datasets, Binance, CCXT, downloads, findings, hypotheses, normalization, scaling, PCA, feature selection, clustering, embeddings, and ML.

## Status

Specified and implemented in Block 4 as a pure in-memory profiler with synthetic tests.
