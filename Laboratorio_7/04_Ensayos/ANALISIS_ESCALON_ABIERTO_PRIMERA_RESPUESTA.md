# Lectura de la respuesta experimental en lazo abierto (Lab7)

**Evidencia del usuario:** captura MATLAB de 256 muestras y figura con la respuesta a un pulso solicitado de 50mV, con mando DAC nominal de ~46.1mV entre 64 y 256ms; la salida ADC convertida sube de ~5mV a ~44mV y regresa a ~1mV.

La prueba ya demuestra un pulso y una respuesta coherente cualitativamente con la de un sistema estable y de respuesta no instantánea. La diferencia aproximada de salida durante el pulso es `44-5 ≈39mV`, por lo que `K_aparente ≈39/46.1=0.85 V/V`. Es solo una estimación visual: la tensión realmente aplicada a J5 aún no fue medida para este mismo pulso. **No asignar K aparente como ganancia de planta física definitiva.**

Es posible que escalones de ~5mV en `y_rel_mV` se deban a la resolución del ADC después de deshacer la amplificación de escala ~0.21025 V/V del acondicionador. Una cuenta ADC equivale al orden de 5–6mV referidos a la planta. Evitar concluir que pequeñas fluctuaciones son oscilaciones de control.

Se agrega `01_Modelado_MATLAB/analizar_escalon_abierto_lab7.m`: localiza el CSV ABIERTO reciente, calcula estadísticos robustos en el preescalón y meseta, dibuja respuesta experimental con baseline corregido y las predicciones del modelo nominal (15ms, 1.5ms) y del modelo identificado Lab5 (9.06915ms, 0.774399ms), y exporta PNG + resumen CSV. No altera ningún firmware, calibración ni alimentación.

**Siguiente medición necesaria, no es barrido de calibración:** repetir el mismo escalón con Rigol CH1 en J5 y CH2 en J7, ambas masas en GND, para comparar `Delta_y/Delta_u` usando tensiones realmente medidas. Después analizar e implementar predicción E1 si la respuesta y la temporización resultan compatibles, sin desactivar enclavamientos de seguridad.
