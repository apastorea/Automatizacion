# Laboratorio 7 — Ensayo experimental con estimador ACTUAL E1 alternativo y comparación con Predictor

**Captura:** 24/11/2026 03:00:47 (-03:00). Osciloscopio Rigol DS1202Z-E (CH1=J5, CH2=J7); firmware del PSoC 5LP identificado por UART como `modo=ACTUAL`, `diseno_E1=ALT_Z035_J010`, 256 muestras, Ts mediana 2000 µs y 0 flags.

**Fuente:** archivos reales enviados por el usuario `psoc_uart(7).csv`, `psoc_uart(7).txt`, `chan1(20261124-060118).csv`, `chan2(20261124-060118).csv`, `metadatos(20261124-060119).json`, `pantalla(10).png`. Comparación con ensayo Predictor previo `psoc_uart(6).csv`, `chan1(10).csv`, `chan2(10).csv`. **No son datos de simulación.**

## Comparación UART para referencia de 50 mV (escalón en k=32, t=64 ms)

| Magnitud | Predictor E1 | Actual E1 |
|---|---:|---:|
| Pico de salida ADC | 60 mV | 65 mV |
| Sobrepasamiento respecto a referencia (50 mV) | 20% | 30% |
| Tiempo al pico desde escalón | 12 ms | 14 ms |
| Salida media, últimos 50 puntos | 46,24 mV | 43,12 mV |
| Error de seguimiento medio, últimos 50 puntos | 3,76 mV (7,52%) | 6,88 mV (13,76%) |
| Desviación típica final, últimos 50 puntos | 2,99 mV | 0,84 mV |
| RMS `y_rel_mV-xhat2_mV` desde escalón | 3,37 mV | 1,56 mV |
| Mando DAC nominal máximo | 92 mV | 92 mV |
| Mando DAC nominal final | 46 mV | 46 mV |
| CPU máximo | 112 µs | 110 µs |
| Muestras con flags no nulas | 0 | 0 |

El RMS del error observable **no es una comparación directa de calidad**: en Actual se corrige con la medida y[k] antes de reportar la estimación, mientras que Predictor reporta estado previo a corrección con y[k] del instante. Ambos modos completaron 256 muestras sin flags y no mostraron excursiones de DAC nominal fuera de ±120 mV.

## Comparación física Rigol: incrementos entre reposo y meseta

Metodología reproducible: reposo promedio en `t<-40 ms` del eje de cada CSV Rigol, meseta promedio en `100 ms<t<290 ms` del eje de cada CSV. **Estas ventanas del Rigol no están sincronizadas a nivel sub-milisegundo con el registro UART**: captura con trigger forzado.

| Magnitud | Predictor E1 | Actual E1 |
|---|---:|---:|
| ΔCH1 J5 | +45,166 mV | +45,421 mV |
| ΔCH2 J7 | +44,675 mV | +44,709 mV |

La diferencia de amplitud física final de CH2 entre ensayos es de apenas **+0,034 mV**, mientras que sus medias UART difieren 3,12 mV. Por ruido visible en CH2 (~11–12 mV de desviación típica en meseta), cuantización de ADC (aprox. 5–6 mV por cuenta en `y_cal_mV`) y referencias de cero distintas, **no sostener superioridad de seguimiento estacionario físico de una estructura con una sola captura**. Los dos modos muestran respuesta acotada durante medio segundo.

## Advertencias instrumentales

- `modo_esperado=ABIERTO`, aunque `modo_detectado=ACTUAL`; por ello `ensayo_valido_preliminar=false`. Es error de selección de etiqueta de capturador, **no** un fallo UART.
- Disparo `TFOR=true`; `trigger_fisico_confirmado=false`. Se observa un escalón real, pero la sincronización exacta de ambos ensayos solo es aproximada. Para comparar curvas Rigol, alinear por cruce al 50% del escalón CH1, indicando el método.
- El umbral temporal del capturador (85 mV) está por encima de la meseta de CH1 (~60 mV absolutos), lo que explica por qué habitualmente no se produce disparo por flanco con esa configuración. Evitar tomar `STOP` como evidencia de trigger físico.
- No informar tiempo de establecimiento al 2% estrictamente respecto a 50 mV, ya que hay error final y cuantización.
- El ruido y filtros usados para ilustrar la salida deben declararse y las señales crudas conservarse.

## Próximos pasos

1. Conservar ambos conjuntos de datos, las 4 figuras fundamentales de cada estructura y el cuadro comparativo en el informe LaTeX.
2. Corregir la etiqueta del capturador al seleccionar `actual_E1`/ `pred_E1` y revisar umbral para flanco físico (por ejemplo 35 mV si el nivel de reposo J5 se mantiene cerca de 15 mV y el de trabajo de 60 mV, verificando contra el banco).
3. Antes de activar E2 físico, realizar primero una verificación con la planta identificada, saturación, robustez a cuantización y modelo real de discretización. Documentar las distintas definiciones del error del observador.
