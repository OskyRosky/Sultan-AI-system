# Feature Quality

## Propósito

Feature Quality valida que las features generadas sean estructuralmente correctas, auditables y aptas para persistencia.

## Checks obligatorios

- No duplicados por clave lógica.
- No infinitos.
- `timestamp` no nulo.
- `feature_set` no nulo.
- `feature_version` no nulo.
- Nulls permitidos solo por warm-up period.
- Timestamp alineado con OHLCV fuente.
- No lookahead.
- Cada feature en timestamp T usa solo datos con timestamp menor o igual a T.
- Row count esperado contra OHLCV.
- `data_quality_score` calculado y entre 0 y 1.

## Severidad

Errores estructurales bloquean la promoción a PostgreSQL. Ejemplos:

- Duplicados.
- Infinitos.
- Timestamps nulos.
- `run_id` nulo.
- `feature_set` o `feature_version` nulos.
- Violaciones no-lookahead.

Warnings pueden quedar auditados si no invalidan el dataset, por ejemplo warm-up nulls esperados dentro de ventanas técnicas.

## Resultado

Cada ejecución debe registrar checks en `feature_quality_checks`, incluyendo filas revisadas, filas fallidas, nulls, infinitos, duplicados, violaciones de lookahead y score final.

## Validación integrada cross-family

Desde el Bloque 10, `06 Feature Quality` incluye una validación integrada del dataset completo `technical_v1`.

La validación integrada consolida:

- Catálogo esperado completo: 27 feature columns más campos base y metadata.
- Validadores por familia: returns, trend, volatility, momentum, breakout context, volume y candle structure.
- Columnas prohibidas globales asociadas a señales, estrategias, backtesting o patrones accionables.
- Metadata obligatoria: `feature_set = technical_v1` y `feature_version = 1.0.0`.
- Duplicados por `exchange + symbol + timeframe + timestamp + feature_set + feature_version`.
- Infinitos en columnas de features.
- Nulls esperados por warm-up.
- Resumen por `symbol` y `timeframe`.
- `data_quality_score` entre 0 y 1.
- `ready_for_storage` como gate previo a persistencia futura.

`ready_for_storage` no escribe datos. Solo indica que el preview calculado está apto para que un bloque posterior persista features en Parquet y PostgreSQL.

## Preview schema vs storage schema

`integrated_feature_quality` valida el dataset preview calculado en memoria. Ese preview incluye:

- Campos base OHLCV: `exchange`, `symbol`, `timeframe`, `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Metadata de catálogo: `feature_set`, `feature_version`.
- Las 27 features técnicas de `technical_v1`.

El storage schema futuro agregará columnas de trazabilidad propias del write path, por ejemplo:

- `run_id`
- `validated_at`
- `data_quality_score`
- `created_at` / `updated_at`, si se define en `07 Feature Storage`

Esas columnas no pertenecen al cálculo preview y no deben exigirse en el schema preview. `ready_for_storage` será el gate booleano que permita o bloquee la escritura futura, pero la escritura no se implementa en este bloque.

## data_quality_score v1

`data_quality_score` es una métrica auxiliar entre 0 y 1. Los warnings estructurales de warm-up esperado no penalizan el score de un dataset limpio. Los warnings reales no estructurales sí pueden penalizarlo.

Los errores bloqueantes, columnas faltantes, duplicados, infinitos y columnas prohibidas siguen afectando el resultado. Si existen `blocking_errors`, el score queda limitado a un máximo de `0.5`.

`ready_for_storage` no depende únicamente del score. Sigue siendo un gate booleano basado en ausencia de errores bloqueantes, columnas faltantes, columnas prohibidas, duplicados e infinitos.
