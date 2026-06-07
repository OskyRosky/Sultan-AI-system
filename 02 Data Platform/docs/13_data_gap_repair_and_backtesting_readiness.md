# 02 Data Platform — Data Gap Repair and Backtesting Readiness Report

## 1. Executive Summary

This report consolidates the diagnosis, repair, pipeline hardening, controlled reconciliation run, and local scheduler configuration for the Binance OHLCV data gap identified in `public.ohlcv_curated`.

The final OHLCV gap affecting `BTCUSDT` and `ETHUSDT` in `1d` and `4h` was repaired at the 02 Data Platform level through a controlled incremental reconciliation run. The pipeline now uses conservative overlap, rejects open candles from curated/PostgreSQL, preserves raw Binance/CCXT responses for audit, performs idempotent upserts, and reports reconciliation health per symbol/timeframe.

The operational scheduler is now `launchd`, with two daily opportunities to run the same reconciliator flow at `10:05` and `18:05` America/Costa_Rica. Prefect remains in the code as flow/task framework, but Prefect Server is not the operational scheduler while the local SQLite backend is blocked.

This is a readiness report for data platform repair and downstream planning. It does not declare Feature Engineering ready, Backtesting ready, Stage 09 ready, Paper Trading ready, or any strategy confidence.

## 2. Scope

This report covers:

- The OHLCV final data gap diagnostic in `02 Data Platform`.
- The Binance/CCXT incremental ingestion pipeline hardening.
- The controlled reconciliation run that repaired the gap.
- Current PostgreSQL data health for `BTCUSDT` and `ETHUSDT` in `1d` and `4h`.
- The current local scheduler configuration using `launchd`.
- Dependencies and limitations before downstream use by `03 Feature Engineering` and `06 Backtesting Engine`.

This report does not cover:

- Feature regeneration in `03 Feature Engineering`.
- Backtesting execution in `06 Backtesting Engine`.
- OOS validation.
- Walk-forward validation.
- Robustness validation.
- Empirical confidence.
- Strategy promotion.
- Stage 09 Paper Trading design or execution.
- Capital allocation or live trading.

## 3. Initial Data Gap Diagnostic

The initial diagnostic confirmed a final gap in `public.ohlcv_curated`.

Reference date:

```text
2026-06-06
```

Affected series:

```text
BTCUSDT 1d
BTCUSDT 4h
ETHUSDT 1d
ETHUSDT 4h
```

Last available timestamps before repair:

```text
1d: 2026-05-11 00:00:00 UTC
4h: 2026-05-11 16:00:00 UTC
```

Approximate missing candles at diagnostic time:

```text
1d: about 25 candles per symbol
4h: about 155 candles per symbol
```

The diagnostic also confirmed no evidence that the data had been continuously updated after the last successful run on `2026-05-11`.

## 4. Root Cause Analysis

The root issue was operational continuity, not a missing data contract.

Confirmed factors:

- The OHLCV flow existed.
- The incremental mode existed but was only partially robust.
- The previous incremental logic started after the latest stored timestamp, so it could miss corrections to the latest previously persisted candle.
- Prefect Server local was not available during diagnostic/repair work.
- Attempting to use Prefect Server exposed:

```text
sqlite3.OperationalError: database is locked
```

- A separate external cron existed:

```text
5 0 * * * bash /Users/sultan/Trading/algo-trading/tools/run_daily_job.sh
```

That cron points to another repository:

```text
/Users/sultan/Trading/algo-trading
```

The referenced script did not exist at that path during inspection. This cron is not part of Sultan-AI-system and must not be treated as the official scheduler for `02 Data Platform`.

## 5. Pipeline Hardening

The OHLCV pipeline was hardened before executing the repair run.

### Incremental Overlap

Incremental mode now uses a configurable overlap window:

```text
SULTAN_OHLCV_INCREMENTAL_OVERLAP_CANDLES=1
```

Instead of starting strictly after `MAX(timestamp)`, the flow starts from:

```text
max(latest_stored_before_run - overlap * timeframe_interval, symbol_start_date)
```

This allows the pipeline to refetch and correct the latest previously persisted candle while relying on idempotent PostgreSQL upsert to avoid duplicates.

### Closed-Candle Promotion

Raw Parquet may preserve the Binance/CCXT response as received, including an open candle if Binance returns one.

Curated Parquet and `public.ohlcv_curated` only accept closed candles:

```text
1d close_time = timestamp + 1 day
4h close_time = timestamp + 4 hours
closed if close_time <= now_utc
```

No `close_time` column was added to PostgreSQL.

### Reconciliation Behavior

The flow now behaves as a reconciliator:

```text
verify current state
detect real missing candles
download required range with overlap
validate
store idempotently
report health
```

Metadata now records, per symbol/timeframe:

- `latest_stored_before_run`
- `latest_closed_expected_timestamp`
- `missing_from_timestamp`
- `missing_to_timestamp`
- `expected_missing_closed_candles_before_run`
- `incremental_start_timestamp`
- `latest_fetched_timestamp`
- `latest_closed_eligible_timestamp`
- `latest_stored_after_run`
- `missing_closed_candles_after_run`
- `is_caught_up_after_run`
- `health_status`
- `rows_fetched_raw`
- `rows_closed_eligible`
- `rows_open_excluded`
- `rows_inserted_or_updated`
- `rows_new`
- `rows_existing`

The view `public.v_ohlcv_reconciliation_health` was added and validated for operational inspection.

## 6. Controlled Reconciliation Run

The controlled repair run was executed in incremental mode.

Run:

```text
run_id = 2db92aa1-1351-46a2-a99e-b6ec9835ae1c
status = success
```

Run metrics:

```text
rows_fetched = 374
rows_validated = 370
rows_inserted = 370
rows_new = 362
rows_existing = 8
rows_fetched_raw = 374
rows_closed_eligible = 370
rows_open_excluded = 4
```

Post-run validations:

```text
duplicates_after_run = 0
open_candles_in_postgres = 0
```

Reconciliation result:

```text
BTCUSDT 1d = caught_up
BTCUSDT 4h = caught_up
ETHUSDT 1d = caught_up
ETHUSDT 4h = caught_up
```

The final OHLCV gap was repaired at the `02 Data Platform` level.

## 7. Operational Scheduling

Prefect remains present as the flow/task framework, but Prefect Server is not currently the operational scheduler because the local SQLite backend encountered:

```text
sqlite3.OperationalError: database is locked
```

Current operational scheduler:

```text
launchd
```

Script:

```text
02 Data Platform/scripts/run_ohlcv_reconciliation.sh
```

Effective command:

```bash
PREFECT_API_URL= SULTAN_OHLCV_MODE=incremental poetry run python "02 Data Platform/flows/ingest_ohlcv_flow.py"
```

LaunchAgents:

```text
/Users/sultan/Library/LaunchAgents/com.sultan.ohlcv.reconciliation.morning.plist
/Users/sultan/Library/LaunchAgents/com.sultan.ohlcv.reconciliation.evening.plist
```

Labels:

```text
com.sultan.ohlcv.reconciliation.morning
com.sultan.ohlcv.reconciliation.evening
```

Schedules:

```text
10:05 America/Costa_Rica
18:05 America/Costa_Rica
```

Both LaunchAgents execute the same reconciliator flow. There is no separate evening flow.

Expected operational behavior:

- If the morning run does not happen because the computer is off, the evening run should detect the missing data and complete it.
- If the morning run succeeds, the evening run should add newly closed candles if available or finish without new inserts.
- If nothing new is available, the upsert should avoid duplicates and the run should still report health.

LaunchAgent policy:

```text
RunAtLoad = false
KeepAlive = not used
```

Both plist files passed `plutil`.

The script was manually validated with:

```text
run_id = 0e0a1b7c-e538-4f96-afa4-99465741b521
status = success
rows_fetched = 12
rows_validated = 8
rows_inserted = 8
rows_new = 0
rows_existing = 8
rows_open_excluded = 4
duplicates = 0
open_candles = 0
health_status = caught_up for all 4 series
```

## 8. Automatic launchd Run Observation

Status:

```text
observed but failed due Binance timeout
```

Observed trigger:

```text
2026-06-06 18:05 America/Costa_Rica
```

Evidence:

```text
launchd label = com.sultan.ohlcv.reconciliation.evening
launchd runs = 1
launchd last exit code = 1
log = 02 Data Platform/logs/ohlcv_reconciliation/run_20260607T000501Z.log
error_type = ccxt.base.errors.RequestTimeout
error = binance GET https://api.binance.com/api/v3/exchangeInfo timed out
```

PostgreSQL impact:

```text
new ingestion_run = not recorded before Repair Block 3C
duplicates = 0
open_candles_in_postgres = 0
latest successful run = 0e0a1b7c-e538-4f96-afa4-99465741b521
```

Interpretation:

- The first automatic calendar-triggered `launchd` run was observed.
- The scheduler executed the correct script.
- The run failed because Binance/CCXT timed out before OHLCV fetch completed.
- Data integrity was preserved: no duplicate rows and no open candles were inserted.
- Because the failure happened before the pre-3C audit registration point, no new `ingestion_run` was created for that failed attempt.

Repair Block 3C response:

- CCXT timeout increased from `30000` ms to configurable `SULTAN_CCXT_TIMEOUT_MS = 60000`.
- Transient CCXT network/API errors now use controlled retry/backoff.
- `ingestion_runs.status = running` is now recorded before Binance fetch.
- Early Binance/CCXT failures now update the same `run_id` to `status = failed` with failure metadata.
- The exception is still re-raised so `launchd`/script retains exit code `!= 0`.

This section documents observation of the first automatic run, but it does not declare final operational closure because the observed run failed due to a transient Binance timeout. The next successful morning/evening reconciliator run must update the pending candles and leave an audited `ingestion_run`.

## 9. Data Health After Repair

Current repaired series:

```text
BTCUSDT 1d
BTCUSDT 4h
ETHUSDT 1d
ETHUSDT 4h
```

Confirmed health after controlled repair and manual launchd-script validation:

```text
health_status = caught_up for all 4 series
missing_closed_candles_after_run = 0 for all 4 series
duplicates = 0
open_candles_in_postgres = 0
latest_data_quality_score = 1.00000
latest_quality_check_status = passed
```

Latest known post-repair ranges:

```text
BTCUSDT 1d: 2017-08-17 00:00:00 UTC to 2026-06-05 00:00:00 UTC
BTCUSDT 4h: 2017-08-17 04:00:00 UTC to 2026-06-06 16:00:00 UTC
ETHUSDT 1d: 2017-08-17 00:00:00 UTC to 2026-06-05 00:00:00 UTC
ETHUSDT 4h: 2017-08-17 04:00:00 UTC to 2026-06-06 16:00:00 UTC
```

## 10. Dependency on 03 Feature Engineering

`03 Feature Engineering` depends on repaired and validated OHLCV data from `public.ohlcv_curated`.

After this repair, `02 Data Platform` is no longer known to have the final OHLCV gap that blocked downstream use. However, this does not make features ready.

Required before downstream research/backtesting use:

- Regenerate or verify feature outputs derived from OHLCV.
- Confirm feature coverage for `BTCUSDT` and `ETHUSDT`.
- Confirm feature timestamp continuity.
- Confirm no feature outputs were generated from stale/gapped OHLCV.
- Produce or validate a feature snapshot suitable for `06 Backtesting Engine`.

Feature Engineering readiness remains pending.

## 11. Impact on 06 Backtesting Engine

The repaired OHLCV dataset reduces a major data-platform blocker, but it does not make `06 Backtesting Engine` ready for real empirical conclusions.

Backtesting remains blocked until:

- `03 Feature Engineering` regeneration or verification is complete.
- A historical data/features snapshot is defined and versioned.
- Backtesting path is executed.
- OOS validation is attempted or explicitly bounded.
- Walk-forward validation is attempted or explicitly bounded.
- Robustness validation is attempted or explicitly bounded.
- Fees/slippage assumptions are modeled.
- Temporal admissibility and leakage controls are enforced.
- Empirical confidence is supported by evidence.

Do not declare:

```text
backtesting_data_readiness = ready
confidence_status = available
strategy_promoted = true
stage_09_readiness = ready
paper_trading_ready = true
```

## 12. Current Status Flags

```text
data_gap_status = repaired
ohlcv_pipeline_status = operational
scheduler_status = configured_pending_first_automatic_observation
feature_engineering_dependency = pending_regeneration_or_verification
backtesting_data_readiness = partial / blocked
stage_09_readiness = blocked
paper_trading_ready = false
```

## 13. Remaining Risks

Remaining risks and pending items:

- The first automatic launchd run is still pending observation.
- Prefect Server local remains blocked by SQLite lock if future UI/deployment orchestration is desired.
- The external cron pointing to `/Users/sultan/Trading/algo-trading/tools/run_daily_job.sh` is broken and unrelated to Sultan-AI-system.
- `03 Feature Engineering` still needs regeneration or verification after the OHLCV repair.
- `06 Backtesting Engine` still needs a versioned data/features snapshot before real backtesting.
- The latest manual launchd-script run showed non-blocking Prefect ephemeral event emission errors, while the flow and PostgreSQL records still completed successfully.

## 14. Recommended Next Steps

Recommended order:

1. Observe the automatic launchd run at `2026-06-06 18:05 America/Costa_Rica`.
2. Update Section 8 of this report with logs, `run_id`, PostgreSQL validation, duplicate check, open-candle check, and health status.
3. Commit the 02 Data Platform repair documentation and scheduler artifacts.
4. Regenerate or verify `03 Feature Engineering` outputs.
5. Produce a feature/data snapshot for `06 Backtesting Engine`.
6. Prepare `06 Backtesting Engine` readiness only after the 03 dependency is verified.

## 15. Evidence Appendix

### Coverage

```sql
SELECT
    symbol,
    timeframe,
    COUNT(*) AS rows_count,
    MIN(timestamp) AS first_available_timestamp,
    MAX(timestamp) AS last_available_timestamp
FROM public.ohlcv_curated
WHERE symbol IN ('BTCUSDT', 'ETHUSDT')
  AND timeframe IN ('1d', '4h')
GROUP BY symbol, timeframe
ORDER BY symbol, timeframe;
```

### Duplicates

```sql
SELECT
    exchange,
    symbol,
    timeframe,
    timestamp,
    COUNT(*) AS n
FROM public.ohlcv_curated
WHERE symbol IN ('BTCUSDT', 'ETHUSDT')
  AND timeframe IN ('1d', '4h')
GROUP BY exchange, symbol, timeframe, timestamp
HAVING COUNT(*) > 1
ORDER BY n DESC, symbol, timeframe, timestamp
LIMIT 20;
```

### Open Candles

```sql
SELECT
    symbol,
    timeframe,
    COUNT(*) AS open_candles_in_postgres
FROM public.ohlcv_curated
WHERE symbol IN ('BTCUSDT', 'ETHUSDT')
  AND timeframe IN ('1d', '4h')
  AND (
      (timeframe = '1d' AND timestamp + INTERVAL '1 day' > NOW())
      OR
      (timeframe = '4h' AND timestamp + INTERVAL '4 hours' > NOW())
  )
GROUP BY symbol, timeframe
ORDER BY symbol, timeframe;
```

### Reconciliation Health

```sql
SELECT *
FROM public.v_ohlcv_reconciliation_health
ORDER BY symbol, timeframe;
```

### Latest Ingestion Runs

```sql
SELECT
    run_id,
    flow_name,
    status,
    started_at,
    finished_at,
    rows_fetched,
    rows_validated,
    rows_inserted,
    error_message,
    metadata
FROM public.ingestion_runs
ORDER BY started_at DESC
LIMIT 5;
```

### Latest Quality Checks

```sql
SELECT
    run_id,
    check_status,
    severity,
    rows_checked,
    rows_failed,
    gaps_found,
    freshness_lag_seconds,
    data_quality_score,
    checked_at,
    error_message,
    metadata
FROM public.data_quality_checks
ORDER BY checked_at DESC
LIMIT 5;
```

### Launchd Inspection

```bash
launchctl print gui/501/com.sultan.ohlcv.reconciliation.morning
launchctl print gui/501/com.sultan.ohlcv.reconciliation.evening
```

### Logs

```bash
ls -lah "02 Data Platform/logs/ohlcv_reconciliation"
tail -n 120 "02 Data Platform/logs/ohlcv_reconciliation/"*.log 2>/dev/null || true
```
