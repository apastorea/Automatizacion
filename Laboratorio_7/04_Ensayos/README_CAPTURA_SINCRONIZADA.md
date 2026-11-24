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

El firmware Lab7 anuncia `# LAB7 inicio; ... espera 3s` antes de iniciar el temporizador. Al detectar ese aviso, Python arma `:SING` aproximadamente **2.25 s** después, para evitar el transitorio del RESET. A los **2.85 s** comprueba si ocurrió un disparo espurio temprano y, de ser así, vuelve a armar. A los **3.15 s** (cuando el pulso de k=32 ya comenzó), si el Rigol sigue `WAIT`/`RUN`/`AUTO`, manda **`:TFOR`** como respaldo temporizado, a la manera del Lab5. Si ya indica `STOP` o `TD`, conserva el disparo físico sin forzarlo. En ABIERTO el pulso va de 64 ms a 256 ms desde el inicio de adquisición, equivalente a 3.064-3.256 s después del anuncio. Con 50 ms/div se cubren aproximadamente 600 ms alrededor del disparo.

Configura CH1/CH2 a 20 mV/div y 50 ms/div horizontal, con flanco ascendente CH1 a 35 mV. El tiempo programado de `:TFOR` se registra en `sincronizacion.instante_TFOR_s`. Para evitar forzar el disparo usar `--sin-respaldo`. Si cambia el nivel de reposo, ajustar el umbral con `--nivel-trigger` (voltios absolutos), por ejemplo `0.045`.

## Archivos generados

Dentro de Laboratorio_7/04_Ensayos/Capturas_Sincronizadas/<fecha>_<etiqueta>/:
- pantalla.png: imagen original Rigol.
- chan1.csv y chan2.csv: muestras fisicas por canal y tiempos.
- psoc_uart.txt: salida UART completa, incluidas cabeceras.
- psoc_uart.csv: 256 filas esperadas, con columnas de tiempo, ADC, DAC, estados estimados y flags.
- metadatos.json: modo solicitado/detectado, filas, errores, tiempos, estado de trigger y evaluacion preliminar.

VALIDACION PRELIMINAR: True significa que coincidió el modo, llegaron 256 filas con flags=0, `SINGLE` terminó en STOP y, en ABIERTO, se detectó en CH1 **una meseta de al menos 20 mV durante 100 ms**. El método se guarda explícitamente como `sincronizacion.disparo_forzado` y `configuracion_rigol.trigger_forzado`. Con `:TFOR` el campo `trigger_fisico_confirmado` debe ser falso, aunque se haya medido un pulso válido. No equivale a validación metrológica completa; el operador debe verificar CH1=J5, CH2=J7 y rangos físicos.

Si no hay flanco y se utiliza :TFOR, el script guarda el evento *si aparece físicamente en la ventana*. Si no hay meseta, lo marca no válido y lo conserva como diagnóstico. No declarar ganancia ni constantes de tiempo a partir de capturas que solo contienen ruido. El script no puede comprobar por sí solo el nodo al que conectaste la sonda.

Este capturador fue probado sin hardware mediante simulacion de COM4 y Rigol. Esta pendiente la primera ejecucion con el equipo real.

## Comprobaciones previas al uso

- El programa no modifica firmware. Los modos `PREDICCION` y `ACTUAL` solo se ensayan después de compilar y programar el PSoC para cada variante, manteniendo límites y protecciones.
- Cerrar MATLAB o cualquier cliente que ocupe COM4/USB VISA antes de ejecutar. Si parece detenido en «Conectando RIGOL USB VISA...», cerrar el proceso anterior con Ctrl+C y comprobar que ningún otro programa use el instrumento.
- Ejecución explícita con recurso exacto y respaldo activado:

```powershell
python -u ".\Herramientas_Comunes\Rigol_y_UART\lab7_ensayo_sincronizado.py" --resource "USB0::0x1AB1::0x0517::DS1ZE275014864::INSTR" --modo-esperado ABIERTO --label abierto_respaldo
```

- Prueba aislada sin respaldo (solo flanco real): agregar `--sin-respaldo`.

## Pruebas de regresión sin hardware

La lógica de sincronización se ejercitó con un puerto serie simulado y un Rigol simulado: escenario con flanco físico (no debe emitir TFOR) y sin flanco (debe emitir un solo TFOR a 3.15 s). El detector separó correctamente las dos trazas reales subidas por el usuario: pulso anterior de aproximadamente 45 mV y captura posterior solo con ruido. La versión con respaldo publicada requiere todavía una ejecución instrumental real.
