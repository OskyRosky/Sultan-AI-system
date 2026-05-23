# 18 Block 03 Validation And Closure

## Scope Completed

Block 03 creates the Signal Definition Layer as an auditable conceptual layer.

It defines:

- signal definition structure;
- allowed conceptual orientations;
- origin requirements;
- supporting finding context rules;
- validation behavior;
- synthetic mockups;
- unit tests.

## Validation Intent

Validation proves only that signal definitions obey governance and traceability rules. It does not validate market behavior, profitability, robustness, or strategy quality.

## Expected Test Coverage

The Block 03 tests must show that:

- a valid signal can be created from an eligible hypothesis decision;
- a non-eligible hypothesis decision cannot originate a signal;
- an eligible finding decision cannot originate a signal;
- supporting finding decisions are allowed only as context;
- non-eligible supporting findings are rejected;
- evidence decisions cannot support signal definitions directly;
- required assumptions, limitations, falsification references, and audit references are enforced;
- signal definitions do not expose orders, trades, rules, strategy candidates, PnL, or performance metrics.

## Closure Conditions

Block 03 is closed when:

- the signal definition contract is documented;
- the signal definition implementation is covered by tests;
- every signal origin is constrained to eligible hypothesis decisions;
- findings are limited to supporting context;
- no real signals are created;
- no rules, strategy candidates, risk templates, backtesting, PnL, execution, or data integration are created;
- 04 Research Layer is not modified.

## Non-Edge Statement

No signal definition created under this block confirms edge, profitability, robustness, tradability, or deployability.
