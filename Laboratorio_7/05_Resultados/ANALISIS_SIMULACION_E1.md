# Comparación E1 — Predicción frente a estimador actual

**Fecha:** 2026-11-23. **Estado:** simulación nominal, no ensayo físico.

> CORRECCIÓN: en `simular_lab7.m`, `r(k)=p.referencia_V*(k>10)`, por lo que la referencia aparece en **t=22ms**, no 20ms. Las cifras de este archivo están recalculadas con esa temporización. Ver también `COMPARATIVA_CUATRO_CASOS.md`.

| Métrica | Predictor E1 | Actual E1 |
|---|---:|---:|
| Salida máxima [V] | 0.057839601 | 0.057897046 |
| Sobrepasamiento [%] | 15.679202 | 15.794093 |
| Tiempo al pico desde escalón [ms] | 20 | 22 |
| Establecimiento ±2% desde escalón [ms] | 46 | 48 |
| Convergencia norma de error <1e-4 [ms] | 14 | 14 |
| Control inicial [V] | 0.025574820 | 0.055896257 |
| Control máximo [V] | 0.099280442 | 0.099572570 |
| Control mínimo [V] | -0.008716071 | -0.016250966 |
| Máximo |y| previo al escalón [V] | 0.008196786 | 0.015224646 |
| Control final [V] | 0.049088908 | 0.049088909 |

El estimador actual E1 corrige con y[k] antes de controlar, lo que produce una acción inicial superior bajo error inicial de estimación. Ambos sistemas son estables, pero ninguno demuestra superioridad universal. Comparar directamente las normas iniciales es engañoso, porque el actual ya realizó su corrección en k=0.
