# 06 Decision Log

## Initial Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-001 | 06 Backtesting Engine is historical evaluation only, not trading authorization. | Accepted |
| D-002 | StrategyDossier is the upstream governed input, but it is not proof of edge. | Accepted |
| D-003 | Operational assumptions added by 06 must be explicit, versioned, auditable, and separate from 05. | Accepted |
| D-004 | Temporal admissibility is blocking before operationalization. | Accepted |
| D-005 | Experiment protocol must be frozen before results are observed. | Accepted |
| D-006 | Positive backtest results do not authorize paper trading, deployment, capital allocation, or live trading. | Accepted |
| D-007 | Feedback to 04 and 05 is governed handoff only, not direct upstream mutation. | Accepted |
| D-008 | 06 does not use LLMs to decide trades. | Accepted |
| D-009 | 06 does not use reinforcement learning. | Accepted |
| D-010 | Indiscriminate parameter mining is prohibited. | Accepted |
| D-011 | Block 01 creates documentation architecture only and does not implement simulation, metrics, data loading, risk models, frictions, PnL, execution, paper trading, or exchange integration. | Accepted |

## Notes

These decisions initialize the architectural constraints for Block 01. They do not validate any strategy, edge, performance claim, operational readiness, paper trading path, live trading path, or deployment path.

Future blocks may append decisions to this log as contracts, schemas, tests, and governance artifacts are introduced.

## Block 02 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-012 | Eligibility depends on dossier integrity, traceability, governance completeness, candidate clarity, and absence of unresolved contradictions rather than expected performance. | Accepted |
| D-013 | Operational parameters intentionally absent from StrategyDossier cannot be used as eligibility rejection criteria. | Accepted |
| D-014 | 06 Backtesting Engine must never infer missing strategic information. | Accepted |
| D-015 | Eligibility rejection generates auditable feedback without mutating upstream artifacts. | Accepted |
| D-016 | StrategyDossier is the only conceptual input to Block 02. | Accepted |
| D-017 | Block 03 may receive only dossiers marked `eligible_for_backtest_evaluation` by Block 02. | Accepted |
| D-018 | Block 02 creates documentation only and does not create historical snapshots, temporal controls, operationalization, simulation, metrics, risk models, frictions, executable schemas, paper trading, live trading, or deployment paths. | Accepted |

## Block 03 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-019 | Every historical evaluation must reference a uniquely identifiable snapshot. | Accepted |
| D-020 | Snapshot definition precedes temporal admissibility validation. | Accepted |
| D-021 | Feature lineage must remain traceable to 03 Feature Engineering outputs. | Accepted |
| D-022 | Known limitations must be registered explicitly rather than hidden. | Accepted |
| D-023 | Snapshot certification confirms documentation completeness but does not certify temporal validity. | Accepted |
| D-024 | Block 04 is the exclusive authority for lookahead review, leakage review, temporal admissibility, future information contamination, and availability-at-decision-time review. | Accepted |
| D-025 | Block 03 creates documentation only and does not create datasets, storage artifacts, SQL, pipelines, temporal validation controls, leakage checks, simulation, metrics, risk models, or executable schemas. | Accepted |

## Block 04 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-026 | Temporal admissibility is a blocking prerequisite before operationalization or simulation. | Accepted |
| D-027 | Snapshot certification does not imply temporal validity. | Accepted |
| D-028 | Data must be evaluated by availability time, not only event time. | Accepted |
| D-029 | Feature windows must close before the simulated decision point; any intraperiod or incomplete-bar exception must be pre-approved by Block 04 before temporal certification. | Accepted |
| D-030 | Confirmed lookahead, leakage, or unresolved temporal ambiguity prevents advancement to operationalization. | Accepted |
| D-031 | Block 05 may only consume temporally certified snapshots. | Accepted |
| D-032 | An independent Claude Code audit is required after Block 04 before starting Block 05. | Accepted |
| D-033 | Block 05 cannot introduce new feature timing exceptions without returning to Block 04 for re-certification. | Accepted |
| D-034 | Exchange OHLCV availability may use conservative documented inference; non-market, delayed-publication, manually curated, or revisable datasets require explicit availability, publication, point-in-time, or revision-as-of metadata. | Accepted |
| D-035 | Point-in-time or revision-as-of governance is required for revisable datasets. | Accepted |
| D-036 | Composite feature availability is governed by the latest availability time of all constituent inputs, dependencies, revisions, and lags. | Accepted |
| D-037 | Cross-sectional transformations must use contemporaneously available universes, not final snapshot universes or retrospectively included assets. | Accepted |
| D-038 | Audit trails must document both risks found and risks reviewed but not found. | Accepted |
| D-039 | Declared survivorship or retrospective universe limitations do not automatically qualify for clean temporal certification and must be carried into later governance when material. | Accepted |

## Block 05 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-040 | Operationalization is translation of governed intent, not strategy creation. | Accepted |
| D-041 | Material assumptions belong to Backtesting Engine and never become retroactive outputs of Strategy Engine. | Accepted |
| D-042 | Every operationalized rule must remain traceable to StrategyDossier content or explicit assumptions. | Accepted |
| D-043 | Operationalization must fail when strategic ambiguity cannot be resolved without introducing material interpretation. | Accepted |
| D-044 | Assumption explosion is evidence of insufficient operationalizability rather than justification for additional interpretation. | Accepted |
| D-045 | Preservation of strategic intent takes precedence over simulation convenience. | Accepted |
| D-046 | All ambiguity resolutions must be registered regardless of materiality. | Accepted |
| D-047 | Multiple plausible mappings from conceptual rule to evaluable representation require an interpretation record. | Accepted |
| D-048 | Block 05 may only accept `temporally_certified` or `temporally_certified_with_declared_limitations` unless the lifecycle and decision log are explicitly updated. | Accepted |
| D-049 | Cumulative interpretation drift must be assessed after individual assumption and interpretation classification. | Accepted |
| D-050 | Originating gaps must be shown to be structurally required for operationalizability, not merely convenient. | Accepted |
| D-051 | Material assumptions classified as preserving intent must be reviewed against rationale, hypothesis, conceptual rules, falsification criteria, and relevant risk references. | Accepted |
| D-052 | Block 06 cannot use protocol design to repair or hide unresolved operationalization limitations. | Accepted |
| D-053 | Pending assumptions or interpretation records cannot be passed downstream. | Accepted |

## Block 06 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-054 | Backtesting is an experiment and not evidence by itself. | Accepted |
| D-055 | Protocol validity precedes interpretation of results. | Accepted |
| D-056 | Changes to protocol create new experiments and never overwrite prior experiments. | Accepted |
| D-057 | Partition boundaries are governance artifacts and not optimization tools. | Accepted |
| D-058 | Benchmark selection must be documented before evaluation and cannot be justified using observed results. | Accepted |
| D-059 | Undocumented assumptions invalidate experimental reproducibility. | Accepted |
| D-060 | Experiment outputs cannot compensate for protocol defects. | Accepted |
| D-061 | Protocol integrity takes precedence over result attractiveness. | Accepted |

## Block 07 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-062 | Execution realism exists to reduce optimism bias, not improve results. | Accepted |
| D-063 | Execution assumptions are protocol assumptions and must be explicitly documented. | Accepted |
| D-064 | Absence of slippage is an assumption and not a neutral baseline. | Accepted |
| D-065 | Ignoring transaction costs is an assumption and not a neutral baseline. | Accepted |
| D-066 | Infinite liquidity assumptions are not admissible. | Accepted |
| D-067 | Execution timing must remain consistent with temporal certification. | Accepted |
| D-068 | Execution assumptions cannot be tuned using observed results. | Accepted |
| D-069 | Material friction changes create new experiments and never overwrite prior evidence. | Accepted |
| D-070 | Execution realism takes precedence over result attractiveness. | Accepted |

## Block 08 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-071 | Risk simulation exists to represent exposure realism and not to improve performance. | Accepted |
| D-072 | Risk assumptions are protocol assumptions and must be explicitly documented. | Accepted |
| D-073 | Absence of position sizing assumptions is itself a risk assumption. | Accepted |
| D-074 | Absence of exposure limits is an exposure assumption. | Accepted |
| D-075 | Absence of leverage constraints is a leverage assumption. | Accepted |
| D-076 | Risk assumptions cannot be selected using observed results. | Accepted |
| D-077 | Material risk changes create new experiments and never overwrite prior evidence. | Accepted |
| D-078 | Portfolio constraints must be explicit and traceable. | Accepted |
| D-079 | Unconstrained concentration assumptions are not admissible unless explicitly declared. | Accepted |
| D-080 | Exposure realism takes precedence over result attractiveness. | Accepted |
| D-081 | Multiple protocol versions over the same StrategyDossier and snapshot must remain linked and visible to Results Registry. | Accepted |
| D-082 | Primary experiment selection cannot be based on observed results. | Accepted |
| D-083 | Protocol Governance assumptions are limited to structural experiment design only. | Accepted |
| D-084 | Window exclusions of known adverse regimes require explicit non-result-based rationale. | Accepted |
| D-085 | Benchmark rationale must justify appropriateness for the strategy type. | Accepted |
| D-086 | Superseded experiments remain reportable and linked to successors. | Accepted |
| D-087 | External references must be frozen by citation metadata. | Accepted |
| D-088 | Immediate fills are optimistic assumptions requiring explicit justification. | Accepted |
| D-089 | Risk mark-to-market timing must be consistent with execution fill timing. | Accepted |
| D-090 | Asset eligibility constraints cannot silently reduce the certified snapshot universe. | Accepted |
| D-091 | Negative evidence principle applies to Blocks 06-08 audit trails. | Accepted |
| D-092 | Block 09 must validate the integrated assumption set before simulation. | Accepted |
| D-093 | Protocol freeze requires an explicit audit-trail event before downstream use. | Accepted |
| D-094 | Returned-to-prior-block correction states must preserve traceability. | Accepted |

## Block 09 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-095 | Simulation engine executes governed instructions and does not design strategy, protocol, execution, or risk. | Accepted |
| D-096 | Block 09 requires integrated assumption set validation before simulation. | Accepted |
| D-097 | Unresolved pending assumptions block simulation. | Accepted |
| D-098 | Same governed inputs must produce the same simulation trace. | Accepted |
| D-099 | Mutable external dependencies are not admissible during simulation execution. | Accepted |
| D-100 | Simulation outputs are simulated artifacts and not real trades, recommendations, or execution instructions. | Accepted |
| D-101 | Block 10 cannot modify simulation events, trades, or positions. | Accepted |
| D-102 | Simulation convenience never overrides governed input integrity. | Accepted |

## Block 10 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-103 | Metrics describe outcomes and do not establish edge. | Accepted |
| D-104 | Block 10 only consumes governed simulation outputs. | Accepted |
| D-105 | Missing simulation outputs invalidate performance measurement. | Accepted |
| D-106 | Metric creation after result inspection is prohibited. | Accepted |
| D-107 | Benchmark comparison does not establish superiority. | Accepted |
| D-108 | Performance diagnostics do not imply future profitability. | Accepted |
| D-109 | Block 11 may challenge metrics but cannot rewrite them. | Accepted |
| D-110 | Measurement integrity takes precedence over attractive narratives. | Accepted |

## Block 11 Decisions

| ID | Decision | Status |
| --- | --- | --- |
| D-111 | A profitable backtest is not evidence of edge. | Accepted |
| D-112 | Block 11 attempts to refute evidence rather than confirm edge. | Accepted |
| D-113 | Failure to falsify is not proof and survival of challenge is not validation. | Accepted |
| D-114 | Robustness testing cannot create alpha or repair strategy, protocol, execution, risk, data, simulation, or metric defects. | Accepted |
| D-115 | Falsification criteria must trace to StrategyDossier, Research Layer, or Assumptions Registry and cannot be invented by Block 11. | Accepted |
| D-116 | Passing many tests does not prove edge. | Accepted |
| D-117 | Experiment families, superseded experiments, abandoned experiments, and robustness variants must remain visible. | Accepted |
| D-118 | Selective presentation of favorable robustness outcomes is prohibited. | Accepted |
| D-119 | Block 11 consumes Block 10 metrics but cannot modify, recalculate, or reinterpret them to hide results. | Accepted |
| D-120 | Block 12 receives Block 11 outcomes but cannot rewrite robustness, falsification, fragility, or anti-overfitting findings. | Accepted |
| D-121 | StrategyDossier falsification criteria are presumed applicable and cannot be declared inapplicable by Block 11 alone. | Accepted |
| D-122 | Confirmed experiment shopping blocks `robust_result`. | Accepted |
| D-123 | Predefined challenge outcomes dominate post-outcome challenge outcomes. | Accepted |
| D-124 | Post-outcome challenges are supplementary and cannot offset adverse predefined findings. | Accepted |
| D-125 | Iterative returns from Block 11 are limited and must escalate after repeated returns. | Accepted |
| D-126 | `overfit_result` maps to the blocking lifecycle state `overfit_detected`. | Accepted |
| D-127 | Metric defects are verifiable calculation or implementation errors, not methodology preferences. | Accepted |
| D-128 | Materiality criteria must be predefined before challenge execution. | Accepted |
| D-129 | Challenge scope and depth must be predefined and recorded. | Accepted |
| D-130 | Robustness variants must not hide new experiments. | Accepted |
| D-131 | Primary experiment designation must be timestamped before simulation or result inspection. | Accepted |
| D-132 | Not-applicable challenge categories require positive, verifiable, non-result-based justification. | Accepted |
| D-133 | Assumption Registry entries cannot be retroactively selected as falsification criteria. | Accepted |
| D-134 | Core challenge failures cannot be overridden by peripheral successes. | Accepted |
| D-135 | Block 12 cannot alter Block 11 classifications. | Accepted |
