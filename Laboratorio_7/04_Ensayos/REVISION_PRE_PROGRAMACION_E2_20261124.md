# Laboratorio 7 — Revisión E2 previa al primer ensayo físico

**Entrada:** captura de PSoC Creator del usuario de 24/11/2026 03:25:10: `Build Succeeded`, memoria Flash 9.936 bytes (3,8%), SRAM 14.905 bytes (22,7%), stack 2.048, heap 128.

## Ganancias y selección verificadas en el repositorio

En `Preparacion_E1_Alternativo/Propuesta/main.c` las ramas `LAB7_ESTIMADOR_VARIANTE == 2u` usan:
- Predictor E2: L = [-2.14809283, +0.73877046].
- Actual E2: L = [-2.45447706, +0.78326191].
- K = [2.15692217, 6.87132640], Nr = 1.09474803 y A,B,C nominales comunes.

**Importante:** la copia versionada de `Propuesta/lab7_config.h` permanece por defecto en MONITOR y las autorizaciones 0. El usuario editó localmente la copia enlazada para compilar E2; confirmar su modo y variante antes de programar.

## Verificación C portable (no hardware)

Se compiló y ejecutó bajo Linux GCC con `-std=c11 -Wall -Wextra -Werror -fsanitize=address,undefined` una reproducción del núcleo fuente `lab7_estimadores.c` y sus tipos/constantes E2. Se superaron **30 comprobaciones** entre Predictor y Actual, cubriendo inicialización, petición ideal de 54.7374 mV, cuantización nominal +4 = 61.4818 mV, diferencia aplicada/pedida, detección de saturación positiva y negativa, y aplicación diferenciada de la innovación. Este ensayo portable **no valida ISR, HAL ni timing real**, ni ejecuta el binario específico ARM.

Revisión estática de la ISR común al E1 ya medido:
- `estado.saturaciones` aumenta cuando la ley de control solicita fuera de [-0.115, 0.107]V.
- La ISR detecta ese cambio y ordena `u_solicitada_V=0` antes de llamar a HAL.
- Se detectan ADC fuera de rango, salida no finita, salida >0.5V relativa e intervalo fuera de tolerancia.
- `detener_seguro()` detiene timer y pone la salida a cero cuando flags son no nulos.
- **Límite pendiente:** `F_CPU` y la validación del valor nominal de `u_nominal_V` se ejecutan después de llamar a `Lab5HardwareWriteOutput`; la salida puede haber sido escrita transitoriamente antes del corte. No asumir protección absoluta frente a fallas de HAL.

## Captura mejorada

Nuevo lanzador `Laboratorio_7/04_Ensayos/capturar_lab7_E2_flanco_fisico.cmd`: obliga a elegir `pred_E2` o `actual_E2`, configura modo de disparo físico CH1, flanco ascendente a **35 mV absolutos** (partiendo de reposo J5 ~15mV y meseta ~60mV en E1) y respaldo TFOR si no dispara. El umbral se deberá cambiar si la tensión base de J5 difiere sustancialmente; TFOR no equivale a disparo físico.

## Condiciones para primera medida física E2

1. Conservar firmware y datos E1. Confirmar en PSoC Creator el proyecto correcto, `LAB7_MODO_PREDICCION`, `LAB7_ESTIMADOR_VARIANTE (2u)` y que las autorizaciones reflejen los ensayos verificados.
2. Fuente DC de PCB con tensión y polaridad comprobada, limitación de corriente según el montaje validado; Rigol CH1 J5, CH2 J7, sondas 10X/ACOP DC y masas cortas y comunes.
3. Supervisar físicamente la alimentación: el firmware arranca la adquisición aproximadamente 3s después de programar/reset. Interrumpir si hay sobrecorriente, excursión anormal o oscilación inesperada.
4. Programar PSoC solo en condiciones seguras y confirmar `Finished Programming`; después abrir CMD E2, al mostrar LISTO pulsar SW3 una vez y observar el transitorio.
5. Guardar archivos crudos y verificar `modo=PREDICCION`, `diseno_E2=ORIG_Z020_J010`, 256 filas si no hay fallos, flags=0, periodo ~2ms, códigos DAC y tensión nominal dentro de rango. Si surge bandera, no repetir sin análisis.

El resultado de compilación es evidencia de construcción, **no** de programación ni de estabilidad física.
