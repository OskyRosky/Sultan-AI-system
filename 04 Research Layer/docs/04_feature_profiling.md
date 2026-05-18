# Feature Profiling

## Concept

Feature Profiling analyzes the standalone behavior of each feature by asset and timeframe before evaluating relationship with forward returns.

## Scope

Profiling should cover:

- Distribution shape.
- Null rates.
- Infinite values.
- Outliers.
- Stability of summary statistics.
- Stationarity diagnostics where appropriate.
- Asset-level and timeframe-level coverage.

## Explicit Exclusion

Feature Profiling does not use forward returns. It describes feature quality and behavior only. Any relationship between a feature and future returns belongs to Temporal Stability Analysis or Feature Informativeness Analysis.

## Status

Not implemented in Block 1.

