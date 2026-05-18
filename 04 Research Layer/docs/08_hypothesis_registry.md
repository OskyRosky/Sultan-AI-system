# Hypothesis Registry

## Concept

The Hypothesis Registry records research hypotheses in a structured, auditable form.

It is a registry, not an automated hypothesis generator.

The correct research chain is:

```text
quantitative evidence -> candidate hypothesis -> human review -> possible future promotion
```

The prohibited chain is:

```text
LLM -> invented hypothesis -> automatic strategy
```

A research hypothesis is an explicit, falsifiable statement about a possible relationship suggested by observational evidence. It is not proof, not edge, not a signal, and not a strategy.

## Hypothesis Versus Strategy

A hypothesis states what might be true and what evidence would be needed to reject or continue investigating it.

A strategy defines operational trading behavior: entries, exits, sizing, portfolio logic, execution, and performance evaluation. Those are outside the Hypothesis Registry.

`promoted_for_strategy_review` means the hypothesis can be reviewed by humans for possible later strategy research. It does not mean approved for trading.

## Evidence Versus Proof

Evidence is observational and conditional. It can support a hypothesis candidate, but it does not prove causality, profitability, robustness, or tradability.

Hypotheses may later be rejected when new evidence, temporal validation, regime analysis, multiple-testing controls, or human review fails to support them.

## Schema

Each hypothesis record must include:

- `hypothesis_id`
- `title`
- `description`
- `rationale`
- `related_features`
- `related_horizons`
- `related_regimes`
- `evidence_summary`
- `evidence_source`
- `assumptions`
- `falsification_conditions`
- `status`
- `created_at`
- `updated_at`
- `notes`

List fields must be typed as lists of non-empty strings. `evidence_source` must be structured metadata, not free-floating narrative. Timestamps must be valid and `updated_at` must not precede `created_at`.

## Status Lifecycle

Allowed statuses:

- `draft`
- `proposed`
- `rejected`
- `archived`
- `promoted_for_strategy_review`

Disallowed statuses include:

- `approved_for_trading`
- `live_strategy`
- `deploy_ready`

Lifecycle transitions are registry state changes only. They do not create findings, signals, strategies, backtests, or automated promotion.

## Validation Rules

The registry must validate:

- required fields are present;
- `hypothesis_id` is unique within a registry;
- required text fields are non-empty;
- `status` is one of the allowed statuses;
- list fields are lists of non-empty strings;
- `evidence_source` is non-empty structured metadata;
- `falsification_conditions` are present;
- timestamps are valid and ordered.

## Methodological Rationale

The registry exists to prevent narrative drift and hindsight fitting. Hypotheses should be traceable to evidence, assumptions, and falsification criteria before any future strategy research begins.

Human review is mandatory. The registry can structure and validate records, but it cannot decide that a hypothesis is true, profitable, or deployable.

## Risks

Main risks:

- hypothesis overfitting;
- narrative fitting after seeing metrics;
- treating rankings or IC values as automatic hypotheses;
- converting observational evidence into causal claims;
- promoting hypotheses without falsification criteria;
- confusing research governance with strategy approval.

## Boundary

Hypotheses must not be invented automatically by an LLM. An LLM may help draft wording, but the hypothesis must be grounded in economic logic, documented assumptions, and quantitative evidence requirements.

Block 8 does not create hypotheses automatically, use LLMs, generate findings, create signals, create strategies, run backtests, calculate PnL, train ML models, optimize parameters, select features automatically, score hypotheses automatically, or promote hypotheses automatically.

## Status

Specified and implemented in Block 8 as a pure in-memory registry with synthetic tests. No real hypotheses are registered.
