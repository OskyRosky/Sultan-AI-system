# Fuentes de Datos

## Fase inicial

### Binance vía CCXT

Fuente principal inicial para market data crypto.

- Tipo: exchange centralizado.
- Dataset inicial: OHLCV.
- Símbolos iniciales: `BTCUSDT`, `ETHUSDT`.
- Timeframes iniciales: `1d`, `4h`.
- Librería prevista: `ccxt`.
- Capa de destino inicial: `raw`.
- Capa posterior a validación: `curated`.

## Fases posteriores

### Más pares USDT

Se agregará un universo más amplio de pares USDT cuando el pipeline base sea confiable.

### FRED API

Fuente prevista para indicadores macro como tasas, CPI, M2, DXY u otros indicadores relevantes.

### CoinGecko

Fuente prevista para market cap, volumen agregado y universo crypto.

### On-chain avanzado

Fuentes candidatas: Glassnode, CryptoQuant u otros proveedores equivalentes.

### Noticias y sentimiento

Fuentes candidatas: RSS, CryptoPanic, Fear & Greed.

## Reglas de incorporación

Toda fuente nueva debe documentar:

- Propietario o proveedor.
- Método de acceso.
- Frecuencia esperada.
- Límites de rate limit.
- Campos mínimos.
- Reglas de validación.
- Política de reintentos.
- Impacto esperado en PostgreSQL y filesystem.

