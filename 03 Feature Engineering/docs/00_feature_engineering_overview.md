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
-> base lista para 04 Research Layer
```

## Estado v1

`03 Feature Engineering` queda cerrada formalmente para `technical_v1 / 1.0.0`.

Snapshot productivo disponible:

```text
manifest_path = 03 Feature Engineering/manifests/feature_snapshot_technical_v1_1_0_0_20260608_163510.json
run_id = 5faf4e40-0087-4a63-95fe-03e9d11a3271
feature_set = technical_v1
feature_version = 1.0.0
```

Estados finales:

```text
feature_engineering_status = closed
feature_snapshot_status = available
backtesting_feature_readiness = ready
stage_09_readiness = blocked
paper_trading_ready = false
```

`backtesting_feature_readiness = ready` significa que `03` entrega un snapshot apto como entrada para `06 Backtesting Engine`. No significa que `06` este implementado, que backtesting ya haya sido ejecutado, ni que Stage 09/Paper Trading esten listos.

Uso downstream obligatorio:

- `06` debe consumir el snapshot desde el manifest.
- `06` debe respetar la politica de warm-up del manifest.
- `06` debe ser gap-aware y leer `docs/gap_report_4h_historical.md`.
- Los consumidores no deben usar glob libre sobre `data/features/**/*.parquet`.

El cierre formal se documenta en:

```text
docs/99_feature_engineering_v1_closure.md
```

Siguiente etapa recomendada: auditoria final de `03` y luego entrada controlada a `06 Backtesting Engine` usando el manifest como input.

## Principios

- Data-first: las features dependen de datos OHLCV confiables.
- Risk-first: se evita introducir señales o supuestos operativos prematuros.
- Audit-first: cada ejecución debe ser trazable con `run_id`.
- No-lookahead: una feature en timestamp T solo puede usar datos hasta T.
- Reproducibilidad: cada cálculo debe identificar `feature_set` y `feature_version`.
