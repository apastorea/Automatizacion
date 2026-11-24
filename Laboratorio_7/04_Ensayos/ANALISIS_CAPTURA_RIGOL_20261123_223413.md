# Lab7 — Análisis de la primera captura USB del Rigol DS1202Z-E

**Origen:** archivos `pantalla.png`, `chan1.csv`, `chan2.csv` y `metadatos.json` aportados en conversación; originales aún no incorporados a este repositorio. Fecha del archivo metadata: `2026-11-23T22:34:13-03:00`.

## Adquisición comprobada

- Rigol DS1202Z-E, serie DS1ZE275014864, firmware 00.06.04; USB-VISA/SCPI.
- Rigol en STOP al descargar; 1200 puntos por canal, 0.0001 s por punto, de -0.0600 a +0.0599 s respecto al disparo.
- CH1 en DC, 10X, 1 V/div; CH2 en DC, 10X, 20 mV/div; límite de ancho de banda 20 MHz.
- NOTA: el valor global `VAVG` del instrumento para CH1 (1.173512 V) mezcla el tramo anterior y posterior a la transición, por lo que NO representa la meseta de entrada.

## Promedios calculados a partir de CSV

Ventana antes de la transición: [-50,-10] ms. Ventana posterior: [+30,+55] ms. El salto de CH1 se produce alrededor de t=0 (disparo).

| Parámetro | CH1 | CH2 |
|---|---:|---:|
| Promedio previo | -0.0310 V | +0.016652 V |
| Promedio posterior | +2.37992 V | +0.011500 V |
| Cambio posterior - previo | +2.41092 V | -0.005152 V |
| Vmax | +2.60 V | +0.0216 V |
| Vmin | -0.040 V | +0.0072 V |

**No etiquetar esta captura como respuesta al escalón de 50 mV de Lab7.** Un salto de 2.41 V en CH1 no coincide con la excitación nominal que debía estar en J5, y CH2 solo cambia -5.15 mV. El registro UART mostrado anteriormente tenía `k=0`, `flags=32`, `u_solicitada=0`, DAC=0, lo que muestra que el firmware abortó ANTES de k=32 (momento programado del escalón). Por tanto no se dispone todavía de un ensayo abierto válido para identificar la planta.

**Confirmación posterior del usuario:** CH1 estaba conectado en **J9** durante esta captura (CH2 en J7). Por tanto, el nivel final de J9 próximo a 2.38 V representa la polarización del acondicionador ADC y **NO** un mando de 2.41 V aplicado a la planta. Queda descartada la interpretación de un escalón excesivo en J5 a partir de esta imagen.

**Discrepancia pendiente:** el registro UART anterior entregó `adc_mV=594` (522 cuentas) y se detuvo en `k=0` con `flags=32`, mientras que el Rigol midió J9 próximo a 2.38 V **en otra ventana temporal**. Estos datos no están sincronizados y no permiten afirmar todavía si la causa es falta de continuidad J9→P0[2], lectura ADC antes de fin de conversión, o variación del acondicionador durante el arranque. El HAL Lab7 heredado (`lab5_hardware.c`) llama `ADC_GetResult16()` sin comprobar previamente el fin de conversión; investigar sincronización SOC/EOC si persiste la discrepancia con J9–P0[2] unido.

El metadato SCPI incluye `-410,"Query INTERRUPTED"` tras exportar, pero el archivo de pantalla y los dos CSV existen y contienen 1200 puntos cada uno. Es una incidencia de consulta de metadatos, no evidencia de pérdida de esas formas de onda.

## Próxima acción mínima

1. Confirmar ubicación física de CH1 (J9 o J5).
2. Con firmware detenido/seguro, si CH1 está en J9, comparar en la **misma condición temporal** J9≈2.38V con `adc_mV` por UART; el registro previo `adc_mV=594` podría corresponder a otro instante (arranque del acondicionador).
3. No anular la bandera `F_Y` ni forzar cerrado. Cuando exista una secuencia válida de 256 muestras con flags=0 en ensayo abierto, repetir CH1=J5, CH2=J7 y obtener incremento de mando y de salida.
4. Guardar datos crudos en un directorio fechado y evaluar `Delta_y / Delta_u` solo entonces.
