# Laboratorio 7 — Comparación de las cuatro simulaciones nominales

**Fecha:** 2026-11-23.
**Procedencia:** simulaciones del estudiante en MATLAB R2026b (cuatro gráficos), con reproducción numérica independiente de las ecuaciones implementadas en `simular_lab7.m`. Estas cifras NO son mediciones de PSoC.

## Errata de tiempo y métricas

El código contiene `r(k) = p.referencia_V*(k>10)`. Como k empieza en 1 y `t=(0:N-1)*Ts`, el primer valor positivo de la referencia ocurre en el índice 12, **t=0.022 s (22 ms)**. Los análisis previos referían erróneamente 20 ms y reportaban sobrepasamientos y máximos ligeramente distintos. Esta tabla **sustituye** las cifras preliminares anteriores.

Parámetros: Ts=2ms; referencia=50mV; controlador K=[2.15692217,6.87132640], Nr=1.09474803; x0=[0,0]; xh0=[0.02,-0.01]; límites u=±1V provisionales; sin ruido ni cuantización.

| Métrica | Pred E1 | Actual E1 | Pred E2 | Actual E2 |
|---|---:|---:|---:|---:|
| Pico y [mV] | 57.839601 | 57.897046 | 57.928867 | 57.928225 |
| Mp [%] | 15.679202 | 15.794093 | 15.857734 | 15.856449 |
| tp desde escalón [ms] | 20 | 22 | 20 | 20 |
| ts ±2% desde escalón [ms] | 46 | 48 | 46 | 46 |
| Norma error <1e-4 persistente desde [ms] | 14 | 14 | 10 | 8 |
| Norma error mostrada en t=0 [V] | 0.02236068 | 0.01077809 | 0.02236068 | 0.00503512 |
| Máximo |y| antes del escalón [mV] | 8.196786 | 15.224646 | 5.515107 | 5.377430 |
| u[0] [mV] | 25.574820 | 55.896257 | 25.574820 | 24.695498 |
| Máx u [mV] | 99.280442 | 99.572570 | 99.844626 | 99.840336 |
| Mín u [mV] | -8.716071 | -16.250966 | -5.589159 | -5.456101 |
| u final [mV] | 49.088908 | 49.088909 | 49.088908 | 49.088908 |
| Muestras saturadas | 0 | 0 | 0 | 0 |

**Definiciones:** sobrepasamiento (max y-50mV)/50mV*100; tp desde primera muestra con referencia positiva; ts al ±2% como primera muestra tras la última salida fuera de tolerancia; error norm <1e-4 y permanente desde ese instante.

## Qué enseña Actual E2

Frente a Actual E1, Actual E2 reduce el tiempo de convergencia del error desde 14 a 8 ms (42.9%) y el máximo de desviación previo a la referencia desde 15.225 a 5.377 mV (64.7%). El sobrepasamiento pasa de 15.794% a 15.856% y ts2 de 48 a 46 ms; el máximo de mando es similar (~99.8 mV).

El error inicial en el gráfico del observador **actual** se calcula DESPUÉS de la corrección y[0], mientras que el predictor muestra la predicción anterior a corregir. Los valores iniciales de la norma no se comparan ingenuamente entre arquitecturas.

## Archivo fuente para repetir el cálculo

Ejecutar en MATLAB `analizar_metricas_lab7`. Exporta `05_Resultados/metricas_nominales_lab7.csv`. El algoritmo comprueba el momento REAL del escalón a partir de `s.r_V`, de modo que un cambio futuro de la referencia actualiza métricas sin reescribir cifras.

## Pendiente de validación

Ruido del ADC y efecto de polos rápidos; diferencias entre modelo nominal y planta real; tiempo de procesamiento PSoC; calibración de canal; error experimental; gráficos PNG todavía no incorporados a GitHub.
