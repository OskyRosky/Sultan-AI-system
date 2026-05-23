# 14 Input Eligibility Rules

## Purpose

This document defines the eligibility rules that protect 05 Strategy Engine from consuming incomplete, non-admissible, or non-auditable research outputs.

Eligibility is a governance decision. It is not a signal, rule, strategy candidate, backtest result, edge claim, or trading approval.

## Mandatory Rules

1. Evidence alone does not create a signal.
2. Evidence alone is not eligible for strategy design.
3. A finding without admissible 04 source status cannot feed strategy design.
4. A finding without linked evidence cannot feed strategy design.
5. A hypothesis without admissible 04 source status cannot feed strategy design.
6. A hypothesis without falsification criteria cannot feed strategy design.
7. A hypothesis with incomplete traceability cannot feed strategy design.
8. Every eligible input must have an audit reference.
9. Every eligible input must declare limitations.
10. Every eligible input must preserve source context from 04.
11. Eligibility never implies edge.
12. Eligibility never implies profitable performance.
13. Eligibility only permits later conceptual signal and rule design inside 05.

## Approval Boundary

Eligible for strategy design is not the same as:

- approved for trading;
- approved for deployment;
- approved as alpha;
- validated as profitable;
- validated by historical simulation.

## Source Status Translation

04 Research Layer retains its own lifecycle states. 05 Strategy Engine stores those states as `source_status` and interprets them inside the Strategy Inputs Contract.

Admissible source statuses for 05 eligibility evaluation:

- Hypothesis: `promoted_for_strategy_review`.
- Finding: `promoted_to_quality_review`.
- Evidence: no source status is sufficient by itself.

No 04 status is interpreted as edge, profitability, trading approval, or deployment approval.

## Rejection Reasons

An input must be rejected or marked ineligible when:

- source status is not admissible for the input type;
- traceability is incomplete;
- audit reference is missing;
- limitations are missing;
- falsification criteria are missing for a hypothesis;
- a finding is not linked to evidence;
- the source layer is not 04 Research Layer;
- the input tries to bypass Research Closure or quality governance.

## Evidence Rule

Research evidence is admissible context only. It may support a finding or hypothesis, but it cannot directly authorize future signals, rules, candidates, or trading logic.

## Finding Rule

A finding may become eligible only when its 04 source status is `promoted_to_quality_review`, it is linked to evidence, scoped, limited, and auditable.

Findings do not require hypothesis `falsification_criteria`. That requirement applies only to hypotheses.

## Hypothesis Rule

A hypothesis may become eligible only when its 04 source status is `promoted_for_strategy_review`, it is linked to evidence and optionally findings, falsifiable, limited, auditable, and traceable.

## No Strategy Leakage

The eligibility layer must not include strategy scoring, entry logic, exit logic, invalidation logic, position sizing, portfolio construction, or execution assumptions.
