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

## 2026-11-23 — Ensayo ABIERTO: adquisición UART completa

- Usuario ejecutó `capturar_uart_monitor_lab7.m` tras restablecer el enlace del ADC: cabecera `modo=ABIERTO`; 256 filas, 13.906 bytes, `# LAB7 END; DAC=0`.
- Primera muestra k=0: t_us=0, adc_counts=2069, adc_mV=2354, y_cal=0mV, y_rel=0mV, u_solicitada=0, cpu_us=45, flags=0.
- Muestras finales: k=254 t_us=508000, adc_mV=2355, y_rel=1mV, cpu_us=45, intervalo_us=2001, flags=0; k=255 t_us=509999, adc_mV=2355, y_rel=1mV, cpu_us=46, intervalo_us=1999, flags=0.
- El script guardó `Lab7_UART_20261123_225357/uart_bruto.txt` y `monitor_lab7.csv` **solo en la PC del usuario**. Aún no están disponibles como adjuntos ni en GitHub para verificar las muestras intermedias.
- El bloqueo previo con flags=32 ya no se manifestó; la señal del ADC se estabilizó cerca del offset histórico. No afirmar todavía ganancia de planta ni respuesta al escalón: falta verificar `u_solicitada` en k32..127 y capturar físicamente CH1=J5, CH2=J7 con Rigol.

## 2026-11-23 — Primer pulso en lazo abierto adquirido y graficado en MATLAB

- El usuario compartió nueva captura UART en modo `ABIERTO`: 256 filas, `flags=0` en muestras inicial/final; `adc_mV=2355` y `y_rel_mV=5` en k=0 y k=255, `intervalo_us=1999` en k255.
- Figura `Lab7 - Ensayo experimental abierto`: pulso solicitado 50mV; nominal DAC ~46mV; comienza ~64ms y termina ~256ms. Salida `y_rel` aumenta de ~5mV a ~44mV y regresa a ~1mV tras el pulso, con saltos de ~5mV por cuantización probable.
- Aproximación visual: Delta y ~39mV; Delta u nominal ~46.1mV; K aparente ~0.85. No es una identificación de ganancia física de planta (falta CH1=J5).
- Se prepara script `analizar_escalon_abierto_lab7.m` con tabla y contraste frente al modelo nominal y al identificado Lab5, sin reajustar calibraciones.
- Pendiente urgente: captura simultánea Rigol J5/J7 durante un solo escalón y evaluar consistencia para desbloquear observador E1. No volver a barrido largo de calibración.

## 2026-11-23 — Segunda captura Rigol: datos transferidos, pero sin pulso

- Se recibieron los CSV del Rigol en modo quick, 1200 puntos por canal, 0.5ms por punto, ventana temporal 600ms, pantalla STOP, escalas 20mV/div.
- CH1 media 14.026mV, mínimo 10.4mV, máximo 18.4mV; CH2 media 10.766mV, mínimo -1.6mV, máximo 27.2mV.
- Trigger capturado en pantalla ~25.2mV por flanco CH1, umbral que **no se alcanzó** en ningún punto del CH1 exportado. No se detecta pulso de 192ms ni meseta de la respuesta en CH2.
- Evidencia de transferencia de datos USB operativa, NO de captura del estímulo real. Ver `04_Ensayos/ANALISIS_CAPTURA_RIGOL_20261123_231651_SIN_ESCALON.md`.
- Siguiente acción: armar SINGLE antes de SW3 y comprobar WAIT/STOP y meseta amarilla; elevar trigger a ~35mV entre reposo de ~14mV y pulso esperado ~60mV.

## 2026-11-23 — Tercera captura Rigol: pulso real identificado en los CSV

- `chan1(3).csv`, `chan2(3).csv` y `metadatos(3).json` aportados por usuario, analizados en Python; modo de transferencia quick data, 0.554s, 1200 puntos/canal, 0.5ms de incremento temporal.
- Pulso CH1 de -193.5 a -1ms en tiempo relativo; medias antes/meseta CH1 15.5133/60.1022mV y CH2 11.9600/56.6756mV.
- Delta CH1=44.5889mV; Delta CH2=44.7156mV; ganancia aparente por medición simultánea 1.00284. Compatible con esquema nominal 1.01856 y modelo identificado Lab5 1.00294.
- Confirmar que CH1 estaba en J5 y CH2 en J7; de otro modo no etiquetar la relación como ganancia de planta.
- Se cambió el lanzador de doble clic para descargar PNG original y CSV en una sola ejecución rápida.

## 2026-11-23 — Capturador sincronizado Lab7 (nuevo)

- Se adaptó el comportamiento de las herramientas originales lab4_ensayo_sincronizado.py y lab5_captura_monitor_rigol.m al protocolo real de Lab7.
- Script creado: Herramientas_Comunes/Rigol_y_UART/lab7_ensayo_sincronizado.py.
- Lanzador de doble clic: Laboratorio_7/04_Ensayos/capturar_lab7_sincronizado.cmd.
- Sincronización: detecta '# LAB7 inicio;', arma :SING tras 0.5s, antes de LAB7_INICIO_MS=3000; después descarga UART con '# LAB7 END;', dos CSV del Rigol, PNG y metadatos.
- No modifica el PSoC ni fuerza el trigger. Exige 256 filas, flags=0, coincidencia de modo y excursión de CH1 para etiquetar la captura preliminar como válida.
- Prueba offline: serial simulado y Rigol simulado con 256 muestras, estado STOP y pulso de 45 mV; verificó seis archivos y armado 0.6s después de inicio. **Pendiente de ejecución en banco con equipo real.**

## 2026-11-23 23:47 — Primera captura sincronizada Lab7: UART válida, evento Rigol no capturado

- Archivos aportados por usuario: \`psoc_uart.csv\`, \`psoc_uart.txt\`, \`chan1(4).csv\`, \`chan2(4).csv\`, \`metadatos(4).json\`, \`pantalla(3).png\`. Su contenido sigue adjunto a la conversación; originales aún no volcados al repositorio.
- UART: 256 filas, todas flags=0, Ts mediana 2000us, CPU máxima 55us, pulso pedido 50mV por 96 muestras (k32..k127), DAC nominal 46mV. ADC registra respuesta de 5mV de reposo a 43–49mV durante pulso y vuelve a 0–5mV.
- Rigol: CH1 1200 puntos, 0.5ms de resolución visual, min 12.8mV, max 22.4mV, media 16.901mV; CH2 min -4.0mV, max 31.2mV, media 13.159mV con oscilación/ruido. Ningún pulso físico de ~45mV en CH1. Variación robusta CH1 = 5.6mV.
- Capturador previo etiquetaba trigger_fisico_confirmado=true solo por estado STOP, aunque el propio validador preliminar decía false. Se corrigió en \`lab7_ensayo_sincronizado.py\`: separar \`rigol_finalizo_single\` de \`pulso_ch1_detectado\` y exigir pulso robusto >=20mV además de STOP.
- Esta captura sirve para validar telemetría y automatización de adquisición, pero **NO** para cálculo de ganancia física ni comparación dinámica con Rigol. Existe una captura anterior de CSV CH1/CH2 con pulso físico ~44.59/44.72mV y ganancia preliminar ~1.003, más apropiada para el ensayo de planta.
- Siguiente intento opcional, sin cambiar firmware, con umbral 45mV y armado a 2.0s del aviso de inicio para evitar transitorios: \`python -u .../lab7_ensayo_sincronizado.py --modo-esperado ABIERTO --label abierto_trigger45 --nivel-trigger 0.045 --demora-armado 2.0\`.

## 2026-11-24 — Captura Lab7 mejorada con respaldo temporizado Lab5

- Actualizado `Herramientas_Comunes/Rigol_y_UART/lab7_ensayo_sincronizado.py` para combinar flanco físico con `:TFOR` programado si el Rigol aún espera.
- Sincronía con `# LAB7 inicio;`: armar `:SING` a t≈2.25 s; revisar falso `STOP` y rearmar a t≈2.85 s; aplicar un único `:TFOR` a t≈3.15 s solo si estado `WAIT`, `RUN` o `AUTO` (no si `STOP` o `TD`).
- Marca `configuracion_rigol.trigger_forzado` y `sincronizacion.disparo_forzado` cuando se usa respaldo. El disparo forzado no implica que haya existido respuesta física; la validación de ABIERTO exige pulso en CH1 de al menos 20mV sostenido por 100ms y 256 filas UART sin banderas, con modo coincidente.
- Archivo `capturar_lab7_sincronizado.cmd` conserva recurso VISA exacto del Rigol y usa los tiempos del disparo de respaldo.
- Pruebas fuera de línea: datos CH1 de una captura previa con escalón real reconocidos (≈45.2mV de excursión, ≈194ms de meseta); captura posterior sin escalón descartada (≈0.99mV de excursión filtrada). Simulación UART/Rigol comprobó escenario con disparo físico (0 comandos TFOR) y sin disparo físico (1 TFOR). **La versión corregida todavía requiere prueba en instrumento real.**
- Todos los componentes Lab5 permanecen sin cambios, y el firmware Lab7 mantiene sus protecciones. El nuevo capturador es software anfitrión.

## 2026-11-24 — Diagnóstico instrumentación: PSoC y Rigol capturan eventos distintos

- Nuevos CSV aportados: `chan1(5).csv`, `chan2(5).csv`, `psoc_uart(1).csv`, `metadatos(5).json` y captura `pantalla(4).png`.
- PSoC: 256 muestras, Ts mediana 2000us, CPU máxima 55us, 96 muestras con `u_solicitada_mV=50`, nominal DAC 46mV, flags=0, y_rel alcanza alrededor de 44mV.
- Rigol: 1200 puntos por canal, 0.5ms/punto; CH1 mediana 15.6mV, mínimo10.4mV, máximo20.8mV, NO hay pulso sostenido; CH2 promedio11.886mV, min -6.4mV, max30.4mV, ruido. En metadata `estado_rearme=WAIT`, `estado_antes_respaldo=STOP`, `disparo_forzado=false`, `pulso_detectado=false`.
- Diagnóstico: bajo trigger CH1=35mV, adquisición terminó sin mostrar el escalón. Sospecha de disparo espurio o ventana distinta al pulso, no demostración de desfasaje fijo. No etiquetar esta captura como respuesta física.
- Cambio: estrategia por defecto `temporizada`: CH1 trigger 85mV (dentro de ±5div a 20mV/div), HRES, SINGLE t≈2.25s, rearme t≈2.85s, TFOR t≈3.025s para registrar evento previsto 3.064..3.256s. Se conservan el modo `fisica` y los metadatos/flags de seguridad. **Pendiente probar en el Rigol real.**

## 2026-11-24 — Comparación real de ruido Lab5 contra Lab7

- Referencia Lab5 en el repositorio: ensayo `lab5_identificado_TS1_deadbeat_50mV_zerocorr_final_20261121_175752`, CH1/CH2 CSV, ventana 40–80ms. Desviación estándar CH1≈8.44mV, CH2≈5.79mV. Ajustes Lab5: CH1 50mV/div, CH2 20mV/div, BW20M, HRES.
- Nueva captura Lab7 desde `chan1(6).csv`/`chan2(6).csv`: CH1≈3.00mV, CH2≈11.57mV sobre meseta 65–180ms; CH2 aproximadamente doble de la referencia. No concluir causa física exacta: modos distintos y datos NORM 1200 puntos; diferencias incluyen condiciones de adquisición.
- Se ajusta script Python Lab7: por defecto CH1=50mV/div, CH2=20mV/div, sin resetear OFFS vertical; se permite separación visual manual sin tocar valores físicos.
- Siguiente discriminación: CH2 a GND cerca de PCB con clip a GND, verificar si la dispersión procede de sonda/masa o del nodo J7; después reconectar con alimentación apagada.

## 2026-11-24 00:59 — Ensayo abierto real válido al restablecer alimentación analógica

- Durante ensayo anterior (00:57) la fuente analógica estaba apagada por olvido; UART se detuvo en k=0 con ADC=586mV, y_cal=-8409mV, flags=32. Rigol tuvo 0 puntos por canal y quedó WAIT; el error no era de sincronización sino falta de alimentación.
- Al conectar fuente, el usuario aportó `pantalla(7).png`, `chan1(8).csv`, `chan2(8).csv`, `psoc_uart(4).csv`, `psoc_uart(4).txt`, `metadatos(8).json`. Archivos crudos aún permanecen en conversación y deben conservarse en carpeta del ensayo para trazabilidad.
- Rigol: HRES, t=−0.3..+0.2995s (0.5ms/punto), CH1 50mV/div (J5), CH2 20mV/div (J7), base 50ms/div, `:TFOR` a 3.0312 s del aviso UART. Se detecta pulso sostenido ~193.5ms y excursion robusta CH1=45.524mV.
- Estadísticos independientes calculados de CSV: reposo [−240,−80] ms y meseta [+70,+160] ms, referidos al trigger: CH1 media 15.175mV→60.298mV (delta +45.123mV, ruido RMS pre 3.282mV, meseta 3.380mV); CH2 media 11.7025mV→56.115mV (delta +44.412mV, ruido RMS pre 11.150mV, meseta 10.371mV). Ganancia aparente física K=0.984245, desviación −3.37% frente a K_nominal=1.0185604.
- UART: 256 muestras, Ts mediana 2000us, intervalos 1999..2001us, tiempo máximo CPU=55us, 96 muestras con mando solicitado 50mV, ninguna bandera distinta de 0; el CSV nominal indica 46mV DAC durante el pulso.
- Metadatos: `ensayo_valido_preliminar=true`, pulso detectado, `disparo_forzado=true`, `trigger_fisico_confirmado=false`; esto es correcto y **no invalida** la respuesta física: el osciloscopio usó disparo SCPI temporizado y sí detectamos un pulso en CSV.
- Pendiente: validar dinámica mediante ajuste/contraste de modelos nominal e identificado Lab5 con desfase instrumental estimado; la señal CH2 continúa más ruidosa (~10-11mV RMS), aunque el promedio por meseta permite medir amplitud con cautela. No activar lazo cerrado hasta validar el observador y condiciones previstas.

## 2026-11-24 — Revisión pre-cierre: estabilidad real no garantizada para Actual E1

- Tras ejecutar correctamente la comparación física ABIERTO vs modelos, se inspeccionó la plantilla exacta de firmware `Lab7.cydsn/main.c`, `lab7_config.h`, el núcleo portable y la guía oficial del enunciado.
- Comprobación numérica independiente del lazo aumentado con planta de Lab5 identificada (K=1.002941, tau1=9.06915ms, tau2=.774399ms): radio espectral Pred E1=.911, Actual E1=1.049, Pred E2=.829 y Actual E2=.825. Con planta nominal todos .838. Actual E1 bajo modelo identificado supera el círculo unidad: NO habilitar sin rediseño y revalidación.
- Polos alternativos para E1 0.35±j0.1 dan rho Pred=.855, Actual=.874 en el mismo contraste (solo candidato, no incorporado a firmware).
- Se agregaron `01_Modelado_MATLAB/evaluar_robustez_observadores_lab7.m`, `simular_no_ideal_observadores_lab7.m`, `explorar_polos_E1_robustos_lab7.m` y `04_Ensayos/VALIDACION_PRE_CERRADO_E1.md`.
- El núcleo C aislado `lab7_estimadores.c` compiló y pasó `test_portable.c` con GCC. Esto no sustituye PSoC Creator ni pruebas en placa.
- Se detectó además diferencia para pruebas justas: MATLAB previo usa `x_estimado0=[.02;-.01]` y referencia desde 20ms; firmware inicia estimación en cero y referencia desde k=32 (64ms). No comparar tiempos directamente sin alinear excitación y estados iniciales.
- **No se modificaron enclavamientos ni se programó el PSoC**. Próximo: ejecutar las tres auditorías MATLAB, estudiar rediseño de E1 Actual si se confirma la sensibilidad y entonces planificar ensayo físico seguro.
