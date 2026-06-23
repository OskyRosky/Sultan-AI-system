# 09 Paper Trading — Block 09.1: Input / Risk Handoff Contract

## Purpose

Block 09.1 defines the only permitted input boundary into `09 Paper Trading` V1.

This block documents how Stage 09 may receive handoff from `08 Risk Engine` while preserving all V1 non-operational governance blocks.

Block 09.1 produces a contract only. It does not implement paper trading runtime, broker/exchange connections, CCXT integration, order routing, fills, slippage, fees, reconciliation, portfolio sizing, execution logic, or operational readiness.

## Stage 08 Runtime Inspection Summary

This contract is based on inspection of the current Stage 08 implementation, not only on theoretical documentation.

The inspected Stage 08 files are:

```text
08 Risk Engine/src/contracts.py
08 Risk Engine/src/dry_run.py
08 Risk Engine/src/decision_engine.py
08 Risk Engine/src/intake.py
08 Risk Engine/src/audit_trace.py
```

Current Stage 08 runtime output is produced by:

```text
08 Risk Engine/src/dry_run.py
run_stage08_dry_run(...)
```

The dry-run returns a dataclass:

```text
Stage08DryRunResult
```

defined in:

```text
08 Risk Engine/src/contracts.py
```

`Stage08DryRunResult` contains:

```text
input_package: Stage08InputPackage
gate_results: tuple[Stage08GateResult, ...]
risk_decision: Stage08RiskDecision
audit_trace: Stage08AuditTrace
```

The current Stage 08 decision artifact is:

```text
Stage08RiskDecision
```

defined in:

```text
08 Risk Engine/src/contracts.py
```

and produced by:

```text
08 Risk Engine/src/decision_engine.py
build_risk_decision(...)
```

Stage 08 currently produces in-memory Python dataclasses with `to_dict()` serialization support. It does not currently persist a JSON file, markdown report, registry record, database record, or standalone handoff-to-09 artifact.

The closest current equivalent to a Stage 09 handoff artifact is the `risk_decision` field inside `Stage08DryRunResult`.

## Current Stage08RiskDecision Fields

The current `Stage08RiskDecision` contains:

```text
risk_decision_id
related_stage08_input_package_id
risk_decision_status
operational_status
risk_approval
paper_trading_ready
handoff_to_09
downstream_operational_eligibility
stage_09_operational_start_allowed
capital_allocation_ready
live_trading_ready
reason_codes
blocking_gaps
forbidden_downstream_usage
non_approval_statement
```

Current blocked values observed from `run_stage08_dry_run()` are:

```text
risk_decision_status = blocked
operational_status = non_operational
risk_approval = false
paper_trading_ready = false
handoff_to_09 = blocked
downstream_operational_eligibility = blocked
stage_09_operational_start_allowed = false
capital_allocation_ready = false
live_trading_ready = false
```

Current reason codes include:

```text
confidence_not_available
confidence_score_missing
downstream_operational_eligibility_blocked
empirical_evidence_not_available
final_signal_confidence_score_missing
forbidden_downstream_usage_present
framework_only_input
handoff_to_09_blocked
paper_trading_blocked
strategy_not_promoted
upstream_risk_handoff_blocked
v1_dry_run_only
```

Current blocking gaps include:

```text
confidence_not_available
confidence_score_missing
downstream_operational_eligibility_blocked
empirical_evidence_not_available
final_signal_confidence_score_missing
forbidden_downstream_usage_present
framework_only_input
handoff_to_09_blocked
missing_real_empirical_evidence
oos_not_available
paper_trading_blocked
robustness_not_available
stage07_dry_run_only_not_operational
strategy_not_promoted
upstream_stage07_risk_handoff_blocked
walk_forward_not_available
```

## Upstream Authority

`08 Risk Engine` is the only valid upstream authority for Stage 09.

Stage 09 must not consume:

- raw Stage 06 diagnostics;
- raw Stage 06 backtesting artifacts;
- direct Stage 07 signals;
- Stage 07 `RiskHandoffPackage` directly;
- raw Motor A outputs;
- raw Motor B outputs;
- raw Motor C outputs;
- raw LLM outputs;
- manually promoted strategy claims;
- direct execution requests;
- any input bypassing Stage 08.

Stage 09 cannot reinterpret Stage 08 blocked output as approval.

If Stage 08 is blocked, Stage 09 remains blocked.

## Required Stage 08 Source Artifact

The current required Stage 08 source artifact for V1 is:

```text
Stage08DryRunResult.risk_decision: Stage08RiskDecision
```

Source path:

```text
08 Risk Engine/src/contracts.py
08 Risk Engine/src/dry_run.py
08 Risk Engine/src/decision_engine.py
```

In V1, this artifact may be referenced only as a non-operational dry-run decision record.

It is not a Paper Trading approval.

It is not an executable paper trading session input.

It is not a candidate order package.

It is not a portfolio construction instruction.

It is not a broker/exchange instruction.

## Required Handoff Fields

Before Stage 09 may even consider documentary-only acceptance, the Stage 08 source must provide the following fields or traceable equivalents.

Fields that exist today in `Stage08RiskDecision`:

| Stage 09 requirement | Current Stage 08 field | Current V1 value |
| --- | --- | --- |
| Stage 08 decision identifier | `risk_decision_id` | `stage08-risk-decision-...` |
| decision status | `risk_decision_status` | `blocked` |
| operational status | `operational_status` | `non_operational` |
| risk approval | `risk_approval` | `false` |
| handoff to Stage 09 | `handoff_to_09` | `blocked` |
| paper trading readiness | `paper_trading_ready` | `false` |
| Stage 09 operational start | `stage_09_operational_start_allowed` | `false` |
| capital allocation readiness | `capital_allocation_ready` | `false` |
| live trading readiness | `live_trading_ready` | `false` |
| downstream operational eligibility | `downstream_operational_eligibility` | `blocked` |
| blocking reasons | `reason_codes` and `blocking_gaps` | blocked reason tuples |
| forbidden usage | `forbidden_downstream_usage` | includes `paper_trading`, `live_trading`, `capital_allocation`, `stage_09_unlock` |
| source input reference | `related_stage08_input_package_id` | `stage08-input-...` |
| non-approval statement | `non_approval_statement` | V1 non-approval text |

Fields that exist today in adjacent Stage 08 artifacts:

| Stage 09 requirement | Current Stage 08 source | Current field |
| --- | --- | --- |
| source stage | `Stage08AuditTrace` | `stage_id = "08 Risk Engine"` |
| timestamp/generated at | `Stage08AuditTrace` | `dry_run_timestamp` |
| upstream artifact reference/path | repository path only | `08 Risk Engine/src/dry_run.py` and `Stage08DryRunResult` |
| artifact hashes | `Stage08AuditTrace` | `artifact_hashes`, `decision_hash` |

These `Stage08AuditTrace` fields were verified against:

```text
08 Risk Engine/src/audit_trace.py
08 Risk Engine/src/contracts.py
```

Fields that do not exist today and must be treated as V2/schema gaps:

| Conceptual requirement | Current status |
| --- | --- |
| explicit machine-readable schema version | not present |
| persisted JSON artifact path | not present |
| persisted Stage 08 decision report path | not present |
| explicit `source_stage` on `Stage08RiskDecision` itself | not present |
| explicit `strategy_promotion_status` on `Stage08RiskDecision` itself | not present; represented indirectly through `reason_codes` / `blocking_gaps` |
| explicit `confidence_status` on `Stage08RiskDecision` itself | not present; represented indirectly through `reason_codes` |
| explicit `confidence_score` on `Stage08RiskDecision` itself | not present; represented indirectly through `confidence_score_missing` |
| explicit `generated_at` on `Stage08RiskDecision` itself | not present; available in `Stage08AuditTrace.dry_run_timestamp` |
| explicit handoff-to-09 artifact | not present; `handoff_to_09` field exists inside `Stage08RiskDecision` |

Stage 09 V1 must document these gaps honestly and must not pretend the missing fields already exist.

## Acceptance Rules For Stage 09 V1

Stage 09 V1 may only classify a Stage 08 input as:

```text
documentary_only_candidate
```

when all governance constraints remain non-operational.

For V1, even a structurally valid Stage 08 handoff must not make Stage 09 operational.

The Stage 09 V1 intake posture must preserve:

```text
paper_trading_ready = false
stage_09_operational_start_allowed = false
live_trading_ready = false
capital_allocation_ready = false
risk_approval = false
handoff_to_09 = blocked
strategy_promotion_status = not_promoted
confidence_status = confidence_not_available
confidence_score = null
```

Because the current Stage 08 `Stage08RiskDecision` has `risk_approval = false`, V1 Stage 09 must remain non-operational. This is the expected V1 blocked state, not an implementation error.

## Rejection And Blocked-State Rules

Stage 09 must reject, or remain blocked, if:

- input does not originate from `08 Risk Engine`;
- input originates from Stage 06 directly;
- input originates from Stage 07 directly;
- input originates from raw motor outputs;
- input bypasses Stage 08;
- Stage 08 says `risk_decision_status = blocked`;
- Stage 08 says `risk_approval = false`;
- Stage 08 says `handoff_to_09 = blocked`;
- `strategy_promotion_status = not_promoted` is present; this is the expected V1 blocked/default state and does not authorize Stage 09 operational activity;
- any claim that `strategy_promotion_status` represents valid promotion without real V2 evidence is present;
- `confidence_score` is non-null in V1 without real V2 evidence;
- any readiness flag is true;
- any live readiness is claimed;
- any paper readiness is claimed;
- any capital allocation readiness is claimed;
- required Stage 08 artifact identity is missing;
- schema version cannot be traced;
- artifact path cannot be traced.

In V1, `risk_approval = false`, `handoff_to_09 = blocked`, and `strategy_promotion_status = not_promoted` are expected. They mean Stage 09 stays blocked and non-operational.

If `documentary_only_candidate` appears as a future upstream Stage 08 handoff value, Stage 09 may treat it only as documentary continuity. Separately, this document uses `documentary_only_candidate` as a Stage 09 V1 classification label for non-operational intake. Neither usage authorizes operational Stage 09 activity.

## Output Of 09.1

Block 09.1 produces only this input / risk handoff contract.

It must not produce:

- orders;
- candidate orders;
- sizing decisions;
- portfolio allocations;
- execution plans;
- fills;
- PnL;
- broker calls;
- exchange calls;
- CCXT calls;
- paper trading sessions;
- execution eligibility;
- capital allocation approval;
- live-small eligibility.

## V2 Notes

Future V2 work will need:

- concrete persisted `Stage08RiskDecision` schema;
- machine-readable handoff artifact;
- explicit schema version;
- explicit artifact path or registry reference;
- validation logic;
- risk-approved candidate portfolio handoff;
- execution eligibility check;
- paper trading session initialization only after risk approval;
- traceable rejection logs;
- traceable acceptance logs;
- replayable audit path from Stage 08 into Stage 09.

None of those items are implemented in Block 09.1.

## Exit Criteria For 09.1

Block 09.1 is complete only when:

- actual Stage 08 outputs have been inspected and summarized;
- the Stage 09 input boundary is documented;
- direct Stage 06 consumption is prohibited;
- direct Stage 07 consumption is prohibited;
- raw motor consumption is prohibited;
- blocked-state handling is explicit;
- V1 readiness flags remain false;
- V2 schema gaps are documented honestly;
- no operational paper trading code has been introduced.

## Block 09.1 Closure Statement

Block 09.1 establishes that the only valid Stage 09 input boundary is through Stage 08 Risk Engine output.

Today, the concrete Stage 08 decision object is `Stage08RiskDecision` inside `Stage08DryRunResult`. It is blocked, non-operational, and not a handoff approval.

Stage 09 remains non-operational and blocked.
