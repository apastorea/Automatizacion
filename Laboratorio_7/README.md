# Laboratorio 7 — Estimadores de estado de predicción y actual

**Guía rectora:** `00_Enunciado/Lab6_Estimadores_Enunciado.pdf`. El encabezado es erróneo pero la consigna es válida para este Laboratorio 7.

## Requisitos tomados de la guía oficial

1. Elegir y justificar el periodo de muestreo antes de discretizar.
2. Obtener el espacio de estados continuo y discreto; verificar observabilidad desde la salida medida.
3. Diseñar el controlador por realimentación de estados estimados con estimador de predicción y estimador actual.
4. Seleccionar polos de lazo cerrado y comparar **dos** ubicaciones de polos para cada tipo de estimador.
5. Implementar ambos compensadores en el PSoC usando exclusivamente estimaciones de estados.
6. Comparar dinámica del estimador, esfuerzo y diferencia MATLAB–experimento, con discusión y conclusiones.

## Estado de ejecución

- [x] Recuperación estructurada del Lab5 e instrumentación.
- [x] Guía oficial, estructura de proyecto, plan de ensayos y borrador LaTeX.
- [x] Núcleo genérico C de predictor y estimador actual (no conectado a hardware).
- [x] Script MATLAB de diseño/simulación preparado.
- [x] Modelo nominal de la guia derivado; Ts=2 ms provisional.
- [ ] Modelo y muestreo validados fisicamente para Lab7.
- [ ] Calibración física ADC/DAC posterior al montaje definitivo.
- [x] Ganancias nominales K, Nr, L_pred, L_actual calculadas y contrastadas numericamente.
- [ ] Validacion en MATLAB local y posterior ajuste con la planta medida.
- [ ] Mapa completo TopDesign, ADC, DAC, Timer, ISR y UART para Lab7.
- [ ] Ensayos en PSoC de ambas arquitecturas, con dos juegos de polos evaluados.
- [ ] Datos crudos, gráficos, tablas, métricas, comparación y conclusiones.

## Advertencias técnicas

La planta del Lab7 **no debe darse por igual a la del Lab5** sin verificar el nuevo esquema y parámetros. La placa **no debe programarse con este núcleo C aislado**; faltan las interfaces físicas, la calibración y el test de seguridad. La ley de control será `u[k] = -K x_est[k] + Nr r[k]`.

La función matemática del observador actual usa la medición **de la misma muestra** para corregir la predicción antes de computar el control; la del predictor aplica la innovación para construir la estimación de **la muestra siguiente**.

## Etapa 1 — Modelo nominal

Consultar `01_Modelado_MATLAB/DERIVACION_MODELO_NOMINAL.md`. Ejecutar `validar_nominal_lab7` y `lab7_principal` con Control System Toolbox. Datos simulados, no experimentales.
