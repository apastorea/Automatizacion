# Automatización — Laboratorios 5 y 7

**Repositorio:** https://github.com/apastorea/Automatizacion

Repositorio académico para mantener trazabilidad de los antecedentes experimentales del **Laboratorio 5** y desarrollar el **Laboratorio 7** de la asignatura Automatización (Ingeniería Electrónica, Universidad Católica «Nuestra Señora de la Asunción»).

> **Estado del proyecto:** Lab5 conservado como antecedente histórico seleccionado. Lab7 creado con guía oficial, módulos iniciales de diseño y observación, estructura experimental y borrador LaTeX. **Lab7 todavía no tiene diseño numérico validado ni resultados físicos.**

> **Aclaración de numeración:** el archivo oficial del Lab7 se llama `Lab6_Estimadores_Enunciado.pdf` y conserva un encabezado errado; corresponde a nuestra práctica **N.º 7**. La consigna que utilizamos es la de **estimadores de predicción y de estado actual**, no los fragmentos superpuestos de síntesis directa que figuran en la digitalización de la guía.

## Mapa del repositorio

- `Laboratorio_5/`: archivos seleccionados del proyecto histórico de PSoC, MATLAB, calibración y resultados; **no modificar los datos crudos**.
- `Herramientas_Comunes/Rigol_y_UART/`: scripts heredados para RIGOL DS1202Z-E (USB-TMC/SCPI) y telemetría PSoC.
- `Laboratorio_7/00_Enunciado/`: consigna oficial, sin modificar.
- `Laboratorio_7/01_Modelado_MATLAB/`: preparación de planta, ubicación de polos y simulación de observadores.
- `Laboratorio_7/02_Firmware_PSoC_5LP/`: núcleo portable de los dos estimadores. **No está conectado aún a un proyecto PSoC Creator ni listo para programar una placa.**
- `Laboratorio_7/03_Calibracion/`: protocolo de revalidación; pendientes datos físicos propios de Lab7.
- `Laboratorio_7/04_Ensayos/`: protocolo, evidencias por fecha y metadatos.
- `Laboratorio_7/05_Resultados/`: tablas, gráficos y métricas propias de Lab7.
- `Laboratorio_7/06_Informe_IEEE/`: informe LaTeX de dos columnas, sin valores experimentales inventados.
- `Laboratorio_7/07_Registro_de_decisiones/`: bitácora de cambios y pendientes.

## Cómo comenzar

1. Leer `Laboratorio_5/README_REUTILIZACION.md` y `Laboratorio_7/README.md`.
2. Revisar `Laboratorio_7/03_Calibracion/PROTOCOLO.md` y medir el nuevo cableado **antes de cerrar el lazo**.
3. Completar la matriz continua y la salida física correcta en `Laboratorio_7/01_Modelado_MATLAB/modelo_lab7.m` (el script bloquea cálculos no validados).
4. Ejecutar `lab7_diseno_observadores.m` en MATLAB con Control System Toolbox.
5. Validar coeficientes, límites y temporización antes de integrar el firmware con PSoC Creator.
6. Compilar LaTeX con `pdflatex` o en Overleaf abriendo `Laboratorio_7/06_Informe_IEEE/main.tex`.

## Precauciones sobre la herencia de Lab5

- El firmware histórico `Laboratorio_5/PSoC_5LP/Lab5.cydsn/lab5_experiment.h` quedó guardado con **modo CONTROL y `LAB5_CALIBRATED=1`**, aunque su README describe MONITOR. **No programar directamente esa configuración histórica sobre un circuito conectado.** Poner explícitamente el modo seguro MONITOR y verificar antes de energizar.
- Las calibraciones y parámetros de Lab4/Lab5 son antecedentes útiles, **no sustituyen mediciones actuales**.
- Mantener separadas magnitudes pedidas, crudas, calibradas y efectivamente aplicadas; nunca renormalizar sin documentar.
- El laboratorio utiliza el RIGOL **DS1202Z-E** (no un Tektronix).
- Los metadatos heredados pueden incluir identificadores de equipos y otros datos de procedencia. **Crear el repositorio como PRIVADO** y revisar el contenido antes de volverlo público.
- Los informes de compañeros **no se incorporaron al repositorio** por respeto a la autoría y a los datos personales: se usaron solamente para tomar referencias de estructura.

## Alcance de herramientas

El núcleo C provisto no contiene control del ADC, DAC, ISR ni temporizador de PSoC Creator; no debe utilizarse con hardware sin completar y validar dichas capas. El script MATLAB no declara que el modelo de Lab5 sea idéntico al del Lab7.

Para crear y subir el proyecto ver `GUIA_GITHUB_WINDOWS.md`.
