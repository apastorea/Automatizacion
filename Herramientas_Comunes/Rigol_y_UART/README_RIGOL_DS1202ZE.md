# Instrumentación RIGOL DS1202Z-E

Esta carpeta contiene la interfaz local para adquirir datos del osciloscopio
RIGOL DS1202Z-E mediante USB-TMC y SCPI.

## Estado verificado

- Modelo: DS1202Z-E.
- Firmware detectado: 00.06.04.
- Interfaz: USB-TMC/VISA.
- Recurso detectado automáticamente por fabricante RIGOL.
- Dependencia Python: `pyvisa`.

## Conexión segura de las sondas

- Usar sondas en posición 10X y configurar 10X en el menú de cada canal.
- Usar acoplamiento DC para las mediciones de control.
- Conectar todas las pinzas de masa únicamente al GND común del circuito.
- Las masas BNC de los canales están unidas internamente y referidas a tierra.
- No conectar una pinza de masa a VCC, VEE ni a un nodo de señal.

## Comandos

Ejecutar desde la carpeta `Laboratorio 4`.

Identificación y mediciones actuales:

```powershell
python .\Instrumentacion_RIGOL\rigol_ds1202ze.py info
```

Captura de pantalla:

```powershell
python .\Instrumentacion_RIGOL\rigol_ds1202ze.py screenshot .\capturas_rigol\pantalla.png
```

Forma de onda visible de un canal:

```powershell
python .\Instrumentacion_RIGOL\rigol_ds1202ze.py waveform CHAN1 .\capturas_rigol\ch1.csv
```

Paquete completo para un ensayo:

```powershell
python .\Instrumentacion_RIGOL\rigol_ds1202ze.py bundle --label escalon_lab4
```

El paquete completo contiene:

- `pantalla.png`: imagen de la pantalla del osciloscopio.
- `chan1.csv` y `chan2.csv`: tiempo en segundos y tensión en voltios.
- `metadatos.json`: identificación, escalas, acoplamientos, factores de sonda,
  parámetros de adquisición y mediciones automáticas.

## Uso sin línea de comandos

Para comprobar la conexión, hacer doble clic en:

- `verificar_conexion_rigol.cmd`

Para capturar un ensayo completo, hacer doble clic en:

- `capturar_ensayo_rigol.cmd`

El iniciador solicita un nombre breve para el ensayo y crea automáticamente
una subcarpeta fechada dentro de `capturas_rigol`.

## Preparación de cada ensayo

1. Compensar las dos sondas con la salida de calibración del osciloscopio.
2. Confirmar 10X tanto en la sonda como en el menú del canal.
3. Seleccionar acoplamiento DC e impedancia de 1 megaohm.
4. Conectar todas las masas al mismo GND de la placa.
5. Ajustar escalas, base de tiempo y disparo desde el panel frontal.
6. Detener la adquisición cuando se necesite conservar un evento único.
7. Ejecutar `bundle` para obtener todos los archivos del ensayo.

La adquisición `waveform` usa el modo NORM del instrumento y descarga los
1200 puntos visibles. No modifica las escalas ni la configuración de disparo.
