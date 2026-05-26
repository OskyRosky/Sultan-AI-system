# 16 Robustness Falsification And Anti Overfitting Framework

## Purpose

Block 11 defines the Robustness, Falsification & Anti-Overfitting Framework for 06 Backtesting Engine.

Its purpose is to govern how measured results from Block 10 are challenged before they can be treated as credible historical evidence.

This block answers the question: can the measured result survive governed attempts to refute it?

It does not answer whether the strategy has edge, whether the strategy should be deployed, whether capital should be allocated, or whether the result will persist.

A profitable backtest is not evidence of edge.

Block 11 exists to attempt to show that:

- The result may be spurious.
- The result may be overfit.
- The result may depend on a specific window.
- The result may depend on a specific partition.
- The result may depend on a specific configuration.
- The result may depend on a specific friction assumption.
- The result may disappear under reasonable perturbations.

Block 11 does not try to confirm edge. Block 11 tries to refute edge.

## Robustness Framework Objective

The robustness framework defines governed challenge categories that test whether a measured result is fragile to reasonable changes in conditions, assumptions, windows, partitions, frictions, risk settings, benchmarks, universes, or regimes.

Robustness precedes confidence.

Robustness testing cannot create alpha.

Robustness testing cannot repair strategy defects, protocol defects, execution defects, risk defects, data defects, simulation defects, or metric defects.

More tests do not automatically create stronger evidence. A large set of poorly governed or selectively reported challenges may increase overfitting risk rather than reduce it.

Challenges must be defined before observing challenge outcomes whenever possible. Post-outcome challenge selection must be treated as suspect and must be explicitly documented.

Materiality thresholds or qualitative materiality criteria must be predefined per challenge category before challenges are executed. Post-outcome materiality threshold selection is prohibited.

If materiality criteria are missing for an affected challenge category, that category cannot support `robust_result`. Depending on severity, the correct classification is `inconclusive_result` or `challenge_failure`.

## Falsification Framework Objective

The falsification framework governs how predefined failure criteria are applied to measured results.

Falsification criteria must come from:

- StrategyDossier.
- Research Layer.
- Assumptions Registry.

Block 11 must verify consistency between those criteria and the operationalized specification, frozen protocol, simulation outputs, and Block 10 metrics.

Block 11 must not invent falsification criteria after observing results.

Assumptions Registry entries may serve as falsification criteria only if they were explicitly designated as falsification criteria when created or approved upstream. Block 11 cannot retroactively select assumptions as falsification criteria. Trivial or non-substantive assumptions cannot substitute for StrategyDossier falsification criteria.

Block 11 must not redefine the hypothesis, edge, strategy, candidate, benchmark, protocol, execution assumptions, risk assumptions, simulation outputs, or metrics.

Failure to falsify is not proof.

Survival of challenge is not validation.

A strategy that survives testing is merely less refuted under the reviewed challenge set.

## Terminology Boundaries

Validation is a governance conclusion that a model or strategy is acceptable for a defined purpose under defined standards. Block 11 does not grant validation.

Verification confirms that an artifact followed its governing specification. Block 11 may check whether robustness and falsification review followed the framework, but it does not verify implementation correctness through executable tests in this block.

Robustness describes whether measured results remain materially similar under governed challenge conditions. Robustness does not prove edge.

Falsification attempts to reject the strategy thesis or measured evidence using predefined criteria. Falsification is a challenge process, not a confirmation process.

Confirmation is a claim that evidence supports a thesis. Block 11 does not issue confirmation.

Confidence is a later governance posture informed by accumulated evidence, limitations, and challenge outcomes. Block 11 may reduce uncertainty by documenting survival of challenge, but it does not create confidence by itself.

## Result Classifications

`robust_result` means the measured result survived the predefined robustness challenge scope without material fragility findings. It does not prove edge, validation, deployment readiness, or future profitability.

`fragile_result` means the measured result materially deteriorated, changed interpretation, or became unstable under one or more governed challenge categories.

`non_falsified_result` means the predefined falsification criteria did not reject the result or thesis under the reviewed evidence. It is not proof that the thesis is true.

`falsified_result` means predefined falsification criteria were met and the result or thesis failed the governed challenge.

`overfit_result` means the evidence indicates dependence on excessive tuning, repeated selection, favorable experiment survival, narrow partitions, benchmark shopping, regime shopping, parameter fishing, or narrative fitting.

`inconclusive_result` means the challenge evidence is insufficient, contradictory, incomplete, or unresolved and cannot support a clear robustness, falsification, or overfitting classification.

These classifications are governance outcomes. They are not deployment decisions, trading approvals, capital allocation approvals, or production risk approvals.

Final classification must obey these mappings:

- `robust_result` maps to lifecycle state `robust_pending_review`.
- `fragile_result` maps to lifecycle state `not_robust`.
- `falsified_result` maps to lifecycle state `falsified`.
- `overfit_result` maps to lifecycle state `overfit_detected`.
- `inconclusive_result` maps to lifecycle state `inconclusive`.

`overfit_result` is blocking. It cannot transition to `robust_pending_review`. It must be registered downstream as overfitting evidence and may trigger feedback handoff, but never promotion.

Confirmed experiment shopping, favorable selection from a larger unfavorable or inconclusive experiment family, or primary result survival from mostly unfavorable variants blocks `robust_result`. The permitted classifications are `overfit_result`, `inconclusive_result`, or `fragile_result`, depending on severity.

Predefined challenge outcomes dominate post-outcome challenge outcomes. A failed predefined challenge cannot be overridden by a favorable post-outcome challenge. Post-outcome challenges cannot convert `fragile_result` or `falsified_result` into `robust_result` or `inconclusive_result`.

Core challenge failures dominate peripheral challenge successes. If any core challenge category fails materially, the result cannot be `robust_result`.

Core categories include, at minimum:

- Temporal robustness.
- Regime robustness.
- Partition robustness.
- Assumption robustness.
- Falsification criteria.

Peripheral categories may inform review but cannot override core failures. Mixed outcomes must map to `fragile_result`, `inconclusive_result`, or `not_robust` depending on severity and lifecycle usage.

## Robustness Categories

Robustness categories define conceptually what may be challenged.

Minimum categories include:

- Temporal robustness.
- Partition robustness.
- Execution robustness.
- Friction robustness.
- Risk robustness.
- Benchmark robustness.
- Assumption robustness.
- Parameter robustness.
- Universe robustness.
- Regime robustness.

These categories are conceptual. Block 11 does not implement walk-forward procedures, Monte Carlo procedures, bootstrap procedures, statistical tests, optimization logic, parameter search, hyperparameter tuning, or executable robustness checks.

Each robustness category must define:

- Reviewed artifact references.
- Challenge rationale.
- Predefined challenge scope.
- Predefined challenge depth.
- Predefined materiality threshold or qualitative materiality criteria.
- Expected relationship to the original experiment.
- Required lineage references.
- Allowed interpretation boundaries.
- Failure or fragility conditions.

Selective robustness testing is prohibited. Categories cannot be added, removed, emphasized, or suppressed because their outcomes are favorable or unfavorable.

Each challenge category must have predefined scope and depth. Trivial or superficial challenges cannot be treated as equivalent to rigorous challenges. Depth differences must be visible, justified, and recorded in the audit trail.

Categories marked `not_applicable` require positive justification from StrategyDossier content or frozen protocol scope. A `not_applicable` marking cannot be based on expected weakness, expected adverse outcome, or post-outcome convenience. It must be verifiable without referencing challenge outcomes. Questionable `not_applicable` classification leads to `inconclusive_result` or `robustness_review_failed`, depending on severity.

## Challenge Selection Governance

Predefined challenge outcomes dominate post-outcome challenge outcomes.

Post-outcome challenges are supplementary only. They may help understand failure mechanisms, but they cannot contradict, dilute, offset, neutralize, or compensate for adverse findings from predefined challenges.

A failed predefined challenge cannot be overridden by a favorable post-outcome challenge.

Post-outcome challenges cannot upgrade classification. They cannot convert `fragile_result`, `falsified_result`, or `overfit_result` into `robust_result` or `inconclusive_result`.

Challenge selection must preserve the original challenge scope. Adding favorable post-outcome challenges after adverse findings is evidence of narrative fitting unless separately justified as failure analysis.

## Falsification Criteria Governance

Falsification criteria must be predefined and traceable.

Accepted sources are:

- StrategyDossier falsification criteria.
- Research Layer evidence or hypothesis records.
- Assumptions Registry entries closed before downstream evaluation.

Block 11 may evaluate whether criteria are applicable, internally consistent, and traceable. It may not create new criteria to fit observed results.

StrategyDossier falsification criteria are presumed applicable.

Block 11 cannot unilaterally declare StrategyDossier falsification criteria inapplicable.

Inapplicability is allowed only if:

- The criterion itself explicitly defines non-applicability conditions.
- The process returns to the StrategyDossier owner or upstream governance for formal resolution.

If applicability is disputed, Block 11 must emit `falsification_applicability_disputed` or `robustness_review_failed` and stop review until the owning upstream process resolves the dispute.

Applicability disputes cannot be resolved by Block 11 alone. A criterion that would falsify the result cannot be bypassed by declaring it inapplicable post hoc.

Assumptions Registry entries may serve as falsification criteria only if explicitly designated as falsification criteria when created or approved upstream. Block 11 cannot retroactively select assumptions as falsification criteria after observing results.

If falsification criteria are absent, ambiguous, contradictory, or untraceable, Block 11 cannot close as a valid falsification review.

If predefined falsification criteria conflict with the operationalized specification or assumptions registry, Block 11 must document the conflict and return the process to the owning prior block.

## Anti-Overfitting Governance

Anti-overfitting governance controls attempts to transform repeated historical evaluation into apparent evidence.

Block 11 must explicitly review for:

- P-hacking.
- Data snooping.
- Parameter fishing.
- Repeated experiment selection.
- Benchmark shopping.
- Regime shopping.
- Survivorship of successful experiments.
- Narrative fitting.
- Selective robustness reporting.
- Abandoned unfavorable variants.

Passing many tests does not prove edge.

A strategy that survives many related tests may still be overfit if the tests were selected, repeated, narrowed, or narrated after observing outcomes.

Anti-overfitting review must examine experiment lineage, assumptions lineage, benchmark lineage, protocol lineage, and robustness variant lineage. It must not focus only on the surviving favorable result.

If Block 11 confirms experiment shopping or favorable selection from a larger unfavorable or inconclusive experiment family, the result cannot be classified as `robust_result`.

Favorable primary result selected from a mostly unfavorable experiment family is evidence of overfitting or result shopping, not robustness.

Experiment family distribution must affect the final classification. Documentation alone is not enough to neutralize experiment shopping.

## Multiple Experiment Governance

Block 11 must preserve visibility across experiment families.

Governed experiment review must include:

- Experiment families.
- Experiment lineage.
- Superseded experiments.
- Abandoned experiments.
- Robustness variants.
- Failed robustness variants.
- Inconclusive robustness variants.
- Successor and predecessor references.
- Distribution of outcomes across the experiment family.
- Ratio of favorable, unfavorable, and inconclusive outcomes.
- Assessment of whether the distribution suggests experiment shopping.

Selective presentation of favorable robustness outcomes is prohibited.

Superseded and abandoned experiments remain part of the evidentiary record. They must not be hidden because they weaken the narrative.

If multiple experiment variants exist for the same StrategyDossier, snapshot, protocol family, or assumption set, Block 11 must assess whether favorable outcomes are being selected from a larger family of unfavorable or inconclusive attempts.

Confirmed experiment shopping blocks `robust_result`.

`Robustness variant` means a challenge inside predefined scope, using the same snapshot, same operationalization, same protocol family, and same assumptions except the specific governed perturbation.

`New experiment` means any change requiring a different snapshot, different protocol, different benchmark, different evaluation window, different operationalization, or material assumption change.

New experiments must enter experiment family lineage. They cannot be hidden as robustness variants.

Block 11 must verify that primary experiment designation was timestamped before simulation or result inspection. If the primary experiment designation timestamp is missing, Block 11 must classify the review as `inconclusive_result` or `challenge_failure`, depending on severity.

Returns from Block 11 to prior blocks must be counted over the same StrategyDossier, snapshot, and experiment family. Repeated returns are evidence of systematic search or governance instability.

Return-loop control:

- First return is allowed with documented reason.
- Second return is allowed only with explicit escalation note.
- Third return blocks further iteration and requires governance review before any new experiment can proceed.

Returns cannot be used to tune assumptions until robustness passes. Return history must be included in the audit trail and downstream Results Registry handoff.

## Robustness Failure Governance

Robustness failures must be documented, classified, and escalated.

Conceptual failure categories include:

- `robustness_failure`
- `falsification_failure`
- `challenge_failure`
- `evidence_of_fragility`

`robustness_failure` means one or more governed challenge categories show material instability or fragility.

`falsification_failure` means predefined falsification criteria were met or falsification review could not be validly completed due to missing or inconsistent criteria.

`challenge_failure` means the challenge process itself failed because required artifacts, scope, lineage, or audit evidence were missing or invalid.

`evidence_of_fragility` means challenge outcomes indicate dependence on narrow assumptions, windows, regimes, benchmarks, parameters, universes, frictions, or risk settings.

`core_fragility` means fragility appears in a core challenge category such as temporal robustness, regime robustness, partition robustness, assumption robustness, or falsification criteria.

`protocol_fragility` means fragility appears because the result depends on protocol choices such as windows, partitions, benchmark identity, or experiment family selection.

When these appear, Block 11 does not correct the result. It documents, classifies, and may return the process to the relevant prior block.

Block 11 must not repair measured performance, modify metrics, alter simulation outputs, change protocol, tune assumptions, or redesign the strategy.

Returns from Block 11 must remain correction routing, not optimization routing. Iterative returns must follow the return-loop control defined in Multiple Experiment Governance.

## Boundary With Block 10

Block 11 consumes metrics, diagnostics, benchmark comparisons, warning records, failure records, lineage metadata, and performance audit trail artifacts from Block 10.

Block 11 must not:

- Modify metrics.
- Recalculate metrics.
- Rewrite diagnostics.
- Reinterpret metrics to hide unfavorable results.
- Alter simulation outputs.
- Create missing performance artifacts.
- Replace benchmark comparisons.
- Change metric definitions.
- Selectively suppress Block 10 warnings or failures.

If Block 11 detects metric defects, it must return the process to Block 10 or the relevant upstream block. It must not repair metrics inside robustness review.

Metric defect means a verifiable implementation or calculation error under the metric methodology already approved by Block 10.

Methodology disagreement is not a metric defect. Block 11 cannot return to Block 10 merely because it prefers another methodology. Methodology concerns must be recorded as limitations or inconclusive evidence, not recalculated inside Block 11.

## Boundary With Block 12

Block 12 receives:

- Robustness outcomes.
- Falsification outcomes.
- Anti-overfitting findings.
- Fragility findings.
- Experiment family lineage.
- Challenge audit trail.
- Escalation and return decisions.
- Audit conclusions.

Block 12 must not rewrite Block 11 outcomes.

Block 12 may register, close, or route the evaluation according to governed results registry rules. It may not convert fragile, falsified, overfit, or inconclusive results into validated evidence.

Routing may only:

- Register the final result with Block 11 classification intact.
- Return to Block 11 for review defect correction.
- Create governed feedback handoff.

Routing cannot convert `overfit_result`, `falsified_result`, `fragile_result`, or `inconclusive_result` into `robust_pending_review`.

If Block 12 detects defects in robustness, falsification, anti-overfitting review, lineage, or audit evidence, it must return the process to Block 11 or the relevant prior block.

## Audit Trail Requirements

Every Block 11 review must leave auditable evidence.

The audit trail must include:

- Reviewer identity or process identity, when formalized.
- Reviewed artifacts.
- Block 10 metric and diagnostic references.
- Block 09 simulation references.
- Protocol lineage references.
- Assumptions registry references.
- Robustness categories reviewed.
- Categories reviewed and cleared.
- Categories reviewed with findings.
- Categories reviewed and marked not applicable.
- Positive justification for every `not_applicable` category.
- Predefined challenge scope for each category.
- Predefined challenge depth for each category.
- Predefined materiality threshold or qualitative materiality criteria for each category.
- Falsification criteria used.
- Falsification criteria source references.
- Falsification criteria applicability determinations.
- Applicability disputes and upstream resolution references.
- Experiment family references.
- Robustness variant references.
- Superseded experiment references.
- Abandoned experiment references.
- Experiment family outcome distribution.
- Primary experiment designation timestamp.
- Fragility findings.
- Challenge outcomes.
- Distinction between predefined challenge outcomes and post-outcome challenge outcomes.
- Core versus peripheral challenge outcome aggregation.
- Anti-overfitting review findings.
- Rationale.
- Escalation decisions.
- Returns to previous blocks.
- Return count and return-loop escalation status.
- Unresolved categories.
- Confirmation that no optimization, parameter search, hyperparameter tuning, machine learning validation logic, statistical test implementation, Monte Carlo implementation, bootstrap implementation, walk-forward implementation, robustness execution, falsification execution, simulation execution, metric recalculation, or strategy redesign occurred in Block 11.

Decision D-038 applies explicitly: the audit trail must document both findings and reviewed categories without findings.

The audit trail must be sufficient for quant research governance, model risk management, internal audit, trading systems engineering, reproducibility review, and external technical due diligence.

## Stop Conditions

Block 11 cannot close when any of the following are confirmed or cannot be resolved:

- Falsification criteria are absent.
- Falsification criteria are untraceable.
- Falsification criteria are contradictory.
- Falsification criterion applicability is disputed and not formally resolved upstream.
- Block 11 attempts to declare a StrategyDossier falsification criterion inapplicable without criterion-defined conditions or upstream owner resolution.
- A falsification criterion that would fail the result is declared inapplicable post hoc.
- Experiment lineage is unavailable.
- Experiment family references are missing.
- Superseded or abandoned experiments are hidden.
- Confirmed experiment shopping is presented as robustness.
- Favorable primary result is selected from a mostly unfavorable or inconclusive experiment family and still presented as `robust_result`.
- Primary experiment designation timestamp is missing.
- Assumptions registry is incomplete.
- Assumptions Registry entries are retroactively selected as falsification criteria.
- Robustness scope is undefined.
- Challenge scope or challenge depth is undefined.
- Materiality criteria are missing for core challenge categories.
- Robustness categories are selectively chosen after outcomes are known.
- Post-outcome challenges are used to dilute, offset, or neutralize adverse predefined findings.
- Core challenge failures are overridden by peripheral successes.
- `not_applicable` challenge category markings lack positive, verifiable, non-result-based justification.
- New experiments are hidden as robustness variants.
- Return-loop count reaches the third return without governance review.
- Unresolved upstream defects exist.
- Block 10 metrics are missing, inconsistent, or invalid.
- Block 09 simulation outputs are missing, inconsistent, or invalid.
- Protocol lineage is unavailable.
- Contradictory evidence is unresolved.
- Challenge outcomes cannot be traced to reviewed artifacts.
- Audit trail lacks reviewed-and-cleared categories.
- Block 11 attempts to optimize, repair, rerun, recalculate, or redesign.

If a stop condition occurs, Block 11 must not issue a completed robustness review. It must document the condition and return the process to the owning prior block where applicable.

## Governance Requirements

Block 11 must preserve:

- Strategy intent from Block 05.
- Frozen protocol and experiment lineage from Block 06.
- Execution assumptions from Block 07.
- Risk assumptions from Block 08.
- Simulation artifacts from Block 09.
- Metrics and diagnostics from Block 10.
- Assumptions registry and traceability records.
- Experiment family lineage and superseded experiment references.

Block 11 must not authorize trading, paper trading, deployment, live execution, broker connectivity, capital allocation, production risk controls, leverage approval, edge claims, validation claims, or future profitability claims.

## Robustness Integrity Principle

The purpose of robustness, falsification, and anti-overfitting review is to challenge evidence, not to promote it.

When attractive interpretation and challenge integrity conflict, challenge integrity takes precedence.

The system must reject selective or non-traceable robustness narratives rather than accept a persuasive but overfit performance story.

## Explicit Non-Scope

Block 11 does not create code.

Block 11 does not create SQL.

Block 11 does not create notebooks.

Block 11 does not create metrics.

Block 11 does not create statistics.

Block 11 does not create formulas.

Block 11 does not calculate Sharpe.

Block 11 does not calculate Sortino.

Block 11 does not execute backtests.

Block 11 does not execute simulations.

Block 11 does not perform optimization.

Block 11 does not perform machine learning.

Block 11 does not perform parameter search.

Block 11 does not perform hyperparameter tuning.

Block 11 does not implement walk-forward testing.

Block 11 does not implement Monte Carlo testing.

Block 11 does not implement bootstrap testing.

Block 11 does not implement statistical hypothesis tests.

Block 11 does not execute robustness testing.

Block 11 does not execute falsification testing.

Block 11 is a documentation and conceptual governance block that defines how measured historical evidence must be challenged before results are registered and closed by Block 12.
