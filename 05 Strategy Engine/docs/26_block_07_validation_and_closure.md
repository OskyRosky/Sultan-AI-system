# 26 Block 07 Validation And Closure

## Scope Completed

Block 07 creates Risk Template assignment as an auditable conceptual layer.

It defines:

- risk template structure;
- conceptual risk dimensions;
- required candidate origin;
- uncalibrated-only status;
- required governance fields;
- synthetic mockups;
- unit tests.

## Validation Intent

Validation proves only that risk templates are assigned to valid pending-risk-template candidates and remain constrained to Block 07 scope. It does not validate real risk, safety, robustness, profitability, or strategy quality.

## Expected Test Coverage

The Block 07 tests must show that:

- a valid risk template can be assigned to a valid `pending_risk_template` candidate;
- non-candidate origins are rejected;
- candidates not pending risk template are rejected;
- empty risk dimensions are rejected;
- invalid risk dimensions are rejected;
- unsupported calibration status is rejected;
- required constraint intent, assumptions, limitations, falsification references, non-calibrated rationale, and audit references are enforced;
- the risk template preserves the candidate -> rule -> regime -> signal -> hypothesis chain;
- risk templates do not expose registry status, quality gate status, backtests, PnL, performance metrics, position sizing, capital allocation, stop loss, take profit, leverage, orders, or execution fields.

## Closure Conditions

Block 07 is closed when:

- the risk template contract is documented;
- implementation is covered by tests;
- every risk template is constrained to a valid `pending_risk_template` candidate;
- every risk template remains explicitly uncalibrated;
- no real risk parameters are created;
- no registry, quality gates, closure, dossier, backtesting, PnL, performance metrics, execution, or data integration are created;
- 04 Research Layer is not modified.

## Non-Edge Statement

No risk template created under this block confirms edge, profitability, safety, robustness, tradability, deployability, or execution readiness.
