# 07 Signal Fusion + LLM Motors - Confidence Status and Aggregation Policy

## 1. Purpose

Block 09 defines the Confidence Status and Aggregation Policy for `07 Signal Fusion + LLM Motors`.

The purpose is to govern how confidence fields are preserved, blocked, degraded, or left unavailable for fused signal candidates.

Confidence policy is not trade approval.

Confidence aggregation does not create empirical evidence.

Final signal confidence cannot be computed when Motor B is framework_only.

LLM confidence cannot replace backtest/OOS/robustness evidence.

Block 09 produces confidence governance metadata only. It does not authorize downstream usage.

## 2. Scope

This block covers:

- confidence governance definition;
- input contracts;
- output contract;
- `ConfidenceGovernanceResult` schema;
- confidence source taxonomy;
- `final_signal_confidence_status` enum;
- confidence score rules;
- deterministic aggregation policy;
- minimum governed evidence rule;
- capped-confidence policy;
- unavailable propagation rules;
- evidence-based degradation rules;
- confidence blocking rules;
- Motor B `framework_only` protection rules;
- Motor A context confidence rules;
- Motor C classification confidence rules;
- LLM confidence boundary rules;
- Bull/Bear disagreement handling;
- `FusedSignalCandidate` confidence handling;
- missing evidence handling;
- blocking gaps handling;
- synthetic and dry-run handling;
- human review triggers;
- audit and replay metadata requirements;
- relationship with 07-Block-10 Downstream Eligibility and Risk Handoff;
- relationship with `08 Risk Engine`.

This block does not implement Python code, trading logic, Paper Trading, Live Trading, execution, capital allocation, Risk Handoff, or Block 10.

## 3. Non-Authority Reminder

Block 09 is non-authoritative.

Block 09 must not:

- approve trades;
- approve strategies;
- authorize Paper Trading;
- authorize Live Trading;
- create execution readiness;
- allocate capital;
- relax risk limits;
- override `08 Risk Engine`;
- invent empirical evidence;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- calculate `final_signal_confidence_score` under `framework_only`;
- convert confidence governance into trade approval;
- convert confidence status into Paper Trading readiness;
- convert LLM confidence into empirical evidence;
- convert Bull/Bear agreement into confidence;
- convert fused signal alignment into confidence;
- convert synthetic data into evidence;
- create a ML ensemble.

Current Motor B state remains binding:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

## 4. Relationship With Blocks 00-08

Block 00 defines 07 boundaries and non-authority rules.

Block 01 defines accepted, degraded, rejected, unavailable, and synthetic input states.

Block 02 defines the Motor B Adapter and preserves Motor B confidence fields.

Block 03 defines Motor A context and uncertainty as context-only.

Block 04 defines Motor C classification confidence as event classification-only.

Block 05 defines LLM confidence boundaries and evidence rules.

Block 06 preserves confidence fields in `NormalizedSignalCandidate`.

Block 07 defines `DebateSummary`; disagreement scoring is not confidence scoring.

Block 08 defines `FusedSignalCandidate`; fusion does not create final signal confidence.

Block 09 consumes prior outputs and governs confidence status. It does not redefine prior contracts.

## 5. Definition Of Confidence Governance

Confidence governance is the deterministic policy layer that decides whether final signal confidence is unavailable, blocked, degraded, requires human review, or eligible for future computation.

Confidence governance does not assert profitability, robustness, production readiness, or trading approval.

Confidence governance preserves:

- source confidence fields;
- source uncertainty fields;
- source evidence completeness;
- missing evidence;
- blocking gaps;
- synthetic status;
- forbidden downstream usage;
- non-approval statements;
- audit references.

Under the current Motor B `framework_only` state, confidence governance primarily blocks unsupported confidence and preserves null scores.

## 6. Input Contracts

Block 09 may consume only:

1. `FusedSignalCandidate` from 07-Block-08 Deterministic Signal Fusion Engine.
2. `NormalizedSignalCandidate` references from 07-Block-06 Signal Candidate Normalization.
3. `DebateSummary` references from 07-Block-07 Bull/Bear Debate Layer.
4. Preserved Motor B confidence fields.
5. Preserved Motor A context confidence or uncertainty fields.
6. Preserved Motor C classification confidence fields.
7. Audit references and schema versions.

Inputs must be schema-versioned, audit-referenced, and linked to governed upstream artifacts.

## 7. Rejected Inputs

Block 09 must reject:

- raw Motor A input;
- raw Motor B input;
- raw Motor C input;
- raw LLM output;
- raw event, news, filing, social, or source text;
- raw strategy candidate;
- raw backtest claim;
- unversioned payload;
- unaudited confidence claim;
- confidence score without `confidence_status`;
- confidence score without source contract reference;
- payloads that claim confidence can approve trading.

Rejected inputs must not contribute to `ConfidenceGovernanceResult` except as rejected audit records.

## 8. Output Contract

The output of Block 09 is:

```text
ConfidenceGovernanceResult
```

`ConfidenceGovernanceResult` is a confidence governance artifact.

It is not Paper Trading authorization.

It is not Live Trading authorization.

It is not execution readiness.

It is not capital allocation.

It is not strategy promotion.

It is not a Risk Engine decision.

## 9. ConfidenceGovernanceResult Schema

The conceptual schema is:

```text
ConfidenceGovernanceResult
  confidence_governance_result_id
  related_fused_signal_candidate_id
  input_schema_versions
  confidence_policy_version
  motor_b_confidence_status
  motor_b_confidence_score
  motor_b_evidence_completeness_level
  motor_a_context_confidence_status
  motor_a_context_confidence_score
  motor_a_uncertainty_level
  motor_c_classification_confidence_status
  motor_c_classification_confidence_score
  motor_c_uncertainty_level
  llm_confidence_boundary_status
  bull_bear_disagreement_level
  evidence_completeness_level
  missing_evidence
  blocking_gaps
  unsupported_claims
  conflicting_sources
  synthetic_status
  final_signal_confidence_status
  final_signal_confidence_score
  confidence_aggregation_rule_applied
  confidence_cap_reason
  confidence_blocking_reason
  confidence_degradation_reasons
  requires_human_review
  paper_trading_eligibility
  downstream_operational_eligibility
  forbidden_downstream_usage
  non_approval_statement
  audit_references
  created_at
  schema_version
```

All fields must map to governed inputs, deterministic policy decisions, or explicit unavailable/null states.

## 10. Confidence Source Taxonomy

Allowed confidence source categories are:

```text
motor_b_trading_confidence
motor_a_context_confidence
motor_c_classification_confidence
llm_classification_confidence
bull_bear_disagreement_metadata
fused_candidate_metadata
synthetic_fixture_metadata
human_review_metadata
```

Rules:

- `motor_b_trading_confidence` is the only confidence layer tied to empirical trading validation.
- `motor_a_context_confidence` is context-only.
- `motor_c_classification_confidence` is event classification-only.
- `llm_classification_confidence` is classification metadata-only.
- `bull_bear_disagreement_metadata` is not confidence.
- `fused_candidate_metadata` is not confidence.
- `synthetic_fixture_metadata` is not confidence.
- `human_review_metadata` is not empirical backtest confidence.

## 11. final_signal_confidence_status Enum

Allowed `final_signal_confidence_status` values are:

```text
final_confidence_not_available
final_confidence_blocked_framework_only
final_confidence_blocked_missing_backtest
final_confidence_blocked_missing_oos
final_confidence_blocked_missing_robustness
final_confidence_blocked_synthetic_input
final_confidence_blocked_contract_violation
final_confidence_degraded_missing_evidence
final_confidence_degraded_conflicting_sources
final_confidence_degraded_high_uncertainty
final_confidence_requires_human_review
final_confidence_eligible_for_computation_later
```

Rules:

- under current Motor B `framework_only`, expected status is `final_confidence_blocked_framework_only` or `final_confidence_not_available`;
- do not use `confidence_high`, `confidence_medium`, or `confidence_low` for final trading confidence;
- do not create status values that imply trading readiness;
- do not create status values that imply paper trading readiness;
- do not create status values that imply live trading readiness.

## 12. Confidence Score Rules

`final_signal_confidence_score` must be null when `final_signal_confidence_status` is unavailable, blocked, degraded, synthetic, requires human review, or framework-only.

Under current state:

```text
final_signal_confidence_score = null
```

Block 09 must not invent `final_signal_confidence_score`.

Block 09 must not derive `final_signal_confidence_score` from Motor A, Motor C, LLM, Bull/Bear, or fusion metadata.

Any future non-null `final_signal_confidence_score` requires explicit empirical evidence from allowed upstream contracts.

Score scale, if ever allowed later, must be defined by an approved future contract and cannot be inferred here.

`motor_b_confidence_score` must preserve source nulls.

```text
confidence_status = confidence_not_available
confidence_score = null
```

must remain unchanged when sourced from current Motor B.

## 13. Aggregation Policy

Confidence aggregation is deterministic governance over status fields, not numeric averaging.

Required policies:

1. minimum governed evidence rule;
2. unavailable propagation rule;
3. framework-only blocking rule;
4. missing evidence blocking rule;
5. synthetic blocking rule;
6. LLM non-substitution rule;
7. debate non-substitution rule;
8. fusion non-substitution rule;
9. event classification non-substitution rule;
10. context non-substitution rule.

Under current Motor B `framework_only`, aggregation must block or return unavailable.

Aggregation must not create evidence, approval, operational eligibility, or a score.

## 14. Minimum Governed Evidence Rule

The minimum governed evidence rule states:

- final confidence cannot exceed the weakest required empirical evidence layer;
- if any required confidence layer is unavailable, final confidence is unavailable or blocked;
- if any required empirical evidence layer is missing, final confidence is blocked;
- the weakest governed evidence state dominates final confidence;
- favorable context cannot raise final confidence above empirical evidence support;
- favorable debate cannot raise final confidence above empirical evidence support;
- favorable event classification cannot raise final confidence above empirical evidence support.

## 15. Unavailable Propagation Rule

The unavailable propagation rule states:

- if Motor B `confidence_status = confidence_not_available`, final confidence must be unavailable or blocked;
- unavailable Motor A context confidence cannot be imputed;
- unavailable Motor C classification confidence cannot be imputed;
- unavailable LLM metadata cannot be treated as neutral confidence;
- unavailable debate metadata cannot improve confidence;
- unavailable fusion metadata cannot improve confidence.

Unavailable confidence must stay explicit and auditable.

## 16. Framework-Only Blocking Rule

The framework-only blocking rule states:

- if `evidence_completeness_level = framework_only`, final confidence is blocked;
- if Motor B is `framework_only`, final score remains null;
- framework-only documentation, synthetic examples, or mock results cannot become empirical evidence;
- favorable Motor A, Motor C, Bull/Bear, or fusion metadata cannot override this rule.

Expected current result:

```text
final_signal_confidence_status = final_confidence_blocked_framework_only
final_signal_confidence_score = null
```

or:

```text
final_signal_confidence_status = final_confidence_not_available
final_signal_confidence_score = null
```

when the candidate is explicitly unavailable rather than evaluable.

## 17. Missing Evidence Blocking Rule

The missing evidence blocking rule states:

- if backtest evidence is missing, final confidence cannot be computed;
- if OOS evidence is missing, final confidence cannot be computed;
- if walk-forward evidence is missing, final confidence cannot be computed;
- if robustness evidence is missing, final confidence cannot be computed;
- missing evidence must be reflected in `confidence_blocking_reason` or `confidence_degradation_reasons`;
- missing evidence cannot be hidden by fusion alignment or debate balance.

Allowed status outcomes include:

```text
final_confidence_blocked_missing_backtest
final_confidence_blocked_missing_oos
final_confidence_blocked_missing_robustness
final_confidence_degraded_missing_evidence
```

## 18. Synthetic Blocking Rule

If candidate input is `synthetic_dry_run_only`, final confidence cannot be computed.

Synthetic input must produce:

```text
final_signal_confidence_status = final_confidence_blocked_synthetic_input
final_signal_confidence_score = null
```

or `final_confidence_not_available` for unavailable synthetic placeholders.

Synthetic data cannot be used as evidence.

Synthetic data cannot authorize Paper Trading or Live Trading.

Synthetic data mixed with real input must require degradation, rejection, or human review unless explicitly marked as dry-run.

## 19. Non-Substitution Rules

### LLM non-substitution rule

LLM confidence cannot replace empirical evidence.

LLM confidence cannot replace backtest, OOS, walk-forward, or robustness evidence.

LLM confidence cannot fill Motor B `confidence_score`.

LLM confidence cannot fill `final_signal_confidence_score`.

### Debate non-substitution rule

Bull/Bear agreement cannot replace empirical evidence.

Debate non-substitution rule prevents `DebateSummary` from becoming confidence.

### Fusion non-substitution rule

Fused alignment cannot replace empirical evidence.

Fusion non-substitution rule prevents `FusedSignalCandidate` metadata from becoming confidence.

### Event classification non-substitution rule

Motor C classification confidence cannot replace trading confidence.

classification confidence is not trading confidence.

### Context non-substitution rule

Motor A context confidence cannot replace trading confidence.

Context confidence is not trading confidence.

## 20. Capped-Confidence Policy

Confidence may only be capped downward by:

- missing evidence;
- high uncertainty;
- conflicting sources;
- unsupported claims;
- stale context;
- weak source reliability;
- synthetic status;
- contract violation;
- `framework_only`.

Block 09 cannot cap upward.

Block 09 cannot upgrade confidence.

Under `framework_only`, the cap is null / unavailable.

Any future score must be capped by weakest evidence and contract state.

## 21. Evidence-Based Degradation Rules

Confidence status must degrade or require human review when:

- evidence is partial or unavailable;
- source reliability is weak, unknown, or conflicting;
- event severity is high or critical with uncertain sources;
- context is stale or unsupported;
- Bull/Bear disagreement is high or unresolved;
- unsupported claims affect the confidence interpretation;
- confidence metadata is malformed or incomplete.

Degradation cannot produce a non-null final score under current Motor B state.

## 22. Confidence Blocking Rules

Confidence must be blocked when:

- Motor B is `framework_only`;
- Motor B confidence is unavailable;
- required empirical evidence is missing;
- input is synthetic-only;
- contract validation fails;
- confidence score appears without status;
- confidence score appears without source contract reference;
- a payload attempts to convert confidence into approval;
- forbidden downstream usage is missing or weakened.

Blocked confidence must preserve `final_signal_confidence_score = null`.

## 23. Motor B framework_only Protection Rules

If any candidate is linked to Motor B `framework_only`, then `ConfidenceGovernanceResult` must preserve:

```text
evidence_completeness_level = framework_only
motor_b_confidence_status = confidence_not_available
motor_b_confidence_score = null
final_signal_confidence_score = null
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
```

`final_signal_confidence_status` must be:

```text
final_confidence_blocked_framework_only
```

or:

```text
final_confidence_not_available
```

when the input is explicitly unavailable.

`forbidden_downstream_usage` and `non_approval_statement` must remain explicit.

Motor A, Motor C, LLM, Bull/Bear, human review metadata, or fusion metadata cannot override this protection.

## 24. Motor A Context Confidence Rules

Motor A context confidence is context-only.

It may describe regime, macro, liquidity, volatility, or risk context uncertainty.

It cannot imply strategy validity.

It cannot imply profitability.

It cannot replace Motor B evidence.

It cannot fill `final_signal_confidence_score`.

`trend_bullish` or favorable context cannot increase final confidence when Motor B is `framework_only`.

Stale, missing, unsupported, or high-uncertainty Motor A context may degrade confidence governance or require human review.

## 25. Motor C Classification Confidence Rules

Motor C classification confidence is event classification-only.

It may describe quality of event classification.

It cannot imply strategy validity.

It cannot imply profitability.

It cannot replace Motor B evidence.

It cannot fill `final_signal_confidence_score`.

High-quality event classification cannot increase final trading confidence.

High or critical event uncertainty can degrade or require human review, but cannot compute final confidence.

## 26. LLM Confidence Boundary Rules

LLM confidence is not trading confidence.

LLM confidence cannot replace backtest/OOS/walk-forward/robustness.

LLM confidence cannot fill Motor B `confidence_score`.

LLM confidence cannot fill `final_signal_confidence_score`.

LLM confidence cannot convert unsupported claims into evidence.

LLM confidence cannot override missing sources.

LLM confidence cannot override `08 Risk Engine`.

LLM confidence must remain source-bound and schema-bound when present.

## 27. Bull/Bear Disagreement Handling

`disagreement_level` is not confidence.

Disagreement scoring is not confidence scoring.

Bull/Bear agreement does not increase confidence.

Bull/Bear disagreement does not mechanically decrease confidence.

High disagreement can require human review or degradation.

`DebateSummary` is argument metadata only.

Bull/Bear metadata can explain uncertainty, but cannot create final confidence.

## 28. FusedSignalCandidate Confidence Handling

FusedSignalCandidate is not confidence.

Fusion explanation is not confidence.

`source_motor_contributions` are not confidence.

`motor_weight_labels` are not confidence.

`event_precedence_outcome` is not confidence.

`fused_actionability_status` is not confidence.

Fused alignment cannot replace empirical evidence.

Fused direction cannot imply confidence.

Fused non-actionability must be preserved in confidence governance.

## 29. Missing Evidence Handling

Block 09 must preserve:

- `missing_evidence`;
- missing backtest evidence;
- missing OOS evidence;
- missing walk-forward evidence;
- missing robustness evidence;
- missing source references;
- missing context;
- missing confidence status;
- missing source contract references.

Missing evidence must drive blocked or unavailable confidence under current policy.

Missing evidence cannot be filled by LLM, context, event classification, debate, fusion, or human review metadata.

## 30. Blocking Gaps Handling

Block 09 must preserve `blocking_gaps`.

Blocking gaps must be included in:

- `confidence_blocking_reason`;
- `confidence_degradation_reasons`;
- `requires_human_review` when material;
- audit references.

Block 09 cannot close a blocking gap.

Block 09 cannot hide a blocking gap behind a confidence status.

## 31. Forbidden Downstream Usage Propagation

`forbidden_downstream_usage` must be propagated to `ConfidenceGovernanceResult`.

Under current Motor B `framework_only` state, it must include:

- trade approval;
- Paper Trading authorization;
- Live Trading authorization;
- execution;
- capital allocation;
- risk limit relaxation;
- strategy promotion;
- confidence invention;
- empirical evidence replacement.

Block 09 must not weaken, remove, or reinterpret forbidden downstream usage.

## 32. Synthetic And Dry-Run Handling

Synthetic and dry-run inputs must preserve `synthetic_status`.

Synthetic `ConfidenceGovernanceResult` records are allowed only for schema validation, interface validation, dry-run testing, documentation, or audit rehearsal.

Synthetic outputs cannot be used as evidence.

Synthetic outputs cannot be used for Paper Trading or Live Trading.

Synthetic outputs must carry:

```text
final_signal_confidence_score = null
```

and explicit `non_approval_statement`.

## 33. Human Review Triggers

Human review is required when:

- final confidence is blocked due to missing evidence;
- a `framework_only` candidate has favorable fusion result;
- event severity is high or critical;
- credible sources conflict;
- uncertainty is high;
- unsupported claims affect confidence interpretation;
- LLM confidence is inconsistent with source quality;
- confidence field is missing required status;
- non-null `confidence_score` appears without valid empirical evidence;
- synthetic input is mixed with real input;
- contract violation occurs;
- output attempts to convert confidence into approval.

Human review does not by itself create empirical confidence.

## 34. Audit And Replay Metadata Requirements

Every `ConfidenceGovernanceResult` must retain:

- confidence governance result ID;
- related fused signal candidate ID;
- input schema versions;
- confidence policy version;
- source confidence statuses and scores;
- evidence completeness level;
- missing evidence;
- blocking gaps;
- unsupported claims;
- conflicting sources;
- synthetic status;
- final signal confidence status;
- final signal confidence score;
- aggregation rule applied;
- cap reason;
- blocking reason;
- degradation reasons;
- human review requirement;
- forbidden downstream usage;
- non-approval statement;
- audit references;
- created_at;
- schema version.

Replay must show:

- which source confidence fields were preserved;
- which rule blocked, degraded, or left confidence unavailable;
- why score remained null;
- which evidence layers were missing;
- which forbidden usage restrictions were propagated;
- why downstream eligibility remains blocked.

## 35. Relationship With 07-Block-10 Downstream Eligibility And Risk Handoff

07-Block-10 Downstream Eligibility and Risk Handoff consumes `ConfidenceGovernanceResult`.

Block 10 defines downstream eligibility and Risk Handoff.

Block 09 does not authorize downstream usage.

Block 09 passes confidence blocks, missing evidence, blocking gaps, forbidden usage, downstream eligibility state, and non-approval status to Block 10.

Block 10 must not reinterpret blocked confidence as approval.

## 36. Relationship With 08 Risk Engine

`08 Risk Engine` retains final authority over downstream eligibility, veto, promotion, risk limits, and operational decisions.

`ConfidenceGovernanceResult` is not Paper Trading authorization.

`ConfidenceGovernanceResult` is not Live Trading authorization.

08 may veto any future fused signal candidate regardless of confidence status.

Under current Motor B `framework_only`, `ConfidenceGovernanceResult` must preserve:

```text
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
```

## 37. Explicit Prohibited Actions

Block 09 must not:

- implement trading logic;
- implement Paper Trading;
- implement Live Trading;
- create execution logic;
- create capital allocation;
- create Risk Handoff;
- create Block 10;
- modify the Motor B Output Contract of 06;
- modify Blocks 00-08;
- redefine prior contracts;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- calculate `final_signal_confidence_score` under `framework_only`;
- convert confidence governance into trade approval;
- convert confidence status into Paper Trading readiness;
- convert LLM confidence into empirical evidence;
- convert Bull/Bear agreement into confidence;
- convert fused signal alignment into confidence;
- convert synthetic data into evidence;
- create a ML ensemble.

## 38. Block 09 Closure Criteria

Block 09 is closed when this document defines:

- Confidence Status and Aggregation Policy purpose;
- scope;
- non-authority rules;
- relationship with Blocks 00-08;
- confidence governance;
- explicit statement that Confidence policy is not trade approval;
- explicit statement that Confidence aggregation does not create empirical evidence;
- explicit statement that Final signal confidence cannot be computed when Motor B is framework_only;
- explicit statement that LLM confidence cannot replace backtest/OOS/robustness evidence;
- input contracts;
- raw input rejection;
- output contract;
- `ConfidenceGovernanceResult` schema;
- confidence source taxonomy;
- `final_signal_confidence_status` enum;
- confidence score rules;
- aggregation policy;
- minimum governed evidence rule;
- capped-confidence policy;
- unavailable propagation rules;
- evidence-based degradation rules;
- confidence blocking rules;
- Motor B `framework_only` protection rules;
- Motor A context confidence rules;
- Motor C classification confidence rules;
- LLM confidence boundary rules;
- Bull/Bear disagreement handling;
- `FusedSignalCandidate` confidence handling;
- missing evidence handling;
- blocking gaps handling;
- synthetic and dry-run handling;
- human review triggers;
- audit and replay metadata requirements;
- relationship with 07-Block-10 Downstream Eligibility and Risk Handoff;
- relationship with `08 Risk Engine`.

Closing Block 09 does not implement confidence aggregation in code and does not create Risk Handoff, Paper Trading, Live Trading, execution logic, or capital allocation.
