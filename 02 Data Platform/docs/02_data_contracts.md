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

## Gaps y freshness implementados

El contrato OHLCV ya cuenta con validación formal de gaps y cálculo de freshness dentro del flow mínimo.

- Los gaps se calculan por `exchange + symbol + timeframe`.
- Para `1d`, el intervalo esperado es 1 día.
- Para `4h`, el intervalo esperado es 4 horas.
- Si `gaps_found > 0`, la validación falla y los datos no pasan a curated ni a PostgreSQL.
- `freshness_lag_seconds` se calcula como `now_utc - max(timestamp)`.
- `data_quality_checks.metadata` guarda detalle de freshness por símbolo/timeframe y detalle de gaps detectados.

Run de validación confirmado: `26c5aba4-e626-41e7-a064-acad2c90c09e`.

- `gaps_found`: `0`.
- `freshness_lag_seconds`: `83575`.
- `data_quality_score`: `1.00000`.

## Versionamiento

Cada contrato deberá evolucionar con cambios explícitos:

- Cambio compatible: agregar un campo opcional.
- Cambio incompatible: renombrar campos, cambiar tipos, eliminar campos o cambiar claves únicas.
- Todo cambio incompatible debe registrarse en `10_decision_log.md`.
