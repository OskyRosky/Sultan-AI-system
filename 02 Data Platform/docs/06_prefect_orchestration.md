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

## Estado inicial

La primera versión será ejecutada localmente. No se crearán deployments programados todavía.

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

