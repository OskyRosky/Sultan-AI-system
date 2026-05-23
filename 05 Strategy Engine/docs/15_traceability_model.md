# 15 Traceability Model

## Purpose

The traceability model defines how future 05 artifacts must point back to governed 04 artifacts.

This model is conceptual in Block 2. It does not read 04 files, databases, Parquet datasets, notebooks, or raw data.

## Traceability Chain

The allowed chain is:

```text
04 evidence -> 04 finding -> 04 hypothesis -> 05 eligibility decision -> future 05 signal definition -> future 05 strategy candidate
```

Evidence may also link directly to a hypothesis when 04 governance permits it:

```text
04 evidence -> 04 hypothesis -> 05 eligibility decision -> future 05 signal definition
```

The prohibited chain is:

```text
raw data or interesting metric -> 05 signal -> strategy candidate
```

## Required Trace Anchors

Every future eligible input must preserve:

- source layer;
- source component;
- source identifier;
- audit reference;
- approval status;
- temporal scope;
- asset scope;
- timeframe scope;
- regime context when applicable;
- limitations;
- falsification criteria for hypotheses.

## Future Signal Traceability

Future Block 3 signal definitions must reference a prior eligibility decision. They must not reference raw 04 evidence, findings, or hypotheses directly without an eligibility decision.

## Future Strategy Candidate Traceability

Future strategy candidates must reference:

- eligible input IDs;
- signal definition IDs;
- risk template IDs;
- quality gate records;
- falsification criteria.

This block does not create those candidates.

## Audit Requirement

Every eligibility decision must be reproducible from the declared input metadata. If a decision cannot explain why the input was eligible or ineligible, the decision is invalid.

## Boundary With 06

06 Backtesting Engine receives dossiers from 05 after strategy closure and dossier handoff. It does not receive raw evidence as a substitute for a strategy dossier.
