# 04 Interfaces With Strategy Engine

## Expected Input

The expected upstream input from 05 Strategy Engine is a StrategyDossier.

The initial expected status is `dossier_prepared_pending_final_audit`, or another status later approved by a formal 06 input eligibility contract.

This status means the dossier is prepared for future governed evaluation. It does not mean the strategy has confirmed edge, validated performance, calibrated risk, backtesting authorization, paper trading authorization, live trading authorization, deployment approval, or capital allocation approval.

## Preserved 05 Content

06 must preserve:

- Source research references.
- Hypothesis and finding traceability.
- Signal definitions.
- Regime context framing.
- Rule framing.
- Risk template references.
- Falsification criteria.
- Quality gate records.
- Strategy closure records.
- Dossier handoff metadata.
- Upstream statuses and limitations.

06 may reference, evaluate, and challenge these elements, but it must not silently mutate them.

## What 05 Does Not Calibrate

05 Strategy Engine deliberately does not provide final calibrated operational values for:

- Trading thresholds.
- Position sizing.
- Stop loss.
- Take profit.
- Maximum holding periods.
- Leverage.
- Capital allocation.
- Execution assumptions.
- Fee assumptions.
- Slippage assumptions.
- Liquidity assumptions.
- Production risk controls.

06 must not treat the absence of these values as a defect in 05. They belong to downstream historical evaluation assumptions and future risk or execution governance.

## 06 Experimental Assumptions

When simulation requires operational details not supplied by 05, 06 may add experimental assumptions only if they are:

- Explicit.
- Versioned.
- Justified.
- Traceable.
- Separated from original 05 content.
- Frozen according to the experiment protocol before results are inspected.
- Reviewed under future robustness and falsification controls.

These assumptions must be labeled as 06 assumptions, not retroactive 05 claims.

## Not Operationalizable

If a dossier cannot be simulated without inventing material assumptions that are unjustified, untraceable, or thesis-changing, the correct outcome is `not_operationalizable` or an equivalent future formal status.

In that case, 06 must not run a simulation. It should record the reason and provide governed feedback.

## Feedback To 04 And 05

06 feedback may include:

- Operationalization gaps.
- Temporal admissibility failures.
- Data or feature availability issues.
- Strategy specification ambiguities.
- Falsification outcomes.
- Robustness failures.
- Sensitivity to assumptions, frictions, regimes, or costs.
- Suggested upstream review topics.

Feedback is a governed handoff. It is not direct mutation of 04 Research Layer or 05 Strategy Engine artifacts.

## Upstream Non-Mutation Rule

06 does not modify upstream documents, statuses, decisions, hypotheses, findings, candidates, risk templates, quality gates, closure records, or StrategyDossiers. Any upstream change must happen through the owning stage's governance process.
