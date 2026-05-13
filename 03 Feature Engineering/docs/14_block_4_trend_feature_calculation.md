# Bloque 4 - Trend Feature Calculation

## Objetivo

Implementar el cálculo real de features técnicas de tendencia usando OHLCV validado, manteniendo no-lookahead y sin persistir resultados en Parquet ni PostgreSQL.

## Features implementadas

- `sma_20`
- `sma_50`
- `ema_20`
- `ema_50`
- `price_above_sma20`
- `sma20_slope`
- `ema20_above_ema50`

## Fórmulas

`sma_20`:

```text
mean(close_t ... close_{t-19})
```

`sma_50`:

```text
mean(close_t ... close_{t-49})
```

`ema_20` y `ema_50` usan `pandas.ewm(..., adjust=False)` por grupo.

`price_above_sma20`:

```text
close_t > sma_20_t
```

`sma20_slope`:

```text
sma_20_t - sma_20_{t-1}
```

`ema20_above_ema50`:

```text
ema_20_t > ema_50_t
```

## No-lookahead

El cálculo se ordena por `exchange + symbol + timeframe + timestamp` y se ejecuta por grupo. Las medias móviles y exponenciales solo usan observaciones hasta T. `sma20_slope` usa `sma_20_t` y `sma_20_{t-1}`.

## Warm-up periods

- `sma_20`: `NaN` esperado durante los primeros 19 registros por grupo.
- `sma_50`: `NaN` esperado durante los primeros 49 registros por grupo.
- `sma20_slope`: `NaN` hasta que existan `sma_20_t` y `sma_20_{t-1}`.
- `price_above_sma20`: `NaN` mientras `sma_20` no exista.

## Estado neutral

`ema20_above_ema50` es un estado técnico neutral. No representa señal de compra, venta, entrada, salida ni posición.

No se implementan eventos `cross`, `crossover`, `golden_cross` ni `death_cross`, porque esos nombres inducen lectura de señal o estrategia y están fuera del alcance de esta etapa.

## Validación

`feature_quality.py` valida:

- Columnas trend requeridas.
- Ausencia de infinitos.
- Warm-up periods esperados.
- Estados booleanos o 0/1 en `price_above_sma20` y `ema20_above_ema50`.
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
python -B -m py_compile "03 Feature Engineering/features/trend.py"
python -B -m py_compile "03 Feature Engineering/features/feature_quality.py"
python -B -m py_compile "03 Feature Engineering/flows/generate_features_flow.py"
poetry run python -m pytest "03 Feature Engineering/tests" -q
```

## Próximo paso recomendado

Implementar features de volatilidad con el mismo patrón: cálculo por grupo, no-lookahead, warm-up explícito, quality checks y sin persistencia hasta cerrar validación.
