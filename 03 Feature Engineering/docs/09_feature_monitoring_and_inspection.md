# Feature Monitoring and Inspection

## Propósito

La inspección operativa debe permitir revisar que cada ejecución de features sea completa, trazable y consistente con OHLCV fuente.

## Elementos esperados

- Tabla `feature_runs`.
- Tabla `feature_quality_checks`.
- Tabla `ohlcv_features`.
- Vistas operativas futuras para inspección en DBeaver.
- Reportes locales por ejecución.

## Métricas mínimas

- Estado de ejecución.
- Símbolos procesados.
- Timeframes procesados.
- Filas cargadas.
- Filas generadas.
- Filas validadas.
- Filas insertadas.
- Nulls encontrados.
- Infinitos encontrados.
- Duplicados encontrados.
- Violaciones de lookahead.
- `data_quality_score`.

## DBeaver

DBeaver se usará para inspección manual de tablas y vistas. La capa v1 prioriza una tabla ancha para facilitar lectura y comparación directa de columnas.

## Restricción

Las vistas operativas se crearán en bloques posteriores. Bloque 1 solo deja propuesta SQL inicial.
