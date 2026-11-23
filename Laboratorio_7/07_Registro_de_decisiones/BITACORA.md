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

## 2026-11-23 — Simulaciones nominales E1 verificadas por el usuario en MATLAB R2026b

- Captura del usuario: `validar_nominal_lab7` terminó correctamente (solo advertencia intencional de modelo nominal); `lab7_principal` confirmó cuatro conjuntos simulados y generó PNG/CSV en su PC.
- Gráficas recibidas y analizadas: `lab7_prediccion_E1.png` y `lab7_actual_E1.png`; no se han incorporado los archivos de imagen al repositorio.
- Reconstrucción numérica independiente del script: predictor E1 Mp=15.293%, ts2=46ms; actual E1 Mp=15.263%, ts2=48ms (ambos medidos desde escalón en t=20ms); picos en t=42ms.
- u[0] predictor=25.57mV y actual=55.90mV; máximos positivos 97.98mV y 97.88mV; mínimos -8.72mV y -16.25mV, respectivamente.
- Desviación de salida previa al escalón: máximos 8.20mV predictor y 15.22mV actual, originados en error inicial de estimación.
- Nota: la norma de error del actual en k=0 ya incluye la corrección con y[0]; no comparar directamente la primera muestra con el predictor.
- Pendiente: análisis de E2 y exportación de métricas directamente desde MATLAB; validación física en PSoC y Rigol.
