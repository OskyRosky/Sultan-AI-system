# Bloque 8 - Volume Feature Calculation

## Objetivo

Implementar features técnicas de volumen dentro de `05 Feature Calculation Engine`, manteniendo no-lookahead y sin persistencia en Parquet ni PostgreSQL.

Volume es una familia del `02 Feature Catalog`. No se crea un subcomponente nuevo ni se renombra la estructura oficial de 03 Feature Engineering.

## Features implementadas

- `volume_change`
- `volume_sma_20`
- `volume_ratio_20`

## Fórmulas

`volume_change`:

```text
volume_t / volume_{t-1} - 1
```

`volume_sma_20`:

```text
mean(volume_t ... volume_{t-19})
```

`volume_ratio_20`:

```text
volume_t / volume_sma_20_t
```

## No-lookahead

El cálculo se ordena por `exchange + symbol + timeframe + timestamp` y se ejecuta por grupo.

- `volume_change` usa `volume_t` y `volume_{t-1}`.
- `volume_sma_20` usa volumen hasta T.
- `volume_ratio_20` usa `volume_t` y `volume_sma_20_t`.

Ninguna feature usa datos futuros.

## Warm-up periods

- `volume_change`: `NaN` en el primer registro por grupo.
- `volume_sma_20`: `NaN` durante los primeros 19 registros por grupo.
- `volume_ratio_20`: `NaN` mientras `volume_sma_20` no exista.

Si `volume_{t-1} <= 0`, `volume_change` queda `NaN`. Si `volume_sma_20 <= 0`, `volume_ratio_20` queda `NaN`.

## Contexto no señal

Estas features describen actividad relativa de volumen. Volumen alto o bajo no se interpreta como señal accionable en esta etapa.

No se crean columnas `volume_signal` ni `volume_spike_signal`.

## Columnas agregadas

- `volume_change`
- `volume_sma_20`
- `volume_ratio_20`

No se conservan columnas auxiliares en el output final.

## Validación

`feature_quality.py` valida:

- Columnas requeridas.
- Ausencia de infinitos.
- `volume_sma_20` y `volume_ratio_20` no negativos.
- Warm-up periods esperados.
- Duplicados por clave lógica de features.
- `feature_set`, `feature_version` y `timestamp` válidos.
- Ausencia de columnas prohibidas de señales, estrategia o backtesting.

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
python -B -m py_compile "03 Feature Engineering/features/volume.py"
python -B -m py_compile "03 Feature Engineering/features/feature_quality.py"
python -B -m py_compile "03 Feature Engineering/flows/generate_features_flow.py"
poetry run python -m pytest "03 Feature Engineering/tests" -q
```

## Próximo paso recomendado

Implementar la familia Candle Structure v1 (`high_low_range`, `body_size`, `upper_wick`, `lower_wick`, `body_to_range_ratio`) con no-lookahead, quality checks y preview sin persistencia.
