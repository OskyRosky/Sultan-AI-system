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

[docs/01_blueprint_unificado.md](docs/01_blueprint_unificado.md)

## Estructura base

- `docs/`: documentación de mandato, arquitectura, roadmap, riesgo y backlog.
- `src/sultan/`: paquete principal del sistema.
- `data/`: zonas de datos raw, curated y features.
- `configs/`: configuración versionable no secreta.
- `notebooks/`: investigación exploratoria.
- `tests/`: pruebas.
- `scripts/`: utilidades operativas.
- `logs/`: logs locales no versionados.
