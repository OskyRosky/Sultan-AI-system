-- Sultan Data Platform - Initial PostgreSQL Tables
-- Scope: metadata, lineage, quality checks, and validated OHLCV.
-- This is an initial clear schema, not a complex migration system.

CREATE TABLE IF NOT EXISTS asset_universe (
    id BIGSERIAL PRIMARY KEY,
    exchange TEXT NOT NULL,
    symbol TEXT NOT NULL,
    base_asset TEXT,
    quote_asset TEXT,
    asset_class TEXT NOT NULL DEFAULT 'crypto',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (exchange, symbol)
);

CREATE TABLE IF NOT EXISTS data_sources (
    id BIGSERIAL PRIMARY KEY,
    source_name TEXT NOT NULL UNIQUE,
    provider TEXT NOT NULL,
    source_type TEXT NOT NULL,
    access_method TEXT NOT NULL,
    base_url TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
    run_id UUID PRIMARY KEY,
    flow_name TEXT NOT NULL,
    source_name TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TIMESTAMPTZ NOT NULL,
    finished_at TIMESTAMPTZ,
    symbols TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    timeframes TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    rows_fetched BIGINT NOT NULL DEFAULT 0,
    rows_validated BIGINT NOT NULL DEFAULT 0,
    rows_inserted BIGINT NOT NULL DEFAULT 0,
    raw_path TEXT,
    curated_path TEXT,
    error_message TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS data_quality_checks (
    id BIGSERIAL PRIMARY KEY,
    run_id UUID NOT NULL REFERENCES ingestion_runs(run_id) ON DELETE CASCADE,
    dataset_name TEXT NOT NULL,
    check_name TEXT NOT NULL,
    check_status TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'error',
    rows_checked BIGINT NOT NULL DEFAULT 0,
    rows_failed BIGINT NOT NULL DEFAULT 0,
    gaps_found INTEGER NOT NULL DEFAULT 0,
    freshness_lag_seconds BIGINT,
    data_quality_score NUMERIC(6, 5),
    error_message TEXT,
    checked_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE TABLE IF NOT EXISTS ohlcv_curated (
    id BIGSERIAL PRIMARY KEY,
    exchange TEXT NOT NULL,
    symbol TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    open NUMERIC(28, 12) NOT NULL,
    high NUMERIC(28, 12) NOT NULL,
    low NUMERIC(28, 12) NOT NULL,
    close NUMERIC(28, 12) NOT NULL,
    volume NUMERIC(38, 12) NOT NULL,
    source TEXT NOT NULL,
    run_id UUID NOT NULL REFERENCES ingestion_runs(run_id),
    ingested_at TIMESTAMPTZ NOT NULL,
    validated_at TIMESTAMPTZ NOT NULL,
    data_quality_score NUMERIC(6, 5) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT ohlcv_curated_unique_bar UNIQUE (exchange, symbol, timeframe, timestamp),
    CONSTRAINT ohlcv_curated_high_low CHECK (high >= low),
    CONSTRAINT ohlcv_curated_high_open CHECK (high >= open),
    CONSTRAINT ohlcv_curated_high_close CHECK (high >= close),
    CONSTRAINT ohlcv_curated_low_open CHECK (low <= open),
    CONSTRAINT ohlcv_curated_low_close CHECK (low <= close),
    CONSTRAINT ohlcv_curated_volume_nonnegative CHECK (volume >= 0),
    CONSTRAINT ohlcv_curated_quality_score_range CHECK (data_quality_score >= 0 AND data_quality_score <= 1)
);

CREATE INDEX IF NOT EXISTS idx_ingestion_runs_source_status
    ON ingestion_runs (source_name, status);

CREATE INDEX IF NOT EXISTS idx_ingestion_runs_started_at
    ON ingestion_runs (started_at DESC);

CREATE INDEX IF NOT EXISTS idx_data_quality_checks_run_id
    ON data_quality_checks (run_id);

CREATE INDEX IF NOT EXISTS idx_ohlcv_curated_lookup
    ON ohlcv_curated (exchange, symbol, timeframe, timestamp DESC);

