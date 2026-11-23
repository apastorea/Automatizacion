# Criterio de configuración y calibración reutilizable

Este directorio conserva el estado que permitió adquirir y contrastar los
resultados del Laboratorio 4. Debe tomarse como punto de partida del próximo
laboratorio, pero la calibración se debe comprobar nuevamente cada vez que se
modifique el cableado, la alimentación o el acondicionamiento analógico.

## Estado verificado

- Osciloscopio: RIGOL DS1202Z-E, firmware 00.06.04, serie DS1ZE275014864.
- Recurso VISA: `USB0::0x1AB1::0x0517::DS1ZE275014864::0::INSTR`.
- Comunicación: USB-TMC/SCPI; VISA de 32 y 64 bits instalados.
- PSoC: PSoC 5LP, proyecto compilado con PSoC Creator 4.4 en configuración Release.
- Telemetría: COM4, 57600 bit/s, 8 bits, sin paridad y un bit de parada.
- MATLAB: R2026b; `visadevlist` detectó el osciloscopio y `serialportlist` detectó COM4.
- Muestreo del controlador: 1 ms.

## Cableado físico validado

1. Unir todas las masas de las placas, el PSoC y las sondas en el GND común.
2. Conectar J8 con J5: mando generado por el acondicionador DAC hacia la planta.
3. Conectar J10 con J6: continuidad entre las secciones físicas indicada en el esquemático.
4. Conectar J7 con J4: salida de la planta hacia el acondicionador del ADC.
5. Conectar J9 con P0[2] del PSoC para la entrada ADC.
6. Para los ensayos finales, conectar CH1 a J5 (mando/entrada de planta) y CH2 a J7
   (salida física de la planta). Las pinzas de masa van únicamente a GND.

Antes de alimentar, verificar continuidad de cada jumper y ausencia de cortocircuito
entre los rieles de alimentación y GND. Las masas BNC del RIGOL están unidas entre sí;
nunca debe colocarse una pinza de masa sobre VCC, VEE ni sobre un nodo de señal.

## Preparación del RIGOL DS1202Z-E

1. Compensar las sondas con la salida de calibración del instrumento.
2. Colocar físicamente cada sonda en 10X y seleccionar 10X en el menú del canal.
3. Usar acoplamiento DC, entrada de 1 megaohm y límite de ancho de banda de 20 MHz.
4. Seleccionar CH1 como fuente de disparo; usar flanco ascendente y ajustar el nivel
   dentro de la excursión de la señal.
5. Ajustar la escala vertical sin recortar la señal y una base de tiempo que muestre
   el transitorio completo. Para un evento único, usar SINGLE y luego guardar la captura.
6. Comprobar la conexión desde `Scripts_instrumentacion` con
   `verificar_conexion_rigol.cmd` o `python rigol_ds1202ze.py info`.
7. Guardar pantalla, formas de onda y metadatos con
   `python rigol_ds1202ze.py bundle --label nombre_del_ensayo`.

## Preparación del PSoC

1. Abrir `Lab4.cywrk` en PSoC Creator 4.4.
2. Revisar `lab4_experiment.h`: modo de ensayo, referencia, amplitud y cantidad de muestras.
3. No habilitar el control si `LAB4_CALIBRATED` no refleja una verificación física actual.
4. Generar componentes, compilar en Release, programar el PSoC y reiniciarlo con el
   circuito ya cableado.
5. Confirmar por UART un intervalo de 999 a 1001 us, ausencia de banderas y un tiempo
   de ISR ampliamente menor que 1 ms. En el ensayo final el máximo fue 96 us.
6. Mantener el mando dentro de +/-1 V. El barrido final alcanzó 0.549 V sin saturación.

## Preparación de MATLAB

1. Ejecutar `visadevlist` y comprobar el recurso VISA del RIGOL.
2. Ejecutar `serialportlist("available")` y comprobar COM4.
3. Cerrar cualquier terminal que esté ocupando COM4.
4. Usar `lab4_capturar_uart.m` para telemetría temporal y
   `lab4_capturar_margenes_experimentales.m` para el barrido de respuesta en frecuencia.
5. Conservar siempre datos crudos, datos procesados, metadatos y figuras en una carpeta
   fechada. No sustituir los archivos crudos durante el procesamiento.

## Calibración que debe repetirse

1. Con el controlador deshabilitado, medir cero y niveles positivos y negativos conocidos.
2. Comparar el mando solicitado, el mando físico en J5, la salida en J7 y la lectura ADC.
3. Ajustar offset y escala del ADC mediante regresión lineal; comprobar el residuo máximo.
4. Ajustar por separado las ganancias positiva y negativa del DAC, porque las ramas no son
   idénticas.
5. Repetir un nivel de cero al terminar para detectar deriva o inversión de polaridad.
6. Recién entonces actualizar las constantes de `lab4_config.h` y habilitar el control.

Valores finales del Laboratorio 4: offset ADC 2.353802067 V, escala ADC/planta
0.210251951 V/V, paso de DAC 0.004 V/cuenta, ganancia positiva 3.842612 y ganancia
negativa 2.640105691. Son antecedentes, no valores universales.

## Diagnóstico rápido

- Sin detección VISA: revisar cable USB, encender el instrumento y ejecutar `visadevlist`.
- COM4 ocupado: cerrar PuTTY, otra sesión de MATLAB o PSoC Creator Serial Terminal.
- Señal constante o saturada: verificar J8-J5, J10-J6, J7-J4 y J9-P0[2].
- Polaridad incorrecta: volver al modo de calibración y verificar ambas ramas del DAC.
- Diferencia entre pantalla y MATLAB: comprobar 10X en la sonda y en el canal, además de
  la escala de la forma de onda descargada.
- Medición ruidosa: acortar las masas de las sondas, limitar el ancho de banda y comprobar
  que todas las placas compartan una única referencia de GND.

