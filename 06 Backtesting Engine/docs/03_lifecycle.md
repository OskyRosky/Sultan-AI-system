# 03 Backtesting Lifecycle

## Status

This lifecycle is conceptual for Block 01. Later blocks may formalize these states as schemas, contracts, tests, registries, or executable validation rules.

## Initial States

| State | Meaning |
| --- | --- |
| `backtest_stage_initialized` | 06 architecture exists as a documented stage. No execution capability is implied. |
| `eligible_for_operationalization` | A StrategyDossier has passed future 06 eligibility checks and may proceed toward temporal and operational review. |
| `not_eligible` | A StrategyDossier cannot enter 06 evaluation under the current eligibility contract. |
| `temporally_certified` | The data and feature snapshot has passed temporal admissibility and leakage baseline controls. |
| `temporal_integrity_failed` | The snapshot, features, timestamps, or availability assumptions fail temporal integrity controls. |
| `operationalized` | The StrategyDossier has been translated into a simulation specification with explicit 06 assumptions. |
| `not_operationalizable` | The dossier cannot be converted into an honest simulation specification without unjustified material invention. |
| `protocol_frozen` | The experiment and evaluation protocol has been defined before result inspection. |
| `simulation_executed` | A historical simulation has run under approved contracts. No favorable result is implied. |
| `falsified` | The evaluation met predefined falsification criteria. |
| `inconclusive` | The evaluation did not support a clear falsification or robustness judgment. |
| `not_robust` | Results were materially unstable, fragile, cost-sensitive, regime-dependent, or otherwise failed robustness checks. |
| `robust_pending_review` | Results passed defined robustness checks but still require governance review. No trading authorization is implied. |
| `closed_with_feedback` | The evaluation is closed and feedback has been recorded for governed handoff to 04 and 05. |

## Lifecycle Notes

`simulation_executed` does not imply a favorable result, valid edge, robustness, approval, paper trading authorization, live trading authorization, deployment readiness, or capital allocation.

`operationalized` means the dossier has a historically evaluable specification. It does not mean the strategy is approved, profitable, validated, or eligible for trading.

`protocol_frozen` means the evaluation plan was fixed before observing results. This status exists to reduce outcome-driven changes, comparison switching, and parameter mining.

`robust_pending_review` means the historical result passed the defined robustness checks for that protocol. It does not authorize trading, paper trading, deployment, leverage, or capital allocation.

## Blocking Conditions

If eligibility fails, the lifecycle must stop at `not_eligible`.

If temporal integrity fails, the lifecycle must stop at `temporal_integrity_failed` until the data and feature issues are resolved through governed upstream processes.

If operationalization requires unjustified assumptions, the lifecycle must stop at `not_operationalizable`.

If the protocol is changed after result inspection, the evaluation must be treated as compromised unless a future governance process explicitly restarts and re-freezes the protocol.
