# 03 Backtesting Lifecycle

## Status

This lifecycle is conceptual for Block 01. Later blocks may formalize these states as schemas, contracts, tests, registries, or executable validation rules.

## Initial States

| State | Meaning |
| --- | --- |
| `backtest_stage_initialized` | 06 architecture exists as a documented stage. No execution capability is implied. |
| `eligible_for_operationalization` | A StrategyDossier has passed future 06 eligibility checks and may proceed toward temporal and operational review. |
| `not_eligible` | A StrategyDossier cannot enter 06 evaluation under the current eligibility contract. |
| `temporally_certified` | The data and feature snapshot has passed temporal admissibility and leakage baseline controls. |
| `temporally_certified_with_declared_limitations` | The snapshot passes temporal review only with explicit non-clean limitations that must be carried into later governance, including Block 11 where relevant. This state does not imply the limitation is harmless. |
| `temporal_integrity_failed` | The snapshot, features, timestamps, or availability assumptions fail temporal integrity controls. |
| `temporally_incomplete` | Required temporal review information is incomplete, so certification cannot be issued. |
| `temporal_metadata_missing` | Required event, availability, processing, feature generation, decision, execution, lag, or revision metadata is missing. |
| `temporal_availability_ambiguous` | The review cannot determine whether information was available at the simulated decision point. |
| `leakage_risk_detected` | Leakage risk is detected and unresolved, including possible label leakage or outcome-driven dataset construction. |
| `lookahead_risk_detected` | Lookahead risk is detected and unresolved, including possible use of future values or future-informed transformations. |
| `survivorship_bias_undeclared` | The asset universe appears retrospectively filtered by survival, future liquidity, future performance, future listing status, or future data completeness without declaration. |
| `snapshot_rejected_for_temporal_review_failure` | The snapshot is rejected because temporal review failed and cannot support operationalization. |
| `operationalized` | The StrategyDossier has been translated into a simulation specification with explicit 06 assumptions. |
| `operationalized_with_assumptions` | The simulation specification requires explicit 06 assumptions that are registered, justified, traceable, and judged non-material or non-thesis-changing. |
| `operationalized_with_material_assumptions` | The simulation specification requires material 06 assumptions that preserve strategic intent but must be carried into later protocol, robustness, and interpretation review. |
| `not_operationalizable` | The dossier cannot be converted into an honest simulation specification without unjustified material invention. |
| `insufficient_information` | Required operational information is absent and cannot be filled without unjustified assumptions. |
| `strategic_ambiguity_detected` | Multiple materially different strategy interpretations exist and cannot be resolved without changing or inventing strategy logic. |
| `conflicting_rules_detected` | Dossier rules conflict in a way that blocks deterministic operationalization. |
| `protocol_defined_pending_freeze` | The experiment protocol has been defined but has not yet been frozen for downstream execution assumptions. |
| `protocol_frozen` | The experiment and evaluation protocol has been defined before result inspection. |
| `protocol_invalid` | The experiment protocol contains missing, ambiguous, unversioned, leaking, or non-reproducible elements and cannot proceed. |
| `protocol_superseded_by_new_experiment` | A protocol change created a new experiment rather than overwriting the prior one. |
| `execution_friction_configured` | Execution and market-friction assumptions have been documented, versioned, and linked to the frozen protocol. |
| `execution_friction_invalid` | Execution or friction assumptions are missing, unrealistic, temporally inconsistent, untraceable, or selected after observing results. |
| `execution_friction_superseded_by_new_experiment` | A material friction change created a new experiment rather than overwriting prior evidence. |
| `risk_exposure_configured` | Risk, sizing, exposure, leverage, allocation, concentration, and portfolio assumptions have been documented, versioned, and linked to the frozen protocol and execution configuration. |
| `risk_exposure_invalid` | Risk or exposure assumptions are missing, unrealistic, untraceable, inconsistent, selected after observing results, or used to repair prior defects. |
| `risk_exposure_superseded_by_new_experiment` | A material risk change created a new experiment rather than overwriting prior evidence. |
| `returned_to_prior_block_pending_correction` | A downstream block detected an issue requiring correction by a prior owning block before evaluation can continue. |
| `simulation_ready` | All pre-simulation gates, including integrated assumption set validation, are complete and the simulation may execute under governed inputs. |
| `simulation_blocked` | Simulation cannot execute because required governed inputs, validation records, versions, or audit metadata are missing or inconsistent. |
| `simulation_failed` | Simulation execution started but failed due to deterministic execution, event trace, input consistency, or assumption consistency failure. |
| `simulation_executed` | A historical simulation has run under approved contracts. No favorable result is implied. |
| `performance_measured` | Metrics and diagnostics have been generated from governed Block 09 simulation artifacts. No interpretation, edge claim, robustness conclusion, or deployment readiness is implied. |
| `performance_measurement_invalid` | Performance measurement cannot proceed or cannot be accepted because required simulation outputs, metric lineage, benchmark references, reproducibility metadata, or version consistency are missing or invalid. |
| `robustness_review_in_progress` | Robustness, falsification, and anti-overfitting review has begun using governed Block 10 artifacts. No conclusion is implied. |
| `robustness_findings_recorded` | Robustness, falsification, fragility, overfitting, or inconclusive findings have been documented with lineage and audit evidence. No validation is implied. |
| `robustness_review_completed` | Required Block 11 challenge categories and falsification review have been completed and recorded. No proof of edge, deployment readiness, or trading authorization is implied. |
| `robustness_review_failed` | Block 11 cannot close because challenge scope, lineage, criteria, artifacts, or audit evidence are missing, inconsistent, selective, or invalid. |
| `falsified` | The evaluation met predefined falsification criteria. |
| `inconclusive` | The evaluation did not support a clear falsification or robustness judgment. |
| `not_robust` | Results were materially unstable, fragile, cost-sensitive, regime-dependent, or otherwise failed robustness checks. |
| `robust_pending_review` | Results passed defined robustness checks but still require governance review. No trading authorization is implied. |
| `closed_with_feedback` | The evaluation is closed and feedback has been recorded for governed handoff to 04 and 05. |

## Lifecycle Notes

`simulation_executed` does not imply a favorable result, valid edge, robustness, approval, paper trading authorization, live trading authorization, deployment readiness, or capital allocation.

`performance_measured` means governed simulation outputs have been described by versioned metrics and diagnostics. It does not imply edge, robustness, superiority, future profitability, strategy approval, paper trading authorization, live trading authorization, deployment readiness, or capital allocation.

`robustness_review_completed` means governed challenge review has been documented. It does not imply validation, confirmation of edge, future profitability, deployment readiness, paper trading authorization, live trading authorization, or capital allocation.

`operationalized` means the dossier has a historically evaluable specification. It does not mean the strategy is approved, profitable, validated, or eligible for trading.

`protocol_frozen` means the evaluation plan was fixed by an explicit freeze event before observing results. The freeze event must record reviewer or process identity, timestamp, protocol version, complete component definition, no result inspection, and locked partitions, windows, benchmarks, and assumptions.

`robust_pending_review` means the historical result passed the defined robustness checks for that protocol. It does not authorize trading, paper trading, deployment, leverage, or capital allocation.

## Blocking Conditions

If eligibility fails, the lifecycle must stop at `not_eligible`.

If temporal integrity fails, if temporal metadata is missing, if availability is ambiguous, if leakage or lookahead risk remains unresolved, if survivorship bias is undeclared, or if the snapshot is rejected for temporal review failure, the lifecycle must stop until the issues are resolved through governed upstream processes.

Only `temporally_certified` or `temporally_certified_with_declared_limitations` permits movement to operationalization. Any additional admissible temporal state must be explicitly added to this lifecycle and the decision log before Block 05 may accept it. Block 05 cannot introduce new feature timing exceptions; any unapproved timing exception must return to Block 04 for re-certification.

If operationalization requires unjustified assumptions, the lifecycle must stop at `not_operationalizable`.

If operationalization encounters insufficient information, material strategic ambiguity, conflicting rules, non-traceable operational rules, or assumption explosion, the lifecycle must stop before Block 06.

If the experiment protocol is missing traceability, contains undocumented assumptions, has partition leakage, has unversioned inputs, lacks benchmark rationale, attempts to overwrite a prior experiment, or is otherwise non-reproducible, the lifecycle must stop at `protocol_invalid`.

Any protocol change creates a new experiment and must not overwrite the prior protocol record.

Superseded experiments remain reportable, linked to successors, and visible to the Results Registry.

If a downstream block returns work to a prior block for correction, the lifecycle must record the source block, target block, reason for return, and successor experiment reference if a new experiment is created. This is metadata and governance, not authorization to modify upstream artifacts outside their owning process.

If execution or friction assumptions are undocumented, unrealistic, temporally inconsistent, untraceable, tuned from observed results, or depend on infinite liquidity, the lifecycle must stop at `execution_friction_invalid`.

Any material friction change creates a new experiment and must not overwrite prior evidence.

If risk or exposure assumptions are undocumented, unrealistic, untraceable, inconsistent with prior governed artifacts, tuned from observed results, or used to repair operationalization, protocol, or execution defects, the lifecycle must stop at `risk_exposure_invalid`.

Any material risk change creates a new experiment and must not overwrite prior evidence.

Before Block 09 may execute simulation, the integrated assumption set from Blocks 05-08 must be validated for contradictions, duplicate or conflicting assumptions, timing consistency, ownership clarity, version completeness, traceability completeness, and interaction risks.

If pre-simulation gates are incomplete, if integrated assumption validation fails, if governed inputs are unversioned or inconsistent, or if mutable external dependencies are required, the lifecycle must stop at `simulation_blocked` or `simulation_failed`.

If required Block 09 simulation outputs are missing, inconsistent, corrupted, unversioned, or unverifiable, or if metric lineage, benchmark references, reproducibility metadata, or metric definitions cannot be verified, the lifecycle must stop at `performance_measurement_invalid`.

If metrics are created after result inspection, if metric cherry-picking occurs, if missing simulation data is reconstructed, or if Block 10 attempts to repair simulation defects, the lifecycle must stop at `performance_measurement_invalid`.

If falsification criteria are absent, experiment lineage is unavailable, the assumptions registry is incomplete, robustness scope is undefined, upstream defects remain unresolved, evidence is contradictory and unresolved, or Block 11 attempts to optimize, repair, rerun, recalculate, or redesign, the lifecycle must stop at `robustness_review_failed`.

If Block 11 detects falsification, fragility, overfitting, or inconclusive evidence, the lifecycle must record the finding rather than repair the strategy, protocol, execution assumptions, risk assumptions, simulation outputs, or metrics.

If the protocol is changed after result inspection, the evaluation must be treated as compromised unless a future governance process explicitly restarts and re-freezes the protocol.
