# Arquitectura de Ingesta

## Objetivo

La ingesta debe capturar datos externos con trazabilidad completa, persistir una copia raw inmutable y promover solo datos validados a `curated`.

## Pipeline inicial ejecutado

Flow: `ingest_ohlcv_flow`

Tasks:

- `load_config`: carga configuración local y variables de entorno.
- `fetch_ohlcv`: obtiene OHLCV desde Binance vía CCXT.
- `filter_closed_candles`: excluye velas abiertas antes de curated/PostgreSQL.
- `validate_ohlcv`: valida columnas mínimas, nulos, reglas OHLC, volumen y duplicados.
- `save_raw_parquet`: guarda la copia raw en Parquet.
- `transform_to_curated`: normaliza campos y tipos para capa curated.
- `save_curated_parquet`: persiste Parquet validado.
- `upsert_postgres`: inserta o actualiza registros validados en PostgreSQL.
- `finalize_reconciliation_health`: calcula salud posterior al upsert por símbolo/timeframe.
- `write_ingestion_run`: registra estado del run.
- `write_quality_report`: registra resultado de validaciones.

## Política raw

La capa raw debe preservar el dato lo más cercano posible a la fuente, agregando metadata mínima:

- `source`
- `run_id`
- `ingested_at`

Raw Parquet puede contener la respuesta original recibida desde Binance/CCXT, incluyendo la ultima vela abierta si Binance la devuelve. Esa copia existe para auditoria de ingesta y no implica promocion a curated.

## Política curated

La capa curated solo recibe datos que no tengan errores estructurales bloqueantes. Si hay errores de contrato, duplicados dentro del lote o campos nulos críticos, el lote no debe promoverse.

Desde el hardening previo al catch-up de 2026-06-06, curated y PostgreSQL solo aceptan velas cerradas. El flow calcula `close_time` en memoria:

- `1d`: `timestamp + 1 day`.
- `4h`: `timestamp + 4 hours`.

Una vela solo puede pasar a curated si `close_time <= now_utc`. No se agrega columna `close_time` a PostgreSQL.

Los gaps históricos detectados en Binance son warnings auditables. No se imputan datos, no se rellenan velas y no se bloquea el histórico estructuralmente válido por gaps de disponibilidad o mantenimiento del exchange.

## Modo incremental y overlap

El modo incremental ya no empieza estrictamente en `MAX(timestamp) + intervalo`. Para reducir el riesgo de dejar una ultima vela provisional sin corregir, el flow usa una ventana de solape configurable:

```text
SULTAN_OHLCV_INCREMENTAL_OVERLAP_CANDLES=1
```

Con datos existentes, el inicio incremental se calcula como:

```text
max(latest_stored_before_run - overlap_candles * timeframe_interval, symbol_start_date)
```

La politica default vuelve a descargar al menos la ultima vela persistida previamente y una vela adicional anterior por `symbol/timeframe`. El upsert idempotente actualiza registros existentes y evita duplicados.

Este hardening prepara una futura reparacion segura del gap. No ejecuta catch-up, no ejecuta `full_history`, no modifica schedules y no repara datos por si mismo.

## Reconciliacion incremental

Desde Repair Block 1B, cada corrida incremental debe comportarse como un proceso reconciliador:

```text
verificar estado actual
detectar faltantes reales
descargar el rango necesario con overlap
validar velas cerradas
guardar sin duplicar
reportar salud posterior
```

Antes de descargar, el flow calcula por `symbol/timeframe`:

- `latest_stored_before_run`: ultimo timestamp persistido en `ohlcv_curated`.
- `latest_closed_expected_timestamp`: ultima apertura de vela que deberia estar cerrada segun `now_utc`.
- `missing_from_timestamp` y `missing_to_timestamp`: rango cerrado faltante esperado.
- `expected_missing_closed_candles_before_run`: numero de velas cerradas faltantes antes del run.
- `is_already_caught_up_before_run`: si la serie ya estaba al dia antes de descargar.
- `incremental_start_timestamp`: inicio real de descarga, incluyendo overlap conservador.

La convencion de Binance se mantiene: `timestamp` representa apertura de vela. Para `1d`, la ultima vela cerrada esperada es la ultima apertura diaria cuyo `timestamp + 1 day <= now_utc`. Para `4h`, es la ultima apertura 4h cuyo `timestamp + 4 hours <= now_utc`.

Despues del upsert, el flow recalcula el ultimo timestamp disponible y registra:

- `latest_stored_after_run`.
- `is_caught_up_after_run`.
- `missing_closed_candles_after_run`.
- `remaining_gap_start` y `remaining_gap_end`.
- `health_status`.

Estados de salud permitidos:

- `caught_up`.
- `caught_up_with_historical_warnings`.
- `gap_remaining`.
- `no_new_closed_candles`.
- `failed_validation`.

Los gaps se reportan; no se imputan datos. Si queda una vela cerrada faltante que Binance debio devolver, la metadata debe indicar `gap_remaining`.

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

El deployment diario `ingest_ohlcv_flow/sultan-ohlcv-daily` queda definido en Prefect con schedule `0 10 * * *` y timezone `America/Costa_Rica`.
