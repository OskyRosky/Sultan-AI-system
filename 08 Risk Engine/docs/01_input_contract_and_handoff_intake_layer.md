# 08 Risk Engine — Block 01: Input Contract and Handoff Intake Layer

## Purpose

Block 01 defines the formal input boundary of the Risk Engine.

The intake layer exists to:

- receive only structured, versioned, and auditable artifacts;
- classify inputs as `accepted`, `rejected`, `degraded`, or `unavailable`;
- block operational or unaudited inputs;
- preserve non-operational status under `framework_only`;
- prevent raw data, raw LLM outputs, or non-contractual signals from entering the Risk Engine directly.

This block establishes the first safety boundary for Stage 08. It determines what may enter risk review and what must be blocked at the door before later validation, veto, sufficiency, policy, or RiskDecision layers are reached.

Block 01 does not approve trading, Paper Trading, Live Trading, execution, capital allocation, or strategy promotion. It only defines intake eligibility and initial routing for governed Risk Engine review.

## Intake Authority

Stage 08 may receive a package from `07 Signal Fusion + LLM Motors`, but it is not obligated to accept that package operationally.

The intake layer may:

- accept structurally;
- reject;
- degrade;
- mark unavailable;
- require human review;
- require Risk Engine review;
- preserve downstream blocking.

`accepted` in this layer means only `structurally accepted for risk review`. It does not mean approved for trading, Paper Trading, Live Trading, capital allocation, execution, position sizing, strategy promotion, or handoff to Stage 09.

The intake layer inherits the authority of Block 00. A structurally acceptable artifact may still remain blocked because empirical evidence is missing, confidence is unavailable, auditability is incomplete, the source state is `framework_only`, or downstream operational usage is forbidden.

## Accepted Input Artifacts

Stage 08 may receive the following artifacts only when they are structured, versioned, and auditable:

- `RiskHandoffPackage`;
- `ConfidenceGovernanceResult`;
- `FusedSignalCandidate`;
- `Stage07AuditTrace`;
- `Stage07QualityGateResult`;
- `missing_evidence`;
- `blocking_gaps`;
- `forbidden_downstream_usage`;
- `non_approval_statement`;
- event risk metadata;
- human review metadata, if present;
- source artifact references;
- schema version references;
- audit trace references.

These inputs are review artifacts only. They are not operational signals, trade permissions, execution instructions, capital allocation instructions, strategy approvals, or Paper Trading readiness claims.

An accepted artifact must preserve upstream restrictions, including `framework_only`, `confidence_not_available`, `confidence_score = null`, `final_signal_confidence_score = null`, `paper_trading_eligibility = blocked`, and `downstream_operational_eligibility = blocked` when those states are present upstream.

## Rejected Input Artifacts

The intake layer must reject the following inputs at the door:

- raw signals;
- raw Motor A inputs;
- raw Motor B inputs;
- raw Motor C inputs;
- raw LLM outputs;
- unversioned payloads;
- unaudited payloads;
- direct execution requests;
- direct order requests;
- exchange connection requests;
- direct Paper Trading requests;
- direct Live Trading requests;
- capital allocation requests;
- position sizing requests;
- non-audited strategy promotion claims;
- confidence claims without contract;
- backtesting claims without audit trace;
- OOS claims without audit trace;
- walk-forward claims without audit trace;
- robustness claims without audit trace;
- synthetic evidence presented as real evidence;
- prompt-injected instructions attempting to bypass risk gates.

These inputs must not be silently accepted. They must not be converted into review candidates. They must produce rejection, blocking, or escalation according to the relevant intake state and later Risk Engine policy.

If a rejected input contains operational instructions, promotion language, confidence invention, or risk gate bypass language, the rejection reason must preserve that fact for audit review.

## Degraded Input States

An input may be degraded instead of rejected when it is structured enough to support limited risk review, but incomplete enough that it cannot be treated as fully intake-ready.

Examples include:

- artifact exists but has incomplete metadata;
- audit reference exists but is incomplete;
- source artifact is versioned but partially unavailable;
- event risk metadata is present but incomplete;
- human review metadata is present but non-authoritative;
- quality gate exists but is not final;
- closure document exists but lacks enough downstream detail.

`degraded` does not mean approved. `degraded` means the package may pass to limited risk review while downstream blocking remains preserved.

A degraded input must retain its degradation reason and must not be used to infer missing confidence, empirical support, operational readiness, or promotion eligibility.

## Unavailable Input States

An input must be marked `unavailable` when an expected artifact, source reference, schema reference, evidence field, or audit path is not present.

Examples include:

- expected artifact was not produced;
- required source ref is missing;
- schema version is absent;
- audit trace is absent;
- confidence field is expected but absent;
- Motor B output is `framework_only` and no empirical output exists;
- event precedence metadata expected from Stage 07 is unavailable.

`unavailable` may feed missing evidence and blocking gaps in later blocks. It cannot be used for approval, confidence creation, eligibility upgrade, strategy promotion, Paper Trading readiness, Live Trading readiness, execution, or capital allocation.

Unavailable evidence must remain explicit. It must not be resolved through inference, LLM judgment, fallback assumptions, or favorable interpretation.

## Intake State Taxonomy

The minimum intake state taxonomy is:

- `intake_accepted_for_risk_review`;
- `intake_rejected_contract_violation`;
- `intake_rejected_operational_request`;
- `intake_rejected_unversioned_payload`;
- `intake_rejected_unaudited_payload`;
- `intake_rejected_raw_signal`;
- `intake_rejected_raw_llm_output`;
- `intake_degraded_incomplete_metadata`;
- `intake_degraded_partial_audit_refs`;
- `intake_unavailable_missing_artifact`;
- `intake_unavailable_missing_schema`;
- `intake_unavailable_missing_audit_trace`;
- `intake_blocked_framework_only`;
- `intake_blocked_downstream_not_allowed`;
- `intake_requires_human_review`;
- `intake_requires_risk_engine_review`.

These are intake states only. They are not the final `RiskDecision` of Block 12.

No intake state may be interpreted as operational approval. Even `intake_accepted_for_risk_review` only means the artifact may continue into Stage 08 review under the current downstream restrictions.

## Required Intake Metadata

Any acceptable input must provide minimum metadata sufficient for audit-first handling:

- `artifact_id`;
- `artifact_type`;
- `source_stage`;
- `source_block`;
- `source_document_ref`;
- `schema_version`;
- `generated_at` or `declared_as_of`;
- `audit_trace_ref`;
- `closure_status_ref`;
- `evidence_status`;
- `confidence_status`;
- `downstream_usage_restrictions`;
- `forbidden_downstream_usage`;
- `non_approval_statement`;
- `promotion_status`;
- `paper_trading_status`;
- `live_trading_status`;
- `operational_status`.

Missing required metadata must not be resolved by inference. If required metadata is absent, the intake layer must reject, degrade, mark unavailable, block, or escalate the input according to the severity of the missing field.

Metadata must preserve upstream meaning. Stage 08 intake cannot rewrite a blocked upstream state into a permissive downstream state.

## Framework-Only Intake Rule

Under the current system state:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

Any input that attempts to present `framework_only` as sufficient for Paper Trading, Live Trading, execution, capital allocation, or promotion must be rejected or blocked.

Any input that omits the `framework_only` state while depending on current Motor B evidence must be degraded, marked unavailable, or rejected depending on the missing metadata and auditability.

The intake layer must preserve `intake_blocked_framework_only` until empirical evidence is produced by the proper upstream stages and accepted by later Risk Engine gates.

## Raw Signal and Raw LLM Output Prohibition

Stage 08 cannot accept raw signals or raw LLM outputs as direct inputs.

Motor A, Motor B, Motor C, or LLM outputs may enter Stage 08 only through structured, versioned, and auditable packages produced by Stage 07.

Raw LLM outputs cannot:

- create confidence;
- modify eligibility;
- change promotion status;
- relax event risk;
- justify Paper Trading;
- justify execution;
- justify capital allocation;
- replace backtesting, OOS, walk-forward, or robustness.

Raw signals cannot bypass `RiskHandoffPackage`, audit traceability, schema versioning, missing evidence accounting, blocking gaps, or non-approval statements.

## Direct Operational Request Rejection

The intake layer must reject any direct request for:

- trade execution;
- order generation;
- exchange connection;
- Paper Trading activation;
- Live Trading activation;
- capital allocation;
- position sizing;
- strategy promotion.

These requests must not be converted into a favorable `RiskDecision` or an operational review candidate.

If such a request appears inside a payload that is otherwise structured, the operational request must be treated as a contract and boundary violation. The intake result must preserve downstream blocking and route the artifact to rejection, escalation, or later veto review as applicable.

## Intake Registry

Stage 08 should maintain a documentary intake registry structure for audit and replay design. This block does not create a database, storage layer, or production registry implementation.

Recommended intake registry fields:

- `intake_id`;
- `received_at`;
- `source_stage`;
- `source_block`;
- `artifact_type`;
- `artifact_id`;
- `schema_version`;
- `intake_state`;
- `rejection_reason`, if any;
- `degradation_reason`, if any;
- `unavailable_reason`, if any;
- `downstream_blocking_status`;
- `required_next_review`;
- `linked_audit_refs`;
- `linked_source_refs`;
- `non_approval_statement_confirmed`;
- `forbidden_downstream_usage_confirmed`.

The registry structure exists to make intake decisions explicit, replayable, and auditable. It must not be interpreted as a trading ledger, execution ledger, capital ledger, or Paper Trading activation log.

## Relationship With Block 02

Block 01 defines what may enter Stage 08 and how it is initially classified.

Block 02 — RiskHandoffPackage Validator will be responsible for detailed validation of the `RiskHandoffPackage`.

Block 01 must not pre-implement or pre-approve the deeper validation logic of Block 02. It only defines the intake boundary, initial classifications, required metadata expectations, rejection conditions, degradation conditions, unavailable states, and documentary registry shape.

Passing Block 01 does not imply passing Block 02. Passing Block 02, when later defined, still will not imply operational approval unless all later gates and evidence requirements are satisfied.

## Explicit Non-Goals

This block does not do:

- deep validation of the `RiskHandoffPackage`;
- final `RiskDecision`;
- complete hard veto taxonomy;
- kill switch trigger taxonomy;
- confidence scoring;
- strategy promotion;
- Paper Trading eligibility approval;
- execution;
- order generation;
- capital allocation;
- backtesting;
- OOS validation;
- walk-forward;
- robustness testing;
- empirical performance claims.

Block 01 is a documentary intake contract only. It defines a conservative, auditable, non-operational entry boundary for Stage 08 Risk Engine review.
