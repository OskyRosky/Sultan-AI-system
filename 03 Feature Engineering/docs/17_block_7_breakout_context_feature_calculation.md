# Bloque 7 - Relative Strength / Breakout Context Feature Calculation

## Objetivo

Implementar features técnicas de Relative Strength / Breakout Context dentro de `05 Feature Calculation Engine`, manteniendo no-lookahead y sin persistencia en Parquet ni PostgreSQL.

Esta familia pertenece al `02 Feature Catalog`. No se crea un subcomponente nuevo ni se renombra la estructura oficial de 03 Feature Engineering.

## Features implementadas

- `close_vs_high_52w`
- `rolling_max_20`
- `rolling_min_20`

## Fórmulas

`rolling_max_20`:

```text
max(high_t ... high_{t-19})
```

`rolling_min_20`:

```text
min(low_t ... low_{t-19})
```

`close_vs_high_52w`:

```text
close_t / rolling_high_52w_t
```

`rolling_high_52w_t` es el máximo móvil de `high` hasta T. Se usa como serie auxiliar interna y no queda en el output final.

## Lookback por timeframe

- `1d`: 365 períodos.
- `4h`: 2190 períodos.

La decisión refleja crypto operando todos los días y seis velas de 4h por día.

## No-lookahead

El cálculo se ordena por `exchange + symbol + timeframe + timestamp` y se ejecuta por grupo.

- `rolling_max_20` usa `high` hasta T.
- `rolling_min_20` usa `low` hasta T.
- `close_vs_high_52w` usa `close_t` y rolling high hasta T.

Ninguna feature usa datos futuros.

## Warm-up periods

- `rolling_max_20`: `NaN` durante los primeros 19 registros por grupo.
- `rolling_min_20`: `NaN` durante los primeros 19 registros por grupo.
- `close_vs_high_52w`: `NaN` hasta completar el lookback 52w del timeframe.

En el flow mock puede no existir suficiente historia para `close_vs_high_52w`; eso es esperado y se valida como warm-up.

## Contexto no señal

Estas features describen contexto relativo a máximos y mínimos. No representan ruptura operativa ni decisión de trading.

No se crean columnas `breakout_signal`, `breakout`, `high_breakout`, `low_breakdown`, `support` ni `resistance`.

## Columnas agregadas

- `close_vs_high_52w`
- `rolling_max_20`
- `rolling_min_20`

## Validación

`feature_quality.py` valida:

- Columnas requeridas.
- Ausencia de infinitos.
- Valores no negativos.
- Warm-up periods esperados.
- Duplicados por clave lógica de features.
- `feature_set`, `feature_version` y `timestamp` válidos.
- Ausencia de columnas prohibidas de señales, estrategia, backtesting, breakout o soporte/resistencia.

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
python -B -m py_compile "03 Feature Engineering/features/breakout_context.py"
python -B -m py_compile "03 Feature Engineering/features/feature_quality.py"
python -B -m py_compile "03 Feature Engineering/flows/generate_features_flow.py"
poetry run python -m pytest "03 Feature Engineering/tests" -q
```

## Próximo paso recomendado

Implementar la familia Volume v1 (`volume_change`, `volume_sma_20`, `volume_ratio_20`) con cálculo por grupo, no-lookahead, quality checks y sin persistencia hasta completar validación de features.
