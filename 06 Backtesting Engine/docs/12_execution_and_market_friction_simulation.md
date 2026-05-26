# 12 Execution And Market Friction Simulation

## Purpose

Block 07 defines the Execution & Market Friction Simulation contract for 06 Backtesting Engine.

Its purpose is to govern how an experiment incorporates market frictions and execution constraints in a consistent, reproducible, conservative, and audit-ready way.

This block answers the question: how should the system model the difference between a theoretical signal and a realistic execution?

Execution realism is evidence hygiene.

It is not alpha generation. It is not optimization. It is not edge creation. It is not result improvement.

Execution assumptions exist to reduce artificially optimistic historical evidence. They must never be selected or tuned to make a strategy appear better.

## Execution Modeling Philosophy

Signals are theoretical.

Execution is realized.

A strategy signal may say that a position should be entered, exited, reduced, or increased. Execution modeling governs whether, when, and under what market-friction assumptions that action could have been represented in historical evaluation.

Backtests that ignore execution assumptions generate incomplete evidence. A result without explicit execution assumptions may be reproducible as a calculation, but it is not execution-realistic evidence.

Execution realism exists to reduce optimism bias. It does not exist to improve results.

## Market Friction Taxonomy

Market friction categories include, at minimum:

- Slippage.
- Transaction costs.
- Spreads.
- Liquidity constraints.
- Delayed fills.
- Partial fills.
- Execution latency.
- Market impact assumptions.
- Venue limitations.
- Trading availability constraints.

This taxonomy is conceptual. Block 07 does not define formulas, numerical parameters, order book models, calibration logic, or concrete execution algorithms.

## Execution Assumption Framework

Every execution assumption must be explicit, versioned, traceable, and audit-ready.

Each execution assumption must record:

- Identifier.
- Description.
- Rationale.
- Source.
- Classification.
- Expected effect.
- Review status.
- Traceability to protocol, strategy specification, snapshot, or external market-structure reference.

Execution assumptions are protocol assumptions. They are not outcomes. They must be defined before execution simulation and before result inspection.

If an execution assumption systematically improves expected performance, it is suspicious and requires explicit justification. If the justification is unavailable or weak, the assumption must be rejected or replaced with a more conservative alternative.

## Fill Model Governance

Fill modeling governs how theoretical orders are represented as simulated historical fills.

Conceptual fill assumptions may include:

- Immediate fills.
- Next bar fills.
- Delayed fills.
- Partial fills.
- No-fill conditions.

Rules:

- Fill assumptions must be explicit.
- Fill assumptions must not be hidden in simulator defaults.
- Fill assumptions must be versioned.
- Fill assumptions must be traceable to the frozen protocol or execution assumption registry.
- Changing fill assumptions creates a new experiment.
- Fill assumptions cannot be selected after observing results.

Fill assumptions are protocol assumptions, not outcomes.

Block 07 does not implement a fill engine. It defines governance for future execution simulation.

## Slippage Governance

Slippage is the modeled difference between the theoretical reference price and the simulated execution price.

Slippage is not a performance adjustment chosen after results are observed. It is not an optimization knob. It is not a mechanism for improving backtest results.

Rules:

- Slippage assumptions must be documented.
- Slippage assumptions must be versioned.
- Slippage assumptions must be traceable.
- Slippage changes create new experiments.
- Slippage assumptions cannot be tuned to improve results.
- Absence of slippage is itself an execution assumption.

If no slippage is modeled, the audit trail must explicitly record that assumption and its rationale. It must not be treated as a neutral default.

## Transaction Cost Governance

Transaction costs are modeled costs associated with simulated trading activity.

They may conceptually include exchange fees, commissions, funding-related costs where applicable, borrow-related costs where applicable, taxes where applicable, and other trade-related cost categories.

Transaction costs are not result interpretation. They are not risk controls. They are not performance metrics.

Rules:

- Cost assumptions must be documented.
- Cost assumptions must be traceable.
- Cost assumptions must be versioned.
- Cost changes create new experiments.
- Costs cannot be omitted silently.
- Ignoring costs is an assumption, not neutrality.

If transaction costs are excluded, the exclusion must be explicitly documented and justified as an execution assumption.

## Liquidity Constraint Governance

A liquidity constraint is any assumption limiting whether a theoretical order could be executed at the desired size, timing, price reference, venue, or market condition.

Liquidity constraints may conceptually relate to volume, order size, market depth, venue availability, asset availability, trading halts, market outages, or historical data limitations.

Rules:

- Liquidity assumptions must be documented.
- Liquidity limitations must be declared.
- Liquidity assumptions must be versioned and traceable.
- Unrealistic liquidity assumptions are prohibited.
- The system must not assume infinite liquidity.

Any assumption that all desired orders can be fully executed without size, venue, volume, or market availability constraints must be treated as suspicious and must not be accepted without explicit justification. If such justification is unavailable, the experiment must fail or use a more conservative assumption.

## Execution Timing Governance

Execution timing governs the relationship between:

- Signal generation time.
- Decision time.
- Order submission assumption.
- Fill timing assumption.

Execution timing must remain consistent with temporal certification.

Block 07 must not:

- Relax temporal restrictions.
- Reintroduce lookahead.
- Reinterpret temporal admissibility.
- Move a decision earlier than permitted by Block 04.
- Use bar-close information before it is available.
- Introduce unapproved intraperiod timing exceptions.

If an execution assumption contradicts Block 04 temporal certification, the process must fail and return to the owning upstream governance step. Block 07 cannot override temporal admissibility.

## Conservative Assumption Principle

When multiple execution assumptions are plausible and evidence is insufficient to prefer one, the protocol must select the assumption that is less likely to overstate performance.

Conservative assumptions reduce optimism bias. They do not guarantee validity.

Conservatism must be documented. A conservative assumption still requires traceability, rationale, versioning, and audit evidence.

## Friction Change Governance

A material friction change is any modification that could alter simulated fills, execution prices, trade count, timing, costs, liquidity feasibility, or market access.

Examples include changes to:

- Slippage assumptions.
- Transaction cost assumptions.
- Fill model assumptions.
- Liquidity assumptions.
- Execution timing assumptions.
- Latency assumptions.
- Venue limitation assumptions.
- Market impact assumptions.

Material friction changes create new experiments. They never overwrite prior evidence.

If a friction assumption is changed because an earlier configuration was defective, the prior configuration must remain auditable and must be marked according to future governance rather than silently replaced.

## Failure Conditions

Block 07 must stop the process before simulation when any of the following are confirmed or cannot be resolved:

- Undocumented friction assumptions.
- Hidden fill assumptions.
- Missing slippage assumption or missing explicit no-slippage assumption.
- Missing transaction cost assumption or missing explicit cost-exclusion assumption.
- Unrealistic liquidity assumptions.
- Infinite liquidity assumption.
- Inconsistent execution timing assumptions.
- Execution assumptions contradict temporal certification.
- Execution assumptions reintroduce lookahead.
- Untraceable execution parameters.
- Protocol ambiguity.
- Versioning failures.
- Fill, slippage, cost, liquidity, or timing assumptions selected after observing results.
- Execution assumptions tuned using observed results.
- Execution assumptions systematically improve expected performance without explicit justification.
- Material friction changes attempt to overwrite prior experiment evidence.

If a failure condition occurs, the simulation must not execute.

## Audit Trail Requirements

Every execution and friction configuration must leave auditable evidence.

The audit trail must include:

- Experiment identifier.
- Protocol version.
- Execution configuration identifier and version.
- Friction configuration.
- Fill assumptions.
- Slippage assumptions, including explicit no-slippage assumptions if applicable.
- Transaction cost assumptions, including explicit cost-exclusion assumptions if applicable.
- Liquidity assumptions and declared limitations.
- Timing assumptions.
- Latency assumptions where applicable.
- Market impact assumptions where applicable.
- Venue limitation assumptions where applicable.
- Reviewer or process identifier, when formalized.
- Deviations.
- Rationale.
- Source references.
- Expected effect.
- Version history.
- Failure findings, if any.
- Confirmation that no formulas, execution engine, order book simulator, broker integration, optimization, calibration, parameter search, robustness testing, performance interpretation, metrics, PnL, or result inspection occurred in Block 07.

The audit trail must be sufficient for quant research governance, model risk management, internal audit, trading systems engineering, reproducibility review, and external technical due diligence.

## Relationship With Block 08

Block 08 receives:

- Experiment outputs from Block 07, meaning the governed execution and friction configuration, not interpreted performance.
- Execution configuration.
- Friction assumptions.
- Execution audit trail.
- Protocol metadata.
- Assumptions context.

Block 08 may define risk and exposure simulation only within the boundaries of the frozen protocol and governed execution configuration.

Block 08 must not:

- Change execution assumptions.
- Modify frictions.
- Alter execution timing.
- Reinterpret results using new execution assumptions.
- Repair execution defects.
- Convert optimistic execution assumptions into accepted risk assumptions.
- Change the protocol.

If Block 08 detects execution modeling problems, it must return the process to Block 07. It must not repair execution defects downstream.

## Governance Requirements

Block 07 must preserve:

- Temporal certification from Block 04.
- Strategy specification from Block 05.
- Frozen protocol from Block 06.
- Assumptions registry and traceability records.
- Experiment identity and versioning.
- Prior experiment records.

Block 07 must not authorize trading, paper trading, deployment, live execution, broker connectivity, capital allocation, production risk controls, or edge claims.

## Execution Integrity Principle

Execution assumptions exist to represent uncertainty and friction, not to manufacture performance.

When execution realism and result attractiveness conflict, execution realism takes precedence.

The system must reject optimistic execution assumptions rather than accept inflated evidence.

## Explicit Non-Scope

Block 07 does not create mathematical execution models.

Block 07 does not create formulas.

Block 07 does not create a simulator.

Block 07 does not create an execution engine.

Block 07 does not create an order book simulator.

Block 07 does not create broker integrations.

Block 07 does not execute simulations.

Block 07 does not calculate metrics.

Block 07 does not calculate PnL.

Block 07 does not create trades.

Block 07 does not optimize parameters.

Block 07 does not perform calibration.

Block 07 does not perform parameter search.

Block 07 does not create robustness testing.

Block 07 does not interpret performance.

Block 07 does not create SQL.

Block 07 does not create executable schemas.

Block 07 does not create Python code.

Block 07 is a documentation and conceptual governance block that defines how execution realism and market frictions must be governed before downstream risk and exposure simulation.
