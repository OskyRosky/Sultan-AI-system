# 13 Decision Log

## Initial Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-001 | 05 Strategy Engine starts after the closure of 04 Research Layer. | Accepted |
| D-002 | 05 Strategy Engine does not perform backtesting. | Accepted |
| D-003 | 05 Strategy Engine does not calculate PnL. | Accepted |
| D-004 | 05 Strategy Engine does not execute orders. | Accepted |
| D-005 | 05 Strategy Engine does not confirm edge. | Accepted |
| D-006 | 05 Strategy Engine creates auditable strategy candidates. | Accepted |
| D-007 | Regime Context Framing comes before Rule Construction and Strategy Composition. | Accepted |
| D-008 | Falsification Criteria will be mandatory in the Strategy Candidate Registry. | Accepted |
| D-009 | Risk Templates are design constraints, not a real Risk Engine. | Accepted |
| D-010 | Strategy Closure and Strategy Dossier Handoff are separate blocks. | Accepted |
| D-011 | 02 Strategy Inputs Contract will be treated as a critical block. | Accepted |

## Notes

These decisions are architectural constraints for Block 1. They do not validate any strategy, edge, performance claim, or downstream execution path.

## Block 02 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-012 | 05 Strategy Engine will maintain its own explicit eligibility decision separate from 04 research lifecycle status. | Accepted |
| D-013 | Evidence alone is never eligible to feed future signal or strategy candidate design. | Accepted |
| D-014 | Findings must preserve their real 04 source status and require `promoted_to_quality_review`, auditability, limitations, and linked evidence before they can be eligible for strategy design. | Accepted |
| D-015 | Hypotheses must preserve their real 04 source status and require `promoted_for_strategy_review`, auditability, limitations, traceability, and falsification criteria before they can be eligible for strategy design. | Accepted |
| D-016 | `eligible_for_strategy_design` is produced by 05 as part of the eligibility decision and permits only future conceptual signal and rule design inside 05. | Accepted |
| D-017 | Eligibility does not imply edge, profitability, robustness, backtest readiness, deployment readiness, or trading approval. | Accepted |
| D-018 | Block 02 uses synthetic mockups only and does not integrate with real 04 outputs. | Accepted |
| D-019 | 05 does not treat 04 `promoted_for_strategy_review` or `promoted_to_quality_review` as edge, profitability, or trading approval. | Accepted |
| D-020 | Findings do not require hypothesis falsification criteria; that requirement applies only to hypotheses. | Accepted |

## Block 03 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-021 | Signal definitions must originate from eligible hypothesis decisions produced by Block 02. | Accepted |
| D-022 | Eligible findings may support signal context but cannot originate a signal definition by themselves. | Accepted |
| D-023 | Evidence decisions cannot originate or directly support signal definitions. | Accepted |
| D-024 | Signal orientations are conceptual labels only and are not orders, rules, trades, or execution instructions. | Accepted |
| D-025 | Block 03 creates synthetic mockups and tests only; it does not create real signals or advance to rule construction. | Accepted |
