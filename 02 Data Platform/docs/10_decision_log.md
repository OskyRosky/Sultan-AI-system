# Decision Log

## 2026-05-10 - Separación entre artefactos de etapa y datos reales

Decisión: `02 Data Platform/` contiene documentación, schemas, SQL, flows, notebooks, mockups, reportes y logs de la etapa. Los datos físicos reales se guardan en `data/`.

Razón: evita mezclar diseño de plataforma con datasets versionables o pesados.

## 2026-05-10 - Primer dataset: OHLCV Binance

Decisión: el primer pipeline real usará Binance vía CCXT para OHLCV de `BTCUSDT` y `ETHUSDT` en `1d` y `4h`.

Razón: es un alcance pequeño, líquido y suficiente para validar arquitectura de ingesta, calidad y almacenamiento.

## 2026-05-10 - Prefect local antes de deployments

Decisión: iniciar con flow local `ingest_ohlcv_flow` sin deployment programado.

Razón: primero se validan contratos, persistencia y tracking antes de automatizar scheduling.

## 2026-05-10 - TimescaleDB pospuesto

Decisión: usar PostgreSQL 16 inicialmente sin TimescaleDB.

Razón: reduce complejidad operativa de la etapa inicial.

## 2026-05-10 - Pandera para validación tabular

Decisión: usar Pandera como primera herramienta de validación de OHLCV.

Razón: integra bien con pandas y permite expresar contratos de datos tabulares en Python.

## 2026-05-10 - Primer flow real mínimo OHLCV funcional

Decisión: se confirmó una primera versión funcional local de `ingest_ohlcv_flow` para OHLCV de Binance.

Resultado: el run `faf0e84e-5b6e-4751-9664-7fcbda356d68` descargó `2000` filas para `BTCUSDT` y `ETHUSDT` en timeframes `1d` y `4h`, validó `2000` filas, escribió raw Parquet, escribió curated Parquet, insertó `2000` filas en `ohlcv_curated`, registró `ingestion_runs` con `status = success` y registró `data_quality_checks` con `check_status = passed`.

Razón: se alcanzó el primer objetivo de punta a punta de la plataforma de datos mínima.

Decisión operativa: no optimizar todavía ni ampliar fuentes hasta completar una primera versión estable de la etapa `02 Data Platform`.

## 2026-05-10 - Gaps y freshness implementados en flow mínimo

Decisión: se implementó detección formal de gaps y cálculo de freshness dentro de `ingest_ohlcv_flow` sin modificar arquitectura ni SQL.

Resultado: el run `26c5aba4-e626-41e7-a064-acad2c90c09e` terminó con `status = success`, `rows_fetched = 2000`, `rows_validated = 2000`, `rows_inserted = 2000`, `gaps_found = 0`, `freshness_lag_seconds = 83575` y `data_quality_score = 1.00000`.

Detalle: los gaps se calculan por `exchange + symbol + timeframe`, usando 1 día para `1d` y 4 horas para `4h`. Freshness se calcula como `now_utc - max(timestamp)`. El detalle por símbolo/timeframe queda registrado en `data_quality_checks.metadata`.

Razón: completar el contrato mínimo de calidad operativo antes de avanzar a scheduling, más pares o nuevas fuentes.

## 2026-05-10 - Idempotencia de re-runs OHLCV validada

Decisión: mantener `ON CONFLICT (exchange, symbol, timeframe, timestamp) DO UPDATE` para `ohlcv_curated`.

Resultado: se ejecutó una doble corrida controlada del flow OHLCV. Los runs `4cd9c775-d7b8-40ed-8f7c-6e5c6ebdd096` y `e9e0dd92-9550-4519-9c0d-a43b50d191b5` terminaron con `status = success`, `rows_fetched = 2000`, `rows_validated = 2000` y `rows_inserted = 2000`. En ambos casos el upsert detectó `rows_new = 0` y `rows_existing = 2000`.

Confirmación: el total final de `ohlcv_curated` permaneció en `2000` filas, con `500` filas por cada combinación de `BTCUSDT`/`ETHUSDT` y `1d`/`4h`. `ingestion_runs` y `data_quality_checks` registraron cada ejecución.

Razón: el sistema debe permitir re-runs auditables sin duplicar barras OHLCV.

## 2026-05-10 - Vistas operativas para inspección PostgreSQL

Decisión: crear vistas SQL simples para inspeccionar datos OHLCV, pipeline runs y data quality sin modificar tablas existentes.

Resultado: se agregó `002_operational_views.sql` con `v_ohlcv_summary`, `v_ohlcv_latest_bars`, `v_pipeline_runs_latest`, `v_data_quality_latest` y `v_ohlcv_operational_health`.

Razón: habilitar inspección clara en PostgreSQL y DBeaver antes de agregar dashboards o nuevas fuentes.

## 2026-05-10 - Histórico completo OHLCV con gaps auditables

Decisión: tratar gaps históricos de Binance como warnings auditables cuando no existan errores estructurales bloqueantes.

Resultado: el run `2a979115-402f-4243-aef1-8c5aead2cc89` descargó y validó `44612` filas en modo `full_history`, escribió curated Parquet y actualizó `ohlcv_curated`. El estado del run fue `success_with_warnings` y `data_quality_checks.check_status = passed_with_warnings`.

Rangos cargados: `BTCUSDT 1d` con `3189` filas, `BTCUSDT 4h` con `19117` filas, `ETHUSDT 1d` con `3189` filas y `ETHUSDT 4h` con `19117` filas. Los rangos van desde `2017-08-17` hasta `2026-05-10`, según disponibilidad de Binance.

Data quality: `gaps_found = 16`, con `8` gaps en `BTCUSDT 4h` y `8` gaps en `ETHUSDT 4h`; `rows_failed = 0`; `data_quality_score = 0.95000`. No se imputaron datos ni se rellenaron velas.

Razón: en históricos reales de exchange pueden existir gaps por mantenimiento, listing o disponibilidad de datos. La plataforma debe auditarlos sin bloquear datos OHLCV estructuralmente válidos.

## 2026-05-10 - Deployment local Prefect diario

Decisión: crear un deployment local diario para `ingest_ohlcv_flow` usando Prefect Server local y un work pool tipo `process`.

Resultado: se creó el deployment `ingest_ohlcv_flow/sultan-ohlcv-daily` con id `64345509-70a4-420b-973e-10754115e1e2`, work pool `sultan-local-pool`, cron `0 1 * * *` y timezone `America/Costa_Rica`. El deployment quedó visible en Prefect UI y el work pool fue validado con un worker local.

Razón: dejar la ingesta OHLCV preparada como job operativo diario sin introducir Airflow, infraestructura adicional ni cambios en la lógica de ingesta.

## 2026-05-10 - Operacion diaria incremental y schedule 10:00 a.m.

Decisión: mantener `full_history` para bootstrap inicial y usar `incremental` como modo operativo diario del flow OHLCV.

Resultado: el deployment `ingest_ohlcv_flow/sultan-ohlcv-daily` fue actualizado de `0 1 * * *` a `0 10 * * *` con timezone `America/Costa_Rica`, manteniendo el mismo deployment id `64345509-70a4-420b-973e-10754115e1e2` y el work pool `sultan-local-pool`.

Validación: una corrida incremental descargó `4` velas nuevas desde `MAX(timestamp) + intervalo`, validó `4` filas e insertó/actualizó `4` filas. Una segunda corrida inmediata terminó con `status = success` y `0` filas, confirmando que el flow no falla cuando la data ya está actualizada.

Razón: el job diario no debe repetir el histórico completo. Debe completar desde el último timestamp disponible en PostgreSQL y permitir catch-up si la computadora o Prefect estuvieron apagados durante varios días.

## 2026-05-11 - Hardening minimo antes de cerrar Data Platform v1

Decision: aplicar fixes puntuales sin redisenar arquitectura ni cambiar el deployment diario.

Resultado: `v_ohlcv_operational_health` fue corregida para no propagar el ultimo `data_quality_checks` global a todos los `symbol/timeframe`. La vista conserva las columnas operativas principales y agrega contexto `latest_global_*` y `latest_symbol_timeframe_summary`.

Resultado: `ingest_ohlcv_flow` protege `ingestion_runs` contra runs huerfanos en `status = running`; si ocurre una excepcion despues del registro inicial, el mismo `run_id` se actualiza a `status = failed` con `finished_at` y `error_message`, y la excepcion se relanza para que Prefect marque el flow como failed.

Resultado: la instancia `ccxt.binance` mantiene `enableRateLimit = True` y ahora usa `timeout = 30000` ms.

Confirmacion: no se cambio la arquitectura, no se agregaron fuentes, no se agrego logica de trading y el deployment diario sigue en `0 10 * * *` con timezone `America/Costa_Rica`.
