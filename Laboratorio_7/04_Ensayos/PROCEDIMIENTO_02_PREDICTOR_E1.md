# Lab7 — Primer ensayo supervisado: Predictor E1 alternativo

## Antecedentes confirmados
- 256 muestras válidas en MONITOR; flags=0; DAC nominal=0; tiempo máximo CPU=51µs; periodo mediano=2000µs.
- Los tres archivos HAL (lab5_hardware.c, lab5_hardware.h, lab5_config.h) son idénticos entre proyecto original y copia E1 (SHA-256).
- Planta validada en ABIERTO con referencia solicitada 50mV; tensión real de entrada/salida aproximadamente 45mV/44mV.
- E1 candidato rediseñado con polos z=0.35±j0.10, Lpred=[-1.31786653;0.43877046], K=[2.15692217,6.87132640], Nr=1.09474803, Ts=2ms.
- Actual E1 original con polos z=0.40±j0.25 NO debe probarse en físico: radio espectral lineal en planta Lab5 identificada=1.0487.

## 1. Conservar el respaldo MONITOR
NO editar el proyecto original ni sustituir la copia que produjo la UART MONITOR válida. Crear otra copia local del proyecto Lab7_E1_Alternativo para el ensayo PRED_PRUEBA. Mantener su fuente, TopDesign y HAL en los estados actuales.

## 2. Verificaciones offline (antes de compilar control)
Ejecutar en MATLAB el script actualizado comparar_E1_original_y_redisenado_lab7. Comprobar que todos los controles máximos simulados quedan por debajo de 120mV y revisar si hay saturaciones de código DAC.

En la COPIA PRED_PRUEBA, comprobar en main.c:
- Lpred E1 = [-1.31786653f, 0.43877046f].
- C=[0 1], K=[2.15692217 6.87132640], Nr=1.09474803.
- F_LIMITE se genera ante saturación por ley de control y también ante tensión nominal del DAC fuera de ±0.120V, con Lab5HardwareZeroOutput.
- La muestra contiene banderas, CPU y códigos DAC. No suprimir ninguno de los mecanismos de parada.

## 3. Prueba del enclavamiento (control BLOQUEADO)
En lab7_config.h de la COPIA PRED_PRUEBA modificar SOLO estas dos líneas:

    #define LAB7_MODO LAB7_MODO_PREDICCION
    #define LAB7_ESTIMADOR_VARIANTE (1u)

Mantener inicialmente las tres autorizaciones del control cerrado en cero y presionar Build. El resultado CORRECTO es un error de compilación CONTROL BLOQUEADO. No programar PSoC en esta etapa.

## 4. Preparación para autorización explícita
Solo después de comprobar el bloqueo, la integridad de HAL y la simulación actualizada, las autorizaciones de la copia PRED_PRUEBA para el ensayo supervisado serán:

    #define LAB7_PLANTA_VERIFICADA (1u)
    #define LAB7_ADC_DAC_REVALIDADOS (1u)
    #define LAB7_AUTORIZAR_LAZO_CERRADO (1u)

LAB7_AUTORIZAR_ESCALON se deja en 0 porque se utiliza únicamente en el modo ABIERTO.
Los límites de la propuesta se mantienen en -0.115 a +0.107 V (petición al DAC); el código comprueba además el límite físico absoluto ±0.120 V. No aumentar la referencia inicial de 50mV.

Revisar el equipo y el proyecto elegido ANTES de programar. Un Build Succeeded no demuestra seguridad física.

## 5. Banco supervisado
Con alimentación apagada, verificar conexiones originales J8-J5, J9-P0[2], J10-J6 y J7-J4; masa común y polaridades de fuente analógica. Usar sondas 10X, acoplamiento DC, CH1 a J5 y CH2 a J7, masas cortas. Preparar parada por fuente y respaldo MONITOR.

Programar únicamente la copia PRED_PRUEBA con presencia del operador y conexiones comprobadas. Cerrar MATLAB y cualquier aplicación que ocupe COM4 o VISA. Abrir capturar_lab7_sincronizado.cmd y seleccionar pred_E1; cuando diga LISTO, pulsar SW3 una vez. Supervisar el Rigol y las indicaciones de la fuente durante el ensayo. Si hay sobrecorriente, señal fuera de rango, oscilación no prevista o flags distintos de cero, cortar salida y volver al modo MONITOR. No reintentar automáticamente.

## 6. Resultados que hay que conservar
Guardado sincronizado: pantalla.png, chan1.csv, chan2.csv, psoc_uart.csv, psoc_uart.txt, metadatos.json. Para el análisis en MATLAB ejecutar:

    analizar_predictor_E1_experimental_lab7

Obtendrá 4 figuras experimentales UART: respuesta y referencia, esfuerzo de control, salida frente a estimación y error observable; además tabla de indicadores. Verificar 256 filas, flags=0, cpu_us < 2000, códigos DAC+ <=7 y DAC- <=11, u_nominal <=120mV. Revisar manualmente el PNG y los CSV de Rigol.

## Advertencias de interpretación
- La etiqueta preliminar del capturador fue diseñada inicialmente para el pulso ABIERTO; no sustituye el análisis dinámico de referencia sostenida en PREDICCION.
- El error de salida se analiza desde k>=32 porque antes del pretrigger el firmware informa salida_V en vez de salida_V menos cero estimado.
- En Predictor la estimación reportada es previa a corregir con la muestra y[k] de ese instante.
- Los resultados con ruido hipotético no prueban estabilidad bajo todas las perturbaciones, ni la simulación excluye problemas físicos. No atribuir mediciones del antecedente Luis Morel al montaje propio.
