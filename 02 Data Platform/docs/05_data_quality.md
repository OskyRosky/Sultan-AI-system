# Data Quality

## Objetivo

La calidad de datos es un bloqueo explícito entre `raw` y `curated`. El sistema debe detectar datos incompletos, inválidos, duplicados o desactualizados antes de que sean usados en research o features.

## Validaciones iniciales OHLCV

La versión mínima ejecutada aplica:

- `timestamp` no puede ser nulo.
- `open`, `high`, `low`, `close` no pueden ser nulos.
- `high >= low`.
- `high >= open`.
- `high >= close`.
- `low <= open`.
- `low <= close`.
- `volume >= 0`.
- No duplicados por `exchange + symbol + timeframe + timestamp`.
- Rechazo de velas abiertas antes de curated/PostgreSQL.
- Detección formal de gaps por `exchange + symbol + timeframe`.
- Cálculo de freshness por `exchange + symbol + timeframe`.

## Closed-candle eligibility

Raw Parquet puede guardar la respuesta original de Binance/CCXT para auditoria. La capa curated y `public.ohlcv_curated` solo pueden recibir velas cerradas.

La elegibilidad se calcula en memoria:

```text
1d close_time = timestamp + 1 day
4h close_time = timestamp + 4 hours
closed if close_time <= now_utc
```

Si una vela abierta llega al candidato curated, la validacion falla con `open_candles_in_curated_candidate`. Si una vela abierta llega al upsert PostgreSQL, el upsert falla con `postgres_upsert_rejected_open_candles`.

El flow registra metadata de auditoria:

- `rows_fetched_raw`.
- `rows_closed_eligible`.
- `rows_open_excluded`.
- `closed_candles_only = true`.
- `latest_closed_eligible_timestamp`.

## Reconciliation checks

El pipeline incremental ahora registra un plan de reconciliacion antes de descargar y una lectura de salud despues del upsert.

Plan previo por `symbol/timeframe`:

- `latest_stored_before_run`.
- `latest_closed_expected_timestamp`.
- `missing_from_timestamp`.
- `missing_to_timestamp`.
- `expected_missing_closed_candles_before_run`.
- `is_already_caught_up_before_run`.
- `incremental_start_timestamp`.

Health posterior por `symbol/timeframe`:

- `latest_fetched_timestamp`.
- `latest_closed_eligible_timestamp`.
- `latest_stored_after_run`.
- `rows_fetched_raw`.
- `rows_closed_eligible`.
- `rows_open_excluded`.
- `rows_inserted_or_updated`.
- `rows_new`.
- `rows_existing`.
- `is_caught_up_after_run`.
- `missing_closed_candles_after_run`.
- `remaining_gap_start`.
- `remaining_gap_end`.
- `health_status`.

`health_status` puede ser:

- `caught_up`: la serie quedo al dia y no hubo warnings historicos.
- `caught_up_with_historical_warnings`: la serie quedo al dia, pero la validacion detecto gaps historicos auditables.
- `gap_remaining`: despues del run sigue faltando al menos una vela cerrada esperada.
- `no_new_closed_candles`: no habia velas cerradas nuevas que promover.
- `failed_validation`: la validacion bloqueante impidio curated/PostgreSQL.

Estos checks no declaran readiness para Feature Engineering ni Backtesting. Solo hacen observable la completitud OHLCV del run.

## Gap detection

Los gaps se detectan ordenando cada grupo por `timestamp` y comparando la diferencia entre velas consecutivas contra el intervalo esperado.

- Para `1d`, el intervalo esperado es 1 día.
- Para `4h`, el intervalo esperado es 4 horas.
- Si `gaps_found > 0` y no hay errores estructurales, `check_status = passed_with_warnings`.
- Si solo hay gaps, el lote puede pasar a curated y `ohlcv_curated`.
- No se imputan datos.
- No se rellenan gaps.

## Freshness

Freshness se calcula por símbolo/timeframe usando:

```text
freshness_lag_seconds = now_utc - max(timestamp)
```

El mayor lag observado se registra en `data_quality_checks.freshness_lag_seconds`.

El detalle por `exchange + symbol + timeframe` se guarda en `data_quality_checks.metadata`.

## Vista operativa de health

`v_ohlcv_operational_health` separa el ultimo quality check global del detalle disponible por `symbol/timeframe`.

- Las columnas `latest_global_*` describen el ultimo registro global en `data_quality_checks`.
- Las columnas `latest_data_quality_score`, `latest_gaps_found`, `latest_freshness_lag_seconds` y `latest_check_status` solo se llenan cuando el ultimo `metadata` contiene detalle para ese `symbol/timeframe`.
- `latest_symbol_timeframe_summary` indica si el dato viene de `symbol_timeframe` o si no estuvo presente en el ultimo metadata.

Esto evita presentar metricas globales como si fueran metricas especificas por par/timeframe.

## Resultado de validación

Cada corrida debe producir:

- Estado general del lote.
- Número de filas evaluadas.
- Número de filas inválidas.
- Gaps detectados.
- Score de calidad.
- Error principal, si aplica.

## Regla crítica

Si hay errores estructurales bloqueantes, el dato no debe pasar a `curated`.

Errores bloqueantes:

- `timestamp` nulo.
- OHLC nulo.
- Reglas OHLC inválidas.
- `volume < 0`.
- Duplicados por `exchange + symbol + timeframe + timestamp` dentro del lote.
- Velas abiertas en el candidato curated.

Warnings auditables:

- `gaps_found > 0`.

Score:

- `1.0`: sin errores ni gaps.
- `0.95`: solo gaps/warnings.
- `0.0`: errores bloqueantes.

## Idempotencia y re-runs

Las corridas repetidas no deben fallar por duplicados si las velas ya existen en `ohlcv_curated`.

- Los duplicados dentro del mismo lote siguen siendo una falla de validación.
- Las barras ya existentes en PostgreSQL se manejan por `ON CONFLICT DO UPDATE`.
- `ohlcv_curated` mantiene una sola fila por `exchange + symbol + timeframe + timestamp`.
- `ingestion_runs` y `data_quality_checks` registran cada ejecución.

## Resultado confirmado

En el primer run real mínimo:

- `rows_checked`: `2000`.
- `rows_failed`: `0`.
- `gaps_found`: `0` en la validación mínima actual.
- `data_quality_score`: `1.00000`.
- `check_status`: `passed`.

Run confirmado: `faf0e84e-5b6e-4751-9664-7fcbda356d68`.

En el run con gaps/freshness implementados:

- `run_id`: `26c5aba4-e626-41e7-a064-acad2c90c09e`.
- `rows_checked`: `2000`.
- `rows_failed`: `0`.
- `gaps_found`: `0`.
- `freshness_lag_seconds`: `83575`.
- `data_quality_score`: `1.00000`.
- `check_status`: `passed`.

En la doble ejecución controlada de idempotencia:

- Run `4cd9c775-d7b8-40ed-8f7c-6e5c6ebdd096`: `rows_checked = 2000`, `rows_failed = 0`, `gaps_found = 0`, `check_status = passed`.
- Run `e9e0dd92-9550-4519-9c0d-a43b50d191b5`: `rows_checked = 2000`, `rows_failed = 0`, `gaps_found = 0`, `check_status = passed`.

En el run histórico completo:

- `run_id`: `2a979115-402f-4243-aef1-8c5aead2cc89`.
- `rows_checked`: `44612`.
- `rows_failed`: `0`.
- `gaps_found`: `16`.
- `check_status`: `passed_with_warnings`.
- `data_quality_score`: `0.95000`.
- `freshness_lag_seconds`: `85642`.
- `BTCUSDT 4h`: `8` gaps.
- `ETHUSDT 4h`: `8` gaps.

En el Repair Block 2 de reconciliacion controlada:

- `run_id`: `2db92aa1-1351-46a2-a99e-b6ec9835ae1c`.
- Modo: `incremental`.
- `rows_checked`: `370`.
- `rows_failed`: `0`.
- `gaps_found`: `0`.
- `data_quality_score`: `1.00000`.
- `check_status`: `passed`.
- `rows_fetched_raw`: `374`.
- `rows_closed_eligible`: `370`.
- `rows_open_excluded`: `4`.
- `BTCUSDT 1d`: `health_status = caught_up`, ultimo timestamp `2026-06-05T00:00:00+00:00`.
- `BTCUSDT 4h`: `health_status = caught_up`, ultimo timestamp `2026-06-06T16:00:00+00:00`.
- `ETHUSDT 1d`: `health_status = caught_up`, ultimo timestamp `2026-06-05T00:00:00+00:00`.
- `ETHUSDT 4h`: `health_status = caught_up`, ultimo timestamp `2026-06-06T16:00:00+00:00`.
- Duplicados posteriores en PostgreSQL: `0`.
- Velas abiertas posteriores en PostgreSQL: `0`.

Este resultado cierra el gap final operativo observado en 02 Data Platform, pero no declara readiness para Feature Engineering, Backtesting, Stage 09 ni Paper Trading.

En la prueba manual de Repair Block 3B usando el script launchd:

- `run_id`: `0e0a1b7c-e538-4f96-afa4-99465741b521`.
- Modo: `incremental`.
- `rows_checked`: `8`.
- `rows_failed`: `0`.
- `gaps_found`: `0`.
- `data_quality_score`: `1.00000`.
- `check_status`: `passed`.
- `rows_fetched_raw`: `12`.
- `rows_closed_eligible`: `8`.
- `rows_open_excluded`: `4`.
- `rows_new`: `0`.
- `rows_existing`: `8`.
- `health_status`: `caught_up` para las cuatro series.
- Duplicados posteriores en PostgreSQL: `0`.
- Velas abiertas posteriores en PostgreSQL: `0`.

La prueba confirma que una segunda ejecucion incremental sobre base al dia re-descarga solo la ventana de overlap, actualiza filas existentes por upsert y no duplica datos.
