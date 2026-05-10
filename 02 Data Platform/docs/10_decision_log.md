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

