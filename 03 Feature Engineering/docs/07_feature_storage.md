# Feature Storage

## Decisión v1

Se usará tabla ancha en PostgreSQL.

Tabla sugerida:

- `ohlcv_features`

Cada feature será una columna. No se usará formato long/key-value en v1.

## Razones

- DBeaver más simple para inspección.
- Pandas más simple para research.
- Menos pivoteos.
- Catálogo v1 pequeño y conocido.
- Lectura más directa por símbolo, timeframe y timestamp.

## PostgreSQL

`ohlcv_features` debe incluir:

- Campos base.
- Columnas de features v1.
- Constraints básicas.
- Unique key por `exchange + symbol + timeframe + timestamp + feature_set + feature_version`.
- Índices útiles por `symbol`, `timeframe` y `timestamp`.

## Parquet

Los datos reales de features deben guardarse fuera de `03 Feature Engineering`, en:

```text
/Users/sultan/Trading/Sultan-AI-system/data/features/
```

Estructura esperada:

```text
data/features/
└── technical/
    ├── BTCUSDT/
    │   ├── 1d/
    │   └── 4h/
    └── ETHUSDT/
        ├── 1d/
        └── 4h/
```

## Restricción Bloque 1

En este bloque no se guardan Parquet reales ni se insertan features en PostgreSQL.
