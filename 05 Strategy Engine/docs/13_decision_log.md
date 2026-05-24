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

## Block 04 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-026 | Regime context frames must originate from valid signal definitions produced by Block 03. | Accepted |
| D-027 | Regime context frames cannot originate directly from evidence, findings, hypotheses, or eligibility decisions. | Accepted |
| D-028 | Block 04 declares conceptual context only; it does not calculate, classify, forecast, or switch regimes. | Accepted |
| D-029 | Regime context framing cannot modify hypothesis eligibility, signal origin, or Block 02 decisions. | Accepted |
| D-030 | Block 04 creates synthetic mockups and tests only; it does not create rules, strategy candidates, backtests, or performance claims. | Accepted |

## Block 05 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-031 | Rule definitions must originate from a valid signal definition and a valid regime context frame. | Accepted |
| D-032 | The regime context frame referenced by a rule must reference the same signal definition. | Accepted |
| D-033 | Rule definitions are declarative and conceptual; they are not executable trading rules. | Accepted |
| D-034 | Block 05 does not define position sizing, stop loss, take profit, leverage, portfolio logic, or execution. | Accepted |
| D-035 | Block 05 creates synthetic mockups and tests only; it does not create strategy candidates, backtests, PnL, or performance claims. | Accepted |

## Block 06 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-036 | Strategy candidates must originate from one or more valid rule definitions produced by Block 05. | Accepted |
| D-037 | Block 06 candidates must remain `pending_risk_template` and cannot assign risk templates. | Accepted |
| D-038 | Block 06 does not register candidates, run quality gates, close candidates, or prepare dossier handoff. | Accepted |
| D-039 | Strategy candidates composed in Block 06 are conceptual artifacts, not validated or profitable strategies. | Accepted |
| D-040 | Block 06 creates synthetic mockups and tests only; it does not create backtests, PnL, performance claims, sizing, capital allocation, or execution. | Accepted |
| D-041 | Block 06 V1 permits multi-rule composition only when all rules share the same source hypothesis, signal definition, and regime context frame. | Accepted |
| D-042 | Cross-hypothesis, cross-signal, or cross-regime candidate composition is deferred beyond Block 06 V1. | Accepted |

## Block 07 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-043 | Risk templates must reference valid strategy candidates from Block 06 with status `pending_risk_template`. | Accepted |
| D-044 | Risk templates in Block 07 are conceptual and must remain explicitly uncalibrated. | Accepted |
| D-045 | Risk templates declare governance dimensions only and do not define capital allocation, position sizing, stop loss, take profit, leverage, or execution controls. | Accepted |
| D-046 | Risk template assignment does not register, quality-approve, validate, close, or hand off a candidate. | Accepted |
| D-047 | Block 07 creates synthetic mockups and tests only; it does not create backtests, PnL, risk calibration, safety claims, or trading approval. | Accepted |
| D-048 | `draft` and `composed` candidate statuses are reserved or deferred and remain disabled in the current V1 flow. | Accepted |
| D-049 | Risk templates must carry falsification references for governance consistency with prior Strategy Engine artifacts. | Accepted |
