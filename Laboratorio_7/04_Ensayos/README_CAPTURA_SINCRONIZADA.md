# Lab7: captura sincronizada PSoC 5LP + Rigol DS1202Z-E

Este script reutiliza la logica de lab4_ensayo_sincronizado.py y lab5_captura_monitor_rigol.m, adaptada al protocolo UART real de Lab7. No programa el PSoC, no cambia el firmware y no desactiva protecciones.

## Preparacion

1. PSoC programado con modo ABIERTO para el primer ensayo. Preparar la alimentacion analogica y el cableado de planta como en el ensayo anterior con 256 muestras y flags=0.
2. CH1 del Rigol en J5, CH2 en J7 y ambas masas en el GND comun de PCB. Sondas fisicas 10X.
3. Conectar USB-TMC Rigol y KitProg/PSoC a la PC; cerrar MATLAB, terminales o programas que tengan abierto COM4. Python debe tener pyserial, pyvisa y numpy. Si falta algun modulo, instalarlo en el entorno correspondiente: python -m pip install pyserial pyvisa numpy.
4. Desde la raiz de git, ejecutar git pull --ff-only origin main.
5. Abrir Laboratorio_7/04_Ensayos/capturar_lab7_sincronizado.cmd mediante doble clic. Responder la etiqueta del ensayo, o usar la predeterminada 'abierto'.
6. Esperar el mensaje LISTO y pulsar SW3 una vez. No es necesario tocar SINGLE: el script lo hace automaticamente despues de detectar el arranque del PSoC.

## Comando alternativo desde PowerShell

    python -u ".\Herramientas_Comunes\Rigol_y_UART\lab7_ensayo_sincronizado.py" --modo-esperado ABIERTO --label abierto

Para observadores, tras compilar/programar por separado el firmware correspondiente, usar respectivamente:
- --modo-esperado PREDICCION --label pred_E1
- --modo-esperado PREDICCION --label pred_E2
- --modo-esperado ACTUAL --label actual_E1
- --modo-esperado ACTUAL --label actual_E2

El archivo CMD convierte estas etiquetas al modo esperado, pero no elige la variante de firmware: esa seleccion sigue haciendose en lab7_config.h, con compilacion y programacion explicitas.

## Sincronizacion exacta

El archivo Lab7.cydsn/main.c de la plantilla de Lab7 emite '# LAB7 inicio; ... espera 3s' ANTES del inicio del Timer_TS. Al detectar ese aviso, Python espera 0.5 s, envia :SING al Rigol y espera el pulso. El firmware inicia adquisicion 3 s despues del aviso; el pulso abierto comienza en k=32 (64 ms despues del inicio de muestreo) y finaliza en k=128 (256 ms). El script no usa :TFOR; solo trata STOP despues de SINGLE como posible captura fisica.

Configura CH1/CH2 a 20 mV/div, 50 ms/div horizontal, trigger CH1 ascendente a 35 mV. Si cambia el nivel de reposo, ajustar --nivel-trigger con voltios absolutos, por ejemplo 0.040.

## Archivos generados

Dentro de Laboratorio_7/04_Ensayos/Capturas_Sincronizadas/<fecha>_<etiqueta>/:
- pantalla.png: imagen original Rigol.
- chan1.csv y chan2.csv: muestras fisicas por canal y tiempos.
- psoc_uart.txt: salida UART completa, incluidas cabeceras.
- psoc_uart.csv: 256 filas esperadas, con columnas de tiempo, ADC, DAC, estados estimados y flags.
- metadatos.json: modo solicitado/detectado, filas, errores, tiempos, estado de trigger y evaluacion preliminar.

VALIDACION PRELIMINAR: True significa que coincidio el modo, se recibieron 256 filas con flags=0, SINGLE llego a STOP y, en ABIERTO, se detecto una excursion visible en CH1. No implica validacion metrologica completa.

Si no hay flanco, el script guarda lo disponible como diagnostico y lo marca no valido. No mezclar capturas sin flanco con resultados experimentales de la planta.

Este capturador fue probado sin hardware mediante simulacion de COM4 y Rigol. Esta pendiente la primera ejecucion con el equipo real.
