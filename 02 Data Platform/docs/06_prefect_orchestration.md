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

No se crearán deployments programados todavía.

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
- error, si aplica

## Alertas

Telegram queda fuera del primer bloque. Se agregará después de tener validaciones y registros confiables.
