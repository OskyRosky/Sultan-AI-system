# 07 Decision Log

Este archivo registra decisiones relevantes de arquitectura, riesgo, datos y operación.

| Fecha | Decisión | Motivo | Impacto |
| --- | --- | --- | --- |
| 2026-05-03 | Sultan inicia como sistema research-first, sin live trading. | Reducir riesgo operativo y construir base auditable. | La ejecución real queda fuera del alcance inicial. |
| 2026-05-03 | BTC y ETH son los activos iniciales. | Mayor liquidez y disponibilidad de datos en crypto. | El diseño inicial se optimiza para estos activos. |
| 2026-05-03 | El Risk Engine tendrá autoridad absoluta de veto. | Separar generación de señales de control de riesgo. | Ninguna estrategia puede ejecutar sin aprobación de riesgo. |
| 2026-05-03 | El LLM no podrá ejecutar órdenes. | Evitar decisiones operativas no deterministas o no controladas. | El LLM queda limitado a análisis, explicación y asistencia. |
