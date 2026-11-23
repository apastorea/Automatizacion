# Comparacion E1 — Prediccion frente a estado actual

**Fecha:** 2026-11-23. **Condición:** simulación con modelo nominal de la guía, no mediciones físicas. **Evidencia:** capturas del usuario de MATLAB R2026b y reproducción numérica independiente con las ecuaciones de `simular_lab7.m`.

Referencia 0.05 V a t=0.020 s; Ts=0.002 s; 2 polos del controlador 0.8±0.25j; E1 del observador 0.4±0.25j; x0=[0;0] y xh0=[0.02;-0.01].

| Métrica | Predictor | Actual |
|---|---:|---:|
| Pico salida (V) | 0.0576463 | 0.0576315 |
| Sobrepasamiento (%) | 15.2926 | 15.2629 |
| Tiempo al pico desde escalón (ms) | 22 | 22 |
| Tiempo establecimiento ±2% desde escalón (ms) | 46 | 48 |
| u[0] (V) | 0.0255748 | 0.0558963 |
| max u (V) | 0.0979811 | 0.0978820 |
| min u (V) | -0.0087161 | -0.0162510 |
| max y antes del escalón (V) | 0.0081968 | 0.0152246 |
| u estacionaria (V) | 0.0490889 | 0.0490889 |

## Interpretación

La medición actual corrige la estimación antes del cálculo de u[k], lo que causa una acción inicial mayor debido a las condiciones iniciales erróneas; el predictor corrige la predicción para k+1. Se obtienen transitorios principales prácticamente iguales; este ensayo no demuestra superioridad dinámica general del observador actual.

En la gráfica de norma del error, para `actual` se representa estimación ya corregida en k=0; en `prediccion`, la estimación usada para actuar antes de corregir. Comparar ambas curvas iniciales sin controlar el instante de corrección introduce sesgo de interpretación.

## Pendiente

Falta analizar gráficas E2, instrumentar ruido de medida y retardo, obtener CSV reales del banco, comparar con PSoC, incorporar imágenes de MATLAB al informe con trazabilidad.
