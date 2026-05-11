# 02 Data Platform v1 — Cierre de etapa

## 1. Objetivo de la etapa

La etapa `02 Data Platform` construyo una plataforma local de datos confiable, trazable, validada y orquestada para OHLCV crypto. El objetivo fue dejar una base operativa para research cuantitativo posterior, sin introducir logica de trading, backtesting, ejecucion de ordenes ni agentes LLM.

La plataforma permite descargar datos desde una fuente publica, conservar evidencia raw, validar contratos minimos de calidad, promover datos a curated, persistirlos en PostgreSQL y observar la ejecucion diaria con Prefect.

## 2. Alcance implementado

- Binance como fuente oficial actual.
- `BTCUSDT` y `ETHUSDT`.
- Timeframes `1d` y `4h`.
- Historico completo disponible en Binance para el alcance definido.
- Ingesta incremental/catch-up para operacion diaria.
- Raw Parquet.
- Curated Parquet.
- PostgreSQL como capa consultable y auditable.
- Prefect para orquestacion local.
- DBeaver para inspeccion visual de PostgreSQL.
- Vistas operativas para data quality, runs y resumen OHLCV.

## 3. Arquitectura final

La arquitectura fisica y operacional queda organizada asi:

- Raw Parquet: `data/raw/binance/{symbol}/{timeframe}/{year}/{month}/`
- Curated Parquet: `data/curated/ohlcv/{symbol}/{timeframe}/`
- PostgreSQL: database local `sultan_ai`
- Prefect deployment: `ingest_ohlcv_flow/sultan-ohlcv-daily`

Flujo operativo:

```text
Binance / CCXT
  -> raw Parquet
  -> validation
  -> curated Parquet
  -> PostgreSQL
  -> monitoring views
```

El flow conserva una copia raw, valida el lote, promueve solo datos estructuralmente validos a curated y actualiza PostgreSQL mediante upsert idempotente.

## 4. Base de datos

Database:

```text
sultan_ai
```

Usuario local:

```text
sultan_user
```

Tablas:

- `asset_universe`
- `data_sources`
- `ingestion_runs`
- `data_quality_checks`
- `ohlcv_curated`

Vistas:

- `v_ohlcv_summary`
- `v_ohlcv_latest_bars`
- `v_pipeline_runs_latest`
- `v_data_quality_latest`
- `v_ohlcv_operational_health`

## 5. Datos cargados

Estado validado en PostgreSQL:

- `BTCUSDT 1d`
- `BTCUSDT 4h`
- `ETHUSDT 1d`
- `ETHUSDT 4h`

El rango historico parte desde `2017-08-17` y llega hasta la fecha actual disponible segun Binance y las ejecuciones incrementales confirmadas. El historico corresponde a lo efectivamente disponible en Binance para los pares y timeframes definidos; no se imputaron velas ni se rellenaron gaps.

## 6. Validaciones de calidad

Validaciones aplicadas:

- `timestamp` no nulo.
- OHLC no nulo.
- `high >= low`.
- `high >= open`.
- `high >= close`.
- `low <= open`.
- `low <= close`.
- `volume >= 0`.
- Duplicados bloqueados por `exchange + symbol + timeframe + timestamp`.
- Gaps tratados como warning auditable.
- `freshness_lag_seconds`.
- `data_quality_score`.

Los errores estructurales bloquean la promocion a curated/PostgreSQL. Los gaps historicos se auditan, pero no se imputan ni se rellenan.

## 7. Orquestacion Prefect

Flow:

```text
ingest_ohlcv_flow
```

Deployment:

```text
ingest_ohlcv_flow/sultan-ohlcv-daily
```

Work pool:

```text
sultan-local-pool
```

Schedule:

```text
0 10 * * *
```

Timezone:

```text
America/Costa_Rica
```

UI:

```text
http://127.0.0.1:4200
```

Modo diario:

```text
incremental/catch-up
```

`full_history` queda reservado para bootstrap inicial o recargas controladas. No debe usarse como modo diario.

## 8. Operacion diaria

Iniciar Prefect Server:

```bash
cd "/Users/sultan/Trading/Sultan-AI-system"
poetry run prefect server start
```

En otra terminal, iniciar el worker:

```bash
cd "/Users/sultan/Trading/Sultan-AI-system"
poetry run prefect worker start --pool sultan-local-pool
```

Condiciones operativas:

- La Mac debe estar encendida.
- Prefect Server debe estar activo.
- El worker `sultan-local-pool` debe estar activo.
- El deployment diario corre a las 10:00 a.m. Costa Rica.
- Si pasan varios dias sin correr, el modo incremental/catch-up completa desde `MAX(timestamp)` persistido en PostgreSQL por `exchange + symbol + timeframe`.

## 9. Como verificar datos

Resumen OHLCV:

```sql
SELECT * FROM public.v_ohlcv_summary ORDER BY symbol, timeframe;
```

Ultimos runs:

```sql
SELECT run_id, flow_name, status, rows_fetched, rows_validated, rows_inserted, started_at, finished_at, error_message
FROM public.ingestion_runs
ORDER BY started_at DESC
LIMIT 10;
```

Ultimos checks de calidad:

```sql
SELECT run_id, check_status, rows_checked, rows_failed, gaps_found, freshness_lag_seconds, data_quality_score, checked_at
FROM public.data_quality_checks
ORDER BY checked_at DESC
LIMIT 10;
```

Ultima vela por par/timeframe:

```sql
SELECT exchange, symbol, timeframe, timestamp, open, high, low, close, volume
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY exchange, symbol, timeframe
               ORDER BY timestamp DESC
           ) AS rn
    FROM public.ohlcv_curated
    WHERE symbol IN ('BTCUSDT', 'ETHUSDT')
      AND timeframe IN ('1d', '4h')
) x
WHERE rn = 1
ORDER BY symbol, timeframe;
```

## 10. Hardening aplicado

- `v_ohlcv_operational_health` fue corregida para no presentar metricas globales como si fueran metricas especificas por `symbol/timeframe`.
- `ingestion_runs` fue protegido contra runs huerfanos en `status = running`.
- CCXT Binance usa timeout de 30 segundos.
- Idempotencia confirmada con upsert sobre `exchange + symbol + timeframe + timestamp`.
- Prefect schedule confirmado en `0 10 * * *` con timezone `America/Costa_Rica`.

## 11. Decisiones tecnicas finales

- Binance queda como fuente actual para OHLCV crypto.
- PostgreSQL queda como capa consultable principal.
- Parquet queda como capa fisica para raw y curated.
- Los gaps no se imputan.
- Los gaps no se rellenan.
- `full_history` no debe ejecutarse todos los dias.
- `incremental/catch-up` es el modo operativo diario.

## 12. Pendientes para futuras etapas

Pendientes explicitamente fuera de `02 Data Platform v1`:

- Umbrales formales de freshness.
- Score de calidad granular por `symbol/timeframe`.
- Particionado temporal de curated Parquet.
- Alertas operativas.
- Backup automatico de PostgreSQL.
- Mas pares USDT.
- DuckDB.
- Grafana.
- FRED.
- CoinGecko.
- On-chain.
- Noticias/sentimiento.
- TimescaleDB.
- MLflow.
- Feast.

## 13. Estado de cierre

`02 Data Platform v1` queda cerrada como una plataforma local operativa, validada, trazable y orquestada para OHLCV de `BTCUSDT` y `ETHUSDT` en Binance.
