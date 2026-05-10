-- Sultan Data Platform - Operational Views
-- Scope: simple read-only views for inspecting OHLCV data, pipeline runs, and data quality.

CREATE OR REPLACE VIEW v_ohlcv_summary AS
WITH latest AS (
    SELECT
        exchange,
        symbol,
        timeframe,
        close AS last_close,
        volume AS last_volume,
        ROW_NUMBER() OVER (
            PARTITION BY exchange, symbol, timeframe
            ORDER BY timestamp DESC
        ) AS rn
    FROM ohlcv_curated
)
SELECT
    o.exchange,
    o.symbol,
    o.timeframe,
    COUNT(*) AS rows_count,
    MIN(o.timestamp) AS min_timestamp,
    MAX(o.timestamp) AS max_timestamp,
    l.last_close,
    l.last_volume
FROM ohlcv_curated o
JOIN latest l
  ON l.exchange = o.exchange
 AND l.symbol = o.symbol
 AND l.timeframe = o.timeframe
 AND l.rn = 1
GROUP BY
    o.exchange,
    o.symbol,
    o.timeframe,
    l.last_close,
    l.last_volume;

CREATE OR REPLACE VIEW v_ohlcv_latest_bars AS
SELECT
    exchange,
    symbol,
    timeframe,
    timestamp,
    open,
    high,
    low,
    close,
    volume,
    source,
    run_id,
    ingested_at,
    validated_at,
    data_quality_score,
    ROW_NUMBER() OVER (
        PARTITION BY exchange, symbol, timeframe
        ORDER BY timestamp DESC
    ) AS row_number_desc
FROM ohlcv_curated;

CREATE OR REPLACE VIEW v_pipeline_runs_latest AS
SELECT
    run_id,
    flow_name,
    source_name,
    status,
    started_at,
    finished_at,
    rows_fetched,
    rows_validated,
    rows_inserted,
    error_message,
    metadata
FROM ingestion_runs
ORDER BY started_at DESC;

CREATE OR REPLACE VIEW v_data_quality_latest AS
SELECT
    run_id,
    dataset_name,
    check_name,
    check_status,
    rows_checked,
    rows_failed,
    gaps_found,
    freshness_lag_seconds,
    data_quality_score,
    error_message,
    checked_at,
    metadata
FROM data_quality_checks
ORDER BY checked_at DESC;

CREATE OR REPLACE VIEW v_ohlcv_operational_health AS
WITH latest_quality AS (
    SELECT
        run_id,
        check_status,
        gaps_found,
        freshness_lag_seconds,
        data_quality_score,
        checked_at,
        ROW_NUMBER() OVER (ORDER BY checked_at DESC) AS rn
    FROM data_quality_checks
    WHERE dataset_name = 'ohlcv'
)
SELECT
    s.symbol,
    s.timeframe,
    s.rows_count,
    s.min_timestamp,
    s.max_timestamp,
    q.data_quality_score AS latest_data_quality_score,
    q.gaps_found AS latest_gaps_found,
    q.freshness_lag_seconds AS latest_freshness_lag_seconds,
    q.check_status AS latest_check_status
FROM v_ohlcv_summary s
LEFT JOIN latest_quality q
  ON q.rn = 1;

-- Example queries:
-- SELECT * FROM v_ohlcv_summary;
-- SELECT * FROM v_ohlcv_latest_bars WHERE symbol = 'BTCUSDT' AND timeframe = '1d' ORDER BY timestamp DESC LIMIT 20;
-- SELECT * FROM v_pipeline_runs_latest;
-- SELECT * FROM v_data_quality_latest;
-- SELECT * FROM v_ohlcv_operational_health;

