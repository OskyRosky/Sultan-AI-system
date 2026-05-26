# 11 Experiment And Evaluation Protocol

## Purpose

Block 06 defines the Experiment & Evaluation Protocol contract for 06 Backtesting Engine.

Its purpose is to govern how an operationalized Strategy Specification may be evaluated historically under controlled, reproducible, and auditable experimental conditions.

Backtesting is an experiment.

It is not evidence by itself. It is not validation. It is not proof of edge. It is not deployment authorization.

This block defines how valid evaluations are designed. It does not determine whether a strategy works. Result interpretation, robustness review, falsification, overfitting assessment, metrics, and closure belong to later blocks.

Block 06 occurs after Block 05 because the strategy specification, assumptions registry, traceability records, and operationalization decision must already be closed. Block 06 occurs before Block 07 because execution and market-friction simulation must follow a frozen protocol rather than shape the protocol.

## Experiment Philosophy

A backtest is an experiment designed to generate evidence.

The existence of a backtest does not make the result admissible. The protocol determines whether the result can later be interpreted as evidence.

Good results can come from invalid experiments.

Bad results can come from valid experiments.

Protocol validity precedes result interpretation. If the protocol is invalid, attractive results must be rejected as invalid evidence. If the protocol is valid, unfavorable results remain useful evidence for later interpretation.

## Evaluation Protocol Framework

Every evaluation protocol must define the minimum controlled components required for reproducibility:

- Operationalized strategy specification.
- Certified historical snapshot.
- Assumptions registry.
- Experiment configuration.
- Evaluation windows.
- Dataset partitions.
- Benchmark definition.
- Protocol metadata.

The protocol must be complete before results are inspected. It must be reproducible by an independent reviewer using the referenced versions, inputs, configuration, assumptions, and metadata.

The protocol must not add strategy logic, repair operationalization gaps, change temporal assumptions, create frictions, calculate metrics, optimize parameters, or choose robustness tests. Those responsibilities belong to other blocks or are explicitly prohibited here.

## Experimental Unit

An experimental unit is one governed historical evaluation run definition.

At minimum, an experimental unit is defined by:

- Strategy specification version.
- Historical snapshot version.
- Protocol version.
- Assumptions version.
- Benchmark version.
- Evaluation window definition.
- Dataset partition definition.
- Experiment configuration version.

Any change to one of these elements creates a new experimental unit. A changed unit must receive a new experiment identifier or version and must not overwrite the prior experiment.

## Dataset Partitioning Governance

Dataset partitions are governance constructs, not optimization tools.

Partitioning must preserve:

- No leakage between partitions.
- Chronological integrity.
- Documented partition definitions.
- Reproducible partition boundaries.
- Consistency with the temporally certified snapshot.
- Consistency with the operationalized specification.

Partition definitions must be fixed before evaluation. They must not be adjusted to improve results, avoid difficult regimes, hide losses, or support a preferred interpretation.

Partition leakage invalidates the experiment. If a partition boundary changes, the changed protocol creates a new experiment.

## In-Sample / Out-Of-Sample Governance

In-sample is the portion of historical data used for protocol-authorized development, calibration, or exploratory evaluation when such use is explicitly permitted by later governance.

Validation is the portion used to assess choices without final interpretation as an untouched holdout, when such a role is defined.

Out-of-sample is the portion reserved for evaluation under conditions not used to shape the strategy specification, assumptions, partitions, benchmark, or protocol.

Block 06 defines these roles conceptually. It does not perform optimization, model selection, parameter tuning, robustness testing, falsification testing, or result interpretation.

Rules:

- Partition roles must be documented before evaluation.
- No retroactive reassignment is allowed.
- No selective reporting is allowed.
- No post-hoc boundary changes are allowed.
- Changing partitions creates a new experiment.

In-sample, validation, and out-of-sample labels are protocol commitments. They are not narrative labels assigned after seeing results.

## Walk-Forward Governance

Walk-forward evaluation is a governed sequence of time-ordered evaluation windows intended to reduce dependence on a single static split and to generate evidence across multiple historical periods.

Walk-forward controls the protocol structure for repeated chronological evaluation. It can help make evaluation design more disciplined.

Walk-forward does not prove robustness. It does not prove edge. It does not eliminate overfitting. It does not replace Block 11 robustness, falsification, and anti-overfitting review.

Walk-forward is evidence generation. Interpretation belongs to later blocks.

Any walk-forward design must document:

- Window definitions.
- Step sequence.
- Chronological ordering.
- Refit or recalibration permissions, if any, and only when allowed by prior governance.
- Relationship to the certified snapshot and operationalized specification.

Block 06 does not execute walk-forward logic or interpret walk-forward results.

## Benchmark Governance

A benchmark is a predeclared comparator used to contextualize later historical results.

A benchmark is not proof of edge. It is not a target to optimize against after results are observed. It is not a justification for changing the strategy, protocol, windows, or partitions.

Benchmark selection must be documented before evaluation. Benchmark rationale must be documented before evaluation. Benchmark changes create a new experiment. A benchmark cannot be selected, replaced, or justified after observing results.

Conceptual benchmark examples include:

- Passive market exposure.
- Cash or flat exposure.
- Equal-weight asset universe.
- Buy-and-hold reference.
- Naive baseline strategy.
- Strategy-family baseline.

This block does not define concrete benchmarks for any strategy. It defines the governance requirement that benchmark choice must be explicit, versioned, justified, and frozen before evaluation.

## Evaluation Window Governance

Evaluation windows define the historical periods over which the strategy will be evaluated.

Window governance must document:

- Start dates.
- End dates.
- Market regimes considered.
- Coverage constraints.
- Declared data or universe limitations.
- Relationship to certified snapshot coverage.
- Relationship to partition definitions.

Windows must be selected before evaluation. Windows must not be modified after observing results. Changing windows creates a new experiment.

Window selection must not be used to hide known limitations, omit unfavorable regimes, or select favorable periods after inspection.

## Experiment Assumption Controls

Every assumption used in the protocol must come from one of:

- Strategy Specification.
- Assumptions Registry.
- Protocol Governance.

No implicit assumptions are allowed.

No hidden assumptions are allowed.

No undocumented assumptions are allowed.

Protocol assumptions must not change strategic intent, introduce new strategy logic, repair operationalization gaps, override temporal certification, or create frictions and execution assumptions reserved for Block 07.

Undocumented assumptions invalidate experimental reproducibility.

## Protocol Change Governance

A protocol change is any modification to a component that defines the experimental unit.

Examples include changes to:

- Benchmark.
- Dataset partition.
- Evaluation window.
- Strategy specification version.
- Snapshot version.
- Assumptions version.
- Experiment configuration.
- Execution assumptions, when introduced by future blocks.
- Protocol metadata.

Protocol changes never overwrite prior experiments. They create new experiments.

Prior experiment records must remain intact, even when a later protocol is improved, corrected, or rejected.

If a change is required because a defect is discovered, the original protocol must be marked according to future governance rather than silently edited.

## Failure Conditions

Block 06 must stop the experiment before execution when any of the following are confirmed or cannot be resolved:

- Missing traceability.
- Missing Strategy Specification reference.
- Missing certified snapshot reference.
- Missing assumptions registry reference.
- Missing benchmark rationale.
- Missing partition definition.
- Missing evaluation window definition.
- Undocumented assumptions.
- Partition leakage.
- Temporal governance violation.
- Protocol ambiguity.
- Unversioned inputs.
- Inconsistent specification.
- Benchmark selected after observing results.
- Partition boundary changed after observing results.
- Evaluation window changed after observing results.
- Protocol change attempts to overwrite a prior experiment.
- Protocol attempts to repair operationalization defects.
- Protocol attempts to create strategy assumptions not closed in Block 05.
- Protocol relies on future Block 07 frictions or execution assumptions before they are governed.

If a failure condition occurs, the experiment must not execute.

## Reproducibility Requirements

A protocol is reproducible only when an independent reviewer can reconstruct the experimental unit without relying on memory, hidden context, or mutable defaults.

Minimum reproducibility evidence includes:

- Experiment identifier.
- Protocol version.
- Strategy specification version.
- Snapshot version.
- Assumptions registry version.
- Benchmark version.
- Evaluation window definition.
- Partition definition.
- Experiment configuration.
- Input references.
- Assumptions used.
- Protocol definition.
- Timestamps or version markers.
- Reviewer or process identity, when formalized.

If these records are insufficient, the protocol cannot support an auditable experiment.

## Audit Trail Requirements

Every protocol decision must leave auditable evidence.

The audit trail must include:

- Experiment identifier.
- Protocol version.
- Strategy specification version.
- Snapshot version.
- Assumptions registry version.
- Benchmark definition and rationale.
- Partition definition.
- Evaluation window definition.
- Experiment configuration.
- Assumptions used.
- Protocol deviations.
- Failure findings.
- Change history.
- Reviewer or process identity, when formalized.
- Confirmation that no simulation, metrics, PnL, optimization, parameter tuning, robustness testing, falsification testing, frictions, execution logic, or result interpretation occurred in Block 06.

The audit trail must be sufficient for quant research governance, model risk management, internal audit, trading systems engineering, reproducibility review, and external technical due diligence.

## Relationship With Block 07

Block 07 receives:

- Experiment outputs from Block 06, meaning the frozen protocol artifacts and experiment definition, not simulation results.
- Experiment metadata.
- Protocol metadata.
- Audit trail.
- Assumptions context.

Block 07 may define execution and market-friction simulation only within the boundaries of the frozen experiment protocol.

Block 07 must not:

- Change the protocol.
- Redefine benchmarks.
- Alter partitions.
- Change evaluation windows.
- Reinterpret the Strategy Specification.
- Modify assumptions.
- Correct experiment failures.
- Select favorable execution assumptions to compensate for protocol defects.

If Block 07 detects protocol problems, it must return the process to Block 06. It must not repair protocol defects downstream.

## Governance Requirements

Block 06 must preserve:

- Strategy intent from Block 05.
- Temporal certification from Block 04.
- Snapshot identity from Block 03.
- Eligibility governance from Block 02.
- Assumption ownership and registry closure from Block 05.
- Reproducible experiment identity.

Block 06 must not authorize trading, paper trading, deployment, capital allocation, live execution, production risk controls, or edge claims.

## Protocol Integrity Principle

The purpose of the evaluation protocol is to ensure that evidence is generated under controlled, reproducible, and auditable conditions.

When result quality and protocol integrity conflict, protocol integrity takes precedence.

The system must reject invalid evidence rather than accept evidence generated under an invalid protocol.

## Explicit Non-Scope

Block 06 does not create a simulator.

Block 06 does not execute simulations.

Block 06 does not calculate metrics.

Block 06 does not create scorecards.

Block 06 does not calculate PnL.

Block 06 does not create trades.

Block 06 does not define frictions, fees, slippage, liquidity simulation, fills, or execution logic.

Block 06 does not define risk sizing, leverage approval, capital allocation, or production risk controls.

Block 06 does not optimize parameters.

Block 06 does not perform parameter tuning.

Block 06 does not perform model selection.

Block 06 does not create robustness testing.

Block 06 does not create falsification testing.

Block 06 does not approve deployment.

Block 06 does not approve live trading.

Block 06 does not create SQL.

Block 06 does not create executable schemas.

Block 06 does not create Python code.

Block 06 is a documentation and conceptual governance block that defines the experimental protocol required before downstream simulation assumptions and execution modeling can be governed.
