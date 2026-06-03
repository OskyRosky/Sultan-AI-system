# 08 Risk Engine — Block 00: Stage Charter, Authority and Veto Mandate

## Purpose

Stage 08 Risk Engine exists to act as the formal arbiter of risk, veto, blocking, conservative eligibility, and preservation of non-operational status when sufficient evidence does not exist.

The Risk Engine is a risk governance layer for downstream eligibility. It reviews structured handoff material, preserves absence-of-evidence states, enforces blocking conditions, and prevents unsupported promotion into Paper Trading, Live Trading, execution, or capital allocation.

Stage 08 is not a signal engine. Stage 08 is not an execution engine. Stage 08 is not a capital allocation system. It does not create trading signals, approve trades, route orders, assign capital, or convert upstream framework artifacts into operational readiness.

## Stage Authority

Stage 08 has authority to:

- veto outputs from `07 Signal Fusion + LLM Motors`;
- block downstream handling;
- block Paper Trading;
- block Live Trading;
- require more evidence;
- require human review;
- require Risk Engine review;
- downgrade states;
- preserve `non_operational`;
- activate or require Kill Switch handling under critical conditions.

Stage 08 may receive a structurally valid package from Stage 07 and still keep it blocked because empirical evidence is missing, incomplete, conflicted, non-replayable, or insufficient for promotion.

Structural validity is not operational approval. Contract compliance is not trading authorization. A complete handoff format does not override missing backtesting, missing OOS validation, missing walk-forward, missing robustness, unavailable confidence, or explicit upstream blocking states.

## Veto Mandate

The Risk Engine veto mandate is the formal authority to block downstream eligibility when risk, evidence, auditability, contract, or operational boundary conditions are not satisfied.

Stage 08 may veto for reasons including:

- Motor B `framework_only`;
- absence of real backtesting;
- absence of OOS validation;
- absence of walk-forward;
- absence of robustness;
- confidence unavailable;
- audit trace missing;
- source conflict;
- prohibited inference;
- event risk critical;
- contract violation;
- direct Paper Trading request without evidence;
- direct execution request;
- capital allocation attempt.

A Stage 08 veto is not a recommendation. It is a formal block of downstream eligibility. Once vetoed, a package, candidate, strategy, event path, or handoff cannot proceed to Paper Trading, Live Trading, execution, capital allocation, promotion, or operational downstream handling unless the relevant blocking condition is formally resolved and replayable evidence supports reconsideration.

## Notation and Reference Convention

This section resolves the potential collision between:

- Stage 08 Risk Engine;
- Block 08 Event, Regime and Market Risk Gate.

The official notation convention is:

```text
stage_id = "08"
stage_name = "Risk Engine"
block_number = "08"
block_id = "08.08"
block_ref = "stage_08.block_08"
```

All schemas, audit logs, risk decisions, replay artifacts, quality gates, and downstream documents must use this convention when ambiguity could exist between the stage number and the block number.

Block 08 is not renamed to `08A`. Stage 08 preserves the standard block numbering sequence from `00` through `17`.

## Current Framework-Only Blocking State

Under the current system state, Stage 08 must preserve the following safety restrictions:

```text
evidence_completeness_level = framework_only
paper_trading_eligibility = blocked
downstream_operational_eligibility = blocked
execution_eligibility = blocked
order_generation_eligibility = blocked
exchange_connection_eligibility = blocked
capital_allocation_eligibility = blocked
productive_position_sizing_eligibility = blocked
risk_budget_activation = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
handoff_to_09 = blocked
promotion_status = not_promoted
```

These values are Stage 08 safety restrictions, not simple informational metadata. They must block promotion, Paper Trading, Live Trading, execution, capital allocation, strategy approval, and downstream operational eligibility while Motor B remains `framework_only`.

No Stage 08 document, quality gate, dry run, review state, or future RiskDecision may reinterpret these values as conditional approval.

## Relationship With Stage 06 / Motor B

The Motor B Output Contract belongs to Stage 06:

`06 Backtesting Engine/docs/18_motor_b_output_contract.md`

Stage 08 must respect the current Motor B state defined by that contract. Motor B is currently `framework_only`: it has partial executable modules in Stages 04 and 05, but no final real backtesting output from Stage 06.

The current Motor B state blocks:

- Paper Trading;
- Live Trading;
- execution;
- capital allocation;
- strategy promotion;
- downstream operational eligibility.

Stage 08 cannot substitute Motor B. Stage 08 cannot substitute backtesting, OOS validation, walk-forward, or robustness. Stage 08 cannot invent historical performance, empirical validation, confidence, or eligibility where Stage 06 has not produced it.

If Motor B evidence remains incomplete, Stage 08 must preserve the block even when Stage 07 handoff artifacts are structurally valid.

## Relationship With Stage 07

Stage 08 receives outputs from Stage 07, but is not obligated to accept them operationally.

The Stage 07 closure artifact is:

`07 Signal Fusion + LLM Motors/docs/99_signal_fusion_llm_motors_closure.md`

Stage 08 may:

- accept a package structurally;
- downgrade it;
- reject it;
- veto it;
- require more evidence;
- require human review;
- require Risk Engine review;
- preserve operational blocking.

Stage 07 did not deliver:

- operational approval;
- Paper Trading readiness;
- Live Trading readiness;
- confidence score;
- final signal confidence score;
- capital allocation;
- execution permission;
- strategy promotion.

Stage 07 delivered bounded, documented, non-operational framework artifacts for Risk Engine review. Stage 08 must preserve the non-operational status unless downstream eligibility is supported by explicit, replayable, empirically sufficient evidence from the proper upstream stages.

## Non-Execution and Non-Allocation Rules

Stage 08:

- does not execute trades;
- does not generate orders;
- does not connect exchanges;
- does not allocate capital;
- does not define productive position sizing;
- does not activate Paper Trading;
- does not activate Live Trading;
- does not convert RiskDecision into trade execution;
- does not convert `review_package_only` into promotion;
- does not convert `requires_more_evidence` into conditional approval;
- does not convert a favorable event into approval;
- does not relax blocking conditions or operational restrictions declared by Stage 07 without formal replayable evidence.

Any request, artifact, or downstream consumer that attempts to convert Stage 08 review into execution, order generation, exchange integration, capital allocation, productive position sizing, or operational trading must be treated as a boundary violation and routed to block, veto, or review according to future Risk Engine policy.

## Kill Switch Declaration

The Kill Switch exists from Block 00 as an emergency authority of the Risk Engine.

The Kill Switch will be developed formally in Block 05 — Hard Veto Rules and Kill Switch Triggers.

The Kill Switch:

- is not a simple capital restriction;
- is not position sizing;
- is not an ordinary stop loss;
- may activate total blocking;
- may suspend downstream handling;
- may require immediate veto;
- may require urgent review;
- may operate independently of Human Review;
- does not permit trading, Paper Trading, or capital allocation.

Block 05 must formally define trigger taxonomy, Kill Switch outcomes, and downstream consequences. Until Block 05 is completed, the existence of Kill Switch authority is declarative and conservative: it can only preserve or increase blocking, never unlock operational activity.

## Block Scope Map

Stage 08 is expected to contain the following blocks:

```text
00 Stage Charter, Authority and Veto Mandate
01 Input Contract and Handoff Intake Layer
02 RiskHandoffPackage Validator
03 Motor B Evidence and Eligibility Gate
04 Risk Policy Registry
05 Hard Veto Rules and Kill Switch Triggers
06 Missing Evidence and Blocking Gap Assessment
07 Confidence and Evidence Sufficiency Gate
08 Event, Regime and Market Risk Gate
09 Exposure, Position and Capital Constraint Framework
10 Strategy Promotion and Downgrade Rules
11 Paper Trading Eligibility Gate
12 Risk Decision Engine
13 Human Review, Override and Escalation Policy
14 Audit, Traceability and Risk Decision Replay
15 Mock and Dry-Run Risk Scenarios
16 Quality Gates for 08
17 Stage Closure and Handoff to 09 Paper Trading
```

Block 00 defines the stage charter, authority, veto mandate, current blocking state, and non-operational boundaries.

Block 01 will define input and handoff intake rules.

Block 02 will define RiskHandoffPackage validation.

Block 03 will define the Motor B evidence and eligibility gate.

Block 04 will define the risk policy registry.

Block 05 will define hard veto rules and Kill Switch triggers.

Block 06 will define missing evidence and blocking gap assessment.

Block 07 will define confidence and evidence sufficiency handling.

Block 08 will define event, regime, and market risk gating.

Block 09 will define exposure, position, and capital constraint framework boundaries.

Block 10 will define strategy promotion and downgrade rules.

Block 11 will define Paper Trading eligibility gate rules.

Block 12 will define Risk Decision Engine framework behavior.

Block 13 will define human review, override, and escalation policy.

Block 14 will define audit, traceability, and risk decision replay.

Block 15 will define mock and dry-run risk scenarios.

Block 16 will define quality gates for Stage 08.

Block 17 will define Stage 08 closure and handoff boundaries for Stage 09.

This map defines scope only. It does not implement or pre-approve the content of Blocks 01 through 17.

## Expected Stage 08 Closure State

Under the current framework-only state, the expected Stage 08 closure state is:

```text
stage_status = risk_engine_framework_complete
operational_status = non_operational
paper_trading_eligibility = blocked
handoff_to_09 = blocked
confidence_status = confidence_not_available
confidence_score = null
final_signal_confidence_score = null
promotion_status = not_promoted
```

Completing Stage 08 as a framework does not mean Stage 09 Paper Trading can start operationally. Stage 09 must remain blocked while Motor B is `framework_only`, empirical evidence is unavailable, confidence is unavailable, and downstream operational eligibility is blocked.

## Explicit Non-Goals

This block does not do:

- trading;
- Paper Trading;
- Live Trading;
- exchange integration;
- order generation;
- productive position sizing;
- capital allocation;
- strategy approval;
- strategy promotion;
- confidence scoring;
- backtesting;
- OOS validation;
- walk-forward;
- robustness testing;
- empirical performance claims;
- LLM model selection;
- runtime LLM execution.

Block 00 is a documentary and governance artifact only. It establishes conservative authority for Stage 08 and preserves all current operational blocks.
