# 02 Boundaries And Prohibitions

## What 06 Can Do

06 can, in future blocks and only inside controlled historical simulations:

- Evaluate governed StrategyDossiers from 05.
- Bind evaluations to historical data and feature snapshots.
- Enforce temporal admissibility and leakage controls.
- Operationalize conceptual rules when assumptions can be justified.
- Define explicit experimental assumptions.
- Simulate entries, exits, positions, fees, slippage, frictions, exposure, and risk controls.
- Calculate PnL, returns, metrics, and diagnostics.
- Run in-sample, out-of-sample, walk-forward, robustness, sensitivity, and falsification analyses.
- Register historical results.
- Produce governed feedback to 04 Research Layer and 05 Strategy Engine.

## What 06 Cannot Do

06 must not:

- Execute real orders.
- Connect to exchanges for execution.
- Perform live trading.
- Authorize paper trading.
- Authorize deployment.
- Allocate real capital.
- Approve leverage or live position sizing.
- Confirm edge from a positive historical result.
- Guarantee future performance.
- Modify 04 or 05 artifacts silently.
- Rewrite a StrategyDossier after seeing results.
- Use LLMs to decide trades.
- Use reinforcement learning.
- Perform indiscriminate parameter mining.
- Treat optimization as validation.
- Skip temporal admissibility controls.
- Treat historical simulation as production readiness.

## Historical Evaluation vs Paper Trading vs Live Trading vs Deployment

Historical evaluation uses past data under explicit assumptions to estimate how a candidate would have behaved in a simulated setting. It is retrospective and evidence-generating.

Paper trading simulates real-time operation against current market conditions. It is forward-running and operational, even if no capital is at risk. 06 does not authorize it.

Live trading sends real orders or otherwise creates real market exposure. 06 never performs or authorizes it.

Deployment means promotion to operational infrastructure. 06 results may inform future governance, but they are not deployment approval.

## No Edge Confirmation

Positive backtest results do not confirm edge by themselves. They may be artifacts of leakage, overfitting, data quality issues, unmodeled frictions, regime dependence, survivorship, selection bias, or unstable assumptions.

Any claim of edge requires later governed review beyond an isolated historical result.

## No Silent Upstream Mutation

06 must preserve the StrategyDossier and its traceability. If evaluation identifies a problem with 04 or 05 assumptions, 06 records governed feedback. It does not rewrite upstream documents, change the thesis, or alter eligibility records directly.

## No LLM Trade Decisions

LLMs may support documentation, review, explanation, or audit workflows where explicitly allowed by governance. They must not decide entries, exits, sizing, risk controls, or trade actions inside 06.

## No Reinforcement Learning

Reinforcement learning is outside the scope of 06. This stage evaluates governed strategy candidates under explicit historical protocols; it does not train adaptive trading agents.

## No Indiscriminate Parameter Mining

Parameter search without predeclared constraints, protocol governance, and robustness controls is prohibited. Any parameter or threshold assumption introduced by 06 must be explicit, justified, versioned, and separated from 05.
