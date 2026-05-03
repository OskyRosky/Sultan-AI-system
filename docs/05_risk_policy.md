# 05 Risk Policy

## Principio central

El Risk Engine tiene autoridad absoluta de veto. Ninguna estrategia, modelo, señal, proceso automático o LLM puede omitirlo.

## Estado inicial permitido

- Investigación.
- Backtesting.
- Paper trading.
- Monitoreo.

## Estado inicial prohibido

- Ejecución real de órdenes.
- Apalancamiento.
- Escalamiento automático de exposición.
- Cambios automáticos de límites de riesgo.

## Controles mínimos futuros

- Límite por posición.
- Límite por activo.
- Límite de exposición total.
- Límite de pérdida diaria.
- Límite de drawdown.
- Control de correlación.
- Control de frescura de datos.
- Control de anomalías.
- Kill-switch manual.
- Kill-switch automático.

## Auditoría

Cada veto, aprobación o reducción de tamaño debe registrar:

- Timestamp.
- Datos disponibles.
- Señal recibida.
- Límites aplicados.
- Decisión tomada.
- Razón de la decisión.
