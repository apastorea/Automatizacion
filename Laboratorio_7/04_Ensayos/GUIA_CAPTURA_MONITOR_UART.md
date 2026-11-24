# Captura UART en modo monitor (primera validación en banco)

**Situación confirmada:** el usuario compiló correctamente Lab7 en PSoC Creator 4.4 y programó CY8C5888LTI-LP097 con `LAB7_MODO_MONITOR` y todas las autorizaciones en 0. Se mantiene la planta aislada del DAC para la prueba inicial.

## Procedimiento

1. Dejar la fuente Minipa con salidas deshabilitadas; J8--J5 aislado; si J9--P0[2] sigue aislado, los códigos ADC no representan la planta y pueden disparar F_ADC.
2. Mantener conectado el USB de KitProg al PC. Cerrar terminales seriales que puedan ocupar COM4.
3. En MATLAB R2026b, desde `01_Modelado_MATLAB`, ejecutar `capturar_uart_monitor_lab7`.
4. Cuando el script imprima «CAPTURA INICIADA», pulsar **SW3** (RESET/BOOT) del KitProg **una vez**; no pulsar SW1. Este botón resetea XRES del PSoC y vuelve a iniciar la adquisición. No mantener SW3 durante el enchufado del USB (entra en modo bootloader).
5. Tras la captura, revisar `04_Ensayos/Monitor_UART_YYYYMMDD_HHMMSS/uart_bruto.txt`. Si el registro contiene el encabezado `k,t_us,` y el marcador `# LAB7 END;`, se exporta `monitor_lab7.csv`.
6. Verificar `modo=MONITOR`, `Ts_nominal_us=2000`, y las banderas. Si el ADC flotante satura o no llegan muestras, no equivale a una falla del observador.
7. No activar `LAZO_ABIERTO` ni `PREDICCION`/`ACTUAL` hasta medir el mando físico, la alimentación y los valores de planta.

**Ejemplo de indicadores:** `flags=0` sin errores; `flags=1` ADC fuera de rango; `flags=16` periodo anómalo; `flags=8` sobretiempo CPU. El registro termina después de 256 muestras o de la primera bandera de error.

El script no modifica ningún registro SCPI ni configuración PSoC. Mantener los cables, sondas y GND como en el ensayo previo.
