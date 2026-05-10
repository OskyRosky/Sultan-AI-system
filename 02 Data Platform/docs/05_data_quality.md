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
- Detección formal de gaps por `exchange + symbol + timeframe`.
- Cálculo de freshness por `exchange + symbol + timeframe`.

## Gap detection

Los gaps se detectan ordenando cada grupo por `timestamp` y comparando la diferencia entre velas consecutivas contra el intervalo esperado.

- Para `1d`, el intervalo esperado es 1 día.
- Para `4h`, el intervalo esperado es 4 horas.
- Si `gaps_found > 0`, `check_status = failed`.
- Si `gaps_found > 0`, el lote no debe pasar a curated ni a `ohlcv_curated`.
- No se imputan datos.
- No se rellenan gaps.

## Freshness

Freshness se calcula por símbolo/timeframe usando:

```text
freshness_lag_seconds = now_utc - max(timestamp)
```

El mayor lag observado se registra en `data_quality_checks.freshness_lag_seconds`.

El detalle por `exchange + symbol + timeframe` se guarda en `data_quality_checks.metadata`.

## Resultado de validación

Cada corrida debe producir:

- Estado general del lote.
- Número de filas evaluadas.
- Número de filas inválidas.
- Gaps detectados.
- Score de calidad.
- Error principal, si aplica.

## Regla crítica

Si una validación falla, el dato no debe pasar a `curated`.

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
