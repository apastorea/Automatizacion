# PSoC 5LP — Laboratorio 5

Abrir `Lab5.cywrk` en PSoC Creator 4.4. El proyecto conserva sin cambios el
esquema, los pines y la cadena analógica validados en el Laboratorio 4.

## Estado seguro inicial

`lab5_experiment.h` permite seleccionar:

- modo seguro `LAB5_MODE_MONITOR`, modo de calibracion acotado o control;
- calibración pendiente (`LAB5_CALIBRATED = 0`);
- controlador `LAB5_DESIGN_TS1_DEADBEAT`;
- referencia común de `0,100 V`;
- 256 muestras, con 32 muestras de pretrigger.

En MONITOR ambos DAC permanecen en cero. El preprocesador impide compilar el
modo CONTROL mientras la calibración no se marque como revalidada.

El modo `LAB5_MODE_CALIBRATION` aplica, durante 32 muestras por nivel, la
secuencia 0, +50, +100, 0, -50, -100 y 0 mV. Se utiliza exclusivamente para
medir en J5 el offset y la amplitud realmente aplicados antes de cerrar el
lazo.

## Diseños disponibles

- `LAB5_DESIGN_TS1_OSCILLATORY`: 9,540 ms, Period = 953.
- `LAB5_DESIGN_TS1_DEADBEAT`: 9,540 ms, Period = 953.
- `LAB5_DESIGN_TS2_OSCILLATORY`: 3,180 ms, Period = 317.
- `LAB5_DESIGN_TS2_DEADBEAT`: 3,180 ms, Period = 317.

El periodo se escribe por firmware; no es necesario reconfigurar manualmente
el componente Timer para cambiar de diseño.

## Arquitectura conservada

- ADC SAR simple de 12 bits, rango Vssa–Vdda y disparo por hardware.
- `Clock_1 = 100 kHz` y `Timer_TS` de 16 bits.
- dos DAC mutuamente excluyentes para el esfuerzo bipolar;
- operacionales, pines, UART y temporizador de medición del Lab4.

`ADC_SAR_Seq` no pertenece a este laboratorio y no fue agregado.

## Antes del control físico

1. Revalidar offset y escala ADC con la cadena conectada.
2. Revalidar las ganancias positiva y negativa de los DAC.
3. Confirmar que la referencia MATLAB y firmware tenga la misma amplitud.
4. Verificar el periodo y el tiempo máximo de ISR.
5. Cambiar `LAB5_CALIBRATED` a 1 y luego `LAB5_MODE` a
   `LAB5_MODE_CONTROL`.

Compilar no programa la placa.
