-- 03 Feature Engineering - Operational monitoring views.
-- Read-only inspection layer for DBeaver and psql.

CREATE OR REPLACE VIEW vw_feature_latest_runs AS
SELECT
    run_id,
    flow_name,
    status,
    feature_set,
    feature_version,
    rows_loaded,
    rows_generated,
    rows_validated,
    rows_inserted,
    started_at,
    finished_at,
    (metadata ->> 'data_quality_score')::NUMERIC AS data_quality_score,
    error_message
FROM feature_runs
ORDER BY started_at DESC;

CREATE OR REPLACE VIEW vw_feature_quality_latest AS
SELECT
    run_id,
    check_name,
    check_status,
    severity,
    rows_checked,
    rows_failed,
    data_quality_score,
    error_message,
    created_at
FROM feature_quality_checks
ORDER BY created_at DESC, run_id, check_name;

CREATE OR REPLACE VIEW vw_feature_storage_summary AS
SELECT
    exchange,
    symbol,
    timeframe,
    feature_set,
    feature_version,
    COUNT(*) AS row_count,
    MIN(timestamp) AS min_timestamp,
    MAX(timestamp) AS max_timestamp,
    (ARRAY_AGG(run_id ORDER BY validated_at DESC NULLS LAST, timestamp DESC))[1] AS latest_run_id,
    AVG(data_quality_score) AS avg_data_quality_score,
    MAX(validated_at) AS max_validated_at
FROM ohlcv_features
GROUP BY
    exchange,
    symbol,
    timeframe,
    feature_set,
    feature_version;

CREATE OR REPLACE VIEW vw_feature_duplicate_check AS
SELECT
    exchange,
    symbol,
    timeframe,
    timestamp,
    feature_set,
    feature_version,
    COUNT(*) AS duplicate_count
FROM ohlcv_features
GROUP BY
    exchange,
    symbol,
    timeframe,
    timestamp,
    feature_set,
    feature_version
HAVING COUNT(*) > 1;

CREATE OR REPLACE VIEW vw_feature_null_summary AS
SELECT
    exchange,
    symbol,
    timeframe,
    feature_set,
    feature_version,
    COUNT(*) AS row_count,
    COUNT(*) FILTER (WHERE simple_return IS NULL) AS simple_return_nulls,
    COUNT(*) FILTER (WHERE sma_20 IS NULL) AS sma_20_nulls,
    COUNT(*) FILTER (WHERE sma_50 IS NULL) AS sma_50_nulls,
    COUNT(*) FILTER (WHERE rolling_std_20 IS NULL) AS rolling_std_20_nulls,
    COUNT(*) FILTER (WHERE atr_14 IS NULL) AS atr_14_nulls,
    COUNT(*) FILTER (WHERE rsi_14 IS NULL) AS rsi_14_nulls,
    COUNT(*) FILTER (WHERE close_vs_high_52w IS NULL) AS close_vs_high_52w_nulls,
    COUNT(*) FILTER (WHERE volume_sma_20 IS NULL) AS volume_sma_20_nulls,
    COUNT(*) FILTER (WHERE body_to_range_ratio IS NULL) AS body_to_range_ratio_nulls
FROM ohlcv_features
GROUP BY
    exchange,
    symbol,
    timeframe,
    feature_set,
    feature_version;

CREATE OR REPLACE VIEW vw_feature_latest_by_symbol_timeframe AS
SELECT DISTINCT ON (exchange, symbol, timeframe, feature_set, feature_version)
    exchange,
    symbol,
    timeframe,
    feature_set,
    feature_version,
    timestamp AS latest_timestamp,
    run_id,
    validated_at,
    data_quality_score
FROM ohlcv_features
ORDER BY
    exchange,
    symbol,
    timeframe,
    feature_set,
    feature_version,
    timestamp DESC;
