# 07 Signal Fusion + LLM Motors - Deterministic Signal Fusion Engine

## 1. Purpose

Block 08 defines the Deterministic Signal Fusion Engine for `07 Signal Fusion + LLM Motors`.

The purpose is to combine governed, normalized candidate inputs and bounded debate metadata into a traceable `FusedSignalCandidate`.

Deterministic Signal Fusion is not trade approval.

FusedSignalCandidate is not Paper Trading authorization.

Fusion does not create empirical evidence.

Fusion does not create final signal confidence.

Motor B framework_only remains binding after fusion.

Block 08 produces a fused candidate for later review. It does not produce a trading decision.

## 2. Scope

This block covers:

- input contracts for deterministic fusion;
- raw input rejection;
- `FusedSignalCandidate` definition;
- `FusedSignalCandidate` schema;
- `fused_direction` enum;
- `fused_actionability_status` enum;
- deterministic fusion rule hierarchy;
- base weighting policy;
- event precedence policy;
- conflict resolution policy;
- motor contribution explanation;
- unavailable motor handling;
- missing evidence handling;
- blocking gaps handling;
- forbidden downstream usage propagation;
- Bull/Bear metadata handling;
- confidence boundary rules;
- framework-only protection rules;
- synthetic and dry-run handling;
- audit and replay metadata requirements;
- relationship with 07-Block-09 Confidence Status and Aggregation Policy;
- relationship with 07-Block-10 Downstream Eligibility and Risk Handoff;
- relationship with `08 Risk Engine`.

This block does not implement Python code, trading logic, Paper Trading, Live Trading, execution, capital allocation, Confidence Aggregation, Risk Handoff, or Block 09.

## 3. Non-Authority Reminder

Block 08 is non-authoritative with respect to trading operations.

Block 08 must not:

- approve trades;
- approve strategies;
- authorize Paper Trading;
- authorize Live Trading;
- create execution readiness;
- allocate capital;
- relax risk limits;
- override `08 Risk Engine`;
- modify Motor B evidence state;
- compensate for Motor B `framework_only`;
- invent empirical evidence;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- calculate final signal confidence;
- convert `FusedSignalCandidate` into trade approval;
- convert `fused_direction` into execution instruction;
- convert event precedence into trading authorization;
- convert motor weights into a ML ensemble;
- convert Bull/Bear debate into confidence;
- convert LLM output into empirical evidence;
- convert synthetic data into real evidence.

Current Motor B state remains:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

## 4. Relationship With Blocks 00-07

Block 00 defines 07 stage boundaries and non-authority rules.

Block 01 defines input family acceptance states and forbidden downstream usage preservation.

Block 02 defines the Motor B Adapter and Motor B `framework_only` protection rules.

Block 03 defines Motor A regime context, conceptual base motor weights, and event modulation hooks.

Block 04 defines Motor C event classification and `event_precedence_hint`.

Block 05 defines LLM safety, prompting, evidence boundaries, replay, and prompt injection handling.

Block 06 defines `NormalizedSignalCandidate`.

Block 07 defines `DebateSummary`.

Block 08 consumes Block 06 and Block 07 outputs only. It does not redefine prior contracts.

## 5. Definition Of FusedSignalCandidate

`FusedSignalCandidate` is a deterministic, auditable, pre-risk-review candidate produced from normalized candidate inputs and optional debate metadata.

It may summarize:

- Motor B technical or systematic evidence state;
- Motor A macro, regime, liquidity, volatility, or contextual state;
- Motor C event classification state;
- Bull/Bear debate metadata;
- missing evidence;
- blocking gaps;
- forbidden downstream usage;
- event precedence outcome;
- unresolved conflicts;
- non-approval state.

`FusedSignalCandidate` is not trade approval.

`FusedSignalCandidate` is not Paper Trading authorization.

`FusedSignalCandidate` is not Live Trading authorization.

`FusedSignalCandidate` is not an execution instruction.

`FusedSignalCandidate` is not capital allocation.

`FusedSignalCandidate` is not final signal confidence.

## 6. Input Contracts

Block 08 may consume only:

1. `NormalizedSignalCandidate` from 07-Block-06 Signal Candidate Normalization.
2. `DebateSummary` from 07-Block-07 Bull/Bear Debate Layer.
3. Audit references and schema versions linked to accepted normalized inputs.
4. Optional human review metadata only when already normalized or audit-referenced.

Each input must be:

- schema-versioned;
- audit-referenced;
- linked to source identifiers;
- limitation-aware;
- non-authoritative;
- compatible with prior blocks.

If input is not normalized or not audit-referenced, fusion must be rejected or unavailable.

## 7. Rejected Inputs

Block 08 must reject:

- raw Motor A input;
- raw Motor B input;
- raw Motor C input;
- raw LLM output;
- raw event, news, filing, social, or source text;
- raw strategy candidate;
- raw backtest claim;
- unversioned payload;
- unnormalized candidate;
- `DebateSummary` not linked to a `NormalizedSignalCandidate`;
- payloads that claim trade approval, execution authority, confidence invention, or Risk Engine override.

Rejected inputs must not be used to derive a `FusedSignalCandidate` except as rejected/unavailable audit records.

## 8. Output Contract

The output of Block 08 is:

```text
FusedSignalCandidate
```

`FusedSignalCandidate` must preserve source references, limitations, missing evidence, blocking gaps, confidence boundaries, forbidden downstream usage, and non-approval statements.

The output must be deterministic for the same versioned inputs, rule version, schema version, and policy version.

## 9. FusedSignalCandidate Schema

The conceptual schema is:

```text
FusedSignalCandidate
  fused_signal_candidate_id
  fusion_schema_version
  fusion_rule_version
  input_normalized_signal_candidate_ids
  input_debate_summary_ids
  source_motor_contributions
  source_motor_availability
  source_motor_limitations
  asset
  asset_scope
  timeframe
  horizon
  fused_direction
  fused_direction_status
  fused_actionability_status
  evidence_completeness_level
  evidence_level_normalized
  motor_b_evidence_state
  motor_a_context_state
  motor_c_event_state
  debate_state
  base_weighting_policy_applied
  motor_weight_labels
  event_precedence_policy_applied
  event_precedence_outcome
  conflict_resolution_policy_applied
  conflict_status
  unresolved_conflicts
  missing_evidence
  blocking_gaps
  unsupported_claims
  conflicting_sources
  forbidden_downstream_usage
  paper_trading_eligibility
  downstream_operational_eligibility
  confidence_status
  confidence_score
  classification_confidence_status
  classification_confidence_score
  uncertainty_level
  requires_human_review
  non_approval_statement
  fusion_explanation
  audit_references
  created_at
```

Fields unavailable from inputs must remain null, unavailable, empty, or explicitly degraded according to source contract semantics.

## 10. fused_direction Enum

Allowed `fused_direction` values are:

```text
long_bias
short_bias
neutral
risk_reduce
risk_suspend
no_direction
unknown_direction
rejected_direction
```

Rules:

- `fused_direction` is not a trade instruction.
- `long_bias` is not buy.
- `short_bias` is not sell.
- `risk_reduce` is not an execution order.
- `risk_suspend` is not an execution order.
- `no_direction` is valid when evidence is insufficient.
- `unknown_direction` is valid when inputs are ambiguous, degraded, or incomplete.
- `rejected_direction` is valid when contracts are violated.

## 11. fused_actionability_status Enum

Allowed `fused_actionability_status` values are:

```text
non_actionable_framework_only
non_actionable_missing_evidence
non_actionable_conflict
non_actionable_synthetic
non_actionable_requires_human_review
non_actionable_risk_engine_required
research_only_candidate
dry_run_only_candidate
rejected_candidate
```

Under the current Motor B `framework_only` state, `fused_actionability_status` cannot be operational.

The enum must not include:

```text
trade_ready
paper_trade_ready
live_trade_ready
execution_ready
capital_ready
```

Any future operational status would require governed upstream evidence, Block 09 confidence policy, Block 10 downstream eligibility policy, and `08 Risk Engine` review.

## 12. deterministic fusion rule hierarchy

Block 08 applies the deterministic fusion rule hierarchy in this order:

1. Contract validity check.
2. Synthetic/dry-run status check.
3. Motor B evidence state check.
4. Missing evidence and blocking gaps check.
5. Forbidden downstream usage propagation.
6. Motor availability check.
7. Event severity and event precedence check.
8. Source reliability and conflicting sources check.
9. Motor A regime context adjustment.
10. Bull/Bear debate metadata review.
11. Direction derivation or preservation.
12. Fused candidate explanation.
13. Final non-approval statement.

Earlier blocking rules dominate later favorable context.

No later rule may convert a blocked, missing, synthetic, rejected, or framework-only condition into operational eligibility.

## 13. Contract Validity Check

Fusion must verify:

- input is `NormalizedSignalCandidate` or linked `DebateSummary`;
- schema versions are present;
- audit references are present;
- source candidate IDs are present;
- `non_approval_statement` is present;
- `forbidden_downstream_usage` is present;
- required confidence and eligibility fields are present or explicitly unavailable;
- debate metadata is linked to a known normalized candidate when supplied.

Contract validity failures must produce:

```text
fused_direction = rejected_direction
fused_actionability_status = rejected_candidate
```

or unavailable output when the input absence is explicit and non-violating.

## 14. base weighting policy

Block 08 uses deterministic conceptual weight labels only.

Allowed `motor_weight_labels` values are:

```text
dominant_blocking_constraint
elevated_contextual_weight
normal_contextual_weight
reduced_contextual_weight
suspended_contextual_weight
unavailable_weight
synthetic_weight
```

Rules:

- weights are deterministic labels, not learned weights;
- weights are not ML ensemble;
- weights are not confidence;
- weights do not create evidence;
- weights do not create approval;
- Motor B `framework_only` can dominate operational eligibility regardless of other weights;
- Motor C critical event may constrain or suspend favorable context, but does not approve trading;
- Bull/Bear balance does not mechanically change weights.

Base weighting can explain relative contribution treatment, but it cannot alter upstream evidence state or downstream eligibility.

## 15. event precedence policy

Block 08 may consume `event_precedence_hint` from Motor C after Block 06 normalization.

Block 08 defines deterministic event precedence rules only for fused candidate handling, not trading approval.

Allowed `event_precedence_outcome` values are:

```text
no_event_precedence
monitor_only
constrain_direction
degrade_candidate
require_human_review
risk_suspend_candidate
reject_candidate_due_to_event_risk
unavailable_event_context
```

Event precedence can constrain, degrade, require review, or suspend candidate handling.

Event precedence cannot approve a trade.

Event precedence cannot create confidence.

Event precedence cannot override Motor B `framework_only`.

Event precedence cannot bypass `08 Risk Engine`.

Bullish events cannot promote candidates.

Favorable events cannot compensate missing evidence.

Critical events dominate favorable regime context.

Event precedence outcome must be audit-referenced.

### Event Precedence Examples

| Event | Possible event_precedence_outcome | Boundary |
| --- | --- | --- |
| FOMC surprise | `degrade_candidate` or `require_human_review` | Does not approve trading. |
| exchange hack | `risk_suspend_candidate` or `reject_candidate_due_to_event_risk` | Does not execute suspension; it marks fused candidate handling. |
| regulatory ban | `constrain_direction`, `require_human_review`, or `reject_candidate_due_to_event_risk` | Does not make regional risk decisions final. |
| stablecoin depeg | `risk_suspend_candidate` | Does not bypass `08 Risk Engine`. |
| protocol exploit | `risk_suspend_candidate` or `require_human_review` | Does not authorize trade avoidance execution. |
| exchange outage | `constrain_direction` or `risk_suspend_candidate` | Does not route orders. |
| systemic crypto event | `risk_suspend_candidate` or `reject_candidate_due_to_event_risk` | Does not create a trading decision. |

## 16. conflict resolution policy

Conflicts must be preserved, not silently resolved.

Block 08 must cover these conflict classes:

- Motor A bullish context plus Motor B `framework_only`;
- Motor C bullish event plus Motor B `framework_only`;
- Motor C critical event plus Motor A `trend_bullish`;
- Bull argues favorable plus Bear highlights missing evidence;
- debate disagreement high or unresolved;
- missing backtest evidence;
- missing OOS evidence;
- missing robustness evidence;
- conflicting credible sources;
- weak source reliability with high severity event;
- synthetic input mixed with real input;
- confidence unavailable but direction favorable.

Rules:

- conflicts must be preserved in `unresolved_conflicts` unless deterministically downgraded;
- missing evidence dominates favorable argumentation;
- `framework_only` dominates downstream operational eligibility;
- high or critical event risk can degrade or suspend candidate handling;
- unresolved conflicts require human review or non-actionable status;
- conflict resolution cannot create trade approval.

Allowed `conflict_status` values are:

```text
no_conflict_detected
conflict_preserved
conflict_downgraded_by_blocking_rule
conflict_requires_human_review
conflict_rejected
unknown_conflict_status
```

## 17. Motor Contribution Explanation

`fusion_explanation` must include structured explanations for:

- Motor B contribution;
- Motor A contribution;
- Motor C contribution;
- Bull/Bear debate contribution;
- missing evidence contribution;
- blocking gaps contribution;
- event precedence contribution;
- final non-approval statement.

`source_motor_contributions` must identify each contributing motor and whether the contribution is technical evidence state, contextual state, event state, debate metadata, unavailable, synthetic, or rejected.

Explanation is traceability, not confidence.

Explanation is not investment advice.

Explanation is not a trade recommendation.

Explanation must include limitations and unresolved conflicts.

## 18. Unavailable Motor Handling

Unavailable motor handling must be explicit:

- If Motor B is unavailable, the candidate must be unavailable or rejected for technical evidence path.
- If Motor A is unavailable, context must be unavailable, not inferred.
- If Motor C is unavailable, event context is unavailable, not assumed safe.
- If `DebateSummary` is unavailable, fusion may proceed only if debate is optional for that candidate type; otherwise it must degrade or require review.
- Missing motor cannot be imputed.
- Missing motor cannot be replaced by LLM speculation.

`source_motor_availability` must indicate available, unavailable, degraded, rejected, synthetic, or not_applicable per motor.

## 19. Missing Evidence Handling

Block 08 must preserve:

- `missing_evidence`;
- missing backtest evidence;
- missing OOS evidence;
- missing walk-forward evidence;
- missing robustness evidence;
- missing source references;
- missing context;
- missing debate metadata when required.

Missing evidence must drive `non_actionable_missing_evidence`, `non_actionable_framework_only`, `non_actionable_requires_human_review`, or `research_only_candidate` when material.

Missing evidence cannot be offset by favorable regime context, bullish event classification, Bull arguments, or motor weight labels.

## 20. Blocking Gaps Handling

Block 08 must preserve `blocking_gaps`.

Blocking gaps must be included in:

- `blocking_gaps`;
- `source_motor_limitations`;
- `conflict_status` when relevant;
- `requires_human_review` when material;
- `fusion_explanation`;
- audit references.

Block 08 cannot close a blocking gap.

Block 08 cannot hide a blocking gap behind a favorable fused direction.

## 21. Forbidden Downstream Usage Propagation

`forbidden_downstream_usage` must be propagated to `FusedSignalCandidate`.

Under the current Motor B `framework_only` state, it must include:

- trade approval;
- Paper Trading authorization;
- Live Trading authorization;
- execution;
- capital allocation;
- risk limit relaxation;
- strategy promotion;
- confidence invention;
- empirical evidence replacement.

Block 08 must not weaken, remove, rename into permissive language, or reinterpret forbidden downstream usage.

## 22. Bull/Bear Metadata Handling

Block 08 may consume `DebateSummary` as metadata.

Bull/Bear metadata can:

- expose favorable and adverse arguments;
- identify disagreement level;
- identify disagreement reason codes;
- highlight missing evidence;
- highlight blocking gaps;
- highlight unsupported claims;
- highlight conflicting sources;
- require human review.

Bull/Bear metadata cannot:

- create evidence;
- create final confidence;
- mechanically change motor weights;
- approve trades;
- approve strategies;
- resolve fusion outcome by argument count;
- override Motor B;
- override Block 09;
- override `08 Risk Engine`.

High or unresolved disagreement must generally produce `non_actionable_conflict`, `non_actionable_requires_human_review`, or a degraded fused candidate.

## 23. Confidence Boundary Rules

Block 08 does not compute final signal confidence.

Block 08 does not aggregate confidence.

Block 08 preserves:

- `confidence_status`;
- `confidence_score`;
- `classification_confidence_status`;
- `classification_confidence_score`;
- `uncertainty_level`;
- confidence boundary statements from debate when available.

Final signal confidence belongs to Block 09.

Fusion explanation cannot be converted into confidence.

More aligned motors do not automatically increase confidence.

Bull/Bear balance does not create confidence.

LLM classification confidence is not trading confidence.

Motor B `confidence_score` remains null under `framework_only`.

If confidence fields conflict or are unavailable, Block 08 must preserve the conflict or unavailability and mark the fused candidate as non-actionable, degraded, or requiring human review.

## 24. Framework-Only Protection Rules

If any fused candidate is linked to Motor B `framework_only`, then:

```text
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

`fused_actionability_status` must be one of:

```text
non_actionable_framework_only
research_only_candidate
dry_run_only_candidate
non_actionable_missing_evidence
non_actionable_requires_human_review
```

`forbidden_downstream_usage` must include trade approval, Paper Trading, Live Trading, execution, capital allocation, risk limit relaxation, strategy promotion, confidence invention, and empirical evidence replacement.

`non_approval_statement` must remain explicit.

Motor A favorable context, Motor C favorable event classification, Bull arguments, or conceptual weights cannot override this rule.

## 25. Synthetic And Dry-Run Handling

Synthetic candidates can be fused only for dry-run, interface validation, schema validation, documentation, or audit rehearsal.

Synthetic fusion output cannot be used as evidence.

Synthetic fusion output cannot be used for Paper Trading or Live Trading.

Synthetic fusion output must carry:

```text
fused_actionability_status = dry_run_only_candidate
```

or:

```text
fused_actionability_status = non_actionable_synthetic
```

It must also carry synthetic status, source references, limitations, and `non_approval_statement`.

Synthetic and real inputs mixed together must trigger degraded or rejected status unless explicitly marked as dry-run.

## 26. Direction Derivation And Preservation

Block 08 may derive or preserve `fused_direction` only after blocking, missing evidence, synthetic, event, source reliability, conflict, and confidence boundary checks are applied.

Direction derivation must be deterministic and explainable.

Examples:

- if all valid directional inputs are unavailable, use `no_direction` or `unknown_direction`;
- if contracts are violated, use `rejected_direction`;
- if event precedence outcome is `risk_suspend_candidate`, use `risk_suspend` or preserve a prior direction with suspended status;
- if evidence is `framework_only`, any favorable direction remains non-actionable.

`fused_direction_status` must explain whether direction was preserved, constrained, suspended, degraded, unavailable, unknown, or rejected.

## 27. Audit And Replay Metadata Requirements

Every `FusedSignalCandidate` must retain:

- `fused_signal_candidate_id`;
- fusion schema version;
- fusion rule version;
- input normalized candidate IDs;
- input debate summary IDs;
- source schema versions;
- source motor identifiers;
- source audit references;
- fusion rule hierarchy result;
- base weighting policy applied;
- event precedence policy applied;
- conflict resolution policy applied;
- validation status;
- fallback status when applicable;
- human review requirement;
- created_at.

Replay must show:

- which inputs were accepted, degraded, unavailable, synthetic, or rejected;
- which rule in the deterministic hierarchy dominated;
- how each motor contributed;
- how `fused_direction` was selected or rejected;
- how event precedence was applied;
- which conflicts remain unresolved;
- which missing evidence and blocking gaps were preserved;
- why downstream usage remains forbidden.

## 28. Relationship With 07-Block-09 Confidence Status And Aggregation Policy

07-Block-09 Confidence Status and Aggregation Policy defines confidence status and aggregation policy.

Block 08 does not compute final confidence.

Block 08 passes preserved confidence fields, missing evidence, uncertainty, classification confidence, debate metadata, and fusion metadata to Block 09.

Block 09 may evaluate confidence policy later, but Block 08 must not precompute or imply final signal confidence.

## 29. Relationship With 07-Block-10 Downstream Eligibility And Risk Handoff

07-Block-10 Downstream Eligibility and Risk Handoff defines downstream eligibility and Risk Handoff.

Block 08 does not authorize downstream usage.

Block 08 passes fused candidate, blocking gaps, forbidden usage, actionability status, human review requirement, and non-approval statement to Block 10.

Block 10 may prepare handoff metadata, but `08 Risk Engine` retains final authority.

## 30. Relationship With 08 Risk Engine

`08 Risk Engine` retains final authority over downstream eligibility, veto, promotion, risk limits, and operational decisions.

`FusedSignalCandidate` is not eligible for Paper Trading under current Motor B `framework_only` state.

08 may veto any future fused signal candidate regardless of fusion outcome.

Block 08 must preserve enough detail for 08 to identify missing evidence, blocked eligibility, forbidden usage, unresolved conflicts, event risk, synthetic inputs, source limitations, and human review requirements.

## 31. Explicit Prohibited Actions

Block 08 must not:

- implement trading logic;
- implement Paper Trading;
- implement Live Trading;
- create execution logic;
- create capital allocation;
- create Confidence Aggregation;
- create Risk Handoff;
- create Block 09;
- modify the Motor B Output Contract of 06;
- modify Blocks 00-07;
- redefine prior contracts;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- calculate final signal confidence;
- convert `FusedSignalCandidate` into trade approval;
- convert `fused_direction` into execution instruction;
- convert event precedence into trading authorization;
- convert motor weights into a ML ensemble;
- convert Bull/Bear debate into confidence;
- convert LLM output into empirical evidence;
- convert synthetic data into real evidence.

## 32. Block 08 Closure Criteria

Block 08 is closed when this document defines:

- Deterministic Signal Fusion Engine purpose;
- scope;
- non-authority rules;
- relationship with Blocks 00-07;
- `FusedSignalCandidate`;
- explicit statement that Deterministic Signal Fusion is not trade approval;
- explicit statement that FusedSignalCandidate is not Paper Trading authorization;
- explicit statement that Fusion does not create empirical evidence;
- explicit statement that Fusion does not create final signal confidence;
- explicit statement that Motor B framework_only remains binding after fusion;
- input contracts;
- raw input rejection;
- output contract;
- `FusedSignalCandidate` schema;
- `fused_direction` enum;
- `fused_actionability_status` enum;
- deterministic fusion rule hierarchy;
- base weighting policy;
- event precedence policy;
- `event_precedence_outcome` enum;
- conflict resolution policy;
- motor contribution explanation;
- unavailable motor handling;
- missing evidence handling;
- blocking gaps handling;
- forbidden downstream usage propagation;
- Bull/Bear metadata handling;
- confidence boundary rules;
- framework-only protection rules;
- synthetic and dry-run handling;
- audit and replay metadata requirements;
- relationship with 07-Block-09 Confidence Status and Aggregation Policy;
- relationship with 07-Block-10 Downstream Eligibility and Risk Handoff;
- relationship with `08 Risk Engine`.

Closing Block 08 does not implement deterministic fusion in code and does not create Confidence Aggregation, Risk Handoff, Paper Trading, Live Trading, execution logic, or capital allocation.
