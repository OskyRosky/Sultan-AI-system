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
