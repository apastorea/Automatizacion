# Ensayo experimental 01 — Escalón de 50 mV en lazo abierto

**Objetivo:** medir la respuesta dinámica real de la **misma PCB del Laboratorio 5**, que será usada para el Lab7, sin rehacer un barrido de calibración. Es un contraste de coherencia en un solo ensayo que precede a los cuatro ensayos principales de estimadores.

## Configuración para PSoC Creator 4.4

Proyecto local del usuario: `Laboratorio_7/02_Firmware_PSoC_5LP/PSoC_Creator_Lab7/Lab7.cywrk`. Actualmente se conserva localmente; **no** asumir que esos fuentes ya están sincronizados a GitHub.

En `Lab7.cydsn/lab7_config.h`:

```c
#define LAB7_MODO                   LAB7_MODO_LAZO_ABIERTO
#define LAB7_AUTORIZAR_ESCALON      (1u)
#define LAB7_PLANTA_VERIFICADA      (0u)
#define LAB7_ADC_DAC_REVALIDADOS    (0u)
#define LAB7_AUTORIZAR_LAZO_CERRADO (0u)
```

No modificar `LAB7_U_MIN_V=-0.120f`, `LAB7_U_MAX_V=0.120f` ni `LAB7_Y_FALLO_V=0.500f`. Recompilar con Build Succeeded y programar el CY8C5888LTI-LP097 desde PSoC Creator.

## Condiciones del montaje

- Preparar con alimentación de la fuente Minipa y USB del PSoC desconectados.
- Si se habían retirado durante la captura de monitor: restaurar **J8–J5** (salida acondicionador DAC → entrada planta) y **J9–P0[2]** (acondicionador ADC → PSoC). Retirar la resistencia temporal J5-GND de la prueba aislada, si existe.
- Mantener cableado histórico **J10–J6** y **J7–J4**. Utilizar la fuente bipolar del Lab5, no improvisar otra polaridad.
- Rigol DS1202Z-E: CH1 en **J5**, CH2 en **J7**; ambas masas a **GND de PCB**, sondas y canales 10X, DC.
- No energizar si existen signos de conexión incorrecta, fuente en CC inesperado o un pin ADC con voltaje fuera del rango del PSoC.

## Adquisición

- Con placa conectada, firmware abierto programado, y alimentación normal habilitada: preparar Rigol en CH1 + flanco ascendente, disparo SINGLE; ajustar ~50 ms/div, ~50 mV/div si las señales son pequeñas y centradas. Arrancar en escala mayor si existe incertidumbre de excursiones.
- En MATLAB, desde `01_Modelado_MATLAB`, ejecutar **`capturar_uart_monitor_lab7`**. A pesar del nombre, captura cualquier modo que emita la misma cabecera. Esperar «CAPTURA INICIADA» y pulsar SW3 una vez para reiniciar el PSoC, **sin reconectar USB con SW3 pulsado**.
- El programa espera 3000 ms tras arrancar, luego captura `N=256` muestras con `Ts=2 ms`. La orden es `u=0.050 V` desde `k=32` (t=64ms) hasta k=127 incluido (t=254ms); se desactiva en k=128 (t=256ms). La salida se lleva a cero al terminar (y ante cualquier bandera de fallo). La señal física en J5 no será exactamente 50 mV por cuantización y offset.
- Guardar captura UART cruda y CSV con fecha. Tras el evento, guardar el Rigol detenido mediante `Herramientas_Comunes/Rigol_y_UART/rigol_ds1202ze.py bundle --label lab7_01_abierto` o el lanzador del directorio.
- Verificar CSV: cabecera `modo=ABIERTO`, 256 filas deseables, flags 0, intervalos cercanos 2000 us, `u_solicitada_mV=50` durante el pulso y 0 fuera, `dac_pos>0` durante el escalón, sin saturación. Si aparecen flags, **no deshabilitar protecciones**: guardar registro y diagnosticar.
- El canal CH1 (J5) proporciona el **mando físico**, CH2 (J7) la salida real. El CSV de PSoC contiene `u_nominal_mV` (estimación a partir de códigos), no sustituye al CH1 físico.

## Magnitudes principales para el informe

De ambas señales en el osciloscopio, cuantificar:
`u_0` promedio antes del escalón; `u_{ss}` promedio durante la meseta; `y_0`; `y_{ss}`. Calcular en diferencias:
```
Delta_u = u_ss - u_0;
Delta_y = y_ss - y_0;
K_estatica_exp = Delta_y / Delta_u.
```
Nominal del esquema: `K_estatica = 1.01856`, `tau1 = 15 ms`, `tau2 = 1.5 ms`. También existe modelo identificado Lab5 de `tau_lenta ≈9.069 ms` y `tau_rapida ≈0.7744 ms`, distinto al nominal. Contrastar transitorio y registrar discrepancias; no ajustar artificialmente el modelo ni reutilizar ganancias sin verificar condiciones.

## Qué se mide después — Ensayos propios de observadores

Luego: predictor E1, predictor E2, actual E1, actual E2. Mantener `K`, `Nr`, `Ts` y referencia iguales y variar arquitectura/ganancia de observador. Capturar por UART `y_rel`, `xhat1`, `xhat2`, `innovacion`, `u_solicitada`, `u_nominal`, flags y CPU/intervalos; capturar simultáneamente J5/J7 con Rigol. Comparar sobrepasamiento, establecimiento, error estacionario y esfuerzo de control con MATLAB nominal y eventualmente modelo medido.

**Seguridad:** NO habilitar modos PREDICCION/ACTUAL con el modelo aún inválido o banderas de ADC; respetar enclavamientos del firmware.
