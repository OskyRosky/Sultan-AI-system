# Operacion Local con Prefect

## Objetivo

Prefect se usa en esta etapa para orquestar y observar el flow local `ingest_ohlcv_flow`. No ejecuta logica de trading, backtesting ni ordenes.

## Iniciar Prefect Server local

Desde la raiz del proyecto:

```bash
cd "/Users/sultan/Trading/Sultan-AI-system"
poetry run prefect server start
```

La UI queda disponible en:

```text
http://127.0.0.1:4200
```

La API local queda en:

```text
http://127.0.0.1:4200/api
```

Si la CLI no apunta al server local:

```bash
poetry run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

## Work pool local

Work pool creado:

```text
sultan-local-pool
```

Tipo:

```text
process
```

Para iniciar un worker local:

```bash
cd "/Users/sultan/Trading/Sultan-AI-system"
poetry run prefect worker start --pool sultan-local-pool
```

El worker debe estar activo para que un deployment ejecute runs.

## Flow y deployment

Flow:

```text
ingest_ohlcv_flow
```

Deployment:

```text
ingest_ohlcv_flow/sultan-ohlcv-daily
```

Entrypoint:

```text
02 Data Platform/flows/ingest_ohlcv_flow.py:ingest_ohlcv_flow
```

Work pool:

```text
sultan-local-pool
```

Schedule:

```text
0 10 * * *
```

Timezone:

```text
America/Costa_Rica
```

Hora operativa local:

```text
10:00 a.m. Costa Rica
```

El schedule anterior era `0 1 * * *`. Fue reemplazado por `0 10 * * *`.

## Modo diario incremental

El deployment diario debe operar con:

```text
SULTAN_OHLCV_MODE=incremental
```

`full_history` queda reservado para bootstrap inicial o recargas controladas. En operacion diaria, el flow consulta PostgreSQL para obtener `MAX(timestamp)` en `ohlcv_curated` por `exchange + symbol + timeframe`, luego descarga desde `MAX(timestamp) + intervalo` hasta el presente.

Si la computadora estuvo apagada o Prefect no estuvo activo durante varios dias, el siguiente run incremental hace catch-up desde el ultimo timestamp persistido. No borra datos y no duplica barras porque `ohlcv_curated` usa upsert idempotente con `ON CONFLICT`.

## Hardening del flow

- La conexion CCXT a Binance usa `enableRateLimit = True` y `timeout = 30000` ms.
- Si el flow ya registro `ingestion_runs.status = running` y ocurre una excepcion inesperada antes del cierre normal, el mismo `run_id` se actualiza a `status = failed`, `finished_at` y `error_message`.
- La excepcion se relanza para que Prefect marque el flow run como failed.
- El deployment diario no cambio: sigue usando `ingest_ohlcv_flow/sultan-ohlcv-daily`, work pool `sultan-local-pool`, cron `0 10 * * *` y timezone `America/Costa_Rica`.

## Ver flow y deployment

Listar flows:

```bash
poetry run prefect flow ls
```

Listar deployments:

```bash
poetry run prefect deployment ls
```

Inspeccionar el deployment:

```bash
poetry run prefect deployment inspect "ingest_ohlcv_flow/sultan-ohlcv-daily"
```

En la UI:

- Abrir `http://127.0.0.1:4200`.
- Ir a `Flows` para ver `ingest_ohlcv_flow`.
- Ir a `Deployments` para ver `sultan-ohlcv-daily`.
- Ir a `Work Pools` para ver `sultan-local-pool`.
- Ir a `Flow Runs` para ver historial de ejecuciones.

## Ejecutar manualmente el deployment

Con Prefect Server y worker activos:

```bash
poetry run prefect deployment run "ingest_ohlcv_flow/sultan-ohlcv-daily"
```

Tambien se puede ejecutar desde la UI usando el boton de run del deployment.

Nota operativa: este deployment ejecuta el modo configurado en `.env`. Para operacion diaria debe quedar en `incremental`.

## Confirmar que alimento PostgreSQL

Resumen OHLCV:

```bash
psql "postgresql://sultan_user:sultan_local_password@localhost:5432/sultan_ai" \
  -c "SELECT * FROM public.v_ohlcv_summary ORDER BY symbol, timeframe;"
```

Ultimos runs:

```bash
psql "postgresql://sultan_user:sultan_local_password@localhost:5432/sultan_ai" \
  -c "SELECT run_id, flow_name, source_name, status, rows_fetched, rows_validated, rows_inserted, error_message FROM public.ingestion_runs ORDER BY started_at DESC LIMIT 5;"
```

Data quality:

```bash
psql "postgresql://sultan_user:sultan_local_password@localhost:5432/sultan_ai" \
  -c "SELECT run_id, check_status, rows_checked, rows_failed, gaps_found, freshness_lag_seconds, data_quality_score, error_message FROM public.data_quality_checks ORDER BY checked_at DESC LIMIT 5;"
```

Para confirmar catch-up incremental, revisar tambien `ingestion_runs.metadata`, donde queda el ultimo timestamp existente y el timestamp inicial usado para fetch por cada `symbol/timeframe`.

## Detener Prefect Server

En la terminal donde corre el server:

```text
Ctrl+C
```

Para detener un worker, usar `Ctrl+C` en la terminal del worker.

## Si Prefect no aparece

- Confirmar que el server esta activo: `poetry run prefect server start`.
- Confirmar que la CLI apunta a `http://127.0.0.1:4200/api`.
- Confirmar que el work pool existe: `poetry run prefect work-pool ls`.
- Confirmar que el deployment existe: `poetry run prefect deployment ls`.
- Si el deployment aparece como `NOT_READY`, iniciar el worker: `poetry run prefect worker start --pool sultan-local-pool`.
