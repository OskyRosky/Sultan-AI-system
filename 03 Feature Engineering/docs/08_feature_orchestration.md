# Feature Orchestration

## Proposito

Feature Orchestration coordina el flujo real de Feature Engineering:

- cargar OHLCV;
- validar OHLCV;
- calcular las 27 features tecnicas;
- validar quality por familia;
- validar quality integrada;
- aplicar `ready_for_storage`;
- escribir Parquet y PostgreSQL solo cuando se habilite explicitamente.

## Flow Actual

Nombre:

- `generate_features_flow`

El flow es real y controlado. Por defecto:

```text
read_from_db=True
enable_storage=False
limit=1000
allow_full_history=False
```

Esto significa que calcula y valida features, pero no escribe Parquet ni PostgreSQL salvo que `enable_storage=True`.

## Parametros de Control

- `symbols`
- `timeframes`
- `limit`
- `read_from_db`
- `enable_storage`
- `enable_parquet`
- `enable_postgres`
- `require_freshness`
- `allow_full_history`

## Protecciones

- Full history queda bloqueado si `limit is None` y `allow_full_history=False`.
- Storage requiere `read_from_db=True`.
- Storage requiere `ready_for_storage=True`.
- Con `enable_storage=False`, el flow se detiene antes de persistencia.
- No se ejecuta DDL.
- No se crea deployment todavia.

## Secuencia

```text
load_feature_config
-> check_ohlcv_freshness
-> load_ohlcv_data_read_only
-> validate_ohlcv_data
-> calculate returns
-> calculate trend
-> calculate volatility
-> calculate momentum
-> calculate breakout context
-> calculate volume
-> calculate candle structure
-> validate family quality
-> validate integrated quality
-> summarize
-> optional storage
```

## Storage Opcional

Si `enable_storage=True` y `ready_for_storage=True`:

- `prepare_features_for_storage`
- `write_features_parquet` si `enable_parquet=True`
- `store_features_postgres` si `enable_postgres=True`

Si `ready_for_storage=False`, no se escribe nada.

## Estado Actual

Bloque 12 implementa el flow real controlado. El siguiente paso es Monitoring & Inspection. Deployment Prefect queda fuera de este bloque.
