# Sultan-AI-system

Sultan es un sistema algorítmico de trading con AI, diseñado con enfoque data-first, risk-first y audit-first.

El objetivo inicial es construir una plataforma cuantitativa para investigación, validación, backtesting, paper trading y, solo después de superar controles estrictos, live-small. El alcance inicial es crypto, empezando por BTC y ETH.

## Estado actual

Este repositorio está en fase fundacional. La prioridad es consolidar documentación, arquitectura, mandato, roadmap, estructura técnica y políticas de riesgo antes de implementar lógica compleja o conectarse a ejecución real.

## Reglas iniciales

- No ejecutar trades reales al inicio.
- El LLM puede analizar noticias, eventos, sentimiento y explicar señales, pero no puede ejecutar órdenes.
- El Risk Engine tiene autoridad absoluta de veto.
- Todo resultado debe ser auditable, reproducible y trazable.
- BTC y ETH son los primeros activos soportados.

## Documento principal

El documento rector del proyecto es:

[01 Blueprint + Memo/00_blueprint_unificado.md](<01 Blueprint + Memo/00_blueprint_unificado.md>)

## Estructura numerada por etapas

- `00 Inicio/`: visión general, propósito, objetivos, decisiones iniciales y backlog fundacional.
- `01 Blueprint + Memo/`: blueprint unificado, investment memo, arquitectura, roadmap y política de riesgo.
- `02 Data Platform/`: etapa futura para ingesta, almacenamiento, calidad, metadata y lineage.
- `03 Feature Engineering/`: etapa futura para definición y generación de features.
- `04 Research + Estrategias/`: etapa futura para notebooks de research y estrategias baseline.
- `05 Backtesting/`: etapa futura para simulación histórica robusta.
- `06 Risk Engine/`: etapa futura para controles de riesgo, veto y kill-switch.
- `07 Paper Trading/`: etapa futura para operación simulada en tiempo real.
- `08 Dashboard + Monitoreo/`: etapa futura para métricas, alertas y observabilidad.
- `09 Live Small + Escalamiento/`: etapa futura para exposición mínima bajo controles estrictos.

## Estructura técnica conservada

- `src/sultan/`: paquete principal del sistema.
- `data/`: zonas de datos raw, curated y features.
- `configs/`: configuración versionable no secreta.
- `notebooks/`: investigación exploratoria.
- `tests/`: pruebas.
- `scripts/`: utilidades operativas.
- `logs/`: logs locales no versionados.
