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

## Captura ultrarrápida para Laboratorio 7 (sin consultas adicionales)

Con el osciloscopio en STOP después de SINGLE y las sondas CH1=J5 y CH2=J7, ejecutar desde la raíz del repositorio `Automatizacion/git`:

```powershell
git pull --ff-only origin main

# Solo las curvas numéricas (dos CSV + metadatos básicos). Más ágil que una captura completa.
python -u ".\Herramientas_Comunes\Rigol_y_UART\rigol_ds1202ze.py" bundle --quick --only data --label abierto_Lab7 --root ".\Laboratorio_7\04_Ensayos\Capturas_Rigol"
```

Opcionalmente capturar **solo imagen**:

```powershell
python -u ".\Herramientas_Comunes\Rigol_y_UART\rigol_ds1202ze.py" bundle --quick --only screen --label abierto_Lab7 --root ".\Laboratorio_7\04_Ensayos\Capturas_Rigol"
```

Para guardar imagen, CSV y metadatos mínimos en un mismo directorio:

```powershell
python -u ".\Herramientas_Comunes\Rigol_y_UART\rigol_ds1202ze.py" bundle --quick --only all --label abierto_Lab7 --root ".\Laboratorio_7\04_Ensayos\Capturas_Rigol"
```

Cada ejecución crea una carpeta con fecha propia. El script muestra los segundos consumidos en conexión, captura de pantalla y descarga de cada canal. Si `data` tarda muy poco pero `screen` tarda mucho, conviene guardar PNG únicamente en las capturas seleccionadas para el informe. Si incluso `data` tarda mucho, revisar los tiempos que imprime y conexiones USB/VISA.

Opcional: añadir antes de `bundle` el argumento
`--resource "USB0::0x1AB1::0x0517::DS1ZE275014864::INSTR"`
para omitir el barrido de descubrimiento VISA del instrumento que ya identificamos. El identificador debe coincidir con el recurso PyVISA encontrado; no confundirlo con el recurso de MATLAB que incluye `::0::`.

El modo `NORM` descarga los 1200 puntos visibles por canal (ideal para ensayos de respuesta temporal de decenas de ms); no es una exportación de toda la memoria profunda del osciloscopio. La adquisición debe estar detenida en STOP y el evento correctamente capturado por SINGLE antes de ejecutarse. No se modifican escalas ni el trigger.
