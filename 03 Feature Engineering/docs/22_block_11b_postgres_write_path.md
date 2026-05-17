# Bloque 11B - PostgreSQL Write Path

## Objetivo

Este bloque pertenece al subcomponente oficial `07 Feature Storage`.

El objetivo es preparar el write path PostgreSQL para features sin ejecutar DDL, sin crear tablas reales y sin insertar datos reales en PostgreSQL.

## Tablas Involucradas

- `feature_runs`
- `feature_quality_checks`
- `ohlcv_features`

`ohlcv_features.run_id` depende de `feature_runs.run_id`, por lo que el run debe registrarse antes de escribir features.

## Orden Obligatorio de Escritura

1. Insertar `feature_runs` con `status = running`.
2. Revisar `ready_for_storage`.
3. Si `ready_for_storage = False`:
   - insertar registros en `feature_quality_checks`;
   - actualizar `feature_runs` con `status = failed`;
   - no ejecutar upsert en `ohlcv_features`.
4. Si `ready_for_storage = True`:
   - ejecutar upsert en `ohlcv_features`;
   - insertar registros en `feature_quality_checks`;
   - actualizar `feature_runs` con `status = passed`;
   - registrar `rows_inserted`.

## ready_for_storage

`ready_for_storage` es el gate obligatorio del write path. El score por si solo no habilita escritura.

Cuando el gate bloquea, el sistema conserva auditoria del intento mediante `feature_runs` y `feature_quality_checks`, pero no escribe features.

## Upsert Idempotente

La llave de idempotencia de `ohlcv_features` es:

```text
exchange, symbol, timeframe, timestamp, feature_set, feature_version
```

El SQL usa:

```sql
INSERT ... ON CONFLICT (...) DO UPDATE
```

En conflicto se actualizan:

- `run_id`
- `validated_at`
- `data_quality_score`
- las 27 feature columns

`created_at` no se actualiza en conflicto. Ese campo representa la primera vez que la fila fue creada en storage.

## Columnas Excluidas

El write path usa el storage contract y no inserta:

- `open`
- `high`
- `low`
- `close`
- `volume`

Esas columnas pertenecen al OHLCV source y no al feature storage.

## feature_runs

`build_insert_feature_run_payload` prepara el payload de run con:

- identidad del run;
- estado inicial;
- set/version;
- symbols/timeframes;
- row counts;
- metadata.

`insert_feature_run` recibe una conexion ya creada y no hace commit automatico. El control transaccional queda fuera de esta funcion.

`update_feature_run_finished` marca cierre del run con `finished_at`, `status`, `rows_inserted`, `error_message` y metadata.

## feature_quality_checks

`build_quality_check_records` genera registros de quality. Siempre incluye `integrated` y puede incluir validadores por familia si se pasan como argumento.

`insert_feature_quality_checks` inserta los records y devuelve la cantidad insertada.

## Metadata

La metadata final del run incluye:

- `data_quality_score`
- `ready_for_storage`
- `parquet_paths`

`parquet_paths` se guarda como lista de strings si el pipeline ya genero archivos Parquet.

## SQL Readiness

El archivo `001_create_feature_engineering_tables.sql` define las tablas principales, FK, unique key e indices base.

El archivo `002_add_feature_storage_indexes.sql` agrega el indice recomendado:

```sql
CREATE INDEX IF NOT EXISTS idx_ohlcv_features_set_version
    ON ohlcv_features (feature_set, feature_version);
```

Estos archivos son declarativos. No se ejecutan automaticamente en este bloque.

## Fuera de Alcance

Este bloque no ejecuta SQL real, no abre conexiones PostgreSQL, no crea tablas, no hace smoke test real, no escribe Parquet real, no modifica formulas, no crea nuevas features, no crea senales y no implementa backtesting.

## Proximo Paso

El siguiente paso recomendado es ejecutar DDL de forma controlada en un bloque separado y luego hacer un smoke test real con un dataset pequeno ya validado.
