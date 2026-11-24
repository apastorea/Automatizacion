# Laboratorio 7 — Evaluación de estabilidad antes de habilitar lazo cerrado

## Punto de partida comprobado
- Se obtuvo una captura de lazo ABIERTO con 256 muestras a ~2 ms y `flags=0`, en la PCB original del Lab5.
- Rigol DS1202Z-E: CH1=J5 y CH2=J7; ganancia incremental aproximadamente 0.983–0.984.
- El firmware plantilla mantiene enclavamientos en `lab7_config.h` para impedir control cerrado hasta autorización explícita.
- Se verificó mediante GCC la compilación y un test algebraico del núcleo `lab7_estimadores.c` (no prueba de hardware).

## Nueva comprobación numérica independiente (2026-11-24)
Modelo nominal usado por `modelo_lab7.m`: Ts=0.002s, tau1=0.015s, tau2=0.0015s, K=1.01856, C=[0,1]. Modelo identificado en Lab5 usado como comparación: K5=1.002941, tau1=0.00906915s, tau2=0.000774399s.

Las matrices ampliadas del control con estimador deben incluir la planta ACTUAL y las matrices de diseño NOMINALES, no solo comprobar `eig(A-LC)` y `eig(A-BK)` individualmente.

Si `z=[x_planta; xhat_mem]`:
- Predictor: `Mpred=[Ap,-Bp*K; Lp*Cp,A-B*K-Lp*C]`
- Actual: `E=I-La*C; Mact=[Ap-Bp*K*La*Cp,-Bp*K*E; (A-B*K)*La*Cp,(A-B*K)*E]`

Se obtuvo con Python/SciPy (cálculo numérico independiente, pendiente reproducción en MATLAB):

| Diseño | rho nominal | rho identificado Lab5 | Diagnóstico lineal |
|---|---:|---:|---|
| Predicción E1: 0.4±j0.25 | 0.838 | 0.911 | estable |
| Actual E1: 0.4±j0.25 | 0.838 | **1.049** | **NO estable** |
| Predicción E2: 0.2±j0.1 | 0.838 | 0.829 | estable |
| Actual E2: 0.2±j0.1 | 0.838 | 0.825 | estable |

Interpretación: bajo la transferencia identificada de Lab5, Actual E1 no cumple radio espectral <1. No afirmar que el circuito oscilará necesariamente: faltan efectos no lineales, cuantización, saturación, variabilidad de componentes y validación de la identificación. **NO habilitar Actual E1 físicamente con estos coeficientes.**

El script `evaluar_robustez_observadores_lab7.m` reproduce este cálculo y exporta gráfico y CSV. `simular_no_ideal_observadores_lab7.m` añade cuantización ADC/DAC y ruido hipotético (0 y 10mV RMS) para explorar control no ideal; ese ruido no es una medición demostrada del ADC.

## Alternativas de polos del observador
Sin modificar el diseño publicado, se evaluaron opciones alternativas de polos E1 para **ambas** arquitecturas, contra la misma planta identificada Lab5:

| Polos E1 propuestos | rho predicción | rho actual |
|---|---:|---:|
| 0.40±j0.25 (original) | 0.911 | **1.049** |
| 0.35±j0.10 | 0.855 | 0.874 |
| 0.30±j0.10 | 0.841 | 0.840 |
| 0.25±j0.10 | 0.833 | 0.825 |
| 0.20±j0.10 (E2 original) | 0.829 | 0.825 |

`explorar_polos_E1_robustos_lab7.m` permite reproducir esta tabla. Los polos 0.35±j0.10 son una alternativa de diseño E1 a evaluar; no están incorporados en las cuatro simulaciones previas ni en el firmware y **no deben mezclarse** con las cifras anteriores sin regenerarlas. Su estabilidad lineal tampoco demuestra robustez absoluta frente al ruido.

## Verificaciones obligatorias antes de activar Predictor E1
1. Ejecutar desde MATLAB: `auditar_pre_cerrado_lab7`; `evaluar_robustez_observadores_lab7`; `simular_no_ideal_observadores_lab7`.
2. Verificar que las matrices PSoC compiladas coinciden con las de MATLAB. `lab7_config.h` puede haber sido modificado localmente y no necesariamente coincide con la plantilla original.
3. Confirmar alimentación analógica (+10/-10 V, polaridades correctas), J8–J5, J9–P0[2], masas comunes, CH1 J5/CH2 J7 y ausencia de conexión flotante.
4. Control de software pedido a ±0.120V; el DAC positivo cuantizado tiene paso nominal ~15.37mV por código y podría redondear el mando aplicado ligeramente por encima de ±0.120V. Revisar el límite físico por código y decidir si exige modificación antes de cerrar.
5. El ensayo ABIERTO de 50mV fue válido, pero no demuestra funcionamiento con realimentación. Para el primer ensayo cerrado, usar referencia 50mV, captura sincronizada de UART+Rigol, y comprobar flags, saturaciones y esfuerzo.
6. Mantener retorno seguro a modo MONITOR y cero DAC en caso de error. No habilitar control cerrado por automatismo ni desactivar protecciones.
7. La simulación MATLAB previa de cuatro casos usa `x_estimado0=[0.02;-0.01]` y referencia desde 20ms; firmware usa estados iniciales nulos y referencia a partir de k32 (64ms). Para comparación justa de la prueba física, usar simulación alineada con tiempos y condiciones iniciales de firmware.

## Próximo orden
(A) Auditoría y robustez offline; (B) verificar en MATLAB el posible problema de Actual E1; (C) si se confirma, rediseñar E1 y regenerar ganancias, simulaciones y documentación; (D) evaluar Predictor E1 físico mediante un procedimiento separado con protecciones. No se considera completado el ensayo con estimador hasta obtener UART e imagen/CSV del Rigol.
