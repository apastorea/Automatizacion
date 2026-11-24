# Matriz de requisitos y figuras — Laboratorio 7

## Fuentes verificadas
Guía oficial: Lab6_Estimadores_Enunciado.pdf (encabezado 6 erróneo); antecedente: Lab7_Auto_LM (1).pdf, Luis Morel, 26 páginas. No usar sus mediciones como si fuesen propias.

## Requisitos de guía
- Justificar el tiempo de muestreo y obtener modelo continuo y discreto ZOH; comprobar observabilidad.
- Diseñar K y precompensación de referencia, usando SOLO estados estimados en la realimentación.
- Diseñar observador de predicción y estimador actual; evaluar dos ubicaciones de polos E1/E2.
- Implementar ambas estructuras en PSoC, comparar dinámica, error de estimación, esfuerzo y resultados reales frente a simulación.
- Discutir diferencias y elaborar conclusiones.

## Las 24 figuras del informe de Luis
| Números | Arquitectura / polos | Tipo | Cuatro gráficas |
|---|---|---|---|
| 1–4 | Predictor E1 | MATLAB | respuesta, u, y vs yhat, error |
| 5–8 | Actual E1 | MATLAB | respuesta, u, y vs yhat, error |
| 9–12 | Predictor E2 | MATLAB | respuesta, u, y vs yhat, error |
| 13–16 | Actual E2 | MATLAB | respuesta, u, y vs yhat, error |
| 17–20 | Predictor E1 | Experimental | respuesta, u, y vs yhat, error |
| 21–24 | Actual E1 | Experimental | respuesta, u, y vs yhat, error |

Luis simuló las cuatro combinaciones, pero implementó físicamente solo E1 predictor y E1 actual. Sus figuras de error tras reinicio simulado a 16 ms y sus métricas de respuesta nominal son de ensayos DIFERENTES; no deben compararse sin aclaración.

## Diferencias fundamentales frente al montaje propio
- Luis: referencia cuadrada 0.5–1.0 V (100ms/nivel), base de estados con C=[1 0] y salida física y=x1.
- Proyecto actual: referencia inicial de 50mV, C=[0 1] y salida física y=x2. En nuestro reporte el error observable es e_y = y - C*xhat = y - xhat2, SI la telemetría y el firmware conservan esta misma base. Nunca renombrar xhat1 como salida medida sin transformación explícita.
- No copiar las ganancias K, Ke o Ka de Luis a nuestro PSoC sin comprobar la transformación de coordenadas, signos, saturación, escalas ADC/DAC y límites del actuador.
- La perturbación de estimador debe diferenciarse del ensayo de respuesta a referencia. Solo y es medible directamente; las estimaciones se reciben por UART o señales de depuración implementadas, no como estados físicos.

## Evidencia del montaje propio
- Modelo, discretización, controlabilidad, observabilidad, K, Nr y cuatro simulaciones nominales: preparados en MATLAB.
- Ensayo ABIERTO en PCB original de Lab5: comprobado; Rigol CH1=J5 y CH2=J7; UART 256 filas, Ts mediana 2000us, flags=0, mando solicitado 50mV durante 96 muestras. Pulso físico aproximadamente 45mV, respuesta física aproximadamente 44mV. Se etiqueta como VALIDACIÓN DE PLANTA, no evaluación de observador.
- Capturas y telemetría originales conservar como evidencias: chan1/chan2 CSV, PNG, psoc_uart CSV/TXT, metadatos JSON.
- El ruido de J7 (~10–11mV RMS en la meseta) es significativo; no borrar datos brutos ni calcular dinámica sin considerarlo.
- El programa generar_16_figuras_lab7.m produce 4 figuras individuales por cada simulación; compara y=C*x frente a yhat=C*xhat, no un estado no medido.
- El programa comparar_abierto_rigol_modelos_lab7.m contrasta entrada medida en J5 y salida medida en J7 con modelo nominal y el identificado en Lab5.

## Medidas experimentales aún obligatorias
1. Predictor E1 en lazo cerrado: captura respuesta al cambio de referencia, u, y, yhat, error observable, tiempos, flags.
2. Actual E1 con exactamente las mismas condiciones y límites.
3. Separar ensayo de convergencia de estimador (perturbación segura de xhat) de ensayo de seguimiento de referencia. Calcular Mp, tr, ts, ess en seguimiento; convergencia de error en perturbación.
4. Evaluar E2 como simulación obligatoria; considerarlo experimental si la validación de seguridad y ruido lo permite, como extensión.
5. Comparar métricas en tablas MATLAB vs PSoC y documentar si una magnitud no se mide (N/D).

## Estado actual y prioridad
Pendiente de completar: 16 PNG individuales en MATLAB, control en PSoC con predictor E1, actual E1, medidas de convergencia y esfuerzo, comparativa y discusión LaTeX. El ensayo abierto actual ya es suficiente como validación previa; no repetir barridos de calibración.

Próximo comando tras git pull desde MATLAB y directorio 01_Modelado_MATLAB:
generar_16_figuras_lab7
comparar_abierto_rigol_modelos_lab7

No habilitar lazo cerrado solo porque el ensayo abierto fue válido: revisar el algoritmo de estados, la base de coordenadas, el uso del estimado y las protecciones.
