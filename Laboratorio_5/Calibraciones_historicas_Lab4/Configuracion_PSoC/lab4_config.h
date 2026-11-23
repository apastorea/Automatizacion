/*
 * lab4_config.h - Configuracion comun del Laboratorio 4.
 *
 * Clock_1 opera a 100 kHz: una cuenta equivale a 10 us. Los factores de
 * calibracion se heredan del Laboratorio 3 solo como punto de partida y
 * deben comprobarse de nuevo antes de habilitar la salida de control.
 */
#ifndef LAB4_CONFIG_H
#define LAB4_CONFIG_H

#define LAB4_MODE_MONITOR       (0u)
#define LAB4_MODE_OPEN_LOOP     (1u)
#define LAB4_MODE_CONTROL_BODE  (2u)
#define LAB4_MODE_DMM_CALIBRATION (3u)
#define LAB4_MODE_FREQUENCY_RESPONSE (4u)

#define LAB4_REFERENCE_STEP     (0u)
#define LAB4_REFERENCE_RAMP     (1u)

#include "lab4_experiment.h"

#define LAB4_TS_US              (LAB4_TS_COUNTS * 10u)
#define LAB4_TS_SECONDS         ((float)LAB4_TS_US * 1.0e-6f)
#define LAB4_TS_TOLERANCE_US    (LAB4_TS_US / 10u)

/* C(z) = (b0 + b1 z^-1 + b2 z^-2) /
 *        (1 + a1 z^-1 + a2 z^-2)
 * Coeficientes obtenidos por el diseno Bode en el plano w y la
 * transformacion bilineal inversa, con Ts = 1 ms. */
#define LAB4_DESIGN_REVISION    (2u)
#define LAB4_BODE_B0            (0.427100239f)
#define LAB4_BODE_B1            (0.033543583f)
#define LAB4_BODE_B2            (-0.393556656f)
#define LAB4_BODE_A1            (-1.606872382f)
#define LAB4_BODE_A2            (0.606872382f)

/* Calibracion del Laboratorio 4 obtenida el 17/11/2026 con la cadena
 * J8--J5, J10--J6 y J7--J4 cerrada. El ajuste sincronizado de cinco puntos
 * RIGOL--ADC dio Vadc = 2.353696 + 0.209825*y, con error maximo de ajuste
 * 0.224 mV. */
#define LAB4_ADC_OFFSET_VOLTS            (2.353802067f)
#define LAB4_ADC_VOLTS_PER_PLANT_VOLT    (0.210251951f)
#define LAB4_DAC_POSITIVE_GAIN           (3.842612000f)
#define LAB4_DAC_NEGATIVE_GAIN           (2.640105691f)
#define LAB4_DAC_VOLTS_PER_COUNT         (0.004f)
#define LAB4_OUTPUT_MAX_VOLTS             (1.0f)
#define LAB4_OUTPUT_MIN_VOLTS             (-1.0f)

#if LAB4_MODE > LAB4_MODE_FREQUENCY_RESPONSE
#error LAB4_MODE invalido.
#endif
#if LAB4_REFERENCE_TYPE > LAB4_REFERENCE_RAMP
#error LAB4_REFERENCE_TYPE invalido.
#endif
#if LAB4_TS_COUNTS != 100u
#error El enunciado del Laboratorio 4 exige Ts = 1 ms (100 cuentas de 10 us).
#endif
#if LAB4_DELAY_SAMPLES != 0u
#error El firmware nominal implementa B(z)=1; validar y redisenar antes de incluir z^-1.
#endif
#if LAB4_SAMPLE_COUNT < 64u || LAB4_SAMPLE_COUNT > 1024u
#error La captura debe contener entre 64 y 1024 muestras.
#endif
#if LAB4_PRETRIGGER_SAMPLES < 8u || LAB4_PRETRIGGER_SAMPLES >= LAB4_SAMPLE_COUNT
#error Longitud de pretrigger invalida.
#endif
#if LAB4_MODE != LAB4_MODE_MONITOR && \
    LAB4_MODE != LAB4_MODE_DMM_CALIBRATION && !LAB4_CALIBRATED
#error Verificar la calibracion analogica antes de habilitar el control.
#endif
#if LAB4_MODE == LAB4_MODE_DMM_CALIBRATION && !LAB4_DMM_CALIBRATION_ARMED
#error Confirmar masa comun y habilitar LAB4_DMM_CALIBRATION_ARMED.
#endif
#if LAB4_DMM_HOLD_MS < 10000u || LAB4_DMM_HOLD_MS > 60000u
#error Cada nivel para tester debe mantenerse entre 10 y 60 segundos.
#endif
#if LAB4_DMM_START_DELAY_MS < 3000u || LAB4_DMM_START_DELAY_MS > 30000u
#error El retardo inicial para tester debe estar entre 3 y 30 segundos.
#endif

#endif
