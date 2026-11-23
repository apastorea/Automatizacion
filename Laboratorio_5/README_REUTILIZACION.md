# Antecedentes recuperados del Laboratorio 5

Este directorio contiene **una selección trazable de archivos originales**, copiados sin editar desde `Laboratorio 5.zip`. La lista completa y las huellas SHA-256 se encuentran en `INVENTARIO_ARCHIVOS.csv`. Se omitieron dependencias generadas por PSoC Creator, resultados redundantes, renders temporales, bibliografía de terceros y respaldos anidados.

## Información que sí conviene reutilizar

- Proyecto fuente PSoC Creator 4.4: `PSoC_5LP/Lab5.cywrk`, carpeta `Lab5.cydsn/` con `Lab5.cyprj`, pines `.cydwr`, TopDesign, lógica C y encabezados; los archivos autogenerados se regeneran con PSoC Creator.
- Rutinas de instrumentación: `../Herramientas_Comunes/Rigol_y_UART/`.
- Scripts MATLAB de adquisición, calibración, evaluación y exportación de resultados.
- Calibración histórica de ADC/DAC, curva J5 del actuador y trazabilidad J7/ADC.
- Capturas seleccionadas de calibración, revalidación y control experimental, con `metadata.json` y archivos crudos `.csv` conservados.
- Informe propio de Lab5 y script con el que se generó.

## Valores históricos, NO validados aún para Lab7

| Antecedente | Valor | Archivo de procedencia |
|---|---:|---|
| Offset ADC | 2.353802067 V | `PSoC_5LP/Lab5.cydsn/lab5_config.h` |
| Escala ADC/planta | 0.210251951 V/V | igual |
| Ganancia rama DAC positiva | 3.842612 | igual |
| Ganancia rama DAC negativa | 2.640105691 | igual |
| Offset J5 | 0.0172086 V | `MATLAB/datos_experimentales/lab5_calibracion_final_circuito_cerrado_v4_20261120_231219/ajustes_calibracion.csv` |
| Pendiente J5/u aplicada | 0.9817098 V/V | igual |
| Pendiente J7/lectura ADC | 1.0169923 V/V | igual |
| Error RMS de ajuste de J7 | 0.0033743 V | igual |
| Límites históricos mando | ±1 V | `PSoC_5LP/Lab5.cydsn/lab5_config.h` |

**Atención:** no mezclar el resumen antiguo del Laboratorio 5 ni los tiempos de muestreo históricos con el nuevo diseño. Existen distintas etapas y revisiones; se recomienda obtener el modelo continuo de Lab7 desde el circuito conectado y registrar la selección en la bitácora.

## Medidas válidas y diagnósticas

Los subdirectorios de `MATLAB/datos_experimentales` conservan el nombre y la fecha originales. Los casos de calibración final `v4` y revalidación posterior son bases de calibración. También se mantienen las capturas de control TS1/TS2 seleccionadas, y los ensayos oscilatorios fallidos por saturación **solo para diagnóstico**. Otras capturas posteriores de modelo identificado se guardan para su análisis comparativo, sin conferirles automáticamente estatus de validación Lab7.

## Advertencia de firmware

`lab5_experiment.h` recuperado fija `LAB5_MODE_CONTROL`, `LAB5_CALIBRATED=1`, diseño `TS2_DEADBEAT` y referencia `0.050 V`. Esto contradice la instrucción de modo MONITOR del README histórico. Se ha preservado exactamente para no falsificar la historia: **no utilizarlo como firmware seguro predeterminado en pruebas físicas**.

## Placa, conexiones y equipo

Laboratorios 4/5: PSoC 5LP, Rigol DS1202Z-E, PSoC Creator 4.4, MATLAB R2026b, USB-VISA/SCPI, UART COM4 a 57600 8N1, sondas 10X, acoplamiento DC, CH1/J5, CH2/J7. Cableado en `Calibraciones_historicas_Lab4/README_CONFIGURACION_INSTRUMENTACION.md`; verificar físicamente el circuito de Lab7 antes de reutilizarlo.
