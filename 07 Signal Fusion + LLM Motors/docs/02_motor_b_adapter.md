# 07 Signal Fusion + LLM Motors - Motor B Adapter

## 1. Purpose

Block 02 defines how `07 Signal Fusion + LLM Motors` conceptually adapts the Motor B Output Contract produced by `06 Backtesting Engine` into a normalized Motor B input shape for later 07 blocks.

The adapter exists to preserve Motor B input state, missing evidence, blocking gaps, confidence limitations, paper trading restrictions, non-approval status, non-approval statements, and `forbidden_downstream_usage` before any Signal Candidate Normalization or Signal Fusion work begins.

This block is documentary and contractual only. It does not implement Python code, parsing, validation, signal normalization, fusion, confidence aggregation, trading logic, or risk handoff.

## 2. Scope

This block covers:

- source contract reference;
- required preserved fields;
- allowed derived fields;
- prohibited derived fields;
- normalized Motor B input schema;
- adapter status taxonomy;
- framework-only degradation rules;
- missing evidence propagation;
- blocking gaps propagation;
- confidence preservation;
- forbidden downstream usage propagation;
- mock and synthetic input handling;
- relationship with later 07 blocks and `08 Risk Engine`.

This block does not cover:

- executable Motor B Adapter implementation;
- Signal Candidate Normalization;
- Bull/Bear Debate;
- Deterministic Signal Fusion;
- Confidence Aggregation;
- Motor A Context Layer;
- Motor C Event Classifier;
- LLM prompting rules;
- Risk Handoff;
- Paper Trading;
- Live Trading;
- execution logic;
- capital allocation.

## 3. Relationship With Block 00 And Block 01

Block 00 established that 07 has no authority to approve trades, authorize Paper Trading, allocate capital, override `08 Risk Engine`, invent `confidence_score`, or reinterpret missing evidence.

Block 01 established the input state model:

```text
accepted
rejected
degraded
unavailable
synthetic_dry_run_only
```

Block 02 specializes those rules for Motor B.

Input adaptation means no trade approval.

Input adaptation means no Paper Trading approval.

Input adaptation means no confidence generation.

Accepted input means only contract-consumable input. It does not mean an approved signal.

## 4. Source Contract Reference

The source contract is:

```text
06 Backtesting Engine/docs/18_motor_b_output_contract.md
```

The Motor B Output Contract belongs to `06 Backtesting Engine`.

Stage 07 consumes the contract, references it, and adapts its contents into a 07-internal normalized shape. Stage 07 must not redefine the Motor B Output Contract, change its semantics, remove restrictions, or upgrade evidence state.

## 5. Current Motor B State

The current mandatory Motor B state is:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

This means:

- `04 Research Layer` has framework tools and synthetic tests, but no real persisted research output.
- `05 Strategy Engine` has strategy candidate and dossier framework objects, but examples are mockups and not real approved strategies.
- `06 Backtesting Engine` is currently framework/director/documentation only, not a productive Python backtesting engine.
- There is no real backtest, OOS validation, walk-forward execution, robustness result, or historical performance result.

The adapter must preserve this state exactly until a later governed Motor B Output Contract instance provides real evidence.

## 6. Normalized Motor B Input Schema

The conceptual normalized Motor B input schema is:

```text
NormalizedMotorBInput
  motor_b_input_id
  source_contract_path
  source_contract_version
  source_stage
  source_stage_status
  strategy_candidate_id
  strategy_family
  asset
  timeframe
  horizon
  signal_direction
  evidence_completeness_level
  backtest_status
  oos_status
  walk_forward_status
  robustness_status
  paper_trading_eligibility
  confidence_status
  confidence_score
  approval_status
  non_approval_statement
  missing_evidence
  blocking_gaps
  forbidden_downstream_usage
  allowed_usage_within_07
  adapter_status
  adapter_limitations
  audit_references
  created_at
  schema_version
```

### Field Meaning

- `motor_b_input_id`: stable identifier for the normalized adapter record.
- `source_contract_path`: path to the consumed Motor B Output Contract.
- `source_contract_version`: schema version from the Motor B Output Contract.
- `source_stage`: expected to include `06 Backtesting Engine`.
- `source_stage_status`: current status of the source stage, such as `documentation_only` or later governed states.
- `strategy_candidate_id`: candidate reference if available; null only with explicit unavailable status.
- `strategy_family`: strategy family if available; must not be invented.
- `asset`: scoped asset if available; must not be invented.
- `timeframe`: scoped timeframe if available; must not be invented.
- `horizon`: forecast or evaluation horizon if available; must not be invented.
- `signal_direction`: directional indication if contractually present; must not be invented.
- `evidence_completeness_level`: preserved from source contract.
- `backtest_status`: mapped from source simulation/backtest state.
- `oos_status`: mapped from source OOS validation state.
- `walk_forward_status`: mapped from source walk-forward state.
- `robustness_status`: preserved or mapped from source robustness state.
- `paper_trading_eligibility`: preserved from source contract.
- `confidence_status`: preserved from source contract.
- `confidence_score`: preserved from source contract, including null.
- `approval_status`: preserved from the Motor B Output Contract of 06; it must retain the source non-approval state and must not be converted into trading approval, promotion, authorization, or downstream eligibility by 07.
- `non_approval_statement`: preserved from the Motor B Output Contract of 06; it must retain the explicit statement that Motor B output does not constitute trading approval and must not be weakened or reworded to enable trading.
- `missing_evidence`: preserved from source contract.
- `blocking_gaps`: preserved from source contract.
- `forbidden_downstream_usage`: preserved from source contract.
- `allowed_usage_within_07`: derived only from source restrictions and Block 01 rules.
- `adapter_status`: 07 adapter classification.
- `adapter_limitations`: limitations added by the adapter without weakening source restrictions.
- `audit_references`: preserved source references plus adapter reference.
- `created_at`: adapter record creation timestamp.
- `schema_version`: adapter schema version.

## 7. Adapter Status Taxonomy

The Motor B Adapter must classify adapted inputs using:

```text
accepted_for_design_only
accepted_for_dry_run_only
degraded_framework_only
rejected_missing_required_fields
rejected_contract_violation
unavailable
```

### accepted_for_design_only

The input is usable as design reference, documentation review, contract validation, or interface planning.

For `framework_only` input, use this status when the input is consumed exclusively for documentation, schema design, or contract review.

This status does not permit signal promotion, confidence scoring, Paper Trading, Live Trading, execution, or capital allocation.

### accepted_for_dry_run_only

The input is usable for dry-run execution of later interfaces, mock validation, or downstream contract testing.

For `framework_only` input, use this status when the input is consumed in dry-run, mock validation, or interface validation.

This status does not permit empirical claims or operational usage.

### degraded_framework_only

The input is structurally usable but has:

```text
evidence_completeness_level = framework_only
```

This is the expected current state.

Use this status as the canonical downstream readiness classification when `framework_only` input enters any pathway that evaluates signal state, eligibility, risk handoff readiness, or preparation for later 07 blocks.

The adapter must preserve all blocking gaps and forbidden downstream usage.

Any of `accepted_for_design_only`, `accepted_for_dry_run_only`, or `degraded_framework_only` must preserve:

```text
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

Each status means no trade approval, no downstream operational eligibility, no signal approval, and no Paper Trading approval.

### rejected_missing_required_fields

The input is rejected because minimum required fields are missing without explicit unavailable status.

Examples include missing source path, schema version, audit references, evidence completeness level, confidence status, paper trading eligibility, or forbidden downstream usage.
Missing `approval_status` or `non_approval_statement` must also be treated as missing required preserved fields unless the entire Motor B input is explicitly unavailable.

### rejected_contract_violation

The input is rejected because it violates source or 07 governance.

Examples include attempting to enable Paper Trading without sufficient evidence, inventing confidence, claiming OOS validation that is not present, weakening forbidden downstream usage, or claiming trading approval.

### unavailable

The Motor B Output Contract is unavailable. The absence must be explicit and downstream processing must not infer evidence from it.

## 8. Required Preserved Fields

The adapter must preserve these fields from Motor B without weakening them:

- `evidence_completeness_level`
- `paper_trading_eligibility`
- `confidence_status`
- `confidence_score`
- `missing_evidence`
- `blocking_gaps`
- `forbidden_downstream_usage`
- `allowed_downstream_usage`
- `approval_status`
- `non_approval_statement`
- `audit_references`
- `source_stage_references`
- `schema_version`
- `backtest_eligibility_status`
- `simulation_status`
- `oos_validation_status`
- `walk_forward_status`
- `robustness_status`
- `falsification_status`

Preservation means:

- copy the value;
- keep explicit null semantics;
- keep limitations;
- keep restrictions;
- keep audit references.

If `approval_status` or `non_approval_statement` is missing from a real Motor B input, the adapter must classify the input as `rejected_missing_required_fields` or `rejected_contract_violation` according to the failure mode.

07 must not modify `approval_status` or `non_approval_statement` to enable trading, authorize Paper Trading, promote a strategy, create downstream operational eligibility, or turn an accepted input into an approved signal.

## 9. Derived Fields Allowed

07 may derive only adapter-local operational metadata that does not change evidence meaning.

Allowed derived fields:

- `motor_b_input_id`
- `adapter_status`
- `adapter_limitations`
- `allowed_usage_within_07`
- `created_at`
- adapter-local `schema_version`
- normalized aliases such as `backtest_status` from source `simulation_status`
- normalized aliases such as `oos_status` from source `oos_validation_status`

Allowed derivation must be deterministic and traceable.

Allowed derivation must not upgrade evidence quality.

## 10. Derived Fields Prohibited

07 must not derive:

- `confidence_score` when missing or null;
- empirical confidence from LLM output;
- backtest results;
- OOS validation;
- walk-forward results;
- robustness results;
- historical performance;
- Paper Trading eligibility;
- Live Trading eligibility;
- capital allocation readiness;
- signal promotion readiness;
- execution readiness;
- risk limit relaxation;
- strategy approval;
- trade approval.

The adapter cannot transform absence of evidence into confidence.

The adapter cannot transform documentation into empirical validation.

## 11. Framework-Only Degradation Rules

If:

```text
evidence_completeness_level = framework_only
```

then:

- `adapter_status` must be `degraded_framework_only`, `accepted_for_design_only`, or `accepted_for_dry_run_only`;
- `paper_trading_eligibility` must remain `blocked`;
- `confidence_status` must remain `confidence_not_available`;
- `confidence_score` must remain `null`;
- `missing_evidence` must preserve missing backtest, OOS, walk-forward, robustness, and confidence evidence;
- `blocking_gaps` must preserve unresolved upstream gaps;
- `forbidden_downstream_usage` must continue blocking Paper Trading, Live Trading, execution, capital allocation, confidence generation, and signal promotion.

Framework-only Motor B may be accepted only for:

- design;
- dry-run;
- mock validation;
- interface validation;
- downstream contract testing.

Framework-only Motor B must not create an operational signal candidate.

## 12. Missing Evidence Propagation

The adapter must propagate `missing_evidence` exactly.

If source Motor B lacks:

- real research outputs;
- real strategy dossier;
- backtest result;
- OOS validation;
- walk-forward result;
- robustness result;
- falsification result;
- confidence score;

then the normalized input must preserve those missing evidence codes.

The adapter may add adapter-local missing evidence notes, but it must not remove source missing evidence.

## 13. Blocking Gaps Propagation

The adapter must propagate `blocking_gaps` exactly.

Blocking gaps must remain visible to later 07 blocks and to `08 Risk Engine`.

The adapter may add adapter-local blocking gaps if adaptation reveals incompatibility, stale versioning, missing required fields, or unsupported schema versions.

The adapter must not remove source blocking gaps.

## 14. Confidence Preservation Rules

The adapter must preserve:

```text
confidence_status
confidence_score
```

Rules:

- If `confidence_score` is `null`, 07 must not fill it.
- If `confidence_status = confidence_not_available`, 07 must preserve it.
- If confidence is unavailable, later 07 blocks must not treat Motor B as scored evidence.
- LLM certainty, regime confidence, and text classification confidence must not be substituted for Motor B confidence.
- Confidence aggregation is not part of Block 02.

## 15. Forbidden Downstream Usage Propagation

The adapter must propagate `forbidden_downstream_usage` from Motor B.

For the current `framework_only` state, forbidden usage must preserve bans on:

- Paper Trading;
- Paper Trading without OOS;
- Live Trading;
- autonomous execution;
- production signal routing;
- execution signal generation;
- capital allocation;
- risk bypass;
- risk limit relaxation;
- confidence generation;
- signal promotion;
- strategy promotion;
- performance claims.

Any later 07 artifact that consumes the adapted Motor B input must include these restrictions unless a later owner stage provides stronger evidence and `08 Risk Engine` review permits change.

## 16. Strategy Candidate References From 05

The Motor B Output Contract may reference strategy candidates or dossiers originating from `05 Strategy Engine`.

The adapter may preserve:

- `strategy_candidate_id`;
- `strategy_family`;
- dossier references;
- registry status;
- quality gate status;
- falsification references;
- rule summaries;
- limitations.

The adapter must not treat 05 examples or mockups as real approved strategies.

If a candidate reference is sourced from mockups, examples, or fixtures, the adapter must mark it as:

```text
synthetic_dry_run_only
```

or reject it if it attempts to claim real evidence.

## 17. Mock And Synthetic Input Handling

Mock, fixture, example, or synthetic Motor B inputs must be marked:

```text
synthetic_dry_run_only
```

Synthetic inputs may be used for:

- dry-run;
- mock validation;
- interface validation;
- downstream contract testing;
- documentation examples.

Synthetic inputs must not be used for:

- real evidence;
- confidence scoring;
- Paper Trading;
- Live Trading;
- execution;
- capital allocation;
- signal promotion;
- strategy promotion;
- performance claims.

Mock data must not be converted into evidence.

## 18. Contract Violation Handling

The adapter must use:

```text
rejected_contract_violation
```

when a Motor B input:

- attempts to enable Paper Trading without sufficient evidence;
- claims confidence while `confidence_status = confidence_not_available`;
- provides `confidence_score` without evidence;
- claims OOS validation without an OOS artifact;
- claims robustness without robustness evidence;
- omits required forbidden downstream usage;
- weakens upstream restrictions;
- claims trade approval;
- claims risk approval;
- attempts to bypass `08 Risk Engine`;
- redefines the Motor B Output Contract.

The adapter must use:

```text
rejected_missing_required_fields
```

when a Motor B input lacks required auditable fields.

## 19. Relationship With 04, 05, And 06

`04 Research Layer` may exist as contextual reference through research or regime outputs, but the Motor B Adapter does not consume Motor A or Regime Context directly.

`05 Strategy Engine` may provide strategy candidates, dossiers, registry entries, quality gate status, or conceptual references through the Motor B Output Contract. Its mock examples are not real evidence and must not be treated as approved strategies.

`06 Backtesting Engine` provides the Motor B Output Contract. It is currently closed as framework/director/documentation, not as a productive backtesting engine.

The adapter consumes `06` output. It does not modify `04`, `05`, or `06`.

## 20. Preparing Input For 07-Block-06 Signal Candidate Normalization

The adapter prepares a normalized Motor B input for later `07-Block-06 Signal Candidate Normalization`.

Preparation means:

- organizing preserved fields;
- making missing evidence explicit;
- carrying forbidden downstream usage;
- preserving confidence status;
- exposing adapter status;
- preserving audit references;
- preserving limitations.

Preparation does not mean:

- creating a signal candidate;
- normalizing signal candidates;
- fusing signals;
- computing confidence;
- approving strategy promotion;
- authorizing Paper Trading.

## 21. Relationship With 08 Risk Engine

`08 Risk Engine` keeps final authority over downstream eligibility, veto, promotion, risk decisions, risk limits, and operational blocking.

The adapter must preserve enough information for `08 Risk Engine` to reject or require review when:

- Motor B is `framework_only`;
- Paper Trading eligibility is `blocked`;
- confidence is unavailable;
- backtest evidence is missing;
- OOS validation is missing;
- walk-forward evidence is missing;
- robustness evidence is missing;
- forbidden downstream usage blocks the requested promotion;
- synthetic inputs are present;
- audit references are incomplete.

08 may veto any later 07 artifact regardless of adapter status.

## 22. Explicit Prohibited Actions

Block 02 must not:

- implement trading logic;
- implement Paper Trading;
- implement Live Trading;
- create execution logic;
- create capital allocation;
- create signal fusion;
- create Signal Candidate Normalization;
- create Bull/Bear Debate;
- create Motor A Context Layer;
- create Motor C Event Classifier;
- create LLM prompting rules;
- create Confidence Aggregation;
- create Risk Handoff;
- modify the Motor B Output Contract of 06;
- redefine contracts of prior stages;
- invent backtesting, OOS validation, walk-forward, robustness, or historical results;
- invent `confidence_score`;
- convert mock data into real evidence;
- create an ML ensemble;
- start Block 03.

## 23. Block 02 Closure Criteria

Block 02 is closed when this document defines:

- Motor B Adapter purpose;
- relationship with Block 00 and Block 01;
- source contract reference;
- current Motor B state;
- normalized Motor B input schema;
- adapter status taxonomy;
- required preserved fields;
- allowed derived fields;
- prohibited derived fields;
- framework-only degradation rules;
- missing evidence propagation;
- blocking gaps propagation;
- confidence preservation rules;
- forbidden downstream usage propagation;
- strategy candidate reference handling;
- mock and synthetic input handling;
- contract violation handling;
- relationship with prior stages;
- relationship with later 07-Block-06 Signal Candidate Normalization;
- relationship with `08 Risk Engine`.

Closing Block 02 does not implement the adapter in code and does not create Signal Candidate Normalization, Signal Fusion, Confidence Aggregation, Risk Handoff, Paper Trading, Live Trading, execution logic, or capital allocation.
