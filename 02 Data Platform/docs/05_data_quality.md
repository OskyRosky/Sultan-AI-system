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

Pendiente para siguientes bloques:

- Detección formal de gaps según timeframe.
- Cálculo formal de freshness por símbolo y timeframe.

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
