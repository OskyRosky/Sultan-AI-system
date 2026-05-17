# Bloque 11A - Storage Contract + Parquet Writer

## Objetivo

Este bloque pertenece al subcomponente oficial `07 Feature Storage`.

El objetivo es preparar el storage de features sin tocar PostgreSQL. Se implementa:

- Contrato explicito de columnas storage.
- Preparacion del DataFrame preview para storage.
- Inyeccion de metadata de trazabilidad.
- Exclusion de columnas OHLCV crudas.
- Writer Parquet local controlado.
- Tests unitarios con `tmp_path`.

## Fuera de alcance

Este bloque no ejecuta SQL, no crea tablas, no inserta en PostgreSQL, no implementa upsert y no escribe `feature_runs` ni `feature_quality_checks`.

Tampoco modifica formulas de features, no crea nuevas features, no crea senales y no implementa backtesting.

## Preview DataFrame vs Storage DataFrame

El preview DataFrame es la salida del motor de calculo y de la validacion integrada. Contiene:

- Campos base OHLCV: `exchange`, `symbol`, `timeframe`, `timestamp`, `open`, `high`, `low`, `close`, `volume`.
- Metadata de catalogo: `feature_set`, `feature_version`.
- Las 27 features tecnicas de `technical_v1`.

El storage DataFrame elimina OHLCV crudo e incorpora metadata de trazabilidad:

- `run_id`
- `created_at`
- `validated_at`
- `data_quality_score`

## Exclusion de OHLCV crudo

`open`, `high`, `low`, `close` y `volume` pertenecen al dataset OHLCV fuente. El feature storage debe guardar solo identidad, metadata de trazabilidad y columnas de features.

Esta separacion evita duplicar datos fuente, reduce ambiguedad entre precios crudos y features, y mantiene clara la frontera entre Data Platform y Feature Engineering.

## Gate de quality

`prepare_features_for_storage` requiere `integrated_quality_result["ready_for_storage"] == True`.

Si el gate falla, la preparacion se detiene antes de inyectar metadata o escribir archivos. `data_quality_score` se copia desde el resultado integrado y queda como columna por fila en el storage DataFrame.

## Contrato de storage

Identity columns:

- `exchange`
- `symbol`
- `timeframe`
- `timestamp`
- `feature_set`
- `feature_version`
- `run_id`

Metadata columns:

- `created_at`
- `validated_at`
- `data_quality_score`

Feature columns:

- 27 columnas tecnicas de `technical_v1`.

## Ruta Parquet

La ruta definitiva para Parquet es:

```text
data/features/{feature_set}/{feature_version}/{symbol}/{timeframe}/features_{run_id}.parquet
```

Ejemplo:

```text
data/features/technical_v1/1.0.0/BTCUSDT/1d/features_<run_id>.parquet
```

Los tests no escriben en `data/features/`; usan `tmp_path`.

## Granularidad de archivos

`write_features_parquet` escribe un archivo por `symbol/timeframe/run_id`.

Esta granularidad mantiene archivos pequenos y auditables durante v1, permite reescritura idempotente del mismo `run_id`, y prepara una frontera clara para el bloque PostgreSQL posterior.

## Ejecucion de tests

Desde la raiz del proyecto:

```bash
poetry run python -m pytest "03 Feature Engineering/tests" -q
```

## Proximo paso

El siguiente bloque recomendado es 11B: implementar el write path PostgreSQL respetando el orden `feature_runs` antes de `ohlcv_features` por FK, sin cambiar el contrato Parquet definido en 11A.
