# Sultan Data Platform - Overview

## Objetivo

La etapa `02 Data Platform` define la base de datos, trazabilidad, validación y monitoreo operativo para Sultan. El objetivo es construir una plataforma data-first, risk-first y audit-first antes de crear estrategias, backtesting, agentes LLM o ejecución de órdenes.

## Alcance de esta etapa

Esta etapa cubre:

- Capa 1: fuentes de datos.
- Capa 2: ingesta y almacenamiento.
- Capa T1: data quality, metadata y lineage.
- Monitoreo operativo inicial con Prefect.

No cubre:

- Trading con dinero real.
- Lógica de estrategias.
- Backtesting.
- Agentes LLM.
- Ejecución de órdenes.
- Airflow.
- TimescaleDB.

## Principios

- Todo dato debe tener fuente, timestamp, run_id, validación y trazabilidad.
- Ningún dato inválido debe pasar a `curated`.
- Los datos físicos reales viven fuera de esta carpeta, en `data/`.
- Los artefactos de diseño, SQL, schemas, flows y reportes viven en `02 Data Platform/`.
- Primero se construye confiabilidad de datos; después features; después research.

## Primer pipeline real mínimo ejecutado

El primer pipeline real mínimo, `ingest_ohlcv_flow`, fue ejecutado correctamente de forma local con Prefect.

Resultado confirmado:

- Fuente: Binance público vía CCXT.
- Símbolos: `BTCUSDT`, `ETHUSDT`.
- Timeframes: `1d`, `4h`.
- Filas descargadas: `2000`.
- Filas validadas: `2000`.
- Filas insertadas en PostgreSQL: `2000`.
- Run exitoso: `faf0e84e-5b6e-4751-9664-7fcbda356d68`.
- Run con gaps/freshness: `26c5aba4-e626-41e7-a064-acad2c90c09e`.
- `gaps_found`: `0`.
- `freshness_lag_seconds`: `83575`.
- `data_quality_score`: `1.00000`.

Datos actuales:

- `BTCUSDT`: `1d`, `4h`.
- `ETHUSDT`: `1d`, `4h`.

Rutas usadas:

- Raw Parquet: `data/raw/binance/{symbol}/{timeframe}/{year}/{month}/`.
- Curated Parquet: `data/curated/ohlcv/{symbol}/{timeframe}/`.

Tablas PostgreSQL usadas:

- `ohlcv_curated`
- `ingestion_runs`
- `data_quality_checks`

Data quality actual:

- Gap detection implementado por `exchange + symbol + timeframe`.
- Para `1d`, el intervalo esperado es 1 día.
- Para `4h`, el intervalo esperado es 4 horas.
- Si `gaps_found > 0`, la validación falla y el lote no debe pasar a curated ni a `ohlcv_curated`.
- Freshness implementado como `now_utc - max(timestamp)`.
- `data_quality_checks.metadata` guarda detalle por símbolo/timeframe.

La etapa ya cuenta con un flujo mínimo funcional de punta a punta para OHLCV. Las siguientes mejoras deben mantenerse acotadas y orientadas a estabilizar esta base antes de ampliar fuentes o funcionalidades.
