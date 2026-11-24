# Laboratorio 7 — Ensayo Actual E2 y comparación experimental de cuatro observadores

**Fecha:** 2026-11-24 03:47:28 (Paraguay); hardware PSoC 5LP + PCB Lab5, Rigol DS1202Z-E (CH1 J5, CH2 J7); escalón r=50 mV desde k=32 (64 ms); Ts=2 ms.

## Estado del Actual E2

- UART: `modo_detectado=ACTUAL`, `diseno_E2=ORIG_Z020_J010`, 256 muestras, cero flags, CPU máx 111 µs (5,55% de Ts), DAC nominal máximo 92 mV y final 46 mV.
- ADC: pico de salida y_rel = **64 mV**, sobrepasamiento respecto a la referencia de 50 mV **28%**, tiempo hasta el pico **14 ms** desde escalón; media últimas 50 muestras **47,88 mV**, error de seguimiento medio **2,12 mV (4,24%)**.
- RMS de `y_rel_mV-xhat2_mV` desde el escalón: 0,366 mV. No comparar directamente con el predictor porque Actual incorpora la corrección de la medición en el estado reportado.
- Rigol (medias de reposo entre -250 y -50 ms; meseta entre 100 y 280 ms del eje del osciloscopio):
  - CH1 J5: reposo **15,123 mV**, meseta **60,128 mV**, incremento **45,005 mV**.
  - CH2 J7: reposo **12,355 mV**, meseta **56,680 mV**, incremento **44,325 mV**, sigma de meseta ~11,59 mV.

**Advertencia de metadatos:** el lanzador registró `modo_esperado=PREDICCION` aunque el firmware ejecutó `ACTUAL`; `pulso_ch1_detectado=true`, `ensayo_valido_preliminar=false` por discrepancia de modo esperado. Conservar metadatos originales e identificar el resultado como **Actual E2 recuperable con limitación documental**. `trigger_forzado=true`, `trigger_fisico_confirmado=false`; la captura sí contiene el escalón, pero no sincronización física confirmada.

## Comparación final: 4 ensayos físicos UART

| Configuración | Pico ADC (mV) | Sobrepasamiento | Tp desde escalón | Media últimas 50 (mV) | Error medio relativo | ΔCH2 Rigol (mV) | CPU max (µs) | Flags |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Predictor E1 alternativo | 60 | 20% | 12 ms | 46,24 | 7,52% | 44,740 | 112 | 0 |
| Actual E1 alternativo | 65 | 30% | 14 ms | 43,12 | 13,76% | 44,687 | 110 | 0 |
| Predictor E2 original | 61 | 22% | 12 ms | 45,00 | 10,00% | 44,485 | 112 | 0 |
| Actual E2 original | 64 | 28% | 14 ms | 47,88 | 4,24% | 44,325 | 111 | 0 |

Todas las medias de salida UART son relativos a calibración ADC y no directamente tensiones absolutas J7. La comparación Rigol muestra incrementos finales estrechos, 44,325–44,740 mV, pese a diferencias de media ADC. No inferir precisión física superior de Actual E2 sin replicación y control de offset.

Los estimadores Actuales muestran picos de ADC mayores en ambas variantes con estos datos; resultado específico de una ejecución por caso, no una afirmación de superioridad global de predictores. No afirmar estabilidad global/robustez o tiempo de establecimiento 2% respecto a 50 mV a partir de esta sola tanda.

## Archivos reproducibles

La sesión del asistente generó un paquete local `Lab7_Comparacion_Final_Cuatro_Observadores_20261124.zip` que reúne 4× CSV UART + CSV CH1/CH2 + metadatos originales, comparación consolidada CSV/JSON, 10 figuras y script MATLAB. **No se ha subido ese ZIP al repositorio GitHub**.

Próximo paso: archivar originales, incorporar las gráficas al informe IEEE LaTeX y discutir formalmente cuantización y disparo TFOR; para futuros ensayos seleccionar `actual_E2` en el lanzador. 
