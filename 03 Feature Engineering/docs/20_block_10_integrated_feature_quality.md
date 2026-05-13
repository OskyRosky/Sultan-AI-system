# Bloque 10 - Integrated Cross-Family Feature Quality

## Objetivo

Este bloque fortalece `06 Feature Quality` con una validación integrada del dataset completo de features técnicas v1. No agrega features nuevas y no crea subcomponentes nuevos.

La pregunta operativa que responde es:

```text
¿El dataset completo de features está listo para persistirse en storage en un bloque futuro?
```

## Alcance implementado

Se creó `validate_integrated_feature_dataset`, una validación cross-family que consolida el catálogo `technical_v1` completo:

- 11 columnas base y de metadata.
- 27 columnas de features técnicas.
- Validaciones por familia ya existentes.
- Resumen por `symbol` y `timeframe`.
- `data_quality_score` simple y auditable.
- `ready_for_storage` como gate previo a persistencia futura.

## Qué valida

- Dataset no vacío.
- Columnas esperadas presentes.
- Columnas prohibidas ausentes.
- `feature_set = technical_v1`.
- `feature_version = 1.0.0`.
- `exchange`, `symbol`, `timeframe` y `timestamp` no nulos.
- No duplicados por `exchange + symbol + timeframe + timestamp + feature_set + feature_version`.
- No infinitos en columnas de features.
- Nulls esperados por warm-up, reportados por familia.
- Resultado de validadores de returns, trend, volatility, momentum, breakout context, volume y candle structure.

## Ready for storage

`ready_for_storage = True` solo si:

- `status = passed`.
- No hay errores bloqueantes.
- No faltan columnas esperadas.
- No existen columnas prohibidas.
- No hay duplicados.
- No hay infinitos.
- Metadata de `feature_set` y `feature_version` es válida.

Este flag no persiste nada; solo prepara el criterio de promoción para el bloque de storage.

## Data quality score

`data_quality_score` v1 es una métrica simple:

- Parte de `1.0`.
- Penaliza columnas faltantes.
- Penaliza duplicados.
- Penaliza infinitos.
- Penaliza warnings de forma moderada.
- Si hay errores bloqueantes, el score queda limitado a máximo `0.5`.
- Siempre queda entre `0.0` y `1.0`.

El objetivo no es modelar calidad perfecta, sino producir una métrica auditable y estable para gates futuros.

## Errores bloqueantes

Son bloqueantes:

- Dataset vacío.
- Columnas esperadas faltantes.
- Columnas prohibidas como `signal`, `buy_signal`, `sell_signal`, `pnl`, `strategy_return`, `backtest_return`, `cross`, `breakout_signal`, `volume_signal` o `candle_signal`.
- Metadata inválida.
- Identidad nula.
- Duplicados.
- Infinitos.
- Fallos en validadores por familia.

## Warnings

Son warnings:

- Columnas inesperadas no prohibidas.
- Features totalmente nulas por warm-up cuando el dataset preview no tiene historia suficiente, por ejemplo `close_vs_high_52w` en mocks pequeños.
- Warm-up esperado reportado por validadores de familia.

## Qué NO hace este bloque

- No calcula features nuevas.
- No modifica fórmulas existentes.
- No guarda Parquet.
- No inserta en PostgreSQL.
- No crea tablas.
- No crea señales.
- No crea backtesting.
- No modifica `02 Data Platform`.
- No crea deployments.

## Validación

Desde la raíz del proyecto:

```bash
python -B -m py_compile "03 Feature Engineering/features/integrated_feature_quality.py"
python -B -m py_compile "03 Feature Engineering/features/feature_quality.py"
python -B -m py_compile "03 Feature Engineering/flows/generate_features_flow.py"
poetry run python -m pytest "03 Feature Engineering/tests" -q
```

## Próximo paso recomendado

Implementar el bloque de storage controlado: persistencia Parquet y PostgreSQL solo si `ready_for_storage = True`, manteniendo idempotencia, auditoría y rollback lógico.
