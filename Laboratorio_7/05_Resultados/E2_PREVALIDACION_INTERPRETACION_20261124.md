# Laboratorio 7 — Interpretación de prevalidación E2 (24-11-2026)

## Resultados de MATLAB aportados por el usuario

Se ejecutó `prevalidar_E2_para_PSoC_lab7` con la planta identificada de Lab5, Ts = 2 ms, 256 muestras, referencia 50 mV, ADC y DAC cuantizados, límites conservadores de solicitud `[-115,+107] mV` y corte abortivo de simulación.

- Radio espectral Predictor E2: **0.828798**; Estimador Actual E2: **0.825120**. Ambos cumplen estabilidad lineal local `rho < 1`, no garantizan robustez global.
- Códigos DAC máximos simulados nominales: **+7 → +107.593 mV** y **−11 → −116.165 mV** (ambos dentro de ±120 mV).
- Ruido hipotético **0 mV RMS**: cero fallos de 20 repeticiones, ambas estructuras.
- Ruido hipotético **3 mV RMS**: cero fallos de 20 repeticiones, ambas estructuras.
- Ruido hipotético **10 mV RMS**: **1 de 20** repeticiones falla para Predictor y **1 de 20** para Actual.
- En las dos estructuras, la única falla es `SATURACION_SOLICITADA`, repetición **16**, muestra **k=35** (70 ms desde t=0, unos 6 ms después del escalón de t=64 ms).
- `DAC_max_abs_mV=107.59` representa el máximo aplicado hasta la parada, **no** una superación del límite físico. La falla implica que el mando ideal solicitado queda fuera del rango conservador.
- Se usa la misma semilla `rng(700+rep)` para ambos modos en cada repetición; las fallas simultáneas no son dos realizaciones independientes de ruido.

## Criterios de interpretación

Las condiciones de fallo simuladas se relacionan con el arranque/transitorio y ruido de medida hipotético; no evidencian divergencia asintótica de la planta. El ruido de 10 mV RMS se inyecta al ADC como **escenario hipotético**, y no se debe igualar automáticamente con el ruido CH2 del osciloscopio sin analizar el filtrado y la cadena de adquisición. Frecuencias de 1/20 no estiman con precisión una probabilidad real de fallo. El modelo no reemplaza pruebas C/ISR, HAL y supervisión física.

## Comprobación adicional de núcleo portable C

Se ejecutó un ejercicio local con GCC de las operaciones del núcleo `lab7_estimadores.c` para E2: referencia inicial 50mV con estado cero genera **54.7374 mV** antes de cuantización en Predictor y Actual. Se comprobó que el núcleo contabiliza saturación en solicitudes extremas positivas y negativas, en ambos modos. **No es ejecución de firmware PSoC/ISR/HAL real**, por lo que no autoriza por sí solo la conexión de lazo cerrado.

## Preparación de firmware

Se corrigió en `Propuesta/main.c` exclusivamente el mensaje UART, dependiente de `LAB7_ESTIMADOR_VARIANTE`, para reportar `diseno_E1=ALT_Z035_J010` si variante 1 y `diseno_E2=ORIG_Z020_J010` si variante 2. Las matrices y la ley de control no cambiaron.

Siguiente paso: descargar los cambios, preservar respaldo del E1, seleccionar modo PREDICCION y variante 2 en una copia separada, compilar **sin programar**. Revisar la compilación e identificación correcta y ensayos de la ISR antes de alimentar el lazo físico.
