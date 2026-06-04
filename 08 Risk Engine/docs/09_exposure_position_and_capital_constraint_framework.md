# 08 Risk Engine — Block 09: Exposure, Position and Capital Constraint Framework

## Purpose

Block 09 defines the documentary framework for future exposure, position, and capital constraints inside Stage 08 Risk Engine.

This block exists to document how future constraints will be governed, versioned, audited, restricted, and blocked until sufficient empirical evidence and formal review exist.

Block 09 does not activate capital allocation. It does not calculate position sizing. It does not create productive risk budgets. It does not approve Paper Trading. It does not approve Live Trading. It does not enable execution, order generation, exchange connection, or operational downstream handling.

Under the current `framework_only` state, exposure, position, capital, drawdown, loss, concentration, cooldown, no-trade zone, and risk budget templates are documentary only.

## Constraint Framework Authority

Stage 08 / Block 09 may:

- define documentary exposure constraint templates;
- define documentary position constraint templates;
- define documentary capital constraint templates;
- define drawdown constraint categories;
- define loss limit categories;
- define concentration constraint categories;
- define asset cap categories;
- define cooldown categories;
- define no-trade zone categories;
- define risk budget template categories;
- declare capital allocation blocked under `framework_only`;
- declare productive position sizing blocked under `framework_only`;
- declare risk budget activation blocked under `framework_only`;
- require empirical evidence before activation;
- require Risk Engine review before activation;
- require human review before activation, if applicable.

Defining a constraint category or template does not activate it.

Registration, documentation, naming, versioning, or audit preparation of a constraint does not create trading permission, Paper Trading readiness, Live Trading readiness, execution permission, capital allocation, or productive position sizing.

## Non-Operational Constraint Rule

Block 09 is documentary-only under `framework_only`.

No exposure limit is active for trading.

No position size limit is active for trading.

No capital allocation is active.

No risk budget is active.

No drawdown engine is active.

No stop loss engine is active.

No portfolio optimizer is active.

No execution permission is created.

No Paper Trading readiness is created.

No Live Trading readiness is created.

No constraint can override Motor B `framework_only`.

No constraint can override `confidence_not_available`.

No constraint can override downstream blocking.

Documentary constraints may preserve blocking, harden future review requirements, or define future audit surfaces. They cannot approve anything.

## Current Framework-Only Constraint Baseline

The current constraint baseline is:

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
```

No exposure, position, or capital constraint may contradict this baseline.

If a constraint artifact attempts to relax this baseline, it must be rejected, blocked, degraded, or escalated to Risk Engine review according to severity.

## Exposure Constraint Categories

Documentary exposure constraint categories include:

- `max_total_exposure_template`;
- `max_asset_exposure_template`;
- `max_exchange_exposure_template`;
- `max_strategy_exposure_template`;
- `max_regime_exposure_template`;
- `max_event_exposure_template`;
- `max_correlation_exposure_template`;
- `max_volatility_adjusted_exposure_template`;
- `max_liquidity_adjusted_exposure_template`;
- `max_drawdown_adjusted_exposure_template`.

All exposure templates are `documentary_only`, `future_candidate`, or `blocked_under_framework_only` under the current state.

No exposure template is active. No exposure template can permit trading, Paper Trading, Live Trading, execution, capital allocation, productive position sizing, strategy promotion, or `handoff_to_09`.

## Position Constraint Categories

Documentary position constraint categories include:

- `max_position_size_template`;
- `max_position_notional_template`;
- `max_position_percentage_template`;
- `max_open_positions_template`;
- `max_symbol_position_template`;
- `max_strategy_position_template`;
- `max_event_sensitive_position_template`;
- `max_volatility_adjusted_position_template`;
- `max_liquidity_adjusted_position_template`;
- `position_scaling_rule_template`;
- `position_reduction_rule_template`.

Block 09 does not calculate productive position sizing.

Position constraint templates define future review surfaces only. They do not produce executable quantities, order sizes, notional allocations, scaling instructions, reduction automation, or portfolio adjustments.

## Capital Constraint Categories

Documentary capital constraint categories include:

- `total_capital_allocation_template`;
- `per_strategy_capital_cap_template`;
- `per_asset_capital_cap_template`;
- `per_exchange_capital_cap_template`;
- `capital_at_risk_template`;
- `capital_reserve_template`;
- `drawdown_based_capital_lock_template`;
- `event_based_capital_lock_template`;
- `emergency_capital_freeze_template`;
- `capital_allocation_prohibition_under_framework_only`.

Capital allocation remains blocked.

Capital templates are not allocation instructions. They do not authorize deployment, reserve usage, capital-at-risk activation, or per-strategy/per-asset/per-exchange capital assignment.

## Drawdown, Loss and Stop Condition Constraints

Documentary drawdown, loss, and stop condition categories include:

- `max_drawdown_template`;
- `daily_loss_limit_template`;
- `weekly_loss_limit_template`;
- `monthly_loss_limit_template`;
- `rolling_loss_limit_template`;
- `strategy_loss_limit_template`;
- `portfolio_loss_limit_template`;
- `stop_condition_template`;
- `emergency_stop_condition_reference`.

`stop_condition_template` is documentary only.

It does not implement a stop loss engine.

It does not implement Kill Switch.

Kill Switch authority belongs to Block 05 — Hard Veto Rules and Kill Switch Triggers.

Drawdown and loss constraints require empirical validation, audit trace, replayability, future governance, Risk Engine review, and human review if required before any activation can be considered.

## Concentration and Correlation Constraints

Documentary concentration and correlation constraint categories include:

- `max_asset_concentration_template`;
- `max_sector_or_theme_concentration_template`, if applicable;
- `max_exchange_concentration_template`;
- `max_strategy_concentration_template`;
- `max_correlation_cluster_template`;
- `correlation_breakdown_review_template`;
- `concentration_hardening_template`.

Block 09 does not activate a portfolio optimizer, concentration allocator, correlation engine, exposure engine, or allocation engine.

Concentration and correlation templates may define future blocking or review requirements, but they cannot approve trading or allocate capital.

## Liquidity, Volatility and Market Condition Constraints

Documentary liquidity, volatility, and market condition constraint categories include:

- `minimum_liquidity_requirement_template`;
- `maximum_spread_template`;
- `volatility_threshold_template`;
- `volatility_spike_hardening_template`;
- `market_dislocation_no_trade_zone_template`;
- `liquidity_freeze_template`;
- `degraded_market_condition_template`;
- `market_condition_hardening_template`.

Normal or favorable market conditions cannot approve anything.

Liquidity, volatility, and market condition constraints may harden handling, preserve blocks, or require review. They cannot create Paper Trading readiness, Live Trading readiness, execution permission, capital allocation, position sizing, confidence, or strategy promotion.

## Cooldown and No-Trade Zone Constraints

Documentary cooldown and no-trade zone categories include:

- `post_loss_cooldown_template`;
- `post_event_cooldown_template`;
- `post_kill_switch_cooldown_template`;
- `post_human_review_cooldown_template`;
- `event_no_trade_zone_template`;
- `critical_event_no_trade_zone_template`;
- `market_dislocation_no_trade_zone_template`;
- `audit_gap_no_trade_zone_template`;
- `missing_evidence_no_trade_zone_template`;
- `confidence_unavailable_no_trade_zone_template`.

No-trade zones preserve blocking and do not approve trading.

Cooldowns and no-trade zones may document conservative restrictions for future review. They do not implement automation, schedule trading pauses, route orders, allocate capital, activate Paper Trading, or execute a Kill Switch.

## Risk Budget Template Boundary

Documentary risk budget template categories include:

- `total_risk_budget_template`;
- `strategy_risk_budget_template`;
- `asset_risk_budget_template`;
- `event_risk_budget_template`;
- `regime_risk_budget_template`;
- `drawdown_risk_budget_template`;
- `volatility_risk_budget_template`;
- `liquidity_risk_budget_template`.

Under the current state:

```text
risk_budget_activation = blocked
```

Risk budgets are not active.

Risk budgets cannot allocate capital.

Risk budgets cannot enable position sizing.

Risk budgets cannot approve Paper Trading.

Risk budgets require future empirical evidence, governance, audit trace, Risk Engine review, and approval before any activation can be considered.

## Capital Allocation Prohibition Rule

Under `framework_only`:

```text
capital_allocation_eligibility = blocked
```

Capital allocation is prohibited.

Per-strategy allocation is prohibited.

Per-asset allocation is prohibited.

Per-exchange allocation is prohibited.

Capital-at-risk activation is prohibited.

Capital reserve deployment is prohibited.

Risk budget activation is prohibited.

Block 09 can document capital constraints, but it cannot allocate capital.

Any artifact that attempts to treat a capital template as an allocation instruction must be rejected, blocked, degraded, or escalated to Risk Engine review.

## Productive Position Sizing Prohibition Rule

Under `framework_only`:

```text
productive_position_sizing_eligibility = blocked
```

Position sizing calculation is prohibited.

Position scaling activation is prohibited.

Position reduction automation is prohibited.

Exposure-adjusted sizing is prohibited.

Volatility-adjusted sizing is prohibited.

Liquidity-adjusted sizing is prohibited.

Block 09 can document position constraints, but it cannot produce executable position sizes.

Any artifact that attempts to convert a position constraint into an executable order size, target weight, notional allocation, or scaling instruction must be rejected, blocked, degraded, or escalated to Risk Engine review.

## Constraint Applicability Rules

A constraint may only be considered applicable in the future if the relevant review path has:

- real backtesting results;
- OOS validation;
- walk-forward validation;
- robustness testing;
- empirical historical results;
- transaction cost assumptions;
- slippage assumptions;
- drawdown analysis;
- liquidity evidence;
- volatility evidence;
- risk policy compliance;
- audit trace;
- quality gate results;
- no blocking gaps;
- confidence availability, if required;
- Risk Engine review;
- human review, if required.

These conditions do not exist currently. Therefore, no constraint may be activated now.

Future applicability review must be versioned, auditable, replayable, and tied to the proper upstream evidence artifacts.

## Constraint Status Taxonomy

Allowed documentary constraint status values include:

- `constraint_documentary_only`;
- `constraint_future_candidate`;
- `constraint_blocked_under_framework_only`;
- `constraint_requires_empirical_evidence`;
- `constraint_requires_backtesting`;
- `constraint_requires_oos_validation`;
- `constraint_requires_walk_forward`;
- `constraint_requires_robustness`;
- `constraint_requires_audit_trace`;
- `constraint_requires_risk_engine_review`;
- `constraint_requires_human_review`;
- `constraint_not_active`;
- `constraint_rejected`;
- `constraint_deprecated`.

Under `framework_only`, the following status values are prohibited:

- `constraint_active`;
- `constraint_live`;
- `constraint_paper_trading_enabled`;
- `constraint_production_enabled`;
- `constraint_capital_allocation_enabled`;
- `constraint_position_sizing_enabled`.

No constraint status may be interpreted as operational approval under the current state.

## Constraint Output Record

Stage 08 may document a constraint record with fields such as:

- `constraint_record_id`;
- `constraint_id`;
- `constraint_name`;
- `constraint_category`;
- `constraint_version`;
- `constraint_status`;
- `current_applicability`;
- `activation_allowed_now`;
- `activation_blocked_reason`;
- `evidence_completeness_level`;
- `simulation_status`;
- `oos_validation_status`;
- `walk_forward_status`;
- `robustness_status`;
- `confidence_status`;
- `confidence_score`;
- `final_signal_confidence_score`;
- `paper_trading_eligibility`;
- `live_trading_status`;
- `execution_eligibility`;
- `order_generation_eligibility`;
- `exchange_connection_eligibility`;
- `capital_allocation_eligibility`;
- `productive_position_sizing_eligibility`;
- `risk_budget_activation`;
- `promotion_status`;
- `handoff_to_09`;
- `required_future_evidence`;
- `required_review`;
- `audit_trace_ref`;
- `source_document_ref`;
- `final_note_non_operational`.

This block does not create a database, storage layer, portfolio optimizer, allocation engine, productive exposure engine, or executable constraint engine. This structure is documentary only.

## Current Gate Conclusion

Under the current `framework_only` state:

```text
constraint_framework_status = non_operational
constraint_activation_status = blocked
exposure_limits_active = false
position_limits_active = false
capital_allocation_active = false
risk_budgets_active = false
portfolio_optimizer_active = false
allocation_engine_active = false
stop_loss_engine_active = false
drawdown_engine_active = false
paper_trading_eligibility = blocked
live_trading_status = blocked
execution_eligibility = blocked
order_generation_eligibility = blocked
exchange_connection_eligibility = blocked
capital_allocation_eligibility = blocked
productive_position_sizing_eligibility = blocked
risk_budget_activation = blocked
downstream_operational_eligibility = blocked
promotion_status = not_promoted
handoff_to_09 = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
```

Documentary constraints are not active constraints. They do not assign capital, calculate position sizing, activate risk budgets, approve Paper Trading, approve Live Trading, enable execution, or create downstream operational eligibility.

## Relationship With Block 04

Block 04 registers risk policy categories.

Block 09 develops the specific documentary framework for exposure, position, and capital constraints.

Both blocks are non-operational under `framework_only`. Block 04 policy categories and Block 09 constraint templates cannot activate trading, capital allocation, productive position sizing, risk budgets, Paper Trading, Live Trading, or execution.

## Relationship With Block 05

Block 05 defines hard veto and Kill Switch triggers.

Block 09 may document `emergency_capital_freeze_template`, `emergency_stop_condition_reference`, cooldown templates, and no-trade zone templates. It cannot implement Kill Switch.

Kill Switch remains an emergency authority. It is not a capital constraint, not position sizing, not a stop loss engine, and not a risk budget template.

## Relationship With Block 08

Block 08 handles event, regime, and market risk.

Block 09 may document event-sensitive exposure templates, event-based capital locks, event no-trade zones, regime risk budget templates, and market condition hardening templates.

Block 09 cannot use favorable events, stable regimes, or normal market conditions to approve anything.

Critical events, market dislocations, liquidity freezes, or audit gaps may be documented as reasons to preserve or harden blocking.

## Relationship With Block 11

Block 11 — Paper Trading Eligibility Gate will define Paper Trading eligibility conditions.

Block 09 cannot approve Paper Trading. It only documents constraints that would be required in a future eligibility review.

Under `framework_only`, Paper Trading remains blocked regardless of how complete a documentary constraint template appears.

## Relationship With Block 12

Block 12 — Risk Decision Engine will produce the formal `RiskDecision`.

Block 09 produces documentary constraint records, not the final `RiskDecision`.

A constraint record may become input to a later RiskDecision, but it must not be converted into trade execution, Paper Trading readiness, Live Trading readiness, capital allocation, strategy promotion, confidence assignment, or `handoff_to_09` approval.

## Explicit Non-Goals

This block does not:

- activate exposure limits;
- activate position limits;
- allocate capital;
- calculate productive position sizing;
- activate risk budgets;
- run portfolio optimization;
- create allocation engine;
- create execution engine;
- create stop loss engine;
- create drawdown engine;
- implement Kill Switch;
- approve Paper Trading;
- approve Live Trading;
- approve execution;
- approve strategy promotion;
- approve `handoff_to_09`;
- create `confidence_score`;
- create `final_signal_confidence_score`;
- create empirical evidence;
- run backtesting;
- run OOS validation;
- run walk-forward;
- run robustness;
- create Paper Trading eligibility gate;
- create RiskDecision final;
- create human override policy;
- create audit replay.
