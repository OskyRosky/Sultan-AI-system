# Bloque 5 - Volatility Feature Calculation

## Objetivo

Implementar features técnicas de volatilidad dentro de `05 Feature Calculation Engine`, manteniendo no-lookahead y sin persistencia en Parquet ni PostgreSQL.

Volatility es una familia del `02 Feature Catalog`. No se crea un subcomponente nuevo ni se renombra la estructura oficial de 03 Feature Engineering.

## Features implementadas

- `rolling_std_20`
- `volatility_20`
- `atr_14`

## Fórmulas

`rolling_std_20`:

```text
std(simple_return_t ... simple_return_{t-19})
```

`volatility_20` en v1:

```text
volatility_20 = rolling_std_20
```

`true_range_t`:

```text
max(
    high_t - low_t,
    abs(high_t - close_{t-1}),
    abs(low_t - close_{t-1})
)
```

Para el primer registro de cada grupo, donde no existe `close_{t-1}`, `true_range_t` queda determinado por `high_t - low_t`.

`atr_14`:

```text
mean(true_range_t ... true_range_{t-13})
```

## No-lookahead

El cálculo se ordena por `exchange + symbol + timeframe + timestamp` y se ejecuta por grupo.

- `rolling_std_20` usa returns hasta T.
- `volatility_20` usa `rolling_std_20` en T.
- `true_range` usa `high_t`, `low_t` y `close_{t-1}`.
- `atr_14` usa `true_range` hasta T.

Ninguna feature usa datos futuros.

## Warm-up periods

- `rolling_std_20`: `NaN` hasta tener 20 retornos válidos.
- `volatility_20`: `NaN` donde `rolling_std_20` sea `NaN`.
- `atr_14`: `NaN` durante los primeros 13 registros por grupo.

## Decisión v1 sobre anualización

`volatility_20` se mantiene igual a `rolling_std_20` en v1. No se anualiza todavía para evitar introducir supuestos distintos entre timeframes `1d` y `4h`.

## Columnas agregadas

- `rolling_std_20`
- `volatility_20`
- `atr_14`

No se conserva `true_range` en el output final porque es una serie auxiliar interna.

## Validación

`feature_quality.py` valida:

- Columnas volatility requeridas.
- Ausencia de infinitos.
- Warm-up periods esperados.
- Valores no negativos en `rolling_std_20`, `volatility_20` y `atr_14`.
- Igualdad `volatility_20 = rolling_std_20` en v1, ignorando `NaN`.
- Duplicados por clave lógica de features.
- `feature_set`, `feature_version` y `timestamp` válidos.
- Ausencia de columnas prohibidas de señales, estrategia, backtesting o cruces.

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
python -B -m py_compile "03 Feature Engineering/features/volatility.py"
python -B -m py_compile "03 Feature Engineering/features/feature_quality.py"
python -B -m py_compile "03 Feature Engineering/flows/generate_features_flow.py"
poetry run python -m pytest "03 Feature Engineering/tests" -q
```

## Próximo paso recomendado

Implementar la siguiente familia del Feature Catalog v1, como momentum, manteniendo cálculo por grupo, no-lookahead, quality checks y sin persistencia hasta completar validación de features.
