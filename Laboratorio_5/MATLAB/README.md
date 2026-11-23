# Laboratorio 5 - MATLAB

## Puntos 1 y 2

Ejecutar `lab5_puntos_1_2.m` con Control System Toolbox. El script obtiene el
modelo nominal, selecciona dos periodos de muestreo, diseña los cuatro
controladores de síntesis directa y exporta resultados en
`resultados_puntos_1_2`.

La variable `reference_step_v` es la amplitud física común para las gráficas de
salida y esfuerzo. Debe coincidir con la referencia realmente programada en el
PSoC. La calibración heredada del Laboratorio 4 fue revalidada con el cableado
definitivo y queda identificada como `LAB5_J5_J7_20261120_231219`.

Archivos principales generados:

- `resumen.txt`: modelo, muestreo, ecuaciones en diferencias y métricas.
- `muestreo.csv`: trazabilidad entre criterio, `Ts` ideal, cuentas y `Period`.
- `coeficientes_controladores.csv`: coeficientes listos para el firmware.
- `metadatos_ensayo.csv`: amplitud, límites y calibración utilizada.
- `resumen_controladores.csv`: indicadores simulados con unidades explícitas.
- Figuras de respuesta y diagramas de polos y ceros a 300 dpi.

Los resultados conservan por separado las tensiones crudas, las tensiones
corregidas por offset y la amplitud cuantizada realmente aplicada. No se debe
normalizar una captura experimental sin declararlo explícitamente.

## Trazabilidad de las capturas del 20/11/2026

Las carpetas `lab5_calibracion_dac_20261120_223736` y
`lab5_calibracion_integridad_20261120_224421` se conservan como diagnóstico,
pero no son datos válidos para el informe: la primera se obtuvo con J10--J6
abierto y la segunda no mostró excursión física en J5 pese a que la telemetría
registró los códigos DAC previstos. No deben emplearse para ajustar ganancias
ni para comparar el esfuerzo de control.

## Diagnóstico bipolar aislado en J8 (20/11/2026)

Con J10--J6 conectado, J8--J5 abierto y CH1 directamente en J8, se programaron
niveles estáticos para verificar por separado el generador bipolar y su
acondicionador. Los promedios medidos fueron:

- salida solicitada `+0,200 V`: `+0,21506 V`;
- salida solicitada `-0,200 V`: `-0,18220 V`;
- modo `MONITOR` (salida solicitada nula): `+0,01744 V`.

Al restar el nivel de reposo, las excursiones son aproximadamente `+0,19762 V`
y `-0,19964 V`. Por tanto, ambas ramas DAC y el acondicionamiento bipolar son
coherentes con la ganancia heredada; la diferencia absoluta observada se debe
principalmente a un offset positivo de unos `17 mV`. Estas mediciones aisladas
validan la integridad del actuador, pero no sustituyen la calibración final con
J8--J5 conectado ni autorizan normalizar u ocultar el offset en las
comparaciones MATLAB--experimento.

Datos válidos del diagnóstico:

- `lab5_diagnostico_J8_pos200mV_forzado_20261120_225840`;
- `lab5_diagnostico_J8_neg200mV_forzado_20261120_230124`;
- `lab5_diagnostico_J8_monitor_cero_20261120_230221`.

## Calibración final con J8--J5 conectado

La captura válida es
`lab5_calibracion_final_circuito_cerrado_v4_20261120_231219`. CH1 se midió en
J5 y CH2 en J7. La secuencia incluyó cero, `+50 mV`, `+100 mV`, cero,
`-50 mV`, `-100 mV` y retorno a cero. Los 256 registros del PSoC terminaron
con `flags = 0` y `Ts = 9,540 ms`.

Resultados del ajuste:

- offset crudo de J5: `17,209 mV`;
- relación entre J5 crudo y mando cuantizado: pendiente `0,98171 V/V` e
  intercepto `17,551 mV`;
- RMSE del ajuste del actuador: `0,967 mV`;
- relación J7/lectura calculada desde ADC: pendiente `1,01699 V/V` e
  intercepto `0,081 mV`;
- RMSE de la lectura: `3,374 mV`.

Los archivos `resumen_niveles.csv`, `ajustes_calibracion.csv` y
`calibracion_bipolar.png` fueron generados por
`lab5_analizar_calibracion_final.m`. Las capturas `v2` y `v3` se conservan
únicamente como diagnóstico: el RIGOL fue disparado por el transitorio de
reinicio y registró el reposo. No deben aparecer como resultados válidos en el
informe.

## Primera prueba de control TS1 deadbeat (diagnóstico)

La carpeta `lab5_control_TS1_deadbeat_20261121_085950` se conserva solamente
para diagnosticar la implementación y no constituye una comparación
MATLAB--experimento válida. La captura del osciloscopio quedó en el nivel de
reposo porque el disparo ocurrió durante el transitorio de reinicio, mientras
que la telemetría UART mostró oscilación y saturación: el mando aplicado
alcanzó aproximadamente `-1,003 V` y `+0,999 V`, la salida medida recorrió de
`-32 mV` a `216 mV` y 85 muestras indicaron saturación (`flags = 2`).

Antes de repetir el control se debe revalidar la respuesta en lazo abierto con
la secuencia bipolar de baja amplitud. Esta captura no debe incluirse como
resultado del controlador ni usarse para calcular métricas de desempeño.

## Revalidación posterior al primer control (21/11/2026)

La captura `lab5_revalidacion_post_control_20261121_101459` confirmó nuevamente
la integridad del camino J8--J5--planta--J7. La salida J7 respondió una muestra
después del escalón aplicado en J5, con `Ts = 9,540 ms` y sin banderas de
fallo. El ajuste obtuvo pendiente J5/mando aplicado `0,99852 V/V` (RMSE
`0,641 mV`) y pendiente J7/lectura ADC `1,0233 V/V` (RMSE `2,932 mV`).

Esto descarta un retardo permanente del firmware o de la planta: la falta de
respuesta inmediata en la primera prueba de control correspondió a una
condición física transitoria de aquella captura. Como protección adicional,
desde esta revalidación el firmware detiene el temporizador y lleva la salida
a cero en la primera muestra que indique saturación.

## Control TS1 deadbeat válido (21/11/2026)

La captura válida es `lab5_control_TS1_deadbeat_final_20261121_120313`. Se
aplicó el mismo escalón de `100 mV` empleado por la simulación, sin
normalización ni corrección adicional de offset. Las 256 muestras terminaron
con `flags = 0`; el esfuerzo aplicado máximo fue `184 mV`, la salida alcanzó
`124 mV` y su promedio final fue `99,984 mV`. La oscilación final pico a pico
fue `16 mV`, asociada a la cuantización del ADC y del actuador.

`lab5_analizar_control_experimental.m` generó las trazas alineadas, las
métricas y dos figuras: una vista completa y otra ampliada a los primeros
`350 ms`. La simulación usa referencia absoluta de `100 mV` y condición
inicial experimental `y(0) = 10,812 mV`; por ello el escalón equivalente en
variables de desviación es `89,188 mV`. Los RMSE obtenidos fueron `7,878 mV`
para la salida y `15,706 mV` para el esfuerzo aplicado.

El RIGOL fue detenido de forma temporizada con `:TFOR` a los `3,15 s` del
encabezado, no mediante normalización ni edición de la señal. Esta decisión se
registra en `metadata.json` con `triggerWasForced = true`.

## Control TS1 oscilatorio válido (21/11/2026)

La captura válida es `lab5_control_TS1_oscillatory_final_20261121_165538`.
También emplea una referencia común de `100 mV`, sin normalización ni
corrección adicional de offset. Se registraron 256 muestras con
`Ts = 9,540 ms`, `flags = 0` y tiempo máximo de ejecución de `66 us`. El mando
aplicado recorrió de `-21 mV` a `231 mV`; la salida alcanzó `141 mV`, convergió
a un promedio de `99,734 mV` y presentó una oscilación final pico a pico de
`16 mV`.

La comparación MATLAB--experimento utiliza la condición inicial medida
`y(0) = -3,594 mV`, equivalente a un escalón de desviación de `103,594 mV`
hasta la referencia absoluta común. El RMSE fue `8,037 mV` para la salida y
`17,714 mV` para el esfuerzo aplicado. El tiempo de establecimiento dentro de
la banda del 10 % fue `124,02 ms`. La captura física del RIGOL muestra la
alternancia amortiguada esperada y el disparo temporizado queda documentado en
`metadata.json` con `triggerWasForced = true`.

## Control TS2 deadbeat válido (21/11/2026)

La captura válida es `lab5_control_TS2_deadbeat_final_20261121_170023`. La
referencia experimental y la simulada son de `100 mV`, sin normalización ni
corrección adicional de offset. Las 256 muestras presentan `Ts = 3,180 ms`,
`flags = 0` y un tiempo máximo de ejecución de `66 us`. El mando aplicado
recorrió de `-317 mV` a `584 mV`; la salida alcanzó `130 mV`, convergió a un
promedio de `99,828 mV` y tuvo una oscilación final pico a pico de `16 mV`.

La simulación toma la condición inicial medida `y(0) = 0,313 mV`, por lo que
el escalón equivalente en variables de desviación es `99,688 mV`. Los RMSE
fueron `7,048 mV` para la salida y `54,761 mV` para el esfuerzo aplicado. El
tiempo de establecimiento experimental dentro de la banda del 10 % fue
`178,08 ms`. Para mantener legibles los transitorios rápidos de TS2, la figura
ampliada cubre los primeros `120 ms`; la vista completa se conserva por
separado.

## TS2 oscilatorio: descarte experimental por saturación (21/11/2026)

El diseño TS2 oscilatorio se ensayó primero con el escalón nominal de `100 mV`
en `lab5_control_TS2_oscillatory_final_20261121_170404`. En la segunda muestra
de control solicitó `-1,191 V`; el actuador quedó limitado a `-1,003 V`, se
activó `flags = 2` y la protección detuvo el temporizador. La captura contiene
34 muestras y se conserva únicamente como diagnóstico.

Para comprobar si la causa era solo la amplitud, se repitió con `50 mV` en
`lab5_control_TS2_oscillatory_50mV_final_20261121_170616`, usando esa misma
referencia en el experimento y en la simulación prevista. También resultó no
válido: en la tercera muestra solicitó `+1,308 V`, se aplicaron `+0,999 V` y se
activó nuevamente `flags = 2`. Esto evidencia falta de robustez del controlador
de tiempo mínimo para `Ts = 3,180 ms` frente al modelo físico, los offsets y la
cuantización; no corresponde normalizar estas señales ni presentarlas como una
comparación MATLAB--experimento válida. Las configuraciones experimentales
seleccionadas para el informe son, por tanto, TS1 deadbeat, TS1 oscilatorio y
TS2 deadbeat.

El archivo `lab5_experiment.h` se deja finalmente en modo `MONITOR`, con salida
en cero y referencia nominal restaurada a `100 mV`.
