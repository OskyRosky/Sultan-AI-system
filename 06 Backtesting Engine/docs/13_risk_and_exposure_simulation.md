# 13 Risk And Exposure Simulation

## Purpose

Block 08 defines the Risk & Exposure Simulation contract for 06 Backtesting Engine.

Its purpose is to govern how an experiment represents exposure, sizing, capital allocation, leverage, concentration, and portfolio constraints in a consistent, reproducible, and audit-ready way.

This block answers the question: how should the risk assumed by a strategy be represented during historical evaluation?

Risk simulation is exposure realism.

It is not alpha creation. It is not performance enhancement. It is not optimization. It is not result repair. It is not robustness validation.

Risk assumptions exist to represent plausible exposure constraints and uncertainty. They must never be selected or tuned to make a strategy appear better.

## Risk Simulation Philosophy

Strategy signals describe intent.

Execution models describe realizability.

Risk simulation describes exposure.

A strategy may generate an entry, exit, or allocation signal, and execution modeling may define whether that action could be filled under market frictions. Risk simulation governs the exposure that the historical evaluation is allowed to assume after those prior controls are fixed.

Risk simulation exists to represent constraints and uncertainty. It does not exist to improve performance, rescue weak strategies, hide drawdowns, retrofit sizing, or manufacture attractive outcomes.

If a risk assumption systematically improves expected results, it is suspicious and requires explicit justification. If the justification is unavailable or weak, the assumption must be rejected or replaced with a more conservative alternative.

## Exposure Governance Framework

Every exposure configuration must be explicit, versioned, traceable, and audit-ready.

The minimum conceptual components are:

- Capital base.
- Position sizing assumptions.
- Exposure limits.
- Leverage assumptions.
- Allocation assumptions.
- Concentration constraints.
- Portfolio constraints.

No exposure assumption may be implicit.

No exposure assumption may be hidden.

No exposure assumption may be treated as neutral merely because it is absent.

## Risk Assumption Framework

Every risk assumption must record:

- Identifier.
- Description.
- Rationale.
- Source.
- Classification.
- Expected effect.
- Review status.
- Traceability to protocol, strategy specification, assumptions registry, execution configuration, or risk governance reference.

Risk assumptions are protocol assumptions. They are not outcomes. They must be defined before simulation and before result inspection.

Risk assumptions must remain consistent with the Strategy Specification, frozen protocol, execution configuration, and prior assumptions registry. They must not create new strategy logic or repair operationalization, protocol, or execution defects.

Risk governance references must be identified by name, version or date, source, and retrieval or publication timestamp when available. External references must be frozen by citation metadata at the time the assumption is registered.

## Position Sizing Governance

Position sizing governs how a signal or strategy state is translated into simulated exposure size.

Sizing is not proof of edge. It is not performance interpretation. It is not an optimizer. It is not a mechanism for rescuing a weak strategy.

Rules:

- Sizing assumptions must be documented.
- Sizing assumptions must be versioned.
- Sizing assumptions must be traceable.
- Sizing changes create new experiments.
- Sizing assumptions cannot be selected after observing results.
- Sizing assumptions cannot be tuned to improve observed results.
- Absence of sizing assumptions is itself a risk assumption.

If sizing is absent, fixed, simplified, or delegated to a later process, that condition must be explicitly recorded and justified.

## Portfolio Constraint Governance

A portfolio constraint is any rule that limits or shapes the set of positions, assets, exposures, or allocations permitted in the historical evaluation.

Conceptual examples include:

- Maximum positions.
- Minimum positions.
- Asset eligibility constraints.
- Allocation limits.
- Diversification requirements.
- Exposure caps by asset, group, venue, strategy sleeve, or portfolio segment.

Block 08 does not define numbers or concrete portfolio configurations.

Portfolio constraints must be explicit and traceable. They must not be hidden inside simulation defaults, execution mechanics, or later risk interpretation.

Asset eligibility constraints must not silently reduce the effective trading universe below the Block 03 snapshot universe certified by Block 04.

Any more restrictive eligibility constraint requires justification independent of observed results. If eligibility constraints change the effective universe, they must be recorded as material risk or protocol assumptions. If they create selection leakage risk, the process must fail or return upstream.

## Exposure Limit Governance

Exposure limits define the maximum or minimum exposure that may be represented in the historical evaluation.

They may conceptually apply to gross exposure, net exposure, asset-level exposure, strategy-level exposure, portfolio-level exposure, or other governed exposure dimensions.

Rules:

- Exposure limits must be documented.
- Exposure limits must be versioned.
- Exposure limits must be traceable.
- Limit changes create new experiments.
- Limits cannot be tuned to improve results.
- Absence of exposure limits is an exposure assumption.

If no exposure limits are applied, the audit trail must explicitly record that assumption and its rationale. It must not be treated as a neutral default.

## Concentration Governance

Concentration describes how much simulated exposure can be concentrated in one asset, group, venue, signal, strategy component, or portfolio segment.

Concentration is not performance interpretation. It is not a metric calculation. It is not robustness validation.

Rules:

- Concentration assumptions must be documented.
- Concentration assumptions must be traceable.
- Concentration assumptions must be versioned.
- Unrealistic concentration assumptions are prohibited.
- The system must not assume unconstrained concentration without explicit declaration.

An assumption that exposure may concentrate without limit must be treated as suspicious and cannot be accepted unless explicitly declared, justified, and carried into later review.

## Capital Allocation Governance

Capital allocation governs how simulated capital is assigned across positions, assets, strategy components, sleeves, or portfolio segments.

Capital allocation is not an outcome. It is not performance interpretation. It is not proof of strategy quality.

Rules:

- Allocation assumptions must be documented.
- Allocation assumptions must be versioned.
- Allocation assumptions must be traceable.
- Allocation changes create new experiments.
- Allocation assumptions cannot be retroactively modified.
- Allocation assumptions cannot be selected after observing results.

Capital allocation choices are protocol assumptions, not outcomes.

The capital base assumption must explain its relationship to intended strategy scale. If capital scale is arbitrary for backtesting, it must be explicitly declared.

Leverage interpretation must be consistent with the capital base definition. Changing capital base creates a new experiment if it affects exposure interpretation.

## Leverage Governance

Leverage is the assumption that simulated exposure may exceed the relevant capital base or otherwise use borrowed, synthetic, derivative, or margin-enabled exposure.

Leverage is not proof of edge. It is not risk approval. It is not production leverage authorization. It is not a post-hoc performance amplifier.

Rules:

- Leverage assumptions must be documented.
- Leverage assumptions must be traceable.
- Leverage assumptions must be versioned.
- Leverage changes create new experiments.
- Leverage assumptions cannot be selected after observing results.
- Leverage assumptions cannot be tuned to improve results.
- Absence of leverage constraints is itself a leverage assumption.

If leverage is unconstrained, unavailable, capped, disallowed, or simplified, the audit trail must explicitly record the assumption and rationale.

## Risk Mark-To-Market Timing Governance

Risk mark-to-market timing must be consistent with execution fill timing assumptions.

For example, if fills occur at next bar open, risk exposure calculations during the prior bar must reflect the pending nature of the order rather than assume the fill already occurred.

Any mismatch between fill timing and risk exposure timing must be documented or treated as a failure condition.

## Conservative Risk Principle

When multiple risk assumptions are plausible and evidence is insufficient to prefer one, the protocol must prefer the assumption less likely to overstate risk-adjusted performance.

Conservative risk assumptions reduce optimism bias. They do not guarantee validity.

Conservatism must be documented. A conservative risk assumption still requires traceability, rationale, versioning, and audit evidence.

## Risk Change Governance

A material risk change is any modification that could alter simulated exposure, sizing, leverage, allocation, concentration, portfolio eligibility, or constraint behavior.

Examples include changes to:

- Position sizing assumptions.
- Leverage assumptions.
- Exposure limits.
- Concentration assumptions.
- Capital allocation rules.
- Portfolio constraints.
- Capital base assumptions.

Material risk changes create new experiments. They never overwrite prior evidence.

If a risk assumption is changed because an earlier configuration was defective, the prior configuration must remain auditable and must be marked according to future governance rather than silently replaced.

## Failure Conditions

Block 08 must stop the process before simulation when any of the following are confirmed or cannot be resolved:

- Undocumented risk assumptions.
- Hidden sizing assumptions.
- Missing sizing assumption or missing explicit no-sizing assumption.
- Missing exposure limit assumption or missing explicit no-limit assumption.
- Missing leverage assumption or missing explicit leverage-constraint assumption.
- Untraceable exposure constraints.
- Inconsistent leverage assumptions.
- Unrealistic concentration assumptions.
- Unconstrained concentration without explicit declaration.
- Protocol ambiguity.
- Versioning failures.
- Risk mark-to-market timing inconsistent with execution fill timing.
- Undocumented mismatch between fill timing and risk exposure timing.
- Asset eligibility constraints silently reduce the certified snapshot universe.
- Eligibility constraints create selection leakage risk.
- Risk assumptions contradict the Strategy Specification.
- Risk assumptions contradict the frozen protocol.
- Risk assumptions contradict the execution configuration.
- Risk assumptions selected after observing results.
- Risk assumptions tuned using observed results.
- Risk assumptions systematically improve expected performance without explicit justification.
- Material risk changes attempt to overwrite prior experiment evidence.
- Risk configuration attempts to repair operationalization, protocol, or execution defects.

If a failure condition occurs, the simulation must not execute.

## Audit Trail Requirements

Every risk and exposure configuration must leave auditable evidence.

The audit trail must include:

- Experiment identifier.
- Protocol version.
- Execution configuration reference.
- Risk configuration identifier and version.
- Exposure configuration.
- Capital base assumption.
- Position sizing assumptions, including explicit no-sizing assumptions if applicable.
- Leverage assumptions, including explicit no-leverage-constraint assumptions if applicable.
- Allocation assumptions.
- Concentration assumptions.
- Portfolio constraints.
- Exposure limits, including explicit no-limit assumptions if applicable.
- Reviewer or process identifier, when formalized.
- Deviations.
- Rationale.
- Source references.
- External reference citation metadata, including name, version or date, source, and retrieval or publication timestamp when available.
- Expected effect.
- Version history.
- Failure findings, if any.
- Risks found.
- Risks reviewed and cleared.
- Categories reviewed and marked not applicable.
- Unresolved categories.
- Confirmation that no formulas, mathematical models, VaR, CVaR, Kelly, risk parity, optimizer, portfolio optimizer, sizing engine, robustness framework, drawdown analysis, performance interpretation, metrics, PnL, or result inspection occurred in Block 08.

The audit trail must be sufficient for quant research governance, model risk management, internal audit, trading systems engineering, reproducibility review, and external technical due diligence.

## Relationship With Block 09

Block 09 receives:

- Experiment outputs from Block 08, meaning the governed risk and exposure configuration, not interpreted performance.
- Execution configuration.
- Risk configuration.
- Risk assumptions.
- Risk audit trail.
- Protocol metadata.
- Assumptions context.

Block 09 may execute a reproducible historical simulation only within the boundaries of the frozen protocol, governed execution configuration, and governed risk configuration.

Before Block 09 may execute simulation, it must validate the integrated assumption set from:

- Block 05 strategy and operationalization assumptions.
- Block 06 protocol assumptions.
- Block 07 execution assumptions.
- Block 08 risk assumptions.

This validation must verify no contradictions, no duplicate or conflicting assumptions, timing consistency, ownership clarity, version completeness, traceability completeness, and interaction risks.

Block 09 must not:

- Change sizing.
- Change leverage.
- Change allocation assumptions.
- Modify concentration assumptions.
- Modify portfolio constraints.
- Modify exposure limits.
- Reinterpret risk assumptions.
- Repair risk defects.
- Convert optimistic risk assumptions into accepted simulation behavior.
- Change execution assumptions.
- Change the protocol.

If Block 09 detects risk modeling problems, it must return the process to Block 08. It must not repair risk defects downstream.

## Governance Requirements

Block 08 must preserve:

- Temporal certification from Block 04.
- Strategy specification from Block 05.
- Frozen protocol from Block 06.
- Execution configuration from Block 07.
- Assumptions registry and traceability records.
- Experiment identity and versioning.
- Prior experiment records.

Block 08 must not authorize trading, paper trading, deployment, live execution, broker connectivity, capital allocation, production risk controls, leverage approval, or edge claims.

## Risk Integrity Principle

Risk assumptions exist to represent plausible exposure conditions, not to manufacture attractive outcomes.

When exposure realism and result attractiveness conflict, exposure realism takes precedence.

The system must reject optimistic risk assumptions rather than accept inflated evidence.

## Explicit Non-Scope

Block 08 does not create formulas.

Block 08 does not create mathematical models.

Block 08 does not create VaR.

Block 08 does not create CVaR.

Block 08 does not create Kelly sizing.

Block 08 does not create risk parity.

Block 08 does not create an optimizer.

Block 08 does not create a portfolio optimizer.

Block 08 does not create a sizing engine.

Block 08 does not create robustness testing.

Block 08 does not create drawdown analysis.

Block 08 does not interpret performance.

Block 08 does not execute simulations.

Block 08 does not calculate metrics.

Block 08 does not calculate PnL.

Block 08 does not create trades.

Block 08 does not create SQL.

Block 08 does not create executable schemas.

Block 08 does not create Python code.

Block 08 is a documentation and conceptual governance block that defines how exposure realism and risk assumptions must be governed before historical simulation execution.
