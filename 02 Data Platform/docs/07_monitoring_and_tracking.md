# Monitoreo y Tracking

## Objetivo

El monitoreo debe permitir responder rápidamente:

- Qué pipelines corrieron.
- Cuándo corrieron.
- Qué fuente usaron.
- Cuántas filas procesaron.
- Qué validaciones fallaron.
- Qué datos están frescos.
- Qué datos tienen gaps.

## KPIs iniciales

- Active Sources.
- Successful Runs Today.
- Failed Runs Today.
- Last BTC Update.
- Last ETH Update.
- Freshness Score.
- Missing Data Gaps.
- Rows Ingested.

## Fuentes de tracking

- Prefect para ejecución operacional.
- PostgreSQL para metadata auditable.
- Reportes locales en `02 Data Platform/reports/`.
- Logs locales en `02 Data Platform/logs/pipeline_runs/`.

## Mockup

El mockup inicial se encuentra en:

`02 Data Platform/mockups/data_platform_monitoring_v1.html`

No consume APIs reales y usa datos simulados.

