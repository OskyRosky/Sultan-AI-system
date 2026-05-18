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

