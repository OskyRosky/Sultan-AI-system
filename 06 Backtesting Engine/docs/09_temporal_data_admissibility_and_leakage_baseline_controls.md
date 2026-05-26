# 09 Temporal Data Admissibility And Leakage Baseline Controls

## Purpose

Block 04 defines the Temporal Data Admissibility & Leakage Baseline Controls for 06 Backtesting Engine.

Its purpose is to decide whether a documented Historical Data & Feature Snapshot from Block 03 is temporally admissible for honest historical evaluation.

This block controls the risk that a backtest appears valid while using information that would not have been available at the historical decision point. That risk includes lookahead bias, data leakage, future information contamination, feature availability violations, label leakage, timestamp ambiguity, undeclared survivorship bias, revised data misuse, and retrospective universe selection.

Block 04 is blocking because no operationalization, simulation specification, protocol design, friction modeling, risk simulation, trade simulation, metric calculation, robustness review, or result interpretation is valid if the underlying snapshot fails temporal admissibility.

Block 04 occurs after Block 03 because the snapshot must first define what data and features are intended for review. It occurs before Block 05 because strategy operationalization must not be built around data or features that could not have been used honestly at the simulated decision time.

No historical result from 06 is admissible if this layer fails. A profitable backtest produced from temporally contaminated data is invalid evidence.

## Temporal Admissibility

Temporal admissibility is the condition that every datum, feature, metadata field, universe definition, label boundary, and documented assumption used by a historical evaluation was available to the system at or before the historical decision point where it is used.

The governing rule is:

For any historical decision timestamp `t`, 06 may use only information that can be demonstrated to have been available to the system at or before `t`, considering event time, publication time, availability time, processing time, feature generation time, feature window boundaries, decision time, and simulated execution time.

A historical date alone is not sufficient. A record can describe an event that occurred before `t` while still being unavailable, unpublished, revised later, processed later, or transformed using information after `t`.

Block 04 must distinguish at least these temporal concepts:

| Concept | Meaning |
| --- | --- |
| Event time | When the underlying market, data, or external event occurred. |
| Availability time | When the information was available to the system for use. |
| Processing time | When the information was ingested, normalized, transformed, or otherwise processed. |
| Feature generation time | When the feature value was generated or would have been generated for the evaluation. |
| Decision time | When the simulated strategy decision is made. |
| Simulated execution time | When a simulated order, fill, position change, or execution event would occur in later blocks. |

Temporal admissibility requires availability at decision time. It does not require only that the event happened before decision time.

## Lookahead Bias

Lookahead bias occurs when the evaluation uses information from after the simulated decision point to make or influence a decision at that point.

Lookahead bias includes direct use of future values and indirect use of features, filters, metadata, labels, rankings, or corrected records that encode future information.

Conceptual examples include:

- Using the close price of the current candle to decide an entry before that candle has closed.
- Using features calculated with data from future bars, future trades, future candles, or future labels.
- Treating later-revised data as if the final revised value was known historically.
- Building rankings, liquidity filters, candidate universes, or inclusion rules using knowledge from after the decision point.
- Selecting strategy inputs using future performance, future survival, or future realized volatility.

Lookahead bias is a temporal integrity failure. Confirmed lookahead prevents advancement to Block 05.

## Data Leakage

Data leakage occurs when information that should be isolated from the model inputs or evaluation inputs enters the data, features, selection process, or protocol in a way that contaminates the historical evaluation.

Lookahead bias is one important form of temporal leakage, but leakage is broader. Leakage may occur even when timestamps appear plausible if labels, outcomes, evaluation rules, or future-derived variables influence the construction of inputs.

Conceptual examples include:

- Including a label, target, future return, realized outcome, or success/failure field in the feature set.
- Selecting features because they are known to perform well on the evaluation period.
- Using variables derived from later outcomes while presenting them as contemporaneous inputs.
- Allowing the evaluation protocol, metric target, or desired result to influence dataset construction.
- Redesigning features, filters, candidate inclusion, or falsification criteria after inspecting outcomes.

Confirmed leakage prevents advancement to Block 05.

## Future Information Contamination

Future information contamination is the general category covering any use of information that would not have been known or available at the historical moment being simulated.

It can enter through:

- Features.
- Labels.
- Universe selection.
- Survivorship filters.
- Liquidity or market quality filters.
- Revised or restated data.
- Post-event metadata.
- Manual annotations created after the evaluated period.
- Retrospective research notes.
- Evaluation protocol changes made after observing outcomes.

Future information contamination does not need to be intentional to invalidate a backtest. If contamination is confirmed, the snapshot must fail temporal review.

## Timestamp Requirements

Block 04 requires sufficient timestamp evidence to determine whether each data component and feature value was available at the historical decision point.

The exact technical field names may be formalized later, but the conceptual timestamp requirements include:

| Timestamp | Required Meaning |
| --- | --- |
| `event_timestamp` | When the underlying event occurred. |
| `availability_timestamp` | When the information became available for use by the system. |
| `revision_as_of_timestamp` or `point_in_time_as_of_timestamp` | Which version of a revisable record was available as of the historical review point. |
| `processing_timestamp` | When the record was ingested, normalized, corrected, transformed, or otherwise processed. |
| `feature_generation_timestamp` | When the feature value was generated or would have been generated. |
| `decision_timestamp` | When the simulated strategy decision is made. |
| `simulated_execution_timestamp` | When the simulated execution would occur in later blocks. |

Timestamp sufficiency is mandatory. If the review cannot establish enough temporal ordering to prove availability at decision time, the correct outcome is not optimistic acceptance. The outcome must be failure, incompleteness, missing metadata, or temporal ambiguity.

Event time alone is insufficient. A record with a valid historical event timestamp may still be inadmissible if availability time, processing time, or feature generation time cannot be demonstrated.

For revisable or correctable datasets, `availability_timestamp` alone is insufficient. Block 04 must also determine which version of the record was available at the historical point being simulated. A retrospectively revised value cannot be certified as temporally valid unless point-in-time or revision-as-of governance proves that the value used in the snapshot was the value available at that time, or the limitation is explicitly recorded and judged non-clean for later review.

## Data Availability Requirements

Each data component in the snapshot must be reviewable by availability at decision time.

The review must distinguish exchange-reported market data from non-exchange, non-market, or delayed-publication datasets.

For exchange-reported market data, such as OHLCV, availability may be inferred only under a conservative, explicit, and documented rule. For example, a closed candle may be considered available only after candle close plus any defined processing lag. The inference rule must be recorded in the audit trail and must not allow current-bar close data to drive decisions before the bar is closed and available.

For non-exchange, non-market, delayed-publication, manually curated, or revisable datasets, explicit availability or point-in-time metadata is mandatory. This includes:

- Fundamentals.
- Economic releases.
- Corporate actions.
- Filings.
- Alternative data.
- Analyst revisions.
- Manually curated datasets.
- Any delayed-publication dataset.

For these sources:

- `availability_timestamp`, `publication_timestamp`, or equivalent point-in-time metadata is required.
- Event timestamp alone is never sufficient.
- Inference from event time is not allowed.
- If availability cannot be demonstrated, temporal certification must fail or remain ambiguous.

The review must also determine whether:

- Publication, delivery, ingestion, and processing lags are documented where relevant.
- Revisions, restatements, corrections, or backfills are identified.
- Point-in-time or revision-as-of governance exists for revisable records.
- Missing periods and late-arriving records are registered.
- Availability assumptions are explicit and not hidden inside source descriptions.
- Historical records were not reconstructed from future snapshots without disclosure.

If availability cannot be demonstrated, the snapshot cannot be temporally certified.

## Feature Availability Rules

Each feature must have temporal lineage sufficient to show that its value at decision time was calculated only from information available at or before that decision time.

Every feature must declare:

- Feature identity and version.
- Upstream data dependencies.
- Temporal lineage to source records.
- Calculation window.
- Window start and window close rule.
- Whether the feature uses closed candles, incomplete candles, event streams, end-of-period values, or delayed records.
- Known lags or availability assumptions.
- Feature generation timestamp or equivalent generation timing rule.

Feature availability rules:

- Rolling windows must close before the decision timestamp.
- Any intraperiod or incomplete-bar feature rule must be explicitly reviewed and pre-approved within Block 04 before `temporally_certified` can be issued.
- Block 05 may only consume intraperiod exceptions already approved and recorded in the Block 04 audit trail.
- Block 05 cannot introduce new timing exceptions. If Block 05 needs a timing exception not pre-approved by Block 04, the process must return to Block 04 for re-certification.
- A feature calculated from a candle close may not be used before that candle is closed and available.
- By default, signals based on a closed bar may decide only at the next decision point after the bar is closed and available, unless an intraperiod exception has been pre-approved by Block 04.
- Features using current-candle information must document whether the candle is closed or incomplete and exactly what fields are available at decision time.
- The availability time of a derived or composite feature is the maximum or latest availability time of all constituent inputs, including upstream features, raw data, revisions, lags, and dependencies.
- A composite feature cannot be available earlier than its latest-available input. `feature_generation_timestamp` and pipeline completion time do not replace availability timestamps for dependencies and do not prove availability at decision time.
- Forward-fill or last-observation-carried-forward logic may begin only from availability time, or from the first bar after availability time according to the evaluation granularity. Forward-fill from event time is prohibited when event time precedes availability time.
- Any forward-fill must document source, lag, start point, and the timestamp basis used.
- Features must not use future labels, future outcomes, future universe membership, future liquidity, future volatility, or future corrections.
- Feature lineage from 03 Feature Engineering is required but does not by itself prove temporal admissibility.

If feature availability cannot be demonstrated, Block 04 must not issue `temporally_certified`.

## Label Leakage Controls

Future labels must remain isolated from historical inputs.

Block 04 must verify conceptually that:

- Labels, targets, future returns, future drawdowns, future stop outcomes, future take-profit outcomes, or future success/failure criteria do not appear inside input features.
- Future outcome criteria are not used to select the feature set.
- Falsification criteria are preserved from the governed dossier and are not redesigned after observing outcomes.
- Dataset construction is not conditioned on future target values.
- Evaluation labels are generated only for evaluation purposes and are not available to decision inputs at the same timestamp.

Confirmed label leakage is a stop condition.

## Cross-Sectional Leakage Controls

Cross-sectional leakage occurs when a transformation at a timestamp uses assets, values, ranks, or distributional information that were not contemporaneously available at that timestamp.

This risk applies to:

- Z-scores.
- Ranks.
- Deciles.
- Percentiles.
- Cross-sectional normalization.
- Universe-wide transformations.

Any cross-sectional transformation must use only the universe contemporaneously available at each historical timestamp. It must not use the final snapshot universe, assets added retrospectively, future survivors, future liquidity members, future data-complete assets, or assets selected using future performance.

If the contemporaneous universe cannot be reconstructed or governed, the transformation cannot be certified as clean.

## Universe And Survivorship Controls

The asset universe must be temporally valid.

Block 04 must evaluate whether universe selection could have been known at the historical decision point. The review must detect or require declaration of:

- Survivorship filtering.
- Exclusion of delisted, failed, migrated, inactive, or low-performing assets using future knowledge.
- Liquidity filters based on future liquidity rather than contemporaneous availability.
- Performance filters based on future returns.
- Exchange listing filters based on future listing status.
- Manual exclusions made after the evaluated period.

A universe filtered retrospectively by survival, liquidity, data completeness, or performance cannot be certified as clean merely because the limitation is declared.

Declaring survivorship bias or retrospective filtering is necessary but not automatically sufficient for `temporally_certified`. If the limitation is material to the strategy, universe, liquidity assumptions, or expected behavior, the snapshot must not receive simple `temporally_certified`; it must fail temporal review or receive a differentiated limitation-bearing state such as `temporally_certified_with_declared_limitations` if later governance accepts that state.

Material declared limitations must be carried forward for explicit review in Block 11 Robustness, Falsification & Anti-Overfitting. Declaration records the risk; it does not cleanse the data.

Undeclared survivorship bias prevents advancement to Block 05.

## Protocol Independence

The future experiment protocol must not contaminate data, features, labels, or universe construction.

Block 04 must preserve the independence between the planned evaluation and the inputs being reviewed. The snapshot must not be adapted to produce expected results, improve expected metrics, avoid known failures, or support a preferred narrative.

The dataset, feature universe, and asset universe must be defined independently of later outcomes. Later protocol design may constrain how an approved snapshot is evaluated, but it must not retroactively alter the data or feature inputs to fit desired results.

Block 04 covers data, feature, timing, label, and universe leakage. Research leakage, multiple testing, parameter mining, and overfitting are primarily governed by Block 11, but they must not contaminate Block 04 data, feature, timing, or universe inputs.

## Baseline Temporal Review Process

The baseline review process is conceptual and audit-oriented. It does not create executable validators in this block.

1. Confirm the Block 03 snapshot reference and the eligible StrategyDossier binding.
2. Confirm data source temporal metadata, including event, availability, processing, revision, and lag evidence where applicable.
3. Confirm feature lineage temporal metadata, including upstream dependencies, feature versions, and generation timing.
4. Confirm timestamp sufficiency for data, features, decision timing, and simulated execution timing.
5. Confirm feature window validity and that each rolling window closes before the simulated decision point.
6. Confirm labels, targets, future outcomes, and falsification criteria are isolated from inputs.
7. Confirm any intraperiod or incomplete-bar exception is reviewed and pre-approved by Block 04 before certification.
8. Confirm universe selection is not future-informed or that any survivorship or retrospective limitation is explicitly declared and assessed for materiality.
9. Register limitations, ambiguities, missing metadata, detected risks, risks reviewed and not found, and unresolved assumptions.
10. Issue exactly one temporal decision state.

This process must not run a simulation, calculate metrics, produce PnL, create trades, create datasets, create SQL, create pipelines, or create executable schemas.

## Decision States

The initial conceptual temporal decision states are:

| State | Meaning |
| --- | --- |
| `temporally_certified` | The snapshot has sufficient temporal evidence and passes baseline admissibility, leakage, lookahead, feature availability, label isolation, and universe review. It may proceed to Block 05. |
| `temporally_certified_with_declared_limitations` | The snapshot passes temporal review only with explicit non-clean limitations that must be carried into later governance, including Block 11 where relevant. This state does not mean the limitation is harmless. |
| `temporal_integrity_failed` | The snapshot, data, features, timestamps, windows, labels, or universe fail temporal integrity controls. It must not proceed to Block 05. |
| `temporally_incomplete` | Required temporal review information is incomplete. Certification cannot be issued. |
| `temporal_metadata_missing` | Required event, availability, processing, generation, decision, execution, lag, or revision metadata is missing. |
| `temporal_availability_ambiguous` | The review cannot determine whether information was available at the decision point. Ambiguity blocks certification. |
| `leakage_risk_detected` | Leakage risk is detected and unresolved, including possible label leakage or outcome-driven dataset construction. |
| `lookahead_risk_detected` | Lookahead risk is detected and unresolved, including possible use of future values or future-informed transformations. |
| `survivorship_bias_undeclared` | The universe appears to depend on survival, future liquidity, future performance, future listing status, or future data completeness without explicit declaration. |
| `snapshot_rejected_for_temporal_review_failure` | The snapshot is rejected because temporal review failed and cannot support operationalization. |

These names are conceptual for Block 04 and may be formalized later as schemas, validators, registries, or tests.

Only `temporally_certified`, or a future formally accepted limitation-bearing equivalent, permits advancement to Block 05. Simple certification must not be issued for material declared survivorship or retrospective filtering limitations.

## Stop Conditions

Block 04 must stop the process when any of the following are confirmed or cannot be resolved:

- Confirmed leakage.
- Confirmed lookahead.
- Insufficient timestamps.
- Missing availability timestamps or equivalent availability evidence.
- Missing explicit availability, publication, or point-in-time metadata for non-exchange, non-market, delayed-publication, manually curated, or revisable datasets.
- Inference from event time for non-market or delayed-publication datasets.
- Feature availability cannot be demonstrated.
- Feature windows include information after the decision point.
- Intraperiod or incomplete-bar feature timing exception was not pre-approved by Block 04.
- Block 05 requires a new feature timing exception not recorded in the Block 04 audit trail.
- Forward-fill or LOCF begins before availability time.
- Composite feature availability is earlier than the latest availability time of any constituent input.
- Label leakage.
- Cross-sectional transformation uses the final snapshot universe or retrospectively included assets instead of the contemporaneously available universe.
- Retrospective universe selection is undeclared.
- Survivorship bias is undeclared.
- Declared survivorship or retrospective filtering is material but treated as clean certification.
- Snapshot is not traceable to a certified Block 03 snapshot.
- Snapshot was modified after Block 03 certification without returning to Block 03 and Block 04 review.
- Temporal metadata is inconsistent.
- Processing, revision, or backfill behavior is incompatible with historical availability.
- Revisable data lacks point-in-time or revision-as-of governance.
- Temporal ambiguity remains unresolved.

If a failure or unresolved ambiguity state is issued, the process must not advance to Block 05.

## Relationship With Block 05

Block 05 may receive only snapshots marked `temporally_certified`.

Block 05 cannot correct temporal failures. It cannot reinterpret temporal metadata. It cannot waive missing availability evidence. It cannot convert a temporally ambiguous snapshot into a simulation-ready input by adding operational assumptions.

Block 05 may only consume intraperiod, incomplete-bar, or feature timing exceptions that were pre-approved by Block 04 and recorded in the Block 04 audit trail before temporal certification. Block 05 cannot introduce new feature timing exceptions, change feature window timing, alter bar-close alignment, or move availability assumptions. If operationalization requires any timing exception not already certified by Block 04, the process must return to Block 04 for re-certification.

If Block 04 fails, 06 must generate governed feedback and stop. Remediation must occur through the owning upstream data, feature, snapshot, or dossier governance process before a new temporal review can be performed.

Operationalization is downstream of temporal certification. It is not a substitute for temporal certification.

## Audit Trail Requirements

Every temporal certification or failure must leave auditable evidence.

The audit trail must include:

- Snapshot identifier and version reviewed.
- Bound StrategyDossier identifier and version.
- Review timestamp or review version marker.
- Reviewer or process identifier, when formalized.
- Data sources reviewed.
- Feature lineage reviewed.
- Timestamp evidence evaluated.
- Availability assumptions reviewed.
- Exchange OHLCV availability inference rules, if used.
- Explicit availability, publication, point-in-time, or revision-as-of metadata for non-market or delayed-publication datasets.
- Processing, lag, revision, and backfill evidence reviewed.
- Feature windows reviewed.
- Intraperiod or incomplete-bar exceptions reviewed and either approved or rejected.
- Forward-fill or LOCF source, lag, start point, and timestamp basis reviewed.
- Cross-sectional transformations and contemporaneous universe basis reviewed.
- Label isolation checks performed.
- Universe and survivorship review performed.
- Risks detected and risks reviewed but not found.
- Limitations and ambiguities registered.
- Temporal decision state issued.
- Justification for the decision.
- Confirmation that no simulation, metrics, PnL, trades, or result inspection occurred in Block 04.

The audit trail must include a conceptual checklist using these statuses:

| Status | Meaning |
| --- | --- |
| `reviewed` | The category was reviewed and no unresolved issue remains. |
| `not_applicable` | The category does not apply to the snapshot under review. |
| `found` | A risk or issue was detected and recorded. |
| `unresolved` | The review could not resolve the risk or missing evidence. |
| `failed` | The category failed temporal review. |

The minimum checklist categories are:

- Lookahead risks.
- Leakage risks.
- Feature window compliance.
- Timestamp sufficiency.
- Availability metadata sufficiency.
- Label isolation.
- Cross-sectional transformations.
- Forward-fill or LOCF.
- Survivorship and universe construction.
- Point-in-time or revision governance.
- Intraperiod exception review.

The audit trail must be sufficient for quant research governance, model risk management, internal audit, trading systems engineering, reproducibility review, and external technical due diligence.

## Claude Code Audit Trigger

At the close of Block 04, an independent Claude Code audit is required before starting Block 05.

The audit must review:

- Whether the definitions of lookahead and leakage are sufficiently strict.
- Whether the process blocks contaminated snapshots.
- Whether the boundary between Block 03 snapshot definition and Block 04 temporal validation remains clean.
- Whether Block 05 can receive only temporally certified snapshots.
- Whether any wording implies permission to simulate before temporal certification.
- Whether unresolved temporal ambiguity blocks advancement.

Block 05 must not start until this audit is completed or formally waived by a documented governance decision outside this block.

## Explicit Non-Scope

Block 04 does not create a simulator.

Block 04 does not create a backtesting engine.

Block 04 does not calculate metrics.

Block 04 does not calculate PnL.

Block 04 does not create trades.

Block 04 does not create SQL.

Block 04 does not create pipelines.

Block 04 does not create datasets.

Block 04 does not create physical snapshots.

Block 04 does not create executable schemas.

Block 04 does not create Python code.

Block 04 does not create automated tests.

Block 04 does not create an executable leakage checker.

Block 04 is a documentation and conceptual governance block that defines the temporal admissibility contract for later technical implementation.
