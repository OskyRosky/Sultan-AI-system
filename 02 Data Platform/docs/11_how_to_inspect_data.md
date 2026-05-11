# Como Inspeccionar Datos en PostgreSQL

## Objetivo

Esta guia explica como inspeccionar la data operativa de Sultan en PostgreSQL usando vistas simples. No ejecuta pipelines ni descarga datos.

## Vistas operativas

Las vistas creadas en `02 Data Platform/sql/002_operational_views.sql` son:

- `v_ohlcv_summary`: resumen por `exchange`, `symbol` y `timeframe`.
- `v_ohlcv_latest_bars`: velas OHLCV ordenables por timestamp.
- `v_pipeline_runs_latest`: ultimos runs del pipeline.
- `v_data_quality_latest`: ultimos checks de calidad.
- `v_ohlcv_operational_health`: vista compacta de salud operativa por `symbol` y `timeframe`.

## Crear o actualizar las vistas

Desde la raiz del proyecto:

```bash
cd "/Users/sultan/Trading/Sultan-AI-system"
psql "postgresql://sultan_user:sultan_local_password@localhost:5432/sultan_ai" \
  -f "02 Data Platform/sql/002_operational_views.sql"
```

## Ver resumen de BTC/ETH 1d/4h

```sql
SELECT *
FROM v_ohlcv_summary
ORDER BY symbol, timeframe;
```

Campos clave:

- `rows_count`: numero de barras disponibles.
- `min_timestamp`: primera vela disponible.
- `max_timestamp`: ultima vela disponible.
- `last_close`: ultimo cierre disponible.
- `last_volume`: volumen de la ultima vela.

## Ver ultimas velas

```sql
SELECT symbol, timeframe, timestamp, open, high, low, close, volume
FROM v_ohlcv_latest_bars
ORDER BY symbol, timeframe, timestamp DESC
LIMIT 20;
```

Para inspeccionar un caso especifico:

```sql
SELECT *
FROM v_ohlcv_latest_bars
WHERE symbol = 'BTCUSDT'
  AND timeframe = '1d'
ORDER BY timestamp DESC
LIMIT 20;
```

## Ver ultimos pipeline runs

```sql
SELECT *
FROM v_pipeline_runs_latest
LIMIT 10;
```

Campos clave:

- `status`: estado final del run.
- `rows_fetched`: filas descargadas.
- `rows_validated`: filas que pasaron validacion.
- `rows_inserted`: filas afectadas por el upsert.
- `metadata`: rutas Parquet y detalle operativo adicional.

## Ver data quality

```sql
SELECT run_id, dataset_name, check_status, rows_checked, gaps_found,
       freshness_lag_seconds, data_quality_score, checked_at
FROM v_data_quality_latest
LIMIT 10;
```

Interpretacion:

- `gaps_found = 0`: no se detectaron saltos entre velas segun el timeframe.
- `gaps_found > 0`: hay gaps auditables; revisar `metadata` para detalle por simbolo/timeframe.
- `freshness_lag_seconds`: diferencia entre `now_utc` y el `max(timestamp)` observado.
- `data_quality_score = 1.00000`: el lote paso la validacion minima.
- `data_quality_score = 0.95000`: el lote paso con warnings auditables, normalmente gaps historicos.
- `check_status = passed`: el lote puede pasar a curated/PostgreSQL.
- `check_status = passed_with_warnings`: el lote paso a curated/PostgreSQL, pero requiere seguimiento operativo.
- `check_status = failed`: el lote no debe pasar a curated/PostgreSQL.

## Ver salud operativa OHLCV

```sql
SELECT *
FROM v_ohlcv_operational_health
ORDER BY symbol, timeframe;
```

Esta vista combina conteos y timestamps de OHLCV con el ultimo estado global de calidad registrado para el dataset `ohlcv`.

La vista no copia metricas globales sobre todos los pares/timeframes. Las columnas `latest_global_*` muestran el ultimo quality check global. Las columnas `latest_data_quality_score`, `latest_gaps_found`, `latest_freshness_lag_seconds` y `latest_check_status` se llenan solo cuando `data_quality_checks.metadata` contiene detalle para ese `symbol/timeframe`; si no existe detalle en el ultimo run, quedan en `NULL` y `latest_symbol_timeframe_summary` lo indica.

## Uso en DBeaver

1. Abrir la conexion PostgreSQL `sultan_ai`.
2. Ir a `Schemas` y seleccionar el schema publico.
3. Abrir `Views`.
4. Seleccionar una vista, por ejemplo `v_ohlcv_summary`.
5. Usar `View Data` para inspeccionar resultados.
6. Para filtros especificos, abrir un SQL Editor y ejecutar las consultas de esta guia.

## Lectura rapida

- Si `rows_count` es estable tras re-runs, la idempotencia esta funcionando.
- Si `max_timestamp` avanza en nuevas ejecuciones, hay data mas reciente.
- Si `gaps_found` es mayor que cero, el lote debe revisarse, pero no implica datos imputados.
- Si `freshness_lag_seconds` crece demasiado, la data puede estar desactualizada.
- Si `data_quality_score` baja a `0.00000`, la validacion fallo.

## Rango historico cargado

El run historico completo `2a979115-402f-4243-aef1-8c5aead2cc89` dejo estos rangos en PostgreSQL:

- `BTCUSDT 1d`: `3189` filas, desde `2017-08-17 00:00:00 UTC` hasta `2026-05-10 00:00:00 UTC`.
- `BTCUSDT 4h`: `19117` filas, desde `2017-08-17 04:00:00 UTC` hasta `2026-05-10 20:00:00 UTC`.
- `ETHUSDT 1d`: `3189` filas, desde `2017-08-17 00:00:00 UTC` hasta `2026-05-10 00:00:00 UTC`.
- `ETHUSDT 4h`: `19117` filas, desde `2017-08-17 04:00:00 UTC` hasta `2026-05-10 20:00:00 UTC`.
