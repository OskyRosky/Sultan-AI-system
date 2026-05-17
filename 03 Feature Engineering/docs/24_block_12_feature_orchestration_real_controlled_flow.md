# Bloque 12 - Feature Orchestration Real Controlled Flow

## Objetivo

Integrar calculo real de features, validacion integrada, Parquet writer y PostgreSQL writer dentro de un flujo controlado de Feature Engineering.

Este bloque pertenece al subcomponente oficial `08 Feature Orchestration`.

## Principio de Seguridad

El flow real es seguro por defecto:

```text
enable_storage=False
```

Con ese default el flow:

- carga OHLCV;
- calcula las 27 features;
- ejecuta validaciones por familia;
- ejecuta validacion integrada;
- retorna resumen;
- no escribe Parquet;
- no inserta en PostgreSQL.

## Parametros del Flow

`generate_features_flow` acepta:

- `symbols: list[str] | None = None`
- `timeframes: list[str] | None = None`
- `limit: int | None = 1000`
- `read_from_db: bool = True`
- `enable_storage: bool = False`
- `enable_parquet: bool = True`
- `enable_postgres: bool = True`
- `require_freshness: bool = True`
- `allow_full_history: bool = False`

## Proteccion Contra Full History

Si `limit is None` y `allow_full_history=False`, el flow falla con error claro:

```text
limit_none_requires_allow_full_history_true
```

Esto evita ejecuciones accidentales sobre historia completa.

## Proteccion de Storage

Si `enable_storage=True`, el flow exige:

- `read_from_db=True`;
- `ready_for_storage=True`;
- `limit` definido salvo `allow_full_history=True`.

Si `enable_storage=False`, no se llama al Parquet writer ni al PostgreSQL writer.

## Orden del Pipeline

1. `load_feature_config`
2. `check_ohlcv_freshness` si `require_freshness=True`
3. `load_ohlcv_data_read_only`
4. `validate_ohlcv_data`
5. calcular returns
6. calcular trend
7. calcular volatility
8. calcular momentum
9. calcular breakout context
10. calcular volume
11. calcular candle structure
12. validar quality por familia
13. validar quality integrada
14. construir summary
15. si `enable_storage=False`, detener antes de persistencia
16. si `enable_storage=True`, preparar storage y escribir segun flags

## ready_for_storage

`ready_for_storage` es el gate obligatorio. Si la validacion integrada no esta lista para storage, el flow no prepara `storage_df`, no escribe Parquet y no inserta en PostgreSQL.

## Parquet

Si `enable_storage=True` y `enable_parquet=True`, el flow escribe Parquet con el storage schema en:

```text
data/features/{feature_set}/{feature_version}/{symbol}/{timeframe}/features_{run_id}.parquet
```

## PostgreSQL

Si `enable_storage=True` y `enable_postgres=True`, el flow usa el write path de Feature Storage:

- `feature_runs`
- `feature_quality_checks`
- `ohlcv_features`

No ejecuta DDL y no crea tablas.

## Fuera de Alcance

Este bloque no crea deployment, no crea schedule, no descarga datos, no llama Binance, no usa CCXT, no crea senales y no crea backtesting.

## Proximo Paso

Avanzar a `09 Feature Monitoring & Inspection` para inspeccionar runs, quality checks, conteos, freshness operacional y estado de features almacenadas.
