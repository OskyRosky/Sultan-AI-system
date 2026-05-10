# Contrato de Datos OHLCV

## Objetivo

Definir el contrato mínimo para datos OHLCV usados por Sultan. Este contrato aplica al primer pipeline de Binance vía CCXT para `BTCUSDT` y `ETHUSDT` en timeframes `1d` y `4h`.

## Campos mínimos

| Campo | Tipo esperado | Requerido | Descripción |
|---|---:|---:|---|
| `exchange` | string | sí | Exchange de origen, por ejemplo `binance`. |
| `symbol` | string | sí | Símbolo normalizado, por ejemplo `BTCUSDT`. |
| `timeframe` | string | sí | Timeframe, por ejemplo `1d` o `4h`. |
| `timestamp` | timestamp UTC | sí | Inicio de la vela. |
| `open` | decimal/float | sí | Precio de apertura. |
| `high` | decimal/float | sí | Precio máximo. |
| `low` | decimal/float | sí | Precio mínimo. |
| `close` | decimal/float | sí | Precio de cierre. |
| `volume` | decimal/float | sí | Volumen negociado. |
| `source` | string | sí | Fuente técnica, por ejemplo `ccxt.binance.fetch_ohlcv`. |
| `run_id` | uuid/string | sí | Identificador único de la corrida de ingesta. |
| `ingested_at` | timestamp UTC | sí | Momento en que el dato fue ingerido. |
| `validated_at` | timestamp UTC | sí en curated | Momento en que el dato pasó validación. |
| `data_quality_score` | decimal/float | sí en curated | Score de calidad entre `0` y `1`. |

## Clave única

No debe haber duplicados por:

```text
exchange + symbol + timeframe + timestamp
```

## Reglas de validación

- `timestamp` no puede ser nulo.
- `open`, `high`, `low` y `close` no pueden ser nulos.
- `high >= low`.
- `high >= open`.
- `high >= close`.
- `low <= open`.
- `low <= close`.
- `volume >= 0`.
- No se permiten duplicados por la clave única del contrato.
- Deben detectarse gaps según `timeframe`.
- Debe calcularse freshness para cada `exchange + symbol + timeframe`.

## Gaps esperados por timeframe

- `1d`: diferencia esperada de 1 día entre velas consecutivas.
- `4h`: diferencia esperada de 4 horas entre velas consecutivas.

## Freshness

Freshness mide qué tan actualizado está un dataset frente al momento actual y su timeframe esperado.

Ejemplo conceptual:

```text
freshness_lag = now_utc - max(timestamp)
```

La política exacta de umbrales se definirá en el primer pipeline real.

## Regla de promoción a curated

El dato que no pase validación no debe ir a `curated`. Las fallas deben registrarse en `data_quality_checks` y reportes locales.

