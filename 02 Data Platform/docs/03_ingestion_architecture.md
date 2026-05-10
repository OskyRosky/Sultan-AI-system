# Arquitectura de Ingesta

## Objetivo

La ingesta debe capturar datos externos con trazabilidad completa, persistir una copia raw inmutable y promover solo datos validados a `curated`.

## Pipeline inicial previsto

Flow: `ingest_ohlcv_flow`

Tasks:

- `load_config`: carga configuración local y variables de entorno.
- `fetch_ohlcv`: obtiene OHLCV desde Binance vía CCXT.
- `validate_ohlcv`: valida contrato, duplicados, gaps y reglas de negocio.
- `save_raw_parquet`: guarda la copia raw en Parquet.
- `transform_to_curated`: normaliza campos y tipos para capa curated.
- `save_curated_parquet`: persiste Parquet validado.
- `upsert_postgres`: inserta o actualiza registros validados en PostgreSQL.
- `write_ingestion_run`: registra estado del run.
- `write_quality_report`: registra resultado de validaciones.

## Política raw

La capa raw debe preservar el dato lo más cercano posible a la fuente, agregando metadata mínima:

- `source`
- `run_id`
- `ingested_at`

## Política curated

La capa curated solo recibe datos que pasen validación. Si hay errores de contrato, duplicados inválidos, gaps no explicados o campos nulos críticos, el lote no debe promoverse.

## Ejecución

La primera versión será un flow local de Prefect. No se define deployment programado todavía.

