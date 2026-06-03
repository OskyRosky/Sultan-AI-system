# 08 Risk Engine — Block 06: Missing Evidence and Blocking Gap Assessment

## Purpose

Block 06 defines the formal taxonomy for classifying missing evidence and blocking gaps inside Stage 08 Risk Engine.

This block identifies, classifies, and communicates evidence absences. It does not resolve them.

The function of this block is to prevent critical absences from being softened, inferred, hidden, relabeled, or converted into approval paths. Missing evidence remains explicit and blocking when downstream eligibility depends on it.

## Assessment Authority

Stage 08 may classify:

- evidence missing;
- evidence incomplete;
- evidence unauditable;
- evidence insufficient;
- robustness missing;
- OOS missing;
- backtest missing;
- walk-forward missing;
- source missing;
- audit missing;
- confidence evidence missing;
- policy evidence missing;
- event evidence missing;
- human review evidence missing;
- blocking gaps.

Classifying a gap does not resolve it. Classification provides an audit-visible state for later review, veto, sufficiency assessment, and RiskDecision handling.

## Current Framework-Only Evidence Baseline

The current evidence baseline is:

```text
evidence_completeness_level = framework_only
simulation_status = backtest_not_implemented
oos_validation_status = oos_not_available
robustness_status = robustness_not_available
empirical_historical_results_status = not_available
productive_backtesting_engine_status = not_implemented
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
handoff_to_09 = blocked
live_trading_status = blocked
execution_eligibility = blocked
capital_allocation_eligibility = blocked
productive_position_sizing_eligibility = blocked
risk_budget_activation = blocked
promotion_status = not_promoted
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

This baseline produces missing evidence and blocking gaps by default under the current state.

No downstream eligibility field may be upgraded while this baseline remains unresolved.

## Missing Evidence Taxonomy

Missing evidence categories include:

- `evidence_missing`;
- `evidence_incomplete`;
- `evidence_unauditable`;
- `evidence_insufficient`;
- `empirical_evidence_missing`;
- `backtest_missing`;
- `oos_validation_missing`;
- `walk_forward_missing`;
- `robustness_missing`;
- `sensitivity_testing_missing`;
- `transaction_cost_assumption_missing`;
- `slippage_assumption_missing`;
- `drawdown_analysis_missing`;
- `historical_results_missing`;
- `reproducibility_metadata_missing`;
- `data_version_ref_missing`;
- `feature_version_ref_missing`;
- `strategy_version_ref_missing`;
- `risk_policy_compliance_evidence_missing`;
- `audit_trace_missing`;
- `quality_gate_missing`;
- `confidence_evidence_missing`;
- `event_risk_evidence_missing`;
- `human_review_evidence_missing`;
- `source_artifact_missing`.

These categories may coexist. A single artifact or handoff can contain multiple missing evidence flags.

## Blocking Gap Taxonomy

Blocking gap categories include:

- `blocking_gap_framework_only`;
- `blocking_gap_backtest_missing`;
- `blocking_gap_oos_missing`;
- `blocking_gap_walk_forward_missing`;
- `blocking_gap_robustness_missing`;
- `blocking_gap_confidence_unavailable`;
- `blocking_gap_audit_trace_missing`;
- `blocking_gap_source_conflict`;
- `blocking_gap_contract_violation`;
- `blocking_gap_forbidden_downstream_usage_missing`;
- `blocking_gap_non_approval_statement_missing`;
- `blocking_gap_event_critical`;
- `blocking_gap_policy_not_active`;
- `blocking_gap_policy_evidence_missing`;
- `blocking_gap_handoff_to_09_blocked`;
- `blocking_gap_paper_trading_blocked`;
- `blocking_gap_live_trading_blocked`;
- `blocking_gap_execution_blocked`;
- `blocking_gap_capital_allocation_blocked`;
- `blocking_gap_promotion_blocked`.

Blocking gaps prevent downstream eligibility. They cannot be converted into conditional approval without formal evidence and later Stage 08 review.

## Severity Classification

Missing evidence and blocking gaps may use these severity levels:

- `severity_info_documentary_gap`;
- `severity_low_incomplete_metadata`;
- `severity_medium_review_required`;
- `severity_high_downstream_blocking`;
- `severity_critical_veto_or_kill_switch_candidate`.

Low or medium severity does not mean approval. It only indicates priority and review route.

Under `framework_only`, multiple gaps are at least `severity_high_downstream_blocking`, including missing backtesting, missing OOS validation, missing walk-forward validation, missing robustness, unavailable confidence, Paper Trading blocked, Live Trading blocked, execution blocked, capital allocation blocked, promotion blocked, and `handoff_to_09` blocked.

## Evidence Status Definitions

The assessment layer uses these definitions:

- `missing`: required evidence does not exist or was not produced;
- `incomplete`: evidence exists partially but does not cover minimum requirements;
- `unauditable`: evidence exists but cannot be traced, versioned, or reproduced;
- `insufficient`: evidence exists but does not meet quality, coverage, robustness, OOS, stability, sample, regime, or traceability requirements;
- `unavailable`: an expected artifact is not available;
- `blocked`: the gap prevents downstream eligibility;
- `future_required`: evidence is required for a possible future review.

This prepares the distinction that Block 12 will later formalize between:

- `blocked_missing_evidence`;
- `requires_more_evidence`.

Block 06 does not develop the full Block 12 RiskDecision semantics.

## Current Missing Evidence Assessment

Under the current `framework_only` state:

- real backtesting results are missing;
- OOS validation is missing;
- walk-forward validation is missing;
- robustness testing is missing;
- empirical historical results are missing;
- productive backtesting engine is not implemented;
- confidence evidence is missing;
- `confidence_score` is `null`;
- `final_signal_confidence_score` is `null`;
- Paper Trading eligibility evidence is missing;
- Live Trading eligibility evidence is missing;
- capital allocation evidence is missing;
- promotion evidence is missing;
- `handoff_to_09` remains blocked.

This produces downstream blocking. It does not produce a partial approval path.

## Required Evidence Map

Future downstream eligibility review would require evidence such as:

- Paper Trading eligibility: real backtesting, OOS validation, walk-forward validation, robustness testing, audit trace, reproducibility metadata, risk policy compliance, quality gates, human review if required, and Risk Engine review.
- Live Trading eligibility: all Paper Trading evidence plus stronger operational evidence, live-readiness controls, exchange/venue governance, audited escalation controls, and later-stage review.
- execution eligibility: empirical evidence, execution admissibility, audit trace, venue governance, operational controls, human review if required, and Risk Engine review.
- capital allocation eligibility: empirical evidence, risk policy compliance, drawdown analysis, exposure constraints, capital governance, audit trace, human review if required, and Risk Engine review.
- productive position sizing eligibility: empirical evidence, versioned strategy references, risk policy compliance, exposure/position framework evidence, audit trace, and Risk Engine review.
- strategy promotion eligibility: empirical evidence, strategy version references, quality gates, robustness, OOS validation, walk-forward validation, no blocking gaps, human review if required, and Risk Engine review.
- confidence availability: empirical evidence, confidence contract, audit trace, sufficient validation quality, and later confidence sufficiency review.
- `handoff_to_09` eligibility: all relevant upstream evidence, no blocking gaps, Paper Trading eligibility review, audit trace, quality gates, and Risk Engine review.

This map approves nothing currently. It only describes future evidence expectations.

## Non-Substitution Rule

Missing evidence cannot be substituted by:

- documentation completeness;
- Stage 04 in-memory modules;
- Stage 05 `StrategyDossier`;
- Stage 05 mock examples;
- Stage 07 fused candidates;
- Stage 07 LLM outputs;
- Bull/Bear agreement;
- Motor A research context;
- Motor C event context;
- regime analysis;
- technical indicators;
- feature availability;
- policy registry entries;
- hard veto not triggered;
- Kill Switch not required;
- synthetic tests;
- mock scenarios;
- human review metadata;
- human optimism;
- favorable market events.

These elements may provide context, structure, or review surfaces. They are not sufficient empirical evidence.

## Gap Resolution Requirements

Future gap resolution would require artifacts such as:

- production-quality or review-quality backtesting artifact;
- versioned data;
- versioned features;
- versioned strategy;
- reproducible run configuration;
- audit trace;
- OOS validation;
- walk-forward validation;
- robustness testing;
- transaction cost assumptions;
- slippage assumptions;
- risk policy compliance;
- quality gate result;
- source artifact references;
- human review if required;
- Risk Engine review.

Block 06 does not produce these artifacts. It only records that they are missing, incomplete, unauditable, insufficient, unavailable, blocked, or future-required.

## Gap Assessment Outcome Taxonomy

Gap assessment outcomes include:

- `gap_assessment_framework_only_blocked`;
- `gap_assessment_missing_evidence_detected`;
- `gap_assessment_incomplete_evidence_detected`;
- `gap_assessment_unauditable_evidence_detected`;
- `gap_assessment_insufficient_evidence_detected`;
- `gap_assessment_blocking_gaps_present`;
- `gap_assessment_requires_more_evidence_future_only`;
- `gap_assessment_requires_human_review`;
- `gap_assessment_requires_risk_engine_review`;
- `gap_assessment_hard_veto_candidate`;
- `gap_assessment_kill_switch_candidate`;
- `gap_assessment_no_downstream_eligibility`.

These outcomes are not the final `RiskDecision` of Block 12.

No gap assessment outcome may approve Paper Trading, Live Trading, execution, capital allocation, promotion, confidence assignment, or `handoff_to_09`.

## Missing Evidence Assessment Record

Stage 08 may document a missing evidence assessment with fields such as:

- `assessment_id`;
- `assessed_at`;
- `source_artifact_id`;
- `source_stage`;
- `source_block`;
- `source_document_ref`;
- `evidence_completeness_level`;
- `missing_evidence_flags`;
- `incomplete_evidence_flags`;
- `unauditable_evidence_flags`;
- `insufficient_evidence_flags`;
- `unavailable_artifacts`;
- `blocking_gap_flags`;
- `severity_level`;
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
- `required_future_evidence`;
- `required_review`;
- `audit_trace_ref`;
- `final_note_non_operational`.

This block does not create a database, storage layer, executable gap resolver, or production assessment engine. The record is documentary only.

## Relationship With Block 03

Block 03 identifies the Motor B state as `framework_only` and blocking.

Block 06 expands and formally classifies the evidence absences and blocking gaps derived from that state.

Block 06 does not modify, weaken, or soften the Motor B Evidence and Eligibility Gate.

## Relationship With Block 05

Block 05 defines hard veto and Kill Switch triggers.

Block 06 may identify gaps that are candidates for hard veto or Kill Switch review. It does not execute Kill Switch and does not produce the final `RiskDecision`.

## Relationship With Block 07

Block 07 — Confidence and Evidence Sufficiency Gate will evaluate whether sufficient evidence and confidence exist.

Block 06 provides missing evidence taxonomies and assessment outputs so Block 07 can preserve `confidence_not_available` and block insufficient confidence.

## Relationship With Block 12

Block 12 — Risk Decision Engine will formally distinguish between:

- `blocked_missing_evidence`;
- `requires_more_evidence`.

Block 06 prepares that distinction by classifying evidence status and blocking gaps, but it does not produce the final `RiskDecision`.

## Explicit Non-Goals

This block does not do:

- resolve gaps;
- create evidence;
- infer missing evidence;
- approve Paper Trading;
- approve Live Trading;
- approve execution;
- approve capital allocation;
- approve strategy promotion;
- create `confidence_score`;
- create `final_signal_confidence_score`;
- run backtesting;
- run OOS validation;
- run walk-forward;
- run robustness;
- create empirical historical results;
- create productive backtesting engine;
- create policy enforcement;
- execute Kill Switch;
- produce final `RiskDecision`;
- create Paper Trading eligibility gate;
- create human override policy;
- create audit replay.

Block 06 is a non-operational assessment taxonomy. It classifies missing evidence and blocking gaps while preserving downstream blocking under `framework_only`.
