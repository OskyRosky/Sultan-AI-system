# 08 Historical Data And Feature Snapshot Contract

## Purpose

Block 03 defines the Historical Data & Feature Snapshot Contract for 06 Backtesting Engine.

A snapshot is the documented, uniquely identifiable, versioned description of the historical data and features that a specific evaluation intends to use. It is a frozen reference universe for an evaluation, not a physical dataset created by this block.

This contract exists because no historical evaluation can be reproducible unless it can demonstrate exactly which data, features, time coverage, asset universe, source references, versions, assumptions, and known limitations were bound to the evaluation.

The risk controlled by this block is uncontrolled data drift: changing datasets, changing feature definitions, dynamic queries, retrospective corrections, missing lineage, and undocumented limitations that make later results impossible to reproduce or audit.

Block 03 occurs before temporal admissibility, operationalization, experiment protocol, frictions, risk simulation, simulation execution, metrics, and robustness review. It defines the evaluation universe before any technical validation or result-producing activity begins.

## Conceptual Flow

1. An eligible StrategyDossier exits Block 02.
2. Block 03 defines the historical data and feature snapshot.
3. Block 03 certifies documentation completeness for the snapshot.
4. Block 04 reviews temporal admissibility, lookahead risk, leakage risk, and future information contamination.

## Snapshot Definition

A Historical Data & Feature Snapshot is a frozen conceptual reference for a specific historical evaluation.

It must identify:

- Dataset universe.
- Asset universe.
- Market universe.
- Feature universe.
- Time coverage.
- Granularity.
- Source references.
- Data versions.
- Feature versions.
- Assumptions.
- Known limitations.

The snapshot is not a guarantee that the data is temporally admissible, leak-free, complete, clean, or suitable for simulation. It only defines what will be reviewed and evaluated by later blocks.

## Data Components

The snapshot must document the minimum data components needed to identify the historical data universe:

- Assets included.
- Markets or venues included.
- Instruments, symbols, or contract identifiers where applicable.
- Timeframes or bar intervals included.
- Historical start date.
- Historical end date.
- Declared data granularity.
- Data source references.
- Source metadata relevant to auditability.
- Version identifiers or equivalent immutable references.
- Known exclusions from the data universe.

This contract defines required information only. It does not define a technical schema, table, SQL model, parquet layout, DuckDB file, PostgreSQL table, or data pipeline.

## Feature Components

The snapshot must document the feature universe intended for evaluation:

- Feature names or conceptual identifiers.
- Feature origin.
- Feature version reference.
- Feature generation context.
- Upstream data dependencies.
- Feature Engineering reference from 03 Feature Engineering.
- Known feature limitations.
- Known exclusions from the feature universe.

Features must remain traceable to 03 Feature Engineering outputs. Block 03 does not create features, modify features, calculate features, or validate whether feature values are temporally admissible.

## Data Lineage Requirements

Every data component referenced by the snapshot must have identifiable lineage.

Data lineage must establish:

- Identifiable origin.
- Traceable source reference.
- Version or immutable reference.
- Provenance sufficient for audit review.
- Documentation sufficient to reproduce the selected universe.
- Relationship to the evaluation that will consume it.

Lineage is mandatory because historical results cannot be audited if the underlying data origin, version, or selection basis is unknown.

## Feature Lineage Requirements

Every feature referenced by the snapshot must have identifiable lineage to 03 Feature Engineering.

Feature lineage must establish:

- Feature identifier.
- Feature version or equivalent immutable reference.
- Feature Engineering source reference.
- Upstream data dependency reference.
- Conceptual generation context.
- Known limitations or exclusions.
- Documentation sufficient to reproduce the selected feature universe.

Feature lineage does not mean the feature is temporally safe. Temporal safety belongs to Block 04.

## Snapshot Versioning

Every historical evaluation must reference a uniquely identifiable snapshot.

Snapshots must be:

- Identifiable.
- Versioned.
- Conceptually immutable after certification.
- Auditable.
- Bound to a specific eligible StrategyDossier or evaluation record.
- Independent of future results.

An evaluation must not depend on mutable datasets, unversioned queries, unnamed feature sets, or dynamically changing source references. If a source dataset or feature definition changes, a new snapshot version must be defined rather than silently changing the existing snapshot.

## Temporal Coverage

The snapshot must declare temporal coverage.

At minimum, it must identify:

- Historical start date.
- Historical end date.
- Data granularity.
- Timeframes included.
- Declared coverage expectations.
- Known periods of missing or partial coverage.

Block 03 does not verify whether the declared coverage was available at each simulated decision time. Block 03 only records what coverage is claimed for later review.

## Asset Universe

The snapshot must freeze the asset universe for the intended evaluation.

At minimum, it must identify:

- Assets included.
- Assets excluded when exclusions are relevant to interpretation.
- Markets or venues included.
- Instrument naming or symbol conventions where relevant.
- Universe selection rationale.
- Known universe limitations.

The asset universe must be frozen before downstream work to prevent survivorship bias, cherry-picking, or result-driven universe changes.

## Known Limitations Registry

Every snapshot must include a known limitations registry.

Examples of known limitations include:

- Known data gaps.
- Missing periods.
- Partial coverage.
- Known source changes.
- Known symbol migrations.
- Known market structure changes.
- Known data quality events.
- Known feature coverage limitations.
- Known upstream dependency limitations.

Registering a limitation does not automatically invalidate the snapshot. It makes the limitation visible so Block 04 and later blocks can decide whether it affects temporal admissibility, operationalization, simulation, metrics, robustness, or closure.

Known limitations must be documented explicitly rather than hidden, implied, or left to reviewer memory.

## Snapshot Certification

Snapshot certification is a documentation completeness decision.

It confirms that:

- The snapshot is identifiable.
- The snapshot is versioned.
- Data components are documented.
- Feature components are documented.
- Data lineage is present.
- Feature lineage is present.
- Temporal coverage is declared.
- Asset universe is declared.
- Known limitations are registered.

Snapshot certification does not mean:

- Temporal validity is confirmed.
- Lookahead bias has been ruled out.
- Leakage has been ruled out.
- Future information contamination has been ruled out.
- Data quality is sufficient for simulation.
- Feature values are admissible at simulated decision time.
- The evaluation is approved for simulation.

## Snapshot Decision States

The initial conceptual snapshot decision states are:

| State | Meaning |
| --- | --- |
| `snapshot_defined_pending_temporal_review` | Snapshot documentation is complete enough to proceed to Block 04. |
| `snapshot_not_certified_unknown_data_origin` | Data origin is not identifiable. |
| `snapshot_not_certified_unknown_feature_origin` | Feature origin or Feature Engineering reference is not identifiable. |
| `snapshot_not_certified_missing_version_references` | Data or feature version references are missing. |
| `snapshot_not_certified_undefined_temporal_coverage` | Historical start, end, timeframe, or granularity is not defined. |
| `snapshot_not_certified_undefined_asset_universe` | Asset, market, venue, or instrument universe is not defined. |
| `snapshot_not_certified_undocumented_limitations` | Known limitations are absent, hidden, or not documented sufficiently. |
| `snapshot_not_certified_other` | Snapshot certification fails for a documented reason not covered by the initial states. |

These names are conceptual for Block 03 and may be formalized later as schemas, validators, registries, or tests.

## Failure Conditions

| Failure Condition | Why It Blocks Snapshot Certification |
| --- | --- |
| Unknown data origin. | The evaluation cannot prove what historical data it intends to use. |
| Unknown feature origin. | The evaluation cannot trace features to governed Feature Engineering outputs. |
| Missing version references. | The evaluation may depend on mutable or changing data and feature definitions. |
| Undefined temporal coverage. | The evaluation cannot establish the historical period under review. |
| Undefined asset universe. | The evaluation cannot establish which assets, markets, or instruments are included. |
| Undocumented limitations. | Later reviewers cannot distinguish known constraints from hidden problems. |
| Dynamic or mutable source reference. | Reproducibility cannot be guaranteed if the source can change silently. |
| Missing relationship to an eligible dossier. | The snapshot cannot be tied to a governed evaluation path from Block 02. |

## Governance Rules

Block 03 must not create datasets.

Block 03 must not load data.

Block 03 must not extract data.

Block 03 must not create SQL.

Block 03 must not create parquet, DuckDB, PostgreSQL, or other physical storage artifacts.

Block 03 must not calculate features.

Block 03 must not validate temporal admissibility.

Block 03 must not detect lookahead bias.

Block 03 must not detect leakage.

Block 03 must not approve simulation.

Block 03 may only define, document, and certify the completeness of the historical data and feature snapshot.

## Relationship With Block 04

Block 03 defines the snapshot.

Block 04 validates temporal admissibility.

Block 03 does not certify temporal validity.

Block 03 does not certify absence of lookahead.

Block 03 does not certify absence of leakage.

Block 03 does not certify absence of future information contamination.

Block 04 is the exclusive authority for:

- Lookahead review.
- Leakage review.
- Temporal admissibility.
- Future information contamination.
- Availability-at-decision-time review.

If Block 04 rejects the snapshot on temporal grounds, Block 03 certification remains only a documentation completeness record. It must not be interpreted as simulation approval.

## Relationship With Later Blocks

Block 05 may operationalize strategy rules only after Block 04 completes temporal admissibility review.

Blocks 06-12 may only use the snapshot according to their future contracts. They must not silently expand the asset universe, change feature versions, extend time coverage, or replace source references after results are observed.

## Explicit Non-Scope

Block 03 does not create real snapshots, datasets, storage artifacts, data pipelines, ETL, SQL, DuckDB, PostgreSQL, parquet files, temporal validation controls, leakage checks, simulations, metrics, execution logic, risk models, or executable schemas.
