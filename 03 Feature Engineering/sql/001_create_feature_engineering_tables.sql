-- 03 Feature Engineering - Initial table proposal
-- Declarative SQL only. Do not execute as part of Bloque 1.

CREATE TABLE IF NOT EXISTS feature_runs (
    run_id UUID PRIMARY KEY,
    flow_name TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ,
    feature_set TEXT NOT NULL,
    feature_version TEXT NOT NULL,
    symbols TEXT[] NOT NULL,
    timeframes TEXT[] NOT NULL,
    rows_loaded BIGINT DEFAULT 0 CHECK (rows_loaded >= 0),
    rows_generated BIGINT DEFAULT 0 CHECK (rows_generated >= 0),
    rows_validated BIGINT DEFAULT 0 CHECK (rows_validated >= 0),
    rows_inserted BIGINT DEFAULT 0 CHECK (rows_inserted >= 0),
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS feature_quality_checks (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES feature_runs(run_id),
    check_name TEXT NOT NULL,
    check_status TEXT NOT NULL,
    severity TEXT NOT NULL,
    rows_checked BIGINT DEFAULT 0 CHECK (rows_checked >= 0),
    rows_failed BIGINT DEFAULT 0 CHECK (rows_failed >= 0),
    nulls_found BIGINT DEFAULT 0 CHECK (nulls_found >= 0),
    infinities_found BIGINT DEFAULT 0 CHECK (infinities_found >= 0),
    duplicates_found BIGINT DEFAULT 0 CHECK (duplicates_found >= 0),
    lookahead_violations BIGINT DEFAULT 0 CHECK (lookahead_violations >= 0),
    data_quality_score NUMERIC(6, 5) CHECK (data_quality_score BETWEEN 0 AND 1),
    error_message TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ohlcv_features (
    exchange TEXT NOT NULL,
    symbol TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    feature_set TEXT NOT NULL,
    feature_version TEXT NOT NULL,
    run_id UUID NOT NULL REFERENCES feature_runs(run_id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    validated_at TIMESTAMPTZ,
    data_quality_score NUMERIC(6, 5) NOT NULL CHECK (data_quality_score BETWEEN 0 AND 1),

    simple_return DOUBLE PRECISION,
    log_return DOUBLE PRECISION,
    close_open_return DOUBLE PRECISION,
    rolling_std_20 DOUBLE PRECISION,
    volatility_20 DOUBLE PRECISION,
    atr_14 DOUBLE PRECISION,
    sma_20 DOUBLE PRECISION,
    sma_50 DOUBLE PRECISION,
    ema_20 DOUBLE PRECISION,
    ema_50 DOUBLE PRECISION,
    price_above_sma20 BOOLEAN,
    sma20_slope DOUBLE PRECISION,
    ema20_above_ema50 BOOLEAN,
    rsi_14 DOUBLE PRECISION,
    macd DOUBLE PRECISION,
    macd_signal DOUBLE PRECISION,
    close_vs_high_52w DOUBLE PRECISION,
    rolling_max_20 DOUBLE PRECISION,
    rolling_min_20 DOUBLE PRECISION,
    volume_change DOUBLE PRECISION,
    volume_sma_20 DOUBLE PRECISION,
    volume_ratio_20 DOUBLE PRECISION,
    high_low_range DOUBLE PRECISION,
    body_size DOUBLE PRECISION,
    upper_wick DOUBLE PRECISION,
    lower_wick DOUBLE PRECISION,
    body_to_range_ratio DOUBLE PRECISION,

    CONSTRAINT ohlcv_features_unique_key UNIQUE (
        exchange,
        symbol,
        timeframe,
        timestamp,
        feature_set,
        feature_version
    )
);

CREATE INDEX IF NOT EXISTS idx_ohlcv_features_symbol_timeframe_timestamp
    ON ohlcv_features (symbol, timeframe, timestamp);

CREATE INDEX IF NOT EXISTS idx_ohlcv_features_run_id
    ON ohlcv_features (run_id);

CREATE INDEX IF NOT EXISTS idx_feature_quality_checks_run_id
    ON feature_quality_checks (run_id);
