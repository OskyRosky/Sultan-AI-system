# Feature Versioning

## Versión inicial

- `feature_set = technical_v1`
- `feature_version = 1.0.0`

`feature_set` identifica una familia estable de features. `feature_version` identifica la definición exacta de cálculo dentro de esa familia.

## Semver

Se usará versionado semántico:

- MAJOR: cambia la definición de una feature existente o su significado conceptual.
- MINOR: se agrega una feature nueva sin cambiar el significado de las existentes.
- PATCH: se corrige un bug sin cambiar el significado conceptual de las features.

## Por qué versionar

El versionado es obligatorio por:

- Reproducibilidad de datasets.
- Auditoría de ejecuciones.
- Backtesting futuro con definiciones estables.
- Comparación entre experimentos.
- Evitar ambigüedad cuando una feature cambia.

## Regla operativa

Nunca se debe sobrescribir silenciosamente el significado de una feature bajo la misma versión. Si cambia la fórmula, ventana, tratamiento de nulls o interpretación conceptual, se debe incrementar versión según semver.
