# Bloque 2 - OHLCV Read-Only Loader + Freshness Gate

## Objetivo

Crear una capa mínima y controlada para leer OHLCV desde PostgreSQL, validar su estructura y ejecutar un freshness gate antes de cualquier cálculo futuro de features.

## Qué se implementó

- Configuración mínima de Feature Engineering.
- Loader read-only para `public.ohlcv_curated`.
- Validación estructural de OHLCV en DataFrames.
- Freshness gate por `symbol` y `timeframe`.
- Flow de preview operativo que se detiene antes de calcular features.
- Tests unitarios con DataFrames mock.

## Por qué es read-only

Este bloque solo prepara datos para Feature Engineering. No debe modificar datos reales, tablas de 02 Data Platform ni auditoría existente.

El loader ejecuta `SELECT` sobre PostgreSQL y usa sesión read-only. No crea tablas, no inserta, no actualiza y no borra registros.

## Relación con 02 Data Platform

02 Data Platform entrega la tabla fuente validada:

- Base de datos: `sultan_ai`
- Usuario local: `sultan_user`
- Tabla fuente: `public.ohlcv_curated`

03 Feature Engineering consume esa tabla como entrada confiable, sin modificarla.

## Loader OHLCV

El loader soporta:

- `symbol`
- `timeframe`
- `start_timestamp`
- `end_timestamp`
- `limit`

Columnas leídas:

- `exchange`
- `symbol`
- `timeframe`
- `timestamp`
- `open`
- `high`
- `low`
- `close`
- `volume`

La salida es un `pandas.DataFrame` ordenado por `symbol`, `timeframe`, `timestamp`.

## Validación OHLCV

La validación mínima revisa:

- DataFrame no vacío.
- Columnas requeridas.
- Campos clave no nulos.
- OHLCV y volumen no nulos.
- Tipos numéricos válidos.
- Timestamp convertible a datetime.
- No duplicados por `exchange + symbol + timeframe + timestamp`.
- Timestamp ordenado por `symbol/timeframe`.
- Reglas OHLC: `high >= low`, `high >= open`, `high >= close`, `low <= open`, `low <= close`.
- `volume >= 0`.

## Freshness Gate

El freshness gate lee el último timestamp disponible para cada `symbol/timeframe` y calcula el lag contra el tiempo actual UTC.

Umbrales:

- `1d`: máximo 2 días.
- `4h`: máximo 12 horas.

Devuelve `status`, `symbol`, `timeframe`, `latest_timestamp`, `current_time`, `max_allowed_lag`, `observed_lag`, `passed` y `message`.

## Qué NO hace este bloque

- No calcula features reales.
- No crea señales BUY/SELL.
- No crea estrategias.
- No ejecuta backtesting.
- No guarda Parquet.
- No inserta en PostgreSQL.
- No modifica `ohlcv_curated`.
- No modifica `ingestion_runs`.
- No modifica `data_quality_checks`.
- No crea deployments.

## Cómo validar

Desde la raíz del proyecto:

```bash
python -B -m py_compile "03 Feature Engineering/flows/generate_features_flow.py"
python -B -m py_compile "03 Feature Engineering/features/config.py"
python -B -m py_compile "03 Feature Engineering/features/ohlcv_loader.py"
python -B -m py_compile "03 Feature Engineering/features/freshness_gate.py"
python -B -m py_compile "03 Feature Engineering/features/ohlcv_validation.py"
poetry run pytest "03 Feature Engineering/tests" -q
```

El flow por defecto usa `read_from_db=False`, por lo que puede correr sin PostgreSQL ni variables de entorno.

## Próximo paso recomendado

Implementar cálculo real de las primeras features de returns sobre el DataFrame validado, manteniendo freshness gate obligatorio antes del cálculo y sin persistencia hasta validar quality checks.
