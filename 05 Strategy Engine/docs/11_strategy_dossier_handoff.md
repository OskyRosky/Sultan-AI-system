# 11 Strategy Dossier Handoff

## Purpose

The Strategy Dossier is the external handoff artifact from 05 Strategy Engine to 06 Backtesting Engine.

In Block 11, handoff means documentation preparation only. It does not execute an operational handoff and does not authorize 06 Backtesting Engine to run.

## Closure vs Dossier

Strategy Closure verifies that the candidate is internally complete.

Strategy Dossier Handoff packages the closed conceptual candidate for future downstream review after final audit.

## Required Origin

A dossier may originate only from a valid `StrategyClosureRecord` with status:

- `closed_pending_dossier_handoff`

The required flow is:

```text
Eligible Hypothesis Decision -> SignalDefinition -> RegimeContextFrame -> RuleDefinition -> StrategyCandidate -> RiskTemplate -> Registry Entry -> Quality Gate Assessment -> Strategy Closure Record -> Strategy Dossier
```

## Handoff Preparation Status

Block 11 permits only:

- `dossier_prepared_pending_final_audit`

This status means the conceptual package has been documented for future review. It does not mean handoff executed, backtesting approved, strategy validated, or trading approved.

## Dossier Contents

A dossier should include:

- Candidate identity and status.
- Source artifact references.
- Signal definitions.
- Regime assumptions.
- Rule framing.
- Risk template.
- Quality gate results.
- Falsification criteria.
- Known limitations.
- Test questions for 06.
- Pending requirements before downstream use.
- Explicit non-approval statement.

## Explicit Non-Scope

The dossier does not include backtest results, PnL, execution reports, live deployment configuration, profitability claims, edge confirmation, capital allocation, or trading approval.

The dossier does not start 06 Backtesting Engine and does not create real integration with PostgreSQL, Parquet, APIs, exchanges, or datasets.
