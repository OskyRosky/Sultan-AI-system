# 10 Strategy Operationalization And Simulation Specification

## Purpose

Block 05 defines the Strategy Operationalization & Simulation Specification contract for 06 Backtesting Engine.

Operationalization is the governed translation of a valid StrategyDossier into a historically evaluable simulation specification. It converts conceptual strategy intent into explicit evaluable rules while preserving the original strategic thesis, rationale, candidate definition, traceability, and falsification criteria.

Operationalization is translation, not invention.

This block exists because a StrategyDossier from 05 Strategy Engine may contain rationale, evidence references, candidate definition, conceptual rules, falsification criteria, governance metadata, and conceptual risk framing without containing every operational detail needed for historical evaluation.

The risk controlled by this block is unauthorized strategy creation inside 06: changing the thesis, adding new signals, inventing material parameters, optimizing decisions, resolving ambiguities by convenience, or disguising 06-generated experimental assumptions as if they were governed outputs of 05.

Block 05 occurs after Block 04 because only temporally certified snapshots may be operationalized. Temporal admissibility, lookahead review, leakage review, feature timing review, and availability-at-decision-time review are upstream prerequisites and are not reimplemented here.

Block 05 occurs before Block 06 because the experiment protocol can be frozen only after the strategy specification, assumptions registry, traceability mapping, and operationalization decision are closed.

## Operationalization Concept

Operationalization transforms governed conceptual strategy material into a simulation specification that later blocks can evaluate.

It may clarify how existing dossier content maps to historical evaluation mechanics. It may identify operational gaps. It may define explicit 06-generated experimental assumptions where those assumptions are justified, traceable, and do not alter strategic intent.

It must not create a new strategy. It must not optimize parameters. It must not calibrate for performance. It must not introduce edge. It must not repair an under-specified StrategyDossier by inventing material logic.

When preserving strategic intent and making evaluation possible are in conflict, preservation of intent takes precedence.

## StrategyDossier Interpretation Rules

The StrategyDossier is authoritative for the strategy candidate under review.

The dossier is governed, traceable, and upstream-owned by 05 Strategy Engine. 06 may interpret it for historical evaluation, but 06 must not silently rewrite it, correct it, expand it, or change its meaning.

Operationalization must preserve:

- Candidate identity.
- Candidate version.
- Hypothesis traceability.
- Evidence references.
- Strategy rationale.
- Conceptual rule definitions.
- Regime context.
- Risk template reference.
- Falsification criteria.
- Known limitations.
- Governance metadata.

Dossier meaning must not drift during operationalization. If a rule can be interpreted in multiple materially different ways, Block 05 must record the ambiguity instead of choosing the interpretation most convenient for simulation.

## Operationalization Boundary

Block 05 may:

- Map conceptual rules into evaluable rules.
- Identify missing operational elements.
- Define explicit experimental assumptions owned by 06.
- Document interpretation decisions.
- Create a simulation specification for later blocks.
- Create an assumptions registry.
- Create traceability records linking operational rules to dossier content or 06 assumptions.
- Issue an operationalization decision state.

Block 05 must not:

- Redesign the candidate.
- Introduce new signals.
- Change the rationale.
- Replace the hypothesis.
- Modify strategic intent.
- Optimize parameters.
- Perform parameter search.
- Calibrate to results.
- Alter falsification criteria.
- Resolve material ambiguity by invention.
- Create experiment protocols, walk-forward rules, benchmarks, or splits.
- Define frictions, fees, slippage, fills, or liquidity simulation.
- Define final risk sizing, leverage approval, capital allocation, or production risk controls.
- Run simulations, produce trades, calculate PnL, or calculate metrics.

## Material Vs Non-Material Assumptions

Operationalization must classify every 06-added assumption as material or non-material.

Material assumptions can change strategy behavior, economic exposure, entry or exit timing, risk behavior, trade frequency, holding profile, or interpretation of the strategic thesis.

Examples of material assumptions include:

- Entry thresholds.
- Exit thresholds.
- Leverage.
- Stop loss.
- Take profit.
- Holding periods.
- Execution timing.
- Capital allocation logic.
- Position sizing logic.
- Signal precedence.
- Rule conflict resolution.
- Missing entry or exit condition interpretation.

Non-material assumptions organize or label the specification without changing strategy behavior.

Examples of non-material assumptions include:

- Naming conventions.
- Documentation formatting.
- Stable identifiers.
- Metadata organization.
- Reference ordering.

Material assumptions require special governance. They must be explicit, justified, traceable, and reviewed for whether they preserve strategic intent. If a material assumption would change the strategy rather than operationalize it, the correct result is `not_operationalizable`.

## Assumption Registry

Every assumption added by 06 must be recorded in an assumptions registry.

Each assumption record must include:

- Assumption identifier.
- Description.
- Reason.
- Originating gap.
- Source dossier reference, if any.
- Impact assessment.
- Classification as material or non-material.
- Review status.
- Owner as 06 Backtesting Engine.
- Confirmation that it is not a retroactive output of 05 Strategy Engine.

Assumptions belong to 06. They do not become facts. They do not become upstream Strategy Engine claims. They do not modify the StrategyDossier.

The assumptions registry is an input to Block 06. Block 06 may use the closed registry to freeze an experiment protocol, but it must not add, reinterpret, or modify assumptions.

## Operationalization Review Process

The operationalization review process is conceptual and audit-oriented. It does not create executable schemas, validators, simulation logic, metrics, or code in this block.

1. Confirm that the StrategyDossier passed Block 02 eligibility.
2. Confirm that the bound snapshot passed Block 04 temporal certification or a future formally accepted limitation-bearing equivalent.
3. Review the StrategyDossier without modifying it.
4. Extract operationalizable components from dossier content.
5. Identify missing operational elements.
6. Classify each gap as non-material, material but potentially preservable, or material and thesis-changing.
7. Create the assumptions registry for any 06-added assumption.
8. Evaluate assumption materiality and strategic impact.
9. Map every operationalized rule to dossier content or an assumption record.
10. Determine whether operationalization preserves strategic intent.
11. Issue exactly one operationalization decision state.

The review must not inspect simulation results, optimize parameters, define experiment splits, create benchmarks, model frictions, calculate risk sizing, or run a backtest.

## Operationalization Decision States

The initial conceptual operationalization decision states are:

| State | Meaning |
| --- | --- |
| `operationalized` | The dossier was translated into an evaluable simulation specification without requiring additional assumptions that affect strategic behavior. |
| `operationalized_with_assumptions` | The specification requires explicit 06 assumptions that are registered, justified, traceable, and judged non-material or otherwise non-thesis-changing. |
| `operationalized_with_material_assumptions` | The specification requires material 06 assumptions that are explicitly registered and judged to preserve strategic intent, but must be carried into later protocol, robustness, and interpretation review. |
| `not_operationalizable` | The dossier cannot be converted into an honest simulation specification without inventing, changing, or materially reinterpreting strategic content. |
| `insufficient_information` | Required operational information is absent and cannot be filled without unjustified assumptions. |
| `strategic_ambiguity_detected` | Multiple materially different interpretations exist and cannot be resolved without changing or inventing strategy logic. |
| `conflicting_rules_detected` | Dossier rules conflict in a way that blocks deterministic operationalization. |

These names are conceptual for Block 05 and may be formalized later as schemas, validators, registries, or tests.

Only successful operationalization states may proceed to Block 06. Failure, ambiguity, insufficiency, or conflicting-rule states must stop the process and produce governed feedback.

## Material Assumption Governance

A material assumption must never be presented as an output of 05 Strategy Engine.

Every material assumption must be labeled as:

`06-generated experimental assumption`

The assumption record must identify:

- Who or what process introduced it, when formalized.
- Why it exists.
- Which StrategyDossier gap required it.
- What uncertainty it creates.
- What risk it introduces.
- Why it is considered compatible with the original strategic intent.
- Whether it must be reviewed in Block 06 protocol design or Block 11 robustness and falsification.

Operationalization does not convert assumptions into facts. A material assumption remains an experimental condition attached to the historical evaluation. It does not validate the strategy, prove edge, or mutate upstream research.

If a material assumption materially changes the candidate, modifies the thesis, replaces missing strategy logic, or introduces a new source of edge, the correct decision is `not_operationalizable`.

## Strategic Ambiguity

Strategic ambiguity exists when dossier content permits multiple materially different operational interpretations.

Examples include:

- Multiple valid interpretations of an entry rule.
- Contradictory rules.
- Unclear entry condition.
- Unclear exit condition.
- Unresolved logical conflict between signal and risk framing.
- Missing rule precedence.
- Unclear regime condition.
- Ambiguous candidate scope.

If ambiguity is non-material and can be resolved by a documented interpretation without changing behavior, it may be registered.

If ambiguity is material, Block 05 must not emit simple `operationalized`. If the ambiguity cannot be resolved honestly without introducing material interpretation, the process must stop with `strategic_ambiguity_detected`, `conflicting_rules_detected`, `insufficient_information`, or `not_operationalizable`.

## Traceability Requirements

Every operationalized rule must have an identifiable origin.

Each rule in the simulation specification must trace to at least one of:

- StrategyDossier section.
- Strategy rationale source.
- Candidate definition.
- Conceptual rule definition.
- Falsification criterion.
- Risk template reference.
- 06 assumption record.

No operationalized rule may appear without traceability.

Traceability records must distinguish original 05 content from 06-generated assumptions. A rule derived from an assumption must reference the assumption identifier and must not be described as if it came directly from the StrategyDossier.

## Assumption Explosion Control

Assumption explosion occurs when operationalization requires so many material assumptions that the resulting specification is primarily constructed by 06 rather than translated from the StrategyDossier.

Assumption explosion is evidence of insufficient operationalizability. It is not justification for additional interpretation.

If the strategy only becomes evaluable after multiple material decisions invented by 06, the correct outcome is `not_operationalizable` or an equivalent failure state.

Block 05 must consider both the number and importance of assumptions. A small number of thesis-changing assumptions can be sufficient to fail operationalization.

## Failure Conditions

Block 05 must stop the process when any of the following are confirmed or cannot be resolved:

- Missing candidate definition.
- Missing rationale needed to preserve strategic intent.
- Missing conceptual rules.
- Missing traceability to dossier content.
- Conflicting rules.
- Material strategic ambiguity.
- Non-traceable operational rule.
- Operational rule appears without dossier source or assumption record.
- Inability to define assumptions honestly.
- Material assumption would change the thesis.
- Material assumption would introduce new edge.
- Assumption explosion.
- Dossier is internally inconsistent.
- Operationalization would alter falsification criteria.
- Operationalization would optimize, calibrate, or select parameters based on expected performance.
- Operationalization requires a new temporal, feature timing, or availability exception not pre-approved by Block 04.

If a failure condition occurs, the process must not advance to Block 06.

## Relationship With Block 06

Block 06 receives:

- Operationalized strategy specification.
- Assumptions registry.
- Operationalization decision.
- Traceability records.
- Registered unresolved limitations that are allowed to proceed under the operationalization decision.

Block 06 may use these artifacts to define the Experiment & Evaluation Protocol before results are inspected.

Block 06 must not:

- Reinterpret the strategy.
- Resolve pending strategic ambiguity.
- Create new assumptions.
- Modify approved assumptions.
- Change strategic intent.
- Add signals.
- Change operational rules.
- Optimize parameters.
- Convert material assumptions into Strategy Engine outputs.

If Block 06 discovers that the specification is incomplete, ambiguous, contradictory, or requires new assumptions, the process must return to Block 05 or upstream governance rather than silently continuing.

Block 06 works on closed specifications. It does not repair operationalization.

## Audit Trail Requirements

Every operationalization decision must leave auditable evidence.

The audit trail must include:

- StrategyDossier identifier and version reviewed.
- Snapshot identifier and temporal certification reference.
- Review timestamp or review version marker.
- Reviewer or process identifier, when formalized.
- Dossier sections reviewed.
- Operationalizable components extracted.
- Gaps identified.
- Assumptions introduced.
- Materiality classification for each assumption.
- Ambiguity findings.
- Conflicting-rule findings.
- Assumption explosion assessment.
- Traceability mapping from operational rules to dossier content or assumption records.
- Operationalization decision state.
- Justification for the decision.
- Feedback handoff reference if operationalization fails.
- Confirmation that no simulation, metrics, PnL, trades, frictions, risk sizing, benchmark selection, walk-forward protocol, optimization, or result inspection occurred in Block 05.

The audit trail must be sufficient for quant research governance, model risk management, internal audit, trading systems engineering, reproducibility review, and external technical due diligence.

## Operationalization Integrity Principle

The purpose of operationalization is to make evaluation possible while preserving strategic intent.

When preserving strategic intent and making evaluation possible are in conflict, preservation of intent takes precedence.

The system must reject operationalization rather than silently transform the strategy.

## Explicit Non-Scope

Block 05 does not create a simulator.

Block 05 does not run historical evaluation.

Block 05 does not calculate metrics.

Block 05 does not calculate PnL.

Block 05 does not create trades.

Block 05 does not define frictions, fees, slippage, liquidity simulation, or fills.

Block 05 does not define risk sizing, leverage approval, capital allocation, or production risk controls.

Block 05 does not create experiment protocols, walk-forward design, benchmarks, splits, or comparison rules.

Block 05 does not optimize parameters.

Block 05 does not perform parameter search.

Block 05 does not create SQL.

Block 05 does not create datasets.

Block 05 does not create executable schemas.

Block 05 does not create Python code.

Block 05 is a documentation and conceptual governance block that defines how a governed StrategyDossier may be translated into a simulation specification without changing the strategy.
