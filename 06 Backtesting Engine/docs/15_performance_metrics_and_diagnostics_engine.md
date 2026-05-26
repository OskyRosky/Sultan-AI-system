# 15 Performance Metrics And Diagnostics Engine

## Purpose

Block 10 defines the Performance Metrics & Diagnostics Engine contract for 06 Backtesting Engine.

Its purpose is to govern how outputs from a completed Block 09 simulation are measured, described, versioned, and made auditable.

This block answers the question: what happened during the simulation?

It does not answer why it happened, whether it will happen again, whether the strategy has edge, whether capital should be allocated, or whether the strategy is deployable.

Measurement precedes interpretation.

Metrics are observations. They are not conclusions.

Performance diagnostics describe historical simulation outputs. They do not validate a strategy, prove edge, establish deployability, authorize paper trading, authorize live trading, or approve capital allocation.

## Metrics Philosophy

Metrics describe outcomes.

Metrics do not explain causes.

Metrics do not prove robustness.

Metrics do not prove edge.

Metrics do not imply future profitability.

A strategy may exhibit attractive metrics and still be invalid if upstream governance, simulation integrity, measurement lineage, or diagnostic controls fail.

A strategy may exhibit poor metrics and still be methodologically valid. Poor results from a valid experiment remain governed evidence for later interpretation.

Block 10 must preserve the distinction between measurement and interpretation. It may describe simulated historical outcomes, but it must not convert those outcomes into conclusions about strategy quality.

## Simulation Output Intake Contract

Block 10 consumes only governed simulation outputs from Block 09.

The minimum conceptual intake artifacts are:

- Simulation run record.
- Simulated trades.
- Simulated positions.
- Exposure trace.
- Event log.
- Warning log.
- Failure log.
- Reproducibility metadata.

Block 10 must verify that the received artifacts are complete, versioned, traceable, and consistent with the Block 09 simulation run record.

Block 10 must not:

- Create missing simulation data.
- Reconstruct simulations.
- Modify simulated trades.
- Modify simulated positions.
- Alter simulation events.
- Repair simulation defects.
- Infer missing exposure history.
- Replace missing warning or failure records.
- Reinterpret execution or risk assumptions.
- Rerun the simulation under different assumptions.

If required simulation outputs are missing, inconsistent, corrupted, or unverifiable, performance measurement is invalid and must stop.

## Performance Measurement Categories

Performance measurement categories define what may be described from governed simulation outputs.

Conceptual categories include:

- Return metrics.
- Risk metrics.
- Drawdown metrics.
- Trade metrics.
- Exposure metrics.
- Benchmark-relative metrics.
- Distribution diagnostics.
- Stability diagnostics.

These categories are governance concepts. Block 10 does not define formulas, numerical implementations, concrete metric values, dashboards, visualizations, scorecards, rankings, or deployment thresholds.

Metric categories must be defined before result inspection. Metric definitions must be versioned. A metric must trace to the specific simulation output artifacts it consumes.

## Trade-Level Diagnostics

Trade-level diagnostics describe simulated trade artifacts produced by Block 09.

Conceptual examples include:

- Trade count.
- Holding duration.
- Trade frequency.
- Win and loss characteristics.
- Trade outcome distributions.
- Execution outcome diagnostics.
- Rejected or blocked action diagnostics.

Trade-level diagnostics must not classify a strategy as good, bad, robust, profitable, deployable, or capital-ready.

Trade diagnostics must remain traceable to simulated trades, event records, execution assumption applications, and warning or failure logs.

## Portfolio-Level Diagnostics

Portfolio-level diagnostics describe simulated portfolio behavior produced by Block 09.

Conceptual examples include:

- Cumulative return behavior.
- Capital path behavior.
- Exposure behavior.
- Concentration behavior.
- Turnover behavior.
- Position lifecycle behavior.
- Cash or capital state behavior, where applicable.

Block 10 does not optimize the portfolio, alter portfolio constraints, change sizing, reinterpret capital allocation, or adjust exposure after observing results.

Portfolio-level diagnostics are descriptions of the simulated record, not evidence of future portfolio behavior.

## Risk Diagnostics

Risk diagnostics describe historical risk behavior observed in the governed simulation output.

Conceptual examples include:

- Volatility observations.
- Drawdown observations.
- Tail event observations.
- Exposure concentration observations.
- Leverage behavior observations.
- Constraint activation observations.

Risk diagnostics do not approve risk limits, validate risk models, establish robustness, authorize leverage, or prove downside control.

Block 10 must not use risk diagnostics to repair Block 08 risk assumptions or Block 09 simulation behavior.

## Benchmark Comparison Framework

Metrics may be compared to governed benchmarks defined and frozen under Block 06.

Benchmark comparison describes differences.

Benchmark comparison does not prove superiority.

Benchmark comparison does not establish edge.

Benchmark comparison does not imply future outperformance.

Benchmark selection remains governed by Block 06. Block 10 must not introduce, replace, weaken, or reinterpret benchmarks after seeing results.

If the benchmark reference is missing, unversioned, inconsistent with the frozen protocol, or unavailable in the simulation metadata, benchmark-relative measurement must stop or be marked invalid.

## Metric Integrity Controls

Metric integrity requires that every metric and diagnostic remain traceable to governed simulation outputs.

Controls include:

- Metrics must trace to Block 09 simulation artifacts.
- Metric definitions must be versioned.
- Benchmark definitions must be versioned.
- Metric lineage must identify source artifacts.
- No reconstructed data is allowed.
- No missing input substitution is allowed.
- No selective metric creation is allowed.
- No metric cherry-picking is allowed.
- No metric may be created after inspecting results.
- No metric may be omitted because it is unfavorable if it was part of the governed metric set.
- No diagnostic may be reframed as validation.

Metric creation after inspecting results is prohibited.

If a metric definition changes, the changed definition creates a new measurement artifact version. It must not overwrite prior measurement artifacts.

## Diagnostic Failure Conditions

Block 10 must stop measurement or mark the diagnostic process invalid when any of the following are confirmed or cannot be resolved:

- Missing simulation run record.
- Missing simulated trades when trade diagnostics are required.
- Missing simulated positions when position diagnostics are required.
- Missing exposure trace when exposure or risk diagnostics are required.
- Missing event log.
- Missing warning or failure log.
- Missing benchmark reference for benchmark-relative diagnostics.
- Inconsistent trade records.
- Inconsistent position records.
- Inconsistent exposure records.
- Corrupted reproducibility metadata.
- Unverifiable metric lineage.
- Unversioned metric definitions.
- Unversioned benchmark definitions.
- Simulation version mismatch.
- Protocol version mismatch.
- Metric definition changed after result inspection.
- Selective metric reporting.
- Attempted reconstruction of missing simulation data.
- Attempted repair of simulation defects.

If a failure condition occurs, Block 10 must not emit valid performance artifacts. The process must return to Block 09 or the relevant upstream governance owner.

## Performance Artifact Registry

Block 10 must conceptually register the artifacts it produces from governed simulation outputs.

Performance artifacts include:

- Metric set.
- Diagnostic set.
- Benchmark comparison set.
- Warning set.
- Failure set, if measurement failed.
- Lineage record.
- Version metadata.

Each artifact must identify:

- Simulation run reference.
- Metric definition version.
- Benchmark reference, where applicable.
- Source simulation artifacts.
- Measurement timestamp.
- Reviewer or process identity, when formalized.
- Warning and failure status.

Performance artifacts are measurement records. They are not strategy approvals, edge claims, deployment recommendations, or capital allocation decisions.

## Performance Audit Trail

Every performance measurement attempt must leave auditable evidence.

The audit trail must include:

- Simulation version.
- Simulation run record reference.
- Metric definitions version.
- Benchmark version.
- Source artifact references.
- Reproducibility metadata reference.
- Reviewer or process identity, when formalized.
- Timestamp.
- Warnings.
- Failures.
- Reviewed metric categories.
- Categories reviewed and cleared.
- Categories reviewed and marked not applicable.
- Risks found.
- Risks reviewed and cleared.
- Unresolved categories.
- Lineage checks.
- Version checks.
- Confirmation that no strategy design, simulation execution, robustness testing, falsification testing, optimization, parameter search, dashboard creation, visualization creation, deployment scoring, edge conclusion, or future profitability claim occurred in Block 10.

The negative evidence principle applies: the audit trail must document not only what failed or was found, but also which metric and diagnostic categories were reviewed and cleared or marked not applicable.

The audit trail must be sufficient for quant research governance, model risk management, internal audit, trading systems engineering, reproducibility review, and external technical due diligence.

## Relationship With Block 11

Block 11 receives:

- Performance metrics.
- Diagnostics.
- Benchmark comparisons.
- Warnings.
- Failure records, if any.
- Lineage metadata.
- Performance artifact registry references.
- Performance audit trail.

Block 11 may challenge metrics, question measurement validity, evaluate robustness, perform falsification review, and assess anti-overfitting controls.

Block 11 must not:

- Modify historical metrics.
- Alter Block 09 simulation outputs.
- Rewrite performance results.
- Replace benchmark comparisons.
- Repair metric lineage defects.
- Infer missing simulation data.
- Convert diagnostics into unregistered metrics.
- Treat measurement artifacts as proof of edge.

If Block 11 detects problems in simulation outputs, metric lineage, benchmark references, or measurement integrity, it must return the process to Block 10, Block 09, or the relevant upstream block.

Block 11 may interpret, challenge, and stress the evidence. It cannot rewrite the measurement record.

## Governance Requirements

Block 10 must preserve:

- Temporal certification from Block 04.
- Strategy specification and assumptions from Block 05.
- Frozen protocol and benchmark governance from Block 06.
- Execution configuration from Block 07.
- Risk configuration from Block 08.
- Simulation artifacts from Block 09.
- Integrated assumption validation record.
- Experiment identity and versioning.
- Protocol lineage and prior experiment records.

Block 10 must not authorize trading, paper trading, deployment, live execution, broker connectivity, capital allocation, production risk controls, leverage approval, robustness conclusions, falsification conclusions, or edge claims.

## Performance Integrity Principle

The purpose of performance measurement is faithful description.

Not persuasion.

Not promotion.

Not strategy selection.

Not deployment justification.

When attractive narratives conflict with measurement integrity, measurement integrity takes precedence.

The system must reject incomplete, selective, or non-traceable measurement rather than accept a persuasive but invalid performance story.

## Explicit Non-Scope

Block 10 does not create formulas.

Block 10 does not calculate concrete metric values.

Block 10 does not create Python code.

Block 10 does not create SQL.

Block 10 does not create dashboards.

Block 10 does not create visualizations.

Block 10 does not execute simulations.

Block 10 does not reconstruct simulations.

Block 10 does not optimize parameters.

Block 10 does not perform parameter search.

Block 10 does not rank strategies.

Block 10 does not create deployment scoring.

Block 10 does not create machine learning models.

Block 10 does not create robustness testing.

Block 10 does not create falsification testing.

Block 10 does not interpret strategy edge.

Block 10 does not imply future profitability.

Block 10 is a documentation and conceptual governance block that defines how governed simulation artifacts may be measured and diagnosed before later robustness, falsification, and anti-overfitting review.
