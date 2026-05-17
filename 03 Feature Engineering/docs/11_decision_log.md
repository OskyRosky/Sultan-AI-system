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

## Bloque 9 - Candle Structure Feature Calculation

- Se implementan features de estructura de vela dentro de `05 Feature Calculation Engine`, sin crear subcomponentes nuevos.
- Se implementan `high_low_range`, `body_size`, `upper_wick`, `lower_wick` y `body_to_range_ratio`.
- Las features usan solo valores de la misma vela T y no tienen warm-up temporal.
- Se documentan como geometría de vela, no como patrones accionables.
- No se crean columnas `candle_signal`, `doji_signal`, `hammer_signal` o `engulfing_signal`.
- Se mantiene la etapa sin persistencia: no Parquet, no PostgreSQL, no auditoría real.
- Se mantiene la prohibición de señales, estrategias y backtesting.

## Bloque 10 - Integrated Cross-Family Feature Quality

- Se implementa validación integrada cross-family dentro de `06 Feature Quality`, sin crear subcomponentes nuevos.
- No se agregan nuevas features ni se modifican fórmulas existentes.
- Se valida el catálogo `technical_v1` completo de 27 features.
- `ready_for_storage` queda definido como gate lógico previo a storage futuro.
- `data_quality_score` v1 es simple, auditable y limitado entre 0 y 1.
- Se consolida `family_summary` reutilizando validadores por familia.
- Se agrega `symbol_timeframe_summary` para inspección operacional.
- Se mantiene la etapa sin persistencia: no Parquet, no PostgreSQL, no auditoría real.
- Se mantiene la prohibición de señales, estrategias y backtesting.

## Bloque 10.1 - Pre-Storage Review Fixes

- Se aplican correcciones puntuales previas a `07 Feature Storage` sin agregar features nuevas.
- `data_quality_score` no penaliza warnings estructurales de warm-up esperado en datasets limpios.
- Los warnings reales no estructurales, missing columns, duplicados, infinitos, columnas prohibidas y errores bloqueantes siguen afectando quality.
- Si existen `blocking_errors`, `data_quality_score` queda limitado a un máximo de `0.5`.
- `ready_for_storage` se mantiene como gate booleano y no depende únicamente del score.
- Se documenta la diferencia entre preview schema y storage schema: el preview contiene base OHLCV, metadata de catálogo y 27 features; el storage futuro agregará trazabilidad como `run_id`, `validated_at`, `data_quality_score` y potencialmente `created_at` / `updated_at`.
- Las columnas de trazabilidad pertenecen al write path/storage futuro, no al cálculo preview.
- Se refinan diagnósticos de NaN en EMA/MACD para no duplicar errores cuando el origen es `close` faltante.
- Se corrige el mock OHLCV para usar delta de `1d` o `4h` según timeframe en modo `read_from_db=False`.
- Se mantiene la etapa sin persistencia: no Parquet, no PostgreSQL, no SQL, no tablas.

## Bloque 11A - Storage Contract + Parquet Writer

- Se implementa `07 Feature Storage` solo para contrato storage y writer Parquet local.
- PostgreSQL queda fuera de 11A; no se ejecuta SQL, no se crean tablas, no se insertan filas y no se implementa upsert.
- El storage schema excluye columnas OHLCV crudas: `open`, `high`, `low`, `close` y `volume`.
- El storage schema agrega trazabilidad por fila: `run_id`, `created_at`, `validated_at` y `data_quality_score`.
- `ready_for_storage` es gate obligatorio antes de preparar el DataFrame de storage.
- Parquet se escribe con un archivo por `symbol/timeframe/run_id`.
- La ruta definida es `data/features/{feature_set}/{feature_version}/{symbol}/{timeframe}/features_{run_id}.parquet`.
- Los tests del bloque usan `tmp_path` y no escriben datos reales.

## Bloque 11B - PostgreSQL Write Path + DDL Readiness

- Se implementa el write path PostgreSQL como helpers testeables, sin abrir conexiones reales.
- No se ejecuta DDL, no se crean tablas y no se insertan datos reales en PostgreSQL.
- `ready_for_storage` es gate obligatorio antes del upsert de `ohlcv_features`.
- `feature_runs` se inserta antes de `ohlcv_features` para respetar la FK `run_id`.
- Si `ready_for_storage = False`, se registran quality checks, se cierra el run como `failed` y no se ejecuta upsert.
- Si `ready_for_storage = True`, se ejecuta upsert, se registran quality checks y se cierra el run como `passed`.
- El upsert usa la llave `exchange + symbol + timeframe + timestamp + feature_set + feature_version`.
- `created_at` no se sobrescribe en conflicto; conserva la primera creacion de la fila.
- Se agrega SQL declarativo para `idx_ohlcv_features_set_version`; su ejecucion queda para un paso controlado posterior.

## Notas

Estas decisiones aplican al Bloque 1 y deben revisarse formalmente si cambia el alcance de la etapa.
