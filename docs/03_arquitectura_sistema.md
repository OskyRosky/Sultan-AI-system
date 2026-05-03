# 03 Arquitectura del Sistema

## Visión general

Sultan se organiza como un sistema modular por capas. La separación entre datos, features, señales, riesgo, ejecución y monitoreo es obligatoria para reducir acoplamiento y facilitar auditoría.

## Componentes principales

- Data Platform: ingesta, almacenamiento, normalización y lineage.
- Feature Layer: generación y validación de variables.
- Research Layer: notebooks y experimentos.
- Strategy Layer: motores analíticos y señales.
- Backtesting Layer: simulación histórica robusta.
- Risk Engine: veto independiente y límites.
- Execution Layer: simulación, paper trading y futura ejecución live-small.
- Monitoring Layer: métricas, alertas y auditoría.

## Estructura técnica inicial

- `src/sultan/config`: configuración interna.
- `src/sultan/data`: ingesta y acceso a datos.
- `src/sultan/features`: generación de features.
- `src/sultan/strategies`: estrategias y motores analíticos.
- `src/sultan/backtesting`: simulación histórica.
- `src/sultan/risk`: controles de riesgo.
- `src/sultan/execution`: paper trading y ejecución futura.
- `src/sultan/monitoring`: métricas y alertas.
- `src/sultan/utils`: utilidades compartidas.

## Principio de seguridad

La ejecución real debe permanecer deshabilitada hasta que el sistema complete documentación, datos, backtesting, risk engine, paper trading y monitoreo.
