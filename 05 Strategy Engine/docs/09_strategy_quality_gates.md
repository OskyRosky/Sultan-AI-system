# 09 Strategy Quality Gates

## Purpose

Strategy Quality Gates define whether a registered conceptual candidate is sufficiently coherent, traceable, constrained, and testable to proceed to future Strategy Closure review.

Quality Gates operate only on a valid `StrategyCandidateRegistryEntry` from Block 08 with status `registered_pending_quality_gates`.

They are structural governance checks. They are not empirical validation and do not demonstrate edge, profitability, robustness, safety, or trading readiness.

## Required Origin

The required flow is:

```text
Eligible Hypothesis Decision -> SignalDefinition -> RegimeContextFrame -> RuleDefinition -> StrategyCandidate -> RiskTemplate -> Registry Entry -> Quality Gate Assessment
```

Quality Gates cannot originate directly from evidence, findings, hypotheses, signals, regime frames, rules, candidates, or risk templates outside the Registry contract.

## Gate Themes

Quality gates should evaluate:

- Maximum acceptable complexity.
- Traceability to governed 04 artifacts.
- Evidence governance readiness.
- Explicit assumptions and limitations.
- Structural overfitting risk.
- Rule clarity.
- Risk template completeness.
- Falsification readiness.
- Explicit non-performance scope.

## Block 09 Gate Types

The initial gate set is:

- `traceability`
- `governance_fields`
- `structural_complexity`
- `evidence_governance_readiness`
- `risk_template_completeness`
- `falsification_readiness`
- `non_performance_scope`

Every assessment must include all gate types.

## Assessment Status

Block 09 allows only derived assessment statuses:

- `passed_pending_strategy_closure`
- `failed_requires_revision`

`passed_pending_strategy_closure` means the conceptual registry entry may later be reviewed by Block 10. It does not mean closure, dossier readiness, backtest authorization, trading approval, or validated strategy status.

## Complexity

Candidate design should avoid unnecessary degrees of freedom. Complexity must be justified before downstream testing.

## Structural Overfitting

Quality gates must challenge candidates that appear shaped around expected historical performance, excessive filters, brittle thresholds, or unstated optimization.

## Explicit Non-Scope

Quality gates do not:

- validate profitability;
- confirm edge;
- assert empirical robustness;
- close a candidate;
- prepare dossier handoff;
- authorize backtesting;
- approve deployment;
- authorize trading;
- calculate return, PnL, drawdown, hit rate, Sharpe, Sortino, Calmar, or other performance statistics;
- assign capital, sizing, stops, targets, leverage, or execution settings.
