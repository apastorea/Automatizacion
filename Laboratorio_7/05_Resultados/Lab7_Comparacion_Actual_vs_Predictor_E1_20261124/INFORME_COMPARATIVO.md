# Laboratorio 7 — Comparación experimental E1: Predictor vs Estimador Actual

**Fecha:** 24 de noviembre de 2026. Ambas capturas fueron tomadas sobre la misma PCB y bajo referencia de 50 mV, muestreo de 2 ms, 256 muestras. Se trabajó con el diseño alternativo E1: polos z=0.35±j0.10. Los valores son mediciones, no simulaciones.

## Integridad

| Indicador | Predictor | Actual |
|---|---:|---:|
| Modo UART | PREDICCION | ACTUAL |
| Muestras | 256 | 256 |
| Flags != 0 | 0 | 0 |
| Ts mediana | 2000 µs | 2000 µs |
| CPU máximo | 112 µs | 110 µs |
| Etiqueta esperada en metadatos | ABIERTO | ABIERTO |
| Trigger forzado (TFOR) | True | True |

**Precaución:** aunque las UART confirman los modos correctos, el capturador estaba configurado para ABIERTO y forzó el disparo Rigol. El estado 'ensayo_valido_preliminar=false' no prueba fallo de adquisición. La alineación de CH2 entre ensayos utiliza el flanco CH1 al 50%, no un reloj compartido.

## Métricas UART

| Indicador | Predictor | Actual |
|---|---:|---:|
| Pico ADC y_rel | 60 mV | 65 mV |
| Sobrepasamiento respecto 50 mV | 20.0% | 30.0% |
| t pico desde k=32 | 12.0 ms | 14.0 ms |
| Media de ultimas 50 muestras | 46.24 mV | 43.12 mV |
| Desvío estándar de ultimas 50 muestras | 2.99 mV | 0.84 mV |
| Sesgo respecto 50 mV | 3.76 mV | 6.88 mV |
| Sesgo relativo respecto 50 mV | 7.52% | 13.76% |
| RMS y_rel-xhat2 desde escalón | 3.37 mV | 1.56 mV |
| Mando DAC máximo nominal | 92 mV | 92 mV |
| Mando DAC final | 46 mV | 46 mV |

El error de salida estimada no es equivalente entre estructuras: el ACTUAL incorpora y[k] antes de informar xhat2[k], mientras que el PREDICTOR informa la estimación previa a la corrección con esa medida. La diferencia de RMS muestra dos definiciones/instantes de estimación distintos; no prueba, por sí misma, superioridad del observador actual.

## Señales Rigol (incrementos físicos respecto al reposo)

| Indicador | Predictor | Actual |
|---|---:|---:|
| Delta CH1 J5 | 45.166 mV | 45.421 mV |
| Delta CH2 J7 | 44.675 mV | 44.709 mV |

Ambos incrementos físicos CH2 son prácticamente iguales: la diferencia es **+0.033 mV**. Eso contrasta con la diferencia de medias UART (Predictor 46.24 frente Actual 43.12 mV). Hay ruido ~11–12 mV rms en CH2, diferencias de desplazamiento en ADC y cuantización de varios mV por LSB, además de diferente ventana temporal de promediado. No afirmar mejora del seguimiento físico a partir de una sola adquisición.

## Establecimiento y recomendaciones

- No se puede asignar tiempo de establecimiento estricto al 2% respecto a 50 mV: ambas salidas presentan sesgo y cuantización al final.
- Mantener la captura original de ambos experimentos sin procesar y declarar explícitamente cualquier filtro aplicado **solo para visualización**.
- Si se desea comparación física robusta, repetir 3–5 capturas por estructura con etiquetas correctas. El CMD original permite elegir 'pred_E1' y 'actual_E1' y debería producir el modo esperado correcto; evitar aceptar etiqueta 'abierto'.
- No pasar todavía a E2 físico: la robustez con planta identificada no está demostrada para todos los casos E2. Revisar estabilidad, límites y simulación con las mismas restricciones antes de cargar esa variante.

## Contenido

- Gráficas 01–04: categorías de respuesta/acción/estimación/error para el informe.
- Gráficas 05–06: comparación de UART y DAC en ambos ensayos.
- Gráficas 07–08: señales Rigol con filtro media móvil de 9 puntos (4,5 ms) y alineación aproximada por CH1.
- Comparación UART y métricas JSON; subcarpeta datos_originales con los archivos recibidos.
