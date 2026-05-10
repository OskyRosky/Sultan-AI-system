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

## Primer pipeline previsto

El primer pipeline real será `ingest_ohlcv_flow`, ejecutado localmente con Prefect. Descargará histórico OHLCV de Binance vía CCXT para:

- `BTCUSDT`: `1d`, `4h`.
- `ETHUSDT`: `1d`, `4h`.

Esta primera ejecución solo prepara estructura, documentación, SQL y mockup. No descarga datos.

