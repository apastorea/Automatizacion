# Laboratorio 5 - Desarrollo de los puntos 1 y 2

## 1. Alcance y criterio adoptado

El informe de referencia confirma que el enunciado se interpreta como un
diseño para seguimiento de escalón mediante síntesis directa de
Truxal-Ragazzini. Se adoptan cuatro casos: dos periodos de muestreo y, para
cada periodo, un diseño de tiempo mínimo con oscilación intermuestreo y un
diseño deadbeat que elimina el rizado determinista.

El diseño se realiza con el modelo nominal del circuito. El modelo identificado
del Laboratorio 4 se conserva como referencia para una validación de robustez
posterior; no se mezclan sus parámetros con los coeficientes nominales.

## 2. Punto 1 - Función de transferencia de la planta

Cada etapa inversora de primer orden tiene la forma

\[
G_i(s)=-\frac{R_f/R_{in}}{1+sR_fC}.
\]

Las dos inversiones se cancelan. Con

- \(R_5=150\,\text{k}\Omega\), \(R_6=47\,\text{k}\Omega\),
- \(R_1=15\,\text{k}\Omega\), \(R_2=47\,\text{k}\Omega\),
- \(C_1=C_3=100\,\text{nF}\),

se obtiene

\[
G_p(s)=\frac{(R_5/R_6)(R_1/R_2)}
{(1+sR_5C_1)(1+sR_1C_3)}
=\frac{4.5269353\times10^4}
{s^2+733.3333s+4.4444444\times10^4}.
\]

Los parámetros principales son:

- ganancia estática: \(K=1.0185604\);
- constantes de tiempo: \(15\,\text{ms}\) y \(1.5\,\text{ms}\);
- polos: \(-66.6667\) y \(-666.6667\,\text{rad/s}\);
- ancho de banda: \(65.8610\,\text{rad/s}=10.4821\,\text{Hz}\).

## 3. Punto 2 - Muestreo y síntesis directa

### 3.1 Selección de los periodos

La selección se realiza antes de discretizar, usando frecuencias de muestreo
de \(10f_B\) y \(30f_B\). Con un reloj de Timer de \(100\,\text{kHz}\), se
redondea a cuentas enteras:

| Caso | Criterio | \(T_s\) ideal | Cuentas | `Period` | \(T_s\) real | \(f_s\) |
|---|---:|---:|---:|---:|---:|---:|
| 1 | \(10f_B\) | 9.540064 ms | 954 | 953 | 9.540 ms | 104.8218 Hz |
| 2 | \(30f_B\) | 3.180021 ms | 318 | 317 | 3.180 ms | 314.4654 Hz |

El valor de `Period` supone el Timer contado desde `Period` hasta cero, es
decir, \(N=\text{Period}+1\) ciclos. Esto debe confirmarse en el componente
final del PSoC al medir el pin de diagnóstico o la telemetría temporal.

### 3.2 Diseño oscilatorio de tiempo mínimo

Para realimentación unitaria,

\[
F(z)=\frac{C(z)G(z)}{1+C(z)G(z)},\qquad
C(z)=\frac{F(z)}{G(z)[1-F(z)]}.
\]

Se fija

\[
F_o(z)=z^{-1}.
\]

La salida muestreada alcanza la referencia en una muestra, pero esta elección
no obliga a que el esfuerzo se vuelva constante. El controlador cancela el
cero estable de la planta discreta y deja una cola alternante en \(u[k]\), que
el ZOH transforma en oscilación física entre muestras.

### 3.3 Diseño deadbeat sin rizado determinista

Si

\[
G(z)=\frac{z^{-1}(b_1+b_2z^{-1})}
{1+a_1z^{-1}+a_2z^{-2}},
\]

se elige

\[
F_d(z)=\frac{z^{-1}(b_1+b_2z^{-1})}{b_1+b_2}.
\]

Así se conserva el cero estable de la planta en el lazo cerrado, se cumple
\(F_d(1)=1\) y

\[
\frac{U(z)}{R(z)}=\frac{F_d(z)}{G(z)}
=\frac{1+a_1z^{-1}+a_2z^{-2}}{b_1+b_2},
\]

por lo que, ante un escalón, \(u[k]\) se vuelve constante en tiempo finito.

## 4. Resultados nominales

Los coeficientes se expresan como

\[
C(z)=\frac{b_0+b_1z^{-1}+b_2z^{-2}}
{1+a_1z^{-1}+a_2z^{-2}},
\]

y se implementan mediante

\[
u[k]=-a_1u[k-1]-a_2u[k-2]
+b_0e[k]+b_1e[k-1]+b_2e[k-2].
\]

| \(T_s\) | Diseño | \(b_0\) | \(b_1\) | \(b_2\) | \(a_1\) | \(a_2\) |
|---:|---|---:|---:|---:|---:|---:|
| 9.540 ms | Oscilatorio | 2.383167101 | -1.265783898 | 0.002181877 | -0.859655305 | -0.140344695 |
| 9.540 ms | Deadbeat | 2.089865557 | -1.110001128 | 0.001913349 | -0.876927831 | -0.123072169 |
| 3.180 ms | Oscilatorio | 8.575438285 | -7.966550661 | 0.832686635 | -0.531669497 | -0.468330503 |
| 3.180 ms | Deadbeat | 5.840264345 | -5.425584120 | 0.567097553 | -0.681045581 | -0.318954419 |

Con un escalón físico común de \(0.100\,\text{V}\), los picos de esfuerzo son
0.2383, 0.2090, 0.8575 y 0.5840 V, respectivamente. El caso limitante es el
oscilatorio de 3.180 ms. Para un límite conservador de \(\pm1\,\text{V}\) y
10 % de margen, la amplitud máxima calculada es 0.10495 V; por eso se adopta
0.100 V como amplitud común para simulación, firmware y experimento.

## 5. Revisión crítica del informe de referencia

### Aspectos correctos y confirmados

- El modelo nominal y sus polos coinciden con el circuito del enunciado.
- La elección de \(T_s\) tiene un criterio explícito y se traduce a cuentas del
  Timer.
- Se diseñan los cuatro controladores pedidos.
- La respuesta se reconstruye entre muestras; no se evalúa únicamente en
  \(kT_s\).
- El deadbeat conserva el cero estable de la planta y hace constante el mando
  desde la segunda muestra.
- Las ecuaciones en diferencias coinciden numéricamente con el cálculo
  reproducido en MATLAB.

### Aspectos que la corrección del profesor deja sin validar

El informe compara simulación y experimento, pero no declara de forma
trazable una única amplitud física de escalón ni documenta la transformación
entre la referencia del código, la tensión en el circuito, la lectura cruda del
ADC y la señal mostrada. Por eso las tablas de error del esfuerzo de control no
pueden considerarse plenamente válidas aunque las tendencias sean razonables.

La mención inicial de un `ADC_SAR_Seq_1` no corresponde a este laboratorio.
Lab. 5 conserva el ADC SAR simple y la ruta analógica ya validados en Lab. 4.

## 6. Medidas incorporadas para evitar las observaciones

1. MATLAB usa una sola variable `reference_step_v`, actualmente 0.100 V, para
   la salida y para el esfuerzo de los cuatro casos.
2. El firmware usa exactamente el mismo valor en
   `LAB5_REFERENCE_STEP_VOLTS` y lo transmite en los metadatos UART.
3. La conversión heredada se documenta explícitamente como
   \(y=(V_{ADC}-V_{offset})/S_{ADC}\) y fue revalidada con la captura
   `lab5_calibracion_final_circuito_cerrado_v4_20261120_231219`.
4. Deben guardarse por separado datos crudos, datos calibrados y constantes de
   calibración; nunca reemplazar los crudos.
5. Una comparación MATLAB-experimento solo se realizará si coinciden amplitud,
   periodo de muestreo, controlador y unidades físicas.
6. Los diagramas de polos y ceros se exportan individualmente a 300 dpi, con
   círculo unitario, marcadores grandes y valores numéricos visibles.

## 7. Decisiones de implementación cerradas

Quedan razonablemente contestadas por el informe presentado y por la
devolución del profesor: la referencia es un escalón; se acepta el modelo
nominal; los periodos 9.540 y 3.180 ms son defendibles; el primer diseño usa
\(F_o=z^{-1}\); el rediseño deadbeat conserva el cero estable; se esperan los
cuatro controladores; y el análisis debe incluir el comportamiento
intermuestreo.

No se incorpora `ADC_SAR_Seq_1`: pertenece al laboratorio siguiente. Se
conservan el ADC SAR simple, su entrada en P0[2] y el esquema validado de Lab. 4.
El esfuerzo de control se mide externamente con CH1 en J5; la salida de planta
se registra con CH2 en J7 y también mediante el ADC del PSoC.

Se implementarán y ensayarán secuencialmente los cuatro controladores. El
enunciado exige diseñar ambos tipos para cada periodo y habla de
"configuraciones seleccionadas" en la implementación; el informe de referencia
presentó resultados experimentales para los cuatro y la devolución del profesor
no señaló ninguna omisión ni exceso de alcance. Por tanto, implementar los
cuatro es la interpretación con menor riesgo y permite realizar todas las
comparaciones pedidas.

La amplitud no debería dejarse como pregunta abierta: se debe declarar y usar
el mismo valor físico en firmware, simulación y procesamiento. Si el profesor
prefiere otra amplitud, se cambia una sola constante y se regeneran todas las
figuras y métricas.
