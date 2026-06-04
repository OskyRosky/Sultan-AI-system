# 08 Risk Engine — Block 15: Mock and Dry-Run Risk Scenarios

## Purpose

Block 15 defines documentary mock and dry-run scenarios for conceptually testing expected Stage 08 Risk Engine behavior.

The scenarios in this block are synthetic, documentary, non-operational, and non-empirical. They are review surfaces for expected blocking, veto, missing evidence, confidence unavailable, Paper Trading rejection, event critical, source conflict, hard veto candidate, Kill Switch review, human review, replay incomplete, and RiskDecision outcome handling.

This block declares:

- mocks are not evidence;
- dry-runs are not approval;
- mock scenario pass is not Paper Trading readiness;
- dry-run pass is not downstream eligibility;
- synthetic scenarios cannot substitute backtesting, OOS validation, walk-forward validation, robustness testing, or empirical historical results.

## Mock and Dry-Run Authority

Stage 08 / Block 15 may:

- define synthetic risk scenarios;
- define dry-run risk scenarios;
- define expected RiskDecision outcomes;
- test conceptual blocking paths;
- test conceptual veto paths;
- test conceptual missing evidence paths;
- test conceptual confidence unavailable paths;
- test conceptual event critical paths;
- test conceptual Paper Trading rejection paths;
- test conceptual human review paths;
- test conceptual audit replay incomplete paths;
- classify expected outcomes;
- document expected blocking behavior.

Mock and dry-run authority cannot approve, execute, allocate capital, promote strategies, create confidence, or unblock `handoff_to_09`.

## Current Framework-Only Mock Baseline

The current mock and dry-run baseline is:

```text
evidence_completeness_level = framework_only
simulation_status = backtest_not_implemented
oos_validation_status = oos_not_available
walk_forward_status = walk_forward_not_available
robustness_status = robustness_not_available
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
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
promotion_eligibility = blocked
risk_decision_status = blocked_framework_only
secondary_risk_decision_status = blocked_missing_evidence
mock_scenario_evidence_status = synthetic_not_empirical
dry_run_operational_effect = none
```

No mock or dry-run outcome may contradict this baseline under `framework_only`.

## Mock Is Not Evidence Rule

Mock scenarios are not empirical evidence.

Mock scenarios are not backtesting.

Mock scenarios are not OOS validation.

Mock scenarios are not walk-forward validation.

Mock scenarios are not robustness testing.

Mock scenarios are not historical results.

Mock scenarios are not market evidence.

Mock scenarios are not strategy validation.

Mock scenarios are not confidence evidence.

Mock scenarios cannot produce `confidence_score`.

Mock scenarios cannot produce `final_signal_confidence_score`.

Mock scenarios cannot unblock Paper Trading.

Mock scenarios cannot unblock `handoff_to_09`.

## Dry-Run Is Not Approval Rule

Dry-run pass is not approval.

Dry-run pass is not Paper Trading readiness.

Dry-run pass is not Live Trading readiness.

Dry-run pass is not execution permission.

Dry-run pass is not order generation permission.

Dry-run pass is not exchange connection permission.

Dry-run pass is not capital allocation permission.

Dry-run pass is not productive position sizing permission.

Dry-run pass is not risk budget activation.

Dry-run pass is not strategy promotion.

Dry-run pass is not `handoff_to_09`.

Dry-run pass cannot convert `blocked_missing_evidence` into `requires_more_evidence`.

Dry-run pass cannot convert `requires_more_evidence` into conditional approval.

## Required Mock Scenario Categories

Minimum mock scenario categories include:

- `framework_only` input;
- missing `RiskHandoffPackage`;
- incomplete `RiskHandoffPackage`;
- missing audit references;
- unversioned source artifact;
- missing Motor B evidence;
- `simulation_status = backtest_not_implemented`;
- `oos_validation_status = oos_not_available`;
- `walk_forward_status = walk_forward_not_available`;
- `robustness_status = robustness_not_available`;
- `confidence_status = confidence_not_available`;
- `confidence_score = null`;
- `final_signal_confidence_score = null`;
- prohibited confidence inference;
- LLM confidence substitution attempt;
- Bull/Bear agreement as confidence attempt;
- Motor A as Motor B substitute attempt;
- Motor C as Motor B substitute attempt;
- favorable event attempted as approval;
- event critical;
- source conflict;
- contract violation;
- prompt injection or instruction override attempt;
- synthetic evidence presented as real evidence;
- hard veto trigger;
- Kill Switch review required;
- human override attempt;
- Paper Trading request under blocked state;
- Live Trading request under blocked state;
- execution request under blocked state;
- capital allocation request under blocked state;
- position sizing request under blocked state;
- strategy promotion request under `framework_only`;
- `handoff_to_09` request under blocked state;
- replay incomplete missing refs;
- audit trace missing;
- `requires_more_evidence` vs `blocked_missing_evidence` distinction.

## Mock Scenario Catalog

This documentary catalog defines minimum scenario expectations:

1. `mock_framework_only_baseline`
   - Input: `evidence_completeness_level = framework_only`
   - Expected: `risk_decision_status = blocked_framework_only`
   - Expected: `paper_trading_eligibility = blocked`
   - Expected: `handoff_to_09 = blocked`
   - Expected: mock is not evidence

2. `mock_missing_backtest`
   - Input: `simulation_status = backtest_not_implemented`
   - Expected: `risk_decision_status = blocked_missing_evidence`
   - Expected: `paper_trading_eligibility = blocked`

3. `mock_missing_oos`
   - Input: `oos_validation_status = oos_not_available`
   - Expected: `risk_decision_status = blocked_missing_evidence`

4. `mock_missing_walk_forward`
   - Input: `walk_forward_status = walk_forward_not_available`
   - Expected: `risk_decision_status = blocked_missing_evidence`

5. `mock_missing_robustness`
   - Input: `robustness_status = robustness_not_available`
   - Expected: `risk_decision_status = blocked_missing_evidence`

6. `mock_confidence_null`
   - Input: `confidence_status = confidence_not_available`; `confidence_score = null`
   - Expected: `risk_decision_status = blocked_confidence_unavailable`
   - Expected: no confidence invention

7. `mock_llm_confidence_substitution_attempt`
   - Input: LLM textual confidence attempts to create trading confidence
   - Expected: `blocked_confidence_unavailable` or hard veto candidate
   - Expected: `confidence_score = null`

8. `mock_bull_bear_agreement_confidence_attempt`
   - Input: Bull/Bear agreement used as confidence
   - Expected: `blocked_confidence_unavailable`
   - Expected: `confidence_score = null`

9. `mock_favorable_event_unlock_attempt`
   - Input: favorable event attempts to unlock Paper Trading
   - Expected: `paper_trading_eligibility = blocked`
   - Expected: favorable events unlock nothing

10. `mock_event_critical`
    - Input: event critical
    - Expected: `blocked_event_risk` or `requires_human_review` or hard veto candidate
    - Expected: no approval

11. `mock_paper_trading_request_blocked`
    - Input: direct Paper Trading request under `framework_only`
    - Expected: `paper_trading_not_eligible`
    - Expected: `handoff_to_09 = blocked`

12. `mock_execution_request_blocked`
    - Input: execution request under `framework_only`
    - Expected: `blocked_execution_not_eligible` or hard veto candidate
    - Expected: `order_generation_eligibility = blocked`

13. `mock_capital_allocation_request_blocked`
    - Input: capital allocation request under `framework_only`
    - Expected: `blocked_capital_allocation_not_eligible`
    - Expected: `capital_allocation_eligibility = blocked`

14. `mock_strategy_promotion_request_blocked`
    - Input: strategy promotion request under `framework_only`
    - Expected: `blocked_strategy_promotion_not_eligible`
    - Expected: `promotion_status = not_promoted`

15. `mock_human_override_attempt`
    - Input: human review attempts `framework_only` bypass
    - Expected: `human_review_required` or `risk_engine_review_required`
    - Expected: no approval

16. `mock_kill_switch_review_required`
    - Input: Kill Switch trigger candidate
    - Expected: `blocked_kill_switch_review_required`
    - Expected: all downstream blocked

17. `mock_audit_replay_incomplete`
    - Input: missing audit trace refs
    - Expected: `replay_incomplete_missing_refs`
    - Expected: blocking preserved

18. `mock_requires_more_evidence_vs_blocked_missing_evidence`
    - Input A: required evidence does not exist
    - Expected A: `blocked_missing_evidence`
    - Input B: some evidence exists but insufficient
    - Expected B: `requires_more_evidence`
    - Expected: neither outcome approves anything

This catalog is documentary and not executable.

## Dry-Run Scenario Taxonomy

Documentary dry-run statuses include:

- `dry_run_not_attempted`;
- `dry_run_documentary_only`;
- `dry_run_blocking_path_verified`;
- `dry_run_veto_path_verified`;
- `dry_run_missing_evidence_path_verified`;
- `dry_run_confidence_unavailable_path_verified`;
- `dry_run_event_risk_path_verified`;
- `dry_run_paper_trading_rejection_verified`;
- `dry_run_execution_rejection_verified`;
- `dry_run_capital_allocation_rejection_verified`;
- `dry_run_promotion_rejection_verified`;
- `dry_run_handoff_to_09_rejection_verified`;
- `dry_run_replay_incomplete_path_verified`;
- `dry_run_expected_outcome_mismatch`;
- `dry_run_requires_review`;
- `dry_run_failed_ambiguous_outcome`.

Under `framework_only`, the following statuses are prohibited:

- `dry_run_approved`;
- `dry_run_paper_trading_approved`;
- `dry_run_execution_approved`;
- `dry_run_capital_allocation_approved`;
- `dry_run_strategy_promoted`;
- `dry_run_handoff_to_09_approved`.

## Expected Outcome Rules

Expected outcome rules are conservative:

- if mock input is `framework_only`, expected outcome must preserve blocking;
- if required empirical evidence is missing, expected outcome must be `blocked_missing_evidence`;
- if some evidence exists but is insufficient, expected outcome may be `requires_more_evidence`, but not approval;
- if confidence is null, expected outcome must preserve `confidence_score = null`;
- if Paper Trading is requested under blocked state, expected outcome must reject or block;
- if execution is requested under blocked state, expected outcome must reject, block, or hard veto candidate;
- if capital allocation is requested under blocked state, expected outcome must reject or block;
- if promotion is requested under `framework_only`, expected outcome must preserve `not_promoted`;
- if audit refs are missing, expected outcome must preserve blocking;
- if replay is incomplete, expected outcome must preserve blocking.

## Mock Scenario Record

Stage 08 may document a mock scenario with fields such as:

- `mock_scenario_id`;
- `mock_scenario_version`;
- `mock_category`;
- `mock_description`;
- `synthetic_input_label`;
- `input_state_summary`;
- `expected_risk_decision_status`;
- `expected_secondary_status`;
- `expected_paper_trading_eligibility`;
- `expected_live_trading_status`;
- `expected_execution_eligibility`;
- `expected_order_generation_eligibility`;
- `expected_exchange_connection_eligibility`;
- `expected_capital_allocation_eligibility`;
- `expected_productive_position_sizing_eligibility`;
- `expected_risk_budget_activation`;
- `expected_promotion_status`;
- `expected_promotion_eligibility`;
- `expected_downstream_operational_eligibility`;
- `expected_handoff_to_09`;
- `expected_confidence_status`;
- `expected_confidence_score`;
- `expected_final_signal_confidence_score`;
- `expected_hard_veto_status`;
- `expected_kill_switch_review_status`;
- `expected_human_review_status`;
- `expected_audit_replay_status`;
- `expected_required_future_evidence`;
- `expected_required_review`;
- `expected_non_approval_statement`;
- `mock_is_evidence`;
- `dry_run_is_approval`;
- `final_note_non_operational`.

Required fixed values:

```text
mock_is_evidence = false
dry_run_is_approval = false
```

This block does not create a database, storage layer, executable fixture store, or productive mock registry. The record is documentary only.

## Dry-Run Record

Stage 08 may document a dry-run with fields such as:

- `dry_run_id`;
- `dry_run_version`;
- `dry_run_requested_at`;
- `dry_run_completed_at`;
- `dry_run_scope`;
- `mock_scenario_ref`;
- `source_stage`;
- `source_block`;
- `expected_outcome_ref`;
- `observed_documentary_outcome`;
- `expected_vs_observed_status`;
- `mismatch_reason`;
- `dry_run_status`;
- `dry_run_passed`;
- `dry_run_passed_is_approval`;
- `paper_trading_eligibility`;
- `live_trading_status`;
- `execution_eligibility`;
- `order_generation_eligibility`;
- `exchange_connection_eligibility`;
- `capital_allocation_eligibility`;
- `productive_position_sizing_eligibility`;
- `risk_budget_activation`;
- `promotion_status`;
- `promotion_eligibility`;
- `downstream_operational_eligibility`;
- `handoff_to_09`;
- `confidence_status`;
- `confidence_score`;
- `final_signal_confidence_score`;
- `required_future_evidence`;
- `required_review`;
- `audit_trace_ref`;
- `final_note_non_operational`.

Required fixed value:

```text
dry_run_passed_is_approval = false
```

This block does not create executable dry-runs, pytest tests, runtime validation, a database, or productive storage. The record is documentary only.

## Current Mock/Dry-Run Conclusion

Under the current state:

```text
mock_policy_status = non_operational_documentary
mock_scenarios_are_evidence = false
dry_runs_are_approval = false
mock_pass_can_unblock_paper_trading = false
dry_run_pass_can_unblock_handoff_to_09 = false
mock_pass_can_create_confidence = false
dry_run_pass_can_create_empirical_evidence = false
paper_trading_eligibility = blocked
live_trading_status = blocked
execution_eligibility = blocked
order_generation_eligibility = blocked
exchange_connection_eligibility = blocked
capital_allocation_eligibility = blocked
productive_position_sizing_eligibility = blocked
risk_budget_activation = blocked
promotion_status = not_promoted
promotion_eligibility = blocked
downstream_operational_eligibility = blocked
handoff_to_09 = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

No mock pass, dry-run pass, expected outcome match, or scenario catalog entry can create Paper Trading readiness, downstream eligibility, confidence, capital allocation, execution permission, promotion, or `handoff_to_09`.

## Relationship With Block 12

Block 12 defines `RiskDecision`.

Block 15 can define mock scenarios that expect RiskDecision outcomes, but cannot produce or execute `RiskDecision`.

Expected RiskDecision outcomes in this block are documentary expectations only. They are not final RiskDecision records.

## Relationship With Block 14

Block 14 defines Audit, Traceability and Risk Decision Replay.

Block 15 can define mock and dry-run scenarios for replay completeness and missing refs, but cannot create replay runtime or approval.

Replay-related mock pass cannot convert `replay_successful`, `audit_complete`, or `traceability_complete` into approval.

## Relationship With Block 16

Block 16 will define Quality Gates for Stage 08.

Block 15 can provide mock and dry-run expectations that Block 16 may use as quality gate inputs, but Block 15 does not close quality gates.

Quality gate usage of mock or dry-run expectations must preserve that mocks are not empirical evidence and dry-runs are not approval.

## Relationship With Block 17

Block 17 closes Stage 08 and formalizes handoff to Stage 09.

Block 15 cannot unblock `handoff_to_09` under the current `framework_only` state.

Mock scenario coverage, dry-run pass, or expected outcome matching cannot create Stage 09 readiness.

## Explicit Non-Goals

This block does not do:

- create empirical evidence;
- run backtesting;
- run OOS validation;
- run walk-forward;
- run robustness;
- approve Paper Trading;
- approve Live Trading;
- approve execution;
- approve order generation;
- approve exchange connection;
- approve capital allocation;
- approve productive position sizing;
- activate risk budgets;
- promote strategies;
- create `confidence_score`;
- create `final_signal_confidence_score`;
- implement mock runtime;
- implement dry-run runtime;
- implement executable tests;
- implement pytest tests;
- implement audit replay runtime;
- implement human approval workflow;
- implement override runtime;
- execute RiskDecision;
- execute Kill Switch;
- create Paper Trading runtime;
- create Paper Trading simulator;
- create execution engine;
- create capital allocator;
- close Stage 08;
- hand off to Stage 09.

Block 15 is a non-operational documentary scenario catalog. It defines expected blocking and review behavior; it does not create evidence, approval, execution, confidence, promotion, capital allocation, or handoff capability.
