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
        metadata
    FROM data_quality_checks
    WHERE dataset_name = 'ohlcv'
    ORDER BY checked_at DESC
    LIMIT 1
),
freshness_detail AS (
    SELECT
        split_part(detail.key, ':', 1) AS exchange,
        split_part(detail.key, ':', 2) AS symbol,
        split_part(detail.key, ':', 3) AS timeframe,
        (detail.value ->> 'freshness_lag_seconds')::bigint AS freshness_lag_seconds,
        detail.value ->> 'max_timestamp' AS quality_max_timestamp
    FROM latest_quality q
    CROSS JOIN LATERAL jsonb_each(COALESCE(q.metadata -> 'freshness', '{}'::jsonb)) AS detail(key, value)
),
gap_detail AS (
    SELECT
        gap.exchange,
        gap.symbol,
        gap.timeframe,
        SUM(gap.gaps_found)::bigint AS gaps_found
    FROM latest_quality q
    CROSS JOIN LATERAL jsonb_to_recordset(COALESCE(q.metadata -> 'gaps', '[]'::jsonb)) AS gap(
        exchange text,
        symbol text,
        timeframe text,
        gaps_found integer
    )
    GROUP BY gap.exchange, gap.symbol, gap.timeframe
),
fetch_detail AS (
    SELECT
        detail.key AS dataset_key,
        split_part(detail.key, ':', 1) AS symbol,
        split_part(detail.key, ':', 2) AS timeframe,
        (detail.value ->> 'rows_fetched')::bigint AS rows_fetched,
        detail.value ->> 'last_existing_timestamp' AS last_existing_timestamp,
        detail.value ->> 'fetch_since_timestamp' AS fetch_since_timestamp,
        detail.value ->> 'min_timestamp' AS fetched_min_timestamp,
        detail.value ->> 'max_timestamp' AS fetched_max_timestamp
    FROM latest_quality q
    CROSS JOIN LATERAL jsonb_each(COALESCE(q.metadata #> '{fetch,datasets}', '{}'::jsonb)) AS detail(key, value)
)
SELECT
    s.symbol,
    s.timeframe,
    s.rows_count,
    s.min_timestamp,
    s.max_timestamp,
    (
        CASE
        WHEN f.symbol IS NOT NULL THEN q.data_quality_score::numeric(6,5)
        ELSE NULL
        END
    )::numeric(6,5) AS latest_data_quality_score,
    (
        CASE
        WHEN f.symbol IS NOT NULL THEN COALESCE(g.gaps_found, 0)::integer
        ELSE NULL
        END
    )::integer AS latest_gaps_found,
    f.freshness_lag_seconds AS latest_freshness_lag_seconds,
    CASE
        WHEN f.symbol IS NOT NULL THEN q.check_status
        ELSE NULL
    END AS latest_check_status,
    q.run_id AS latest_global_quality_run_id,
    q.check_status AS latest_global_check_status,
    q.data_quality_score AS latest_global_data_quality_score,
    q.gaps_found AS latest_global_gaps_found,
    q.freshness_lag_seconds AS latest_global_freshness_lag_seconds,
    q.checked_at AS latest_global_checked_at,
    jsonb_build_object(
        'quality_scope',
        CASE
            WHEN f.symbol IS NOT NULL THEN 'symbol_timeframe'
            ELSE 'not_present_in_latest_quality_metadata'
        END,
        'quality_max_timestamp', f.quality_max_timestamp,
        'fetch_dataset_key', fd.dataset_key,
        'rows_fetched', fd.rows_fetched,
        'last_existing_timestamp', fd.last_existing_timestamp,
        'fetch_since_timestamp', fd.fetch_since_timestamp,
        'fetched_min_timestamp', fd.fetched_min_timestamp,
        'fetched_max_timestamp', fd.fetched_max_timestamp
    ) AS latest_symbol_timeframe_summary
FROM v_ohlcv_summary s
LEFT JOIN latest_quality q
  ON TRUE
LEFT JOIN freshness_detail f
  ON f.exchange = s.exchange
 AND f.symbol = s.symbol
 AND f.timeframe = s.timeframe
LEFT JOIN gap_detail g
  ON g.exchange = s.exchange
 AND g.symbol = s.symbol
 AND g.timeframe = s.timeframe
LEFT JOIN fetch_detail fd
  ON fd.symbol = s.symbol
 AND fd.timeframe = s.timeframe;

-- Example queries:
-- SELECT * FROM v_ohlcv_summary;
-- SELECT * FROM v_ohlcv_latest_bars WHERE symbol = 'BTCUSDT' AND timeframe = '1d' ORDER BY timestamp DESC LIMIT 20;
-- SELECT * FROM v_pipeline_runs_latest;
-- SELECT * FROM v_data_quality_latest;
-- SELECT * FROM v_ohlcv_operational_health;
