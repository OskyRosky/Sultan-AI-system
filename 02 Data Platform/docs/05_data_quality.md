# Data Quality

## Objetivo

La calidad de datos es un bloqueo explícito entre `raw` y `curated`. El sistema debe detectar datos incompletos, inválidos, duplicados o desactualizados antes de que sean usados en research o features.

## Validaciones iniciales OHLCV

- `timestamp` no puede ser nulo.
- `open`, `high`, `low`, `close` no pueden ser nulos.
- `high >= low`.
- `high >= open`.
- `high >= close`.
- `low <= open`.
- `low <= close`.
- `volume >= 0`.
- No duplicados por `exchange + symbol + timeframe + timestamp`.
- Detección de gaps según timeframe.
- Cálculo de freshness por símbolo y timeframe.

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

## Herramienta prevista

Pandera será la herramienta inicial para validación tabular en Python.

