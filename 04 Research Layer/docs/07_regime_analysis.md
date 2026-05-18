# Regime Analysis

## Concept

Regime Analysis studies whether feature-to-forward-return relationships differ under market conditions or data-defined regimes.

The goal is conditional research evidence, not conditional trading behavior.

In Block 7, a regime is a simple, explicit, auditable label that describes market context for a row in an already built in-memory research dataset. Regime Analysis asks whether feature informativeness metrics change across those labels.

Detecting differences between regimes does not imply creating automatic trading rules.

## Scope

Block 7 supports simple labels for:

- Trend regime: `bullish`, `bearish`, `neutral`.
- Volatility regime: `low_vol`, `medium_vol`, `high_vol`.
- Momentum regime: `positive`, `negative`, `flat`.
- Range regime: `compressed`, `expanded`.

Labels are derived from caller-provided numeric context columns already present in memory. The component does not read raw OHLCV, calculate complex indicators, train models, cluster observations, or forecast regimes.

Columns used to create regime labels cannot also be analyzed as feature columns in the same call. That overlap creates circular evidence: the feature would partly define the segment used to evaluate itself. The engine rejects this case explicitly.

## Regime Analysis Versus Regime Strategy

Regime Analysis is conditional research. It can show that feature metrics differ by context.

Regime Strategy is operational logic. It decides when to trade, when to disable a rule, how to size positions, or how to switch systems.

Block 7 is strictly Regime Analysis. It must not create regime switches, filters, market-timing rules, BUY/SELL labels, positions, strategy returns, or backtests.

## Methodological Rationale

Feature behavior can be context dependent. A relationship that appears stable in aggregate may be concentrated in high volatility, directional trend, compressed range, or momentum-specific periods.

Simple conditional analysis helps identify:

- changes of behavior by context;
- sensitivity to environment;
- conditional stability or instability;
- dependence on a small segment of observations.

This is not evidence of causality, alpha, or profitability. It is a diagnostic layer before later hypothesis review and anti-overfitting controls.

## Labeling Rules

Block 7 uses simple reproducible labels:

- Trend:
  - value greater than `positive_threshold` -> `bullish`
  - value less than `negative_threshold` -> `bearish`
  - otherwise -> `neutral`
- Momentum:
  - value greater than `positive_threshold` -> `positive`
  - value less than `negative_threshold` -> `negative`
  - otherwise -> `flat`
- Volatility:
  - lower within-group tercile -> `low_vol`
  - middle within-group tercile -> `medium_vol`
  - upper within-group tercile -> `high_vol`
- Range:
  - value less than or equal to within-group median -> `compressed`
  - value greater than within-group median -> `expanded`

Volatility and range labels are calculated independently inside each `symbol/timeframe` group. Constant volatility values map to `medium_vol`. Constant range values map to `compressed`.

## Conditional Metrics

For each `symbol`, `timeframe`, `forward_return`, `regime_type`, `regime`, and feature, Block 7 calculates:

- `sample_count`
- `mean_forward_return`
- `median_forward_return`
- `hit_rate`
- `avg_abs_forward_return`
- Pearson IC
- Spearman IC

These metrics are descriptive research diagnostics. They are not strategy performance metrics.

IC is calculated only when at least 5 non-null feature/return pairs exist inside the conditional segment. Smaller regime segments keep their sample counts and return summaries, but IC remains null to avoid mechanically perfect small-sample correlations.

## Separation Requirements

Regime Analysis must not mix:

- symbols;
- timeframes;
- horizons;
- regime types;
- regime labels.

Every conditional metric must retain traceability through:

```text
symbol, timeframe, forward_return, regime_type, regime
```

## Statistical Risks

Regime Analysis increases multiple testing risk because each feature can be evaluated across many symbols, timeframes, horizons, regime types, and regime labels.

Main risks:

- overfitting to a context segment;
- cherry-picking favorable regimes;
- excessive segmentation and small samples;
- interpreting conditional correlation as causality;
- treating a regime label as a trading switch;
- inventing economic narratives after seeing metrics.

Block 7 does not resolve these risks. Later quality controls must handle multiple testing, minimum sample rules, and hypothesis review.

## Explicit Boundary

Regime Analysis does not activate or deactivate trading rules. It does not create a regime strategy, regime switch, position filter, or execution condition.

It also excludes PostgreSQL, Parquet, real datasets, Binance, CCXT, downloads, ML, complex clustering, hidden Markov models, regime forecasting, optimization, PnL, Sharpe, Sortino, Calmar, strategy returns, positions, signals, BUY/SELL labels, and economic findings.

## Status

Specified and implemented in Block 7 as a pure in-memory regime labeling and conditional informativeness engine with synthetic tests.
