# Sultan-AI-system

Sultan es un sistema algorítmico de trading con AI, diseñado con enfoque data-first, risk-first y audit-first.

El objetivo inicial es construir una plataforma cuantitativa para investigación, validación, backtesting, paper trading y, solo después de superar controles estrictos, live-small. El alcance inicial es crypto, empezando por BTC y ETH.

## Estado actual

Este repositorio ya contiene las capas iniciales de datos, features, research, strategy framework y backtesting framework. La prioridad sigue siendo operar con enfoque data-first, research-first, risk-first y audit-first antes de cualquier paper trading o live-small.

`06 Backtesting Engine` queda cerrado como motor de raw execution scaffold, raw diagnostics y handoff contractual. Su artefacto terminal es `RawDiagnosticsHandoffContract`; no autoriza paper trading, live trading ni despliegue.

`08 Risk Engine` queda cerrado como framework documental no operativo. `09 Paper Trading` permanece bloqueado; el orden oficial previo a cualquier discusion de Stage 09 es `General -> 02 -> 06 -> General`, segun [00 Inicio/05_pre_stage_09_readiness_plan.md](<00 Inicio/05_pre_stage_09_readiness_plan.md>).

La frontera oficial entre cierre estructural V1 y maduración operativa V2 está definida en [00 Inicio/06_v1_completion_strategy_and_v2_operational_roadmap.md](<00 Inicio/06_v1_completion_strategy_and_v2_operational_roadmap.md>). El contrato de alineación 06→07 para Motor B raw diagnostics está definido en `07 Signal Fusion + LLM Motors/docs/14_motor_b_raw_diagnostics_adapter_contract.md`.

`07 Signal Fusion + LLM Motors` tiene un minimal executable dry-run V1 para validar contratos y handoffs con mocks sintéticos. No procesa evidencia real, no llama LLMs, no genera confidence, no produce señales operativas y no desbloquea Paper Trading.

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
- `02 Data Platform/`: ingesta, almacenamiento, calidad, metadata y lineage de datos OHLCV.
- `03 Feature Engineering/`: definición, generación, validación y storage de features técnicas.
- `04 Research Layer/`: research cuantitativo auditado y framework de evidencia.
- `05 Strategy Engine/`: construcción gobernada de candidatos, reglas, quality gates y dossiers.
- `06 Backtesting Engine/`: framework/director de evaluación histórica gobernada.
- `07 Signal Fusion + LLM Motors/`: etapa futura para completar Motor A, agregar Motor C y construir Signal Fusion.
- `08 Risk Engine/`: etapa futura para controles de riesgo, veto y kill-switch.
- `09 Paper Trading/`: etapa futura para operación simulada en tiempo real.
- `10 Dashboard + Monitoreo/`: etapa futura para métricas, alertas y observabilidad.
- `11 Live Small + Escalamiento/`: etapa futura para exposición mínima bajo controles estrictos.

## Nota sobre 07 Signal Fusion + LLM Motors

`07` no debe rehacer Motor A desde cero. Parte del trabajo de Motor A ya existe parcialmente en `04 Research Layer`, especialmente `Regime Detection v1`. La futura etapa 07 debe tomar ese trabajo como input parcial, completar lo que falte del Motor A macro/fundamental, agregar Motor C como LLM/event classifier y construir la fusión de señales entre Motor A, Motor B y Motor C.

No se debe construir `07`, `08 Risk Engine`, paper trading ni live-small hasta validar los outputs reales de las etapas previas y sus límites.

## Estructura técnica conservada

- `src/sultan/`: paquete principal del sistema.
- `data/`: zonas de datos raw, curated y features.
- `configs/`: configuración versionable no secreta.
- `notebooks/`: investigación exploratoria.
- `tests/`: pruebas.
- `scripts/`: utilidades operativas.
- `logs/`: logs locales no versionados.
