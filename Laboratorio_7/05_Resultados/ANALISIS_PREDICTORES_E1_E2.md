# Comparación predictores E1 y E2 — datos nominales corregidos

**Fecha:** 2026-11-23. **Fuente:** ecuaciones de `simular_lab7.m` y gráficos de MATLAB R2026b aportados por el estudiante. No son mediciones reales.

**Verificación directa de MATLAB:** el escalón ocurre a los **20 ms** (`k=11`, `t=(k-1)*Ts`). La afirmación intermedia de 22 ms fue incorrecta y queda anulada.

| Métrica | Predictor E1 | Predictor E2 |
|---|---:|---:|
| Pico salida [V] | 0.057646299 | 0.057807208 |
| Sobrepasamiento [%] | 15.292598 | 15.614416 |
| Tiempo al pico desde escalón [ms] | 22 | 20 |
| Establecimiento ±2% desde escalón [ms] | 46 | 46 |
| Convergencia norma error <1e-4 persistente [ms] | 14 | 10 |
| Máximo |y| antes del escalón [V] | 0.008196786 | 0.005515107 |
| Máximo u [V] | 0.097981136 | 0.099068980 |
| Mínimo u [V] | -0.008716071 | -0.005589159 |
| Control inicial [V] | 0.025574820 | 0.025574820 |

Mover los polos del observador hacia el origen acelera la convergencia del error inicial de 14 a 10 ms (28.6%) sin cambiar los polos del controlador. El establecimiento de salida no cambia; el sobrepasamiento aumenta modestamente y la acción máxima se mantiene por debajo de 0.1V. Falta evaluar robustez al ruido y validar la planta física.
