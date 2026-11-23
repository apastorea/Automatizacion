# Comparación predictores E1 y E2 — datos nominales corregidos

**Fecha:** 2026-11-23. **Fuente:** ecuaciones de `simular_lab7.m` y gráficos de MATLAB R2026b aportados por el estudiante. No son mediciones reales.

> CORRECCIÓN: el escalón ocurre a los 22 ms (`r(k)=0.05*(k>10)`), no a los 20 ms. Esta tabla sustituye las métricas preliminares publicadas en el análisis anterior.

| Métrica | Predictor E1 | Predictor E2 |
|---|---:|---:|
| Pico salida [V] | 0.057839601 | 0.057928867 |
| Sobrepasamiento [%] | 15.679202 | 15.857734 |
| Tiempo al pico desde escalón [ms] | 20 | 20 |
| Establecimiento ±2% desde escalón [ms] | 46 | 46 |
| Convergencia norma error <1e-4 persistente [ms] | 14 | 10 |
| Máximo |y| antes del escalón [V] | 0.008196786 | 0.005515107 |
| Máximo u [V] | 0.099280442 | 0.099844626 |
| Mínimo u [V] | -0.008716071 | -0.005589159 |
| Control inicial [V] | 0.025574820 | 0.025574820 |

Mover los polos del observador hacia el origen acelera la convergencia del error inicial de 14 a 10 ms (28.6%) sin cambiar los polos del controlador. El establecimiento de salida no cambia; el sobrepasamiento aumenta modestamente y la acción máxima se mantiene por debajo de 0.1V. Falta evaluar robustez al ruido y validar la planta física.
