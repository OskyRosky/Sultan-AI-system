# Motor B Raw Diagnostics Adapter Contract — Stage 06 to Stage 07

## A. Purpose

This contract defines how `07 Signal Fusion + LLM Motors` must consume the
real terminal artifact produced by `06 Backtesting Engine`:

```text
RawDiagnosticsHandoffContract
```

The purpose is to align Stage 06 and Stage 07 without ambiguity between the
older documentary `Motor B Output Contract` and the implemented Stage 06
terminal handoff artifact.

Stage 07 may use `RawDiagnosticsHandoffContract` only as a bounded raw
diagnostics handoff. Stage 07 must not reinterpret it as empirical evidence,
strategy validation, signal promotion, confidence, paper trading permission, or
operational readiness.

## B. Scope

This contract belongs to V1.

It is contractual and dry-run compatible. It exists to support:

- schema alignment;
- handoff validation;
- mock and dry-run processing;
- traceability;
- auditability;
- blocked-state preservation.

It does not enable:

- OOS validation;
- walk-forward validation;
- robustness validation;
- strategy promotion;
- confidence generation;
- paper trading;
- live trading;
- Stage 09 readiness.

V2 may later extend this adapter if Motor B produces real governed empirical
evidence. That extension is outside V1.

## C. Source Artifact

The real terminal artifact of Stage 06 is:

```text
RawDiagnosticsHandoffContract
```

Defined in:

```text
06 Backtesting Engine/handoff/raw_diagnostics_handoff_contract.py
```

Documented in:

```text
06 Backtesting Engine/docs/06B_CLOSURE_PACKAGE.md
```

The current fields are:

```text
handoff_contract_id
registry_record_id
diagnostics_id
simulation_id
package_id
strategy_id
strategy_version
snapshot_id
output_scope
diagnostics_scope
registry_scope
simulation_status
trade_count
ending_capital
return_pct
handoff_scope
non_approval_statement
```

Required current scope values are:

```text
output_scope = raw_execution_scaffold
diagnostics_scope = raw_scaffold_diagnostics_only
registry_scope = raw_diagnostics_registry_only
handoff_scope = raw_diagnostics_handoff_only
simulation_status = completed_raw_execution
```

These values mean raw scaffold diagnostics only. They do not imply empirical
strategy validation.

### Governance and Evidence Interpretation

`RawDiagnosticsHandoffContract` does not carry explicit fields named
`evidence_completeness_level`, `empirical_results_available`,
`confidence_status`, `confidence_score`, `paper_trading_ready`, or
`handoff_to_09`.

Stage 07 must therefore derive the following conservative adapter state from
the Stage 06 handoff scope and non-approval statement:

```text
evidence_completeness_level = framework_only
empirical_results_available = false
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
paper_trading_ready = false
paper_trading_eligibility = blocked
handoff_to_09 = blocked
strategy_promotion_status = not_promoted
downstream_operational_eligibility = blocked
```

This conservative derivation is a preservation rule, not a new evidence claim.

## D. Target Stage 07 Concepts

Stage 07 must adapt `RawDiagnosticsHandoffContract` through a conceptual adapter
record:

```text
MotorBRawDiagnosticsInputForStage07
```

This adapter record then feeds existing Stage 07 concepts:

- `NormalizedMotorBInput`
- `NormalizedSignalCandidate`
- `FusedSignalCandidate`
- `ConfidenceGovernanceResult`
- `RiskHandoffPackage`
- `Stage07AuditTrace`

No Stage 07 artifact may consume raw Stage 06 output directly after this
adapter boundary. The adapter is the formal 06->07 contract alignment point.

## E. Field Mapping Table

| Stage 06 field / concept | Stage 07 target field / concept | Mapping rule | Allowed transformation | Forbidden transformation | Notes |
| --- | --- | --- | --- | --- | --- |
| `handoff_contract_id` | `source_artifact_id`, `source_motor_ids`, `audit_trace.source_artifact_id` | Preserve exactly | Copy to Stage 07 source refs | Rename into evidence package id | Deterministic SHA-256 lineage id. |
| `registry_record_id` | `audit_references`, `source_contract_references` | Preserve exactly | Copy as upstream registry ref | Treat as result registry approval | Registry is archival only. |
| `diagnostics_id` | `motor_b_input_id` component, `source_motor_ids`, `audit_trace` | Preserve exactly | Use in deterministic Stage 07 adapter id | Treat as confidence/evidence id | Diagnostics id is descriptive only. |
| `simulation_id` | `source_motor_ids`, `backtest_status` source ref | Preserve exactly | Copy as raw scaffold simulation ref | Treat as real strategy backtest evidence | Simulation is raw execution scaffold. |
| `package_id` | `source_package_ref`, `source_contract_references` | Preserve exactly | Copy as package lineage | Treat as strategy approval | Package lineage is non-promotional. |
| `strategy_id` | `strategy_candidate_id` or `strategy_ref` | Preserve if present | Copy as strategy reference | Promote strategy or infer approval | Reference only. |
| `strategy_version` | `strategy_version`, `source_schema_versions` | Preserve exactly | Copy as source strategy version | Treat version as approval maturity | Version is lineage only. |
| `snapshot_id` | `source_snapshot_ref`, `audit_trace` | Preserve exactly | Copy as feature snapshot lineage | Treat snapshot as empirical validation | Snapshot lineage only. |
| `output_scope` | `source_artifact_type`, `motor_b_evidence_state` | Must equal `raw_execution_scaffold` | Map to `raw_execution_scaffold` state | Convert to full backtest output | If different, fail closed. |
| `diagnostics_scope` | `evidence_level_normalized`, `motor_b_diagnostics_state` | Must equal `raw_scaffold_diagnostics_only` | Map to diagnostics-only state | Convert diagnostics into performance evidence | Diagnostics are descriptive only. |
| `registry_scope` | `audit_trace.registry_scope`, `source_artifact_type` | Must equal `raw_diagnostics_registry_only` | Preserve as registry lineage | Convert registry into evidence package | Registry is archival only. |
| `handoff_scope` | `source_artifact_type`, `adapter_limitations` | Must equal `raw_diagnostics_handoff_only` | Preserve as terminal Motor B handoff | Treat as 09 handoff approval | This is 06->07 only. |
| `simulation_status` | `backtest_status`, `motor_b_execution_state` | Preserve as raw scaffold status | Map `completed_raw_execution` to raw scaffold completed | Map to OOS/robustness/backtest pass | Any insufficient/rejected state must block normalization. |
| `trade_count` | `diagnostics_payload.trade_count` | Preserve as descriptive metric | Copy as raw diagnostic | Use as quality score or promotion signal | No threshold-based promotion in V1. |
| `ending_capital` | `diagnostics_payload.ending_capital` | Preserve as descriptive metric | Copy as raw diagnostic | Treat as profitability evidence | No performance evidence in V1. |
| `return_pct` | `diagnostics_payload.return_pct` | Preserve as descriptive metric | Copy as raw diagnostic | Convert into confidence or ranking | Return is raw scaffold diagnostic only. |
| `non_approval_statement` | `non_approval_statement`, `forbidden_downstream_usage` | Preserve or strengthen | Copy and append Stage 07 restrictions | Weaken or omit | Must remain visible through RiskHandoffPackage. |
| deterministic SHA-256 ids | `adapter_id`, `audit_trace`, `source_hashes` | Preserve and reference | Build Stage 07 ids from stable lineage | Use randomness or wall-clock for identity | Stage 07 dry-run ids must be deterministic. |
| source stage | `source_stage` | Set to `06 Backtesting Engine` | Copy as source owner | Reassign ownership to 07 | 07 adapts; it does not own Motor B. |
| source artifact type | `source_artifact_type` | Set to `RawDiagnosticsHandoffContract` | Copy exactly | Reclassify as `MotorBOutputContract` evidence | Distinguish from older doc contract. |
| lineage | `source_contract_references`, `audit_references` | Preserve full upstream ids | Copy handoff, registry, diagnostics, simulation, package, strategy, snapshot ids | Drop upstream ids | Required for replay. |
| audit trace | `Stage07AuditTrace` | Include handoff path and ids | Add adapter document reference | Replace Stage 06 trace | 07 trace extends source trace. |
| `evidence_completeness_level` absent | `evidence_completeness_level` | Derive conservatively as `framework_only` | Explicit adapter derivation | Infer empirical completeness | Absence must fail closed. |
| empirical results absent | `empirical_results_available` | Set `false` | Preserve blocked evidence state | Infer true from raw diagnostics | V1 has no empirical evidence. |
| `confidence_status` absent | `confidence_status` | Set `confidence_not_available` | Explicit blocked confidence state | Infer from diagnostics, LLM, fusion, or debate | No confidence invention. |
| `confidence_score` absent | `confidence_score` | Set `null` | Preserve null | Fill with return, LLM score, or classifier score | Null remains null. |
| `final_signal_confidence_score` absent | `final_signal_confidence_score` | Set `null` downstream | Preserve null through fusion/governance | Compute under framework-only | Block 09 policy must preserve null. |
| `paper_trading_ready` absent | `paper_trading_ready` | Set `false` | Preserve blocked readiness | Infer readiness from handoff completion | Stage 09 remains blocked. |
| `handoff_to_09` absent | `handoff_to_09` | Set `blocked` | Preserve blocked downstream handoff | Mark approved | 06->07 handoff is not 09 handoff. |
| downstream restrictions | `forbidden_downstream_usage` | Populate from non-approval scope | Include paper/live/capital/promotion/confidence/evidence bans | Relax restrictions | Must pass to all 07 outputs. |
| missing evidence | `missing_evidence`, `blocking_gaps` | Add explicit missing OOS/walk-forward/robustness/confidence/promotion evidence | Preserve as blocking gaps | Treat diagnostics as closing gaps | Missing evidence remains unresolved. |
| forbidden downstream usage | `forbidden_downstream_usage` | Must include paper trading, live trading, capital allocation, confidence generation, evidence claims, promotion | Union with Stage 07 restrictions | Remove any Stage 06 restriction | Conservative union required. |
| diagnostics payload | `diagnostics_payload`, `normalization_limitations` | Preserve as descriptive raw diagnostics | Copy trade_count, ending_capital, return_pct | Use as final signal metrics | Payload is not evidence. |
| error states | `normalization_status`, `blocking_gaps` | Fail closed | Mark rejected/degraded/unavailable | Continue as accepted evidence | Error states block promotion. |
| insufficient information states | `normalization_status`, `blocking_gaps` | Fail closed | Mark insufficient information and preserve source reason | Fill missing values | No inference from missing fields. |

## F. Preservation Rules

Stage 07 must preserve:

```text
framework_only remains framework_only
confidence_not_available remains confidence_not_available
confidence_score = null remains null
paper_trading_ready = false remains false
handoff_to_09 = blocked remains blocked
empirical_results_available = false remains false
not_promoted remains not_promoted
```

Stage 07 may add stronger restrictions. Stage 07 must not weaken any source
restriction.

## G. Forbidden Promotions

Stage 07 must not:

- convert raw diagnostics into an evidence package;
- convert descriptive metrics into confidence;
- convert mock or dry-run output into empirical validation;
- infer strategy promotion;
- infer paper trading eligibility;
- invent OOS, walk-forward, or robustness results;
- allow LLM outputs to substitute for empirical evidence;
- allow Stage 07 to relax restrictions carried by Stage 06;
- convert `completed_raw_execution` into a passed backtest;
- convert `return_pct` into performance evidence;
- convert `RiskHandoffPackage` into Stage 09 readiness.

## H. Missing or Null Handling

When a field required by Stage 07 is missing, null, unknown, or
`insufficient_information`, Stage 07 must:

```text
fail closed
preserve null
add blocking_gap
no promotion
no readiness
```

Specific handling:

- missing ids: reject adapter input or mark unavailable;
- missing source scope: reject adapter input;
- missing confidence: set `confidence_status = confidence_not_available` and
  `confidence_score = null`;
- missing empirical evidence: set `empirical_results_available = false` and
  add missing evidence;
- insufficient simulation status: reject or degrade as non-executable, never
  normalize into evidence;
- unknown downstream restriction: add blocking gap and preserve non-approval.

## I. Compatibility With Stage 08

Stage 08 is built to consume Stage 07 artifacts, not raw Stage 06 artifacts.

This adapter preserves that boundary:

```text
RawDiagnosticsHandoffContract
-> MotorBRawDiagnosticsInputForStage07
-> NormalizedMotorBInput
-> NormalizedSignalCandidate
-> FusedSignalCandidate
-> ConfidenceGovernanceResult
-> RiskHandoffPackage
-> Stage07AuditTrace
-> 08 Risk Engine intake
```

Stage 08 must continue receiving `RiskHandoffPackage`,
`ConfidenceGovernanceResult`, `FusedSignalCandidate`, `Stage07AuditTrace`, and
related Stage 07 artifacts. Stage 08 must not bypass Stage 07 by directly
consuming raw Stage 06 output for operational decisions.

## J. V1 Dry-Run Compatibility

This contract is the controlling reference for Block 2:

```text
Block 2 — 07 Minimal Executable Dry-Run
```

The dry-run may use mock `RawDiagnosticsHandoffContract`-shaped fixtures to
validate field propagation and blocked-state preservation.

Dry-run output must be marked synthetic or dry-run only.

Dry-run does not mean empirical evidence.

Dry-run does not mean confidence.

Dry-run does not mean paper trading readiness.

## K. V2 Operational Extension

In V2, this adapter may be extended if Motor B produces governed empirical
evidence with explicit OOS, walk-forward, robustness, confidence, and promotion
status.

That future extension must be explicit and versioned. It must not reinterpret
current V1 raw diagnostics as V2 evidence.

Until that V2 extension exists, the current adapter state remains:

```text
evidence_completeness_level = framework_only
empirical_results_available = false
confidence_status = confidence_not_available
confidence_score = null
paper_trading_ready = false
handoff_to_09 = blocked
strategy_promotion_status = not_promoted
```

