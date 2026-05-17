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
- Columnas de trazabilidad del write path como `run_id`, `validated_at`, `data_quality_score` y, si aplica, `created_at` / `updated_at`.
- Constraints básicas.
- Unique key por `exchange + symbol + timeframe + timestamp + feature_set + feature_version`.
- Índices útiles por `symbol`, `timeframe` y `timestamp`.

## Frontera preview vs storage

El dataset preview validado por `06 Feature Quality` contiene campos base OHLCV, `feature_set`, `feature_version` y las 27 features técnicas de `technical_v1`.

Las columnas de trazabilidad pertenecen al storage schema y se agregarán en el write path futuro. No forman parte del cálculo preview y no se implementan en el Bloque 10.1.

## Parquet

Los datos reales de features deben guardarse fuera de `03 Feature Engineering`, en:

```text
/Users/sultan/Trading/Sultan-AI-system/data/features/
```

Estructura esperada:

```text
data/features/
└── {feature_set}/
    └── {feature_version}/
        └── {symbol}/
            └── {timeframe}/
                └── features_{run_id}.parquet
```

Ejemplo:

```text
data/features/technical_v1/1.0.0/BTCUSDT/1d/features_<run_id>.parquet
```

Parquet usa el storage schema, no el preview schema. Por eso no incluye `open`, `high`, `low`, `close` ni `volume`.

## Estado Bloque 11A

Bloque 11A implementa solo contrato de storage y writer Parquet local controlado. PostgreSQL queda fuera de 11A y se reserva para 11B.
