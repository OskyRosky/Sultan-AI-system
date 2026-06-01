# 07 Signal Fusion + LLM Motors - Signal Candidate Normalization

## 1. Purpose

Block 06 defines Signal Candidate Normalization for `07 Signal Fusion + LLM Motors`.

The purpose is to convert governed inputs from Motor A, Motor B, Motor C, human review, or synthetic fixtures into a common, auditable `NormalizedSignalCandidate` schema for later 07 blocks.

NormalizedSignalCandidate is not trade approval.

Normalization does not create convergent evidence.

Normalization does not create final signal confidence.

Normalization does not trigger event precedence.

Normalization creates a traceable representation only. It does not fuse signals, aggregate confidence, authorize Paper Trading, authorize Live Trading, create execution readiness, or override `08 Risk Engine`.

## 2. Scope

This block covers:

- permitted inputs;
- `NormalizedSignalCandidate` schema;
- `candidate_type` enum;
- `source_motor` enum;
- `signal_direction` normalization;
- `normalization_status` enum;
- evidence level normalization;
- Motor B normalization rules;
- Motor A normalization rules;
- Motor C normalization rules;
- confidence preservation and boundary rules;
- missing evidence and blocking gap propagation;
- forbidden downstream usage propagation;
- synthetic and dry-run input handling;
- unavailable and degraded input handling;
- conflict and contradiction handling;
- event hint normalization;
- LLM output normalization;
- audit and replay metadata requirements;
- relationship with 07-Block-07 Bull/Bear Debate Layer;
- relationship with 07-Block-08 Deterministic Signal Fusion Engine;
- relationship with 07-Block-09 Confidence Status and Aggregation Policy;
- relationship with `08 Risk Engine`.

This block does not implement Python code, trading logic, Paper Trading, Live Trading, execution, capital allocation, Signal Fusion, Bull/Bear Debate, Confidence Aggregation, Risk Handoff, or Block 07.

## 3. Non-Authority Reminder

Block 06 is non-authoritative.

Block 06 must not:

- approve trades;
- approve strategies;
- authorize Paper Trading;
- authorize Live Trading;
- create execution readiness;
- allocate capital;
- relax risk limits;
- aggregate confidence;
- apply final event precedence;
- fuse signals;
- invent evidence;
- invent trading `confidence_score`;
- convert synthetic data into real evidence;
- convert LLM output into empirical evidence.

## 4. Relationship With Blocks 00-05

Block 00 defines 07 boundaries and non-authority rules.

Block 01 defines accepted input states and input family contracts.

Block 02 defines the Motor B Adapter and `NormalizedMotorBInput`.

Block 03 defines Motor A context outputs, regime metadata, conceptual `base_motor_weights`, and event modulation hooks.

Block 04 defines Motor C event classifier outputs, event metadata, source reliability, classification confidence, and `event_precedence_hint`.

Block 05 defines LLM safety, prompting, evidence, validation, fallback, and replay rules.

Block 06 consumes these contracts. It does not redefine them.

## 5. Definition Of NormalizedSignalCandidate

`NormalizedSignalCandidate` is a common, audit-ready representation of one normalized candidate input or pre-fusion candidate bundle.

It may represent:

- Motor B technical evidence state;
- Motor A context state;
- Motor C event state;
- synthetic dry-run fixture;
- unavailable input placeholder;
- rejected input placeholder;
- pre-fusion composite record that preserves source boundaries.

`NormalizedSignalCandidate` is not trade approval.

It is not a final signal.

It is not Paper Trading approval.

It is not Live Trading approval.

It is not execution instruction.

## 6. Permitted Inputs

Permitted inputs are:

- Motor B Adapter output / `NormalizedMotorBInput`;
- Motor A Context Layer output / `MotorAContextOutput`;
- Motor C Event / LLM Classifier output / `MotorCEventOutput`;
- human review metadata when non-authoritative and traceable;
- synthetic dry-run fixtures when explicitly marked.

Inputs must preserve source identifiers, schema versions, audit references, limitations, and forbidden downstream usage.

Malformed, untraceable, authority-claiming, or source-less inputs must be rejected or marked unavailable.

## 7. Common Output Schema

The conceptual schema is:

```text
NormalizedSignalCandidate
  normalized_signal_candidate_id
  candidate_type
  source_motor
  source_motor_ids
  source_contract_references
  source_schema_versions
  asset
  asset_scope
  timeframe
  horizon
  signal_direction
  signal_direction_status
  strategy_candidate_id
  strategy_family
  regime_label
  context_label
  event_type
  event_severity
  affected_assets
  expected_duration
  evidence_completeness_level
  evidence_level_normalized
  backtest_status
  oos_status
  walk_forward_status
  robustness_status
  paper_trading_eligibility
  downstream_operational_eligibility
  confidence_status
  confidence_score
  classification_confidence_status
  classification_confidence_score
  uncertainty_level
  source_reliability_label
  source_reliability_normalized
  missing_evidence
  missing_context
  missing_sources
  blocking_gaps
  unsupported_claims
  conflicting_sources
  forbidden_downstream_usage
  allowed_usage_within_07
  synthetic_status
  normalization_status
  normalization_limitations
  requires_human_review
  event_precedence_hint
  event_modulation_hook_reference
  non_approval_statement
  audit_references
  created_at
  schema_version
```

Fields absent from a source motor must be explicit nulls, unavailable markers, empty lists, or limitation notes according to source contract semantics.

## 8. candidate_type Enum

Allowed `candidate_type` values are:

```text
motor_b_technical_candidate
motor_a_context_candidate
motor_c_event_candidate
composite_pre_fusion_candidate
synthetic_dry_run_candidate
unavailable_candidate
rejected_candidate
```

`composite_pre_fusion_candidate` preserves source boundaries and must not be treated as fused evidence.

## 9. source_motor Enum

Allowed `source_motor` values are:

```text
MotorA
MotorB
MotorC
HumanReview
SyntheticFixture
Unknown
```

Multiple source motors must be represented in `source_motor_ids` and source contract references. A composite record must not hide which motor contributed each field.

## 10. normalization_status Enum

Allowed `normalization_status` values are:

```text
normalized
normalized_with_limitations
degraded_normalization
rejected_missing_required_fields
rejected_contract_violation
unavailable
synthetic_dry_run_only
```

Use `normalized_with_limitations` when the record is schema-valid but carries limitations such as Motor B `framework_only`.

Use `degraded_normalization` when required context is stale, evidence is missing, sources are weak, confidence is unavailable, or conflicts require caution.

Use rejected statuses when required fields are missing or source contracts are violated.

## 11. Signal Direction Normalization

Allowed `signal_direction` values are:

```text
long_bias
short_bias
neutral
risk_reduce
risk_suspend
no_direction
unknown_direction
```

Rules:

- Motor A context does not necessarily produce operational `signal_direction`.
- Motor C event classification does not necessarily produce operational `signal_direction`.
- `risk_reduce` and `risk_suspend` are not execution instructions.
- `signal_direction` is not a trade recommendation.
- `no_direction` must be used when the input is context, event-only, unavailable, or insufficient evidence.
- `unknown_direction` must be used when the input is ambiguous, malformed, or contradictory.

`signal_direction_status` must explain whether direction was preserved, unavailable, inferred from contract metadata, rejected, or unknown.

## 12. Asset, Timeframe, And Horizon Normalization

`asset`, `asset_scope`, `timeframe`, and `horizon` must be preserved when provided by source contracts.

They must not be invented.

When scope is broad or event-based, `asset_scope` may use Motor C values such as:

```text
all_market
asset_specific
sector_specific
exchange_specific
stablecoin_specific
unknown_scope
```

Missing or unsupported asset/timeframe/horizon fields must set explicit limitation notes and may require `degraded_normalization` or `unavailable`.

## 13. Evidence Level Normalization

Allowed `evidence_level_normalized` values are:

```text
framework_only
synthetic_dry_run_only
partial_empirical
backtest_available
oos_available
robustness_available
unknown_evidence_level
unavailable_evidence_level
```

Rules:

- `framework_only` remains `framework_only`.
- `synthetic_dry_run_only` never becomes empirical evidence.
- `partial_empirical` cannot imply robustness.
- `backtest_available` cannot imply OOS.
- OOS cannot imply robustness unless explicitly present.
- Unknown evidence must be degraded or unavailable.
- Evidence normalization does not create evidence.

Current Motor B input must normalize to:

```text
evidence_completeness_level = framework_only
evidence_level_normalized = framework_only
```

## 14. Motor B Normalization Rules

When source input is Motor B Adapter output, Block 06 must preserve:

- `evidence_completeness_level`;
- `paper_trading_eligibility`;
- `confidence_status`;
- `confidence_score`;
- `missing_evidence`;
- `blocking_gaps`;
- `forbidden_downstream_usage`;
- `approval_status` when present;
- `non_approval_statement`;
- `allowed_usage_within_07`;
- source contract references;
- schema version;
- audit references.

Block 06 must not:

- expand `allowed_usage_within_07`;
- transform `framework_only` into empirical evidence;
- create downstream operational eligibility;
- create `confidence_score`;
- weaken forbidden downstream usage.

If Motor B has:

```text
evidence_completeness_level = framework_only
```

then `NormalizedSignalCandidate` must have:

```text
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
normalization_status = normalized_with_limitations
```

or:

```text
normalization_status = degraded_normalization
```

when additional missing fields, stale metadata, or conflicts exist.

`forbidden_downstream_usage` must include Paper Trading, Live Trading, execution, capital allocation, strategy promotion, and confidence invention.

`non_approval_statement` must explicitly state that the candidate is not trade approval.

## 15. Motor A Normalization Rules

When source input is Motor A Context Layer output, Block 06 must preserve:

- `regime_label`;
- `context_label`;
- `regime_strategy_activation_rules`;
- conceptual `base_motor_weights`;
- `event_modulation_hook` as future reference only;
- limitations;
- `uncertainty_level`;
- `forbidden_downstream_usage`;
- audit references.

Block 06 must not:

- convert regime context into empirical evidence;
- convert `contextually_supported` into trade approval;
- convert `base_motor_weights` into evidence weighting;
- convert `base_motor_weights` into a ML ensemble;
- activate `event_modulation_hook`;
- create operational signal eligibility.

If Motor B remains `framework_only`, Motor A cannot change:

```text
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

This holds even when Motor A contains `trend_bullish`, `favorable_trend_context`, or `contextually_supported`.

## 16. Motor C Normalization Rules

When source input is Motor C Event / LLM Classifier output, Block 06 must preserve:

- `event_type`;
- `event_subtype`;
- `severity` as `event_severity`;
- `affected_assets`;
- `affected_markets`;
- `expected_duration`;
- `event_freshness_status`;
- `uncertainty_level`;
- `classification_confidence_status`;
- `classification_confidence_score`;
- `source_references`;
- `unsupported_claims`;
- `missing_sources`;
- `conflicting_sources`;
- `source_reliability_label`;
- deterministic source hierarchy references when present;
- `event_precedence_hint`;
- `requires_human_review`;
- `forbidden_downstream_usage`.

Block 06 must not:

- apply final event precedence;
- convert severity into trading authorization;
- convert bullish or favorable events into approved signals;
- convert LLM output into empirical evidence;
- use classification confidence as trading confidence.

If Motor C has:

```text
severity = high
```

or:

```text
severity = critical
```

Block 06 may normalize severity and mark `requires_human_review` or risk-sensitive handling in limitations.

Block 06 must not suspend trading, approve trading, execute an action, activate final event precedence, modify risk limits, bypass Block 08, or bypass `08 Risk Engine`.

Event precedence belongs to Block 08.

## 17. Confidence Status Preservation

Block 06 must keep confidence domains separate:

- Motor B `confidence_status` / `confidence_score`;
- Motor A context confidence or `uncertainty_level`;
- Motor C `classification_confidence_status` / `classification_confidence_score`;
- final signal confidence.

Rules:

- final signal confidence belongs to Block 09.
- Block 06 cannot compute final signal confidence.
- Block 06 cannot aggregate confidence.
- Block 06 cannot fill Motor B `confidence_score`.
- classification confidence is not trading confidence.
- context confidence is not trading confidence.
- missing confidence must remain unavailable or null with explicit status.
- if confidence fields conflict, preserve conflict and mark `degraded_normalization` or `requires_human_review`.

## 18. Missing Evidence And Blocking Gaps Propagation

Block 06 must preserve:

- `missing_evidence`;
- `missing_context`;
- `missing_sources`;
- `blocking_gaps`;
- source limitations;
- unavailable markers.

Missing evidence must remain explicit.

Blocking gaps must remain visible to Blocks 07, 08, 09, 10, and `08 Risk Engine`.

Block 06 must not remove upstream blocking gaps or reinterpret them as resolved.

## 19. Forbidden Downstream Usage Propagation

`NormalizedSignalCandidate` must include `forbidden_downstream_usage`.

Under current Motor B `framework_only` state, forbidden usage must include:

- trade approval;
- Paper Trading authorization;
- Live Trading authorization;
- execution;
- capital allocation;
- risk limit relaxation;
- strategy promotion;
- confidence invention;
- empirical evidence replacement.

Later blocks must preserve these restrictions unless a governed upstream contract and `08 Risk Engine` process allow change.

## 20. Synthetic And Dry-Run Input Handling

Synthetic inputs must be marked:

```text
synthetic_status = synthetic_dry_run_only
normalization_status = synthetic_dry_run_only
```

Rules:

- synthetic inputs cannot be mixed into real evidence;
- synthetic `NormalizedSignalCandidate` records cannot be used for Paper Trading or Live Trading;
- synthetic outputs are only for schema validation, dry-run, interface testing, and documentation;
- synthetic outputs must carry explicit `non_approval_statement`;
- mock data must never become empirical evidence.

## 21. Unavailable And Degraded Input Handling

Unavailable input must produce:

```text
candidate_type = unavailable_candidate
normalization_status = unavailable
```

Rejected input must produce:

```text
candidate_type = rejected_candidate
```

with the relevant rejected normalization status.

Degraded input may still be normalized for documentation, review, dry-run, or later contract testing, but must preserve limitations and forbidden downstream usage.

Degraded or unavailable normalized candidates must not proceed as operational signal candidates.

## 22. Conflict And Contradiction Handling

Conflicts must be preserved, not resolved silently.

Examples include:

- Motor A favorable context plus Motor B `framework_only`;
- Motor C bullish event plus Motor B `framework_only`;
- Motor C critical event plus Motor A bullish regime;
- conflicting event sources;
- missing Motor B evidence;
- missing Motor C sources;
- stale Motor A regime context;
- synthetic input mixed with non-synthetic input.

Block 06 may mark:

```text
conflict_detected
requires_human_review
degraded_normalization
unavailable
rejected_contract_violation
```

as appropriate in limitations, status, and review fields.

Block 06 must not decide trade action, fusion outcome, final confidence, or event precedence.

## 23. Event Hint Normalization

Block 06 may preserve:

- `event_precedence_hint`;
- `event_modulation_hook_reference`;
- affected assets;
- expected duration;
- event severity;
- freshness;
- source reliability.

Block 06 must not activate final event precedence.

`event_precedence_hint` is normalized and preserved only for 07-Block-08 Deterministic Signal Fusion Engine.

## 24. LLM Output Normalization

LLM-assisted fields must preserve:

- `source_references`;
- `unsupported_claims`;
- `missing_sources`;
- `conflicting_sources`;
- `prompt_or_instruction_version` when available;
- `llm_model_metadata` when available;
- prompt injection suspicion when present;
- validation status;
- fallback status;
- audit references.

Malformed LLM outputs must be rejected or degraded.

LLM output is not empirical trading evidence.

LLM output is not trade approval.

## 25. Audit And Replay Metadata Requirements

Every `NormalizedSignalCandidate` must include:

- normalized candidate identifier;
- source motor identifiers;
- source contract references;
- source schema versions;
- source timestamps where available;
- normalization timestamp;
- normalization status;
- limitations;
- source audit references;
- created_at;
- schema version;
- replay references for LLM-assisted fields where applicable.

Replay must show how each normalized field maps back to its source motor contract or explicit null/unavailable state.

## 26. Relationship With 07-Block-07 Bull/Bear Debate Layer

07-Block-07 Bull/Bear Debate Layer consumes normalized inputs.

Bull/Bear agents must debate normalized candidates, not raw ungoverned inputs.

Debate output is not evidence and not approval.

Missing evidence, blocking gaps, forbidden downstream usage, source limitations, and non-approval statements must remain visible to debate agents.

## 27. Relationship With 07-Block-08 Deterministic Signal Fusion Engine

07-Block-08 Deterministic Signal Fusion Engine performs deterministic fusion.

Block 06 does not fuse.

Block 06 does not apply final event precedence.

`event_precedence_hint` is only normalized and preserved.

`base_motor_weights` are only normalized and preserved as conceptual inputs.

Block 08 must preserve Motor B `framework_only` constraints unless later governed evidence and `08 Risk Engine` review allow change.

## 28. Relationship With 07-Block-09 Confidence Status And Aggregation Policy

07-Block-09 Confidence Status and Aggregation Policy defines final confidence policy.

Block 06 does not aggregate confidence.

Block 06 only preserves confidence fields and their boundaries.

Classification confidence, context uncertainty, and Motor B confidence are separate domains.

## 29. Relationship With 08 Risk Engine

`08 Risk Engine` retains final authority over downstream eligibility, veto, promotion, risk limits, and operational blocking.

07 cannot approve trading.

`NormalizedSignalCandidate` is not eligible for Paper Trading under the current Motor B `framework_only` state.

08 may veto any future fused signal candidate.

Block 06 must preserve enough detail for 08 to identify missing evidence, blocked eligibility, forbidden usage, unresolved conflicts, synthetic inputs, source limitations, and human review requirements.

## 30. Explicit Prohibited Actions

Block 06 must not:

- implement trading logic;
- implement Paper Trading;
- implement Live Trading;
- create execution logic;
- create capital allocation;
- create Signal Fusion;
- create Bull/Bear Debate;
- create a new Motor A layer;
- create a new Motor B Adapter;
- create a new Motor C classifier;
- create Confidence Aggregation;
- create Risk Handoff;
- create Block 07;
- modify the Motor B Output Contract of 06;
- modify Blocks 00-05;
- redefine prior contracts;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- convert `NormalizedSignalCandidate` into trade signal;
- convert normalized event severity into trading authorization;
- convert `base_motor_weights` into a ML ensemble;
- convert LLM output into empirical evidence;
- convert synthetic data into real evidence.

## 31. Block 06 Closure Criteria

Block 06 is closed when this document defines:

- Signal Candidate Normalization purpose;
- scope;
- non-authority rules;
- relationship with Blocks 00-05;
- `NormalizedSignalCandidate`;
- explicit statement that `NormalizedSignalCandidate` is not trade approval;
- explicit statement that normalization does not create convergent evidence;
- explicit statement that normalization does not create final signal confidence;
- explicit statement that normalization does not trigger event precedence;
- permitted inputs;
- common output schema;
- source motor normalization rules;
- Motor B normalization rules;
- Motor A normalization rules;
- Motor C normalization rules;
- signal direction normalization;
- asset, timeframe, and horizon normalization;
- evidence level normalization;
- confidence status preservation;
- missing evidence and blocking gaps propagation;
- forbidden downstream usage propagation;
- synthetic and dry-run input handling;
- unavailable and degraded input handling;
- conflict and contradiction handling;
- event hint normalization;
- LLM output normalization;
- audit and replay metadata requirements;
- relationship with 07-Block-07 Bull/Bear Debate Layer;
- relationship with 07-Block-08 Deterministic Signal Fusion Engine;
- relationship with 07-Block-09 Confidence Status and Aggregation Policy;
- relationship with `08 Risk Engine`.

Closing Block 06 does not implement normalization in code and does not create Bull/Bear Debate, Signal Fusion, Confidence Aggregation, Risk Handoff, Paper Trading, Live Trading, execution logic, or capital allocation.
