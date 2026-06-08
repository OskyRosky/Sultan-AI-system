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
- Idempotencia/re-runs del flow OHLCV.
- Validación de doble ejecución controlada.
- Crear vistas/queries operativas para inspección de datos.
- Crear guía para inspeccionar BTC/ETH en PostgreSQL.
- Descarga histórica paginada OHLCV.
- Carga completa disponible en Binance para BTCUSDT/ETHUSDT 1d/4h.
- Validación de rangos completos en PostgreSQL.
- Política de gaps históricos como warning auditable.
- Crear deployment local en Prefect.
- Ver flow/job en Prefect UI.
- Crear schedule diario.
- Ajustar schedule diario a 10:00 a.m. Costa Rica.
- Implementar modo incremental/catch-up para operacion diaria.
- Validar run incremental con nuevas velas.
- Validar run incremental sin nuevas velas disponibles.
- Corregir `v_ohlcv_operational_health`.
- Proteger `ingestion_runs` contra runs huerfanos en `running`.
- Configurar timeout de 30 segundos en CCXT.
- Cerrar documentalmente `02 Data Platform v1`.

## Alta prioridad pendiente

- Definir umbrales formales de freshness por timeframe.
- Prueba controlada de validación fallida.
- Observar un run automático `launchd` morning/evening posterior a Repair Block 3C y confirmar:
  - `ingestion_runs.status = success`;
  - `health_status = caught_up`;
  - duplicados en `ohlcv_curated` = `0`;
  - velas abiertas en PostgreSQL = `0`.
- Preservar granularidad de fallos de validación en una mejora futura del handler general. Claude detectó que un run marcado como `failed_validation` podría terminar sobrescrito por `failed`; la mejora debe conservar estados como `failed_validation`, `failed_fetch`, `failed_upsert` y `failed_unknown`.

## Media prioridad

- Agregar Telegram alerts.
- Agregar más pares USDT.
- Crear dashboard HTML de monitoreo.
- Agregar DuckDB queries.
- Agregar alertas operativas futuras por Telegram, email o webhook cuando:
  - `launchd` falle;
  - un `ingestion_run` termine en `failed`;
  - `health_status != caught_up`;
  - freshness supere el umbral definido.

## Remaining non-blocking backlog before 03 Feature Engineering

Estado de cierre documentado:

```text
data_gap_status = repaired
ohlcv_data_status = ready
ohlcv_pipeline_status = operational_with_non_blocking_observations
scheduler_status = launchd_configured_and_observed
platform_observability_status = adequate_now_structured_events_future
feature_engineering_status = pending_audit_regeneration_snapshot
backtesting_data_readiness = blocked_until_03_feature_verification_and_snapshot
stage_09_readiness = blocked
```

Claude auditó `02 Data Platform` con veredicto `approved_with_observations`. Los pendientes siguientes son no bloqueantes para iniciar `03 Feature Engineering`; no cambian el estado OHLCV reparado ni declaran readiness para `06 Backtesting Engine`, Stage 09 o Paper Trading.

### Structured operational log database

Crear en el futuro una tabla operacional fina, por ejemplo `pipeline_events` o `pipeline_execution_logs`, para complementar `ingestion_runs` y `data_quality_checks`.

Campos sugeridos:

- `event_id`
- `run_id`
- `pipeline_name` o `flow_name`
- `stage`
- `severity`
- `event_type`
- `event_time`
- `message`
- `error_type`
- `retry_attempt`
- `symbol`
- `timeframe`
- `metadata JSONB`

Objetivo:

- analizar fallos por causa;
- analizar retries;
- auditar warnings;
- auditar health checks;
- reconstruir comportamiento histórico del scheduler;
- medir frecuencia de timeouts, errores API y errores de red.

No se implementa `pipeline_events` ni `pipeline_execution_logs` en este bloque; queda solo como mejora futura.

### Validation failure status granularity

Pendiente futuro: evitar que un estado granular `failed_validation` sea sobrescrito por un handler general como `failed`. La mejora debe preservar estados operativos diferenciados:

- `failed_validation`
- `failed_fetch`
- `failed_upsert`
- `failed_unknown`

Este pendiente no bloquea `03 Feature Engineering` porque la data OHLCV actual está sana: `caught_up`, sin duplicados y sin velas abiertas en PostgreSQL.

### Next automatic launchd observation

Ya se observó que `launchd` dispara el job: el primer run evening se ejecutó y falló por timeout externo de Binance. Repair Block 3C agregó timeout de 60 segundos, retry/backoff y mejor auditabilidad de fallos tempranos.

Pendiente operativo: observar un run automático `morning` o `evening` posterior a Repair Block 3C y confirmar:

- `status = success`;
- registro en `ingestion_runs`;
- `health_status = caught_up`;
- duplicados = `0`;
- velas abiertas = `0`.

Scheduler operativo actual:

- `com.sultan.ohlcv.reconciliation.morning`: `10:05` America/Costa_Rica.
- `com.sultan.ohlcv.reconciliation.evening`: `18:05` America/Costa_Rica.

### Prefect SQLite lock future work

Prefect Server local no es el scheduler operativo actual porque presentó:

```text
sqlite3.OperationalError: database is locked
```

Scheduler oficial actual: `launchd`.

Pendiente futuro si se quiere recuperar Prefect UI/deployments:

- migrar metadata de Prefect a un PostgreSQL separado; o
- mantener Prefect como librería/flow runner sin server local.

Este pendiente no bloquea `03 Feature Engineering`.

### Historical docs: Prefect vs launchd

Algunos documentos históricos mencionan el deployment Prefect `sultan-ohlcv-daily`. La referencia actual de cierre operativo es:

```text
02 Data Platform/docs/13_data_gap_repair_and_backtesting_readiness.md
```

Pendiente futuro: armonizar documentación histórica para aclarar que el deployment Prefect fue mecanismo histórico/documental, mientras que `launchd` es el scheduler operativo actual. No se deben borrar referencias históricas válidas; se debe marcar el estado actual con claridad.

### External broken cron outside Sultan-AI-system

Existe un cron externo apuntando a:

```text
/Users/sultan/Trading/algo-trading/tools/run_daily_job.sh
```

Ese cron no pertenece a `Sultan-AI-system`; el script no existe o no aplica a este repo. Pendiente futuro: revisarlo y removerlo o desactivarlo manualmente solo si el usuario lo confirma. No modificarlo desde esta etapa documental.

### Dependency on 03 Feature Engineering

`02 Data Platform` deja OHLCV listo para consumo downstream, pero `03 Feature Engineering` sigue pendiente de:

- auditoría;
- limpieza/verificación;
- regeneración completa;
- snapshot para `06 Backtesting Engine`.

`06 Backtesting Engine` permanece bloqueado hasta que `03 Feature Engineering` quede validado y exista snapshot versionado.

### Optional future alerts

Agregar alertas futuras por Telegram, email o webhook para fallos de scheduler, runs fallidos, health distinto de `caught_up` y freshness por encima de umbral. No implementar alertas ahora.

## Futuro

- FRED.
- CoinGecko.
- On-chain avanzado.
- Noticias y sentimiento.
- Grafana.
- TimescaleDB.
- MLflow.
- Feast.
