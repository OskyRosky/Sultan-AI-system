# 08 Risk Engine — Block 04: Risk Policy Registry

## Purpose

Block 04 defines the documentary registry of risk policies permitted by Stage 08 Risk Engine.

The Risk Policy Registry exists to catalog, version, audit, and control future applicability of risk policies. It provides a governed reference surface for policy categories, policy metadata, policy status, applicability constraints, versioning requirements, audit requirements, and downstream usage restrictions.

This block does not activate production policies. It does not allocate capital. It does not calculate position sizing. It does not approve Paper Trading. It does not permit Live Trading. It does not generate signals, orders, execution instructions, or operational recommendations.

## Registry Authority

The Risk Policy Registry may:

- define allowed risk policy categories;
- define policy metadata requirements;
- define policy status;
- define policy applicability;
- define policy versioning;
- define policy audit requirements;
- mark policies as `documentary_only`;
- mark policies as `future_candidate`;
- mark policies as `blocked_under_framework_only`;
- require evidence before activation;
- require Risk Engine review before activation;
- require human review before activation, if applicable.

Registering a policy does not activate it. Registration creates an auditable documentary entry only.

## Non-Operational Registry Rule

The registry is documentary-only under the current `framework_only` state.

No registered policy is active for production trading.

No registered policy enables Paper Trading.

No registered policy enables Live Trading.

No registered policy enables execution.

No registered policy enables capital allocation.

No registered policy enables productive position sizing.

No registered policy creates confidence.

No registered policy overrides Motor B evidence gates.

No registered policy overrides downstream blocking.

Under `framework_only`, every policy must remain `documentary_only`, `future_candidate`, or `blocked_under_framework_only`.

## Current Framework-Only Policy State

All registered policies must inherit the current blocking state:

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
capital_allocation_eligibility = blocked
productive_position_sizing_eligibility = blocked
risk_budget_activation = blocked
promotion_status = not_promoted
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

No policy may contradict these values. Any policy that attempts to relax them must be rejected, blocked, or escalated to Risk Engine review.

## Allowed Risk Policy Categories

The registry may document the following risk policy categories:

- `exposure_policy`;
- `position_size_policy`;
- `concentration_policy`;
- `drawdown_policy`;
- `volatility_policy`;
- `liquidity_policy`;
- `event_risk_policy`;
- `regime_risk_policy`;
- `market_risk_policy`;
- `asset_restriction_policy`;
- `exchange_risk_policy`;
- `cooldown_policy`;
- `stop_condition_policy`;
- `loss_limit_policy`;
- `operational_blocking_policy`;
- `evidence_requirement_policy`;
- `confidence_requirement_policy`;
- `audit_requirement_policy`;
- `human_review_policy`;
- `risk_engine_review_policy`.

These categories are documentary and future-facing. They are not active production policies under the current state.

## Policy Status Taxonomy

Allowed policy status values include:

- `policy_documentary_only`;
- `policy_future_candidate`;
- `policy_blocked_under_framework_only`;
- `policy_requires_empirical_evidence`;
- `policy_requires_backtesting`;
- `policy_requires_oos_validation`;
- `policy_requires_walk_forward`;
- `policy_requires_robustness`;
- `policy_requires_audit_trace`;
- `policy_requires_human_review`;
- `policy_requires_risk_engine_review`;
- `policy_not_active`;
- `policy_deprecated`;
- `policy_rejected`.

Under `framework_only`, the following status values are prohibited:

- `policy_active`;
- `policy_live`;
- `policy_production_enabled`;
- `policy_paper_trading_enabled`.

No status value may be interpreted as operational approval unless later blocks define and approve that interpretation with empirical evidence and audit controls. Under the current state, no such approval exists.

## Policy Applicability Rules

A policy may only be considered applicable in the future if the relevant review path has:

- validated empirical evidence;
- real backtesting results;
- OOS validation;
- walk-forward validation;
- robustness testing;
- risk policy compliance evidence;
- versioned policy definition;
- versioned strategy reference;
- versioned data reference;
- audit trace;
- quality gate result;
- no blocking gaps;
- confidence availability, if required by downstream gates;
- human review, if required;
- Risk Engine review.

These conditions do not exist currently. Therefore, no policy may be activated now.

Future applicability review must preserve source references, version references, audit traceability, and downstream restrictions.

## Policy Versioning Requirements

Each policy entry should define:

- `policy_id`;
- `policy_name`;
- `policy_category`;
- `policy_version`;
- `policy_status`;
- `created_at` or `declared_as_of`;
- `owner_or_responsible_stage`;
- `source_stage`;
- `source_block`;
- `source_document_ref`;
- `applicable_scope`;
- `evidence_requirements`;
- `activation_requirements`;
- `blocking_conditions`;
- `downstream_usage_restrictions`;
- `audit_trace_ref`;
- `supersedes_policy_id`, if applicable;
- `deprecated_by_policy_id`, if applicable.

This block does not create a database, storage layer, executable registry, or production policy store.

## Policy Applicability Matrix

The registry may use a documentary applicability matrix with the following columns:

- `category`;
- `current_status`;
- `current_applicability`;
- `activation_allowed_now`;
- `reason_blocked`;
- `required_future_evidence`;
- `required_review`;
- `downstream_usage_allowed`.

Under the current state, `activation_allowed_now` must be `false` for every category.

The matrix is documentary only. It is not an executable policy engine, enforcement layer, capital allocator, position sizing module, or RiskDecision generator.

## Exposure and Position Policy Boundary

Exposure and position size policies may be registered documentarily, but they cannot be activated under `framework_only`.

The registry must preserve:

- max exposure templates are not activated in this block;
- max position templates are not activated in this block;
- risk budget templates are not activated in this block;
- capital allocation remains blocked;
- productive position sizing remains blocked.

The detailed exposure, position, and capital framework belongs to Block 09 — Exposure, Position and Capital Constraint Framework.

## Drawdown, Volatility and Loss Policy Boundary

Drawdown, volatility, and loss limit policies may be registered documentarily.

They must not be used to enable trading, Paper Trading, Live Trading, execution, capital allocation, productive position sizing, or strategy promotion.

These policies require future empirical evidence, auditable simulations, and Risk Engine review before any activation can be considered.

`stop_condition_policy` documents future risk conditions only. It does not implement a Kill Switch, does not implement productive stop loss logic, and does not activate any operational interruption mechanism. The Kill Switch as emergency authority and its formal triggers are defined in Block 05 and are distinct from any `stop_condition_policy` registered in Block 04.

## Liquidity, Asset and Exchange Risk Policy Boundary

Liquidity policies, asset restriction policies, and exchange risk policies may be registered documentarily.

This block does not:

- connect any exchange;
- approve any venue;
- approve any productive asset universe;
- enable execution;
- enable Paper Trading.

Any future exchange, asset, or liquidity policy activation requires evidence, audit trace, and later-stage review.

## Event, Regime and Market Risk Policy Boundary

Event risk, regime risk, and market risk policies may be registered documentarily.

Block 04 does not consume or redefine event precedence.

Block 04 does not relax critical events.

Block 04 does not convert favorable events into approval.

Block 08 — Event, Regime and Market Risk Gate will develop event, regime, and market risk gate logic later.

Event asymmetry must be preserved:

- favorable events unlock nothing;
- negative or critical events may block, degrade, suspend, or escalate.

## Evidence and Confidence Policy Boundary

Evidence and confidence policies may be registered, but they cannot create evidence or confidence.

The policy registry cannot create `confidence_score`.

The policy registry cannot create `final_signal_confidence_score`.

The policy registry cannot infer confidence from LLM output.

The policy registry cannot infer confidence from Bull/Bear agreement.

The policy registry cannot infer confidence from fusion alignment.

The policy registry cannot substitute Motor B evidence.

Evidence and confidence policy entries must preserve `confidence_status = confidence_not_available`, `confidence_score = null`, and `final_signal_confidence_score = null` under the current state.

## Operational Blocking Policy Boundary

Operational blocking policies may be registered documentarily to preserve blocks on:

- Paper Trading;
- Live Trading;
- execution;
- order generation;
- exchange connection;
- capital allocation;
- productive position sizing;
- strategy promotion;
- `handoff_to_09`.

This block registers blocking policy categories and metadata only. It does not generate the final `RiskDecision`; formal `RiskDecision` belongs to Block 12.

## Policy Registry Record

Each policy registry record may include:

- `policy_record_id`;
- `policy_id`;
- `policy_name`;
- `policy_category`;
- `policy_version`;
- `policy_status`;
- `current_applicability`;
- `activation_allowed_now`;
- `activation_blocked_reason`;
- `evidence_completeness_required`;
- `current_evidence_completeness`;
- `required_backtesting_status`;
- `current_simulation_status`;
- `required_oos_status`;
- `current_oos_validation_status`;
- `required_robustness_status`;
- `current_robustness_status`;
- `downstream_usage_restrictions`;
- `paper_trading_impact`;
- `live_trading_impact`;
- `execution_impact`;
- `capital_allocation_impact`;
- `promotion_impact`;
- `confidence_impact`;
- `audit_trace_ref`;
- `source_document_ref`;
- `required_next_review`;
- `final_note_non_operational`.

This is a documentary structure only. Block 04 does not create a database, storage layer, active policy engine, or production policy registry.

## Relationship With Blocks 00–03

Block 04 inherits:

- authority and veto mandate from Block 00;
- intake restrictions from Block 01;
- `RiskHandoffPackage` validation constraints from Block 02;
- Motor B `framework_only` evidence gate from Block 03.

Block 04 cannot contradict Blocks 00-03. If a policy entry conflicts with those blocks, the stricter blocking interpretation wins.

## Relationship With Block 05

Block 05 — Hard Veto Rules and Kill Switch Triggers will develop absolute veto rules and Kill Switch triggers.

Block 04 may register `operational_blocking_policy` categories, but it must not develop the complete hard veto taxonomy or Kill Switch trigger taxonomy.

## Relationship With Block 09

Block 09 — Exposure, Position and Capital Constraint Framework will develop exposure, position, and capital constraints in more detail.

Block 04 only registers policy categories and metadata. It does not create productive exposure templates, capital allocation, risk budget activation, or productive position sizing.

## Relationship With Block 12

Block 12 — Risk Decision Engine will produce the formal `RiskDecision`.

Block 04 does not produce a final `RiskDecision`. A policy status is not a final risk decision.

## Explicit Non-Goals

This block does not do:

- activate policies;
- production risk enforcement;
- trading;
- Paper Trading;
- Live Trading;
- execution;
- order generation;
- exchange connection;
- capital allocation;
- productive position sizing;
- risk budget activation;
- strategy promotion;
- confidence scoring;
- `final_signal_confidence_score`;
- empirical evidence creation;
- backtesting;
- OOS validation;
- walk-forward;
- robustness testing;
- complete hard veto taxonomy;
- kill switch trigger taxonomy;
- event precedence logic;
- productive exposure templates;
- final `RiskDecision`;
- human override policy;
- audit replay.

Block 04 is a non-operational policy registry document. It catalogs future risk policy surfaces while preserving all current downstream blocks under `framework_only`.
