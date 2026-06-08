# Bloque 6 - Momentum Feature Calculation

## Objetivo

Implementar features técnicas de momentum dentro de `05 Feature Calculation Engine`, manteniendo no-lookahead y sin persistencia en Parquet ni PostgreSQL.

Momentum es una familia del `02 Feature Catalog`. No se crea un subcomponente nuevo ni se renombra la estructura oficial de 03 Feature Engineering.

## Features implementadas

- `rsi_14`
- `macd`
- `macd_signal`

## Fórmulas

`rsi_14` usa cambios de `close` por grupo:

```text
delta_t = close_t - close_{t-1}
gain_t = max(delta_t, 0)
loss_t = abs(min(delta_t, 0))
avg_gain_14 = ewm(gain, alpha=1/14, adjust=False)
avg_loss_14 = ewm(loss, alpha=1/14, adjust=False)
RS = avg_gain_14 / avg_loss_14
rsi_14 = 100 - (100 / (1 + RS))
```

`macd`:

```text
ema_12(close) - ema_26(close)
```

`macd_signal`:

```text
ema_9(macd)
```

Todas las EMAs usan `adjust=False`.

Nota de inicialización: `rsi_14` usa una aproximación EWM/Wilder-style con `ewm(alpha=1/14, adjust=False)`. Puede diferir en los primeros períodos de implementaciones SMA-seeded Wilder RSI, TA-Lib o TradingView. Esto no convierte RSI en señal; sigue siendo una feature técnica descriptiva.

## No-lookahead

El cálculo se ordena por `exchange + symbol + timeframe + timestamp` y se ejecuta por grupo.

- `rsi_14` usa `close` hasta T.
- `macd` usa EMAs de `close` hasta T.
- `macd_signal` usa `macd` hasta T.

Ninguna feature usa datos futuros.

## Warm-up periods

- `rsi_14`: `NaN` durante los primeros 14 registros por grupo.
- `macd`: `NaN` durante las primeras 26 filas por grupo para evitar valores iniciales débiles de EWM.
- `macd_signal`: `NaN` durante las primeras 34 filas por grupo porque depende de EMA26 + EMA9.

El warm-up no se convierte en señal ni regla operativa.

## Indicadores no señales

RSI y MACD se documentan como indicadores técnicos descriptivos. En esta etapa no se interpreta RSI como sobrecompra/sobreventa accionable y MACD no se interpreta como señal.

No se crean columnas `rsi_signal`, `macd_cross`, `macd_signal_cross`, `macd_crossover`, `cross`, `crossover`, `golden_cross` ni `death_cross`.

## Columnas agregadas

- `rsi_14`
- `macd`
- `macd_signal`

Las EMAs auxiliares `ema_12` y `ema_26` no quedan en el output final.

## Validación

`feature_quality.py` valida:

- Columnas momentum requeridas.
- Ausencia de infinitos.
- `rsi_14` entre 0 y 100 cuando no es `NaN`.
- Warm-up esperado en `rsi_14`, `macd` y `macd_signal`.
- `macd` y `macd_signal` no nulos para precios válidos después de su warm-up explícito.
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
python -B -m py_compile "03 Feature Engineering/features/momentum.py"
python -B -m py_compile "03 Feature Engineering/features/feature_quality.py"
python -B -m py_compile "03 Feature Engineering/flows/generate_features_flow.py"
poetry run python -m pytest "03 Feature Engineering/tests" -q
```

## Próximo paso recomendado

Implementar la siguiente familia del Feature Catalog v1, como Relative Strength / Breakout Context, manteniendo cálculo por grupo, no-lookahead, quality checks y sin persistencia hasta completar validación de features.
