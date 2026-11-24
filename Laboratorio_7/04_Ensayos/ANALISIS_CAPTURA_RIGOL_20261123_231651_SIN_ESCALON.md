# Lab7 — Captura Rigol del 2026-11-23 23:16:51, sin escalón

**Evidencia:** archivos `pantalla(2).png`, `chan1(2).csv`, `chan2(2).csv`, `metadatos(2).json` compartidos en conversación. Los archivos binarios originales todavía no se han incorporado al repositorio.

## Datos comprobados

- Rigol DS1202Z-E, USB-TMC, modo `quick`, 1200 puntos por canal.
- Ventana temporal del CSV: -300,0 a +299,5 ms respecto del centro temporal, `dt=0.5ms`, 600ms totales.
- 20mV/div en ambos canales, 50ms/div base horizontal. `STOP` al tomar la captura. Trigger visible en pantalla: flanco CH1, nivel 25.2mV.
- CH1: media 14.026mV; mínimo 10.4mV; máximo 18.4mV; pico-pico 8.0mV.
- CH2: media 10.766mV; mínimo -1.6mV; máximo 27.2mV; pico-pico 28.8mV. Hay algunas perturbaciones puntuales sin meseta sostenida.
- CH1 nunca alcanzó el nivel del trigger (25.2mV), por lo que el registro guardado NO incluye el flanco ascendente esperado. No se observa pulso de 192ms ni incremento de salida de ~39mV.
- No concluir falla de ADC o DAC solamente a partir de esta captura. El PSoC sí había transmitido previamente 256 muestras con pulso de mando y respuesta, aunque corresponde a otra ejecución.

## Procedimiento de siguiente captura

1. Verificar CH1 realmente en J5, CH2 en J7; ambas masas en GND común de la PCB.
2. Rigol: CH1/CH2 20mV/div, DC, sonda 10X, 50ms/div, trigger por CH1 subida, umbral ~35mV (entre nivel de reposo ~14mV y potencial meseta ~60mV).
3. **Pulsar tecla física SINGLE** del Rigol y confirmar que aparece `WAIT`, antes de reiniciar el PSoC. No dejar Rigol detenido en STOP y después pulsar reset: no registraría el evento.
4. En MATLAB iniciar `capturar_uart_monitor_lab7`; después de `CAPTURA INICIADA`, pulsar SW3 una sola vez; el firmware espera 3s y genera pulso entre k32 (64ms) y k128 (256ms).
5. Al disparar, verificar `STOP` y **meseta amarilla visible** ~192ms, con retorno, y CH2 siguiendo. Solo entonces descargar `bundle --quick --only data`; guardar pantalla con `--only screen` si sirve al informe.
6. Si el Rigol no pasa a STOP, investigar si el nivel de trigger fue realmente cruzado en J5; si STOP ocurre antes de reiniciar PSoC, es disparo espurio o adquisición previa y debe rearmarse.

No deshabilitar protecciones F_Y o F_ADC. No afirmar que el escalón fue capturado hasta ver CH1 con la subida correspondiente.
