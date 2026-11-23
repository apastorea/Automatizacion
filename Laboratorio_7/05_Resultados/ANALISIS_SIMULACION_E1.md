# Comparación E1 — Predicción frente a estimador actual

**Fecha:** 2026-11-23. **Estado:** simulación nominal, no ensayo físico.

**Verificación con MATLAB:** `r(k)=p.referencia_V*(k>10)` aplica el escalón en **t=20ms** (k=11). La afirmación previa de 22ms fue un error, rectificado en este documento.

| Métrica | Predictor E1 | Actual E1 |
|---|---:|---:|
| Salida máxima [V] | 0.057646299 | 0.057631460 |
| Sobrepasamiento [%] | 15.292598 | 15.262920 |
| Tiempo al pico desde escalón [ms] | 22 | 22 |
| Establecimiento ±2% desde escalón [ms] | 46 | 48 |
| Convergencia norma de error <1e-4 [ms] | 14 | 14 |
| Control inicial [V] | 0.025574820 | 0.055896257 |
| Control máximo [V] | 0.097981136 | 0.097882034 |
| Control mínimo [V] | -0.008716071 | -0.016250966 |
| Máximo |y| previo al escalón [V] | 0.008196786 | 0.015224646 |
| Control final [V] | 0.049088908 | 0.049088909 |

El estimador actual E1 corrige con y[k] antes de controlar, lo que produce una acción inicial superior bajo error inicial de estimación. Ambos sistemas son estables, pero ninguno demuestra superioridad universal. Comparar directamente las normas iniciales es engañoso, porque el actual ya realizó su corrección en k=0.
