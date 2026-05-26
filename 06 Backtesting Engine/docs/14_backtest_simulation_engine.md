# 14 Backtest Simulation Engine

## Purpose

Block 09 defines the Backtest Simulation Engine contract for 06 Backtesting Engine.

Its purpose is to govern how a historical simulation is executed from already-governed inputs without changing the strategy, protocol, execution assumptions, risk assumptions, or upstream records.

This block answers the question: how should a reproducible historical simulation be executed without modifying strategy, protocol, execution, or risk?

The simulation engine executes governed instructions.

It does not design strategy. It does not tune assumptions. It does not choose protocol. It does not interpret performance. It does not repair upstream defects.

Block 09 exists to produce a faithful, deterministic, auditable simulation trace. It does not exist to improve results.

## Simulation Engine Philosophy

Simulation is execution of already-governed instructions.

It is not protocol design.

It is not strategy design.

It is not performance interpretation.

A simulation can be valid and still produce poor results.

A simulation can produce attractive results and still be invalid if upstream gates fail.

The simulation engine must preserve the governed state it receives. It must not invent missing information, infer missing assumptions, choose between protocol versions, repair upstream defects, or alter execution and risk assumptions for convenience.

## Pre-Simulation Gate

Block 09 may begin only when all required upstream artifacts exist, are closed, and are traceable.

The required pre-simulation gate includes:

- Eligibility decision.
- Certified snapshot.
- Temporal certification.
- Operationalized strategy specification.
- Assumptions registry.
- Protocol freeze event.
- Execution friction configuration.
- Risk exposure configuration.
- Integrated assumption set validation.

Missing, unresolved, unversioned, or inconsistent upstream artifacts block simulation.

If any required upstream artifact is absent or unresolved, Block 09 must stop and return the process to the appropriate prior block or governance owner.

## Integrated Assumption Set Validation

Before simulation, Block 09 must validate the integrated assumption set from:

- Block 05 strategy and operationalization assumptions.
- Block 06 protocol assumptions.
- Block 07 execution assumptions.
- Block 08 risk assumptions.

The validation must confirm:

- No contradictions.
- No duplicate or conflicting assumptions.
- Timing consistency.
- Ownership clarity.
- Version completeness.
- Traceability completeness.
- No unresolved pending assumptions.
- Interaction risks reviewed.
- No protocol laundering.
- No execution and risk inconsistency.

If integrated assumption set validation fails, the simulation must not execute.

This validation is a gate, not a repair mechanism. Block 09 must not fix the assumption set.

## Simulation Input Contract

The minimum conceptual simulation inputs are:

- Strategy Specification version.
- Historical Snapshot reference.
- Temporal Certification record.
- Experiment Protocol version.
- Protocol Freeze record.
- Execution Configuration.
- Risk Configuration.
- Integrated Assumption Set.
- Audit metadata.

This contract defines required conceptual inputs only. It does not define technical schemas, classes, tables, SQL, storage formats, or executable interfaces.

## Deterministic Execution Requirements

The same governed inputs must produce the same simulation trace.

Deterministic execution requires:

- All inputs are versioned.
- All assumptions are versioned.
- Protocol freeze record is stable.
- Execution configuration is stable.
- Risk configuration is stable.
- Simulation logic version is identifiable when later formalized.
- Random elements, if ever allowed in future, are seeded and declared.
- Simulation does not depend on current system time except audit timestamp.
- Simulation does not depend on mutable external sources.

Non-determinism without declared governance invalidates the simulation.

Mutable external dependencies are not admissible during simulation execution.

## Event Model Governance

Block 09 must produce an auditable conceptual event trace when later implemented.

The minimum conceptual event categories are:

- `simulation_started`
- `signal_evaluated`
- `order_intent_created`
- `execution_assumption_applied`
- `fill_simulated`
- `position_opened`
- `position_updated`
- `position_closed`
- `risk_constraint_applied`
- `simulation_warning`
- `simulation_failure`
- `simulation_completed`

This block does not implement events. It defines governance expectations for future event records.

Events must be ordered, traceable to inputs and assumptions, reproducible, and sufficient for later audit reconstruction.

## Trade And Position State Governance

The simulation engine must produce conceptual traceability for:

- Simulated order intent.
- Simulated fill.
- Position state.
- Exposure state.
- Cash or capital state, if applicable.
- Rejected or blocked action.
- Reason codes.

Trade records are simulated artifacts.

They are not real trades.

They are not recommendations.

They are not execution instructions.

They do not authorize paper trading, live trading, broker routing, deployment, capital allocation, or production risk actions.

## Execution/Risk Consistency Requirements

Execution and risk behavior must remain internally consistent.

Requirements:

- Fill timing must align with risk exposure timing.
- Mark-to-market assumptions must align with execution assumptions.
- Risk constraints must apply according to configured timing.
- Execution assumptions cannot be overridden by the risk layer.
- Risk assumptions cannot alter fills.
- Simulated position state must reflect both execution outcomes and risk constraints without rewriting either.

If execution and risk assumptions are inconsistent, the simulation must fail or return to the appropriate prior block.

Block 09 must not choose a convenient interpretation to continue execution.

## Simulation Failure Conditions

Block 09 must stop before or during simulation when any of the following are confirmed or cannot be resolved:

- Missing protocol freeze.
- Missing integrated assumption validation.
- Failed integrated assumption validation.
- Unresolved pending assumptions.
- Inconsistent execution and risk timing.
- Unversioned inputs.
- Mutable external dependency.
- Missing audit metadata.
- Strategy Specification mismatch.
- Historical Snapshot mismatch.
- Temporal Certification mismatch.
- Protocol mismatch.
- Execution Configuration mismatch.
- Risk Configuration mismatch.
- Assumptions registry mismatch.
- Missing event trace requirements.
- Non-determinism without declared governance.
- Simulation attempts to repair upstream defects.
- Simulation requires assumptions not approved in Blocks 05-08.

If a failure condition occurs, the simulation output must be marked failed or blocked and must not proceed to Block 10 as valid simulation results.

## Simulation Output Artifacts

The conceptual output artifacts from Block 09 are:

- Simulation run record.
- Event log.
- Simulated trades.
- Simulated positions.
- Exposure trace.
- Assumption application trace.
- Warning or failure log.
- Reproducibility metadata.

Block 09 does not calculate metrics. It does not interpret performance. It does not produce a performance report.

Simulation outputs are raw governed simulation artifacts for later metric calculation and diagnostics in Block 10.

## Simulation Audit Trail

Every simulation attempt must leave auditable evidence.

The audit trail must include:

- Simulation identifier.
- Input versions.
- Protocol freeze record.
- Integrated assumption validation record.
- Execution configuration version.
- Risk configuration version.
- Event log reference.
- Reviewer or process identity, when formalized.
- Timestamp.
- Warnings and failures.
- Inputs checked.
- Assumptions checked.
- Categories reviewed and cleared.
- Unresolved issues, if any.
- Failure reason, if simulation failed.
- Confirmation that no strategy design, protocol selection, execution assumption tuning, risk assumption tuning, metrics, PnL interpretation, Sharpe, Sortino, drawdown, robustness testing, falsification testing, optimization, parameter search, paper trading, live trading, broker integration, or performance interpretation occurred in Block 09.

The audit trail must be sufficient for quant research governance, model risk management, internal audit, trading systems engineering, reproducibility review, and external technical due diligence.

## Relationship With Block 10

Block 10 receives:

- Simulation run record.
- Event log.
- Simulated trades.
- Simulated positions.
- Exposure trace.
- Reproducibility metadata.
- Warning or failure log.

Block 10 may calculate performance metrics and diagnostics only from governed simulation artifacts.

Block 10 must not:

- Modify trades.
- Modify positions.
- Alter simulation events.
- Repair simulation defects.
- Infer missing simulation data.
- Reinterpret execution assumptions.
- Reinterpret risk assumptions.
- Rerun simulation with different assumptions.

If Block 10 detects simulation defects, the process must return to Block 09 or the relevant upstream block. Block 10 must not repair simulation records downstream.

## Governance Requirements

Block 09 must preserve:

- Temporal certification from Block 04.
- Strategy specification and assumptions from Block 05.
- Frozen protocol and protocol lineage from Block 06.
- Execution configuration from Block 07.
- Risk configuration from Block 08.
- Integrated assumption validation.
- Experiment identity and versioning.
- Prior experiment records.

Block 09 must not authorize trading, paper trading, deployment, live execution, broker connectivity, capital allocation, production risk controls, leverage approval, or edge claims.

## Simulation Integrity Principle

The simulation engine must preserve the governed state of the experiment.

When simulation convenience and governed input integrity conflict, governed input integrity takes precedence.

The system must reject incomplete or inconsistent simulation inputs rather than generate attractive but invalid results.

## Explicit Non-Scope

Block 09 does not create Python code.

Block 09 does not create SQL.

Block 09 does not create an executable simulator.

Block 09 does not create a trading engine.

Block 09 does not create an execution engine.

Block 09 does not calculate metrics.

Block 09 does not interpret PnL.

Block 09 does not calculate Sharpe, Sortino, or drawdown.

Block 09 does not create robustness testing.

Block 09 does not create falsification testing.

Block 09 does not optimize parameters.

Block 09 does not perform parameter search.

Block 09 does not create live trading logic.

Block 09 does not create paper trading logic.

Block 09 does not create broker integrations.

Block 09 does not create numerical formulas.

Block 09 is a documentation and conceptual governance block that defines how historical simulation execution must preserve governed inputs and produce auditable simulation artifacts for Block 10.
