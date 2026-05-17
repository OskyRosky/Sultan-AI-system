# 03 Feature Engineering - Overview

## Propósito

La etapa 03 Feature Engineering convierte datos OHLCV limpios, validados y trazables en features técnicas reproducibles para análisis cuantitativo posterior.

Esta etapa parte de la salida validada de 02 Data Platform v1 y prepara una capa de datos derivada, auditada y versionada. El objetivo no es decidir operaciones ni evaluar rentabilidad, sino construir una base confiable para research, estrategias y backtesting futuros.

## Alcance

Incluye, completado en v1:

- Diseño de arquitectura de features.
- Catálogo técnico v1.
- Contratos de datos.
- Versionado de features.
- Motor de cálculo real con 27 features técnicas.
- Validación de calidad.
- Almacenamiento Parquet y PostgreSQL.
- Orquestación real controlada.
- Vistas operativas para inspección en DBeaver.
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

## Estado v1

`03 Feature Engineering` queda cerrada para `technical_v1 / 1.0.0`.

El cierre formal se documenta en:

```text
docs/99_feature_engineering_v1_closure.md
```

Siguiente etapa recomendada: `04 Research Layer`, una vez que esta etapa este commiteada y limpia.

## Principios

- Data-first: las features dependen de datos OHLCV confiables.
- Risk-first: se evita introducir señales o supuestos operativos prematuros.
- Audit-first: cada ejecución debe ser trazable con `run_id`.
- No-lookahead: una feature en timestamp T solo puede usar datos hasta T.
- Reproducibilidad: cada cálculo debe identificar `feature_set` y `feature_version`.
