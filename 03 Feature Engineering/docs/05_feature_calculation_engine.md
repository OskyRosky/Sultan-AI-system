# Feature Calculation Engine

## Propósito

El motor de cálculo transformará OHLCV validado en features técnicas reproducibles. En el Bloque 1 solo se define la estructura; no se calculan features reales.

## Entrada esperada futura

- Datos desde `public.ohlcv_curated`.
- Filtrado por `exchange`, `symbol`, `timeframe`.
- Ordenamiento estricto por `timestamp`.
- Freshness validado previamente.

## Salida esperada futura

- DataFrame o estructura tabular ancha.
- Campos base obligatorios.
- Columnas de features v1.
- Metadatos de ejecución.
- Validaciones asociadas.

## Reglas de cálculo

- Usar solo datos hasta timestamp T para producir features en T.
- Evitar transformaciones con leakage.
- Mantener ventanas explícitas.
- Documentar warm-up periods.
- No producir señales ni decisiones operativas.

## Estado Bloque 1

El archivo `flows/generate_features_flow.py` contiene un flow mock/no-op para validar la secuencia lógica sin dependencias externas.
