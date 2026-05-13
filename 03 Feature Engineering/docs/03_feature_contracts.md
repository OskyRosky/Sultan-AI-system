# Feature Contracts

## Propósito

Los contratos de features definen estructura, reglas mínimas y expectativas de calidad para que las salidas de Feature Engineering sean reproducibles y auditables.

El contrato operativo principal se documenta en `schemas/feature_contract.md`.

## Reglas principales

- Cada fila representa un punto `exchange + symbol + timeframe + timestamp + feature_set + feature_version`.
- No puede haber duplicados para esa clave lógica.
- `run_id` es obligatorio.
- `feature_set` es obligatorio.
- `feature_version` es obligatorio.
- `timestamp` es obligatorio.
- `data_quality_score` debe estar entre 0 y 1.
- No se permiten infinitos.
- Los nulls solo son aceptables por warm-up period documentado.
- No se permiten señales de trading.
- No se permite lookahead.

## Uso esperado

El contrato debe guiar:

- Diseño SQL.
- Validaciones del motor de cálculo.
- Tests unitarios.
- Inspección operativa.
- Documentación de cambios de versión.
