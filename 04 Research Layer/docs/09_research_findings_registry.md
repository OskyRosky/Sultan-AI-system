# Research Findings Registry

## Concept

The Research Findings Registry stores structured findings derived from quantitative analysis.

The correct chain is:

```text
quantitative evidence -> structured finding -> human review -> quality gates -> possible future promotion
```

The prohibited chain is:

```text
interesting number -> edge claim -> automatic strategy
```

A research finding is a documented observation derived from evidence. It is limited by sample, period, features, horizons, regimes, assumptions, and methodology.

A finding is not proof, not causality, not edge, not profitability, not a signal, and not a strategy.

## Finding Versus Hypothesis

Hypothesis:

- investigable idea;
- falsifiable;
- can be draft, proposed, rejected, archived, or promoted for strategy review.

Finding:

- documented observation;
- derived from evidence;
- linked optionally to a hypothesis;
- constrained by sample scope, limitations, and caveats;
- can later be rejected or promoted to quality review.

## Finding Versus Evidence And Proof

Evidence is the quantitative material that supports a finding, such as metrics, sample scope, and methodology metadata.

Proof is not produced by this registry. The registry records evidence and caveats so humans and later Quality Gates can evaluate whether the observation is robust enough to continue.

## Finding Versus Strategy

A finding may inform future research review. It does not define entry rules, exit rules, position logic, sizing, execution, portfolio behavior, or trading approval.

## Required Finding Fields

Each finding must include:

- `finding_id`
- `title`
- `description`
- `linked_hypothesis_id`
- `evidence_summary`
- `supporting_metrics`
- `sample_scope`
- `related_features`
- `related_horizons`
- `related_regimes`
- `limitations`
- `caveats`
- `decision`
- `status`
- `created_at`
- `updated_at`
- `notes`

`supporting_metrics` and `sample_scope` must be structured metadata. They are not proof and must not be interpreted without limitations and caveats.

## Allowed Decisions

Finding decisions are:

- `advance_to_quality_review`
- `defer`
- `reject`
- `needs_more_data`
- `archive`

Disallowed decisions include:

- `trade`
- `deploy`
- `live`
- `buy`
- `sell`
- `production_ready`

## Allowed Statuses

Finding statuses are:

- `draft`
- `observed`
- `under_review`
- `rejected`
- `archived`
- `promoted_to_quality_review`

Disallowed statuses include:

- `approved_for_trading`
- `live_strategy`
- `deploy_ready`
- `profitable`
- `alpha_confirmed`

## Validation Rules

The registry must validate:

- required fields are present;
- `finding_id` is unique within a registry;
- required text fields are non-empty;
- status is valid;
- decision is valid;
- `supporting_metrics` is structured metadata;
- `sample_scope` is structured metadata;
- limitations are present;
- caveats are present;
- list fields contain non-empty strings;
- timestamps are valid and ordered.

## Relationship With Block 10

Block 9 prepares findings for Block 10 Research Quality / Anti-overfitting. A finding promoted to quality review is not accepted as true. It is only queued for further checks such as multiple testing control, temporal robustness review, sample-size review, leakage review, and narrative-fitting review.

## Risks

Main risks:

- narrative fitting after seeing metrics;
- cherry-picking features, horizons, regimes, or periods;
- treating observational evidence as causal truth;
- treating a finding as edge;
- using incomplete sample scope;
- omitting limitations or caveats;
- bypassing Quality Gates.

## Boundary

Findings cannot be invented by an LLM. They must come from quantitative evidence and predefined interpretation rules. No finding is created in Block 1.

Block 9 does not create findings automatically from metrics, use LLMs, approve findings as truth, generate hypotheses, create signals, create strategies, run backtests, calculate PnL, train ML models, optimize parameters, rank findings automatically, or make trading decisions.

## Status

Specified and implemented in Block 9 as a pure in-memory findings registry with synthetic tests. No real findings are registered.
