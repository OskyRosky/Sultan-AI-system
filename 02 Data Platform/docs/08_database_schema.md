# Esquema de Base de Datos

## Objetivo

El esquema inicial de PostgreSQL soporta auditoría, control de fuentes, tracking de corridas, resultados de data quality y consulta de OHLCV validado.

## Tablas iniciales

### asset_universe

Define activos y pares observados por Sultan.

### data_sources

Registra proveedores de datos, tipo de fuente, estado y metadatos.

### ingestion_runs

Registra cada ejecución de pipeline con estado, tiempos, conteos y errores.

### data_quality_checks

Registra validaciones ejecutadas, resultado, severidad y métricas asociadas.

### ohlcv_curated

Contiene datos OHLCV validados y listos para consumo posterior.

## SQL inicial

Script:

`02 Data Platform/sql/001_create_data_platform_tables.sql`

Este SQL es una base inicial clara, no una migración compleja.

