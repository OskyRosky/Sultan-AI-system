# Feature Calculation Engine

## Proposito

El motor de calculo transforma OHLCV validado en un dataset preview de features tecnicas reproducibles para `technical_v1`.

La etapa actual calcula features en memoria y se detiene antes de cualquier persistencia. No escribe Parquet, no inserta en PostgreSQL y no crea tablas.

## Entrada

- OHLCV con campos base: `exchange`, `symbol`, `timeframe`, `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Datos ordenados por `exchange`, `symbol`, `timeframe` y `timestamp`.
- Freshness gate evaluado antes del calculo.
- Validacion OHLCV previa al calculo de features.

## Salida Preview

El resultado preview conserva las columnas base y agrega metadata de catalogo:

- `feature_set = technical_v1`
- `feature_version = 1.0.0`

Tambien agrega 27 features tecnicas distribuidas en 7 familias.

## Familias Implementadas

### Returns

- `simple_return`
- `log_return`
- `close_open_return`

### Trend

- `sma_20`
- `sma_50`
- `ema_20`
- `ema_50`
- `price_above_sma20`
- `sma20_slope`
- `ema20_above_ema50`

### Volatility

- `rolling_std_20`
- `volatility_20`
- `atr_14`

### Momentum

- `rsi_14`
- `macd`
- `macd_signal`

### Relative Strength / Breakout Context

- `close_vs_high_52w`
- `rolling_max_20`
- `rolling_min_20`

### Volume

- `volume_change`
- `volume_sma_20`
- `volume_ratio_20`

### Candle Structure

- `high_low_range`
- `body_size`
- `upper_wick`
- `lower_wick`
- `body_to_range_ratio`

## Reglas de Calculo

- Cada feature en timestamp T usa solo informacion disponible hasta T.
- Los calculos se agrupan por `exchange + symbol + timeframe`.
- Las ventanas rolling y los periodos de warm-up quedan explicitos.
- Los `NaN` de warm-up son esperados cuando no hay historia suficiente.
- EMA y MACD se calculan con `ewm(..., adjust=False)` y no generan senales.

## Restricciones Actuales

- No se crean senales BUY/SELL.
- No se crean columnas accionables como `signal`, `cross`, `breakout_signal` o equivalentes.
- No se implementa backtesting.
- No se implementa storage.
- No se guarda Parquet.
- No se inserta en PostgreSQL.

## Estado Actual

`flows/generate_features_flow.py` ejecuta un preview read-only:

1. Carga configuracion.
2. Evalua freshness.
3. Carga OHLCV real en modo read-only o mock en `read_from_db=False`.
4. Valida OHLCV.
5. Calcula las 7 familias de features.
6. Ejecuta validadores por familia.
7. Ejecuta validacion integrada cross-family.
8. Se detiene antes de persistencia.

El siguiente paso permitido despues del quality gate es disenar e implementar Feature Storage en el subcomponente `07 Feature Storage`.
