# Decision Log

## Decisiones iniciales

- 03 Feature Engineering inicia después del cierre de 02 Data Platform v1.
- Se usará `feature_set = technical_v1`.
- Se usará `feature_version = 1.0.0`.
- Se usará tabla ancha para `ohlcv_features`.
- No se usarán señales de trading.
- No se hará backtesting en esta etapa.
- No se hará deployment todavía.
- `check_ohlcv_freshness` será obligatorio antes del cálculo real.
- No-lookahead será regla obligatoria.

## Bloque 2 - OHLCV Read-Only Loader + Freshness Gate

- Se implementa un loader OHLCV read-only contra `public.ohlcv_curated`.
- El flow queda con `read_from_db=False` por defecto para poder compilar y correr sin base de datos.
- `read_from_db=True` queda reservado para lectura controlada desde PostgreSQL.
- El freshness gate se evalúa antes de cualquier cálculo futuro de features.
- El bloque se detiene explícitamente antes de calcular features reales.
- No se guarda Parquet ni se inserta en PostgreSQL en este bloque.

## Bloque 3 - Returns Feature Calculation

- Se implementa cálculo real solo para `simple_return`, `log_return` y `close_open_return`.
- El cálculo se agrupa por `exchange + symbol + timeframe` y se ordena por `timestamp`.
- Se mantiene la etapa sin persistencia: no Parquet, no PostgreSQL, no auditoría real.
- Se mantiene la prohibición de señales, estrategias y backtesting.
- El `NaN` inicial por grupo es esperado para returns que dependen de `close_{t-1}`.
- Los precios no positivos producen `NaN` controlado para evitar infinitos.

## Bloque 4 - Trend Feature Calculation

- Se implementan solo features de tendencia: `sma_20`, `sma_50`, `ema_20`, `ema_50`, `price_above_sma20`, `sma20_slope` y `ema20_above_ema50`.
- Se mantiene la etapa sin persistencia: no Parquet, no PostgreSQL, no auditoría real.
- Se mantiene la prohibición de señales, estrategias y backtesting.
- `ema20_above_ema50` se trata como estado técnico neutral, no como señal.
- No se implementan eventos ni columnas `cross`, `crossover`, `golden_cross` o `death_cross`.

## Bloque 5 - Volatility Feature Calculation

- Se implementan features de volatilidad dentro de `05 Feature Calculation Engine`, sin crear subcomponentes nuevos.
- Se implementan `rolling_std_20`, `volatility_20` y `atr_14`.
- `atr_14` usa previous close por grupo para calcular true range sin lookahead.
- `volatility_20 = rolling_std_20` en v1 para evitar supuestos de anualización por timeframe.
- Se mantiene la etapa sin persistencia: no Parquet, no PostgreSQL, no auditoría real.
- Se mantiene la prohibición de señales, estrategias y backtesting.

## Bloque 6 - Momentum Feature Calculation

- Se implementan features de momentum dentro de `05 Feature Calculation Engine`, sin crear subcomponentes nuevos.
- Se implementan `rsi_14`, `macd` y `macd_signal`.
- RSI usa Wilder-style smoothing con `ewm(alpha=1/14, adjust=False)` y warm-up inicial controlado.
- MACD usa EMA 12 y EMA 26 con `adjust=False`; `macd_signal` usa EMA 9 de MACD.
- RSI y MACD se documentan como indicadores técnicos, no señales.
- Se mantiene la etapa sin persistencia: no Parquet, no PostgreSQL, no auditoría real.
- Se mantiene la prohibición de señales, estrategias y backtesting.

## Bloque 7 - Relative Strength / Breakout Context Feature Calculation

- Se implementan features de Relative Strength / Breakout Context dentro de `05 Feature Calculation Engine`, sin crear subcomponentes nuevos.
- Se implementan `close_vs_high_52w`, `rolling_max_20` y `rolling_min_20`.
- `rolling_max_20` usa `high`; `rolling_min_20` usa `low`.
- `close_vs_high_52w` usa rolling high 52w por timeframe: `1d = 365`, `4h = 2190`.
- `close_vs_high_52w` se documenta como contexto técnico, no señal de ruptura.
- No se crean columnas `breakout_signal`, `breakout`, `support` o `resistance`.
- Se mantiene la etapa sin persistencia: no Parquet, no PostgreSQL, no auditoría real.

## Bloque 8 - Volume Feature Calculation

- Se implementan features de volumen dentro de `05 Feature Calculation Engine`, sin crear subcomponentes nuevos.
- Se implementan `volume_change`, `volume_sma_20` y `volume_ratio_20`.
- `volume_ratio_20` se documenta como contexto relativo de volumen, no señal.
- No se crean columnas `volume_signal` o `volume_spike_signal`.
- Se mantiene la etapa sin persistencia: no Parquet, no PostgreSQL, no auditoría real.
- Se mantiene la prohibición de señales, estrategias y backtesting.

## Notas

Estas decisiones aplican al Bloque 1 y deben revisarse formalmente si cambia el alcance de la etapa.
