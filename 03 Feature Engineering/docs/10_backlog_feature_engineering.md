# Backlog Feature Engineering

## Alta prioridad

- Crear SQL inicial. Completado en Bloque 1.
- Crear flow mock. Completado en Bloque 1.
- Crear script de conexión/lectura OHLCV desde PostgreSQL. Completado en Bloque 2 como loader read-only.
- Implementar cálculo real de returns. Completado en Bloque 3 sin persistencia.
- Implementar cálculo real de trend features. Completado en Bloque 4 sin persistencia.
- Implementar cálculo real de volatility features. Completado en Bloque 5 sin persistencia.
- Implementar cálculo real de momentum features. Completado en Bloque 6 sin persistencia.
- Implementar cálculo real de Relative Strength / Breakout Context features. Completado en Bloque 7 sin persistencia.
- Implementar cálculo real de Volume features. Completado en Bloque 8 sin persistencia.
- Implementar cálculo real de Candle Structure features. Completado en Bloque 9 sin persistencia.
- Implementar validación sin infinitos. Avanzado en Bloque 10 con validación integrada cross-family.
- Implementar validación integral del catálogo técnico v1. Completado en Bloque 10 sin persistencia.
- Implementar readiness para storage. Completado en Bloque 10 como gate lógico sin persistencia.
- Definir contrato de columnas storage. Completado en Bloque 11A.
- Implementar Parquet writer local controlado. Completado en Bloque 11A con tests `tmp_path`.
- Preparar PostgreSQL write path. Completado en Bloque 11B con tests mock, sin DB real.
- Preparar SQL readiness de índices storage. Completado en Bloque 11B como SQL declarativo.
- Ejecutar DDL controlado de Feature Storage. Completado en Bloque 11C sobre `sultan_ai`.
- Ejecutar smoke test real Parquet + PostgreSQL. Completado en Bloque 11C con 200 filas.
- Verificar idempotencia PostgreSQL. Completado en Bloque 11C sin duplicados por unique key.
- Estabilizar y documentar Feature Storage. Completado en Bloque 11D.
- Implementar Feature Orchestration real. Completado en Bloque 12 con storage opcional y guards.
- Crear vistas operativas de Feature Monitoring. Completado en Bloque 13.
- Validar inspeccion en PostgreSQL/DBeaver. Completado en Bloque 13 con vistas `vw_feature_*`.
- Ejecutar Feature Closure final. Completado en Bloque 14.
- Implementar no-lookahead checks.
- Integrar guardado Parquet al pipeline controlado.
- Ver features en DBeaver.

## Media prioridad

- Deployment Prefect.
- Incremental feature generation.
- Umbrales de freshness.
- Feature quality granular por symbol/timeframe.
- Tests unitarios de indicadores.
- Particionado temporal de features Parquet.

## Futuro

- Más pares USDT.
- Features macro.
- Features on-chain.
- Features sentiment.
- Feature store.
- Feast.
- MLflow.
- Grafana.
- Alertas Telegram.
