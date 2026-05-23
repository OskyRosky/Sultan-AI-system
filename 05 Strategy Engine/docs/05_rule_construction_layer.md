# 05 Rule Construction Layer

## Purpose

The Rule Construction Layer frames candidate entry, exit, invalidation, and filtering logic at a conceptual level.

## Rule Classes

Future rule definitions may include:

- Entry rules.
- Exit rules.
- Invalidation rules.
- Filtering rules.
- Conflict resolution rules.

## Optimization Warning

Rule construction must not become disguised optimization. Rules should be justified by governed research context and risk constraints, not tuned to maximize historical performance inside 05.

## Explicit Non-Scope

This layer does not:

- Run parameter searches.
- Tune thresholds against PnL.
- Calculate performance.
- Select rules based on Sharpe, Sortino, Calmar, or return metrics.
- Trigger trades.
