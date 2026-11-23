/*
 * lab4_experiment.h - Seleccion segura y reproducible del ensayo.
 *
 * El proyecto arranca en el modo de calibracion para tester solicitado.
 * Este modo solo aplica niveles limitados, los mantiene para una lectura
 * manual y retorna automaticamente a cero. Para los ensayos dinamicos se
 * debe verificar primero masa comun, offset, escala y polaridad.
 */
#ifndef LAB4_EXPERIMENT_H
#define LAB4_EXPERIMENT_H

#define LAB4_MODE                  LAB4_MODE_FREQUENCY_RESPONSE
#define LAB4_REFERENCE_TYPE        LAB4_REFERENCE_STEP
#define LAB4_CALIBRATED            (1u)
#define LAB4_DMM_CALIBRATION_ARMED (1u)
#define LAB4_DMM_START_DELAY_MS    (5000u)
#define LAB4_DMM_HOLD_MS           (12000u)
#define LAB4_DMM_ADC_SAMPLES       (64u)
#define LAB4_TS_COUNTS             (100u) /* 100 x 10 us = 1 ms. */
#define LAB4_SAMPLE_COUNT          (512u)
#define LAB4_PRETRIGGER_SAMPLES    (32u)
#define LAB4_START_DELAY_MS        (3000u)
#define LAB4_STEP_VOLTS            (0.05f)
#define LAB4_RAMP_SLOPE_VOLTS_S    (1.25f)
#define LAB4_DELAY_SAMPLES          (0u) /* B(z)=1; no retardo completo. */

/* Barrido senoidal coherente para medir L(jw)=Y(jw)/E(jw) sin abrir el
 * lazo. Cada frecuencia entera se observa durante dos segundos completos;
 * asi la proyeccion sincronica rechaza la componente continua sin ventana. */
#define LAB4_FR_AMPLITUDE_VOLTS     (0.20f)
#define LAB4_FR_SETTLE_SAMPLES      (300u)
#define LAB4_FR_MEASURE_SAMPLES     (2000u)

#endif
