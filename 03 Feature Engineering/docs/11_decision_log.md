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

## Notas

Estas decisiones aplican al Bloque 1 y deben revisarse formalmente si cambia el alcance de la etapa.
