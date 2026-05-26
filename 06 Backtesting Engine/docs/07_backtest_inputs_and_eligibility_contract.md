# 07 Backtest Inputs And Eligibility Contract

## Purpose

Block 02 defines the formal entry contract for 06 Backtesting Engine.

Its purpose is to decide whether a StrategyDossier from 05 Strategy Engine is sufficiently complete, traceable, governed, and internally coherent for 06 to consider historical evaluation.

This contract controls the risk of spending effort on data snapshots, temporal admissibility, operationalization, or simulation for a dossier that is missing essential governance evidence, lacks traceability, contains unresolved contradictions, or cannot be evaluated without inventing strategic content.

Block 02 occurs before every later technical activity. It does not inspect performance, create data snapshots, certify temporal admissibility, operationalize rules, define execution assumptions, calculate metrics, or run simulations.

## Conceptual Flow

1. StrategyDossier received from 05 Strategy Engine.
2. Input validation checks minimum required information.
3. Eligibility assessment checks integrity, traceability, governance completeness, and candidate clarity.
4. Eligibility decision is issued.
5. Eligible dossiers may proceed to Block 03.
6. Rejected dossiers receive auditable feedback without upstream mutation.

## Required Input

The only conceptual input to Block 02 is a StrategyDossier produced by 05 Strategy Engine.

The expected upstream dossier status is `dossier_prepared_pending_final_audit`, or another status later accepted by a formal 06 input contract. This status is necessary context, not proof of edge, performance validation, trading authorization, paper trading authorization, deployment approval, or capital allocation approval.

At minimum, the StrategyDossier must contain enough governed information to identify and review:

- Candidate identity.
- Candidate version or equivalent versioning metadata.
- Hypothesis traceability.
- Evidence references.
- Strategy rationale.
- Conceptual rule definitions.
- Regime context references where applicable.
- Risk template reference.
- Falsification criteria.
- Quality gate or closure metadata from 05.
- Governance metadata, including source records and handoff status.
- Known limitations or unresolved assumptions.

This document defines required information, not executable schemas.

## Minimum Eligibility Requirements

A StrategyDossier is eligible only when all minimum requirements are satisfied:

| Requirement | Reason |
| --- | --- |
| Dossier is identifiable. | 06 must know which dossier is being reviewed and must be able to reference it in future audit records. |
| Dossier is versioned. | 06 must bind eligibility to a stable dossier version before downstream work begins. |
| Candidate is clearly defined. | 06 must know what candidate is being evaluated. Ambiguous candidate identity makes later evaluation non-reproducible. |
| Hypothesis traceability is present. | 06 must preserve the chain from 04 hypothesis governance through 05 strategy construction. |
| Evidence references are present. | 06 must be able to trace the candidate back to governed research context without independently rediscovering evidence. |
| Rationale is documented. | 06 must understand the candidate's strategic thesis before deciding whether it can enter historical evaluation. |
| Conceptual rules are present. | 06 must have enough rule framing to determine whether later operationalization is possible. |
| Falsification criteria are present. | 06 must preserve what would challenge or invalidate the candidate. |
| Risk template reference is present. | 06 must preserve upstream risk framing even though live risk parameters are not calibrated in 05. |
| Governance metadata is present. | 06 must confirm the dossier came through the required upstream governance path. |
| Known limitations are recorded. | 06 must distinguish acknowledged limitations from missing or silently assumed information. |
| No unresolved internal contradiction blocks interpretation. | 06 cannot evaluate a dossier whose candidate, rules, rationale, or governance records conflict in material ways. |

## Non-Rejection Criteria

Block 02 must not reject a StrategyDossier only because it does not contain final operational parameters.

05 Strategy Engine deliberately does not calibrate:

- Final stop loss.
- Final take profit.
- Final leverage.
- Final position sizing.
- Final capital allocation.
- Final operational thresholds.
- Final maximum holding periods.
- Execution assumptions.
- Fee assumptions.
- Slippage assumptions.
- Liquidity assumptions.

If later simulation requires these elements, they belong to 06 experimental assumptions in later blocks. Their absence is not an eligibility failure in Block 02.

## Performance Independence

Eligibility is independent of expected or historical performance.

Block 02 must not use:

- Expected Sharpe.
- Expected returns.
- Expected drawdown.
- Researcher intuition.
- Strategy popularity.
- Preference for a specific strategy family.
- Prior backtest results.
- Optimization potential.

Eligibility depends only on dossier integrity, traceability, governance completeness, candidate clarity, and absence of unresolved contradictions.

## Eligibility Failure Conditions

| Failure Condition | Why It Blocks Eligibility |
| --- | --- |
| Missing hypothesis traceability. | 06 cannot verify the governed origin of the candidate. |
| Missing evidence references. | 06 cannot preserve the research chain from 04 to 05. |
| Missing rationale. | 06 cannot determine what strategic claim is being evaluated. |
| Missing governance metadata. | 06 cannot confirm the dossier came through an approved upstream process. |
| Missing falsification criteria. | 06 cannot later evaluate whether the thesis was challenged or invalidated. |
| Ambiguous candidate definition. | 06 cannot reproducibly identify what candidate would be evaluated. |
| Incomplete dossier. | 06 cannot proceed when required information is absent or materially incomplete. |
| Unresolved internal contradiction. | 06 cannot choose between conflicting upstream statements or silently repair them. |
| Upstream status not accepted. | 06 cannot accept a dossier that has not reached a future contract-approved 05 handoff status. |
| Material strategic content requires invention. | 06 cannot infer, invent, or rewrite missing hypothesis, rationale, rules, or candidate definition. |

## Eligibility Decision States

The initial conceptual decision states are:

| State | Meaning |
| --- | --- |
| `eligible_for_backtest_evaluation` | The dossier satisfies Block 02 input and eligibility requirements and may proceed to Block 03. |
| `not_eligible_missing_information` | Required dossier information is absent or materially incomplete. |
| `not_eligible_missing_traceability` | Required hypothesis, evidence, candidate, or upstream governance traceability is missing. |
| `not_eligible_governance_failure` | Required upstream status, closure, handoff, or governance metadata is absent or invalid. |
| `not_eligible_candidate_ambiguity` | The candidate cannot be identified or interpreted deterministically. |
| `not_eligible_internal_inconsistency` | The dossier contains unresolved contradictions that block interpretation. |
| `not_eligible_other` | The dossier fails for a documented reason not covered by the initial states. |

These names are conceptual for Block 02 and may be formalized later as schemas, validators, registries, or tests.

## Eligibility Review Process

The review process must be deterministic and reproducible:

1. Confirm that the input is a StrategyDossier from 05.
2. Confirm accepted upstream dossier status.
3. Confirm dossier identity and version metadata.
4. Confirm candidate identity and candidate clarity.
5. Confirm traceability to hypothesis and evidence references.
6. Confirm rationale, conceptual rules, risk template reference, and falsification criteria.
7. Confirm governance metadata and known limitations.
8. Check for unresolved internal contradictions.
9. Issue exactly one eligibility decision state.
10. Record decision evidence and feedback if rejected.

The reviewer must not inspect expected performance, prior backtest results, or optimization outcomes when making the eligibility decision.

## Governance Rules

06 must not modify the dossier.

06 must not correct the dossier.

06 must not infer missing information.

06 must not invent hypotheses.

06 must not invent evidence references.

06 must not invent conceptual rules.

06 must not rewrite the candidate.

06 must not convert missing strategic content into 06 assumptions.

06 may only accept or reject eligibility and record the decision.

## Feedback Requirements

When a dossier is rejected, 06 must produce auditable feedback containing:

- Dossier identifier and version, if available.
- Eligibility decision state.
- Rejection reason.
- Evidence of the problem.
- Required upstream clarification or remediation topic.
- Statement that 06 did not modify upstream artifacts.

Feedback is a governed handoff to the owning upstream process. It is not a patch, correction, or mutation of 04 or 05 records.

## Decision Logging Requirements

Every eligibility decision must be logged in a future audit-ready record that includes:

- Review timestamp or review version marker.
- Dossier identifier.
- Dossier version.
- Upstream status reviewed.
- Reviewer or process identifier, when formalized.
- Eligibility decision state.
- Requirement checks performed.
- Rejection reasons, if any.
- Feedback handoff reference, if any.
- Confirmation that no performance criteria were used.

Block 02 defines these logging requirements conceptually. It does not create executable schemas or registries.

## Relationship With Block 03

Block 03 only receives dossiers with `eligible_for_backtest_evaluation`.

Block 03 does not re-evaluate eligibility. It assumes Block 02 is the authority for entry into the historical data and feature snapshot contract.

If Block 03 discovers that eligibility was based on incorrect or incomplete information, the evaluation must stop and return to Block 02 or upstream governance rather than silently continuing.

## Explicit Non-Scope

Block 02 does not create historical snapshots, temporal controls, simulation logic, metrics, risk models, frictions, operationalization, execution assumptions, walk-forward protocols, backtests, paper trading, live trading, deployment approvals, or schemas executable by software.
