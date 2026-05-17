# Feature Monitoring and Inspection

## Proposito

La inspeccion operativa permite revisar que cada ejecucion de features sea completa, trazable y consistente con OHLCV fuente.

## Objetos Operativos

Tablas:

- `feature_runs`
- `feature_quality_checks`
- `ohlcv_features`

Vistas:

- `vw_feature_latest_runs`
- `vw_feature_quality_latest`
- `vw_feature_storage_summary`
- `vw_feature_duplicate_check`
- `vw_feature_null_summary`
- `vw_feature_latest_by_symbol_timeframe`

## Uso en DBeaver

Abrir la conexion local a `sultan_ai` y revisar `public -> Views`.

Queries recomendadas:

```sql
SELECT * FROM vw_feature_latest_runs LIMIT 10;
SELECT * FROM vw_feature_quality_latest LIMIT 20;
SELECT * FROM vw_feature_storage_summary;
SELECT * FROM vw_feature_duplicate_check LIMIT 20;
SELECT * FROM vw_feature_null_summary;
SELECT * FROM vw_feature_latest_by_symbol_timeframe;
```

## Checks Minimos

- Ultimo run `passed`.
- `data_quality_score` presente.
- Quality checks sin fallos.
- `ohlcv_features` con filas por symbol/timeframe esperado.
- `vw_feature_duplicate_check` sin filas.
- Nulls consistentes con warm-up.
- `latest_run_id` coherente con el ultimo upsert.

## Estado Actual

Bloque 13 crea y valida la capa v1 de vistas read-only para inspeccion manual.

No hay Grafana ni alertas automaticas todavia.
