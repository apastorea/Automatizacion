# Bitácora — decisiones de proyecto

## 2026-11-23 — Inicialización

- La práctica se denomina **Laboratorio 7**; la guía oficial incluida conserva el encabezado erróneo Lab6.
- Se dispone del Rigol **DS1202Z-E**.
- Los antecedentes de Lab5 se preservan de forma seleccionada, con SHA-256 para cada archivo recuperado.
- No se traslada automáticamente el modelo ni las calibraciones Lab5 a Lab7.
- Se crea un informe LaTeX IEEE de dos columnas con resultados pendientes, sin introducir datos simulados como medidos.
- Los informes de compañeros se consultaron como ejemplos de presentación, pero no se publican en el repositorio.
- Se mantiene opción de repositorio GitHub privado debido a datos históricos del laboratorio.

## Próximas decisiones a registrar

- Identificación del circuito real, ecuaciones F,G,H,J y referencia de unidades.
- Justificación exacta del nuevo Ts y registro del Timer.
- Polos de control y dos juegos de polos de estimador.
- Arquitectura final de ISR, ADC y DAC.
- Criterios de saturación / reset y validación física.

## 2026-11-23 — Primera etapa: modelado nominal y comprobacion

- Fig. 1, pagina 2 de la guia oficial: planta central R6=47k, R5=150k, C1=100nF; R2=47k, R1=15k, C3=100nF. El esquema coincide nominalmente con el de Lab5, aunque NO sustituye la verificacion fisica.
- Estados x1=salida primera etapa inversora, x2=segunda; salida y=x2 exclusivamente, C=[0 1].
- F=[-66.6667 0;-212.7660 -666.6667]; G=[-212.7660;0]; ganancia continua 1.0185604.
- Ts preliminar 2 ms, fs=500 Hz, fs/fBW=47.70. Timer de 100 kHz/200 cuentas: antecedente, comprobar con Rigol.
- Se calculan A,B,K,Nr y ganancias de predictor/estimador actual para E1 y E2. No son calibraciones ni mediciones.
- El modelo identificado Lab5 (tau=9.06915 ms y 0.774399 ms) no se confunde con el nominal (15 ms y 1.5 ms).
- Se permitio simulacion nominal sin declarar p.validado=true. Faltan ensayos y autorizacion de hardware.

## 2026-11-23 — Simulaciones nominales E1 verificadas (MÉTRICAS PRELIMINARES, CORREGIDAS ABAJO) por el usuario en MATLAB R2026b

- Captura del usuario: `validar_nominal_lab7` terminó correctamente (solo advertencia intencional de modelo nominal); `lab7_principal` confirmó cuatro conjuntos simulados y generó PNG/CSV en su PC.
- Gráficas recibidas y analizadas: `lab7_prediccion_E1.png` y `lab7_actual_E1.png`; no se han incorporado los archivos de imagen al repositorio.
- Reconstrucción numérica independiente del script: predictor E1 Mp=15.293%, ts2=46ms; actual E1 Mp=15.263%, ts2=48ms (ambos medidos desde escalón en t=20ms); picos en t=42ms.
- u[0] predictor=25.57mV y actual=55.90mV; máximos positivos 97.98mV y 97.88mV; mínimos -8.72mV y -16.25mV, respectivamente.
- Desviación de salida previa al escalón: máximos 8.20mV predictor y 15.22mV actual, originados en error inicial de estimación.
- Nota: la norma de error del actual en k=0 ya incluye la corrección con y[0]; no comparar directamente la primera muestra con el predictor.
- Pendiente: análisis de E2 y exportación de métricas directamente desde MATLAB; validación física en PSoC y Rigol.

## 2026-11-23 — Comparación predictores E1 y E2 (MÉTRICAS PRELIMINARES, CORREGIDAS ABAJO)

- Recibida y analizada imagen `lab7_prediccion_E2.png` del usuario. Aún no se incorporó el PNG al repositorio.
- Comparación numérica reproduciendo `simular_lab7.m` con Ts=2 ms, r=50 mV a 20 ms, y las mismas condiciones iniciales.
- E1 → E2: modulo polos 0.472 → 0.224; error norm <1e-4 persistente desde 14 ms → 10 ms (mejora 4 ms = 28.6 %).
- Sobrepasamiento 15.293 % → 15.614 %; max salida 57.646 mV → 57.807 mV; ts±2 % ambos 46 ms; t_p desde escalon 22 → 20 ms.
- Max salida antes del escalon 8.197 mV → 5.515 mV; max mando 97.981 mV → 99.069 mV; mando inicial en ambos 25.575 mV.
- La rapidez del observador reduce el transitorio por error inicial, pero no cambia los polos de control; no afirmar mejor seguimiento universal.
- Falta revisar grafica `lab7_actual_E2.png`, y medir efecto de ruido y hardware.

## 2026-11-23 — Cierre nominal de los cuatro casos y errata metodologica (OBSOLETO: CORREGIDO MAS ABAJO)

- Recibida grafica `lab7_actual_E2.png` y completada la inspeccion de las cuatro capturas de MATLAB.
- Se detecto que `r(k)=0.05*(k>10)` aplica el escalon en **t=22ms** y no t=20ms. Se recalcularon todas las métricas utilizando esa temporizacion y la implementacion de `simular_lab7.m`; cifras preliminares anteriores sustituidas.
- P-E1: Mp 15.679202%, ts2 46ms, max y 57.839601mV, max u 99.280442mV.
- A-E1: Mp 15.794093%, ts2 48ms, max y 57.897046mV, max u 99.572570mV.
- P-E2: Mp 15.857734%, ts2 46ms, max y 57.928867mV, max u 99.844626mV.
- A-E2: Mp 15.856449%, ts2 46ms, max y 57.928225mV, max u 99.840336mV.
- La norma del error converge <1e-4 persistentemente a 14,14,10,8ms respectivamente desde t=0. Las normas de estimador actual contienen la correccion con y[k] dentro de la muestra.
- Se incorpora `01_Modelado_MATLAB/analizar_metricas_lab7.m` para obtener las metricas y CSV directamente en MATLAB del usuario.
- **Sigue pendiente** validacion fisica ADC/DAC, planta, timer y respuesta ante ruido/perturbaciones; coeficientes NO aprobados para hardware.

## 2026-11-23 — Rectificación verificada con MATLAB (VERSIÓN VIGENTE)

- El usuario ejecutó el script `analizar_metricas_lab7.m` en MATLAB R2026b y compartió la tabla y el CSV generado.
- **Escalón correcto: 20 ms.** La expresión `r(k)=0.05*(k>10)` se activa en k=11, y `t=(k-1)Ts=10*2ms=20ms`. La entrada anterior que afirmó 22ms es errónea; sus valores se anulan.
- Predictor E1: pico 57.646299mV, Mp 15.292598%, tp 22ms, ts2 46ms, max mando 97.981136mV.
- Actual E1: pico 57.631460mV, Mp 15.262920%, tp 22ms, ts2 48ms, max mando 97.882034mV.
- Predictor E2: pico 57.807208mV, Mp 15.614416%, tp 20ms, ts2 46ms, max mando 99.068980mV.
- Actual E2: pico 57.809070mV, Mp 15.618140%, tp 20ms, ts2 46ms, max mando 99.080638mV.
- Convergencia error <1e-4 persistente: P-E1 14ms, A-E1 14ms, P-E2 10ms, A-E2 8ms.
- Todas las cifras son simulaciones nominales, todavía no resultados físicos; no programar el PSoC con estos parámetros sin validación.

## 2026-11-24 — Identificación del Rigol por SCPI (comprobación de banco)

- Inspección física inicial de la PCB del Laboratorio 5 reutilizada en Lab7: el usuario informa que la completó. Continuidad/aislamiento y tensiones no se consignaron numéricamente.
- MATLAB R2026b detectó `USB0::0x1AB1::0x0517::DS1ZE275014864::0::INSTR` mediante `visadevlist`, junto a `ASRL4::INSTR` (COM4).
- Ejecutó `writeread(rigol,"*IDN?")` y el Rigol respondió `RIGOL TECHNOLOGIES,DS1202Z-E,DS1ZE275014864,00.06.04` sin error; después ejecutó `clear rigol`.
- Comunicación USB-TMC / VISA / SCPI confirmada con el mismo número de serie y firmware que la configuración de Lab5. Todavía NO se han realizado mediciones de tensión/corriente de la PCB.
- Atención: el archivo histórico `Laboratorio_5/PSoC_5LP/Lab5.cydsn/lab5_experiment.h` define `LAB5_MODE=LAB5_MODE_CONTROL`; no supone el firmware cargado físicamente, ni habilita a energizar sin verificar su modo real.
- Próximo paso: comprobar fuentes de alimentación con la placa desenergizada, confirmar ausencia de control activo y luego medir en reposo con instrumentación.

## 2026-11-23 — Primera compilación y programación física del firmware Lab7 (confirmadas por capturas)

- Usuario mostró `LAB7_MODO_MONITOR`, `LAB7_AUTORIZAR_ESCALON=0`, `LAB7_PLANTA_VERIFICADA=0`, `LAB7_ADC_DAC_REVALIDADOS=0` y `LAB7_AUTORIZAR_LAZO_CERRADO=0` en PSoC Creator.
- `Build Succeeded`: Flash 9136/262144 bytes (3.5%), SRAM 14905/65536 bytes (22.7%).
- Dispositivo `PSoC 5LP CY8C5888LTI-LP097` programado y verificado correctamente, reportado a las 21:55:43 (hora en captura).
- Se añadió script `capturar_uart_monitor_lab7.m` para captura de COM4 a 57600, sin activar hardware ni lazo cerrado.
- Siguiente verificación pendiente: captura de UART con encabezado MONITOR y medición posterior del periodo real; el éxito de Flash NO prueba el comportamiento analógico ni la adquisición.

## 2026-11-23 — Primera captura UART real en MONITOR: parada segura tras una muestra

- Captura MATLAB `capturar_uart_monitor_lab7.m` realizada por el estudiante, guardada localmente en `04_Ensayos/Monitor_UART_20261123_220453/` (evidencia aún no publicada).
- Cabecera `modo=MONITOR`, `Ts_nominal_us=2000`, calibración histórica SI, modelo nominal NO_VALIDADO; puerto COM4 a 57600 8N1.
- Registro `k=0`: ADC 522 cuentas; `adc_mV=594`, `y_cal_mV=-8371`, `y_rel_mV=-8371`, `r=0`, `u_solicitada=0`, `u_nominal=0`, `dac_pos=0`, `dac_neg=0`, `cpu_us=45`, `intervalo_us=0`, `flags=32`.
- Código `Lab7.cydsn/main.c`: `F_Y=32` se enciende cuando `salida_rel_V` supera en módulo `LAB7_Y_FALLO_V=0.500 V`; cualquier bandera activa `detener_seguro()`, por lo que se conserva una sola muestra y se emite `# LAB7 END; DAC=0`.
- La tensión -8.371 V es `(0.594-2.353802067)/0.210251951`, valor **calculado por calibración heredada**, no tensión medida con Rigol sobre la salida de planta.
- Si J9 está desconectado, o si el acondicionador no está energizado, la señal ADC carece de validez física; no diagnosticar falla PSoC con esta lectura.
- El ciclo de 45 us de una ISR y `intervalo_us=0` para k=0 NO validan periodicidad de 2 ms.
- Próximo ensayo: verificar alimentaciones y rango de tensión en J9 con multímetro, restituir J9-P0[2] con fuentes apagadas, y repetir MONITOR manteniendo J8-J5 aislado.

## 2026-11-23 — Transición a mediciones propias de Lab7

- El usuario solicitó evitar repetir pruebas extensas de Lab5 y pasar a las mediciones directamente relacionadas con la guía.
- Se definió el ensayo único de coherencia en lazo abierto de 50 mV (J5 y J7 físicos, 2ms), seguido de cuatro ensayos con observadores: predicción E1/E2 y actual E1/E2.
- Captura previa en MONITOR confirmó comunicación UART pero no validez del ADC (k=0, flag F_Y=32 con acondicionador no alimentado o aislado). El primer ensayo abierto requiere restituir J9--P0[2] y J8--J5 con todas las fuentes apagadas, y mantener protecciones de firmware.
- Guía operativa: `04_Ensayos/ENSAYO_01_ESCALON_ABIERTO.md`. Se conserva advertencia de que proyecto Lab7 PSoC Creator está actualmente local, no subido automáticamente.

## 2026-11-23 — Primera captura de datos del Rigol por USB

- El usuario aportó `pantalla.png`, `chan1.csv`, `chan2.csv` y `metadatos.json`; se verificaron 1200 muestras por canal y ventana de 120 ms. Metadatos: 22:34:13-03:00.
- CH1: promedio -31.0 mV pretrigger y 2379.92 mV posestímulo (delta +2410.92 mV). CH2: +16.652 mV y +11.500 mV (delta -5.152 mV).
- No es aún un escalón de 50 mV validado de J5 porque no está confirmado el nodo CH1: antes fue solicitado J9. UART en ensayos anteriores detenía el firmware en k=0 por flags=32.
- Ver `04_Ensayos/ANALISIS_CAPTURA_RIGOL_20261123_223413.md`. No confundir trazas con resultados de control E1/E2.
