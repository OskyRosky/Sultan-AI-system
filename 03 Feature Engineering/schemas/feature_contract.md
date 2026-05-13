# Feature Contract

## Identidad

- `feature_set`: `technical_v1`
- `feature_version`: `1.0.0`

## Clave lógica

No se permiten duplicados por:

- `exchange`
- `symbol`
- `timeframe`
- `timestamp`
- `feature_set`
- `feature_version`

## Campos base

- `exchange`
- `symbol`
- `timeframe`
- `timestamp`
- `feature_set`
- `feature_version`
- `run_id`
- `created_at`
- `validated_at`
- `data_quality_score`

## Campos de features v1

- `simple_return`
- `log_return`
- `close_open_return`
- `rolling_std_20`
- `volatility_20`
- `atr_14`
- `sma_20`
- `sma_50`
- `ema_20`
- `ema_50`
- `price_above_sma20`
- `sma20_slope`
- `ema20_above_ema50`
- `rsi_14`
- `macd`
- `macd_signal`
- `close_vs_high_52w`
- `rolling_max_20`
- `rolling_min_20`
- `volume_change`
- `volume_sma_20`
- `volume_ratio_20`
- `high_low_range`
- `body_size`
- `upper_wick`
- `lower_wick`
- `body_to_range_ratio`

## Reglas de calidad

- No duplicados por clave lógica.
- No infinitos.
- Nulls permitidos solo por warm-up period.
- `run_id` obligatorio.
- `feature_set` obligatorio.
- `feature_version` obligatorio.
- `timestamp` obligatorio.
- `data_quality_score` entre 0 y 1.
- No lookahead.
- Cada feature en timestamp T solo puede usar datos hasta T.
- No señales de trading.
