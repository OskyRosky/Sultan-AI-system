# Sultan Algo AI-system — Blueprint Unificado

## 1. Propósito del sistema

Sultan es una plataforma algorítmica de trading con AI orientada a investigación, validación sistemática, gestión de riesgo, ejecución controlada y auditoría completa. Su objetivo no es operar rápido, sino construir una infraestructura confiable para convertir datos en decisiones cuantitativas verificables.

El enfoque inicial es crypto, empezando por BTC y ETH. Antes de cualquier ejecución real, Sultan debe demostrar calidad de datos, robustez de señales, backtesting reproducible, controles de riesgo independientes, paper trading estable y monitoreo completo.

## 2. Principios rectores

- Data-first: ninguna señal se acepta sin datos trazables, validados y reproducibles.
- Risk-first: el riesgo se diseña antes que la ejecución.
- Audit-first: toda decisión debe poder reconstruirse.
- Research before trading: primero investigación, luego backtesting, luego paper trading, luego live-small.
- Simplicidad inicial: evitar complejidad prematura.
- Independencia del Risk Engine: ninguna estrategia puede saltarse sus controles.
- Separación de responsabilidades: datos, señales, riesgo, ejecución y monitoreo deben operar como capas distinguibles.
- Human-in-the-loop al inicio: las decisiones críticas requieren revisión humana.

## 3. Mandato y gobernanza

Sultan tiene mandato de construir una plataforma cuantitativa disciplinada. En la fase inicial no tiene mandato para ejecutar trades reales.

El LLM puede:

- Analizar noticias, eventos, narrativas, sentimiento y documentación.
- Generar explicaciones de señales o cambios de régimen.
- Asistir en research, documentación y revisión.

El LLM no puede:

- Ejecutar órdenes.
- Modificar límites de riesgo sin aprobación.
- Omitir controles del Risk Engine.
- Convertir una señal en trade sin pasar por validación, riesgo y autorización del modo operativo.

La gobernanza del sistema se basa en registros versionados, decisiones documentadas, pruebas reproducibles y autorización explícita para avanzar entre etapas.

## 4. Arquitectura por 10 capas

### Capa 0: Mandato y Gobernanza

Define el propósito, límites, reglas no negociables, roles humanos, criterios para pasar de research a paper trading y de paper trading a live-small.

### Capa 1: Fuentes de Datos

Incluye precios, volumen, order book, funding, open interest, datos on-chain, noticias, calendario macro, sentimiento y fuentes alternativas. Al inicio se priorizan datos confiables para BTC y ETH.

### Capa 2: Ingesta y Almacenamiento

Gestiona conectores, descargas, normalización, particionado, versionado, almacenamiento raw y curated. Debe preservar datos originales y generar datasets reproducibles.

### Capa 3: Feature Engineering

Construye features técnicas, microestructurales, estadísticas, on-chain, de sentimiento y de régimen. Toda feature debe tener definición, ventana temporal, fuente y validación.

### Capa 4: Regime Detection

Identifica condiciones de mercado como tendencia, rango, alta volatilidad, baja liquidez, estrés, eventos extremos y cambios estructurales. Las estrategias deben conocer el régimen antes de producir señales operativas.

### Capa 5: Motores Analíticos

Agrupa modelos y enfoques cuantitativos: momentum, mean reversion, breakout, volatilidad, trend following, modelos estadísticos, modelos ML, NLP para noticias y análisis de eventos.

### Capa 6: Validación y Signal Fusion

Evalúa calidad de señal, consistencia entre motores, correlación, redundancia, incertidumbre, filtros de régimen y condiciones mínimas para proponer una operación.

### Capa 7: Risk Engine Independiente

Controla exposición, tamaño de posición, drawdown, concentración, stop conditions, límites diarios, límites por activo, límites de correlación, modo kill-switch y veto absoluto. Su decisión prevalece sobre cualquier estrategia.

### Capa 8: Portfolio y Ejecución

Convierte señales aprobadas en intención de portfolio, simula ejecución, mide slippage, controla órdenes y, en fases futuras, permite ejecución live-small bajo límites estrictos.

### Capa 9: Monitoreo, Dashboard y Alertas

Muestra estado de datos, señales, riesgo, performance, PnL, drawdown, eventos, errores, latencia y auditoría. Debe permitir entender qué ocurrió, cuándo ocurrió y por qué.

## 5. Capas transversales

### Data Quality, Metadata y Lineage

Cada dataset debe tener controles de completitud, duplicados, frescura, rangos, outliers, gaps, schema y origen. Las transformaciones deben registrar lineage desde raw hasta features.

### Governance, MLflow y Model Lifecycle

Los experimentos, modelos, parámetros, métricas, artefactos y versiones deben registrarse. Ningún modelo debe pasar a paper trading sin evidencia de validación.

### Audit, Replay y Trazabilidad

El sistema debe poder reproducir decisiones históricas: datos usados, features calculadas, señales generadas, filtros aplicados, decisión del Risk Engine y acción final.

## 6. Roadmap por 14 etapas

### Etapa 0: Inicio

Crear documentación base, mandato, estructura del repositorio y reglas no negociables.

### Etapa 1: Setup Mac + Repo

Configurar entorno local, dependencias base, estándares de código, estructura de carpetas y control de versiones.

### Etapa 2: Investment Memo Final

Definir tesis de inversión, límites, universos operables, hipótesis iniciales y criterios de éxito.

### Etapa 3: Data Platform MVP

Implementar ingesta inicial para BTC y ETH, almacenamiento raw/curated y reproducibilidad básica.

### Etapa 4: Data Quality + Lineage

Agregar validaciones de datos, metadatos, tracking de transformaciones y reportes de calidad.

### Etapa 5: Feature Layer MVP

Crear features iniciales con definiciones versionadas y pruebas básicas.

### Etapa 6: Research Notebook Base

Construir notebooks de investigación controlados para explorar hipótesis sin contaminar producción.

### Etapa 7: Primeras Estrategias

Implementar estrategias simples y explicables como baseline: momentum, breakout y mean reversion.

### Etapa 8: Backtesting Robusto

Incluir costos, slippage, walk-forward, splits temporales, métricas de riesgo y análisis de sensibilidad.

### Etapa 9: Regime Detection

Detectar regímenes de mercado y evaluar comportamiento de estrategias por régimen.

### Etapa 10: Signal Fusion

Combinar señales con reglas explícitas, scoring, filtros de incertidumbre y control de redundancia.

### Etapa 11: Risk Engine

Implementar motor de riesgo independiente con veto, límites, kill-switch y auditoría.

### Etapa 12: Paper Trading

Simular operación en tiempo real sin capital real. Medir estabilidad, latencia, señales, riesgo y diferencias contra backtest.

### Etapa 13: Dashboard + Monitoreo

Crear visibilidad operativa: datos, señales, riesgo, performance, alertas y auditoría.

### Etapa 14: Live-Small + Escalamiento

Permitir exposición mínima, controlada y reversible solo si paper trading cumple criterios definidos.

## 7. Motores analíticos

Los motores analíticos deben empezar simples, medibles y explicables. Posibles motores:

- Momentum y trend following.
- Mean reversion.
- Breakouts y volatilidad.
- Modelos estadísticos.
- Modelos ML supervisados.
- Modelos de régimen.
- NLP para noticias, sentimiento y eventos.
- Análisis on-chain para BTC y ETH cuando existan fuentes confiables.

Cada motor debe producir señales con score, confianza, contexto de régimen, explicación y evidencia histórica.

## 8. Risk Engine independiente

El Risk Engine es una capa separada y tiene autoridad absoluta de veto. Una señal válida no implica una operación válida.

Debe controlar:

- Tamaño máximo por posición.
- Exposición máxima por activo.
- Exposición agregada.
- Drawdown máximo.
- Pérdida diaria máxima.
- Correlación entre señales.
- Condiciones de mercado anómalas.
- Calidad y frescura de datos.
- Estado operacional del sistema.
- Kill-switch manual y automático.

## 9. Data Platform

La plataforma de datos debe separar:

- `data/raw`: datos originales, sin modificaciones.
- `data/curated`: datos limpios y normalizados.
- `data/features`: datasets listos para research, backtesting o modelos.

Toda transformación debe ser reproducible, registrable y auditable.

## 10. Paper Trading y Live-Small

Paper trading es obligatorio antes de cualquier ejecución real. Debe validar:

- Estabilidad de datos.
- Calidad de señales.
- Comportamiento del Risk Engine.
- Simulación de órdenes.
- Métricas de performance.
- Alertas y monitoreo.
- Capacidad de auditoría y replay.

Live-small solo puede comenzar con exposición mínima, límites estrictos, kill-switch activo y revisión humana.

## 11. Dashboard y monitoreo

El dashboard debe mostrar:

- Estado de ingesta.
- Calidad y frescura de datos.
- Señales activas.
- Decisiones del Risk Engine.
- PnL simulado o real según modo.
- Drawdown.
- Exposición.
- Eventos relevantes.
- Alertas.
- Trazabilidad por operación o señal.

## 12. Reglas no negociables

- No ejecutar trades reales al inicio.
- No operar sin datos validados.
- No operar sin backtesting robusto.
- No operar sin paper trading estable.
- No operar sin Risk Engine activo.
- No permitir que el LLM ejecute órdenes.
- No permitir que una estrategia ignore el veto de riesgo.
- No aceptar resultados que no puedan reproducirse.
- No escalar exposición sin evidencia y aprobación.
- No ocultar errores operativos o de datos.

## 13. Próximos pasos

1. Completar y revisar el Investment Memo.
2. Definir estándares de datos para BTC y ETH.
3. Seleccionar fuentes iniciales de datos.
4. Diseñar schemas raw, curated y features.
5. Implementar Data Platform MVP.
6. Agregar controles básicos de data quality.
7. Crear research notebook base.
8. Implementar primeras estrategias baseline.
9. Construir backtesting robusto.
10. Implementar Risk Engine antes de paper trading.
