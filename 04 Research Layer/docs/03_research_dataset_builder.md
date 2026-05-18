# Research Dataset Builder

## Concept

The Research Dataset Builder will create auditable datasets that join trusted features from 03 Feature Engineering with validated forward returns from the Forward Returns Engine.

The purpose is to provide a reproducible input surface for profiling, temporal stability analysis, informativeness analysis, and regime analysis.

## Expected Responsibilities

The builder will eventually define:

- Source feature set and feature version.
- Forward return version and horizons.
- Asset and timeframe scope.
- Timestamp alignment contract.
- Null and missing label handling.
- Dataset metadata and lineage.
- Validation status.

## Boundary

This component does not calculate features and does not redefine `technical_v1`. It also does not perform findings generation, strategy design, backtesting, or trading.

## Status

No research dataset is built in Block 1.

