# 00 Backtesting Engine Overview

## Definition

06 Backtesting Engine is the governed historical evaluation layer for StrategyDossiers prepared by 05 Strategy Engine.

It exists to evaluate strategy candidates under reproducible historical simulation controls, not to discover strategies, approve trading, operate live systems, or confirm edge from isolated positive results.

## Problem Solved

The system needs a disciplined boundary between a conceptual strategy candidate and any empirical claim about how that candidate would have behaved historically.

06 solves this by defining the contracts, lifecycle, assumptions, simulation governance, diagnostic responsibilities, robustness checks, and closure records required before historical results can be treated as auditable evidence.

## Upstream Input From 05

The expected upstream input is a StrategyDossier produced by 05 Strategy Engine.

The dossier is a governed documentation package. It may contain strategic intent, traceability, rule framing, regime context, risk template references, falsification criteria, quality gate status, closure records, and handoff metadata.

It is not proof of edge, not performance validation, not backtesting authorization, not paper trading authorization, and not live trading authorization.

## Outputs

In future blocks, 06 may produce:

- Backtest eligibility decisions.
- Historical data and feature snapshot contracts.
- Temporal admissibility certifications or failures.
- Operationalization specifications with explicit experimental assumptions.
- Frozen experiment protocols.
- Simulated execution and risk assumption records.
- Historical simulation outputs.
- Performance diagnostics.
- Robustness and falsification assessments.
- Results registry records.
- Governed feedback handoff to 04 Research Layer and 05 Strategy Engine.

## Non-Outputs

06 does not produce:

- Real orders.
- Live trades.
- Paper trading authorization.
- Deployment authorization.
- Capital allocation approval.
- Confirmed edge.
- Guaranteed future performance.
- Silent modifications to upstream research or strategy artifacts.
- LLM-directed trade decisions.
- Reinforcement learning policies.

## Guiding Principles

Data-first: every evaluation must depend on explicit, reproducible historical data and feature snapshots.

Research-first: historical evaluation must preserve the upstream research and strategy thesis instead of rewriting it after seeing results.

Risk-first: risk and exposure assumptions must be explicit before results are interpreted.

Audit-first: every input, assumption, version, decision, and result must be traceable.

Governance-first: movement through 06 must occur through documented contracts and lifecycle decisions.

Temporal integrity-first: no result is admissible if its data, features, rules, or assumptions rely on unavailable future information.

## Current Project Condition

The project does not yet contain real approved evidence from 04, real approved findings, real approved hypotheses, real StrategyDossiers derived from governed candidates, confirmed edge, or validated strategies.

Therefore, 06 can be designed architecturally now, but future execution against real candidates depends on governed outputs from 04 and 05.
