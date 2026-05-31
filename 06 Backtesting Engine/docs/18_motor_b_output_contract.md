# Motor B Output Contract

## 1. Purpose

The Motor B Output Contract is the formal handoff artifact produced by `06 Backtesting Engine` for downstream review by `07 Signal Fusion + LLM Motors` and `08 Risk Engine`.

The contract exists to summarize the evidence state of Motor B across:

- `04 Research Layer`;
- `05 Strategy Engine`;
- `06 Backtesting Engine`.

It preserves traceability from research evidence to strategy dossier to historical evaluation status. It also makes absence of evidence explicit, so downstream systems cannot infer confidence, robustness, validation, or approval from missing fields.

This contract is not a trading signal. It is not a paper trading approval. It is not live trading approval. It is not capital allocation approval.

## 2. Ownership and Boundaries

Ownership is fixed:

- `owner_stage`: `06 Backtesting Engine`
- `downstream_consumer_stage`: `07 Signal Fusion + LLM Motors`
- future governance consumer: `08 Risk Engine`

`07 Signal Fusion + LLM Motors` consumes this contract. It does not define the contract, reinterpret missing evidence, create confidence, or upgrade validation status.

`08 Risk Engine` may use this contract as a veto and review surface. Any contract with incomplete evidence, missing OOS validation, missing robustness review, missing temporal admissibility, or explicit blocking gaps may be blocked from operational promotion.

This contract does not authorize:

- paper trading;
- live trading;
- capital allocation;
- autonomous execution;
- production signal routing;
- risk bypass;
- risk limit relaxation.

## 3. Current Motor B State

Current Motor B state is:

```text
C. Output parcial con modulos ejecutables en 04/05, pero sin resultado final de backtesting.
```

Current evidence:

- `04 Research Layer` has an executable in-memory framework and synthetic tests, but no real persisted research outputs.
- `05 Strategy Engine` has executable conceptual modules for `StrategyDossier`, candidates, registry, quality gates, closure, and handoff, but its examples are fictitious mockups and are not derived from real research.
- `06 Backtesting Engine` is documentation/contract only at this stage. It has no Python engine, simulation, OOS report, walk-forward execution, robustness result, metrics artifact, or historical performance result.

Therefore, the current honest Motor B output must use:

```text
evidence_completeness_level = framework_only
simulation_status = backtest_not_implemented
oos_validation_status = oos_not_available
robustness_status = robustness_not_available
confidence_status = confidence_not_available
confidence_score = null
approval_status = not_approved
paper_trading_eligibility = blocked
```

## 4. Contract Scope

This contract covers:

- traceability from `04 Research Layer` to `05 Strategy Engine` to `06 Backtesting Engine`;
- evidence status;
- explicit absence-of-evidence states;
- downstream readiness classification;
- permitted and forbidden downstream usage;
- audit references;
- validation invariants;
- governance rules.

This contract does not cover:

- signal fusion;
- Motor A implementation;
- Motor C implementation;
- Risk Engine implementation;
- paper trading implementation;
- live trading implementation;
- invented confidence;
- executable backtesting;
- real trading signals;
- trade execution.

## 5. Schema Version Policy

Every Motor B Output Contract must include:

```text
schema_version
```

`schema_version` follows SemVer:

```text
MAJOR.MINOR.PATCH
```

### MAJOR

Increment MAJOR for incompatible changes:

- removing fields;
- changing required fields;
- changing the meaning of existing fields;
- renaming enum values;
- changing enum semantics;
- changing null evidence semantics;
- changing validation behavior in a way that breaks existing consumers.

### MINOR

Increment MINOR for compatible extensions:

- adding optional fields;
- adding compatible enum values;
- adding optional sections;
- adding metadata that existing consumers can ignore safely.

### PATCH

Increment PATCH for non-structural changes:

- documentation clarifications;
- example corrections;
- wording improvements;
- typo fixes;
- non-semantic description changes.

### Consumer Behavior

`07 Signal Fusion + LLM Motors` must reject incompatible MAJOR versions.

`08 Risk Engine` must reject or block unrecognized versions.

If `schema_version` is missing, the contract is invalid.

If `schema_version` is not valid SemVer, the contract is invalid.

If the contract uses a future unsupported version, the downstream consumer must route the contract to human review or block it.

## 6. Full Contract Structure

The full contract structure is:

```text
MotorBOutputContract
  identity
  research_evidence
  strategy_evidence
  backtesting_evidence
  confidence_and_approval
  evidence_completeness
  audit_governance
```

### identity

Required fields:

- `motor_b_output_id`
- `generated_at`
- `schema_version`
- `source_stage_references`
- `owner_stage`
- `downstream_consumer_stage`
- `audit_references`

### research_evidence

Required fields:

- `source_hypothesis_ids`
- `source_finding_ids`
- `research_dataset_references`
- `feature_informativeness_summary`
- `temporal_stability_summary`
- `regime_context`
- `regime_context_status`
- `research_execution_status`
- `research_limitations`

### strategy_evidence

Required fields:

- `strategy_dossier_id`
- `strategy_handoff_status`
- `candidate_id`
- `candidate_status`
- `candidate_family`
- `signal_ids`
- `rule_summary`
- `registry_status`
- `quality_gate_status`
- `falsification_references`
- `strategy_limitations`

### backtesting_evidence

Required fields:

- `backtest_eligibility_status`
- `temporal_admissibility_status`
- `historical_snapshot_status`
- `simulation_status`
- `execution_friction_status`
- `performance_metrics_status`
- `backtest_result_summary`
- `oos_validation_status`
- `oos_validation_report`
- `walk_forward_status`
- `walk_forward_summary`
- `robustness_status`
- `overfitting_status`
- `falsification_status`
- `backtest_limitations`

### confidence_and_approval

Required fields:

- `confidence_score`
- `confidence_status`
- `approval_status`
- `non_approval_statement`
- `risk_engine_required_action`
- `paper_trading_eligibility`

### evidence_completeness

Required fields:

- `evidence_completeness_level`
- `missing_evidence`
- `blocking_gaps`
- `allowed_downstream_usage`
- `forbidden_downstream_usage`

### audit_governance

Required fields:

- `immutable_inputs`
- `reproducibility_notes`
- `schema_validation_status`
- `contract_generation_mode`
- `human_review_status`
- `reviewer_notes`

## 7. Minimum Viable Motor B Output Contract

The minimum viable Motor B Output Contract is the smallest payload that `07 Signal Fusion + LLM Motors` can consume honestly when evidence is unavailable, not evaluated, not implemented, or framework-only.

The minimum contract must include:

- `motor_b_output_id`
- `schema_version`
- `generated_at`
- `owner_stage`
- `downstream_consumer_stage`
- `source_stage_references`
- `strategy_dossier_id`
- `strategy_handoff_status`
- `candidate_id`
- `candidate_status`
- `regime_context`
- `regime_context_status`
- `research_execution_status`
- `backtest_eligibility_status`
- `simulation_status`
- `oos_validation_status`
- `robustness_status`
- `confidence_status`
- `confidence_score`
- `evidence_completeness_level`
- `approval_status`
- `paper_trading_eligibility`
- `allowed_downstream_usage`
- `forbidden_downstream_usage`
- `missing_evidence`
- `blocking_gaps`
- `audit_references`
- `non_approval_statement`

### Fields That Must Never Be Omitted

The following fields must always exist:

- `motor_b_output_id`
- `schema_version`
- `generated_at`
- `owner_stage`
- `downstream_consumer_stage`
- `source_stage_references`
- `research_execution_status`
- `strategy_handoff_status`
- `candidate_status`
- `regime_context_status`
- `backtest_eligibility_status`
- `simulation_status`
- `oos_validation_status`
- `robustness_status`
- `confidence_status`
- `confidence_score`
- `evidence_completeness_level`
- `approval_status`
- `paper_trading_eligibility`
- `allowed_downstream_usage`
- `forbidden_downstream_usage`
- `missing_evidence`
- `blocking_gaps`
- `audit_references`
- `non_approval_statement`

### Fields That May Be Null

The following fields may be `null`, but only when paired with explicit status:

- `strategy_dossier_id`
- `candidate_id`
- `regime_context`
- `confidence_score`

Examples:

```text
strategy_dossier_id = null
strategy_handoff_status = dossier_not_available
```

```text
candidate_id = null
candidate_status = candidate_not_available
```

```text
regime_context = null
regime_context_status = regime_context_not_available
```

```text
confidence_score = null
confidence_status = confidence_not_available
```

### Why The Minimum Contract Is Sufficient

The minimum contract tells `07`:

- which schema version it received;
- who owns the contract;
- what upstream stages are represented;
- whether a dossier exists;
- whether a candidate exists;
- whether regime context exists;
- whether research was executed;
- whether backtesting was implemented or executed;
- whether OOS validation exists;
- whether robustness review exists;
- whether confidence is available;
- whether paper trading is blocked;
- what downstream usage is allowed;
- what downstream usage is forbidden.

This prevents `07` from inventing evidence or interpreting missing data as neutral, safe, or sufficient.

## 8. Evidence Completeness Levels

Allowed `evidence_completeness_level` values:

```text
framework_only
partial_empirical
backtest_validated
oos_validated
```

### framework_only

Framework and contracts exist, but no complete empirical chain exists.

This is the current state.

Required implications:

- `paper_trading_eligibility = blocked`
- `confidence_status = confidence_not_available`
- `confidence_score = null`
- `forbidden_downstream_usage` includes `paper_trading`, `live_trading`, `capital_allocation`, and `performance_claims`

### partial_empirical

Some real research or strategy artifacts exist, but historical evaluation remains incomplete.

This does not authorize paper trading or capital allocation.

### backtest_validated

A governed backtest exists with traceable historical snapshot, temporal admissibility, simulation record, metrics artifact, and audit references.

This does not equal trading approval. It does not authorize paper trading, live trading, or capital allocation by itself.

### oos_validated

Out-of-sample evidence exists under governed protocol.

This still requires `08 Risk Engine` review and may require human review before any paper trading consideration.

## 9. Explicit Null Evidence Semantics

`null` is valid only when the related status explicitly states why evidence is unavailable.

Missing evidence must be represented as known absence, not silent absence.

Valid examples:

```text
strategy_dossier_id = null
strategy_handoff_status = dossier_not_available
```

```text
candidate_id = null
candidate_status = candidate_not_available
```

```text
regime_context = null
regime_context_status = regime_context_not_available
```

```text
confidence_score = null
confidence_status = confidence_not_available
```

Invalid examples:

```text
strategy_dossier_id = null
```

```text
confidence_score = null
```

These are invalid because the downstream consumer cannot distinguish unavailable evidence from an accidental omission.

## 10. Required Enums and Status Values

### evidence_completeness_level

```text
framework_only
partial_empirical
backtest_validated
oos_validated
```

### confidence_status

```text
confidence_not_available
confidence_not_computable
confidence_computed_from_backtest
confidence_computed_from_oos
confidence_rejected_due_to_incomplete_evidence
```

### approval_status

```text
not_approved
not_evaluated
documentation_only
pending_human_review
rejected
approved_for_research_only
```

### backtest_eligibility_status

```text
not_evaluated
eligible_for_backtest_evaluation
not_eligible_missing_information
not_eligible_missing_traceability
not_eligible_governance_failure
not_eligible_candidate_ambiguity
not_eligible_internal_inconsistency
not_eligible_other
```

### simulation_status

```text
backtest_not_implemented
backtest_not_executed
simulation_blocked
simulation_failed
simulation_executed
simulation_result_invalid
```

### oos_validation_status

```text
oos_not_available
oos_not_executed
oos_passed
oos_failed
oos_inconclusive
oos_invalid
```

### robustness_status

```text
robustness_not_available
robustness_not_executed
robust_result
fragile_result
falsified_result
overfit_result
inconclusive_result
robustness_review_failed
```

### paper_trading_eligibility

```text
blocked
not_evaluated
requires_risk_engine_review
requires_human_review
eligible_for_future_review
```

### allowed_downstream_usage

```text
design_reference_only
documentation_review
contract_validation
simulation_with_mock_inputs_only
signal_fusion_dry_run
offline_research
human_review
paper_trading_with_full_evidence
```

### forbidden_downstream_usage

```text
paper_trading
paper_trading_without_oos
live_trading
capital_allocation
autonomous_execution
production_signal_routing
risk_limit_relaxation
risk_bypass
confidence_generation
strategy_promotion
execution_signal_generation
performance_claims
```

### human_review_status

```text
human_review_not_requested
human_review_required
human_review_in_progress
human_review_passed
human_review_rejected
```

### schema_validation_status

```text
schema_valid
schema_invalid
schema_valid_governance_blocked
```

### contract_generation_mode

```text
contract_generated_from_documentation
contract_generated_from_mockups
contract_generated_from_real_artifacts
contract_generated_from_mixed_sources
```

### Additional Availability Status Values

```text
dossier_not_available
dossier_mock_only
dossier_prepared_pending_final_audit
candidate_not_available
candidate_mock_only
candidate_conceptual_only
candidate_available
regime_context_not_available
regime_context_framework_only
regime_context_available
regime_context_real_empirical
research_not_executed
research_executed_partial
research_output_not_persisted
documentation_only
temporal_admissibility_not_certified
falsification_not_executed
walk_forward_not_available
robustness_not_available
confidence_not_available
metrics_not_available
metrics_available
not_approved
```

## 11. Validation Invariants

Validation invariants are rules that a future schema or Pydantic model can check automatically.

Required invariants:

- `schema_version` is required.
- `schema_version` must follow SemVer.
- `owner_stage` must equal `06 Backtesting Engine`.
- `downstream_consumer_stage` must include `07 Signal Fusion + LLM Motors`.
- If `confidence_status = confidence_not_available`, then `confidence_score = null`.
- If `confidence_score` exists, it must be between `0.0` and `1.0`.
- If `confidence_score` exists, `confidence_status` must not be `confidence_not_available`.
- If `evidence_completeness_level = framework_only`, then `paper_trading_eligibility = blocked`.
- If there is no real OOS evidence, `oos_validation_status` cannot be `oos_passed`.
- If `simulation_status = backtest_not_implemented`, then `backtest_result_summary.status = backtest_not_implemented`.
- If `simulation_status` is `backtest_not_implemented` or `backtest_not_executed`, then `performance_metrics_status` cannot be `metrics_available`.
- If `temporal_admissibility_status = temporal_admissibility_not_certified`, then `simulation_status` cannot be `simulation_executed`.
- If `strategy_handoff_status = dossier_mock_only`, then `approval_status` cannot be `approved_for_research_only`.
- If `robustness_status = robustness_not_available`, then `risk_engine_required_action` must include `block_or_require_review`.
- If `paper_trading_eligibility = blocked`, then `allowed_downstream_usage` cannot include `paper_trading_with_full_evidence`.
- `forbidden_downstream_usage` must include `paper_trading`, `live_trading`, and `capital_allocation` when `evidence_completeness_level` is `framework_only` or `partial_empirical`.
- Any field without evidence must use an explicit not-available, not-evaluated, not-executed, or not-implemented status.

These invariants validate internal consistency. They do not authorize downstream promotion.

## 12. Governance Rules

Governance rules are policy and promotion rules. They may require Risk Engine review, human review, or process-level enforcement even when the schema is technically valid.

Required governance rules:

- `07 Signal Fusion + LLM Motors` may consume incomplete contracts only for design, documentation review, dry-run, offline research, or interface validation.
- `07` must not convert `framework_only` into an operational signal.
- `07` must not generate confidence when `confidence_status = confidence_not_available`.
- `07` must not promote contracts derived from mockups.
- `08 Risk Engine` must block contracts without real OOS evidence before Paper Trading.
- No `framework_only` or `partial_empirical` contract may enable capital allocation.
- No contract derived from mockups may enable strategy promotion.
- Human review may be required even when the contract is technically schema-valid.
- Live trading is prohibited by this contract.
- Capital allocation is prohibited by this contract.
- Paper Trading requires full evidence, Risk Engine review, and any required human review.

## 13. Downstream Usage

Allowed downstream usage values:

```text
design_reference_only
documentation_review
contract_validation
simulation_with_mock_inputs_only
signal_fusion_dry_run
offline_research
human_review
paper_trading_with_full_evidence
```

`paper_trading_with_full_evidence` is a future value. It does not apply to the current `framework_only` state. Even when the value becomes available, it still requires `08 Risk Engine` review and may require human review.

Forbidden downstream usage values:

```text
paper_trading
paper_trading_without_oos
live_trading
capital_allocation
autonomous_execution
production_signal_routing
risk_limit_relaxation
risk_bypass
confidence_generation
strategy_promotion
execution_signal_generation
performance_claims
```

For `framework_only`, all operational and promotional forbidden usages apply, including:

- `paper_trading`
- `paper_trading_without_oos`
- `live_trading`
- `capital_allocation`
- `autonomous_execution`
- `production_signal_routing`
- `risk_bypass`
- `confidence_generation`
- `strategy_promotion`
- `execution_signal_generation`
- `performance_claims`

## 14. Example Payloads

These examples are conceptual and non-executable. They do not represent real evidence.

### Current framework_only State

```yaml
motor_b_output_id: motor-b-framework-only-001
schema_version: 1.0.0
generated_at: "2026-05-31T00:00:00Z"
owner_stage: 06 Backtesting Engine
downstream_consumer_stage:
  - 07 Signal Fusion + LLM Motors
  - 08 Risk Engine
source_stage_references:
  - 04 Research Layer
  - 05 Strategy Engine
  - 06 Backtesting Engine
strategy_dossier_id: null
strategy_handoff_status: dossier_not_available
candidate_id: null
candidate_status: candidate_not_available
regime_context: null
regime_context_status: regime_context_not_available
research_execution_status: research_not_executed
backtest_eligibility_status: not_evaluated
simulation_status: backtest_not_implemented
oos_validation_status: oos_not_available
robustness_status: robustness_not_available
confidence_status: confidence_not_available
confidence_score: null
evidence_completeness_level: framework_only
approval_status: not_approved
paper_trading_eligibility: blocked
allowed_downstream_usage:
  - design_reference_only
  - documentation_review
  - contract_validation
  - simulation_with_mock_inputs_only
  - signal_fusion_dry_run
  - offline_research
  - human_review
forbidden_downstream_usage:
  - paper_trading
  - paper_trading_without_oos
  - live_trading
  - capital_allocation
  - autonomous_execution
  - production_signal_routing
  - risk_limit_relaxation
  - risk_bypass
  - confidence_generation
  - strategy_promotion
  - execution_signal_generation
  - performance_claims
missing_evidence:
  - research_not_executed
  - research_output_not_persisted
  - dossier_not_available
  - backtest_not_implemented
  - oos_not_available
  - walk_forward_not_available
  - robustness_not_available
  - confidence_not_available
blocking_gaps:
  - No real research output has been executed and persisted.
  - No real StrategyDossier derived from real research exists.
  - No backtesting engine or historical result exists.
audit_references:
  - 04 Research Layer/docs/11_research_closure.md
  - 05 Strategy Engine/docs/35_strategy_engine_framework_closure.md
  - 06 Backtesting Engine/README.md
non_approval_statement: This contract is framework-only and blocks paper trading, live trading, capital allocation, confidence generation, and performance claims.
```

### Future partial_empirical State

```yaml
motor_b_output_id: motor-b-partial-empirical-example
schema_version: 1.0.0
evidence_completeness_level: partial_empirical
research_execution_status: research_executed_partial
strategy_handoff_status: dossier_prepared_pending_final_audit
simulation_status: backtest_not_executed
oos_validation_status: oos_not_available
robustness_status: robustness_not_available
confidence_status: confidence_not_available
confidence_score: null
paper_trading_eligibility: blocked
allowed_downstream_usage:
  - design_reference_only
  - contract_validation
  - signal_fusion_dry_run
  - offline_research
  - human_review
forbidden_downstream_usage:
  - paper_trading
  - paper_trading_without_oos
  - live_trading
  - capital_allocation
  - confidence_generation
  - strategy_promotion
  - performance_claims
non_approval_statement: Partial empirical evidence does not authorize promotion or paper trading.
```

### Future backtest_validated State

```yaml
motor_b_output_id: motor-b-backtest-validated-example
schema_version: 1.0.0
evidence_completeness_level: backtest_validated
backtest_eligibility_status: eligible_for_backtest_evaluation
simulation_status: simulation_executed
oos_validation_status: oos_not_executed
robustness_status: robustness_not_executed
confidence_status: confidence_computed_from_backtest
confidence_score: 0.42
paper_trading_eligibility: requires_risk_engine_review
allowed_downstream_usage:
  - design_reference_only
  - documentation_review
  - contract_validation
  - offline_research
  - human_review
forbidden_downstream_usage:
  - paper_trading_without_oos
  - live_trading
  - capital_allocation
  - autonomous_execution
  - production_signal_routing
  - risk_bypass
non_approval_statement: Backtest validation alone does not authorize paper trading, live trading, or capital allocation.
```

### Future oos_validated State

```yaml
motor_b_output_id: motor-b-oos-validated-example
schema_version: 1.0.0
evidence_completeness_level: oos_validated
backtest_eligibility_status: eligible_for_backtest_evaluation
simulation_status: simulation_executed
oos_validation_status: oos_passed
robustness_status: robust_result
confidence_status: confidence_computed_from_oos
confidence_score: 0.61
paper_trading_eligibility: requires_risk_engine_review
allowed_downstream_usage:
  - design_reference_only
  - documentation_review
  - contract_validation
  - offline_research
  - human_review
  - paper_trading_with_full_evidence
forbidden_downstream_usage:
  - live_trading
  - capital_allocation
  - autonomous_execution
  - risk_bypass
non_approval_statement: OOS validation still requires Risk Engine review and any required human review before paper trading can be considered.
```

## 15. Future Implementation Recommendation

The future executable implementation should use Pydantic models with strict enums and model-level validators.

Recommended future locations:

```text
06 Backtesting Engine/contracts/motor_b_output_contract.py
06 Backtesting Engine/tests/test_motor_b_output_contract.py
```

Long-term package location after repository consolidation:

```text
src/sultan/backtesting/contracts/motor_b_output_contract.py
```

Future implementation should include:

- strict enum validation;
- SemVer validation for `schema_version`;
- cross-field validation invariants;
- JSON serialization;
- fixture examples for `framework_only`, `partial_empirical`, `backtest_validated`, and `oos_validated`;
- explicit governance-blocked status support.

No implementation is created in this documentation block.

## 16. Risks if This Contract Is Missing

If this contract is missing:

- `07 Signal Fusion + LLM Motors` may treat documentation as evidence.
- Downstream components may invent confidence.
- Mock dossiers may leak into strategy promotion logic.
- `08 Risk Engine` lacks a clear veto surface.
- Paper Trading may be discussed before OOS validation and robustness review exist.
- Missing evidence may be interpreted as neutral rather than blocking.
- Traceability from `04 -> 05 -> 06 -> 07` may break.
- Audit-first governance may be weakened before operational stages are built.

The Motor B Output Contract is therefore a required boundary before `07 Signal Fusion + LLM Motors` can consume Motor B safely.
