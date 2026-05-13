# Bloque 3 - Returns Feature Calculation

## Objetivo

Implementar el cálculo real de las primeras features técnicas de tipo returns usando OHLCV validado, sin persistir resultados en Parquet ni PostgreSQL.

## Features implementadas

- `simple_return`
- `log_return`
- `close_open_return`

## Fórmulas

`simple_return`:

```text
close_t / close_{t-1} - 1
```

`log_return`:

```text
log(close_t / close_{t-1})
```

`close_open_return`:

```text
close_t / open_t - 1
```

## Regla no-lookahead

El cálculo se agrupa por `exchange + symbol + timeframe` y se ordena por `timestamp`.

- `simple_return` usa `close_t` y `close_{t-1}`.
- `log_return` usa `close_t` y `close_{t-1}`.
- `close_open_return` usa `open_t` y `close_t`.

Ninguna feature usa datos posteriores al timestamp T.

## Columnas agregadas

Además de las columnas OHLCV base, el motor agrega:

- `simple_return`
- `log_return`
- `close_open_return`
- `feature_set = technical_v1`
- `feature_version = 1.0.0`

No se agrega `run_id` todavía porque en este bloque no hay persistencia ni auditoría real.

## NaN iniciales por grupo

El primer registro de cada grupo no tiene `close_{t-1}`. Por eso `simple_return` y `log_return` deben quedar como `NaN` en esa primera fila.

Si `close_{t-1}`, `close_t` u `open_t` son menores o iguales a cero, el cálculo afectado se deja como `NaN` para evitar infinitos o resultados numéricamente inválidos.

## Validación de returns

La capa `feature_quality.py` valida:

- Columnas de returns requeridas.
- Ausencia de infinitos.
- Duplicados por `exchange + symbol + timeframe + timestamp + feature_set + feature_version`.
- `feature_set`, `feature_version` y `timestamp` no nulos.
- NaN permitidos solo por primer registro de grupo o precios inválidos.
- Ausencia de columnas prohibidas de señales, estrategia o backtesting.

## Qué NO hace este bloque

- No guarda Parquet.
- No inserta en PostgreSQL.
- No crea tablas.
- No escribe auditoría real.
- No crea señales BUY/SELL.
- No crea estrategias.
- No ejecuta backtesting.
- No crea deployments.
- No modifica `02 Data Platform`.

## Cómo ejecutar tests

Desde la raíz del proyecto:

```bash
poetry run python -m pytest "03 Feature Engineering/tests" -q
```

Validación de sintaxis:

```bash
python -B -m py_compile "03 Feature Engineering/features/returns.py"
python -B -m py_compile "03 Feature Engineering/features/feature_quality.py"
python -B -m py_compile "03 Feature Engineering/flows/generate_features_flow.py"
```

## Próximo paso recomendado

Implementar las primeras features de tendencia o volatilidad con la misma disciplina: cálculo por grupo, no-lookahead, tests unitarios y quality checks antes de cualquier persistencia.
