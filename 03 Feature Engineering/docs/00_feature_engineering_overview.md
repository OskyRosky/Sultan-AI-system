# 03 Feature Engineering - Overview

## Propósito

La etapa 03 Feature Engineering convierte datos OHLCV limpios, validados y trazables en features técnicas reproducibles para análisis cuantitativo posterior.

Esta etapa parte de la salida validada de 02 Data Platform v1 y prepara una capa de datos derivada, auditada y versionada. El objetivo no es decidir operaciones ni evaluar rentabilidad, sino construir una base confiable para research, estrategias y backtesting futuros.

## Alcance

Incluye:

- Diseño de arquitectura de features.
- Catálogo técnico v1.
- Contratos de datos.
- Versionado de features.
- Motor de cálculo futuro.
- Validación de calidad.
- Propuesta de almacenamiento en Parquet y PostgreSQL.
- Orquestación mock/no-op inicial.
- Documentación operativa.

No incluye:

- Señales BUY/SELL.
- Estrategias de trading.
- Backtesting.
- Paper trading.
- Live trading.
- Ejecución de órdenes.
- Agentes LLM.
- Descarga de datos.

## Flujo objetivo

```text
OHLCV validado
-> features técnicas
-> validación de features
-> almacenamiento Parquet + PostgreSQL
-> vistas operativas
-> inspección en DBeaver
-> base lista para Research + Estrategias
```

## Principios

- Data-first: las features dependen de datos OHLCV confiables.
- Risk-first: se evita introducir señales o supuestos operativos prematuros.
- Audit-first: cada ejecución debe ser trazable con `run_id`.
- No-lookahead: una feature en timestamp T solo puede usar datos hasta T.
- Reproducibilidad: cada cálculo debe identificar `feature_set` y `feature_version`.
