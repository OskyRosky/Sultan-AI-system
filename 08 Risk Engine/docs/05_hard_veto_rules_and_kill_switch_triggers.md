# 08 Risk Engine — Block 05: Hard Veto Rules and Kill Switch Triggers

## Purpose

Block 05 defines the absolute veto rules of the Risk Engine and the declarative taxonomy of Kill Switch triggers.

This block exists to prevent critical conditions, contradictions, missing evidence, operational claims, contract violations, prohibited inferences, unauditable artifacts, source conflicts, or severe risk states from advancing toward downstream handling.

This block does not execute the Kill Switch in production. It does not connect exchanges. It does not generate orders. It does not allocate capital. It does not activate any productive operational control.

## Hard Veto Authority

Stage 08 Risk Engine has authority to apply hard veto to:

- `RiskHandoffPackage`;
- `FusedSignalCandidate`;
- `ConfidenceGovernanceResult`;
- Stage 07 handoff artifacts;
- policy registry entries;
- downstream requests;
- human override attempts;
- operational claims;
- confidence claims;
- Paper Trading requests;
- Live Trading requests;
- execution requests;
- capital allocation attempts.

A hard veto is not a warning or recommendation. It is a formal block of downstream eligibility.

Once hard veto is triggered, the affected artifact, package, request, policy entry, or downstream path cannot proceed to Paper Trading, Live Trading, execution, capital allocation, promotion, confidence assignment, or handoff to Stage 09 unless later review formally resolves the condition with replayable evidence and applicable Stage 08 controls.

## Kill Switch Authority

The Kill Switch is the emergency authority of the Risk Engine.

The Kill Switch:

- may block all downstream handling;
- may require immediate veto;
- may require emergency review;
- may require human review;
- may require Risk Engine review;
- may suspend any path toward Paper Trading, Live Trading, execution, capital allocation, or promotion;
- may operate independently of Human Review;
- cannot be used to enable trading;
- cannot be used to unlock Paper Trading;
- cannot be used as a substitute for empirical evidence.

The Kill Switch is not:

- capital allocation;
- position sizing;
- ordinary stop loss;
- ordinary drawdown limit;
- risk budget;
- exposure template;
- strategy scoring;
- execution policy.

The Kill Switch is a conservative emergency and veto mechanism only.

## Current Framework-Only Veto Baseline

Under the current state:

```text
evidence_completeness_level = framework_only
simulation_status = backtest_not_implemented
oos_validation_status = oos_not_available
robustness_status = robustness_not_available
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
handoff_to_09 = blocked
live_trading_status = blocked
execution_eligibility = blocked
order_generation_eligibility = blocked
exchange_connection_eligibility = blocked
capital_allocation_eligibility = blocked
productive_position_sizing_eligibility = blocked
risk_budget_activation = blocked
promotion_status = not_promoted
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

These values are the mandatory baseline for veto and blocking. No hard veto rule, Kill Switch trigger, policy registry entry, review state, or future RiskDecision input may weaken this baseline under `framework_only`.

## Hard Veto Trigger Categories

Declarative hard veto trigger categories include:

- `framework_only_veto`;
- `missing_empirical_evidence_veto`;
- `missing_backtest_veto`;
- `missing_oos_validation_veto`;
- `missing_walk_forward_veto`;
- `missing_robustness_veto`;
- `confidence_unavailable_veto`;
- `confidence_invention_veto`;
- `synthetic_input_veto`;
- `synthetic_evidence_as_real_veto`;
- `prohibited_inference_veto`;
- `prompt_injection_veto`;
- `event_critical_veto`;
- `audit_trace_missing_veto`;
- `unauditable_package_veto`;
- `contract_violation_veto`;
- `source_conflict_veto`;
- `paper_trading_request_without_evidence_veto`;
- `live_trading_request_without_evidence_veto`;
- `direct_execution_request_veto`;
- `capital_allocation_attempt_veto`;
- `strategy_promotion_without_evidence_veto`;
- `human_override_without_evidence_veto`;
- `downstream_restriction_violation_veto`.

This taxonomy is declarative and not executable in this phase.

## Framework-Only Hard Veto Rule

If `evidence_completeness_level = framework_only`, the Risk Engine must veto:

- Paper Trading activation;
- Live Trading activation;
- execution;
- order generation;
- exchange connection;
- capital allocation;
- productive position sizing;
- risk budget activation;
- strategy promotion;
- confidence assignment;
- `handoff_to_09`.

A `framework_only` package may advance to internal review within Stage 08. It cannot advance downstream.

Internal review is not operational approval.

## Missing Evidence Veto Rules

Missing evidence must produce veto, blocking, or required review according to severity when there is:

- no real backtesting;
- no OOS validation;
- no walk-forward validation;
- no robustness testing;
- no empirical historical results;
- no audit trace;
- no reproducibility metadata;
- no data version references;
- no strategy version references;
- no risk policy compliance evidence.

These gaps will be classified more broadly in Block 06 — Missing Evidence and Blocking Gap Assessment.

Block 05 may hard veto critical missing evidence paths, but it does not build the complete missing evidence taxonomy.

## Confidence Hard Veto Rules

Under the current state:

```text
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

The Risk Engine must veto any attempt to:

- invent `confidence_score`;
- invent `final_signal_confidence_score`;
- infer confidence from LLM output;
- infer confidence from Bull/Bear agreement;
- infer confidence from Motor A;
- infer confidence from Motor C;
- infer confidence from fused signal alignment;
- infer confidence from favorable event;
- infer confidence from human optimism;
- use textual confidence as trading confidence.

Block 07 will develop the confidence and evidence sufficiency gate more broadly.

## Prohibited Inference and Prompt Injection Veto Rules

The Risk Engine must veto instructions or artifacts that attempt to:

- bypass risk gates;
- convert raw LLM output into approval;
- convert raw signals into execution;
- convert `review_package_only` into promotion;
- convert structural validation into approval;
- convert favorable event into eligibility;
- convert human review metadata into approval;
- hide missing evidence;
- relabel synthetic evidence as real evidence;
- alter downstream blocking states without formal evidence.

Prompt injection is a hard veto trigger. If prompt injection attempts to modify risk rules, downstream blocking states, evidence status, confidence status, promotion status, or operational permissions, it must also trigger Kill Switch review.

## Contract Violation and Source Conflict Veto Rules

The Risk Engine must veto or block when there are:

- inconsistencies with Stage 06 Motor B Output Contract;
- inconsistencies with Stage 07 closure;
- contradictions with Blocks 00-05 or with the veto rules and Kill Switch trigger taxonomy defined in this block;
- missing `non_approval_statement`;
- missing `forbidden_downstream_usage`;
- missing audit trace;
- unversioned artifacts;
- unaudited artifacts;
- claims of Paper Trading ready under `framework_only`;
- claims of confidence available with `confidence_score = null`;
- claims of promotion with `promotion_status = not_promoted`.

Material source conflict must produce mandatory review and downstream blocking.

Source conflict must not be resolved by inference, LLM output, favorable interpretation, or human optimism.

## Event Critical Veto Rules

Critical events may produce hard veto or Kill Switch handling.

Block 05 does not redefine complete event precedence. That belongs to Block 08 — Event, Regime and Market Risk Gate.

Event asymmetry must be preserved:

- favorable events unlock nothing;
- negative or critical events may block, degrade, suspend, escalate, or trigger Kill Switch.

A critical event cannot be relaxed by favorable regime, LLM agreement, fused signal alignment, or human optimism.

## Direct Operational Request Veto Rules

Under the current state, any direct request for:

- trade execution;
- order generation;
- exchange connection;
- Paper Trading activation;
- Live Trading activation;
- capital allocation;
- productive position sizing;
- risk budget activation;
- strategy promotion;

must receive hard veto.

These requests must not be converted into operational review candidates or conditional approval.

## Kill Switch Trigger Taxonomy

Declarative Kill Switch triggers include:

- `kill_switch_trigger_framework_only_misrepresented`;
- `kill_switch_trigger_direct_execution_request`;
- `kill_switch_trigger_paper_trading_bypass_attempt`;
- `kill_switch_trigger_live_trading_bypass_attempt`;
- `kill_switch_trigger_capital_allocation_attempt`;
- `kill_switch_trigger_confidence_invention`;
- `kill_switch_trigger_prompt_injection`;
- `kill_switch_trigger_source_conflict_material`;
- `kill_switch_trigger_missing_audit_trace_critical`;
- `kill_switch_trigger_event_critical`;
- `kill_switch_trigger_contract_violation_material`;
- `kill_switch_trigger_downstream_restriction_violation`;
- `kill_switch_trigger_human_override_without_evidence`;
- `kill_switch_trigger_synthetic_evidence_as_real`;
- `kill_switch_trigger_unknown_critical_risk`.

These triggers are declarative. They do not execute productive automation in this phase.

## Kill Switch Outcome Taxonomy

Declarative Kill Switch outcomes include:

- `kill_switch_required`;
- `kill_switch_not_required`;
- `all_downstream_blocked`;
- `risk_engine_veto_required`;
- `paper_trading_blocked`;
- `live_trading_blocked`;
- `execution_blocked`;
- `capital_allocation_blocked`;
- `promotion_blocked`;
- `confidence_assignment_blocked`;
- `handoff_to_09_blocked`;
- `human_review_required`;
- `risk_engine_review_required`;
- `emergency_review_required`;
- `audit_trace_required`;
- `source_reconciliation_required`;
- `package_rejected`;
- `package_degraded`;
- `package_quarantined_for_review`.

No Kill Switch outcome can approve trading or unlock downstream eligibility.

## Kill Switch Severity Levels

Declarative Kill Switch severity levels are:

- `kill_switch_severity_none`;
- `kill_switch_severity_low_review`;
- `kill_switch_severity_medium_block`;
- `kill_switch_severity_high_veto`;
- `kill_switch_severity_critical_emergency_block`.

Only `kill_switch_severity_none` means no Kill Switch is required. It does not mean operational approval.

Under `framework_only`, even with `kill_switch_severity_none`, Paper Trading and downstream operational usage remain blocked by other gates.

## Hard Veto Outcome Taxonomy

Declarative hard veto outcomes include:

- `hard_veto_not_triggered`;
- `hard_veto_triggered_framework_only`;
- `hard_veto_triggered_missing_evidence`;
- `hard_veto_triggered_confidence_unavailable`;
- `hard_veto_triggered_confidence_invention`;
- `hard_veto_triggered_synthetic_evidence`;
- `hard_veto_triggered_prompt_injection`;
- `hard_veto_triggered_contract_violation`;
- `hard_veto_triggered_source_conflict`;
- `hard_veto_triggered_event_critical`;
- `hard_veto_triggered_operational_request`;
- `hard_veto_triggered_capital_allocation_attempt`;
- `hard_veto_triggered_strategy_promotion_attempt`;
- `hard_veto_triggered_human_override_violation`;
- `hard_veto_requires_human_review`;
- `hard_veto_requires_risk_engine_review`.

These outcomes are not the final `RiskDecision` of Block 12.

`hard_veto_not_triggered` must not be interpreted as operational approval.

## Veto and Kill Switch Output Record

Stage 08 may document veto and Kill Switch outcomes with a record structure such as:

- `veto_record_id`;
- `evaluated_at`;
- `source_artifact_id`;
- `source_stage`;
- `source_block`;
- `source_document_ref`;
- `evaluated_policy_ref`, if applicable;
- `veto_triggered`;
- `veto_trigger_category`;
- `hard_veto_outcome`;
- `kill_switch_triggered`;
- `kill_switch_trigger_category`;
- `kill_switch_severity`;
- `kill_switch_outcome`;
- `downstream_blocking_status`;
- `paper_trading_eligibility`;
- `live_trading_status`;
- `execution_eligibility`;
- `capital_allocation_eligibility`;
- `promotion_status`;
- `confidence_status`;
- `confidence_score`;
- `final_signal_confidence_score`;
- `handoff_to_09`;
- `required_review`;
- `required_evidence`;
- `audit_trace_ref`;
- `final_note_non_operational`.

This block does not create a database, storage layer, productive Kill Switch implementation, or execution system. This record is documentary only.

## Relationship With Block 00

Block 00 declared the Kill Switch as an emergency authority of the Risk Engine.

Block 05 develops that declaration into hard veto, trigger, severity, and outcome taxonomies.

Block 05 does not contradict Block 00 authority and does not convert Kill Switch into a productive operational policy.

## Relationship With Block 04

Block 04 registers risk policies documentarily.

Block 05 defines absolute veto rules and Kill Switch triggers.

`policy_documentary_only`, `policy_future_candidate`, or `policy_blocked_under_framework_only` cannot be converted into active enforcement by Block 05.

## Relationship With Block 06

Block 06 — Missing Evidence and Blocking Gap Assessment will classify missing evidence and blocking gaps in more detail.

Block 05 may veto critical missing evidence, but it does not build the complete general gap taxonomy of Block 06.

## Relationship With Block 12

Block 12 — Risk Decision Engine will produce the formal `RiskDecision`.

Block 05 produces hard veto outcomes and Kill Switch outcomes, but not the final `RiskDecision`.

A hard veto may be mandatory input for `RiskDecision`, but it must not become trade execution or approval.

## Explicit Non-Goals

This block does not do:

- execute Kill Switch in production;
- connect exchanges;
- execute trades;
- generate orders;
- activate Paper Trading;
- activate Live Trading;
- allocate capital;
- calculate productive position sizing;
- activate risk budgets;
- enforce policies productively;
- create active policy engine;
- create stop loss engine;
- create drawdown engine;
- create exposure engine;
- create final `RiskDecision`;
- create Paper Trading eligibility approval;
- create Live Trading eligibility approval;
- create `confidence_score`;
- create `final_signal_confidence_score`;
- create empirical evidence;
- run backtesting;
- run OOS validation;
- run walk-forward;
- run robustness;
- implement human override policy;
- implement audit replay.

Block 05 is a documentary hard veto and Kill Switch taxonomy. It preserves downstream blocking and cannot be used as an approval path.
