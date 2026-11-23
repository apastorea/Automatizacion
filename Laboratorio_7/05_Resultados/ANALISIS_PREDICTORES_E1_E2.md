# Comparación entre predictores E1 y E2

**Fuente de datos:** gráfica de MATLAB R2026b aportada por el usuario para E2, gráfica E1 previamente aportada, y reproducción numérica independiente del algoritmo de `simular_lab7.m`. Todos los valores son **simulaciones nominales**, no datos medidos físicamente.

- Controlador común: K=[2.15692217, 6.87132640], Nr=1.09474803.
- Ts = 0.002 s; referencia 0.05 V desde 0.020 s; x0=[0,0], xhat0=[0.02,-0.01].
- E1 polos: 0.4±0.25j, modulo 0.47170.
- E2 polos: 0.2±0.10j, modulo 0.22361.

| Métrica | E1 | E2 |
|:--|--:|--:|
| Máximo salida [V] | 0.05764630 | 0.05780721 |
| Sobrepasamiento [%] | 15.29260 | 15.61442 |
| Pico desde escalón [ms] | 22 | 20 |
| Establecimiento en ±2 % desde escalón [ms] | 46 | 46 |
| Norma error <1e-4 persistente desde [ms] | 14 | 10 |
| Máximo salida antes del escalón [V] | 0.00819679 | 0.00551511 |
| Máximo control [V] | 0.09798114 | 0.09906898 |
| Mínimo control [V] | -0.00871607 | -0.00558916 |
| Control inicial [V] | 0.02557482 | 0.02557482 |

## Lectura técnica

La posición más cercana al origen acelera la convergencia del error estimado (reducción de 14 a 10 ms, criterio de permanencia <1e-4). El transitorio debido al error inicial también disminuye. No obstante, la respuesta principal mantiene 46 ms de establecimiento y el sobrepasamiento sube levemente, como es esperable con polos de controlador invariables. El máximo del mando aumenta en ~1.1 %. No hay ruido de ADC en esta simulación; la sensibilidad al ruido requiere otra evaluación.

## Próximo paso

Contrastar `lab7_actual_E2.png`; después producir una tabla consolidada con los cuatro diseños y elaborar prueba controlada de perturbaciones/ruido antes de seleccionar implementación física.
