# Laboratorio 7 — captura física del pulso de control (23:26:34, 2026-11-23)

La captura fue aportada por el usuario: `chan1(3).csv`, `chan2(3).csv` y `metadatos(3).json`. Todavía no se añadieron los archivos crudos ni la gráfica PNG a GitHub; están en la conversación y el gráfico generado está disponible localmente.

## Datos instrumentales

Rigol DS1202Z-E mediante USB-TMC; 1200 puntos por canal y un intervalo entre puntos de 0.0005s. El archivo captura los 600ms visibles, desde -300 a +299.5ms. Escalas inferidas de preámbulo: 20mV/div en ambos canales. Captura PyVISA modo quick `data`, con tiempo de ejecución reportado **0.554 s** (medición del script, sin las acciones manuales).

## Análisis preliminar de los CSV

Se filtró CH1 con mediana deslizante de 11 muestras y umbral 35mV: pulso desde aproximadamente -193.5ms a -1.0ms; anchura cercana a 192.5ms, compatible con pulso programado de 192ms.

Ventanas usadas sobre tiempo relativo del Rigol:
- Antes: -285 a -225 ms.
- Meseta: -130 a -40 ms.
- Después: +100 a +250 ms.

| Magnitud | CH1 | CH2 |
|---|---:|---:|
| Media antes [mV] | 15.5133 | 11.9600 |
| Media en meseta [mV] | 60.1022 | 56.6756 |
| Variación [mV] | 44.5889 | 44.7156 |
| Media después [mV] | 15.6598 | 12.2339 |

La relación **`Delta CH2/Delta CH1≈1.00284`** es cercana a ganancia nominal de guía `1.01856` y a antecedente Lab5 `1.00294`. Respecto al modelo nominal, la diferencia es aproximadamente -1.54%. La salida CH2 contiene ruido que no permite inferir constantes de tiempo con solo estas medias; necesita ajuste sobre respuesta transitoria.

**Condición de interpretación:** se asumió que CH1 estaba en **J5** y CH2 en **J7**, como se indicó para el ensayo. El usuario aún no confirmó expresamente ambos puntos para estos nuevos archivos. Si difieren, no interpretar 1.00284 como ganancia física de la planta.

## Acción documental

Se actualizó `capturar_rigol_datos_rapido.cmd` para ejecutar `bundle --quick --only all`, guardando PNG original del osciloscopio junto con ambos CSV y metadatos. El usuario solo necesita `git pull --ff-only origin main` y doble clic. Para más rapidez puede conservarse `--only data`, pero no guarda PNG original.
