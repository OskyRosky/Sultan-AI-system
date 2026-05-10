# Contratos de Datos

## Propósito

Los contratos de datos definen la interfaz entre fuentes, ingesta, almacenamiento, validación y consumo posterior. En Sultan, los contratos son obligatorios para evitar que datos ambiguos o inválidos entren a capas confiables.

## Contrato inicial

El primer contrato formal es `OHLCV`, documentado en:

`02 Data Platform/schemas/ohlcv_contract.md`

## Reglas generales

- Todo registro debe tener `source`, `run_id` e `ingested_at`.
- Todo registro que pase a `curated` debe tener `validated_at`.
- Los campos temporales deben ser consistentes y parseables.
- Las validaciones deben ejecutarse antes de escribir en `curated`.
- Las fallas de validación deben generar reporte y bloquear la promoción a `curated`.

## Versionamiento

Cada contrato deberá evolucionar con cambios explícitos:

- Cambio compatible: agregar un campo opcional.
- Cambio incompatible: renombrar campos, cambiar tipos, eliminar campos o cambiar claves únicas.
- Todo cambio incompatible debe registrarse en `10_decision_log.md`.

