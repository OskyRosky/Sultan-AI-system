# Bloque 9 - Candle Structure Feature Calculation

## Objetivo

Implementar features técnicas de estructura de vela dentro de `05 Feature Calculation Engine`, manteniendo no-lookahead y sin persistencia en Parquet ni PostgreSQL.

Candle Structure es una familia del `02 Feature Catalog`. No se crea un subcomponente nuevo ni se renombra la estructura oficial de 03 Feature Engineering.

## Features implementadas

- `high_low_range`
- `body_size`
- `upper_wick`
- `lower_wick`
- `body_to_range_ratio`

## Fórmulas

`high_low_range`:

```text
high_t - low_t
```

`body_size`:

```text
abs(close_t - open_t)
```

`upper_wick`:

```text
high_t - max(open_t, close_t)
```

`lower_wick`:

```text
min(open_t, close_t) - low_t
```

`body_to_range_ratio`:

```text
body_size_t / high_low_range_t
```

Si `high_low_range <= 0`, `body_to_range_ratio` queda como `NaN`.

## No-lookahead

Cada feature usa solo valores de la misma vela T: `open_t`, `high_t`, `low_t` y `close_t`. No hay rolling windows ni `shift`.

## Warm-up

No hay warm-up temporal. Los `NaN` solo deberían aparecer por datos inválidos o rango cero.

## Estructura no señal

Estas features describen geometría de vela. No clasifican patrones ni producen decisiones accionables.

No se crean columnas `candle_signal`, `doji_signal`, `hammer_signal` ni `engulfing_signal`.

## Columnas agregadas

- `high_low_range`
- `body_size`
- `upper_wick`
- `lower_wick`
- `body_to_range_ratio`

No se conservan columnas auxiliares en el output final.

## Validación

`feature_quality.py` valida:

- Columnas requeridas.
- Ausencia de infinitos.
- No negatividad de rango, cuerpo y mechas.
- `body_to_range_ratio` entre 0 y 1 cuando no es `NaN`.
- `NaN` en ratio solo cuando el rango es inválido o cero.
- Duplicados por clave lógica de features.
- `feature_set`, `feature_version` y `timestamp` válidos.
- Ausencia de columnas prohibidas de señales, estrategia, backtesting o patrones accionables.

## Qué NO hace este bloque

- No guarda Parquet.
- No inserta en PostgreSQL.
- No crea tablas.
- No escribe auditoría real.
- No crea señales BUY/SELL.
- No crea patrones accionables de velas.
- No ejecuta backtesting.
- No crea deployments.
- No modifica `02 Data Platform`.

## Cómo ejecutar tests

Desde la raíz del proyecto:

```bash
python -B -m py_compile "03 Feature Engineering/features/candle_structure.py"
python -B -m py_compile "03 Feature Engineering/features/feature_quality.py"
python -B -m py_compile "03 Feature Engineering/flows/generate_features_flow.py"
poetry run python -m pytest "03 Feature Engineering/tests" -q
```

## Próximo paso recomendado

Con el catálogo técnico v1 calculado en preview, el siguiente paso es consolidar quality checks transversales y preparar una validación integral de todas las familias antes de diseñar persistencia.
