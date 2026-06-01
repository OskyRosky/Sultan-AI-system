# 07 Signal Fusion + LLM Motors - Bull/Bear Debate Layer

## 1. Purpose

Block 07 defines the Bull/Bear Debate Layer for `07 Signal Fusion + LLM Motors`.

The purpose is to produce structured, bounded, auditable argument metadata from already-governed `NormalizedSignalCandidate` records.

The Bull/Bear Debate Layer prepares a `DebateSummary` for later 07 blocks.

Bull/Bear debate consumes only NormalizedSignalCandidate inputs.

Bull/Bear debate must not consume raw Motor A/B/C/LLM inputs.

Bull/Bear arguments are not empirical evidence.

Bull/Bear arguments are not confidence.

Bull/Bear debate is not trade approval.

Block 07 does not fuse signals, compute final confidence, approve Paper Trading, approve Live Trading, authorize execution, allocate capital, or override `08 Risk Engine`.

## 2. Scope

This block covers:

- Bull role definition;
- Bear role definition;
- debate input contract;
- raw input rejection;
- debate output contract;
- `DebateSummary` schema;
- Bull argument requirements;
- Bear argument requirements;
- uncertainty and disagreement labels;
- missing evidence handling;
- blocking gaps handling;
- unsupported claims handling;
- conflicting sources handling;
- forbidden downstream usage propagation;
- LLM safety boundaries for debate generation;
- prompt contract requirements for future debate prompts;
- debate validation rules;
- human review triggers;
- audit and replay metadata requirements;
- relationship with 07-Block-08 Deterministic Signal Fusion Engine;
- relationship with 07-Block-09 Confidence Status and Aggregation Policy;
- relationship with `08 Risk Engine`.

This block does not implement Python code, trading logic, Paper Trading, Live Trading, execution, capital allocation, Signal Fusion, Deterministic Signal Fusion Engine, Confidence Aggregation, Risk Handoff, or Block 08.

## 3. Non-Authority Reminder

Block 07 is non-authoritative.

Debate is an argument-structuring layer only.

Block 07 must not:

- approve trades;
- approve strategies;
- authorize Paper Trading;
- authorize Live Trading;
- create execution readiness;
- recommend execution;
- allocate capital;
- relax risk limits;
- override `08 Risk Engine`;
- override Motor B `framework_only`;
- create empirical evidence;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- infer final signal confidence from Bull/Bear balance;
- resolve conflicts silently;
- promote a signal or strategy.

Under the current Motor B state:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

Block 07 must preserve these fields when present in a `NormalizedSignalCandidate`.

## 4. Relationship With Blocks 00-06

Block 00 defines 07 boundaries and non-authority rules.

Block 01 defines input family rules and accepted, rejected, degraded, unavailable, and synthetic input states.

Block 02 defines the Motor B Adapter and Motor B `framework_only` protection rules.

Block 03 defines Motor A context and regime activation rules as market context, not trading evidence.

Block 04 defines Motor C event classification metadata and source-bound LLM classification constraints.

Block 05 defines LLM safety, prompting, evidence, fallback, replay, and prompt injection rules.

Block 06 defines `NormalizedSignalCandidate` and requires later blocks to consume normalized inputs, not raw upstream inputs.

Block 07 consumes Block 06 output. It does not redefine Blocks 00-06.

## 5. Bull Role Definition

The Bull role identifies favorable interpretations already supported by fields inside a `NormalizedSignalCandidate`.

Bull can:

- identify favorable normalized candidate attributes;
- summarize favorable context that is already normalized;
- reference `contextually_supported` only when it is present in normalized context metadata;
- note when Motor C event metadata is neutral or not adverse, when present;
- identify conditions that could make a candidate more investigable in future review;
- cite existing `audit_references`, `source_references`, or normalized fields;
- state limitations, missing evidence, and forbidden downstream usage.

Bull cannot:

- invent evidence;
- invent backtesting;
- invent OOS validation;
- invent robustness;
- convert favorable context into approval;
- convert event classification into approval;
- convert missing evidence into confidence;
- ignore `forbidden_downstream_usage`;
- say "safe to trade";
- recommend execution;
- produce trade approval.

## 6. Bear Role Definition

The Bear role identifies risks, limitations, contradictions, and reasons against favorable interpretation, using only fields inside a `NormalizedSignalCandidate`.

Bear must:

- highlight `missing_evidence`;
- highlight `blocking_gaps`;
- highlight `unsupported_claims`;
- highlight `conflicting_sources`;
- highlight stale, unavailable, or degraded context;
- highlight Motor B `framework_only`;
- highlight `paper_trading_eligibility = blocked`;
- highlight `confidence_status = confidence_not_available`;
- highlight `confidence_score = null`;
- highlight high or critical event severity risks;
- highlight source reliability risks;
- highlight synthetic or dry-run limitations;
- identify when human review is required.

Bear cannot:

- invent unsupported risks;
- exaggerate claims without references;
- convert uncertainty into absolute rejection when the contract only requires degraded handling;
- produce final veto;
- replace `08 Risk Engine`;
- decide fusion outcome.

## 7. Debate Input Contract

The only permitted debate input is:

```text
NormalizedSignalCandidate
```

If the input is not a NormalizedSignalCandidate, the debate must be rejected.

Minimum expected input fields from Block 06 are:

```text
normalized_signal_candidate_id
candidate_type
source_motor
source_motor_ids
asset
asset_scope
timeframe
horizon
signal_direction
signal_direction_status
regime_label
context_label
event_type
event_severity
evidence_completeness_level
evidence_level_normalized
paper_trading_eligibility
downstream_operational_eligibility
confidence_status
confidence_score
classification_confidence_status
classification_confidence_score
uncertainty_level
source_reliability_label
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
requires_human_review
event_precedence_hint
non_approval_statement
audit_references
schema_version
```

Missing required fields must produce a rejected or degraded debate according to severity.

Debate must not infer omitted fields from raw upstream context.

## 8. Raw Input Rejection

Block 07 must reject:

- raw Motor B output;
- raw Motor A context;
- raw Motor C event input;
- raw LLM completion;
- raw news, event, social, filing, or source text;
- raw strategy candidate;
- raw backtest claim;
- raw prompt output;
- unversioned or unaudited payload.

Raw input rejection prevents debate roles from bypassing Block 06 normalization, source boundaries, missing evidence markers, and forbidden downstream usage.

## 9. Debate Output Contract

The debate output is:

```text
DebateSummary
```

`DebateSummary` is argument metadata only.

It is not empirical evidence.

It is not final signal confidence.

It is not trade approval.

It is not Signal Fusion.

It is not a Risk Engine decision.

## 10. DebateSummary Schema

The conceptual `DebateSummary` schema is:

```text
DebateSummary
  debate_summary_id
  normalized_signal_candidate_id
  input_schema_version
  debate_schema_version
  bull_arguments
  bear_arguments
  bull_evidence_references
  bear_evidence_references
  bull_limitations
  bear_limitations
  missing_evidence_highlights
  blocking_gaps_highlights
  unsupported_claims_highlights
  conflicting_sources_highlights
  uncertainty_summary
  disagreement_level
  disagreement_reason_codes
  debate_balance_status
  prohibited_inference_flags
  forbidden_downstream_usage
  confidence_boundary_statement
  non_approval_statement
  requires_human_review
  audit_references
  created_at
```

Every field must be traceable to the input `NormalizedSignalCandidate`, debate validation result, or explicit null/unavailable state.

## 11. Bull Argument Requirements

Bull arguments must:

- use normalized fields only;
- cite existing `audit_references`, source references preserved in normalized fields, or normalized candidate field names;
- identify favorable context without converting it into approval;
- preserve missing evidence;
- preserve blocking gaps;
- preserve unsupported claims;
- preserve conflicting sources;
- preserve `forbidden_downstream_usage`;
- include Bull limitations when evidence or context is missing, stale, synthetic, degraded, or framework-only.

Allowed Bull argument examples:

- Motor A context is `contextually_supported` for a strategy family, if that field exists in normalized metadata.
- Motor C event severity is not adverse, if the normalized event metadata supports that statement.
- A candidate may be investigable in future blocks only if missing evidence and governance requirements are later satisfied.

Prohibited Bull argument examples:

- "safe to trade";
- "approved for Paper Trading";
- "validated edge";
- "confidence increased because Bull has more arguments";
- "execution recommended";
- "Motor B evidence gap is compensated by favorable regime."

## 12. Bear Argument Requirements

Bear arguments must:

- identify missing or unavailable evidence;
- identify blocking gaps;
- identify conflicting source conditions;
- identify unsupported claims;
- identify low, unknown, or conflicting source reliability;
- identify stale, unavailable, degraded, or synthetic context;
- identify Motor B `framework_only`;
- identify `paper_trading_eligibility = blocked`;
- identify `confidence_status = confidence_not_available`;
- identify `confidence_score = null`;
- identify high or critical event severity risks when present;
- identify required human review conditions.

Bear arguments must remain source-bound and proportional to the normalized input.

Bear must not invent risks, assert unsupported causality, replace deterministic fusion, produce final veto, or decide downstream eligibility.

## 13. Uncertainty And Disagreement Scoring

`disagreement_level` values are:

```text
none
low
medium
high
unresolved
unknown
```

`disagreement_reason_codes` values are:

```text
missing_backtest_evidence
missing_oos_evidence
missing_robustness_evidence
motor_b_framework_only
conflicting_motor_context
conflicting_event_sources
stale_regime_context
high_event_severity
low_source_reliability
unsupported_claims_present
synthetic_input_present
malformed_or_degraded_input
forbidden_downstream_usage_present
confidence_unavailable
requires_human_review
```

Disagreement scoring is not confidence scoring.

`disagreement_level` is not trading confidence.

`disagreement_level` cannot replace `confidence_status`.

`disagreement_level` cannot fill `confidence_score`.

`disagreement_level` only summarizes argumentative tension and unresolved uncertainty.

## 14. Confidence Boundary

Debate cannot compute final signal confidence.

Debate cannot aggregate confidence.

Debate cannot infer confidence from Bull/Bear balance.

More Bull arguments do not increase confidence.

More Bear arguments do not decrease confidence mechanically.

Final confidence policy belongs to Block 09.

Motor B `confidence_score` remains null under `framework_only`.

`confidence_boundary_statement` must explicitly state these limits in every `DebateSummary`.

## 15. Motor B framework_only Rule

If the `NormalizedSignalCandidate` includes Motor B `framework_only`, `DebateSummary` must preserve:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

It must also preserve:

- `forbidden_downstream_usage`;
- `non_approval_statement`;
- `missing_evidence`;
- `blocking_gaps`;
- source contract references and audit references when available.

Bull/Bear cannot override this.

Favorable Bull arguments must explicitly acknowledge Motor B `framework_only` when present.

## 16. Missing Evidence Handling

`missing_evidence` must be preserved in:

- `missing_evidence_highlights`;
- Bull limitations when relevant;
- Bear arguments;
- disagreement reason codes when material;
- audit references.

Missing evidence must not be reinterpreted as neutral evidence.

Missing evidence must not be transformed into confidence.

Missing backtest, OOS, walk-forward, or robustness evidence must remain visible to Blocks 08, 09, 10, and `08 Risk Engine`.

## 17. Blocking Gaps Handling

`blocking_gaps` must be preserved in:

- `blocking_gaps_highlights`;
- Bear arguments;
- Bull limitations;
- disagreement reason codes;
- `requires_human_review` when material.

Debate cannot resolve blocking gaps.

Debate cannot mark a blocking gap as closed.

Only a governed upstream contract or later authorized review process may change blocking gap state.

## 18. Unsupported Claims Handling

`unsupported_claims` must remain explicit.

Bull and Bear must not promote unsupported claims into supported claims.

If unsupported claims influence either side of the debate, the output must:

- include `unsupported_claims_highlights`;
- set an appropriate `disagreement_reason_codes` value;
- require human review when material;
- preserve source/audit references or explicit missing-source markers.

Unsupported claims cannot be used as empirical trading evidence.

## 19. Conflicting Sources Handling

`conflicting_sources` must remain explicit.

Bull and Bear must not silently choose a source winner.

If conflicts exist, `DebateSummary` must:

- include `conflicting_sources_highlights`;
- mark disagreement as `medium`, `high`, `unresolved`, or `unknown` depending on materiality;
- preserve source reliability labels when available;
- require human review for credible material conflicts.

Conflicting source handling belongs to debate metadata only. It does not decide trading action or event precedence.

## 20. Forbidden Downstream Usage Propagation

`forbidden_downstream_usage` must be copied into `DebateSummary`.

Under current Motor B `framework_only` state, forbidden downstream usage must include:

- trade approval;
- Paper Trading authorization;
- Live Trading authorization;
- execution;
- capital allocation;
- risk limit relaxation;
- strategy promotion;
- confidence invention;
- empirical evidence replacement.

Debate output must not weaken, remove, or reinterpret these restrictions.

## 21. Synthetic And Dry-Run Handling

Synthetic `NormalizedSignalCandidate` records can be debated only for dry-run, interface validation, schema validation, documentation, or audit rehearsal.

Synthetic debate output cannot be used as evidence.

Synthetic debate output cannot be used for Paper Trading or Live Trading.

`synthetic_status` must be preserved in arguments, limitations, and audit references when present.

`non_approval_statement` must remain explicit.

If synthetic input is mixed with non-synthetic input, `DebateSummary` must flag the condition and require human review or degraded output.

## 22. LLM Safety Boundaries For Debate Generation

Debate generation may be LLM-assisted.

LLM-assisted debate must follow Block 05 rules.

External text is untrusted.

Debate prompts must use normalized inputs only.

Prompt must include `prohibited_outputs`.

Prompt must require source or audit references.

Prompt must require unsupported claims to remain unsupported.

Prompt must prohibit trade approval and execution language.

Prompt injection flags must be preserved.

Malformed LLM debate output must be rejected or degraded.

LLM-generated debate is argument metadata, not evidence.

LLM-generated debate cannot create new facts, cite nonexistent sources, or override normalized restrictions.

## 23. Prompt Contract Requirements For Debate

Block 07 does not create production prompts.

Future debate prompts must declare:

```text
prompt_template_id
prompt_version
input_schema_reference
allowed_output_schema
prohibited_outputs
source_reference_requirements
uncertainty_requirements
missing_evidence_policy
forbidden_usage_policy
confidence_boundary_statement
fallback_rule
audit_reference
```

Prompt contracts must require:

- input schema = `NormalizedSignalCandidate`;
- output schema = `DebateSummary`;
- raw input rejection;
- source-bound argument generation;
- preservation of missing evidence, blocking gaps, unsupported claims, conflicting sources, and forbidden downstream usage;
- no trade approval;
- no execution language;
- no confidence invention.

## 24. Debate Validation Rules

Debate validation must confirm:

- input is `NormalizedSignalCandidate`;
- candidate includes `non_approval_statement`;
- `forbidden_downstream_usage` is present;
- `missing_evidence` is not dropped;
- `blocking_gaps` is not dropped;
- `unsupported_claims` is not dropped;
- `conflicting_sources` is not dropped;
- Bull/Bear arguments reference existing fields or audit references;
- output includes `confidence_boundary_statement`;
- output includes `non_approval_statement`;
- Motor B `framework_only` restrictions are preserved when present;
- synthetic status is preserved when present;
- prompt injection flags are preserved when present.

Debate output must be rejected when it:

- contains trade approval language;
- contains execution language;
- invents evidence;
- invents backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invents trading `confidence_score`;
- omits required Motor B `framework_only` restrictions;
- omits material forbidden downstream usage;
- consumes raw upstream input.

Debate output may be degraded when non-critical metadata is incomplete but non-authority restrictions remain intact and explicit.

## 25. Human Review Triggers

Human review is required for:

- `disagreement_level = high`;
- `disagreement_level = unresolved`;
- high or critical event severity;
- conflicting credible sources;
- unsupported claims affecting the conclusion;
- missing primary source for material event claims;
- Motor B `framework_only` with favorable Bull argument;
- material Bull/Bear asymmetry;
- LLM output schema violation;
- prohibited action language;
- prompt injection suspicion;
- synthetic input mixed with non-synthetic input;
- debate output that could materially affect downstream eligibility interpretation.

Human review metadata remains non-authoritative unless a later governed process grants it a specific role.

## 26. Audit And Replay Metadata Requirements

Every `DebateSummary` must retain:

- `debate_summary_id`;
- source `normalized_signal_candidate_id`;
- input schema version;
- debate schema version;
- debate generation mode;
- role definitions used;
- prompt template ID and prompt version if LLM-assisted;
- LLM model metadata if LLM-assisted;
- validation status;
- fallback status when applicable;
- human review requirement;
- source audit references;
- created_at.

Replay must show:

- which normalized fields were used by Bull;
- which normalized fields were used by Bear;
- which fields triggered disagreement reason codes;
- which restrictions were preserved;
- why the debate output was accepted, degraded, or rejected.

## 27. Relationship With 07-Block-08 Deterministic Signal Fusion Engine

07-Block-08 Deterministic Signal Fusion Engine consumes `DebateSummary` as metadata.

Block 08 performs deterministic fusion.

Block 07 does not fuse.

Bull/Bear balance is not fusion.

Debate disagreement is not final signal confidence.

`DebateSummary` cannot override Motor B, Block 09, or `08 Risk Engine`.

Block 08 must treat debate output as bounded argument metadata, not empirical validation or approval.

## 28. Relationship With 07-Block-09 Confidence Status And Aggregation Policy

07-Block-09 Confidence Status and Aggregation Policy defines confidence aggregation policy.

Debate cannot compute final confidence.

Debate can expose uncertainty and disagreement only.

Debate must preserve confidence boundaries.

Disagreement level, Bull/Bear balance, argument count, or argument tone must not be mapped mechanically into confidence.

## 29. Relationship With 08 Risk Engine

`08 Risk Engine` retains final authority over downstream eligibility, veto, promotion, risk limits, and operational decisions.

DebateSummary is not eligible for Paper Trading under the current Motor B `framework_only` state.

08 may veto any later fused signal candidate regardless of debate outcome.

Block 07 must preserve enough detail for 08 to identify missing evidence, blocked eligibility, forbidden usage, unresolved conflicts, synthetic inputs, source limitations, and human review requirements.

## 30. Explicit Prohibited Actions

Block 07 must not:

- implement trading logic;
- implement Paper Trading;
- implement Live Trading;
- create execution logic;
- create capital allocation;
- create Signal Fusion;
- create Deterministic Signal Fusion Engine;
- create Confidence Aggregation;
- create Risk Handoff;
- create Block 08;
- modify the Motor B Output Contract of 06;
- modify Blocks 00-06;
- redefine prior contracts;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- convert Bull/Bear arguments into empirical evidence;
- convert debate balance into confidence;
- convert debate output into trade approval;
- convert debate output into signal promotion;
- convert LLM-generated debate into a new factual source;
- create a ML ensemble.

## 31. Block 07 Closure Criteria

Block 07 is closed when this document defines:

- Bull/Bear Debate Layer purpose;
- scope;
- non-authority rules;
- relationship with Blocks 00-06;
- Bull role;
- Bear role;
- explicit statement that Bull/Bear debate consumes only NormalizedSignalCandidate inputs;
- explicit statement that Bull/Bear debate must not consume raw Motor A/B/C/LLM inputs;
- explicit statement that Bull/Bear arguments are not empirical evidence;
- explicit statement that Bull/Bear arguments are not confidence;
- explicit statement that Bull/Bear debate is not trade approval;
- debate input contract;
- raw input rejection rules;
- debate output contract;
- `DebateSummary` schema;
- Bull argument requirements;
- Bear argument requirements;
- uncertainty and disagreement labels;
- missing evidence handling;
- blocking gaps handling;
- unsupported claims handling;
- conflicting sources handling;
- forbidden downstream usage propagation;
- synthetic and dry-run handling;
- LLM safety boundaries for debate;
- prompt contract requirements for debate;
- debate validation rules;
- human review triggers;
- audit and replay metadata requirements;
- relationship with 07-Block-08 Deterministic Signal Fusion Engine;
- relationship with 07-Block-09 Confidence Status and Aggregation Policy;
- relationship with `08 Risk Engine`.

Closing Block 07 does not implement debate generation in code and does not create Signal Fusion, Confidence Aggregation, Risk Handoff, Paper Trading, Live Trading, execution logic, or capital allocation.
