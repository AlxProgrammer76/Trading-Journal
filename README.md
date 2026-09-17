# Trading Journal

Aplicación personal para registrar operaciones de trading y, más adelante, analizar estadísticamente el historial con el fin de identificar patrones y tendencias en el comportamiento y en los resultados.

Este repositorio se construye de forma progresiva. El lenguaje de implementación inicial es **Python**. La arquitectura debe permitir incorporar, en versiones posteriores, persistencia en base de datos, estadísticas avanzadas, dashboard, capturas de gráficos, datos de mercado, análisis estadístico, análisis mediante IA e integración con Power BI.

## Objetivo

Disponer de un registro fiable de cada operación y de un cálculo consistente de P&L, de modo que el historial pueda consultarse hoy y servir mañana como fuente de datos para análisis más profundos.

## Principios de diseño

- El MVP es deliberadamente pequeño: registrar, guardar, consultar y calcular P&L.
- El modelo de una operación se trata como un contrato estable. Nuevas capacidades se añaden alrededor de ese núcleo, no reescribiéndolo.
- Persistencia, presentación y análisis se mantendrán desacoplados para facilitar base de datos, dashboard e integraciones externas.
- La implementación de v0.1 se hará en Python, con un almacén local en JSON.

## Alcance del MVP v0.1

### Incluido

1. Registrar una operación.
2. Guardar la operación.
3. Consultar las operaciones registradas.
4. Calcular el P&L de cada operación.

### Fuera de alcance en v0.1

- Autenticación y multiusuario
- Base de datos relacional o en la nube
- Dashboard y gráficos
- Estadísticas agregadas (win rate, expectancy, drawdown, etc.)
- Capturas de gráficos
- Cotizaciones o datos de mercado en tiempo real
- Análisis mediante IA
- Integración con Power BI
- Importación/exportación masiva (CSV, broker, etc.)

## Funcionalidades iniciales

| Función | Descripción |
| --- | --- |
| Alta de operación | Captura los campos del modelo inicial y valida datos mínimos (dirección, precios, cantidad). |
| Persistencia | Guarda cada operación de forma duradera entre sesiones. En v0.1 el almacén es un archivo JSON local. |
| Listado | Muestra las operaciones registradas con sus datos principales. |
| P&L por operación | Calcula el resultado monetario a partir de entrada, salida, cantidad y dirección. |

## Modelo de datos (v0.1)

Campos de una operación:

| Campo | Descripción | Ejemplo |
| --- | --- | --- |
| Fecha y hora | Momento de la operación | 17/09/2026 09:15 |
| Activo | Instrumento operado | INTC |
| Mercado | Plaza o mercado | NYSE |
| Dirección | `Long` o `Short` | Long |
| Precio de entrada | Precio al abrir | 35.20 |
| Precio de salida | Precio al cerrar | 36.10 |
| Cantidad | Tamaño de la posición | 100 |
| Resultado | P&L calculado de la operación | 90.00 |
| Comentario | Nota libre del operador | Ruptura de resistencia |

El campo **Resultado** no se introduce a mano: se deriva del resto de datos.

## Cálculo de P&L

Convención para v0.1 (sin comisiones, slippage ni apalancamiento):

- **Long:** `(precio_salida − precio_entrada) × cantidad`
- **Short:** `(precio_entrada − precio_salida) × cantidad`

Ejemplo (Long INTC):

`(36.10 − 35.20) × 100 = 90.00`

Los importes de v0.1 pueden representarse con tipos numéricos de Python suficientes para el MVP. Más adelante, los cálculos monetarios deberán evolucionar hacia una representación adecuada (por ejemplo decimal de precisión fija) para evitar errores de redondeo propios del floating point.

Notas para versiones posteriores:

- Comisiones, fees y slippage pueden restarse del P&L bruto.
- Contratos, lotes y apalancamiento exigirán un multiplicador por activo o mercado.
- P&L en % sobre capital o sobre riesgo por operación se añadirá cuando exista un contexto de cuenta.

## Arquitectura prevista (sin implementar aún)

Capas conceptuales, para no acoplar el MVP a una tecnología concreta. La presentación y el análisis son consumidores independientes del dominio y de la persistencia; el análisis no es un paso previo a la interfaz.

```
                    [Captura / listado]
                            ↓
                    [Dominio: Operación + P&L]
                            ↓
                    [Persistencia JSON local]
                            ↓
              más adelante: base de datos

        ┌───────────────────┴───────────────────┐
        ↓                                       ↓
[Presentación]                          [Análisis]
dashboard, capturas                     estadísticas, IA,
(cuando existan)                        Power BI (cuando existan)
```

Implicaciones:

- El dominio (qué es una operación y cómo se calcula el P&L) debe ser independiente de la UI y del almacén.
- La persistencia de v0.1 es un archivo JSON local, sustituible luego por una base de datos sin cambiar el modelo.
- Estadísticas, dashboard e IA consumirán el historial; no deben mezclarse con el flujo de registro en v0.1.
- Power BI se alimentará de una exportación o de una capa de datos, no de la interfaz de registro.

## Hoja de ruta

### v0.1 — Registro y P&L (MVP)

- Formulario o captura de operación
- Guardado persistente
- Listado de operaciones
- P&L por operación según la convención anterior

### v0.2 — Consulta y calidad de datos

- Filtros por fecha, activo, mercado y dirección
- Edición y borrado
- Validaciones más estrictas
- Exportación CSV

### v0.3 — Persistencia estructurada

- Base de datos
- Identificador único por operación
- Migración desde el almacén de v0.1

### v0.4 — Estadísticas básicas

- Win rate, P&L acumulado, promedio por operación
- Desglose por activo, mercado y dirección
- Serie temporal de resultados

### v0.5 — Dashboard

- Vista resumen del rendimiento
- Gráficos de P&L y distribución de resultados

### v0.6 — Contexto de mercado y evidencia

- Capturas de gráficos asociadas a la operación
- Campos opcionales: stop, target, riesgo, setup
- Datos de mercado (histórico o cotización)

### v0.7 — Análisis avanzado e IA

- Métricas de riesgo (drawdown, expectancy, R múltiple)
- Detección de patrones de comportamiento
- Análisis asistido por IA sobre comentarios e historial

### v0.8 — Integraciones

- Conector o modelo semántico para Power BI
- Posible importación desde brokers o archivos de operaciones

Las versiones posteriores a v0.1 son orientativas. El orden puede ajustarse según necesidad, siempre preservando el modelo de operación y el cálculo de P&L como núcleo.

## Estado actual

El proyecto está en definición. **v0.1 aún no está implementada.** El siguiente paso, tras este documento, será acordar la forma de la aplicación Python (CLI u otra interfaz mínima) y construir el MVP.
