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
