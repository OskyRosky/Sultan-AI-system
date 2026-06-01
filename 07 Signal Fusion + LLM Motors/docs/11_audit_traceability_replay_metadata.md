# 07 Signal Fusion + LLM Motors - Audit, Traceability and Replay Metadata

## 1. Purpose

Block 11 defines Audit, Traceability and Replay Metadata for `07 Signal Fusion + LLM Motors`.

The purpose is to make every governed 07 artifact reconstructable from source inputs, contract references, schema versions, rule versions, prompt metadata, model metadata, deterministic decisions, missing evidence, blocking gaps, conflicts, forbidden downstream usage, and non-approval statements.

Audit metadata is not trade approval.

Replayability does not create empirical evidence.

Traceability does not create final signal confidence.

Audit records cannot override Motor B framework_only.

Block 11 documents how to reconstruct 07 outputs. It does not modify, approve, promote, or reinterpret them.

## 2. Scope

This block covers:

- input artifacts covered by 07 audit traceability;
- `Stage07AuditTrace` definition;
- `Stage07AuditTrace` schema;
- artifact reference requirements;
- schema and version metadata requirements;
- timestamp requirements;
- source input traceability;
- motor output traceability;
- LLM prompt and model metadata traceability;
- deterministic rule traceability;
- fusion decision path traceability;
- confidence governance traceability;
- risk handoff traceability;
- missing evidence and blocking gap traceability;
- forbidden downstream usage traceability;
- non-approval statement traceability;
- replay requirements;
- replay failure modes;
- immutability and mutation rules;
- human review traceability;
- synthetic and dry-run traceability;
- audit validation checklist;
- relationship with 07-Block-12 Mock and Dry-Run Test Fixtures;
- relationship with 07-Block-13 Quality Gates;
- relationship with 07-Block-14 Stage Closure and Handoff to 08;
- relationship with `08 Risk Engine`.

This block does not implement Python code, trading logic, Paper Trading, Live Trading, execution, capital allocation, Risk Engine behavior, mocks, quality gates, stage closure, or Block 12.

## 3. Non-Authority Reminder

Block 11 is non-authoritative.

Block 11 must not:

- approve trades;
- approve strategies;
- authorize Paper Trading;
- authorize Live Trading;
- create execution readiness;
- execute orders;
- allocate capital;
- relax risk limits;
- promote strategies;
- create `08 Risk Engine` approval;
- bypass `08 Risk Engine`;
- invent empirical evidence;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- create `final_signal_confidence_score`;
- create downstream operational eligibility under Motor B `framework_only`;
- convert audit completeness into approval;
- convert replay success into evidence;
- convert traceability into confidence;
- convert synthetic replay into evidence;
- modify previous 07 outputs.

Current Motor B state remains binding in every audit trace:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

## 4. Relationship With Blocks 00-10

Block 00 defines stage boundaries and non-authority rules.

Block 01 defines input contracts, input states, required audit metadata, and preservation rules.

Block 02 defines `NormalizedMotorBInput` and Motor B `framework_only` preservation.

Block 03 defines `MotorAContextOutput` as market context, not trading evidence.

Block 04 defines `MotorCEventOutput` as event classification metadata, including source and LLM metadata.

Block 05 defines LLM safety, prompt contracts, model metadata, fallback, validation, and replay boundaries.

Block 06 defines `NormalizedSignalCandidate`.

Block 07 defines `DebateSummary`.

Block 08 defines `FusedSignalCandidate`.

Block 09 defines `ConfidenceGovernanceResult`.

Block 10 defines `RiskHandoffPackage`.

Block 11 links those artifacts into a replayable audit trace. It does not redefine their contracts or change their decisions.

## 5. Definition Of Stage07AuditTrace

`Stage07AuditTrace` is the stage-level trace record that links governed 07 artifacts from accepted inputs through the final `RiskHandoffPackage`.

It records:

- source artifact IDs;
- contract and schema references;
- version metadata;
- prompt and model metadata;
- deterministic rule versions;
- validation and replay status;
- missing evidence;
- blocking gaps;
- unsupported claims;
- conflicting sources;
- forbidden downstream usage;
- non-approval statements;
- synthetic and human review metadata.

`Stage07AuditTrace` is audit metadata, not approval.

It is not Paper Trading authorization.

It is not Live Trading authorization.

It is not execution authorization.

It is not capital allocation.

It is not empirical validation.

It is not final signal confidence.

## 6. Input Artifacts Covered

Block 11 covers traceability for at least:

- MotorBAdapter output / `NormalizedMotorBInput`;
- `MotorAContextOutput`;
- `MotorCEventOutput`;
- `NormalizedSignalCandidate`;
- `DebateSummary`;
- `FusedSignalCandidate`;
- `ConfidenceGovernanceResult`;
- `RiskHandoffPackage`;
- `human_review_metadata` if present;
- synthetic fixture metadata if present.

Raw inputs may be referenced only as source artifacts or rejected/unavailable records. Block 11 must not turn raw inputs into governed outputs.

## 7. Output Contract

The output of Block 11 is:

```text
Stage07AuditTrace
```

`Stage07AuditTrace` must be sufficient to reconstruct the 07 decision path from governed source artifacts through `RiskHandoffPackage` without inventing evidence, changing decisions, or relying on hidden context.

If required audit metadata is missing, `Stage07AuditTrace` must mark replay as degraded, unavailable, or rejected according to the replay failure mode taxonomy.

## 8. Stage07AuditTrace Schema

The conceptual schema is:

```text
Stage07AuditTrace
  stage07_audit_trace_id
  trace_schema_version
  stage_id
  repository_path
  run_or_dry_run_id
  source_artifact_ids
  source_contract_references
  source_schema_versions
  input_contract_versions
  motor_b_contract_reference
  motor_b_evidence_completeness_level
  motor_b_confidence_status
  motor_b_confidence_score
  motor_a_context_refs
  motor_c_event_refs
  normalized_signal_candidate_refs
  debate_summary_refs
  fused_signal_candidate_refs
  confidence_governance_result_refs
  risk_handoff_package_refs
  prompt_template_ids
  prompt_versions
  llm_model_metadata_refs
  deterministic_rule_versions
  normalization_rule_version
  debate_validation_rule_version
  fusion_rule_version
  confidence_policy_version
  risk_handoff_policy_version
  event_precedence_policy_version
  conflict_resolution_policy_version
  forbidden_downstream_usage_policy_version
  validation_status
  replay_status
  replay_limitations
  missing_evidence
  blocking_gaps
  unsupported_claims
  conflicting_sources
  forbidden_downstream_usage
  non_approval_statement
  synthetic_status
  human_review_refs
  created_at
  created_by_process
  audit_references
```

Unavailable fields must remain null, unavailable, blocked, rejected, or explicitly limited according to source artifact semantics.

## 9. Artifact Reference Requirements

Every artifact must have a unique ID.

Every artifact must reference its source artifacts.

Every artifact must reference `schema_version`.

Every artifact must reference the contract or block that produced it.

Every downstream artifact must preserve upstream audit references.

Artifact references must not be replaced by summaries only.

Missing artifact references must make replay degraded or unavailable.

Artifact references must be stable enough to reconstruct the path from:

```text
NormalizedMotorBInput / MotorAContextOutput / MotorCEventOutput
-> NormalizedSignalCandidate
-> DebateSummary
-> FusedSignalCandidate
-> ConfidenceGovernanceResult
-> RiskHandoffPackage
-> Stage07AuditTrace
```

## 10. Schema And Version Metadata Requirements

Each trace must preserve:

- block document version or revision reference;
- `schema_version`;
- `rule_version`;
- `prompt_version`;
- model version or snapshot;
- contract reference;
- repository commit or revision reference when available;
- `created_at` timestamp.

Version metadata supports replay.

Version metadata does not create evidence.

Version metadata does not approve usage.

Unversioned payloads must make replay degraded, unavailable, or rejected depending on materiality.

## 11. Timestamp Requirements

Required timestamps include:

- `source_timestamp`;
- `ingestion_timestamp`;
- `classification_timestamp`;
- `normalization_timestamp`;
- `debate_timestamp`;
- `fusion_timestamp`;
- `confidence_governance_timestamp`;
- `risk_handoff_timestamp`;
- `audit_trace_created_at`.

If a timestamp is missing, `replay_status` must be degraded or unavailable.

Missing timestamps cannot be inferred silently.

Timestamps must preserve timezone or UTC convention.

Replay must disclose when ordering cannot be proven because timestamp metadata is incomplete.

## 12. Source Input Traceability

Source input traceability must preserve:

- accepted, degraded, rejected, synthetic, or unavailable input status;
- source contract references;
- source schema versions;
- source artifact IDs;
- source timestamps;
- ingestion timestamps;
- source references;
- limitations;
- missing context;
- missing sources;
- unsupported claims;
- conflicting sources;
- forbidden downstream usage;
- non-approval statements where applicable.

Source traceability does not convert raw input into evidence.

Rejected source input must remain visible as rejected or unavailable audit metadata when it affects replay.

## 13. Motor Output Traceability

Motor B traceability must preserve:

- Motor B contract reference;
- Motor B adapter output ID;
- `evidence_completeness_level = framework_only` when applicable;
- `paper_trading_eligibility = blocked`;
- `downstream_operational_eligibility = blocked`;
- `confidence_status = confidence_not_available`;
- `confidence_score = null`;
- `approval_status`;
- `non_approval_statement`;
- missing evidence;
- blocking gaps;
- forbidden downstream usage.

Motor A traceability must preserve:

- Motor A context output ID;
- regime label;
- context label;
- regime metadata;
- conceptual base motor weights;
- activation rule outcomes;
- uncertainty level;
- stale or missing context flags;
- limitations;
- audit references.

Motor C traceability must preserve:

- Motor C event output ID;
- event type and subtype;
- severity;
- affected assets and markets;
- expected duration;
- source reliability label;
- source references;
- `classification_confidence_status`;
- `classification_confidence_score`;
- unsupported claims;
- missing sources;
- conflicting sources;
- event precedence hint;
- LLM metadata where applicable.

Motor output traceability cannot upgrade confidence, evidence, eligibility, or approval.

## 14. LLM Prompt And Model Metadata Traceability

LLM-assisted artifacts must retain:

- `prompt_template_id`;
- `prompt_version`;
- prompt contract reference;
- `model_provider`;
- `model_id`;
- `model_version_or_snapshot`;
- model parameters reference if available;
- input artifact IDs passed to the LLM;
- output schema version;
- validation status;
- fallback status;
- unsupported claims;
- missing sources;
- conflicting sources;
- prompt injection flags if present.

LLM output without prompt metadata must be degraded or rejected for replay.

LLM output without source references must preserve `unsupported_claims`.

Model metadata does not create confidence.

Prompt metadata does not create evidence.

Replay does not require the model to reproduce identical language, but must reconstruct the decision path and original output artifact.

If the original model is unavailable, `replay_status` must disclose non-identical runtime.

## 15. Deterministic Rule Traceability

Every trace must preserve deterministic rule identifiers when applicable:

- `normalization_rule_version`;
- `debate_validation_rule_version`;
- `fusion_rule_version`;
- `event_precedence_policy_version`;
- `confidence_policy_version`;
- `risk_handoff_policy_version`;
- `conflict_resolution_policy_version`;
- `forbidden_downstream_usage_policy_version`.

Replay must show which deterministic rules were applied.

Replay must show which blocking rule dominated.

Replay must show which favorable context was ignored, degraded, or preserved.

Replay must show why Motor B `framework_only` remained binding.

Replay must show why `confidence_score` remained null.

Replay must show why `final_signal_confidence_score` remained null.

## 16. Fusion Decision Path Traceability

For `FusedSignalCandidate`, the trace must preserve:

- input `NormalizedSignalCandidate` IDs;
- input `DebateSummary` IDs;
- source motor contribution metadata;
- motor availability and limitations;
- base weighting policy labels;
- event precedence policy version;
- event precedence outcome;
- conflict resolution policy;
- unresolved conflicts;
- fused direction and actionability status;
- missing evidence;
- blocking gaps;
- forbidden downstream usage;
- non-approval statement.

Fusion decision path traceability is explanation metadata, not confidence and not investment advice.

## 17. Confidence Governance Traceability

For `ConfidenceGovernanceResult`, the trace must preserve:

- confidence governance result ID;
- confidence policy version;
- Motor B confidence status and score;
- Motor A context confidence or uncertainty fields;
- Motor C classification confidence fields;
- LLM confidence boundary status;
- Bull/Bear disagreement metadata;
- final signal confidence status;
- final signal confidence score;
- confidence blocking reason;
- confidence degradation reasons;
- missing evidence;
- blocking gaps;
- forbidden downstream usage;
- non-approval statement.

Under current Motor B `framework_only`, replay must show:

```text
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

Confidence traceability cannot create confidence.

## 18. Risk Handoff Traceability

For `RiskHandoffPackage`, the trace must preserve:

- risk handoff package ID;
- handoff schema version;
- related fused signal candidate ID;
- related confidence governance result ID;
- normalized signal candidate references;
- debate summary references;
- eligibility status;
- required Risk Engine action;
- event risk status;
- veto reasons;
- review reasons;
- handoff limitations;
- human review requirement;
- forbidden downstream usage;
- non-approval statement.

Risk handoff traceability must show why Block 10 structured information for `08 Risk Engine` without deciding for `08 Risk Engine`.

Risk handoff traceability cannot convert review routing into approval.

## 19. Missing Evidence And Blocking Gaps Traceability

`missing_evidence` must be preserved from upstream artifacts.

`blocking_gaps` must be preserved from upstream artifacts.

`unsupported_claims` must be preserved.

`conflicting_sources` must be preserved.

Missing evidence cannot be marked resolved by Block 11.

Blocking gaps cannot be closed by Block 11.

Block 11 only records them.

Replay must show where each missing evidence item or blocking gap first appeared and how later artifacts propagated it.

## 20. Forbidden Downstream Usage Traceability

`forbidden_downstream_usage` must preserve and propagate bans on:

- trade approval;
- Paper Trading authorization;
- Live Trading authorization;
- execution;
- capital allocation;
- risk limit relaxation;
- strategy promotion;
- confidence invention;
- empirical evidence replacement.

Audit trace must show which upstream artifact introduced each forbidden usage item and which downstream artifacts preserved it.

Block 11 must not weaken, remove, rename into permissive language, or reinterpret forbidden downstream usage.

## 21. Non-Approval Statement Traceability

Every audit trace must preserve `non_approval_statement`.

`non_approval_statement` must be linked to source artifacts.

`non_approval_statement` must remain visible in replay.

Missing `non_approval_statement` makes replay degraded or contract-violating.

Audit trace cannot convert non-approval into approval.

Under current Motor B `framework_only`, non-approval must remain visible through `RiskHandoffPackage`.

## 22. Replay Requirements

Replay must allow reconstruction of:

1. Which inputs were accepted, degraded, rejected, synthetic, or unavailable.
2. How Motor B restrictions were preserved.
3. How Motor A context was normalized and bounded.
4. How Motor C event metadata was normalized and bounded.
5. How LLM output was validated or degraded.
6. How `NormalizedSignalCandidate` was produced.
7. How Bull/Bear `DebateSummary` was produced.
8. How `FusedSignalCandidate` was produced.
9. Which event precedence rule was applied.
10. Which conflict handling rule was applied.
11. Which confidence governance rule blocked or degraded confidence.
12. Why `final_signal_confidence_score` is null.
13. How `RiskHandoffPackage` was built.
14. Why `forbidden_downstream_usage` remains preserved.
15. Why `non_approval_statement` remains explicit.

Replay must not require hidden model memory, unrecorded prompts, unversioned code behavior, or uncaptured raw context.

## 23. Replay Failure Modes

Allowed `replay_status` values are:

```text
replay_available
replay_available_with_limitations
replay_degraded_missing_artifact
replay_degraded_missing_timestamp
replay_degraded_missing_schema_version
replay_degraded_missing_prompt_metadata
replay_degraded_model_unavailable
replay_unavailable_missing_source_artifacts
replay_unavailable_contract_violation
replay_unavailable_unversioned_payload
replay_rejected_integrity_failure
```

Rules:

- replay failure must not create eligibility;
- replay failure must not create confidence;
- replay failure must not remove `non_approval_statement`;
- replay degraded or unavailable status must be passed downstream as limitation;
- replay rejected status must preserve the reason and affected artifact IDs.

## 24. Immutability And Mutation Rules

Audit trace should be append-only in principle.

Existing audit records must not be silently overwritten.

Corrections must create a new revision or correction note.

Manual overrides must be explicitly recorded with reviewer, timestamp, reason, and scope.

Human review does not erase original machine output.

Replay artifacts must preserve original outputs and later corrections separately.

Mutation metadata must never be used to hide missing evidence, blocking gaps, unsupported claims, or forbidden downstream usage.

## 25. Human Review Traceability

Human review traceability must include:

- `human_review_required`;
- reviewer ID or reviewer role if available;
- review timestamp;
- review reason;
- review scope;
- review outcome;
- review limitations;
- human override flag if any;
- link to original artifact.

Human review metadata is not empirical trading evidence.

Human review does not override Motor B `framework_only` unless a future Risk Engine explicitly defines such authority.

Human review must not erase missing evidence or blocking gaps.

Human review must remain separate from machine-generated outputs and deterministic rule outcomes.

## 26. Synthetic And Dry-Run Traceability

Synthetic artifacts must be clearly marked.

Dry-run artifacts must be clearly marked.

`synthetic_status` must propagate through audit trace.

Synthetic replay is allowed only for interface validation, schema validation, dry-run testing, documentation, or audit rehearsal.

Synthetic replay cannot be used as evidence.

Synthetic replay cannot be used for Paper Trading or Live Trading.

Synthetic replay must carry explicit `non_approval_statement`.

## 27. Audit Validation Checklist

A `Stage07AuditTrace` is valid only when it can show:

- unique trace ID;
- source artifact IDs;
- source contract references;
- source_schema_versions;
- schema and rule versions;
- timestamps or explicit timestamp limitations;
- prompt_template_ids when LLM-assisted artifacts exist;
- prompt_versions when LLM-assisted artifacts exist;
- llm_model_metadata_refs when LLM-assisted artifacts exist;
- deterministic_rule_versions;
- `fusion_rule_version`;
- `confidence_policy_version`;
- `risk_handoff_policy_version`;
- replay_status;
- missing_evidence;
- blocking_gaps;
- forbidden_downstream_usage;
- non_approval_statement;
- synthetic_status;
- human_review_refs when applicable;
- preservation of Motor B `framework_only` restrictions.

If any required checklist item is missing, replay must be degraded, unavailable, or rejected.

## 28. Relationship With Block 12 Mock And Dry-Run Test Fixtures

07-Block-12 Mock and Dry-Run Test Fixtures will define mock and dry-run fixtures.

Block 11 defines how synthetic and dry-run traces must be labeled and replayed.

Block 11 does not create mocks.

Block 11 does not convert mock outputs into evidence.

## 29. Relationship With Block 13 Quality Gates

07-Block-13 Quality Gates will define quality gates.

Block 11 provides audit metadata needed for quality gate verification.

Block 11 does not close quality gates by itself.

Quality gates must treat missing audit metadata, missing version references, missing non-approval statements, and replay failures as gate inputs, not as approvals.

## 30. Relationship With Block 14 Stage Closure

07-Block-14 Stage Closure and Handoff to 08 will close the stage and prepare handoff to 08.

Block 11 provides replay and audit inputs needed for closure.

Block 11 does not perform stage closure.

Stage closure must preserve Block 11 trace limitations and non-approval status.

## 31. Relationship With 08 Risk Engine

`08 Risk Engine` retains final authority over downstream eligibility, veto, promotion, risk limits, and operational decisions.

`Stage07AuditTrace` is audit metadata, not approval.

`08 Risk Engine` must receive enough traceability to review or veto.

Audit trace cannot bypass Risk Engine.

Audit trace cannot authorize downstream use.

Audit trace must preserve missing evidence, blocking gaps, forbidden downstream usage, non-approval statements, replay limitations, and Motor B `framework_only` state for `08 Risk Engine`.

## 32. Explicit Prohibited Actions

Block 11 must not:

- implement trading logic;
- implement Paper Trading;
- implement Live Trading;
- create execution logic;
- create capital allocation;
- create Risk Engine;
- create mocks;
- create Block 12;
- create quality gates;
- create Block 13;
- create stage closure;
- create Block 14;
- modify the Motor B Output Contract of 06;
- modify Blocks 00-10;
- redefine prior contracts;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- create downstream operational eligibility under `framework_only`;
- convert audit completeness into approval;
- convert replay success into evidence;
- convert traceability into confidence;
- convert synthetic replay into evidence;
- create a ML ensemble.

## 33. Block 11 Closure Criteria

Block 11 is closed when this document defines:

- Audit, Traceability and Replay Metadata purpose;
- scope;
- non-authority rules;
- relationship with Blocks 00-10;
- `Stage07AuditTrace`;
- explicit statement that Audit metadata is not trade approval;
- explicit statement that Replayability does not create empirical evidence;
- explicit statement that Traceability does not create final signal confidence;
- explicit statement that Audit records cannot override Motor B framework_only;
- input artifacts covered;
- output contract;
- `Stage07AuditTrace` schema;
- artifact reference requirements;
- schema and version metadata requirements;
- timestamp requirements;
- source input traceability;
- motor output traceability;
- LLM prompt and model metadata traceability;
- deterministic rule traceability;
- fusion decision path traceability;
- confidence governance traceability;
- risk handoff traceability;
- missing evidence and blocking gap traceability;
- forbidden downstream usage traceability;
- non-approval statement traceability;
- replay requirements;
- replay failure modes;
- immutability and mutation rules;
- human review traceability;
- synthetic and dry-run traceability;
- audit validation checklist;
- relationship with 07-Block-12 Mock and Dry-Run Test Fixtures;
- relationship with 07-Block-13 Quality Gates;
- relationship with 07-Block-14 Stage Closure and Handoff to 08;
- relationship with `08 Risk Engine`.

Closing Block 11 does not create mocks, quality gates, stage closure, Block 12, Block 13, Block 14, Risk Engine behavior, Paper Trading, Live Trading, execution logic, or capital allocation.
