# Forward Returns Engine

## Concept

The Forward Returns Engine will define and calculate future returns aligned after the feature timestamp. It is the first research component that links present-time feature observations to future price movement.

The engine is a pure in-memory research component. It accepts OHLCV data already loaded into a `pandas.DataFrame` and returns a `pandas.DataFrame` with forward return label columns. It does not read PostgreSQL, read Parquet, write Parquet, create research datasets, orchestrate pipelines, create signals, create strategies, or run backtests.

## Timestamp Alignment Contract

A feature calculated at timestamp `t` may only use information available up to and including `t`. The forward return label attached to that same row must use only prices after `t`.

The required formula is:

```text
forward_return_h[t] = close[t + h] / close[t] - 1
```

Where:

- `h` is a count of future candles.
- `close[t]` is the close price known at timestamp `t`.
- `close[t + h]` is a future close price used only as a label.
- The label is aligned back to row `t`.
- Future prices must never become feature inputs.
- Rows without enough future candles for a given horizon must remain `NaN`.
- The engine must not forward-fill, backfill, or interpolate missing labels.

This contract intentionally uses the current candle close as the denominator. It assumes the feature row timestamp represents the completed candle state at `t`. If a future feature source uses intrabar or pre-close values, that source must define a separate timestamp convention before it can use this engine.

## Temporal Ordering And Boundaries

Input rows must be processed in strict temporal order within each independent `(symbol, timeframe)` series. The engine may sort rows for deterministic calculation, but the caller must treat duplicate `(symbol, timeframe, timestamp)` rows as invalid input.

Duplicate timestamps are rejected because they make `close[t]` ambiguous and can hide accidental data duplication. The engine must fail fast instead of choosing one duplicate row silently.

Gaps are allowed and are not filled. A horizon of `h` means the `h`-th next available candle in that same `(symbol, timeframe)` series, not a guaranteed wall-clock duration. Gap detection and calendar completeness checks belong to later data quality analysis; this engine must not synthesize missing candles.

Each `symbol` is isolated from every other `symbol`. Each `timeframe` is isolated from every other `timeframe`. Forward returns must never cross asset or timeframe boundaries.

## Initial Horizons

The initial forward return horizons are:

- 1 candle.
- 3 candles.
- 5 candles.
- 10 candles.

Horizons are defined as candle counts, not absolute time:

- `h=10` on `1h` means 10 hours.
- `h=10` on `4h` means 40 hours.
- `h=10` on `1d` means 10 days.

No differentiated horizon set by timeframe is introduced in Block 2. The rationale is to investigate behavior relative to candle structure while preserving a consistent methodology across timeframes.

Block 2 calculates simple arithmetic forward returns only. Log forward returns are intentionally out of scope until documented as a separate methodological decision.

## Lookahead Bias Risk

Forward returns are a primary source of lookahead bias. The engine must ensure that features at time `t` are matched only with returns that start strictly after the feature observation point and use future prices unavailable at `t` only as labels, never as inputs.

The safest implementation pattern is to calculate each label with a negative shift of the close column inside each `(symbol, timeframe)` group:

```text
future_close_h = close.shift(-h)
forward_return_h = future_close_h / close - 1
```

The shifted future close is an intermediate label input only. It must not be emitted as a feature and must not be joined back into any feature set as an explanatory variable.

## Validation Requirement

The component must include autonomous tests before being trusted. Tests should cover timestamp ordering, horizon alignment, missing rows, duplicate timestamps, asset boundaries, timeframe boundaries, and prevention of using future information as a feature.

Synthetic tests are required before real data use. They must verify:

- exact alignment of `forward_return_1`, `forward_return_3`, `forward_return_5`, and `forward_return_10`;
- no cross-contamination across `symbol`;
- no cross-contamination across `timeframe`;
- deterministic sorting by timestamp within each series;
- rejection of duplicate `(symbol, timeframe, timestamp)` rows;
- unchanged `NaN` labels where future rows are insufficient;
- no filling or interpolation of missing labels;
- use of only OHLCV columns already present in memory.

## Status

Specified and implemented in Block 2 as a pure in-memory engine with synthetic tests. Real data reads, storage writes, research datasets, signals, strategies, and backtests remain out of scope.
