# LABORATORIO 7 — Primer ensayo experimental cerrado, Predictor E1 alternativo

**Fecha de captura:** 2026-11-24 02:51:18 (-03:00).
**Equipo:** PSoC 5LP + PCB Lab5 y Rigol DS1202Z-E CH1=J5, CH2=J7. 
**Fuentes primarias:** archivos adjuntos a la conversación: `psoc_uart(6).csv`, `psoc_uart(6).txt`, `chan1(10).csv`, `chan2(10).csv`, `metadatos(10).json`, `pantalla(9).png`.

## Verificación de identificación del ensayo

- `modo_detectado=PREDICCION`, 256 muestras UART, `flags!=0` en **0** muestras; `Ts` mediana=2000 µs; `cpu_us` máximo 112 µs (**5.6%** del período).
- `modo_esperado=ABIERTO`, aunque el PSoC ejecutó `PREDICCION`. Por ello `ensayo_valido_preliminar=false`; **no** indica que la adquisición sea experimentalmente inútil.
- `trigger_forzado=true`; el instrumento llegó a STOP por TFOR. La adquisición muestra un escalón real en ambos canales, pero no se puede considerar confirmado el disparo físico ni una sincronización absoluta de precisión sub-ms.
- `diseno_E1=ALT_Z035_J010`; periodo de 2 ms; referencia de 50 mV desde `k=32` (`t=64ms`).

## Resultados desde CSV UART

| Métrica | Valor |
|---|---:|
| Máxima salida y_rel_mV | 60 mV (k=38, 12 ms después del escalón) |
| Sobrepasamiento respecto a referencia 50 mV | 20.0% |
| Media salida últimas 50 muestras (100 ms finales) | 46.24 mV |
| Desviación típica de salida últimas 50 muestras | 3.02 mV |
| Error medio de seguimiento respecto a 50 mV | 3.76 mV (7.52%) |
| RMS de y_rel-xhat2, muestras desde escalón | 3.366 mV |
| RMS de y_rel-xhat2, últimas 50 muestras | 3.265 mV |
| Máximo mando solicitado | 96 mV |
| Máximo mando nominal DAC | 92 mV |
| Mando DAC nominal últimas 50 muestras | 46.0 mV |
| Máximo código DAC+ | 6 |
| Máximo código DAC- | 0 |
| Tiempo CPU máximo | 112 µs |
| Máximo intervalo entre muestras medido | 2001 µs |
| Flags activadas | 0 |

**Nota:** el tiempo de establecimiento 2% estricto respecto a la referencia no se puede afirmar: la salida cuantizada continúa entre 43 y 49 mV con sesgo promedio 46.24 mV, a veces fuera de 49–51 mV.

## Resultados físicos Rigol (tensiones en mV)

Calculados de 1200 muestras en cada canal (muestreo visible: 0.5 ms, registro de ~600 ms). Nivel previo: `t<-40ms` del eje Rigol. Meseta: `+100ms<t<+290ms` del eje Rigol. No confundir tensión absoluta del osciloscopio con tensión relativa procesada por el PSoC.

| Métrica | CH1 J5 (control) | CH2 J7 (salida) |
|---|---:|---:|
| Media reposo | +14.750 | +11.914 |
| Media meseta | +59.916 | +56.589 |
| Incremento de señal | **+45.166** | **+44.675** |
| Desviación típica (reposo) | 3.346 | 12.046 |
| Desviación típica (meseta) | 3.35 aprox. | 11.460 |

CH1 incremento físico +45.17 mV concuerda con código DAC nominal estacionario ~46 mV. CH2 incremento +44.68 mV concuerda con la media final ADC 46.24 mV: diferencia entre mediciones ~1.57 mV (3.4% de la medida ADC), sujeta a diferencias de ventana y ruido. CH2 físico es más ruidoso que ADC; una media móvil de 9 muestras (4.5 ms) es solo para presentación, conservando la captura cruda.

## Comparación con simulación anterior E1 alternativo Predictor

En simulación previa sobre planta identificada Lab5 y cuantización, sin ruido adicional, se informó `salida_max_mV=61.557`, `salida_cola_mV=46.247`. En este ensayo se registró `max=60` y `media_final=46.24`. Los resultados concuerdan favorablemente. La coincidencia de la meseta no demuestra un modelo perfecto; depende también de niveles de cuantización compartidos. Revisar que las simulaciones originales de antes de recortar el código DAC pueden tener discrepancias en escenarios saturados.

## Interpretación y limitaciones

- Control de estados estimados operando físicamente en el rango de 510 ms y sin flags, con pico y salida acotados; no constituye prueba formal de estabilidad global ni de robustez.
- La traza `xhat2` es la estimación de salida del predictor; la diferencia observada `y_rel-xhat2` no es todo el error de estados `||x-xhat||`, ya que no se mide el estado completo.
- Capturador esperado ABIERTO versus detectado PREDICCION: la discrepancia de etiqueta provocó `ensayo_valido_preliminar=false`. Para próximas capturas, elegir `pred_E1` en el CMD. No repetir innecesariamente esta captura; conservarla con estas advertencias.
- No estimar t_s al 2% estricto sin acordar criterio de ruido y banda; la dispersión ADC de un LSB afecta el resultado.
- Los archivos brutos originales deben conservarse junto con imágenes de Rigol y resultados calculados; el análisis se realizó a partir de los anexos enviados por usuario y debe ser reproducible en MATLAB desde esos mismos CSV.
