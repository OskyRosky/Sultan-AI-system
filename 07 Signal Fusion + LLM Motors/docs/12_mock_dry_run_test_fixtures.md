# 07 Signal Fusion + LLM Motors - Mock and Dry-Run Test Fixtures

## 1. Purpose

Block 12 defines Mock and Dry-Run Test Fixtures for `07 Signal Fusion + LLM Motors`.

The purpose is to define synthetic fixture catalogs and dry-run scenario specifications that can test contract shape, schema compatibility, handoff paths, degradation behavior, rejection behavior, and replay paths without pretending to create empirical evidence.

Mock fixtures are not empirical evidence.

Dry-run fixtures are not validation.

Synthetic outputs cannot authorize Paper Trading.

Mock success does not create confidence.

Block 12 produces fixture definitions for documentation, schema validation, interface testing, and replay testing only.

## 2. Scope

This block covers:

- `MockDryRunFixtureCatalog` definition;
- `DryRunScenarioSpec` definition;
- fixture taxonomy;
- fixture metadata requirements;
- dry-run scenario schema;
- expected output schema;
- required synthetic labeling;
- framework-only fixture;
- partial empirical placeholder fixture;
- event shock fixture;
- conflicting motors fixture;
- missing Motor C fixture;
- degraded confidence fixture;
- Bull/Bear debate fixture;
- prohibited inference fixture;
- risk handoff blocked fixture;
- replay degraded and unavailable fixtures;
- negative contract violation fixtures;
- forbidden fixture behavior;
- audit trace requirements;
- relationship with 07-Block-13 Quality Gates;
- relationship with 07-Block-14 Stage Closure and Handoff to 08;
- relationship with `08 Risk Engine`.

V1 update: Stage 07 now includes a minimal executable Python dry-run under
`07 Signal Fusion + LLM Motors/src/` with tests under
`07 Signal Fusion + LLM Motors/tests/`.

The executable dry-run is limited to contract validation with synthetic mocks.
It does not process real data, does not call LLMs, does not create trading
signals, does not produce empirical evidence, does not create confidence, does
not authorize Paper Trading, and does not promote strategies.

This block does not create trading logic, Paper Trading, Live Trading,
execution, capital allocation, Risk Engine behavior, quality gates, or Block 13.

## 3. Non-Authority Reminder

Block 12 is non-authoritative.

Block 12 must not:

- approve trades;
- approve strategies;
- authorize Paper Trading;
- authorize Live Trading;
- create execution readiness;
- execute orders;
- allocate capital;
- relax risk limits;
- promote strategies;
- create empirical evidence;
- create backtesting evidence;
- create OOS validation;
- create walk-forward validation;
- create robustness evidence;
- create trading `confidence_score`;
- create `final_signal_confidence_score`;
- create downstream operational eligibility under Motor B `framework_only`;
- convert mocks into evidence;
- convert dry-run success into validation;
- convert fixture coverage into robustness;
- convert replay success into confidence;
- convert synthetic data into evidence;
- bypass `08 Risk Engine`.

Current Motor B state remains binding in every fixture and dry-run scenario:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

## 4. Relationship With Blocks 00-11

Block 00 defines stage non-authority rules and allows dry-run contract validation only.

Block 01 defines `synthetic_dry_run_only` input state and forbids treating synthetic inputs as evidence.

Block 02 defines Motor B adapter preservation rules and Motor B `framework_only` constraints.

Block 03 defines Motor A context and regime metadata boundaries.

Block 04 defines Motor C event classifier metadata and event severity boundaries.

Block 05 defines LLM safety, prompt metadata, validation, fallback, and prompt injection handling.

Block 06 defines `NormalizedSignalCandidate` and synthetic normalization rules.

Block 07 defines `DebateSummary`, `debate_balance_status`, and `prohibited_inference_flags`.

Block 08 defines `FusedSignalCandidate`, `fused_actionability_status`, and event precedence outcomes.

Block 09 defines `ConfidenceGovernanceResult` and final confidence blocking.

Block 10 defines `RiskHandoffPackage` and downstream eligibility routing.

Block 11 defines `Stage07AuditTrace` and replay metadata.

Block 12 defines dry-run fixture specifications that exercise those contracts. It does not redefine prior contracts or convert fixture success into evidence.

## 5. Definition Of MockDryRunFixtureCatalog

`MockDryRunFixtureCatalog` is a conceptual catalog of synthetic fixture scenarios for 07 contract validation.

It lists fixture IDs, fixture types, intended validation scope, expected degradation or rejection modes, forbidden downstream usage, and audit references.

`MockDryRunFixtureCatalog` is not a dataset.

It is not research evidence.

It is not backtesting evidence.

It is not strategy validation.

It is not Paper Trading authorization.

## 6. Definition Of DryRunScenarioSpec

`DryRunScenarioSpec` is a conceptual specification for one synthetic dry-run scenario.

It describes simulated input artifacts, expected normalized/debate/fusion/confidence/risk handoff/replay outcomes, expected missing evidence, expected blocking gaps, expected rejection or degradation reason, and required non-approval labels.

`DryRunScenarioSpec` is not a real market event, not real performance evidence, and not empirical validation.

## 6A. Minimal Executable Dry-Run Implementation

The V1 minimal executable dry-run is implemented as:

```text
src/contracts.py
src/motor_b_adapter.py
src/normalizer.py
src/fusion_engine.py
src/confidence_governance.py
src/risk_handoff.py
src/audit_trace.py
src/dry_run.py
```

Entry point:

```text
run_stage07_dry_run(mock_payload: dict | None = None) -> Stage07DryRunResult
```

The dry-run produces:

- `NormalizedMotorAInput`
- `NormalizedMotorBInput`
- `NormalizedMotorCInput`
- `NormalizedSignalCandidate`
- `FusedSignalCandidate`
- `ConfidenceGovernanceResult`
- `RiskHandoffPackage`
- `Stage07AuditTrace`

All outputs preserve:

```text
evidence_completeness_level = framework_only
empirical_results_available = false
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
paper_trading_ready = false
handoff_to_09 = blocked
downstream_operational_eligibility = blocked
strategy_promotion_status = not_promoted
```

The dry-run is V1 contract validation only. It is not evidence, signal
readiness, paper trading readiness, LLM production, or strategy promotion.

## 7. Fixture Taxonomy

Allowed fixture types are:

```text
contract_shape_fixture
framework_only_fixture
synthetic_partial_empirical_fixture
event_shock_fixture
conflicting_motors_fixture
missing_motor_fixture
degraded_confidence_fixture
debate_disagreement_fixture
prohibited_inference_fixture
risk_handoff_blocked_fixture
replay_degraded_fixture
replay_unavailable_fixture
negative_contract_violation_fixture
```

Rules:

- every fixture must be `synthetic_dry_run_only`;
- every fixture must carry `non_approval_statement`;
- every fixture must carry `forbidden_downstream_usage`;
- every fixture must carry `synthetic_status`;
- no fixture may be labeled empirical;
- no fixture may be used as trading evidence;
- no fixture may be used for Paper Trading or Live Trading;
- no fixture may create or fill `confidence_score`;
- no fixture may create or fill `final_signal_confidence_score`.

## 8. MockDryRunFixtureCatalog Schema

The conceptual schema is:

```text
MockDryRunFixtureCatalog
  fixture_catalog_id
  fixture_catalog_schema_version
  stage_id
  fixture_set_name
  fixture_set_purpose
  fixture_ids
  fixture_types
  synthetic_status
  allowed_usage
  forbidden_downstream_usage
  non_approval_statement
  source_contract_references
  related_block_references
  expected_validation_scope
  expected_failure_modes
  audit_references
  created_at
```

Allowed usage is limited to:

- documentation;
- schema validation;
- contract shape validation;
- interface testing;
- replay path testing;
- deterministic rule dry-run testing;
- audit rehearsal.

Forbidden downstream usage must remain explicit in the catalog.

## 9. DryRunScenarioSpec Schema

The conceptual schema is:

```text
DryRunScenarioSpec
  dry_run_scenario_id
  scenario_type
  scenario_name
  scenario_purpose
  synthetic_status
  input_artifacts_simulated
  source_contract_references
  expected_normalization_status
  expected_debate_status
  expected_fusion_status
  expected_confidence_status
  expected_risk_handoff_status
  expected_replay_status
  expected_missing_evidence
  expected_blocking_gaps
  expected_forbidden_downstream_usage
  expected_non_approval_statement
  expected_human_review_flag
  expected_rejection_or_degradation_reason
  allowed_usage
  prohibited_usage
  audit_references
  schema_version
```

Expected outputs must describe contract behavior only. They must not assert strategy profitability, expected return, drawdown, live behavior, execution quality, or future market performance.

## 10. Expected Output Schema

Each dry-run scenario must define expected outputs for the relevant path:

```text
DryRunExpectedOutput
  expected_normalized_signal_candidate_state
  expected_debate_summary_state
  expected_fused_signal_candidate_state
  expected_confidence_governance_result_state
  expected_risk_handoff_package_state
  expected_stage07_audit_trace_state
  expected_rejection_or_degradation_reason
  expected_forbidden_downstream_usage
  expected_non_approval_statement
  expected_human_review_flag
```

Expected output state must be compared against schema and boundary requirements only.

Passing expected output checks does not prove empirical validity, robustness, OOS performance, profitability, or operational readiness.

## 11. Required Synthetic Labeling

Every fixture and dry-run scenario must include:

```text
synthetic_status = synthetic_dry_run_only
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

When simulating the current Motor B state, the fixture must use:

```text
evidence_completeness_level = framework_only
```

When simulating future evidence-state shapes without real evidence, the fixture must use:

```text
evidence_completeness_level = synthetic_dry_run_only
```

or another explicitly synthetic placeholder status, never a real empirical label.

`forbidden_downstream_usage` must include:

- Paper Trading;
- Live Trading;
- execution;
- capital allocation;
- strategy promotion;
- confidence invention;
- empirical evidence replacement.

`non_approval_statement` must explicitly say the fixture is synthetic, dry-run-only, non-operational, and not trade approval.

## 12. Framework-Only Fixture

`framework_only_fixture` simulates the current Motor B state:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
missing_evidence = populated
blocking_gaps = populated
forbidden_downstream_usage = populated
synthetic_status = synthetic_dry_run_only
```

Expected result:

- `NormalizedSignalCandidate` preserves `framework_only`.
- `DebateSummary` acknowledges `framework_only`.
- `FusedSignalCandidate` is `non_actionable_framework_only`.
- `ConfidenceGovernanceResult` has `final_signal_confidence_score = null`.
- `RiskHandoffPackage` has `eligibility_status = ineligible_framework_only`.
- `Stage07AuditTrace` preserves the entire path.

The fixture must not imply that current Motor B has empirical evidence.

## 13. Partial Empirical Placeholder Fixture

`synthetic_partial_empirical_fixture` is a synthetic placeholder only.

It must not be interpreted as real partial empirical evidence.

It exists only to validate that future states can be represented by the schema.

It cannot unlock Paper Trading.

It cannot create confidence.

It cannot be used in research conclusions.

Expected result:

- evidence-related fields remain explicitly synthetic;
- `paper_trading_eligibility = blocked`;
- `downstream_operational_eligibility = blocked`;
- `confidence_score = null`;
- `final_signal_confidence_score = null`;
- `forbidden_downstream_usage` remains present;
- audit trace labels the scenario as synthetic placeholder.

## 14. Event Shock Fixture

`event_shock_fixture` simulates event-driven stress cases such as:

- exchange hack;
- stablecoin depeg;
- regulatory ban;
- protocol exploit;
- systemic crypto event.

Expected result:

- Motor C severity is high or critical.
- `event_precedence_outcome` may become `risk_suspend_candidate`, `require_human_review`, `degrade_candidate`, or `reject_candidate_due_to_event_risk`.
- No trade approval.
- No execution instruction.
- No confidence creation.
- `RiskHandoffPackage` routes to event risk review or rejection.
- `Stage07AuditTrace` preserves event source limitations and synthetic labels.

## 15. Conflicting Motors Fixture

`conflicting_motors_fixture` simulates:

- Motor A `trend_bullish`;
- Motor B `framework_only`;
- Motor C critical event;
- Bull favorable argument;
- Bear missing evidence argument.

Expected result:

- conflict is preserved;
- missing evidence dominates favorable context;
- critical event risk can degrade or suspend candidate handling;
- `framework_only` blocks operational eligibility;
- `paper_trading_eligibility = blocked`;
- `downstream_operational_eligibility = blocked`;
- `final_signal_confidence_score = null`;
- `RiskHandoffPackage` routes to review, rejection, or blocked handoff according to deterministic policy.

## 16. Missing Motor C Fixture

`missing_motor_fixture` for Motor C simulates:

- Motor C unavailable;
- event context unavailable;
- no imputation;
- no LLM speculation.

Expected result:

- missing Motor C is explicit;
- event context is unavailable, not assumed safe;
- no assumption of safe market;
- no synthetic LLM substitute is invented;
- downstream remains blocked if Motor B is `framework_only`;
- replay records missing Motor C as a limitation.

## 17. Degraded Confidence Fixture

`degraded_confidence_fixture` simulates:

- `confidence_status = confidence_not_available`;
- degraded classification confidence;
- conflicting sources;
- high uncertainty;
- missing OOS evidence;
- missing robustness evidence.

Expected result:

- `final_signal_confidence_score = null`;
- `final_signal_confidence_status` is blocked, degraded, or unavailable according to Block 09 policy;
- no confidence invention;
- human review may be required;
- missing confidence and evidence remain visible in audit trace.

## 18. Bull/Bear Debate Fixture

`debate_disagreement_fixture` must test:

- `bull_favorable`;
- `bear_favorable`;
- `balanced`;
- `unresolved`;
- `insufficient_arguments`;
- `unavailable`;
- `prohibited_inference_flags`.

Expected result:

- `debate_balance_status` is metadata only;
- disagreement scoring is not confidence scoring;
- prohibited inference flags route to rejection, degradation, or review;
- debate cannot override Motor B `framework_only`;
- `DebateSummary` remains argument metadata only.

## 19. Prohibited Inference Fixture

`prohibited_inference_fixture` must include simulated outputs with:

- `trade_approval_language_detected`;
- `paper_trading_authorization_detected`;
- `execution_language_detected`;
- `confidence_invention_detected`;
- `empirical_evidence_invention_detected`;
- `raw_input_usage_detected`;
- `prompt_injection_suspected`;
- `risk_engine_bypass_language_detected`.

Expected result:

- severe flags reject or degrade `DebateSummary`;
- `RiskHandoffPackage` rejects or routes to review;
- `Stage07AuditTrace` preserves the violation;
- no downstream approval;
- no confidence creation;
- no Risk Engine bypass.

## 20. Risk Handoff Blocked Fixture

`risk_handoff_blocked_fixture` must simulate a path where upstream artifacts are schema-valid but blocked by Motor B `framework_only`.

Expected result:

- `FusedSignalCandidate` remains non-actionable;
- `ConfidenceGovernanceResult` preserves null final confidence;
- `RiskHandoffPackage` has `eligibility_status = ineligible_framework_only`;
- required Risk Engine action routes to review, veto, or blocking gap handling, not approval;
- `non_approval_statement` remains explicit;
- `forbidden_downstream_usage` remains explicit.

## 21. Replay Degraded And Unavailable Fixtures

`replay_degraded_fixture` must test:

- missing artifact;
- missing timestamp;
- missing schema version;
- missing prompt metadata;
- model unavailable.

Expected result:

- `replay_status` is `replay_degraded_missing_artifact`, `replay_degraded_missing_timestamp`, `replay_degraded_missing_schema_version`, `replay_degraded_missing_prompt_metadata`, or `replay_degraded_model_unavailable`;
- replay failure does not create evidence;
- replay failure does not create confidence;
- replay failure preserves `non_approval_statement`.

`replay_unavailable_fixture` must test:

- missing source artifacts;
- contract violation;
- unversioned payload;
- integrity failure.

Expected result:

- `replay_status` is `replay_unavailable_missing_source_artifacts`, `replay_unavailable_contract_violation`, `replay_unavailable_unversioned_payload`, or `replay_rejected_integrity_failure`;
- replay unavailable status is passed as limitation;
- no downstream approval;
- no confidence creation.

## 22. Negative Contract Violation Fixtures

`negative_contract_violation_fixture` must simulate invalid payloads such as:

- missing `schema_version`;
- missing `non_approval_statement`;
- missing `forbidden_downstream_usage`;
- missing `synthetic_status`;
- non-null `confidence_score` without valid empirical evidence;
- non-null `final_signal_confidence_score` under `framework_only`;
- `paper_trading_eligibility` not blocked;
- direct execution request;
- direct capital allocation request;
- raw LLM output used as governed input.

Expected result:

- input is rejected or marked unavailable;
- downstream artifacts are not created except rejected audit records;
- severe violations route to human review or rejected handoff;
- audit trace preserves the violation and affected artifact IDs.

## 23. Forbidden Fixture Behavior

Fixtures cannot:

- prove strategy profitability;
- prove robustness;
- prove OOS validity;
- prove walk-forward performance;
- unlock Paper Trading;
- unlock Live Trading;
- generate real `confidence_score`;
- generate `final_signal_confidence_score`;
- replace missing evidence;
- close blocking gaps;
- remove `forbidden_downstream_usage`;
- bypass `08 Risk Engine`;
- create strategy promotion;
- create production readiness.

Any fixture that claims these outcomes is invalid and must be rejected as a contract violation.

## 24. Fixture Metadata Requirements

Every fixture must include:

- fixture ID;
- fixture type;
- fixture schema version;
- scenario purpose;
- simulated input artifact list;
- source contract references;
- related block references;
- `synthetic_status = synthetic_dry_run_only`;
- expected validation scope;
- expected failure mode when applicable;
- expected missing evidence;
- expected blocking gaps;
- expected forbidden downstream usage;
- expected non-approval statement;
- audit references;
- created_at.

Missing metadata must degrade, reject, or make the fixture unavailable for dry-run validation.

## 25. Audit Trace Requirements

Every dry-run scenario must be traceable through `Stage07AuditTrace` when replay testing is in scope.

The trace must preserve:

- fixture ID;
- scenario ID;
- simulated source artifact IDs;
- source contract references;
- source schema versions;
- synthetic status;
- expected and actual validation status when later executable tests exist;
- missing evidence;
- blocking gaps;
- forbidden downstream usage;
- non-approval statement;
- replay status;
- replay limitations.

Audit trace requirements do not make fixture results evidence.

## 26. Relationship With Block 13 Quality Gates

07-Block-13 Quality Gates will define quality gates.

Block 12 provides fixture scenarios to test whether quality gates can detect violations.

Passing fixtures does not close quality gates automatically.

Passing fixtures does not prove production readiness.

Passing fixtures does not prove strategy quality, robustness, OOS validity, replay completeness for real runs, or Risk Engine readiness.

## 27. Relationship With Block 14 Stage Closure

07-Block-14 Stage Closure and Handoff to 08 will close the stage.

Block 12 provides dry-run evidence of contract coverage only.

Block 12 does not provide empirical trading evidence.

Block 12 does not approve stage closure by itself.

Stage closure must preserve fixture limitations and synthetic labels.

## 28. Relationship With 08 Risk Engine

`08 Risk Engine` retains final authority over downstream eligibility, veto, promotion, risk limits, and operational decisions.

Fixtures are not submitted as trading evidence.

Fixtures may test handoff shape only.

Fixture success cannot force Risk Engine approval.

Fixture success cannot reduce Risk Engine review requirements.

Fixture success cannot bypass `08 Risk Engine`.

## 29. Explicit Prohibited Actions

Block 12 must not:

- implement trading logic;
- implement Paper Trading;
- implement Live Trading;
- create execution logic;
- create capital allocation;
- create Risk Engine;
- create executable fixtures;
- create JSON mock files;
- create YAML mock files;
- create Python tests;
- create Block 13;
- create quality gates;
- create stage closure;
- create Block 14;
- modify the Motor B Output Contract of 06;
- modify Blocks 00-11;
- redefine prior contracts;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- create downstream operational eligibility under `framework_only`;
- convert mocks into evidence;
- convert dry-run success into validation;
- convert fixture coverage into robustness;
- convert replay success into confidence;
- convert synthetic data into evidence;
- create a ML ensemble.

## 30. Block 12 Closure Criteria

Block 12 is closed when this document defines:

- Mock and Dry-Run Test Fixtures purpose;
- scope;
- non-authority rules;
- relationship with Blocks 00-11;
- `MockDryRunFixtureCatalog`;
- `DryRunScenarioSpec`;
- explicit statement that Mock fixtures are not empirical evidence;
- explicit statement that Dry-run fixtures are not validation;
- explicit statement that Synthetic outputs cannot authorize Paper Trading;
- explicit statement that Mock success does not create confidence;
- fixture taxonomy;
- fixture metadata requirements;
- dry-run scenario schema;
- expected output schema;
- required synthetic labeling;
- framework-only fixture;
- partial empirical placeholder fixture;
- event shock fixture;
- conflicting motors fixture;
- missing Motor C fixture;
- degraded confidence fixture;
- Bull/Bear debate fixture;
- prohibited inference fixture;
- risk handoff blocked fixture;
- replay degraded and unavailable fixtures;
- negative contract violation fixtures;
- forbidden fixture behavior;
- audit trace requirements;
- relationship with 07-Block-13 Quality Gates;
- relationship with 07-Block-14 Stage Closure and Handoff to 08;
- relationship with `08 Risk Engine`.

Closing Block 12 does not create executable fixtures, JSON/YAML mocks, Python tests, quality gates, Block 13, stage closure, Block 14, Risk Engine behavior, Paper Trading, Live Trading, execution logic, or capital allocation.
