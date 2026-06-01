# 07 Signal Fusion + LLM Motors - Downstream Eligibility and Risk Handoff

## 1. Purpose

Block 10 defines Downstream Eligibility and Risk Handoff for `07 Signal Fusion + LLM Motors`.

The purpose is to structure a safe, deterministic, audit-ready handoff package for `08 Risk Engine`.

Downstream Eligibility does not mean trade approval.

RiskHandoffPackage is not Paper Trading authorization.

RiskHandoffPackage is not Live Trading authorization.

Block 10 structures information for 08 Risk Engine; it does not decide for 08 Risk Engine.

Block 10 prepares review, veto, risk, missing evidence, blocking gap, and forbidden usage metadata. It does not grant operational authority.

## 2. Scope

This block covers:

- input contracts for downstream eligibility and risk handoff;
- raw input rejection;
- `RiskHandoffPackage` definition;
- `RiskHandoffPackage` schema;
- `eligibility_status` taxonomy;
- `required_risk_engine_action` taxonomy;
- blocking gap propagation;
- missing evidence propagation;
- confidence governance propagation;
- fused actionability handling;
- `DebateSummary` handling;
- event risk handling;
- forbidden downstream usage propagation;
- non-approval statement requirements;
- framework-only protection rules;
- `final_confidence_eligible_for_computation_later` protection;
- synthetic and dry-run handling;
- human review routing;
- veto/readiness separation;
- audit and replay metadata requirements;
- relationship with `08 Risk Engine`.

This block does not implement Python code, trading logic, Paper Trading, Live Trading, execution, capital allocation, Risk Engine behavior, or Block 11.

## 3. Non-Authority Reminder

Block 10 is non-authoritative.

Block 10 must not:

- approve trades;
- approve strategies;
- authorize Paper Trading;
- authorize Live Trading;
- create execution readiness;
- execute orders;
- allocate capital;
- relax risk limits;
- promote strategies;
- perform Risk Engine review;
- issue final Risk Engine decisions;
- bypass `08 Risk Engine`;
- invent empirical evidence;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- create downstream operational eligibility under Motor B `framework_only`;
- convert `eligibility_status` into approval;
- convert `required_risk_engine_action` into a decision;
- convert `RiskHandoffPackage` into Paper Trading readiness;
- convert `final_confidence_eligible_for_computation_later` into operational readiness;
- convert `fused_actionability_status` into trading readiness;
- convert `debate_balance_status` into confidence;
- convert `event_precedence_outcome` into trading authorization;
- convert synthetic data into evidence.

Current Motor B state remains binding:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

## 4. Relationship With Blocks 00-09

Block 00 defines 07 stage boundaries and non-authority rules.

Block 01 defines input acceptance states and forbidden downstream usage preservation.

Block 02 defines the Motor B Adapter and Motor B `framework_only` protection.

Block 03 defines Motor A context as market context, not trading evidence.

Block 04 defines Motor C event classification as classification metadata, not trading authorization.

Block 05 defines LLM safety and evidence boundaries.

Block 06 defines `NormalizedSignalCandidate`.

Block 07 defines `DebateSummary`, including `debate_balance_status` and `prohibited_inference_flags`.

Block 08 defines `FusedSignalCandidate` and `fused_actionability_status`.

Block 09 defines `ConfidenceGovernanceResult` and final confidence blocking.

Block 10 consumes governed outputs from Blocks 06-09. It does not redefine prior contracts.

## 5. Definition Of RiskHandoffPackage

`RiskHandoffPackage` is a structured review package prepared by 07 for `08 Risk Engine`.

It contains:

- fused candidate references;
- confidence governance references;
- normalized candidate references;
- debate summary references;
- missing evidence;
- blocking gaps;
- unsupported claims;
- conflicting sources;
- event risk state;
- eligibility routing status;
- required Risk Engine action;
- forbidden downstream usage;
- non-approval statement;
- audit references.

`RiskHandoffPackage` is a review package, not approval.

It is not Paper Trading authorization.

It is not Live Trading authorization.

It is not execution authorization.

It is not capital allocation.

It is not strategy promotion.

It is not a Risk Engine decision.

## 6. Input Contracts

Block 10 may consume only:

1. `FusedSignalCandidate` from 07-Block-08 Deterministic Signal Fusion Engine.
2. `ConfidenceGovernanceResult` from 07-Block-09 Confidence Status and Aggregation Policy.
3. `NormalizedSignalCandidate` references from 07-Block-06 Signal Candidate Normalization.
4. `DebateSummary` references from 07-Block-07 Bull/Bear Debate Layer.
5. Audit references and schema versions.
6. Human review metadata only when already normalized or explicitly referenced.

Each input must be schema-versioned, audit-referenced, limitation-aware, and linked to governed upstream artifacts.

If input is not normalized, fused, confidence-governed, or audit-referenced, Block 10 must reject or mark the handoff unavailable.

## 7. Rejected Inputs

Block 10 must reject:

- raw Motor A input;
- raw Motor B input;
- raw Motor C input;
- raw LLM output;
- raw event, news, filing, social, or source text;
- raw strategy candidate;
- raw backtest claim;
- unversioned payload;
- unaudited eligibility claim;
- direct paper trading request;
- direct execution request;
- direct capital allocation request;
- payloads that claim downstream approval without `08 Risk Engine` review.

Rejected inputs must not contribute to `RiskHandoffPackage` except as rejected or unavailable audit records.

## 8. Output Contract

The output of Block 10 is:

```text
RiskHandoffPackage
```

`RiskHandoffPackage` must preserve source references, schema versions, missing evidence, blocking gaps, confidence governance status, fused actionability status, event risk state, debate validation metadata, forbidden downstream usage, and non-approval statements.

The output must be deterministic for the same inputs, schema versions, and handoff policy version.

## 9. RiskHandoffPackage Schema

The conceptual schema is:

```text
RiskHandoffPackage
  risk_handoff_package_id
  handoff_schema_version
  related_fused_signal_candidate_id
  related_confidence_governance_result_id
  normalized_signal_candidate_refs
  debate_summary_refs
  source_schema_versions
  asset
  asset_scope
  timeframe
  horizon
  fused_direction
  fused_direction_status
  fused_actionability_status
  eligibility_status
  required_risk_engine_action
  evidence_completeness_level
  missing_evidence
  blocking_gaps
  unsupported_claims
  conflicting_sources
  event_precedence_outcome
  event_risk_status
  confidence_status
  confidence_score
  final_signal_confidence_status
  final_signal_confidence_score
  paper_trading_eligibility
  downstream_operational_eligibility
  forbidden_downstream_usage
  non_approval_statement
  handoff_limitations
  human_review_required
  veto_reasons
  review_reasons
  synthetic_status
  audit_references
  created_at
```

Unavailable fields must remain null, unavailable, blocked, rejected, or explicitly limited according to source contract semantics.

## 10. Eligibility Status Taxonomy

Allowed `eligibility_status` values are:

```text
ineligible_framework_only
ineligible_missing_evidence
ineligible_missing_confidence
ineligible_blocking_gaps
ineligible_forbidden_downstream_usage
ineligible_synthetic_only
ineligible_contract_violation
ineligible_unresolved_conflict
ineligible_event_risk
requires_risk_engine_review
requires_human_review
review_package_only
unavailable_for_handoff
rejected_handoff
```

Rules:

- do not include `trade_ready`;
- do not include `paper_trade_ready`;
- do not include `live_trade_ready`;
- do not include `execution_ready`;
- do not include `capital_ready`;
- do not include `approved`;
- do not include `promoted`;
- `requires_risk_engine_review` is not approval;
- `review_package_only` is not approval;
- `eligibility_status` is a routing, review, and veto-preparation field, not operational authorization.

## 11. Required Risk Engine Action Taxonomy

Allowed `required_risk_engine_action` values are:

```text
risk_engine_veto_required
risk_engine_review_required
risk_engine_blocking_gap_review_required
risk_engine_missing_evidence_review_required
risk_engine_event_risk_review_required
risk_engine_confidence_review_required
risk_engine_synthetic_rejection_required
risk_engine_contract_violation_review_required
risk_engine_no_action_due_to_unavailable_handoff
```

Rules:

- `required_risk_engine_action` routes to `08 Risk Engine`;
- `required_risk_engine_action` is not a decision by Block 10;
- Block 10 cannot perform the Risk Engine action;
- Block 10 cannot convert required review into approval;
- required review must preserve all limitations and forbidden downstream usage.

## 12. Blocking Gap Propagation

Block 10 must preserve `blocking_gaps` from governed inputs.

Blocking gaps must be included in:

- `blocking_gaps`;
- `eligibility_status`;
- `required_risk_engine_action`;
- `veto_reasons`;
- `review_reasons`;
- `handoff_limitations`;
- audit references.

Blocking gaps cannot be closed by Block 10.

Blocking gaps cannot be hidden by favorable fused direction, confidence status, debate balance, event classification, or human review metadata.

## 13. Missing Evidence Propagation

Block 10 must preserve:

- missing backtest evidence;
- missing OOS evidence;
- missing walk-forward evidence;
- missing robustness evidence;
- missing source references;
- missing context;
- missing confidence status;
- unavailable handoff inputs.

Missing evidence must route to `ineligible_missing_evidence`, `ineligible_framework_only`, `requires_risk_engine_review`, `requires_human_review`, or `review_package_only` depending on materiality and source state.

Missing evidence cannot be filled by LLM output, Motor A context, Motor C classification, Bull/Bear debate, fused alignment, confidence governance, or handoff routing.

## 14. Confidence Governance Propagation

Block 10 consumes `ConfidenceGovernanceResult` as confidence governance metadata.

Rules:

- `final_signal_confidence_status` must be preserved;
- `final_signal_confidence_score` must be preserved;
- if `final_signal_confidence_score = null`, Block 10 cannot fill it;
- if `final_signal_confidence_status` is blocked, Block 10 cannot reinterpret it as eligible;
- if `final_signal_confidence_status = final_confidence_blocked_framework_only`, `eligibility_status` must be `ineligible_framework_only`;
- if `final_signal_confidence_status = final_confidence_not_available`, `eligibility_status` must reflect unavailable or blocked confidence;
- `ConfidenceGovernanceResult` is not Paper Trading authorization;
- `ConfidenceGovernanceResult` is not downstream approval.

## 15. final_confidence_eligible_for_computation_later Protection

`final_confidence_eligible_for_computation_later` does not imply downstream operational eligibility.

`final_confidence_eligible_for_computation_later` does not imply Paper Trading readiness.

`final_confidence_eligible_for_computation_later` does not imply Live Trading readiness.

`final_confidence_eligible_for_computation_later` only means confidence may be reevaluated later if evidence improves.

Any future eligibility still requires `08 Risk Engine` review and explicit downstream approval outside 07.

Under current Motor B `framework_only`, this status must not create any operational pathway.

## 16. Fused Actionability Handling

`fused_actionability_status` is not approval.

Block 10 maps `fused_actionability_status` as follows:

| fused_actionability_status | Block 10 routing |
| --- | --- |
| `non_actionable_framework_only` | `ineligible_framework_only` |
| `non_actionable_missing_evidence` | `ineligible_missing_evidence` |
| `non_actionable_conflict` | `ineligible_unresolved_conflict` or `requires_human_review` |
| `non_actionable_synthetic` | `ineligible_synthetic_only` |
| `non_actionable_requires_human_review` | `requires_human_review` |
| `non_actionable_risk_engine_required` | `requires_risk_engine_review` |
| `research_only_candidate` | `review_package_only` or `ineligible_framework_only` depending on Motor B state |
| `dry_run_only_candidate` | `ineligible_synthetic_only` or `review_package_only` |
| `rejected_candidate` | `rejected_handoff` |

Block 10 must not convert `fused_actionability_status` into trading readiness.

## 17. DebateSummary Handling

Block 10 consumes `DebateSummary` as bounded debate metadata.

Relevant fields include:

- `debate_balance_status`;
- `prohibited_inference_flags`;
- `disagreement_level`;
- `disagreement_reason_codes`;
- `validation_status`;
- `fallback_status`.

Rules:

- `debate_balance_status` is metadata only;
- `debate_balance_status` is not confidence;
- `debate_balance_status` is not approval;
- `bull_favorable` does not create eligibility;
- `bear_favorable` does not perform veto;
- unresolved or high disagreement should route to human review or Risk Engine review;
- `prohibited_inference_flags` must be preserved;
- severe prohibited inference flags must route to `rejected_handoff` or `requires_human_review`;
- `trade_approval_language_detected` must trigger `rejected_handoff`;
- `execution_language_detected` must trigger `rejected_handoff`;
- `confidence_invention_detected` must trigger `rejected_handoff` or `risk_engine_review_required`;
- `risk_engine_bypass_language_detected` must trigger `rejected_handoff`;
- `raw_input_usage_detected` must trigger `rejected_handoff`.

Debate metadata cannot override missing evidence, blocking gaps, forbidden downstream usage, confidence governance, or Motor B `framework_only`.

## 18. Event Risk Handling

Block 10 consumes `event_precedence_outcome` as event risk metadata.

Rules:

- `event_precedence_outcome` is not trading authorization;
- `risk_suspend_candidate` routes to `ineligible_event_risk` or `risk_engine_event_risk_review_required`;
- `reject_candidate_due_to_event_risk` routes to `rejected_handoff` or `risk_engine_veto_required`;
- `require_human_review` routes to `requires_human_review`;
- `degrade_candidate` routes to `requires_risk_engine_review` or `review_package_only`;
- `monitor_only` does not create eligibility;
- favorable or no-event status cannot compensate missing evidence;
- event risk cannot bypass `08 Risk Engine`.

`event_risk_status` must summarize whether event state is unavailable, monitor-only, degraded, constrained, suspended, rejected, or requiring review.

## 19. Forbidden Downstream Usage Propagation

`forbidden_downstream_usage` must be propagated to `RiskHandoffPackage`.

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

Block 10 must not weaken, remove, rename into permissive language, or reinterpret forbidden downstream usage.

## 20. Non-Approval Statement Requirements

Every `RiskHandoffPackage` must include `non_approval_statement`.

The statement must explicitly say that the package:

- is not trade approval;
- is not Paper Trading authorization;
- is not Live Trading authorization;
- is not execution authorization;
- is not capital allocation;
- is not Risk Engine approval;
- remains subject to `08 Risk Engine` review.

If `non_approval_statement` is missing, handoff must be rejected or unavailable.

## 21. Framework-Only Protection Rules

If any `RiskHandoffPackage` is linked to Motor B `framework_only`, then:

```text
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

`eligibility_status` must be:

```text
ineligible_framework_only
```

or:

```text
review_package_only
```

only when the blocked state is explicit.

`required_risk_engine_action` must indicate review, veto, or blocking gap handling, not approval.

`forbidden_downstream_usage` must include trade approval, Paper Trading, Live Trading, execution, capital allocation, risk limit relaxation, strategy promotion, confidence invention, and empirical evidence replacement.

`non_approval_statement` must remain explicit.

`handoff_limitations` must state that Motor B is `framework_only` and no empirical validation exists.

## 22. Synthetic And Dry-Run Handling

Synthetic or dry-run inputs must preserve `synthetic_status`.

Synthetic handoff packages are allowed only for:

- schema validation;
- interface validation;
- dry-run testing;
- documentation;
- audit rehearsal.

Synthetic handoff output cannot be used as evidence.

Synthetic handoff output cannot be used for Paper Trading or Live Trading.

Synthetic handoff must route to `ineligible_synthetic_only`, `review_package_only`, or `rejected_handoff` depending on contract validity.

Synthetic and real inputs mixed together must trigger rejected or degraded handoff unless explicitly marked as dry-run.

## 23. Human Review Routing

Human review must be routed when:

- Motor B is `framework_only` with favorable fused direction;
- final confidence is unavailable;
- event risk is high or critical;
- unresolved conflict exists;
- disagreement is high;
- severe `prohibited_inference_flags` are present;
- empirical evidence is missing;
- credible sources conflict;
- unsupported claims affect handoff;
- synthetic input is mixed with real input;
- contract violation occurs;
- any input attempts to infer eligibility from confidence, fusion, debate, or event classification.

Human review metadata is not approval unless a later governed process explicitly grants authority outside Block 10.

## 24. Veto/Readiness Separation

Block 10 may prepare veto reasons.

Block 10 may prepare review reasons.

Block 10 may identify blocking gaps.

Block 10 may identify missing evidence.

Block 10 may identify prohibited downstream usage.

Block 10 may recommend required Risk Engine action.

Block 10 cannot issue the veto itself unless `08 Risk Engine` defines that authority later.

Block 10 cannot issue approval.

Block 10 cannot mark a candidate ready for Paper Trading.

Block 10 cannot mark a candidate ready for Live Trading.

Block 10 cannot mark a candidate ready for execution.

Readiness language must be avoided unless it explicitly means review readiness only.

## 25. Audit And Replay Metadata Requirements

Every `RiskHandoffPackage` must retain:

- risk handoff package ID;
- handoff schema version;
- related fused signal candidate ID;
- related confidence governance result ID;
- normalized signal candidate references;
- debate summary references;
- source schema versions;
- handoff policy version when available;
- eligibility status;
- required Risk Engine action;
- missing evidence;
- blocking gaps;
- unsupported claims;
- conflicting sources;
- event risk status;
- confidence governance fields;
- forbidden downstream usage;
- non-approval statement;
- human review requirement;
- veto reasons;
- review reasons;
- synthetic status;
- audit references;
- created_at.

Replay must show:

- which governed inputs were consumed;
- which raw inputs were rejected or absent;
- why `eligibility_status` was assigned;
- why `required_risk_engine_action` was assigned;
- which missing evidence and blocking gaps were propagated;
- why forbidden downstream usage remains binding;
- why Block 10 did not approve downstream usage.

## 26. Relationship With 08 Risk Engine

`08 Risk Engine` retains final authority over downstream eligibility, veto, promotion, risk limits, and operational decisions.

`RiskHandoffPackage` is a review package, not approval.

08 may veto any candidate regardless of handoff status.

08 may require additional evidence, additional review, additional blocking, or no downstream processing.

08 must receive all missing evidence, blocking gaps, forbidden usage, confidence nulls, synthetic state, event risk, prohibited inference flags, and non-approval status.

Block 10 cannot bypass `08 Risk Engine`.

Block 10 cannot bind `08 Risk Engine` to approve any candidate.

## 27. Explicit Prohibited Actions

Block 10 must not:

- implement trading logic;
- implement Paper Trading;
- implement Live Trading;
- create execution logic;
- create capital allocation;
- create Risk Engine;
- create Block 11;
- modify the Motor B Output Contract of 06;
- modify Blocks 00-09;
- redefine prior contracts;
- invent backtesting, OOS validation, walk-forward validation, robustness, or historical results;
- invent trading `confidence_score`;
- create downstream operational eligibility under `framework_only`;
- convert `eligibility_status` into approval;
- convert `required_risk_engine_action` into decision;
- convert `RiskHandoffPackage` into Paper Trading readiness;
- convert `final_confidence_eligible_for_computation_later` into operational readiness;
- convert `fused_actionability_status` into trading readiness;
- convert `debate_balance_status` into confidence;
- convert `event_precedence_outcome` into trading authorization;
- convert synthetic data into evidence;
- create a ML ensemble.

## 28. Block 10 Closure Criteria

Block 10 is closed when this document defines:

- Downstream Eligibility and Risk Handoff purpose;
- scope;
- non-authority rules;
- relationship with Blocks 00-09;
- `RiskHandoffPackage`;
- explicit statement that Downstream Eligibility does not mean trade approval;
- explicit statement that RiskHandoffPackage is not Paper Trading authorization;
- explicit statement that RiskHandoffPackage is not Live Trading authorization;
- explicit statement that Block 10 structures information for 08 Risk Engine;
- input contracts;
- rejected inputs;
- output contract;
- `RiskHandoffPackage` schema;
- `eligibility_status` taxonomy;
- `required_risk_engine_action` taxonomy;
- blocking gap propagation;
- missing evidence propagation;
- confidence governance propagation;
- `final_confidence_eligible_for_computation_later` protection;
- fused actionability handling;
- `DebateSummary` handling;
- event risk handling;
- forbidden downstream usage propagation;
- non-approval statement requirements;
- framework-only protection rules;
- synthetic and dry-run handling;
- human review routing;
- veto/readiness separation;
- audit and replay metadata requirements;
- relationship with `08 Risk Engine`.

Closing Block 10 does not implement Risk Engine behavior and does not create Block 11, Paper Trading, Live Trading, execution logic, or capital allocation.
