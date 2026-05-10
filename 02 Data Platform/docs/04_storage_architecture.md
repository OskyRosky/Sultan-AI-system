# Arquitectura de Almacenamiento

## Principio

Los datos físicos reales no se guardan dentro de `02 Data Platform/`. Esa carpeta contiene diseño, flows, SQL, schemas, notebooks, mockups, logs de etapa y reportes.

Los datasets reales deben guardarse en:

`/Users/sultan/Trading/Sultan-AI-system/data/`

## Filesystem esperado

Raw:

```text
data/raw/binance/{symbol}/{timeframe}/{year}/{month}/
```

Curated:

```text
data/curated/ohlcv/{symbol}/{timeframe}/
```

Features:

```text
data/features/
```

Logs de pipeline:

```text
02 Data Platform/logs/pipeline_runs/
```

## PostgreSQL

PostgreSQL funcionará como capa relacional para tracking, auditoría y consulta estructurada.

Tablas iniciales propuestas:

- `asset_universe`
- `data_sources`
- `ingestion_runs`
- `data_quality_checks`
- `ohlcv_curated`

## Formato de archivos

- Formato inicial para datasets: Parquet.
- Motor local complementario futuro: DuckDB.
- Particionamiento raw: fuente, símbolo, timeframe, año y mes.
- Particionamiento curated: dataset, símbolo y timeframe.

