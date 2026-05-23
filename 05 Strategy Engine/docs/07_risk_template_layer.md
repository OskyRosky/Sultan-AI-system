# 07 Risk Template Layer

## Purpose

The Risk Template Layer defines risk as a design constraint before a candidate is evaluated for performance.

## Risk As Constraint

Risk templates describe limits, exclusions, structural assumptions, and acceptable design boundaries. They exist to prevent unconstrained strategy construction.

## Explicit Non-Scope

This layer is not a real Risk Engine. It does not implement:

- Dynamic position sizing.
- Portfolio optimization.
- Real-time exposure control.
- Drawdown-based trading decisions.
- Margin management.
- Live kill switches.

## Future Requirement

Every strategy candidate should eventually declare its risk template before it can enter downstream testing.
