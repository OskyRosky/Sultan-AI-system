# 23 Strategy Composition Contract

## Purpose

This contract defines the minimum structure and validation rules for Strategy Composition in Block 06.

It depends on Block 05 Rule Construction and must not bypass it.

## Strategy Candidate Fields

A strategy candidate must include:

- `candidate_id`
- `rule_definitions`
- `composition_summary`
- `composition_rationale`
- `assumptions`
- `limitations`
- `conflict_notes`
- `falsification_references`
- `audit_reference`
- `status`
- `created_at`

## Candidate Status

Initial status values:

- `draft`
- `composed`
- `pending_risk_template`

Block 06 may produce only `pending_risk_template` candidates. That status means the candidate is structurally composed and awaits Block 07. It does not mean registry approval, quality approval, validation, or readiness for trading.

## Origin Rules

1. A strategy candidate must contain at least one valid `RuleDefinition`.
2. Each rule definition must validate under Block 05.
3. A candidate cannot originate directly from evidence, findings, hypotheses, signals, or regime context frames.
4. A candidate cannot assign risk templates.
5. A candidate cannot self-register in a registry.
6. A candidate cannot mark itself as quality-approved, validated, profitable, deployable, or tradeable.

## Required Governance Fields

Every valid strategy candidate must include:

- non-empty composition summary;
- non-empty composition rationale;
- non-empty assumptions;
- non-empty limitations;
- non-empty falsification references;
- non-empty audit reference.

## Explicit Prohibitions

The Strategy Composition Layer must not define:

- risk templates;
- candidate registry entries;
- quality gate results;
- backtests;
- PnL;
- drawdown;
- hit rate;
- Sharpe, Sortino, Calmar, or return metrics;
- position sizing;
- capital allocation;
- stop loss;
- take profit;
- leverage;
- order routing;
- exchange connectivity;
- execution logic.

## Relationship With Future Blocks

Block 07 assigns risk templates.

Block 08 registers candidates.

Block 09 evaluates quality gates.

Block 10 closes candidates internally.

Block 11 prepares dossier handoff.

Block 06 does not perform any of those responsibilities.
