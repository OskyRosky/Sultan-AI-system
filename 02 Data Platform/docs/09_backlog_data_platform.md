# Backlog Data Platform

## Completado

- Crear `.env.example` para conexión PostgreSQL.
- Validar conexión PostgreSQL.
- Crear SQL inicial de tablas.
- Crear script de conexión a PostgreSQL.
- Crear primer fetch OHLCV BTC/ETH.
- Guardar raw Parquet.
- Validar datos OHLCV.
- Guardar curated Parquet.
- Insertar en PostgreSQL.
- Registrar `ingestion_runs`.
- Ejecutar flow local en Prefect.
- Detección formal de gaps.
- Cálculo de freshness.
- Registro de `freshness_lag_seconds` en `data_quality_checks`.
- Registro de metadata de calidad por símbolo/timeframe.

## Alta prioridad pendiente

- Definir umbrales formales de freshness por timeframe.
- Revisar idempotencia/re-runs.

## Media prioridad

- Crear deployment programado en Prefect.
- Agregar Telegram alerts.
- Agregar más pares USDT.
- Crear dashboard HTML de monitoreo.
- Agregar DuckDB queries.

## Futuro

- FRED.
- CoinGecko.
- On-chain avanzado.
- Noticias y sentimiento.
- Grafana.
- TimescaleDB.
- MLflow.
- Feast.
