# Research Layer Decision Log

## Initial Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| 04 starts after closure of 03 Feature Engineering. | Accepted | 03 produced the trusted feature base for research. |
| 04 does not create signals. | Accepted | Signals belong to strategy design, not research architecture. |
| 04 does not create backtesting. | Accepted | Backtesting belongs after strategy definition. |
| 04 does not create strategies. | Accepted | Strategy logic belongs to 05 Strategy Engine. |
| 04 uses quantitative findings, not LLM-invented findings. | Accepted | Findings must come from data, metrics, and interpretation rules. |
| Forward Returns Engine will be a separate component. | Accepted | Forward returns are high-risk for lookahead bias and need isolated validation. |
| Feature Ranking will be output of Feature Informativeness Analysis. | Accepted | Ranking is research evidence, not a signal. |
| Hypothesis Engine is defined as Hypothesis Registry. | Accepted | The component records hypotheses; it does not generate them automatically. |
| Research Reports are outputs of closure, not an independent component. | Accepted | Reports package validated evidence at the end of the layer. |
| Temporal Stability Analysis is an explicit component. | Accepted | Stability over time is a core anti-overfitting control. |

## Block 2 Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Timestamp alignment contract is `forward_return_h[t] = close[t + h] / close[t] - 1`. | Accepted | The feature row at `t` remains aligned with a future label while preserving clear temporal separation. |
| Forward return horizons are candle counts, not absolute time durations. | Accepted | Candle-count horizons preserve methodological comparability across timeframes during initial research. |
| Initial horizons remain `1`, `3`, `5`, and `10` candles for every timeframe. | Accepted | No differentiated horizon set by timeframe is introduced before evidence justifies it. |
| Rows without enough future candles remain `NaN`. | Accepted | Filling or interpolation would fabricate labels and contaminate research evidence. |
| Duplicate `(symbol, timeframe, timestamp)` rows are invalid input. | Accepted | Duplicate timestamps make `close[t]` ambiguous and can hide data quality defects. |
| Gaps are not filled by the Forward Returns Engine. | Accepted | The engine labels the next available candles and leaves calendar completeness checks to later quality analysis. |
| Forward returns are isolated by both `symbol` and `timeframe`. | Accepted | Labels must not cross asset or timeframe boundaries. |
| Block 2 calculates arithmetic forward returns only. | Accepted | Log returns require a separate methodological decision and are out of scope for this block. |
| Future Feature Profiling must include correlation and redundancy analysis. | Accepted | Redundancy control is required before feature evidence can be interpreted or ranked. |
| Block 8 must define a Hypothesis Registry schema/template before use. | Accepted | Hypotheses need consistent fields, evidence links, status, and review metadata. |
| Block 10 must define a multiple testing correction method. | Accepted | Broad feature scans require explicit anti-overfitting controls before conclusions are trusted. |

## Block 3 Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Research datasets are built by joining features and forward returns on `symbol`, `timeframe`, and `timestamp`. | Accepted | These keys define one completed candle observation and preserve the Block 2 label alignment. |
| Block 3 uses an inner join for matched research observations. | Accepted | The builder must not fabricate features or labels for unmatched keys. |
| Duplicate join keys are invalid in both feature and forward return inputs. | Accepted | Duplicate keys make the research observation ambiguous and can hide upstream data defects. |
| The builder consumes forward returns but does not calculate them. | Accepted | Forward return calculation belongs to the Forward Returns Engine and should remain independently validated. |
| Terminal `NaN` forward return labels are preserved. | Accepted | Missing future candles at series boundaries are valid labels state and must not be filled. |
| The builder does not modify feature definitions or feature values. | Accepted | Feature definitions and calculation logic belong to 03 Feature Engineering. |
| Block 3 creates only in-memory research datasets. | Accepted | Storage contracts and real dataset creation are outside this block. |

## Block 4 Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Feature Profiling describes standalone feature behavior and does not use forward returns. | Accepted | Predictive feature-to-return analysis belongs to later research components. |
| Profiling output is structured in memory as summary statistics, correlation diagnostics, and redundancy diagnostics. | Accepted | This keeps the block reproducible and audit-friendly without creating stored research datasets. |
| Default profiling grouping is `symbol` + `timeframe`. | Accepted | Assets and timeframes must not be mixed silently. |
| Profiling also supports explicit grouping by only `symbol` or only `timeframe`. | Accepted | Block 4 needs basic stability views across assets and across timeframes without predictive analysis. |
| Outliers are counted using the IQR rule with `1.5 * IQR` bounds. | Accepted | The method is simple, explicit, and appropriate before introducing more complex robust statistics. |
| Correlation uses pairwise Pearson correlation between numeric feature columns. | Accepted | Pearson correlation is a transparent first-pass redundancy diagnostic. |
| Extreme redundancy is flagged at `abs(correlation) >= 0.95`. | Accepted | The threshold marks candidates for review but does not imply causality, alpha, or automatic removal. |
| Block 4 does not normalize, scale, select, cluster, or transform features. | Accepted | Profiling should describe feature state before later methodology decides transformations. |

## Block 5 Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Temporal Stability Analysis evaluates windowed behavior of feature-to-forward-return relationships. | Accepted | One-period relationships can be unstable, episodic, or cherry-picked. |
| Metrics are grouped by `symbol`, `timeframe`, and `window`. | Accepted | Assets, timeframes, and temporal periods must remain traceable and isolated. |
| Block 5 supports explicit timestamp windows and equal-count chronological windows. | Accepted | Explicit windows support audit reviews, while equal-count windows support early methodology and synthetic tests. |
| Empty explicit windows are retained with `sample_count = 0` and null metrics. | Accepted | Missing coverage should be visible instead of silently dropped. |
| Window-level relationship uses Pearson correlation between feature and forward return columns. | Accepted | Pearson correlation is a simple diagnostic for drift, not a final informativeness metric. |
| Drift metrics summarize ranges and standard deviations across windows. | Accepted | Cross-window variation helps expose instability without creating a ranking or score. |
| Sign consistency is descriptive and not an alpha signal. | Accepted | Stable signs do not prove causality, profitability, or strategy usefulness. |
| Block 5 does not create thresholds for acceptance or rejection. | Accepted | Automatic feature selection and ranking are outside this block. |
| Block 5 does not perform rolling optimization, ML, forecasting, or composite scoring. | Accepted | The block must remain limited to auditable statistical stability diagnostics. |

## Block 6 Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Feature Informativeness compares feature values at `t` with already aligned forward returns at `t`. | Accepted | Reusing aligned labels avoids extra shifting and reduces lookahead risk. |
| Block 6 does not calculate or modify forward returns. | Accepted | Label construction belongs to the Forward Returns Engine. |
| Bucket analysis uses quantile buckets inside each `symbol`, `timeframe`, `feature`, and `forward_return` scope. | Accepted | Local buckets avoid silently mixing assets, timeframes, features, or horizons. |
| Bucket metrics include count, mean forward return, median forward return, hit rate, and average absolute forward return. | Accepted | These provide simple descriptive research evidence without strategy simulation. |
| Information Coefficient includes Pearson and Spearman correlation. | Accepted | Pearson captures linear association; Spearman captures rank association. |
| Constant features or constant forward returns produce null IC. | Accepted | Correlation is undefined when either side has no variation. |
| Preliminary ranking is ordered by absolute Pearson IC, absolute Spearman IC, and sample count. | Accepted | The ranking is technical metadata only and must not become a signal or automatic feature selection. |
| Block 6 does not address formal multiple testing correction. | Accepted | Multiple testing correction belongs to Block 10 before broad conclusions are trusted. |

## Block 7 Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Regime Analysis uses simple auditable labels derived from caller-provided in-memory context columns. | Accepted | Labels must be reproducible and reviewable before complex regime models are considered. |
| Trend labels are `bullish`, `bearish`, and `neutral`. | Accepted | Sign-based trend labels provide a simple first-pass context split. |
| Momentum labels are `positive`, `negative`, and `flat`. | Accepted | Sign-based momentum labels are explicit and easy to audit. |
| Volatility labels are `low_vol`, `medium_vol`, and `high_vol` using within-group terciles. | Accepted | Terciles avoid hard-coded market thresholds while preserving group isolation. |
| Range labels are `compressed` and `expanded` using the within-group median. | Accepted | Median split is simple and avoids complex range models in this block. |
| Conditional metrics are grouped by `symbol`, `timeframe`, `forward_return`, `regime_type`, `regime`, and `feature`. | Accepted | This preserves traceability and prevents silent mixing of horizons or regimes. |
| Conditional metrics include IC, hit rate, mean forward return, median forward return, and average absolute forward return. | Accepted | These match informativeness diagnostics without creating strategy performance metrics. |
| Empty expected regimes are retained with `sample_count = 0` and null metrics. | Accepted | Missing regime coverage should be visible rather than silently omitted. |
| Block 7 does not create regime strategy, switching logic, or operational thresholds. | Accepted | Detecting conditional differences is not equivalent to trading on them. |

## Framework Hardening Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Minimum non-null pairs for Pearson/Spearman correlation is 5 across stability, informativeness, and regime modules. | Accepted | Two-point correlations are mechanically perfect when both series vary and should not be reported as research evidence. |
| Shared helper logic lives in `research/_common.py`. | Accepted | Common validation and correlation behavior should remain consistent without introducing a larger framework. |
| Regime context columns cannot also be analyzed as feature columns. | Accepted | This prevents tautological regime segmentation and circular informativeness evidence. |
| Current Research Layer assumes caller-provided single-exchange series. | Accepted | 04 groups by `symbol/timeframe`; multi-exchange support needs an explicit join and lineage contract before use. |
| Block 6 pooled IC is descriptive and not inferential. | Accepted | Pooled IC can be dominated by specific periods or regimes and does not replace IC time-series, ICIR, t-stats, or confidence intervals. |

## Block 8 Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Hypothesis Registry records human-authored research hypotheses; it does not generate hypotheses automatically. | Accepted | Hypotheses must remain grounded in evidence, assumptions, and human review. |
| Hypotheses require explicit falsification conditions. | Accepted | Falsifiability reduces narrative fitting and prevents vague claims from entering the registry. |
| Allowed statuses are `draft`, `proposed`, `rejected`, `archived`, and `promoted_for_strategy_review`. | Accepted | The lifecycle supports research governance without implying trading approval. |
| Trading statuses such as `approved_for_trading`, `live_strategy`, and `deploy_ready` are excluded. | Accepted | Strategy approval and deployment are outside 04 Research Layer. |
| Registry operations are pure in-memory transformations. | Accepted | Block 8 defines governance structure without storage, SQL, datasets, or orchestration. |
| Registry uniqueness is enforced by `hypothesis_id`. | Accepted | Stable identifiers are required for auditability and future review. |
| Evidence source is structured metadata, not proof. | Accepted | Observational research evidence should remain traceable without being overstated. |

## Block 9 Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Research Findings Registry records human-reviewed structured observations; it does not generate findings automatically. | Accepted | Findings must remain grounded in quantitative evidence and reviewable context. |
| Findings require structured `supporting_metrics` and `sample_scope`. | Accepted | Evidence and scope must be auditable before Quality Gates can evaluate the finding. |
| Findings require explicit limitations and caveats. | Accepted | Caveats reduce narrative fitting and prevent observational metrics from being overstated. |
| Finding decisions are limited to `advance_to_quality_review`, `defer`, `reject`, `needs_more_data`, and `archive`. | Accepted | Decisions should support research governance without implying trading action. |
| Finding statuses are limited to `draft`, `observed`, `under_review`, `rejected`, `archived`, and `promoted_to_quality_review`. | Accepted | Status lifecycle prepares findings for quality review without trading approval. |
| Trading decisions and trading statuses are excluded from the registry. | Accepted | Trading approval, deployment, and live logic are outside 04 Research Layer. |
| Registry operations are pure in-memory transformations. | Accepted | Block 9 defines evidence management without storage, SQL, datasets, or orchestration. |
| Finding uniqueness is enforced by `finding_id`. | Accepted | Stable identifiers are required for traceability and future review. |

## Block 10 Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| Quality Gates evaluate methodological readiness, not edge or profitability. | Accepted | Passing quality review must not be interpreted as strategy validation. |
| Default minimum sample count is 30. | Accepted | Smaller samples are too fragile for broad research interpretation and should be marked insufficient. |
| Default weak absolute IC threshold is 0.03. | Accepted | Very small IC values should be surfaced as weak evidence while remaining descriptive. |
| Default maximum NaN ratio is 0.20. | Accepted | Heavy missingness can distort evidence and should trigger review. |
| Default maximum regime or period concentration is 0.80. | Accepted | Evidence concentrated in one regime or period is vulnerable to cherry-picking and instability. |
| Default minimum regime sample count is 10. | Accepted | Sparse conditional segments should be flagged before interpretation. |
| Pooled-only IC receives a warning. | Accepted | Pooled IC is descriptive and does not replace IC time-series, ICIR, or inferential checks. |
| Quality results include passed checks, failed checks, warnings, reviewer notes, and evaluated timestamp. | Accepted | Auditability requires explicit check-level traceability. |
| Quality statuses are limited to `pass`, `warning`, `fail`, and `insufficient_evidence`. | Accepted | Statuses must not imply alpha, deployment readiness, or trading action. |

## Block 11 Decisions

| Decision | Status | Rationale |
| --- | --- | --- |
| 04 Research Layer is closed as a framework build, not as completed empirical research. | Accepted | Infrastructure can be complete before real research execution. |
| Research dossier outputs are placeholders until real research is executed. | Accepted | Closure must avoid invented findings, hypotheses, or edge claims. |
| 05 Strategy Engine readiness requires real research execution and human-reviewed evidence. | Accepted | Strategy work must not start from framework scaffolding alone. |
| Outputs valid for future 05 review are structured evidence, reviewed hypotheses, reviewed findings, caveats, quality gate results, and methodology notes. | Accepted | These preserve research governance while maintaining separation from strategy logic. |
| Outputs not valid as strategy-ready artifacts include rankings, IC values, findings, hypotheses, and quality statuses by themselves. | Accepted | No 04 artifact confirms edge, profitability, or trading readiness. |
| Deferred items remain explicit at closure. | Accepted | IC time-series, ICIR, t-stats, confidence intervals, formal multiple testing correction, out-of-sample validation, metadata bridges, cross-asset/cross-horizon robustness, multi-exchange support, dataset fingerprinting, real research execution, and strategy conversion are not part of framework closure. |

## Final Documentation Hardening

| Decision | Status | Rationale |
| --- | --- | --- |
| Pooled IC limitation is explicitly documented across informativeness, quality, and closure docs. | Accepted | Pooled IC is descriptive, does not measure temporal consistency, and must not be treated as robust evidence. |
| Rolling IC and ICIR remain deferred but required before serious strategy research. | Accepted | Strategy research needs temporal consistency diagnostics beyond pooled association. |
| Regime look-ahead caveat is documented for volatility and range labels. | Accepted | Global group statistics can use later rows and affect causal interpretation, even without target leakage. |
| Stationarity testing remains deferred. | Accepted | Non-stationary features can create spurious correlations, especially in crypto trending markets. |
| Dataset row-loss monitoring remains deferred for real runs. | Accepted | Inner joins and forward-return horizons can discard rows and must be measured during real research execution. |
| Final hardening items are methodological caveats, not architectural blockers. | Accepted | The framework can close while these research-methodology checks remain required before 05 strategy research. |
