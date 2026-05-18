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
