# Research Dataset Builder

## Concept

The Research Dataset Builder will create auditable datasets that join trusted features from 03 Feature Engineering with validated forward returns from the Forward Returns Engine.

The purpose is to provide a reproducible input surface for profiling, temporal stability analysis, informativeness analysis, and regime analysis.

In Block 3, the builder is a pure in-memory component. It accepts feature rows and forward return rows that are already loaded into `pandas.DataFrame` objects, validates their alignment keys, and returns a merged research dataset in memory. It does not read or write PostgreSQL, Parquet, SQL, files, or external services.

## Relationship With 03 Feature Engineering

03 Feature Engineering owns feature definitions, feature calculation logic, feature quality gates, and feature versioning. The Research Dataset Builder consumes those trusted feature outputs as already materialized in memory.

The builder must not modify feature definitions, recalculate features, rename feature meanings, create derived signals, or repair upstream feature values. It may validate dataset shape and key uniqueness before joining.

## Relationship With Forward Returns Engine

The Forward Returns Engine owns forward return calculation and timestamp label alignment. The Research Dataset Builder consumes its output as already calculated forward return columns.

The builder must not generate forward returns if they are absent. Missing label columns are a validation error, not a trigger for calculation.

## Join Contract

Features and forward returns are joined strictly on:

- `symbol`
- `timeframe`
- `timestamp`

These keys define one research observation. The same `symbol`, `timeframe`, and `timestamp` must refer to the same completed candle state in both inputs.

The join is an inner join in Block 3. Rows without matching keys on both sides are excluded from the research dataset rather than filled or fabricated. Missing labels inside matched forward return rows, such as terminal `NaN` values from insufficient future candles, are preserved.

## Minimum Required Columns

Feature input must contain:

- `symbol`
- `timeframe`
- `timestamp`
- at least one non-key feature column

Forward return input must contain:

- `symbol`
- `timeframe`
- `timestamp`
- at least one forward return column

Forward return columns are identified by the `forward_return_` prefix by default.

## Temporal Alignment Rules

The builder preserves the Block 2 timestamp alignment contract:

```text
feature row at t + forward_return_h[t]
```

Where `forward_return_h[t]` was calculated as:

```text
close[t + h] / close[t] - 1
```

The builder must not shift timestamps, forward-fill labels, backfill labels, interpolate labels, or use future label values as features. Forward returns remain labels aligned to feature rows at `t`.

## Validation Rules

Before joining, the builder must validate:

- required key columns are present in both inputs;
- feature rows have no duplicate `(symbol, timeframe, timestamp)` keys;
- forward return rows have no duplicate `(symbol, timeframe, timestamp)` keys;
- at least one feature column is present;
- at least one forward return column is present;
- join keys remain isolated by `symbol` and `timeframe`;
- output ordering is deterministic by `symbol`, `timeframe`, and `timestamp`.

Duplicate keys are rejected because they make a research observation ambiguous. The builder must fail fast instead of silently choosing one row.

## Expected Responsibilities

The builder defines:

- Source feature input contract.
- Forward return input contract.
- Join keys and alignment rules.
- Null and missing label preservation.
- Validation status for in-memory research datasets.

Later blocks may add source feature set/version metadata, forward return version metadata, asset/timeframe scope metadata, lineage manifests, and storage contracts.

## Boundary

This component does not calculate features and does not redefine `technical_v1`. It also does not perform findings generation, strategy design, backtesting, or trading.

Block 3 also excludes PostgreSQL reads/writes, Parquet reads/writes, SQL execution, real research dataset creation, real findings, real hypotheses, BUY/SELL signals, PnL, Sharpe, Sortino, Calmar, expectancy, CCXT, downloads, and Binance calls.

## Status

Specified and implemented in Block 3 as a pure in-memory builder with synthetic tests. No real research dataset is created or stored.
