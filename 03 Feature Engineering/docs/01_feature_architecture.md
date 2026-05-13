# Feature Architecture

## Relación con 02 Data Platform

03 Feature Engineering inicia después del cierre validado de 02 Data Platform v1. La etapa anterior entrega OHLCV limpio, curado, auditable e idempotente.

La fuente principal será PostgreSQL local:

- Base de datos: `sultan_ai`
- Esquema: `public`
- Tabla fuente: `public.ohlcv_curated`
- Símbolos iniciales: `BTCUSDT`, `ETHUSDT`
- Timeframes iniciales: `1d`, `4h`

03 Feature Engineering no modifica la tabla `ohlcv_curated` ni las tablas de auditoría de 02 Data Platform.

## Flujo lógico

```text
OHLCV validado
-> features técnicas
-> validación
-> Parquet + PostgreSQL
-> vistas operativas
-> inspección
```

El flujo debe ejecutarse únicamente después de validar freshness de OHLCV. El check `check_ohlcv_freshness` es un requisito previo obligatorio antes del cálculo real de features.

## Separación entre features y estrategias

Una feature describe una propiedad observable o derivada del mercado usando datos históricos disponibles hasta un timestamp dado. Una estrategia decide reglas de entrada, salida, sizing, exposición o ejecución.

Esta etapa solo produce features técnicas. No produce decisiones operativas.

Queda explícitamente prohibido crear:

- Señales `BUY`.
- Señales `SELL`.
- Reglas de entrada o salida.
- Posiciones.
- PnL.
- Retornos de estrategia.
- Backtesting.

## Trazabilidad

Cada ejecución de features debe generar o recibir un `run_id` obligatorio. Ese identificador debe conectar:

- Configuración usada.
- Símbolos y timeframes procesados.
- Filas cargadas.
- Filas generadas.
- Validaciones ejecutadas.
- Errores o warnings.
- Artefactos Parquet y registros PostgreSQL.

## Versionado

Todo registro de features debe incluir:

- `feature_set = technical_v1`
- `feature_version = 1.0.0`

Esto permite reproducir experimentos futuros y comparar resultados sin ambigüedad.

## No lookahead

Cada feature en timestamp T solo puede usar datos con timestamp menor o igual a T. No se permite usar información futura, columnas desplazadas hacia atrás ni agregaciones que incluyan observaciones posteriores.

Esta regla es obligatoria para evitar data leakage en research y backtesting futuros.
