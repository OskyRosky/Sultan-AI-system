# Arquitectura de Ingesta

## Objetivo

La ingesta debe capturar datos externos con trazabilidad completa, persistir una copia raw inmutable y promover solo datos validados a `curated`.

## Pipeline inicial ejecutado

Flow: `ingest_ohlcv_flow`

Tasks:

- `load_config`: carga configuración local y variables de entorno.
- `fetch_ohlcv`: obtiene OHLCV desde Binance vía CCXT.
- `validate_ohlcv`: valida columnas mínimas, nulos, reglas OHLC, volumen y duplicados.
- `save_raw_parquet`: guarda la copia raw en Parquet.
- `transform_to_curated`: normaliza campos y tipos para capa curated.
- `save_curated_parquet`: persiste Parquet validado.
- `upsert_postgres`: inserta o actualiza registros validados en PostgreSQL.
- `write_ingestion_run`: registra estado del run.
- `write_quality_report`: registra resultado de validaciones.

## Política raw

La capa raw debe preservar el dato lo más cercano posible a la fuente, agregando metadata mínima:

- `source`
- `run_id`
- `ingested_at`

## Política curated

La capa curated solo recibe datos que no tengan errores estructurales bloqueantes. Si hay errores de contrato, duplicados dentro del lote o campos nulos críticos, el lote no debe promoverse.

Los gaps históricos detectados en Binance son warnings auditables. No se imputan datos, no se rellenan velas y no se bloquea el histórico estructuralmente válido por gaps de disponibilidad o mantenimiento del exchange.

## Idempotencia

El flow puede ejecutarse repetidamente sobre las mismas velas sin duplicar barras en `ohlcv_curated`.

Mecanismo:

- Clave lógica: `exchange + symbol + timeframe + timestamp`.
- PostgreSQL usa `ON CONFLICT (exchange, symbol, timeframe, timestamp) DO UPDATE`.
- Si una barra ya existe, se actualizan valores OHLCV, `run_id`, `ingested_at`, `validated_at` y `data_quality_score`.
- `ingestion_runs` registra cada ejecución con un nuevo `run_id`.
- `data_quality_checks` registra cada ejecución.

Resultado de doble ejecución controlada:

- Run `4cd9c775-d7b8-40ed-8f7c-6e5c6ebdd096`: `rows_fetched = 2000`, `rows_validated = 2000`, `rows_inserted = 2000`, `rows_new = 0`, `rows_existing = 2000`.
- Run `e9e0dd92-9550-4519-9c0d-a43b50d191b5`: `rows_fetched = 2000`, `rows_validated = 2000`, `rows_inserted = 2000`, `rows_new = 0`, `rows_existing = 2000`.
- Total final en `ohlcv_curated`: `2000` filas.

## Ejecución

La primera versión local fue ejecutada correctamente con Prefect.

Resultado confirmado:

- Fuente: Binance público vía CCXT.
- Símbolos: `BTCUSDT`, `ETHUSDT`.
- Timeframes: `1d`, `4h`.
- Filas descargadas: `2000`.
- Filas validadas: `2000`.
- Filas insertadas en PostgreSQL: `2000`.
- Raw Parquet escrito en `data/raw/binance/{symbol}/{timeframe}/{year}/{month}/`.
- Curated Parquet escrito en `data/curated/ohlcv/{symbol}/{timeframe}/`.
- Run registrado en `ingestion_runs` con `status = success`.
- Quality check registrado en `data_quality_checks` con `check_status = passed`.

Resultado histórico completo:

- Modo: `full_history`.
- Fuente: Binance público vía CCXT.
- Run: `2a979115-402f-4243-aef1-8c5aead2cc89`.
- Estado: `success_with_warnings`.
- Filas descargadas: `44612`.
- Filas validadas: `44612`.
- Filas insertadas/actualizadas: `44612`.
- `BTCUSDT 1d`: `3189` filas, `2017-08-17 00:00:00 UTC` a `2026-05-10 00:00:00 UTC`.
- `BTCUSDT 4h`: `19117` filas, `2017-08-17 04:00:00 UTC` a `2026-05-10 20:00:00 UTC`.
- `ETHUSDT 1d`: `3189` filas, `2017-08-17 00:00:00 UTC` a `2026-05-10 00:00:00 UTC`.
- `ETHUSDT 4h`: `19117` filas, `2017-08-17 04:00:00 UTC` a `2026-05-10 20:00:00 UTC`.

No se define deployment programado todavía.
