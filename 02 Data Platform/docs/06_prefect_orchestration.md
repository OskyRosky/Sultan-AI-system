# Orquestación con Prefect

## Objetivo

Prefect será usado para ejecutar, observar y depurar pipelines locales de datos. En esta etapa se prioriza trazabilidad operacional simple antes de scheduling complejo.

## Flow inicial

`ingest_ohlcv_flow`

## Tasks esperadas

- `load_config`
- `fetch_ohlcv`
- `validate_ohlcv`
- `save_raw_parquet`
- `transform_to_curated`
- `save_curated_parquet`
- `upsert_postgres`
- `write_ingestion_run`
- `write_quality_report`

## Estado actual

La primera versión local fue ejecutada correctamente con Prefect.

Run exitoso:

- `run_id`: `faf0e84e-5b6e-4751-9664-7fcbda356d68`.
- `status`: `success`.
- `rows_fetched`: `2000`.
- `rows_validated`: `2000`.
- `rows_inserted`: `2000`.

Run con gaps/freshness:

- `run_id`: `26c5aba4-e626-41e7-a064-acad2c90c09e`.
- `status`: `success`.
- `rows_fetched`: `2000`.
- `rows_validated`: `2000`.
- `rows_inserted`: `2000`.
- `gaps_found`: `0`.
- `freshness_lag_seconds`: `83575`.
- `data_quality_score`: `1.00000`.

Runs de idempotencia:

- `4cd9c775-d7b8-40ed-8f7c-6e5c6ebdd096`: `status = success`, `rows_fetched = 2000`, `rows_validated = 2000`, `rows_inserted = 2000`.
- `e9e0dd92-9550-4519-9c0d-a43b50d191b5`: `status = success`, `rows_fetched = 2000`, `rows_validated = 2000`, `rows_inserted = 2000`.
- En ambos runs, el upsert reportó `rows_new = 0` y `rows_existing = 2000`.
- El total final de `ohlcv_curated` permaneció en `2000` filas.

Deployment local creado:

- Deployment: `ingest_ohlcv_flow/sultan-ohlcv-daily`.
- Work pool: `sultan-local-pool`.
- Tipo de work pool: `process`.
- Schedule anterior: `0 1 * * *`.
- Schedule operativo actual: `0 10 * * *`.
- Timezone: `America/Costa_Rica`.
- Prefect UI: `http://127.0.0.1:4200`.
- Estado validado: deployment y work pool visibles en Prefect; worker local probado correctamente.

## Modo operativo diario

El bootstrap inicial del historico completo se hizo con `SULTAN_OHLCV_MODE=full_history`.
Para operacion diaria el modo recomendado/default es `SULTAN_OHLCV_MODE=incremental`.

En modo incremental, el flow consulta `MAX(timestamp)` en `ohlcv_curated` por `exchange + symbol + timeframe` y descarga desde `MAX(timestamp) + intervalo` hasta el presente. Esto permite catch-up: si la computadora estuvo apagada uno o varios dias, el siguiente run descarga las velas faltantes sin duplicar barras.

Validacion operativa:

- Run incremental con nuevas velas: `rows_fetched = 4`, `rows_validated = 4`, `rows_inserted = 4`, `status = success`.
- Run incremental inmediato sin nuevas velas: `rows_fetched = 0`, `rows_validated = 0`, `rows_inserted = 0`, `status = success`.
- El deployment `ingest_ohlcv_flow/sultan-ohlcv-daily` quedo actualizado a `0 10 * * *` con timezone `America/Costa_Rica`.

## Tracking mínimo

Cada ejecución debe registrar:

- `run_id`
- nombre del flow
- fuente
- símbolos
- timeframes
- hora de inicio
- hora de fin
- estado
- filas obtenidas
- filas validadas
- filas insertadas
- filas nuevas y filas existentes en metadata del run
- gaps encontrados
- freshness lag en segundos
- metadata de calidad por símbolo/timeframe
- error, si aplica

## Alertas

Telegram queda fuera del primer bloque. Se agregará después de tener validaciones y registros confiables.

## Estado operativo despues de Repair Block 3B

Prefect sigue existiendo como framework de flow local y el codigo mantiene `@flow` y `@task`. Sin embargo, Prefect deployments no son el scheduler operativo actual porque el intento de usar Prefect Server local encontro:

```text
sqlite3.OperationalError: database is locked
```

No se migro Prefect a PostgreSQL en este bloque. La migracion de Prefect a PostgreSQL queda como mejora futura opcional, no como bloqueo para la operacion diaria OHLCV.

Scheduler operativo actual:

```text
launchd
```

Script ejecutado por launchd:

```text
02 Data Platform/scripts/run_ohlcv_reconciliation.sh
```

Comando efectivo del script:

```bash
PREFECT_API_URL= SULTAN_OHLCV_MODE=incremental poetry run python "02 Data Platform/flows/ingest_ohlcv_flow.py"
```

`PREFECT_API_URL` se deja vacio en el proceso para evitar depender del Prefect Server local bloqueado. Prefect usa servidor efimero para ejecutar el flow local.

LaunchAgents oficiales de Sultan-AI-system:

- `com.sultan.ohlcv.reconciliation.morning`: `10:05` America/Costa_Rica.
- `com.sultan.ohlcv.reconciliation.evening`: `18:05` America/Costa_Rica.

Ambos LaunchAgents llaman el mismo flow reconciliador. No existe un flow separado para la tarde. Si la ejecucion de la mañana no ocurre, la de la tarde debe detectar lo faltante desde PostgreSQL y completar. Si la ejecucion de la mañana si ocurre, la tarde solo agrega nuevas velas cerradas disponibles o termina sin filas nuevas, sin duplicar datos.

El cron externo:

```text
5 0 * * * bash /Users/sultan/Trading/algo-trading/tools/run_daily_job.sh
```

no pertenece a Sultan-AI-system, apunta a otro repo y el script no existe en esa ruta. No debe considerarse scheduler funcional de `02 Data Platform`.
