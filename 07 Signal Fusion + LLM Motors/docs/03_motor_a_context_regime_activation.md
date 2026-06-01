# 07 Signal Fusion + LLM Motors - Motor A Context Layer and Regime Strategy Activation Rules

## 1. Purpose

Block 03 defines the Motor A Context Layer for `07 Signal Fusion + LLM Motors`.

Motor A provides market, macro, liquidity, volatility, and regime context for later 07 blocks.

Motor A may define context labels, regime metadata, deterministic base motor weights, and `regime_strategy_activation_rules` for contextual routing and weighting inside 07.

Motor A does not approve trades.

Motor A does not approve strategies.

Motor A does not authorize Paper Trading, Live Trading, execution, capital allocation, or downstream operational eligibility.

Regime context is market context, not trading evidence.

Activation means contextual routing or weighting inside 07, not trade approval.

activation is not trade approval.

This block is documentary and contractual only. It does not implement Python code, trading logic, Signal Candidate Normalization, Signal Fusion, Motor C classification, Confidence Aggregation, Risk Handoff, Paper Trading, Live Trading, execution, or capital allocation.

## 2. Scope

This block covers:

- Motor A purpose and boundaries;
- Motor A input contract;
- Motor A output contract;
- context labels;
- regime metadata;
- regime-to-context mapping;
- `regime_strategy_activation_rules`;
- conceptual base motor weights;
- regime-adjusted permissions;
- Motor B `framework_only` protection rules;
- Motor A and Motor C independence;
- event modulation hook for later Block 08;
- missing or stale regime context handling;
- confidence and uncertainty handling;
- audit and traceability requirements;
- relationship with 07-Block-06 Signal Candidate Normalization;
- relationship with `08 Risk Engine`.

This block does not cover:

- executable Motor A implementation;
- Motor C Event Classifier;
- LLM prompting rules;
- Signal Candidate Normalization;
- Bull/Bear Debate;
- Deterministic Signal Fusion;
- Confidence Aggregation;
- Risk Handoff;
- Paper Trading;
- Live Trading;
- execution logic;
- capital allocation;
- strategy approval;
- trade approval.

## 3. Non-Authority Reminder

Motor A is non-authoritative.

Motor A has no authority to:

- approve trades;
- approve strategies;
- promote strategies;
- authorize Paper Trading;
- authorize Live Trading;
- create execution readiness;
- allocate capital;
- relax risk limits;
- override `08 Risk Engine`;
- change Motor B state;
- relax Motor B restrictions;
- compensate for missing Motor B evidence;
- fill `confidence_score`;
- convert regime context into empirical evidence;
- replace backtesting, OOS validation, walk-forward validation, robustness review, or historical performance evidence.

Any accepted Motor A context remains context only.

Any activation rule in this document means contextual support, degradation, blocking, or routing inside 07. It does not mean trade approval, strategy promotion, Paper Trading approval, Live Trading approval, execution readiness, or capital allocation readiness.

## 4. Definition Of Motor A

Motor A is the market and regime context motor within 07.

Motor A can consume regime context originating from `04 Research Layer` / Regime Detection v1 when that context is traceable, scoped, versioned, and limitation-aware.

Motor A may represent:

- trend context;
- volatility context;
- liquidity context;
- macro or risk environment context;
- uncertainty state;
- stale or unavailable regime state;
- contextual compatibility between market regime and strategy families.

Motor A is not:

- a backtesting engine;
- a strategy approval engine;
- a trading engine;
- a Risk Engine;
- an ML ensemble;
- a replacement for Motor B evidence;
- a replacement for Motor C event classification;
- a source of historical validation.

## 5. Relationship With Block 00, Block 01, And Block 02

Block 00 established that 07 is a governed bridge between `06 Backtesting Engine` and `08 Risk Engine`, and that 07 produces no trade approval.

Block 01 established that regime context is an accepted input family only when it is traceable, timestamped, versioned, scoped, limitation-aware, and non-authoritative.

Block 02 established that Motor B currently enters 07 through the Motor B Adapter with:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

Block 03 must preserve those constraints.

Motor A cannot modify, reinterpret, relax, compensate for, or override Motor B adapter status, Motor B evidence state, Motor B confidence state, Motor B non-approval status, or Motor B forbidden downstream usage.

The combination of Motor A context and degraded Motor B input must not be interpreted as convergent empirical evidence.

The sum of degraded inputs does not create downstream operational eligibility.

## 6. Relationship With 04 Research Layer / Regime Detection v1

Motor A may consume regime context from `04 Research Layer` / Regime Detection v1 when available.

The consumed regime context must carry:

- source reference;
- method version;
- timestamp;
- supported assets;
- supported timeframes;
- limitations;
- uncertainty state;
- missing context markers where applicable.

Regime context from 04 remains upstream context. It does not become trading evidence merely because 07 consumes it.

If 04 context is synthetic, stale, framework-only, unsupported, partial, or unavailable, Motor A must preserve that limitation and classify its own output as degraded or unavailable.

## 7. Core Context Principle

Regime context is market context, not trading evidence.

Regime context may help later 07 blocks route, weight, degrade, or block candidate inputs for review.

Regime context must not be used to:

- claim strategy edge;
- claim historical validation;
- claim robustness;
- claim OOS validity;
- fill missing backtest evidence;
- upgrade Motor B evidence completeness;
- approve a signal;
- approve Paper Trading;
- approve Live Trading;
- authorize execution.

## 8. Activation Meaning

`regime_strategy_activation_rules` define contextual compatibility between a regime and strategy family.

Activation means contextual routing or weighting inside 07, not trade approval.

Allowed activation outcomes are:

```text
contextually_supported
contextually_degraded
contextually_blocked
requires_additional_confirmation
unavailable_due_to_missing_context
```

These outcomes are deterministic review states. They are not empirical validation, Paper Trading eligibility, Live Trading eligibility, execution permission, capital allocation permission, or strategy promotion.

## 9. Motor A Input Contract

The conceptual Motor A input schema is:

```text
MotorAInput
  motor_a_input_id
  regime_label
  regime_source
  regime_timestamp
  regime_method_version
  supported_assets
  supported_timeframes
  macro_context_label
  liquidity_context_label
  volatility_context_label
  risk_environment_label
  uncertainty_level
  source_references
  limitations
  missing_context
  stale_context_flag
  schema_version
```

### Field Meaning

- `motor_a_input_id`: stable identifier for the input context record.
- `regime_label`: regime classification, using the taxonomy in this document.
- `regime_source`: source owner or upstream artifact, such as `04 Research Layer` / Regime Detection v1.
- `regime_timestamp`: timestamp of the regime observation or classification.
- `regime_method_version`: method or schema version for regime production.
- `supported_assets`: assets covered by the regime context.
- `supported_timeframes`: timeframes covered by the regime context.
- `macro_context_label`: macro context label when available.
- `liquidity_context_label`: liquidity context label when available.
- `volatility_context_label`: volatility context label when available.
- `risk_environment_label`: risk environment label when available.
- `uncertainty_level`: explicit uncertainty level.
- `source_references`: auditable source references.
- `limitations`: known limitations and allowed usage restrictions.
- `missing_context`: missing context fields or unavailable context areas.
- `stale_context_flag`: explicit flag for stale or time-inadmissible context.
- `schema_version`: Motor A input schema version.

Missing required fields must produce degraded or unavailable output. Inputs that claim trading authority, strategy approval, Paper Trading eligibility, risk override, or empirical validation must be rejected.

## 10. Motor A Output Contract

The conceptual Motor A output schema is:

```text
MotorAContextOutput
  motor_a_context_id
  context_label
  regime_label
  regime_metadata
  base_motor_weights
  regime_strategy_activation_rules
  regime_adjusted_permissions
  event_modulation_allowed
  event_modulation_hook
  motor_b_constraints_observed
  downstream_operational_eligibility
  confidence_status
  confidence_score
  uncertainty_level
  limitations
  forbidden_downstream_usage
  audit_references
  created_at
  schema_version
```

### Field Meaning

- `motor_a_context_id`: stable identifier for the Motor A output.
- `context_label`: normalized context label derived from `regime_label` and metadata.
- `regime_label`: preserved input regime classification.
- `regime_metadata`: timestamp, source, method version, asset scope, timeframe scope, uncertainty, and stale markers.
- `base_motor_weights`: deterministic conceptual weights for Motor A, Motor B, and Motor C.
- `regime_strategy_activation_rules`: deterministic contextual compatibility rules by strategy family.
- `regime_adjusted_permissions`: context-level review permissions, degradations, and blocks.
- `event_modulation_allowed`: boolean or explicit status indicating whether later event modulation may adjust weights.
- `event_modulation_hook`: conceptual handoff interface for later Block 08.
- `motor_b_constraints_observed`: explicit statement that Motor B restrictions are preserved.
- `downstream_operational_eligibility`: must be `blocked` under current Motor B `framework_only` conditions.
- `confidence_status`: Motor A context confidence status, never Motor B confidence.
- `confidence_score`: null unless a later governed Motor A confidence policy defines a valid value; it must never fill Motor B confidence.
- `uncertainty_level`: preserved or derived uncertainty classification.
- `limitations`: Motor A limitations and source limitations.
- `forbidden_downstream_usage`: explicit downstream bans inherited from 07 and Motor B constraints.
- `audit_references`: source references plus Block 03 reference.
- `created_at`: output creation timestamp.
- `schema_version`: Motor A output schema version.

## 11. Context Labels

Initial conceptual `context_label` values are:

```text
favorable_trend_context
defensive_trend_context
non_trending_context
unstable_volatility_context
low_activity_context
defensive_risk_context
event_sensitive_context
liquidity_stress_context
context_unavailable_or_uncertain
```

Context labels are deterministic classifications for later review and weighting only.

Context labels must not be interpreted as trading signals.

## 12. Regime Labels

Initial conceptual `regime_label` values are:

```text
trend_bullish
trend_bearish
chop_range
high_volatility
low_volatility
risk_off
event_driven
liquidity_stress
unknown_or_unclassified
```

Any unrecognized label must be mapped to `unknown_or_unclassified` or rejected, depending on schema version and source validity.

## 13. Regime Metadata

Motor A output must preserve regime metadata:

- source stage or source artifact;
- source method version;
- regime timestamp;
- creation timestamp;
- supported assets;
- supported timeframes;
- input freshness or staleness;
- source limitations;
- missing context fields;
- uncertainty level;
- audit references;
- schema version.

Motor A must not hide stale, missing, synthetic, unsupported, or partial context.

## 14. Regime-To-Context Mapping

| Regime label | Context label | Limitations |
| --- | --- | --- |
| `trend_bullish` | `favorable_trend_context` | Contextually favorable to trend or momentum review only; no trade approval. |
| `trend_bearish` | `defensive_trend_context` | May support defensive or short-bias review where allowed; no trade approval. |
| `chop_range` | `non_trending_context` | Trend-following assumptions may be degraded; range compatibility remains contextual only. |
| `high_volatility` | `unstable_volatility_context` | Technical exposure may be degraded; event-aware review may receive priority later. |
| `low_volatility` | `low_activity_context` | Breakout or momentum assumptions may require additional confirmation. |
| `risk_off` | `defensive_risk_context` | Technical signals may require additional confirmation or contextual blocking. |
| `event_driven` | `event_sensitive_context` | Later Motor C event review may receive higher priority; Motor C is not implemented here. |
| `liquidity_stress` | `liquidity_stress_context` | Liquidity-sensitive strategies may be blocked or require additional confirmation. |
| `unknown_or_unclassified` | `context_unavailable_or_uncertain` | Context cannot support activation; output must be degraded or unavailable. |

## 15. Regime Strategy Activation Rules

Activation outcomes are contextual only.

### trend_bullish

- Trend or momentum strategy families may be `contextually_supported`.
- Mean-reversion strategy families may be `requires_additional_confirmation`.
- Short-bias strategy families may be `contextually_degraded` unless separately supported by Motor B and later review.
- This does not approve trading.

### trend_bearish

- Defensive, hedge, or short-bias strategy families may be `contextually_supported` where the strategy family is permitted by upstream contracts.
- Long-only momentum strategy families may be `contextually_degraded` or `requires_additional_confirmation`.
- This does not approve trading.

### chop_range

- Trend-following strategy families may be `contextually_degraded` or `contextually_blocked`.
- Range-compatible or mean-reversion strategy families may be `contextually_supported`.
- Breakout strategy families may be `requires_additional_confirmation`.
- This does not approve trading.

### high_volatility

- Technical exposure may be `contextually_degraded`.
- High-leverage, tight-stop, or liquidity-sensitive strategy families may be `contextually_blocked`.
- Event-aware review may receive higher priority later.
- This does not approve trading.

### low_volatility

- Breakout and momentum strategy families may be `requires_additional_confirmation`.
- Mean-reversion strategy families may be `contextually_supported` only as context, not evidence.
- This does not approve trading.

### risk_off

- Technical signals may be `requires_additional_confirmation` or `contextually_blocked`.
- Risk-increasing strategy families must not receive relaxed permissions.
- No relaxation of Motor B restrictions is allowed.
- This does not approve trading.

### event_driven

- Event-sensitive review may receive higher priority later in Block 08.
- Motor C event classification may receive higher priority later in Block 08.
- Motor A must not implement Motor C here.
- This does not approve trading.

### liquidity_stress

- Liquidity-sensitive strategy families may be `contextually_blocked`.
- Execution-sensitive or spread-sensitive assumptions must be marked as limited.
- This does not approve trading.

### unknown_or_unclassified

- All strategy families must be `unavailable_due_to_missing_context` or `requires_additional_confirmation`.
- Motor A output must be degraded or unavailable.
- This does not approve trading.

## 16. Base Motor Weights

Base motor weights are conceptual, deterministic, auditable, and non-probabilistic.

They are not a ML ensemble.

They do not create confidence.

They do not approve signals.

| Regime label | Motor A weight | Motor B weight | Motor C weight |
| --- | --- | --- | --- |
| `trend_bullish` | `normal` | `elevated` | `normal` |
| `trend_bearish` | `normal` | `elevated_if_strategy_family_compatible` | `normal` |
| `chop_range` | `normal` | `reduced_unless_range_compatible` | `normal` |
| `high_volatility` | `elevated` | `reduced` | `elevated_later_via_event_modulation` |
| `low_volatility` | `normal` | `reduced_unless_low_volatility_compatible` | `normal` |
| `risk_off` | `elevated` | `constrained` | `elevated_later_via_event_modulation` |
| `event_driven` | `elevated` | `constrained_until_event_review` | `elevated_later_via_event_modulation` |
| `liquidity_stress` | `elevated` | `constrained` | `elevated_later_via_event_modulation` |
| `unknown_or_unclassified` | `reduced` | `constrained` | `normal` |

Under current Motor B `framework_only` conditions, any elevated Motor B conceptual weight remains non-operational and cannot create downstream eligibility.

## 17. Regime-Adjusted Permissions

Regime-adjusted permissions may express:

- contextually supported review;
- contextually degraded review;
- contextually blocked review;
- additional confirmation required;
- unavailable due to missing context.

Regime-adjusted permissions must not express:

- trade approval;
- strategy promotion;
- Paper Trading approval;
- Live Trading approval;
- execution readiness;
- capital allocation readiness;
- Risk Engine approval;
- Motor B evidence upgrade.

If regime context conflicts with Motor B restrictions, Motor B restrictions and `08 Risk Engine` governance dominate.

## 18. Motor B Framework-Only Protection Rules

The current Motor B state remains:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

If Motor B `adapter_status` is one of:

```text
accepted_for_design_only
accepted_for_dry_run_only
degraded_framework_only
```

then Motor A output must preserve:

```text
downstream_operational_eligibility = blocked
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

| Motor B adapter status | Required Motor A handling |
| --- | --- |
| `accepted_for_design_only` | Keep downstream operational eligibility blocked; use only for documentation, schema design, or contract review. |
| `accepted_for_dry_run_only` | Keep downstream operational eligibility blocked; use only for dry-run, mock validation, or interface validation. |
| `degraded_framework_only` | Keep downstream operational eligibility blocked; treat as canonical downstream readiness degradation. |

For all three statuses:

- no trade approval;
- no Paper Trading;
- no Live Trading;
- no execution;
- no capital allocation;
- no strategy promotion;
- no operational signal promotion;
- no confidence generation;
- no relaxation of Motor B restrictions;
- Motor A context cannot override this.

## 19. Motor A / Motor C Independence Rule

Motor A and Motor C are parallel conceptual inputs.

Motor A and Motor C are independent.

Motor A does not depend on Motor C.

Motor C does not depend on Motor A.

Block 03 does not implement Motor C, consume Motor C output, define Motor C classifier behavior, or create LLM prompting rules.

Motor A may define an `event_modulation_hook` so later deterministic fusion logic can receive Motor C event effects, but the hook is only a conceptual interface declared for future use.

## 20. Event Modulation Hook For Block 08

The `event_modulation_hook` is a conceptual interface for later Block 08 Deterministic Signal Fusion Engine.

It allows later fusion logic to apply event precedence when Motor C exists and is contract-valid.

Motor A does not consume or implement Motor C.

Event severity may modulate, constrain, or suspend conceptual motor weights in Block 08.

A favorable regime cannot ignore a critical event.

Examples of event classes that may later require event precedence:

- surprise FOMC decision;
- exchange hack;
- regulatory decision;
- stablecoin depeg;
- security incident;
- systemic crypto event.

Conceptual hook fields may include:

```text
event_modulation_allowed
event_modulation_hook
event_precedence_expected
critical_event_can_suspend_weights
affected_assets_required
event_severity_required
```

This hook does not implement event classification and does not approve trading.

## 21. Missing Or Stale Regime Context Rules

Motor A output must be `degraded` or `unavailable` when:

- `regime_label` is missing;
- `regime_source` is missing;
- `regime_timestamp` is missing;
- `regime_method_version` is missing;
- supported assets are missing or do not cover the candidate asset;
- supported timeframes are missing or do not cover the candidate timeframe;
- source references are missing;
- context is stale;
- context is synthetic without dry-run marking;
- limitations are missing.

If regime context is missing, stale, unsupported, or unknown:

```text
context_label = context_unavailable_or_uncertain
downstream_operational_eligibility = blocked
confidence_score = null
```

Missing or stale regime context must not be silently treated as neutral or favorable.

## 22. Confidence And Uncertainty Handling

Motor A may carry:

- `uncertainty_level`;
- `confidence_status`;
- source-specific context confidence metadata when available.

Motor A confidence is context confidence only.

Motor A confidence does not replace backtesting evidence.

Motor A confidence does not replace Motor B confidence.

Motor A confidence must not fill Motor B `confidence_score`.

If Motor A `confidence_score` does not exist or does not apply, it must remain:

```text
confidence_score = null
```

with explicit `confidence_status`.

If regime context is stale, missing, unsupported, synthetic, or unavailable, Motor A output must be degraded or unavailable and must preserve uncertainty.

## 23. Audit And Traceability Requirements

Every Motor A output must include:

- input identifier;
- output identifier;
- source references;
- source owner;
- source method version;
- regime timestamp;
- output creation timestamp;
- supported assets;
- supported timeframes;
- context label;
- regime label;
- activation rules applied;
- base motor weights selected;
- limitations;
- uncertainty level;
- stale context flag;
- missing context;
- Motor B constraints observed;
- forbidden downstream usage;
- schema version;
- audit references.

Later 07 blocks must be able to replay why a strategy family was `contextually_supported`, `contextually_degraded`, `contextually_blocked`, `requires_additional_confirmation`, or `unavailable_due_to_missing_context`.

## 24. Relationship With 07-Block-06 Signal Candidate Normalization

Motor A prepares context for later `07-Block-06 Signal Candidate Normalization`.

Preparation means:

- exposing context labels;
- exposing regime labels;
- exposing uncertainty;
- exposing activation rules;
- exposing base motor weights;
- exposing limitations;
- exposing downstream restrictions;
- preserving Motor B constraints.

Preparation does not mean:

- creating a signal candidate;
- normalizing signal candidates;
- fusing signals;
- computing confidence;
- approving strategy promotion;
- authorizing Paper Trading.

## 25. Relationship With 08 Risk Engine

`08 Risk Engine` keeps final authority over downstream eligibility, veto, promotion, risk decisions, risk limits, and operational blocking.

Motor A produces context and conceptual routing or weighting only.

07 does not approve trading.

08 may veto any later fused signal candidate regardless of Motor A context.

Paper Trading remains blocked under the current Motor B `framework_only` state.

Motor A output must preserve enough information for `08 Risk Engine` to identify:

- stale context;
- missing context;
- unsupported asset or timeframe;
- high uncertainty;
- Motor B `framework_only` state;
- `paper_trading_eligibility = blocked`;
- `confidence_status = confidence_not_available`;
- `confidence_score = null`;
- event modulation expectations;
- forbidden downstream usage;
- non-approval status.

## 26. Explicit Prohibited Actions

Block 03 must not:

- implement trading logic;
- implement Paper Trading;
- implement Live Trading;
- create execution logic;
- create capital allocation;
- create signal fusion;
- create Signal Candidate Normalization;
- create Bull/Bear Debate;
- create a new Motor B Adapter;
- create Motor C Event Classifier;
- create LLM prompting rules;
- create Confidence Aggregation;
- create Risk Handoff;
- modify the Motor B Output Contract of 06;
- modify Block 00, Block 01, or Block 02;
- redefine contracts of prior stages;
- invent backtesting results;
- invent OOS validation;
- invent walk-forward validation;
- invent robustness results;
- invent historical results;
- invent `confidence_score`;
- convert regime context into empirical evidence;
- convert mock data into real evidence;
- create a ML ensemble;
- start Block 04.

## 27. Block 03 Closure Criteria

Block 03 is closed when this document defines:

- Motor A Context Layer purpose;
- scope;
- non-authority rules;
- Motor A definition;
- relationship with Block 00, Block 01, and Block 02;
- relationship with `04 Research Layer` / Regime Detection v1;
- explicit statement that regime context is market context, not trading evidence;
- explicit statement that activation is not trade approval;
- Motor A input contract;
- Motor A output contract;
- context labels;
- regime labels;
- regime metadata;
- regime-to-context mapping;
- `regime_strategy_activation_rules`;
- `base_motor_weights`;
- regime-adjusted permissions;
- Motor B `framework_only` protection rules;
- Motor A and Motor C independence;
- `event_modulation_hook` for later Block 08;
- missing or stale regime context rules;
- confidence and uncertainty handling;
- audit and traceability requirements;
- relationship with 07-Block-06 Signal Candidate Normalization;
- relationship with `08 Risk Engine`.

Closing Block 03 does not implement Motor A in code and does not create Motor C, Signal Candidate Normalization, Signal Fusion, Confidence Aggregation, Risk Handoff, Paper Trading, Live Trading, execution logic, or capital allocation.
