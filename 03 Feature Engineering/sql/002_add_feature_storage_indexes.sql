-- 03 Feature Engineering - Feature storage index readiness.
-- Declarative SQL only. Do not execute automatically in Bloque 11B.

CREATE INDEX IF NOT EXISTS idx_ohlcv_features_set_version
    ON ohlcv_features (feature_set, feature_version);
