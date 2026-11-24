# Lab7 — Decisión de diseño E1 y preparación de PSoC (2026-11-24)

## Evidencia real de MATLAB aportada en conversación
Script: `comparar_E1_original_y_redisenado_lab7.m`, salida y gráfico de cuatro paneles del 24-11-2026. Se compara planta identificada Lab5, referencia de 50 mV que comienza a 64 ms, ADC/DAC aproximadamente cuantizados y ruido hipotético de 0 o 10 mV RMS.

| Caso | Ruido mV RMS | Máximo salida mV | Promedio final mV | Máximo u mV | Saturaciones (solicitud software) |
|---|---:|---:|---:|---:|---:|
| E1 original Predictor | 0 | 76.09 | 46.247 | 107.59 | 0 |
| E1 original Predictor | 10 | 79.149 | 49.741 | 122.96 | 0 |
| E1 original Actual | 0 | 91.81 | 37.753 | 122.96 | 59 |
| E1 original Actual | 10 | 100.43 | 40.263 | 122.96 | 72 |
| E1 alternativo Predictor | 0 | 61.557 | 46.247 | 92.223 | 0 |
| E1 alternativo Predictor | 10 | 65.633 | 46.445 | 107.59 | 0 |
| E1 alternativo Actual | 0 | 66.27 | 46.247 | 92.223 | 0 |
| E1 alternativo Actual | 10 | 67.527 | 49.371 | 107.59 | 0 |

**Advertencia:** los datos de esta tabla proceden de la primera versión del script, donde el DAC se redondeaba *después* del límite ±120mV y podía aplicar 122.96mV. Se corrigió el script en la revisión 2 para limitar también el código DAC antes de regresar a hardware: **hay que regenerar las métricas de revisión 2; no atribuirle los valores originales**. La saturación física por cuantización no se contaba en la columna anterior.

Radio espectral lineal del sistema aumentado con modelo Lab5: E1 original predictor = 0.91084, E1 original actual = 1.04870 (no estable); E1 alternativo predictor = 0.85497, E1 alternativo actual = 0.87367.

## Candidato elegido para avanzar al paso de integración
E1 alternativo: polos en plano z `0.35 +/- j0.10`, muestreo `Ts=2ms`. Solo *candidato* hasta comprobar firmware real y ensayos físicos.
- `L_pred = [-1.317866535; 0.438770457]`
- `L_actual = [-1.505834909; 0.425644058]`
- `K = [2.15692217, 6.87132640]` (sin cambios)
- `Nr = 1.09474803` (sin cambios)
- `C = [0 1]`; por tanto `y = x2` en estas coordenadas.

**No escribir estos números directamente en un firmware no inspeccionado.** El repositorio actual conserva solo `02_Firmware_PSoC_5LP/lab7_estimadores.c/.h` y `INTEGRACION_PSOC.md`, pero **no conserva la copia activa** de `main.c`, `lab7_config.h` o `TopDesign.cysch` que PSoC Creator compila en la PC. Es indispensable revisarlos antes de indicar qué `#define`, qué unidades o qué protecciones cambiar.

## Punto de control inmediato
1. Ejecutar `git pull --ff-only origin main`.
2. En MATLAB volver a ejecutar `comparar_E1_original_y_redisenado_lab7` (revisión 2) y observar que `control_max_mV` no supere 120 en ninguno de los casos. La diferencia respecto a la captura anterior se explica por el recorte físico después de cuantizar.
3. Localizar en el PC la copia compilada de `lab7_config.h` y `main.c` dentro de `Laboratorio_7/02_Firmware_PSoC_5LP` o en PSoC Creator. No alterar todavía el modo MONITOR/ABIERTO ni cambiar todas las autorizaciones de seguridad.
4. Inspeccionar en `main.c` el orden ADC→unidades de salida→estimador→limitación/software→código DAC→telemetría, la configuración de `LAB7_MODO`, variante E1/E2, las banderas de protección y el comportamiento seguro.
5. Solo después preparar una variante Predictor E1 candidata y ensayarla con alimentación/control y Rigol correctamente cableados. Mantener captura síncrona UART + CH1 J5 + CH2 J7 y vigilancia de flags, tiempos ISR, esfuerzo máximo y saturación.
6. Conservar las cuatro simulaciones anteriores sin mezclarlas con la alternativa. El informe documentará la elección justificada mediante la planta identificada y el comportamiento con cuantización.

## Advertencias de interpretación
- La convergencia ante un único vector de ruido aleatorio no permite garantizar robustez a toda perturbación.
- La proximidad de `salida_cola_mV` a 50 mV con ruido no prueba error estacionario exactamente nulo: usar promedios en ventanas y ensayos repetidos.
- La señal cruda del Rigol CH2 contiene ruido mayor que CH1. Los 10 mV hipotéticos introducidos al simulador no han sido calibrados como una incertidumbre del ADC del PSoC.
- La comprobación `rho<1` es necesaria para el modelo lineal, pero no suficiente con saturaciones, cuantización, retardos y cambios de condiciones.
