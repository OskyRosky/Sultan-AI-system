# Forward Returns Engine

## Concept

The Forward Returns Engine will define and calculate future returns aligned after the feature timestamp. It is the first research component that links present-time feature observations to future price movement.

This document is conceptual only for Block 1. No implementation, data reads, SQL execution, Parquet writes, or PostgreSQL writes are included here.

## Initial Horizons

The initial forward return horizons are:

- 1 candle.
- 3 candles.
- 5 candles.
- 10 candles.

The exact formula, timestamp alignment, missing data behavior, asset/timeframe handling, and storage contract will be specified before implementation.

## Lookahead Bias Risk

Forward returns are a primary source of lookahead bias. The engine must ensure that features at time `t` are matched only with returns that start strictly after the feature observation point and use future prices unavailable at `t` only as labels, never as inputs.

## Validation Requirement

The component must include autonomous tests before being trusted. Tests should cover timestamp ordering, horizon alignment, missing rows, duplicate timestamps, asset boundaries, timeframe boundaries, and prevention of using future information as a feature.

## Status

Not implemented in Block 1.

