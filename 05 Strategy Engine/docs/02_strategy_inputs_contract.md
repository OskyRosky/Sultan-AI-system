# 02 Strategy Inputs Contract

## Purpose

This document defines the conceptual boundary for inputs into 05 Strategy Engine.

Block 2 will be critical because uncontrolled inputs create uncontrolled strategy design. A strategy candidate must be traceable to governed upstream artifacts, not to informal data inspection or unreviewed intermediate files.

## Allowed Input Class

05 Strategy Engine may consume only governed artifacts from 04 Research Layer. These artifacts should include documented provenance, research closure status, assumptions, limitations, and evidence boundaries.

## Prohibited Input Classes

05 Strategy Engine must not consume:

- Raw market data.
- PostgreSQL tables.
- Parquet files.
- Ungoverned feature outputs.
- Draft notebooks.
- Intermediate exploratory files.
- Informal screenshots or manual observations.
- Any artifact that bypasses 04 Research Layer closure.

## Technical Scope

This is not yet a technical schema, API contract, parser, validator, or integration. No technical contract is implemented in Block 1.

The future Block 2 deliverable must define the minimum governed artifact structure required before any strategy candidate can be registered.
