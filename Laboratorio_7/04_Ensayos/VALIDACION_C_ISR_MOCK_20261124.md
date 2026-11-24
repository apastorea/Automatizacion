# Lab7 — Verificación fuera de hardware del Predictor E1 (24-11-2026)

## Ubicación de fuentes resuelta

La salida de PowerShell del usuario confirma que `Preparacion_E1_Alternativo/Lab7_E1_Alternativo.cydsn/Lab7_E1_Alternativo.cyprj` declara:
- `main.c` con atributo `persistent="..\\Propuesta\\main.c"`.
- `lab7_config.h` con atributo `persistent="..\\Propuesta\\lab7_config.h"`.
- `lab7_estimadores.c` con `persistent="lab7_estimadores.c"`.

Por eso no están dentro de `.cydsn`; **son archivos enlazados**. No están enlazados al proyecto Lab7 original. Los cambios al header de `Propuesta` modifican la configuración usada al compilar E1, y no deben confundirse con el respaldo original.

## Comprobaciones realizadas aquí

Se compiló y ejecutó con GCC nativo:
1. El núcleo portátil C del observador: cálculo inicial para referencia 50 mV, mando ideal 54,737 mV, DAC nominal ~61,48 mV (código 4), memoria del predictor y contador de saturación.
2. Una copia de `Propuesta/main.c` como unidad de prueba de ISR con periféricos simulados (stubs, no PSoC). Se ejercitaron 20 aserciones: 32 ciclos pretrigger, DAC a cero, paso inicial del predictor, lectura ADC inválida, saturación de controlador positiva/negativa, valor nominal DAC excesivo simulado, intervalo 2500 µs y carga CPU >2000 µs.

**Resultado: pruebas sobre núcleo y 20 verificaciones de la ISR simulada superadas**; código GCC con advertencias como errores y sanitizadores ASan/UBSan.

## Limitaciones técnicas importantes

- No se probaron físicamente los circuitos ni se ejecutó en la placa; ADC/DAC, temporizadores y UART fueron simulados. No se garantiza comportamiento real en interrupciones ni precisión de calibración.
- La comprobación `F_CPU` se evalúa después de llamar a la función que escribe el DAC; al detectar exceso, se vuelve a cero, pero hubo una escritura inicial durante la ISR. Análogamente, la verificación posterior del valor nominal del DAC ocurre después de la escritura al DAC. El límite solicitado conservador (+0.107 V / -0.115 V) debería evitar que la HAL normal exceda ±0.120 V, pero no demuestra bloqueo previo ante fallos arbitrarios de la HAL.
- El programa comienza a ejecutar adquisición tras aproximadamente **3 segundos de cualquier reset/programación**; no es necesario pulsar SW3 para la primera ejecución. Preparar banco y observación antes de programar, o programar con etapa analógica sin energizar y repetir después de energizar con SW3.
- El repositorio conserva la `Propuesta/lab7_config.h` en MONITOR/autoridades 0 por seguridad; el header local editado para compilar Predictor puede diferir. Los test usaron copia temporal del header en PREDICCION/autoridades 1; no cambiaron la versión por defecto.

## Próximo paso

Verificar condiciones físicas (fuente y masas, J5 y J7, cables a ADC, 10X/DC), elegir y confirmar proyecto correcto en PSoC Creator, supervisar el primer arranque, registrar CH1/CH2 + UART a través de `Laboratorio_7/04_Ensayos/capturar_lab7_sincronizado.cmd` seleccionando `pred_E1`. Revisar `modo=PREDICCION`, 256 muestras, flags=0, códigos DAC, y formas de onda antes de calificar el ensayo.
