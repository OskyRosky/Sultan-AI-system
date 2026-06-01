# 07 Signal Fusion + LLM Motors - Motor C Event / LLM Classifier Contract

## 1. Purpose

Block 04 defines the Motor C Event / LLM Classifier Contract for `07 Signal Fusion + LLM Motors`.

Motor C classifies macro, crypto, exchange, security, liquidity, stablecoin, regulation, market structure, and asset-specific events into auditable event metadata for later 07 blocks.

Motor C may identify event type, severity, affected assets, affected markets, affected exchanges, expected duration, uncertainty, source references, unsupported claims, conflicting sources, and `event_precedence_hint`.

Motor C classifies events; it does not approve trades.

LLM output is classification metadata, not empirical trading evidence.

Event severity is not trading authorization.

Motor A and Motor C are independent parallel inputs.

This block is documentary and contractual only. It does not implement Python code, event collection, LLM prompts, LLM safety policy, trading logic, Signal Candidate Normalization, Signal Fusion, Confidence Aggregation, Risk Handoff, Paper Trading, Live Trading, execution, or capital allocation.

## 2. Scope

This block covers:

- Motor C purpose and boundaries;
- Motor C input contract;
- Motor C output contract;
- `event_taxonomy`;
- severity schema;
- uncertainty rules;
- affected assets schema;
- expected duration schema;
- source reference requirements;
- LLM metadata requirements;
- hallucination and unsupported claim handling;
- missing source handling;
- event freshness and staleness rules;
- event deduplication and conflict handling;
- `event_precedence_hint` for 07-Block-08;
- Motor B `framework_only` protection rules;
- confidence and uncertainty handling;
- forbidden downstream usage propagation;
- audit and traceability requirements;
- relationship with 07-Block-06 Signal Candidate Normalization;
- relationship with 07-Block-08 Deterministic Signal Fusion Engine;
- relationship with `08 Risk Engine`.

This block does not cover:

- executable Motor C implementation;
- data ingestion code;
- complete LLM prompts;
- full LLM safety policy;
- Signal Candidate Normalization;
- Bull/Bear Debate;
- Deterministic Signal Fusion;
- final event precedence rules;
- final signal confidence;
- Confidence Aggregation;
- Risk Handoff;
- Paper Trading;
- Live Trading;
- execution logic;
- capital allocation.

## 3. Non-Authority Reminder

Motor C is non-authoritative.

Motor C has no authority to:

- approve trades;
- approve strategies;
- promote strategies;
- authorize Paper Trading;
- authorize Live Trading;
- execute orders;
- allocate capital;
- relax risk limits;
- bypass `08 Risk Engine`;
- change Motor B state;
- relax Motor B restrictions;
- compensate for missing Motor B evidence;
- fill Motor B `confidence_score`;
- replace empirical evidence;
- replace backtesting, OOS validation, walk-forward validation, robustness review, or historical performance evidence;
- decide final Signal Fusion weights;
- implement final event precedence rules.

Any accepted Motor C event remains classification metadata only.

Event classification, event severity, event freshness, event uncertainty, or LLM classification confidence must not be interpreted as trade approval, Paper Trading eligibility, Live Trading eligibility, execution readiness, capital allocation readiness, strategy promotion, or Risk Engine approval.

## 4. Definition Of Motor C

Motor C is the event and LLM-assisted classification layer within 07.

Motor C can classify and structure:

- macro policy events;
- central bank events;
- inflation or rates events;
- geopolitical events;
- crypto regulatory events;
- exchange security incidents;
- exchange outages;
- stablecoin depeg events;
- liquidity stress events;
- market structure events;
- protocol security events;
- major liquidation events;
- systemic crypto events;
- asset-specific news events;
- unknown or unclassified events.

Motor C may be assisted by LLMs for classification and structuring, but LLM output must remain source-bound, limitation-aware, and auditable.

Motor C is not:

- a trading engine;
- a strategy approval engine;
- a backtesting engine;
- a Risk Engine;
- an ML ensemble;
- a source of historical validation;
- a replacement for Motor A context;
- a replacement for Motor B evidence;
- a final Signal Fusion engine.

## 5. Relationship With Block 00, Block 01, Block 02, And Block 03

Block 00 established that 07 has no authority to approve trades, authorize Paper Trading, allocate capital, override `08 Risk Engine`, invent `confidence_score`, or reinterpret missing evidence.

Block 01 established Motor C event / LLM classifier output as a permitted conceptual input family only when source references, LLM metadata, classification timestamp, uncertainty, limitations, prohibited usage, prompt or instruction version, and audit references are explicit.

Block 02 established that Motor B currently enters 07 through the Motor B Adapter with:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

Block 03 established that Motor A and Motor C are independent parallel inputs and that Motor A may define an event modulation hook for later Block 08 without implementing Motor C.

Block 04 defines the Motor C contract. It must not modify Block 00, Block 01, Block 02, Block 03, or the Motor B Output Contract of 06.

Motor C cannot modify, reinterpret, relax, compensate for, or override Motor B adapter status, Motor B evidence state, Motor B confidence state, Motor B non-approval status, or Motor B forbidden downstream usage.

The combination of Motor C event metadata and degraded Motor B input must not be interpreted as convergent empirical evidence.

## 6. Core Classification Principles

Motor C classifies events; it does not approve trades.

LLM output is classification metadata, not empirical trading evidence.

Event severity is not trading authorization.

A critical event classification does not approve a trade.

A bullish event classification does not approve a trade.

A favorable event does not override Motor B `framework_only`.

A severe event may later constrain or suspend downstream handling, but only through 07-Block-08 Deterministic Signal Fusion Engine and `08 Risk Engine`.

## 7. Motor A / Motor C Independence Rule

Motor A and Motor C are independent parallel inputs.

Motor C does not consume Motor A.

Motor A does not consume Motor C.

Both can later be normalized in 07-Block-06 Signal Candidate Normalization.

Both can later contribute to deterministic fusion in 07-Block-08 Deterministic Signal Fusion Engine.

Block 04 must not create a dependency between Motor A and Motor C.

## 8. Motor C Input Contract

The conceptual Motor C input schema is:

```text
MotorCInput
  motor_c_input_id
  raw_event_id
  raw_event_text_or_payload_reference
  event_source_type
  event_source_name
  source_references
  source_timestamp
  ingestion_timestamp
  asset_universe
  language
  region
  source_reliability_label
  source_reliability_limitations
  deduplication_key
  prior_event_references
  human_review_metadata
  schema_version
```

### Field Meaning

- `motor_c_input_id`: stable identifier for the input event record.
- `raw_event_id`: source-native event or message identifier when available.
- `raw_event_text_or_payload_reference`: reference to raw event text, document, article, feed message, or payload.
- `event_source_type`: source class, such as news, official statement, exchange status, on-chain alert, security report, regulatory notice, or human review note.
- `event_source_name`: source name.
- `source_references`: auditable source URLs, document identifiers, feed identifiers, or file references.
- `source_timestamp`: timestamp asserted by the source.
- `ingestion_timestamp`: timestamp when the event entered 07.
- `asset_universe`: assets or markets considered in scope for classification.
- `language`: source language.
- `region`: source geography or jurisdiction when applicable.
- `source_reliability_label`: source reliability classification.
- `source_reliability_limitations`: known source limitations.
- `deduplication_key`: deterministic key for grouping duplicate or near-duplicate event records.
- `prior_event_references`: related prior events, superseded events, or updates.
- `human_review_metadata`: optional non-authoritative review metadata.
- `schema_version`: Motor C input schema version.

Missing required source references, timestamps, or source reliability metadata must produce degraded, unavailable, or rejected output according to the failure mode.

Inputs that claim trading authority, Paper Trading eligibility, strategy approval, empirical validation, or Risk Engine override must be rejected.

### source_reliability_label Enum

Allowed `source_reliability_label` values are:

```text
primary_verified_source
official_source
high_reliability_source
medium_reliability_source
low_reliability_source
unverified_source
anonymous_or_social_source
conflicting_source
unknown_reliability
```

Assignment criteria:

| Value | Criteria |
| --- | --- |
| `primary_verified_source` | Direct primary artifact with verifiable origin, such as a signed or canonical issuer, exchange, protocol, regulator, or central bank record. |
| `official_source` | Official source without full primary verification metadata, such as an official status page, announcement channel, filing, or policy notice. |
| `high_reliability_source` | Reputable source with strong historical reliability, transparent provenance, and source references. |
| `medium_reliability_source` | Secondary source with plausible provenance but incomplete primary confirmation. |
| `low_reliability_source` | Weak source, partial report, unclear provenance, or limited corroboration. |
| `unverified_source` | Source has not been independently verified. |
| `anonymous_or_social_source` | Anonymous, social, influencer, forum, or unattributed claim. |
| `conflicting_source` | Source materially conflicts with another credible source. |
| `unknown_reliability` | Reliability is missing, unknown, or cannot be evaluated. |

`source_reliability_limitations` must preserve limitations for every label.

Weak, anonymous, contradictory, unverified, or unknown sources must not be treated as validated evidence.

High or critical severity events sourced only from `low_reliability_source`, `unverified_source`, `anonymous_or_social_source`, `conflicting_source`, or `unknown_reliability` must require human review or degraded classification confidence.

### Deterministic Source Hierarchy

The deterministic source hierarchy for Motor C conflict and deduplication handling is:

```text
1. official_exchange_or_protocol_notice
2. official_regulator_or_central_bank_notice
3. issuer_or_project_primary_source
4. reputable_market_data_or_security_provider
5. reputable_news_source
6. cross_verified_independent_sources
7. single_secondary_source
8. social_media_or_anonymous_claim
9. unknown_or_unverified_source
```

The hierarchy supports event classification and conflict handling only.

The hierarchy does not create trading evidence, approve trades, or override Motor B `framework_only`.

Weak or unverified sources must degrade classification confidence or require human review.

Conflicting credible sources must preserve `conflicting_sources` and require review or degraded status unless a documented source hierarchy resolves the conflict.

A high or critical severity event from weak sources must not be treated as confirmed without stronger references.

## 9. Motor C Output Contract

The conceptual Motor C output schema is:

```text
MotorCEventOutput
  motor_c_event_id
  source_input_id
  event_type
  event_subtype
  severity
  severity_rationale
  affected_assets
  affected_markets
  affected_exchanges
  expected_duration
  event_freshness_status
  uncertainty_level
  classification_confidence_status
  classification_confidence_score
  source_references
  unsupported_claims
  missing_sources
  conflicting_sources
  llm_model_metadata
  prompt_or_instruction_version
  classification_timestamp
  prohibited_usage
  forbidden_downstream_usage
  event_precedence_hint
  requires_human_review
  audit_references
  limitations
  schema_version
```

### Field Meaning

- `motor_c_event_id`: stable identifier for the classified event.
- `source_input_id`: reference to the consumed Motor C input.
- `event_type`: top-level event category from `event_taxonomy`.
- `event_subtype`: optional specific subtype.
- `severity`: deterministic severity level.
- `severity_rationale`: source-bound rationale for severity classification.
- `affected_assets`: affected assets schema value and explicit asset list where applicable.
- `affected_markets`: affected markets or sectors.
- `affected_exchanges`: affected exchange venues where applicable.
- `expected_duration`: expected event duration class.
- `event_freshness_status`: freshness or staleness classification.
- `uncertainty_level`: classification uncertainty level.
- `classification_confidence_status`: confidence status for event classification only.
- `classification_confidence_score`: optional classification score, never trading confidence.
- `source_references`: source references used for classification.
- `unsupported_claims`: claims found in input that lack sufficient source support.
- `missing_sources`: required or expected sources that are missing.
- `conflicting_sources`: source conflicts or contradictory reports.
- `llm_model_metadata`: model, provider, version, and run metadata when LLM-assisted.
- `prompt_or_instruction_version`: prompt or instruction version used for classification.
- `classification_timestamp`: timestamp of classification.
- `prohibited_usage`: explicit prohibited usage.
- `forbidden_downstream_usage`: propagated downstream bans.
- `event_precedence_hint`: non-binding hint for 07-Block-08.
- `requires_human_review`: human review requirement flag or status.
- `audit_references`: replay and audit references.
- `limitations`: known limitations.
- `schema_version`: Motor C output schema version.

### classification_confidence_status Enum

Allowed `classification_confidence_status` values are:

```text
classification_confidence_unavailable
classification_confidence_degraded
classification_confidence_computed_from_sources
classification_confidence_rejected_insufficient_sources
classification_confidence_rejected_conflicting_sources
classification_confidence_rejected_stale_event
classification_confidence_requires_human_review
```

Assignment criteria:

| Value | Normalization class | Criteria |
| --- | --- | --- |
| `classification_confidence_unavailable` | unavailable | Classification confidence cannot be determined, model output is unavailable, or required confidence inputs are absent. |
| `classification_confidence_degraded` | degraded | Classification is usable only with limitations because sources are partial, weak, stale, ambiguous, or low quality. |
| `classification_confidence_computed_from_sources` | usable | Classification confidence is source-derived, source-referenced, schema-valid, and limited to event classification quality. |
| `classification_confidence_rejected_insufficient_sources` | rejected | Required sources are missing or insufficient for a valid classification. |
| `classification_confidence_rejected_conflicting_sources` | rejected | Source conflicts are material and cannot be resolved deterministically. |
| `classification_confidence_rejected_stale_event` | rejected | Event is stale, superseded, or temporally inadmissible for current classification. |
| `classification_confidence_requires_human_review` | requires_human_review | Event classification may be material, high uncertainty, high/critical severity, weakly sourced, or otherwise review-gated. |

classification_confidence_status is not trading confidence.

classification_confidence_status cannot replace Motor B `confidence_status`.

classification_confidence_status cannot fill Motor B `confidence_score`.

final signal confidence belongs to Block 09.

Block 06 may normalize these values, but must not convert them into trade approval, Paper Trading eligibility, or final signal confidence.

### classification_confidence_score Scale

`classification_confidence_score` is optional.

If used, it must be numeric in range `[0.0, 1.0]`.

It applies only to event classification quality.

It is not trading confidence.

It must be `null` when `classification_confidence_status` is unavailable, rejected, or `classification_confidence_requires_human_review`.

It must not be mapped to Motor B `confidence_score`.

It must not be used as final signal confidence.

## 10. Event Taxonomy

Initial conceptual `event_taxonomy` values are:

```text
macro_policy_event
central_bank_event
inflation_or_rates_event
geopolitical_event
crypto_regulatory_event
exchange_security_event
exchange_outage_event
stablecoin_depeg_event
liquidity_stress_event
market_structure_event
protocol_security_event
major_liquidation_event
systemic_crypto_event
asset_specific_news_event
unknown_or_unclassified_event
```

Unrecognized, unsupported, or insufficiently sourced events must be mapped to `unknown_or_unclassified_event` or rejected, depending on source validity and schema compatibility.

## 11. Severity Schema

Severity values are deterministic review classifications:

```text
none
low
medium
high
critical
unknown
```

| Severity | Criteria |
| --- | --- |
| `none` | No material event is identified or the input is informational without relevant market context. |
| `low` | Informational event with limited apparent impact, clear sources, no apparent systemic effect, and no direct venue, liquidity, stablecoin, or security stress. |
| `medium` | Relevant event for an asset, sector, protocol, region, or exchange, but without confirmed systemic contagion. |
| `high` | Event with possible material impact on relevant assets, liquidity, exchange operations, stablecoin integrity, protocol security, market structure, or risk conditions. |
| `critical` | Systemic event, severe security incident, major depeg, relevant hack, surprise regulation, critical market interruption, or severe liquidity/venue impairment. |
| `unknown` | Sources are insufficient, contradictory, stale, missing, or the event is not classifiable. |

Severity is not trading authorization.

Severity must not produce final fusion weights in Block 04.

## 12. Uncertainty Rules

Uncertainty values are:

```text
low_uncertainty
medium_uncertainty
high_uncertainty
unknown_uncertainty
```

`uncertainty_level` describes classification uncertainty only.

`uncertainty_level` is not a trading `confidence_score`.

Use `high_uncertainty` or `unknown_uncertainty` when:

- sources are missing;
- sources conflict;
- source reliability is low or unknown;
- event scope is unclear;
- expected duration is unclear;
- affected assets are broad or ambiguous;
- LLM output adds unsupported claims;
- human review is required.

## 13. Affected Assets Schema

Affected asset scope values are:

```text
all_market
asset_specific
sector_specific
exchange_specific
stablecoin_specific
unknown_scope
```

Rules:

- `all_market`: event plausibly affects broad crypto or macro market conditions.
- `asset_specific`: event is scoped to one or more named assets.
- `sector_specific`: event affects a sector such as DeFi, L1s, L2s, staking, miners, AI tokens, or exchange tokens.
- `exchange_specific`: event affects one or more exchanges or venues.
- `stablecoin_specific`: event affects one or more stablecoins or related liquidity channels.
- `unknown_scope`: scope is missing, unsupported, or contradictory.

Affected assets must not be invented.

When affected assets are inferred, the inference must be traceable to source references and limitations.

## 14. Expected Duration Schema

Expected duration values are:

```text
intraday
short_term
multi_day
medium_term
structural
unknown_duration
```

Rules:

- `intraday`: expected relevance within the same trading day or immediate session.
- `short_term`: expected relevance over one to several days.
- `multi_day`: expected relevance across multiple trading days.
- `medium_term`: expected relevance across weeks or a broader review window.
- `structural`: durable regime, regulatory, protocol, venue, liquidity, or market structure change.
- `unknown_duration`: insufficient evidence to estimate duration.

Expected duration is contextual metadata only.

It does not approve trades or determine final holding period.

## 15. Source Reference Requirements

Motor C classification must include `source_references`.

Source references must be sufficient to replay:

- what was classified;
- when the source event occurred;
- when it was ingested;
- which source provided it;
- which claims are supported;
- which claims are unsupported;
- which sources conflict;
- why human review is required, if applicable.

Valid source references may include:

- official exchange status page references;
- official regulatory documents;
- central bank statements;
- issuer or protocol disclosures;
- security advisories;
- on-chain alert references;
- trusted news references;
- human review records;
- internal feed message identifiers.

If source references are missing, Motor C output must be degraded, unavailable, or rejected according to severity of the missing source failure.

LLM output without source references must not be accepted as factual event classification.

## 16. LLM Metadata Requirements

Full LLM prompting policy belongs to Block 05.

Block 04 only defines the event classifier contract.

When event classification is LLM-assisted, output must include:

- `llm_model_metadata`;
- `prompt_or_instruction_version`;
- classification timestamp;
- source references;
- unsupported claims;
- missing sources;
- conflicting sources;
- limitations;
- prohibited usage;
- audit references.

LLMs cannot invent event facts.

LLMs cannot decide trading action.

LLMs cannot produce final signal confidence.

LLMs cannot replace backtesting/OOS/robustness evidence.

LLM classification must include source references.

## 17. Hallucination And Unsupported Claim Handling

Unsupported claims must be captured in `unsupported_claims`.

A claim is unsupported when:

- it appears in LLM output but not in source references;
- it is inferred without documented basis;
- it overstates certainty;
- it extrapolates beyond the source;
- it adds market impact claims without evidence;
- it asserts trading action or strategy approval.

If unsupported claims are material, Motor C output must be degraded or require human review.

If unsupported claims attempt to create trading authority, empirical validation, Motor B confidence, or downstream eligibility, the output must be rejected.

## 18. Missing Source Handling

Missing sources must be explicit in `missing_sources`.

Motor C output must not hide missing primary references, missing timestamps, missing venue confirmation, missing regulatory documents, missing security advisories, or missing conflicting reports.

When sources are missing:

```text
classification_confidence_status = classification_confidence_rejected_insufficient_sources
severity = unknown
event_type = unknown_or_unclassified_event
```

unless enough source-backed evidence remains to classify with explicit limitations.

Missing sources must not be treated as neutral or favorable.

## 19. Event Freshness And Staleness Rules

Motor C output must classify freshness using `event_freshness_status`.

Initial freshness values are:

```text
fresh
recent_but_monitor
stale
superseded
unknown_freshness
```

Use `stale`, `superseded`, or `unknown_freshness` when:

- source timestamp is missing;
- ingestion timestamp is missing;
- event timing is inconsistent;
- a later event supersedes the prior record;
- source references are old relative to the claimed event;
- expected duration has passed without confirmation;
- freshness cannot be replayed.

Stale events must not be silently used as current event context.

## 20. Event Deduplication And Conflict Handling

Motor C input must include `deduplication_key` where possible.

Motor C output must preserve `prior_event_references` or related event references where applicable.

Duplicate or near-duplicate events may be grouped for review, but grouping must not delete source-specific limitations or conflicts.

Conflicting sources must be explicit in `conflicting_sources`.

When sources conflict materially:

- `uncertainty_level` must be `high_uncertainty` or `unknown_uncertainty`;
- `classification_confidence_status` must be `classification_confidence_rejected_conflicting_sources` or `classification_confidence_requires_human_review`;
- `requires_human_review` should be true unless deterministic source hierarchy resolves the conflict;
- event severity must not be upgraded without source-backed rationale.

## 21. Event Precedence Hints For Block 08

Motor C can flag `event_precedence_hint`.

Block 08 decides deterministic event precedence rules.

Motor C must not apply final precedence.

A critical event hint does not approve a trade.

A bullish event classification does not approve a trade.

A favorable event does not override Motor B `framework_only`.

A severe event may later constrain or suspend downstream handling, but only through 07-Block-08 Deterministic Signal Fusion Engine and `08 Risk Engine`.

Conceptual event precedence hints include:

| Event example | Conceptual `event_precedence_hint` |
| --- | --- |
| Surprise FOMC decision | `possible_macro_override_hint` |
| Exchange hack | `possible_risk_suspension_hint` |
| Regulatory ban | `possible_asset_or_region_constraint_hint` |
| Stablecoin depeg | `possible_liquidity_or_systemic_risk_hint` |
| Protocol exploit | `possible_asset_specific_suspension_hint` |
| Exchange outage | `possible_execution_venue_constraint_hint` |

Hints are review metadata only until Block 08 defines deterministic precedence.

## 22. Motor B Framework-Only Protection Rules

The current Motor B state remains:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
confidence_status = confidence_not_available
confidence_score = null
```

If Motor B is `framework_only`, Motor C output must preserve:

```text
paper_trading_eligibility remains blocked
confidence_status remains confidence_not_available
confidence_score remains null
downstream_operational_eligibility remains blocked
```

| Motor B state | Required Motor C handling |
| --- | --- |
| `framework_only` | Keep downstream operational eligibility blocked; event classification may provide context only. |
| `paper_trading_eligibility = blocked` | Preserve the block; do not authorize Paper Trading. |
| `confidence_status = confidence_not_available` | Preserve confidence unavailability; do not substitute event confidence. |
| `confidence_score = null` | Preserve null trading confidence; do not fill it with LLM or event scores. |

For current Motor B state:

- Motor C cannot override this;
- LLM output cannot override this;
- event classification cannot create empirical validation;
- event classification cannot promote a strategy;
- no trade approval;
- no Paper Trading;
- no Live Trading;
- no execution;
- no capital allocation;
- no risk limit relaxation.

## 23. Confidence And Uncertainty Handling

`classification_confidence_status` may describe confidence of event classification only.

`classification_confidence_score`, if conceptually present, must be clearly separated from trading `confidence_score`.

Classification confidence cannot replace Motor B confidence.

Final signal confidence belongs to Block 09, not Block 04.

If sources are missing or conflicting, `classification_confidence_status` must use the explicit enum defined in this document and resolve to degraded, rejected, unavailable, or human-review-required as appropriate.

If event classification is LLM-assisted, model metadata and prompt/instruction version must be retained.

If event cannot be classified:

```text
event_type = unknown_or_unclassified_event
severity = unknown
```

Motor C must not invent trading `confidence_score`.

Motor C must not upgrade `confidence_status = confidence_not_available`.

## 24. Forbidden Downstream Usage Propagation

Motor C output must include `prohibited_usage` and `forbidden_downstream_usage`.

Motor C output must not be used for:

- trade approval;
- Paper Trading authorization;
- Live Trading authorization;
- execution;
- capital allocation;
- risk limit relaxation;
- strategy promotion;
- confidence invention;
- empirical validation replacement;
- Motor B evidence upgrade;
- Risk Engine bypass;
- final Signal Fusion weighting;
- final event precedence.

Any later 07 artifact that consumes Motor C output must preserve these restrictions.

## 25. Audit And Traceability Requirements

Every Motor C output must include:

- input identifier;
- output identifier;
- raw event reference;
- source type;
- source name;
- source references;
- source timestamp;
- ingestion timestamp;
- classification timestamp;
- event type;
- event subtype where applicable;
- severity;
- severity rationale;
- affected assets;
- affected markets;
- affected exchanges;
- expected duration;
- freshness status;
- uncertainty level;
- classification confidence status;
- unsupported claims;
- missing sources;
- conflicting sources;
- LLM model metadata where applicable;
- prompt or instruction version where applicable;
- prohibited usage;
- forbidden downstream usage;
- event precedence hint;
- human review requirement;
- limitations;
- schema version;
- audit references.

Later 07 blocks must be able to replay why an event was classified, which sources supported it, what was missing, what was conflicting, and why a precedence hint was or was not provided.

## 26. Relationship With 07-Block-06 Signal Candidate Normalization

Motor C prepares event context for later 07-Block-06 Signal Candidate Normalization.

Preparation means:

- exposing event type;
- exposing severity;
- exposing affected assets;
- exposing expected duration;
- exposing uncertainty;
- exposing freshness;
- exposing source references;
- exposing unsupported claims;
- exposing missing sources;
- exposing conflicting sources;
- exposing event precedence hints;
- preserving forbidden downstream usage.

Preparation does not mean:

- creating a signal candidate;
- normalizing signal candidates;
- fusing signals;
- computing final confidence;
- approving strategy promotion;
- authorizing Paper Trading.

## 27. Relationship With 07-Block-08 Deterministic Signal Fusion Engine

Motor C may provide event metadata and `event_precedence_hint` to later 07-Block-08 Deterministic Signal Fusion Engine.

Block 04 does not decide final fusion weights.

Block 04 does not implement event precedence rules.

Block 04 does not determine final signal confidence.

07-Block-08 may later define deterministic rules that constrain, suspend, or prioritize candidate handling based on event severity, freshness, affected assets, source quality, uncertainty, and Motor B restrictions.

Any future Block 08 use of Motor C must preserve:

- source references;
- uncertainty;
- unsupported claims;
- missing sources;
- conflicting sources;
- forbidden downstream usage;
- Motor B `framework_only` constraints;
- `08 Risk Engine` authority.

## 28. Relationship With 08 Risk Engine

`08 Risk Engine` keeps final authority over downstream eligibility, veto, promotion, risk decisions, risk limits, and operational blocking.

07 does not approve trading.

Motor C only produces event classification metadata.

08 may veto any later fused signal candidate regardless of Motor C classification.

Paper Trading remains blocked under the current Motor B `framework_only` state.

Motor C output must preserve enough information for `08 Risk Engine` to identify:

- event type;
- event severity;
- affected assets;
- affected exchanges;
- expected duration;
- freshness status;
- uncertainty;
- source quality;
- unsupported claims;
- missing sources;
- conflicting sources;
- Motor B `framework_only` state;
- `paper_trading_eligibility = blocked`;
- `confidence_status = confidence_not_available`;
- `confidence_score = null`;
- forbidden downstream usage;
- event precedence hints;
- human review requirements.

## 29. Explicit Prohibited Actions

Block 04 must not:

- implement trading logic;
- implement Paper Trading;
- implement Live Trading;
- create execution logic;
- create capital allocation;
- create signal fusion;
- create Signal Candidate Normalization;
- create Bull/Bear Debate;
- create a new Motor A layer;
- create a new Motor B Adapter;
- create complete LLM prompts;
- create full LLM Safety Policy;
- create Confidence Aggregation;
- create Risk Handoff;
- modify the Motor B Output Contract of 06;
- modify Block 00, Block 01, Block 02, or Block 03;
- redefine contracts of prior stages;
- invent backtesting results;
- invent OOS validation;
- invent walk-forward validation;
- invent robustness results;
- invent historical results;
- invent trading `confidence_score`;
- convert event classification into empirical evidence;
- convert LLM classification into an approved trading signal;
- convert mock data into real evidence;
- create a ML ensemble;
- start Block 05.

## 30. Block 04 Closure Criteria

Block 04 is closed when this document defines:

- Motor C Event / LLM Classifier Contract purpose;
- scope;
- non-authority reminder;
- Motor C definition;
- relationship with Block 00, Block 01, Block 02, and Block 03;
- explicit statement that Motor C classifies events; it does not approve trades;
- explicit statement that LLM output is classification metadata, not empirical trading evidence;
- explicit statement that Event severity is not trading authorization;
- explicit statement that Motor A and Motor C are independent parallel inputs;
- Motor C input contract;
- Motor C output contract;
- `event_taxonomy`;
- `source_reliability_label` enum;
- deterministic source hierarchy;
- `classification_confidence_status` enum;
- `classification_confidence_score` scale;
- severity schema;
- uncertainty rules;
- affected assets schema;
- expected duration schema;
- source reference requirements;
- LLM metadata requirements;
- hallucination and unsupported claim handling;
- missing source handling;
- event freshness and staleness rules;
- event deduplication and conflict handling;
- event precedence hints for Block 08;
- Motor B `framework_only` protection rules;
- confidence and uncertainty handling;
- forbidden downstream usage propagation;
- audit and traceability requirements;
- relationship with 07-Block-06 Signal Candidate Normalization;
- relationship with 07-Block-08 Deterministic Signal Fusion Engine;
- relationship with `08 Risk Engine`.

Closing Block 04 does not implement Motor C in code and does not create LLM prompts, LLM Safety Policy, Signal Candidate Normalization, Signal Fusion, Confidence Aggregation, Risk Handoff, Paper Trading, Live Trading, execution logic, or capital allocation.
