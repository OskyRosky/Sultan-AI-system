# Feature Catalog v1

## Identidad

- `feature_set`: `technical_v1`
- `feature_version`: `1.0.0`

Este catálogo define features técnicas derivadas de OHLCV. Ninguna feature representa una señal de trading, recomendación de compra, recomendación de venta, posición ni resultado de estrategia.

## Returns

Features:

- `simple_return`
- `log_return`
- `close_open_return`

Miden variaciones relativas de precio entre observaciones o dentro de una vela. Sirven para describir comportamiento direccional histórico y normalizar cambios entre activos o timeframes.

Definiciones v1:

- `simple_return`: `close_t / close_{t-1} - 1`.
- `log_return`: `log(close_t / close_{t-1})`.
- `close_open_return`: `close_t / open_t - 1`.

Estas definiciones respetan no-lookahead: en timestamp T solo usan precios disponibles hasta T.

Limitaciones: pueden ser ruidosas, sensibles a outliers y no capturan por sí solas régimen, liquidez ni riesgo futuro. No representan señal de entrada o salida.

## Volatility

Features:

- `rolling_std_20`
- `volatility_20`
- `atr_14`

Miden dispersión, variabilidad y rango efectivo del precio. Sirven para contextualizar riesgo, amplitud de movimiento y cambios de régimen.

Definiciones v1:

- `rolling_std_20`: desviación estándar móvil de `simple_return` sobre 20 periodos.
- `volatility_20`: igual a `rolling_std_20` en v1.
- `atr_14`: media móvil simple de 14 periodos del true range.

True range en T:

```text
max(high_t - low_t, abs(high_t - close_{t-1}), abs(low_t - close_{t-1}))
```

En v1 no se anualiza `volatility_20` para evitar supuestos no homogéneos entre timeframes.

Limitaciones: dependen de ventanas históricas, tienen warm-up period y pueden reaccionar tarde ante cambios abruptos. No representan señal de trading.

## Trend

Features:

- `sma_20`
- `sma_50`
- `ema_20`
- `ema_50`
- `price_above_sma20`
- `sma20_slope`
- `ema20_above_ema50`

Miden suavización, dirección y relación del precio frente a medias móviles. Sirven para describir contexto tendencial y persistencia histórica.

Definiciones v1:

- `sma_20`: media móvil simple de `close` sobre 20 periodos.
- `sma_50`: media móvil simple de `close` sobre 50 periodos.
- `ema_20`: media móvil exponencial de `close` con span 20 y `adjust=False`.
- `ema_50`: media móvil exponencial de `close` con span 50 y `adjust=False`.
- `price_above_sma20`: estado técnico neutral que indica si `close_t > sma_20_t`.
- `sma20_slope`: `sma_20_t - sma_20_{t-1}`.
- `ema20_above_ema50`: estado técnico neutral que indica si `ema_20_t > ema_50_t`.

`ema20_above_ema50` no representa señal de trading. No se modelan eventos `cross` o `crossover` en esta etapa.

Limitaciones: son indicadores rezagados, pueden fallar en mercados laterales y no definen por sí mismos una estrategia. No representan señal BUY/SELL.

## Momentum

Features:

- `rsi_14`
- `macd`
- `macd_signal`

Miden aceleración, fuerza relativa y diferencia entre medias exponenciales. Sirven para describir presión direccional y cambios de ritmo.

Definiciones v1:

- `rsi_14`: Relative Strength Index con suavizado estilo Wilder usando `ewm(alpha=1/14, adjust=False)`.
- `macd`: `ema_12(close) - ema_26(close)`.
- `macd_signal`: EMA 9 de `macd`.

RSI y MACD son indicadores técnicos descriptivos en esta etapa. No se interpretan como señales, no se crean columnas `rsi_signal`, `macd_cross`, `macd_signal_cross` ni `macd_crossover`.

Limitaciones: pueden generar lecturas extremas durante tendencias prolongadas y requieren interpretación posterior en research. No representan orden, entrada ni salida.

## Relative Strength / Breakout Context

Features:

- `close_vs_high_52w`
- `rolling_max_20`
- `rolling_min_20`

Miden la posición del cierre respecto a máximos o rangos recientes. Sirven para describir contexto de ruptura, proximidad a extremos y compresión o expansión del rango.

Definiciones v1:

- `rolling_max_20`: máximo móvil de `high` sobre 20 períodos.
- `rolling_min_20`: mínimo móvil de `low` sobre 20 períodos.
- `close_vs_high_52w`: `close_t / rolling_high_52w_t`.

Lookback de `rolling_high_52w`:

- `1d`: 365 períodos.
- `4h`: 2190 períodos.

Estas features describen contexto relativo. No representan señales de ruptura, soporte, resistencia, compra o venta.

Limitaciones: no distinguen entre ruptura válida, falso breakout o agotamiento. No representan señal de compra o venta.

## Volume

Features:

- `volume_change`
- `volume_sma_20`
- `volume_ratio_20`

Miden cambios relativos y contexto del volumen frente a su promedio reciente. Sirven para evaluar participación, actividad y confirmación descriptiva del movimiento.

Definiciones v1:

- `volume_change`: `volume_t / volume_{t-1} - 1`.
- `volume_sma_20`: media móvil simple de `volume` sobre 20 períodos.
- `volume_ratio_20`: `volume_t / volume_sma_20_t`.

Estas features describen contexto de actividad. No representan señales de volumen, compra, venta o ejecución.

Limitaciones: volumen exchange-specific, sensible a cambios de mercado y no comparable directamente entre venues sin normalización. No representa señal de trading.

## Candle Structure

Features:

- `high_low_range`
- `body_size`
- `upper_wick`
- `lower_wick`
- `body_to_range_ratio`

Miden forma interna de la vela, rango, cuerpo y mechas. Sirven para describir estructura de precio dentro del periodo y presión intraperiodo.

Limitaciones: son descripciones locales, no modelos predictivos. No representan patrón operativo ni señal de estrategia.

## Exclusiones explícitas v1

No forman parte de este catálogo:

- `buy_signal`
- `sell_signal`
- `entry_price`
- `exit_price`
- `strategy_return`
- `position`
- `pnl`
- `backtest_return`
- Order book features.
- Spread.
- On-chain.
- Macro.
- Sentiment.
