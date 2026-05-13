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

## Notas

Estas decisiones aplican al Bloque 1 y deben revisarse formalmente si cambia el alcance de la etapa.
