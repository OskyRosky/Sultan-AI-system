# 07 Signal Fusion + LLM Motors - Input Contract Layer

## 1. Purpose

Block 01 defines the conceptual input contracts that `07 Signal Fusion + LLM Motors` may accept before any Motor B Adapter, Motor A Context Layer, Motor C classifier, signal normalization, debate, fusion, confidence aggregation, or risk handoff is built.

The purpose of this block is to specify:

- which input families are permitted;
- which fields each input family must carry;
- how inputs are accepted, rejected, degraded, marked unavailable, or limited to synthetic dry-runs;
- how missing evidence must be represented;
- how upstream restrictions must be preserved;
- how downstream compatibility with `08 Risk Engine` is maintained.

This block is documentary and contractual only. It does not implement parsing, adapters, validation code, signal fusion, trading logic, or risk logic.

## 2. Relationship With Block 00

Block 00 established the stage charter, boundaries, and non-authority rules for `07 Signal Fusion + LLM Motors`.

Block 01 follows those boundaries:

- 07 consumes upstream contracts and evidence states.
- 07 does not invent evidence.
- 07 does not approve trades.
- 07 does not authorize Paper Trading.
- 07 does not create execution logic.
- 07 does not redefine the Motor B Output Contract.
- 07 must preserve `forbidden_downstream_usage`.
- 07 must preserve current Motor B state when Motor B is `framework_only`.

The output of the broader 07 stage may later be a `fused signal candidate`, but Block 01 does not create fused signal candidates.

## 3. Scope

Block 01 covers conceptual input acceptance rules for:

1. Motor B output from `06 Backtesting Engine`, with the current V1 terminal
   artifact consumed through
   `docs/14_motor_b_raw_diagnostics_adapter_contract.md`.
2. Regime context from `04 Research Layer` / Regime Detection v1.
3. Motor A macro/fundamental context.
4. Motor C event / LLM classifier outputs.
5. Optional human review metadata.
6. Prior stage references and audit metadata.
7. Optional dry-run/mock input references marked as synthetic.

Block 01 does not cover:

- Motor B Adapter implementation;
- Motor A Context Layer implementation;
- Motor C Event Classifier implementation;
- Signal Candidate Normalization;
- Bull/Bear Debate;
- Deterministic Signal Fusion;
- Confidence Aggregation;
- Risk Handoff;
- Paper Trading;
- Live Trading;
- execution;
- capital allocation.

## 4. Non-Authority Reminder

Inputs accepted by 07 are accepted only for downstream processing inside the governed 07 workflow.

Input acceptance means no trade approval.

Input acceptance is not:

- trade approval;
- Paper Trading approval;
- Live Trading approval;
- capital allocation approval;
- strategy promotion;
- confidence generation;
- historical validation;
- Risk Engine approval.

Any input may be contract-valid and still blocked from operational downstream usage.

## 5. Input Family Registry

| Input family | Source owner | Required now | Implementation status | Notes |
| --- | --- | --- | --- | --- |
| `motor_b_raw_diagnostics_handoff` | `06 Backtesting Engine` | Yes | Terminal V1 handoff exists | Consumed through `07 Signal Fusion + LLM Motors/docs/14_motor_b_raw_diagnostics_adapter_contract.md`; source artifact is `RawDiagnosticsHandoffContract`. |
| `motor_b_output_contract` | `06 Backtesting Engine` | Reference only | Documentation contract exists | Historical/canonical semantics reference from `06 Backtesting Engine/docs/18_motor_b_output_contract.md`; not the current terminal Stage 06 handoff artifact. |
| `regime_context` | `04 Research Layer` / future Motor A | Optional | Framework input exists conceptually through Regime Detection v1 | Context only; not trading evidence by itself. |
| `motor_a_macro_fundamental_context` | future Motor A | Optional | Not implemented | Conceptual input only in this block. |
| `motor_c_event_llm_classification` | future Motor C | Optional | Not implemented | Conceptual input only in this block. |
| `human_review_metadata` | reviewer / governance process | Optional | Not implemented | Non-authoritative metadata. |
| `prior_stage_audit_metadata` | upstream stages | Required when available | Documentation references exist | Required for replay and traceability. |
| `synthetic_dry_run_reference` | 07 fixtures, future Block 12 | Optional | Not implemented | Must never be treated as real evidence. |

## 6. Accepted Input States

Every input family must resolve to one of these states:

```text
accepted
rejected
degraded
unavailable
synthetic_dry_run_only
```

### accepted

The input has the minimum required metadata, explicit source references, schema or method version where applicable, timestamps where applicable, limitations, and no unresolved blocking inconsistency.

Accepted does not mean operationally approved.

### rejected

The input is structurally invalid, untraceable, incompatible with Block 00, missing required fields without explicit unavailable status, or attempts to grant authority that 07 does not have.

Rejected inputs must not be used by later 07 blocks.

### degraded

The input is structurally usable for design, dry-run, interface validation, or documentation review, but evidence quality is incomplete, unavailable, synthetic, framework-only, stale, ambiguous, or restricted.

Degraded inputs must preserve blocking gaps and `forbidden_downstream_usage`.

### unavailable

The input does not exist or has not been produced. The absence must be explicit and traceable.

Unavailable inputs may be represented as null only when paired with an explicit status such as `regime_context_not_available`, `dossier_not_available`, or `confidence_not_available`.

### synthetic_dry_run_only

The input is a mock, fixture, example, or synthetic dry-run artifact.

It may be used only for interface design, contract validation, dry-run logic, and documentation examples. It must not be treated as evidence.

## 7. Motor B Output Contract Input

The historical Motor B Output Contract is referenced from:

```text
06 Backtesting Engine/docs/18_motor_b_output_contract.md
```

The current V1 terminal Stage 06 artifact is:

```text
RawDiagnosticsHandoffContract
```

Stage 07 must consume that terminal artifact through:

```text
07 Signal Fusion + LLM Motors/docs/14_motor_b_raw_diagnostics_adapter_contract.md
```

The Motor B Output Contract remains a semantic reference for framework-only,
confidence, evidence, and downstream restriction rules. It is not the concrete
terminal handoff artifact produced by the completed Stage 06 V1 flow.

The contract and handoff both belong to `06 Backtesting Engine`. Stage 07
consumes them and preserves their semantics. Stage 07 must not redefine either
artifact.

### Required Fields To Preserve

At minimum, 07 must preserve:

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
- `schema_version`
- `source_stage_references`

### Current Required State

The current Motor B state must be represented as:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

When Motor B arrives as `framework_only`, Block 01 may classify it as:

```text
accepted
```

only for:

- design reference;
- documentation review;
- contract validation;
- dry-run simulation;
- interface validation.

It must be classified as:

```text
degraded
```

for any pathway that evaluates downstream readiness.

It must be treated as blocked for any Paper Trading, Live Trading, capital allocation, execution, production signal routing, confidence generation, or strategy promotion path.

## 8. Regime Context Input

Regime context may come from `04 Research Layer` / Regime Detection v1 or a later Motor A Context Layer.

Regime context is market context. It is not sufficient evidence for trading by itself.

### Minimum Fields

Required fields:

- `regime_label`
- `regime_source`
- `regime_timestamp`
- `regime_method_version`
- `regime_confidence_status`
- `supported_assets`
- `supported_timeframes`
- `limitations`
- `audit_references`

### Acceptance Criteria

Regime context may be `accepted` when:

- source is traceable;
- method version is declared;
- timestamp exists;
- supported assets and timeframes are explicit;
- limitations are present;
- confidence status is explicit;
- it does not claim trade approval.

Regime context must be `degraded` when:

- it is derived from framework-only research;
- its labels are not online or rolling;
- confidence is unavailable;
- supported assets or timeframes are incomplete;
- it depends on synthetic or stale context.

Regime context must be `rejected` when:

- it lacks source references;
- it lacks method version;
- it claims trading authority;
- it attempts to override Motor B restrictions;
- it attempts to authorize Paper Trading.

## 9. Motor A Macro/Fundamental Context Input

Motor A macro/fundamental context is a permitted conceptual input family.

It is not implemented in Block 01.

### Minimum Fields

Required fields:

- `context_label`
- `macro_state`
- `liquidity_state`
- `risk_environment`
- `source_references`
- `timestamp`
- `uncertainty_level`
- `limitations`
- `schema_or_method_version`

### Acceptance Criteria

Motor A macro/fundamental context may be `accepted` only when it is traceable, timestamped, versioned, scoped, and limitation-aware.

It must be `degraded` when uncertainty is high, sources are partial, coverage is incomplete, or evidence is qualitative only.

It must be `unavailable` when it has not been produced.

It must be `rejected` when it claims trading authority, paper trading eligibility, risk override, or empirical validation that it does not contain.

## 10. Motor C Event / LLM Classifier Output Input

Motor C event / LLM classifier output is a permitted conceptual input family.

It is not implemented in Block 01.

### Minimum Fields

Required fields:

- `event_id`
- `event_type`
- `severity`
- `affected_assets`
- `expected_duration`
- `source_references`
- `llm_model_metadata`
- `classification_timestamp`
- `uncertainty_level`
- `limitations`
- `prohibited_usage`
- `prompt_or_instruction_version`
- `audit_references`

### Acceptance Criteria

Motor C output may be `accepted` only when:

- source references are present;
- LLM model metadata is present;
- classification timestamp is present;
- uncertainty is explicit;
- limitations are explicit;
- prohibited usage is explicit;
- it does not claim empirical market validation.

Motor C output must be `degraded` when:

- source quality is partial;
- uncertainty is high;
- event duration is unclear;
- affected assets are broad or ambiguous;
- classification comes from synthetic dry-run fixtures.

Motor C output must be `rejected` when:

- it lacks source references;
- it lacks LLM metadata;
- it claims trade approval;
- it claims backtest evidence;
- it generates confidence without evidence;
- it attempts to bypass `08 Risk Engine`.

LLM classifier output is not empirical evidence by itself.

## 11. Human Review Metadata Input

Human review metadata is optional and non-authoritative.

It may support governance and audit, but it does not override missing evidence, Risk Engine veto, or upstream forbidden usage.

### Minimum Fields

Required fields when present:

- `reviewer_id_or_role`
- `review_timestamp`
- `review_scope`
- `review_notes`
- `review_decision_type`
- `limitations`
- `audit_references`

Human review metadata may be `accepted` when it is scoped, timestamped, and traceable.

It must be `degraded` when review scope is narrow, limitations are significant, or reviewer identity is role-only.

It must be `rejected` if it claims trading approval or Risk Engine authority outside a documented downstream process.

## 12. Prior Stage References And Audit Metadata

Every input should preserve prior stage references where available.

Required audit metadata:

- `source_stage`
- `source_artifact_id`
- `source_artifact_path`
- `schema_version` or `method_version`
- `generated_at` or source timestamp;
- `audit_references`
- `limitations`
- `non_approval_statement`, when applicable;
- `forbidden_downstream_usage`, when applicable.

Inputs without audit metadata must be `rejected` unless the input family is explicitly marked `unavailable`.

## 13. Synthetic Dry-Run Rules

Synthetic, mock, fixture, or example inputs must be marked:

```text
synthetic_dry_run_only
```

Synthetic inputs may be used for:

- interface validation;
- dry-run simulation;
- documentation review;
- contract validation;
- local development fixtures in later blocks.

Synthetic inputs must not be used for:

- evidence claims;
- confidence generation;
- Paper Trading;
- Live Trading;
- capital allocation;
- strategy promotion;
- performance claims;
- Risk Engine approval.

Synthetic inputs must preserve `forbidden_downstream_usage`.

## 14. Missing Evidence Handling

Missing evidence must be explicit.

Examples:

```text
confidence_score = null
confidence_status = confidence_not_available
```

```text
regime_context = null
regime_context_status = regime_context_not_available
```

```text
motor_c_event_output = null
motor_c_status = unavailable
```

A null value without an explicit status is invalid for downstream 07 processing.

Missing evidence must not be interpreted as neutral, safe, approved, or low-risk.

## 15. Forbidden Downstream Usage Propagation

If an upstream input contains `forbidden_downstream_usage`, 07 must carry it forward.

07 must not weaken upstream restrictions.

For Motor B in the current `framework_only` state, `forbidden_downstream_usage` must continue to block:

- Paper Trading;
- Paper Trading without OOS;
- Live Trading;
- capital allocation;
- autonomous execution;
- production signal routing;
- risk bypass;
- confidence generation;
- strategy promotion;
- execution signal generation;
- performance claims.

Any later 07 output must include the union of applicable forbidden usage restrictions from all accepted or degraded inputs.

## 16. Confidence Field Rules

07 must preserve confidence fields from upstream inputs.

Rules:

- `confidence_status` must be explicit.
- `confidence_score` may be null only when paired with explicit status.
- If `confidence_status = confidence_not_available`, then `confidence_score = null`.
- 07 must not invent `confidence_score`.
- 07 must not compute aggregate confidence in Block 01.
- 07 must not turn LLM certainty into empirical confidence.
- 07 must not treat regime confidence, LLM classification confidence, and Motor B confidence as equivalent.

Confidence aggregation belongs to a later block. It is not part of Block 01.

## 17. Timestamps, Schema Versions, And Source References

Every available input must include:

- timestamp or generated-at metadata;
- schema version, method version, or prompt/instruction version as applicable;
- source references;
- source stage;
- audit references;
- limitations.

Inputs with unsupported future schema versions must be `degraded`, routed to human review, or `rejected` depending on compatibility.

Inputs with missing schema or method version must be `rejected` unless explicitly marked `unavailable`.

Inputs with stale timestamps must be `degraded` unless a later block defines stricter rejection criteria.

## 18. Compatibility With 08 Risk Engine

Block 01 input handling must preserve enough metadata for `08 Risk Engine` to veto or require review.

Every accepted or degraded input must preserve:

- evidence completeness;
- confidence status;
- confidence score or explicit null;
- missing evidence;
- blocking gaps;
- forbidden downstream usage;
- limitations;
- non-approval statements;
- synthetic status, when applicable;
- human review status, when applicable.

`08 Risk Engine` must be able to block any input chain that includes:

- `framework_only` Motor B;
- missing OOS validation;
- missing robustness review;
- synthetic evidence;
- unavailable confidence;
- unsupported schema version;
- unresolved blocking gaps;
- forbidden downstream usage that conflicts with requested promotion.

## 19. Relationship With Block 02 Motor B Adapter

Block 02 defines the conceptual Motor B adapter. The current V1 concrete source
artifact is `RawDiagnosticsHandoffContract`, mapped by
`docs/14_motor_b_raw_diagnostics_adapter_contract.md` into 07's internal input
representation.

Block 01 does not implement that adapter.

Block 02 must preserve:

- `evidence_completeness_level`;
- `paper_trading_eligibility`;
- `confidence_status`;
- `confidence_score`;
- `missing_evidence`;
- `blocking_gaps`;
- `forbidden_downstream_usage`;
- `non_approval_statement`;
- `audit_references`.

Block 02 must not reinterpret `framework_only` as empirical evidence.

## 20. Relationship With Later Blocks 03-10

Later blocks may consume accepted or degraded inputs under these limits:

- Block 03 may define Motor A context processing, but not in Block 01.
- Block 04 may define Motor C event / LLM classifier contracts, but not in Block 01.
- Block 05 may define LLM safety and prompting rules.
- Block 06 may normalize signal candidates.
- Block 07 may define Bull/Bear Debate.
- Block 08 may define Deterministic Signal Fusion.
- Block 09 may define Confidence Status and Aggregation Policy.
- Block 10 may define Downstream Eligibility and Risk Handoff.

No later block may use Block 01 input acceptance as trading approval.

No later block may weaken upstream forbidden downstream usage without a formal upstream replacement and `08 Risk Engine` review.

## 21. Acceptance Criteria Summary

An input can be `accepted` when:

- it belongs to a permitted input family;
- required metadata is present;
- source references are traceable;
- timestamps are present;
- schema or method version is present where applicable;
- limitations are present;
- confidence status is explicit where applicable;
- forbidden downstream usage is preserved;
- it does not claim authority outside its stage.

## 22. Rejection Criteria Summary

An input must be `rejected` when:

- it belongs to an unpermitted input family;
- required metadata is missing without explicit unavailable status;
- source references are absent;
- schema or method version is missing when required;
- it claims trade approval;
- it claims Paper Trading approval;
- it claims Live Trading approval;
- it claims capital allocation approval;
- it invents backtesting, OOS validation, walk-forward, robustness, confidence, or historical results;
- it attempts to bypass `08 Risk Engine`;
- it attempts to redefine an upstream contract owned by another stage.

## 23. Degradation Criteria Summary

An input must be `degraded` when:

- evidence is incomplete;
- evidence is framework-only;
- source coverage is partial;
- timestamp is stale;
- uncertainty is high;
- source is conceptual rather than empirical;
- input is usable only for design, dry-run, documentation review, or interface validation;
- downstream operational use is blocked.

Degraded inputs must preserve blocking gaps and forbidden downstream usage.

## 24. Block 01 Closure Criteria

Block 01 is closed when this document defines:

- the purpose of the Input Contract Layer;
- relationship with Block 00;
- permitted input families;
- input state model;
- required metadata fields;
- Motor B input rules;
- Regime Context input rules;
- Motor A macro/fundamental conceptual input rules;
- Motor C event / LLM conceptual input rules;
- Human Review metadata rules;
- synthetic dry-run rules;
- missing evidence rules;
- forbidden downstream usage propagation;
- confidence preservation rules;
- timestamp, schema version, and source reference rules;
- compatibility with `08 Risk Engine`;
- relationship with Block 02 and later blocks;
- acceptance, rejection, and degradation criteria.

Closing Block 01 does not create Motor B Adapter, Motor A Context Layer, Motor C Event Classifier, Signal Candidate Normalization, Bull/Bear Debate, Deterministic Signal Fusion, Confidence Aggregation, Risk Handoff, Paper Trading, Live Trading, execution logic, or capital allocation.
