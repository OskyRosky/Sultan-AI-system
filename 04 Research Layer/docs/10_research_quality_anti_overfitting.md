# Research Quality And Anti-overfitting

## Concept

Research Quality / Anti-overfitting defines controls that prevent weak, unstable, or cherry-picked evidence from being promoted to strategy candidates.

Research quality is a minimum methodological review layer for structured hypotheses and findings. It evaluates whether evidence is sufficiently documented, scoped, and guarded against common research failure modes before any future strategy research discussion.

Passing quality gates does not imply edge. Passing quality gates does not imply profitability. Passing quality gates does not imply a valid strategy.

## Evidence Robustness Boundary

A finding can be well-structured but still not robust. Quality review checks whether required evidence, scope, limitations, caveats, and methodological warnings are present. It does not prove causality, economic significance, or future performance.

Quality review is not backtesting, not strategy validation, not trading approval, and not alpha confirmation.

## Required Controls

The quality framework must address:

- Minimum sample size.
- Multiple testing.
- Temporal stability.
- Economic significance.
- Statistical significance where appropriate.
- Robustness across assets and timeframes.
- Data leakage and lookahead prevention.
- Cherry-picking controls.
- Reproducibility.

## Minimum Quality Gates

Block 10 implements explicit in-memory gates:

- Sample quality:
  - minimum sample count;
  - insufficient sample detection;
  - sample scope presence.
- Temporal quality:
  - temporal instability warnings;
  - concentrated-period warnings.
- Regime quality:
  - regime concentration warnings;
  - sparse regime evidence warnings.
- Statistical quality:
  - weak IC warnings;
  - missing metrics warnings;
  - pooled-only warnings;
  - excessive NaN warnings.
- Governance quality:
  - missing limitations;
  - missing caveats;
  - missing falsification logic;
  - invalid lifecycle state.

## Default Thresholds

Initial thresholds are conservative diagnostics, not proof rules:

- `minimum_sample_count = 30`
- `weak_ic_abs_threshold = 0.03`
- `max_nan_ratio = 0.20`
- `max_regime_concentration = 0.80`
- `max_period_concentration = 0.80`
- `minimum_regime_sample_count = 10`

These thresholds are quality warnings and failures for review routing. They do not produce trading conclusions.

`MIN_CORRELATION_PAIRS = 5` remains a diagnostic calculation minimum for IC/correlation, not strong statistical inference.

## Multiple Testing And Cherry-picking

Feature research often scans many features, horizons, assets, timeframes, regimes, and windows. This creates false positive risk. Block 10 flags missing multiple-testing control metadata, but it does not implement a complete inferential framework yet.

Cherry-picking risk appears when evidence depends on one horizon, one period, one regime, one feature variant, or one small segment. Quality Gates surface this as warnings or failures; they do not automatically reject every such finding.

## Pooled IC Limitation

Pooled IC can be dominated by a specific period, regime, or cluster of observations. It does not replace IC time-series, ICIR, t-statistics, confidence intervals, or out-of-sample validation. Findings that only provide pooled IC receive a warning.

## Temporal And Regime Risk

Temporal instability means evidence may be episodic rather than durable. Regime dependency means evidence may exist only in one context segment. Both risks must be documented before future strategy research considers the evidence.

## Interpretation Boundary

Passing a research quality gate does not mean a strategy is profitable. It only means the evidence is sufficiently structured and controlled for human review and possible future research.

Block 10 does not create BUY/SELL signals, strategies, backtests, PnL, Sharpe, Sortino, Calmar, ML, optimization, causal inference, automatic promotion, deployment approval, or production readiness.

## Status

Specified and implemented in Block 10 as a pure in-memory quality engine with synthetic tests.
