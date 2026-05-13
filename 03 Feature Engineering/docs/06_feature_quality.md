# Feature Quality

## Propósito

Feature Quality valida que las features generadas sean estructuralmente correctas, auditables y aptas para persistencia.

## Checks obligatorios

- No duplicados por clave lógica.
- No infinitos.
- `timestamp` no nulo.
- `run_id` no nulo.
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
