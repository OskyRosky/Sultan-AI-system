# Bloque 13 - Feature Monitoring & Inspection

## Objetivo

Crear una capa de inspeccion operativa para Feature Engineering usando vistas SQL read-only y queries de monitoreo en PostgreSQL local `sultan_ai`.

Este bloque pertenece al subcomponente oficial `09 Feature Monitoring & Inspection`.

## Vistas Creadas

### `vw_feature_latest_runs`

Muestra los ultimos runs de Feature Engineering:

- `run_id`
- `flow_name`
- `status`
- `feature_set`
- `feature_version`
- row counts
- timestamps de inicio/cierre
- `data_quality_score`
- `error_message`

Uso principal: responder cual fue el ultimo run y si paso o fallo.

### `vw_feature_quality_latest`

Muestra checks recientes de quality:

- `integrated`
- familias tecnicas
- status
- severity
- rows checked/failed
- score
- error message

Uso principal: identificar rapidamente que checks fallaron.

### `vw_feature_storage_summary`

Agrupa `ohlcv_features` por `exchange`, `symbol`, `timeframe`, `feature_set`, `feature_version`.

Incluye:

- `row_count`
- `min_timestamp`
- `max_timestamp`
- `latest_run_id`
- `avg_data_quality_score`
- `max_validated_at`

Uso principal: verificar cobertura por symbol/timeframe.

### `vw_feature_duplicate_check`

Detecta duplicados por unique key:

```text
exchange, symbol, timeframe, timestamp, feature_set, feature_version
```

Debe devolver cero filas en estado sano.

### `vw_feature_null_summary`

Resume nulls en columnas clave:

- `simple_return`
- `sma_20`
- `sma_50`
- `rolling_std_20`
- `atr_14`
- `rsi_14`
- `close_vs_high_52w`
- `volume_sma_20`
- `body_to_range_ratio`

Uso principal: revisar warm-up esperado y detectar nulls inesperados.

### `vw_feature_latest_by_symbol_timeframe`

Muestra ultimo timestamp, `run_id`, `validated_at` y score por symbol/timeframe.

Uso principal: inspeccionar freshness de features almacenadas.

## Resultado de Validacion

Las vistas fueron creadas con:

```bash
psql -d sultan_ai -f "03 Feature Engineering/sql/003_create_feature_monitoring_views.sql"
```

Validacion observada:

- `vw_feature_latest_runs`: 2 runs `passed`.
- `vw_feature_quality_latest`: 16 checks.
- `vw_feature_storage_summary`: `BTCUSDT / 1d` con 200 filas.
- `vw_feature_duplicate_check`: 0 filas.
- `vw_feature_null_summary`: warm-up esperado en columnas rolling.
- `vw_feature_latest_by_symbol_timeframe`: ultimo timestamp `BTCUSDT / 1d`.

## DBeaver

En DBeaver:

1. Abrir conexion local a `sultan_ai`.
2. Ir a `public -> Views`.
3. Abrir las vistas `vw_feature_*`.
4. Usar filtros por `symbol`, `timeframe`, `feature_set` y `feature_version`.

Queries recomendadas:

```sql
SELECT * FROM vw_feature_latest_runs LIMIT 10;
SELECT * FROM vw_feature_quality_latest LIMIT 20;
SELECT * FROM vw_feature_storage_summary;
SELECT * FROM vw_feature_duplicate_check LIMIT 20;
SELECT * FROM vw_feature_null_summary;
SELECT * FROM vw_feature_latest_by_symbol_timeframe;
```

## Checklist Manual Despues de Cada Run

- Ultimo run esta `passed`.
- `rows_loaded`, `rows_generated`, `rows_validated` y `rows_inserted` son coherentes.
- `data_quality_score` esta dentro de rango esperado.
- No hay checks `failed`.
- `vw_feature_duplicate_check` devuelve cero filas.
- `vw_feature_storage_summary` muestra cobertura esperada.
- `latest_run_id` coincide con el ultimo run que escribio features.
- Nulls corresponden a warm-up esperado.

## Alertas Manuales

Revisar manualmente si aparece:

- run `failed`;
- `rows_inserted = 0` cuando storage estaba habilitado;
- `data_quality_score < 1.0` sin explicacion esperada;
- duplicados en `vw_feature_duplicate_check`;
- nulls fuera de warm-up;
- `max_timestamp` atrasado frente a OHLCV fuente.

## Fuera de Alcance

No hay Grafana todavia, no hay alerting automatico y no hay deployment Prefect.

## Proximo Paso

Avanzar a `11 Feature Closure` cuando Monitoring & Inspection quede revisado manualmente en DBeaver.
