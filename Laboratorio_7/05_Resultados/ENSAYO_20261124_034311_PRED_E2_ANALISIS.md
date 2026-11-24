# Laboratorio 7 — Predictor E2 original, captura física válida

**Fecha local:** 2026-11-24 03:43:11 (-03:00), PSoC 5LP + PCB usada en Lab5, Rigol DS1202Z-E (CH1 J5, CH2 J7).

## Integridad de la adquisición

- UART declara `modo=PREDICCION`, `diseno_E2=ORIG_Z020_J010` y `limite_DAC_codigo=SI`.
- Muestras: **256**, tiempo final **509,999 ms**, período mediano de muestreo **2000 µs**, máximo `cpu_us=112` (**5,6%** de Ts). Cero muestras con bandera distinta de cero.
- Capturador: `modo_esperado=PREDICCION`, `pulso_ch1_detectado=true`, `ensayo_valido_preliminar=true`.
- `trigger_forzado=true`, `trigger_fisico_confirmado=false`: la captura contiene el escalón, pero el disparo fue **TFOR** y no prueba alineación temporal absoluta rigurosa.

## Datos UART del Predictor E2

| Métrica | Resultado |
|---|---:|
| Escalón | r = 50 mV, k=32 (64 ms) |
| Máxima salida relativa y[k] | 61 mV |
| Sobrepasamiento respecto a 50 mV | 22 % |
| Tiempo al pico desde escalón | 12 ms |
| Salida media últimas 50 muestras | 45.00 mV |
| Error medio respecto a referencia | 5 mV, 10 % |
| Mando DAC nominal máximo | 92 mV |
| Mando DAC nominal final | 46 mV |
| RMS de y_rel - xhat2 desde el escalón | 1.473 mV |

No debe equipararse RMS de `y_rel - xhat2` con error completo de estados.

## Datos Rigol desde los CSV de ambos canales

Las ventanas estadísticas se tomaron en tiempo del **osciloscopio**, no del PSoC: reposo [-250,-50] ms y meseta [+100,+280] ms.

| Magnitud | CH1 J5 (mando) | CH2 J7 (salida) |
|---|---:|---:|
| Media en reposo | 14.975 mV | 12.362 mV |
| Media en meseta | 59.934 mV | 56.851 mV |
| Incremento físico | **44.959 mV** | **44.489 mV** |
| Desvío estándar aproximado en meseta | 3.45 mV | 11.50 mV |

Las amplitudes físicas son coherentes con el DAC nominal final (46 mV) y la media final UART de 45 mV, sujeto a calibración, cuantización y ruido.

## Comparación preliminar (UART, tres ensayos físicos)

| Magnitud | Predictor E1 alternativo | Actual E1 alternativo | Predictor E2 original |
|---|---:|---:|---:|
| Máxima salida relativa ADC | 60 mV | 65 mV | 61 mV |
| Salida media final (últimas 50) | 46.24 mV | 43.12 mV | 45.00 mV |
| DAC nominal máximo | 92 mV | 92 mV | 92 mV |
| Banderas diferentes de cero | 0 | 0 | 0 |

La comparación ADC no implica superioridad física definitiva; comprobar diferencias de offset/ruido y faltará la cuarta estructura Actual E2.

## Riesgos y límites de interpretación

- Esta es la repetición realizada después del intento de 03:39 sin pulso físico en el osciloscopio. El CSV original de 03:43 sí registra el escalón.
- CH2 tiene ruido considerable, con `σ` ≈11.5 mV en meseta, de modo que los extremos instantáneos no ofrecen sobrepasamiento físico fiable sin un criterio de filtrado definido.
- No afirmar tiempo de establecimiento del 2% respecto a la referencia con una media final de 45 mV frente a 50 mV.
- La ausencia de errores en una captura no es garantía general de estabilidad ni sustituye ensayos de robustez.

## Próximo ensayo

Resguardar configuración de Predictor E2 y datos originales; cambiar `LAB7_MODO` a `LAB7_MODO_ACTUAL` manteniendo `LAB7_ESTIMADOR_VARIANTE (2u)`; compilar, supervisar banco y utilizar capturador E2 temporizado seleccionando `actual_E2`. No variar alimentación, escalón, ADC, DAC o conexiones.
