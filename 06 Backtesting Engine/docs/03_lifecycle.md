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
| `simulation_executed` | A historical simulation has run under approved contracts. No favorable result is implied. |
| `falsified` | The evaluation met predefined falsification criteria. |
| `inconclusive` | The evaluation did not support a clear falsification or robustness judgment. |
| `not_robust` | Results were materially unstable, fragile, cost-sensitive, regime-dependent, or otherwise failed robustness checks. |
| `robust_pending_review` | Results passed defined robustness checks but still require governance review. No trading authorization is implied. |
| `closed_with_feedback` | The evaluation is closed and feedback has been recorded for governed handoff to 04 and 05. |

## Lifecycle Notes

`simulation_executed` does not imply a favorable result, valid edge, robustness, approval, paper trading authorization, live trading authorization, deployment readiness, or capital allocation.

`operationalized` means the dossier has a historically evaluable specification. It does not mean the strategy is approved, profitable, validated, or eligible for trading.

`protocol_frozen` means the evaluation plan was fixed before observing results. This status exists to reduce outcome-driven changes, comparison switching, and parameter mining.

`robust_pending_review` means the historical result passed the defined robustness checks for that protocol. It does not authorize trading, paper trading, deployment, leverage, or capital allocation.

## Blocking Conditions

If eligibility fails, the lifecycle must stop at `not_eligible`.

If temporal integrity fails, if temporal metadata is missing, if availability is ambiguous, if leakage or lookahead risk remains unresolved, if survivorship bias is undeclared, or if the snapshot is rejected for temporal review failure, the lifecycle must stop until the issues are resolved through governed upstream processes.

Only `temporally_certified` or `temporally_certified_with_declared_limitations` permits movement to operationalization. Any additional admissible temporal state must be explicitly added to this lifecycle and the decision log before Block 05 may accept it. Block 05 cannot introduce new feature timing exceptions; any unapproved timing exception must return to Block 04 for re-certification.

If operationalization requires unjustified assumptions, the lifecycle must stop at `not_operationalizable`.

If operationalization encounters insufficient information, material strategic ambiguity, conflicting rules, non-traceable operational rules, or assumption explosion, the lifecycle must stop before Block 06.

If the experiment protocol is missing traceability, contains undocumented assumptions, has partition leakage, has unversioned inputs, lacks benchmark rationale, attempts to overwrite a prior experiment, or is otherwise non-reproducible, the lifecycle must stop at `protocol_invalid`.

Any protocol change creates a new experiment and must not overwrite the prior protocol record.

If execution or friction assumptions are undocumented, unrealistic, temporally inconsistent, untraceable, tuned from observed results, or depend on infinite liquidity, the lifecycle must stop at `execution_friction_invalid`.

Any material friction change creates a new experiment and must not overwrite prior evidence.

If risk or exposure assumptions are undocumented, unrealistic, untraceable, inconsistent with prior governed artifacts, tuned from observed results, or used to repair operationalization, protocol, or execution defects, the lifecycle must stop at `risk_exposure_invalid`.

Any material risk change creates a new experiment and must not overwrite prior evidence.

If the protocol is changed after result inspection, the evaluation must be treated as compromised unless a future governance process explicitly restarts and re-freezes the protocol.
