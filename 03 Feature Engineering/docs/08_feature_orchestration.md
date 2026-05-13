# Feature Orchestration

## Flow esperado

Nombre objetivo:

- `generate_features_flow`

Tasks esperadas:

- `load_feature_config`
- `check_ohlcv_freshness`
- `load_ohlcv_data`
- `calculate_features`
- `validate_features`
- `save_features_parquet`
- `upsert_features_postgres`
- `write_feature_run`
- `write_feature_quality_report`

## Secuencia

```text
load_feature_config
-> check_ohlcv_freshness
-> load_ohlcv_data
-> calculate_features
-> validate_features
-> save_features_parquet
-> upsert_features_postgres
-> write_feature_run
-> write_feature_quality_report
```

## Estrategia de adopción

Primero se ejecutará localmente. Luego, cuando existan cálculos reales, validaciones y almacenamiento probado, se evaluará crear deployment Prefect.

No se define schedule todavía. No debe ejecutarse automáticamente hasta validar features reales, calidad, persistencia y auditoría.

## Estado Bloque 1

El flow actual es mock/no-op. No consulta PostgreSQL, no calcula features reales, no escribe Parquet, no inserta registros y no crea deployment.
