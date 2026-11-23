# Revalidación de instrumentación Lab7

**Equipo:** PSoC 5LP, RIGOL DS1202Z-E, fuente de alimentación y planta analógica de segundo orden. Usar las conexiones del plano de Lab7; los puntos J5/J7 son **antecedentes** de Lab5, no una identificación automática de los nuevos nodos.

1. **Inspección sin alimentación.** Verificar masas, jumpers, valores R/C, polaridad del suministro y ausencia de corto. Las pinzas GND de ambas sondas del Rigol comparten potencial y NO pueden conectarse a rieles activos.
2. **Medir reposo** con el algoritmo deshabilitado: registrar el mando real, la salida y el ADC; al menos 20 promedios/lecturas, guardando la magnitud cruda y su dispersión.
3. **Verificar actuador bipolar** usando pequeños escalones positivos y negativos dentro del rango verificado. Comparar mando solicitado, código DAC y tensión física. Ajustar pendiente/offset de cada rama por separado.
4. **Verificar ADC** con al menos cinco niveles en el intervalo previsto. Registrar V_ADC, V_salida planta, códigos y aplicar regresión lineal; anotar residuos y RMSE.
5. **Verificar reloj y temporización** midiendo el pin diagnóstico de la ISR y el periodo real; comprobar que el peor caso de adquisición+cálculo+actualización es menor que Ts con margen.
6. **Ensayo en lazo abierto** con señal de amplitud reducida; contrastar respuesta real con el modelo antes de activar realimentación.
7. **Activación gradual de lazo**: controlar límites ±V antes de cada actualización, mantener el modo seguro disponible y detener el ensayo por saturación repetida o fallas ADC.

Registrar en `04_Ensayos/AAAA-MM-DD_identificador/` los archivos `chan1_mando.csv`, `chan2_salida.csv`, `psoc_uart.csv`, `metadata.json`, `pantalla.png` y `calibracion.csv`. No editar ni normalizar los archivos crudos. Escribir los ajustes en una tabla aparte. Un `metadata.json` de ejemplo se proporciona en la carpeta Ensayos.

## Datos históricos de comparación (no aplicar sin verificar)

`Lab5` documenta: ADC offset = 2.353802067 V, escala = 0.210251951 V/V; ganancias DAC 3.842612 y 2.640105691; en J5 se midió aproximadamente +17.21 mV de offset. No considerarlos exactos para el montaje de Lab7.
