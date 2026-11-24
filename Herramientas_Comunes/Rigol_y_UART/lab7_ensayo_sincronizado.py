#!/usr/bin/env python3
"""Laboratorio 7: captura sincronizada de UART PSoC y RIGOL DS1202Z-E.

Usa el aviso '# LAB7 inicio;' del firmware para armar el Rigol *despues*
del reset, antes del inicio de muestreo (LAB7_INICIO_MS=3000).
No programa el PSoC, no cambia la planta ni activa un controlador.
Solo configura el instrumento, espera SW3 y guarda evidencia trazable.
"""

from __future__ import annotations

import argparse
import csv
import io
import re
import sys
import time
from datetime import datetime
from pathlib import Path

import serial
import numpy as np

from rigol_ds1202ze import (
    acquire_screen_waveform,
    connect,
    save_json,
    save_screenshot,
    save_waveform_csv,
)

CAMPOS_ESP = ("k", "t_us", "adc_counts", "adc_mV", "y_cal_mV",
              "y_rel_mV", "r_mV", "u_solicitada_mV", "u_nominal_mV",
              "xhat1_mV", "xhat2_mV", "innovacion_mV", "dac_pos",
              "dac_neg", "cpu_us", "intervalo_us", "flags")


def configurar_rigol(scope, args):
    """Prepara una unica adquisicion, sin modificar el firmware ni el PSoC."""
    scope.write(":STOP")
    for canal, escala in (("CHAN1", args.escala_ch1),
                          ("CHAN2", args.escala_ch2)):
        scope.write(f":{canal}:DISP ON")
        scope.write(f":{canal}:COUP DC")
        scope.write(f":{canal}:PROB 10")
        scope.write(f":{canal}:BWL 20M")
        scope.write(f":{canal}:SCAL {escala:.9g}")
        scope.write(f":{canal}:OFFS 0")
    scope.write(":TIM:MODE MAIN")
    scope.write(f":TIM:SCAL {args.escala_tiempo:.9g}")
    scope.write(":TIM:OFFS 0")
    scope.write(":TRIG:MODE EDGE")
    scope.write(":TRIG:EDGE:SOUR CHAN1")
    scope.write(":TRIG:EDGE:SLOP POS")
    scope.write(f":TRIG:EDGE:LEV {args.nivel_trigger:.9g}")
    scope.write(":TRIG:SWE NORM")


def leer_uart_y_armar(uart, scope, args):
    """Lee el protocolo real del Lab7. No fuerza triggers ni envía UART."""
    recibido = bytearray()
    pendiente = bytearray()
    inicio_anunciado = None
    armado = False
    fin = False
    modo = None
    deadline = time.monotonic() + args.timeout
    print("LISTO: UART COM4 y Rigol preparados. Presioná SW3 UNA VEZ ahora.",
          flush=True)
    while time.monotonic() < deadline:
        n = uart.in_waiting
        if n:
            bloque = uart.read(min(n, 16384))
            recibido.extend(bloque)
            pendiente.extend(bloque)
            if len(recibido) > 250_000:
                raise RuntimeError("UART superó 250 kB: protocolo inesperado.")
            while b"\n" in pendiente:
                linea_bytes, _, resto = pendiente.partition(b"\n")
                pendiente = bytearray(resto)
                linea = linea_bytes.decode("ascii", errors="replace").strip()
                if linea.startswith("# LAB7 inicio;"):
                    inicio_anunciado = time.monotonic()
                    print("PSoC: aviso de arranque detectado; esperando antes de armar SINGLE...",
                          flush=True)
                elif linea.startswith("# LAB7 datos "):
                    match = re.search(r"\bmodo=([A-Z_]+)", linea)
                    if match:
                        modo = match.group(1)
                        print(f"PSoC: modo={modo}", flush=True)
                elif linea.startswith("# LAB7 END;"):
                    fin = True
                    break
        if (inicio_anunciado is not None and not armado and
                time.monotonic() - inicio_anunciado >= args.demora_armado):
            scope.write(":SING")
            armado = True
            print(f"RIGOL ARMADO: SINGLE después de {args.demora_armado:.2f} s del aviso UART.",
                  flush=True)
        if fin:
            break
        time.sleep(0.01)
    return bytes(recibido), inicio_anunciado is not None, armado, fin, modo


def guardar_uart(carpeta: Path, bruto: bytes):
    (carpeta / "psoc_uart.txt").write_bytes(bruto)
    texto = bruto.decode("ascii", errors="replace")
    lineas = [x.strip() for x in texto.splitlines()]
    inicio_csv = next((i for i, v in enumerate(lineas)
                       if v.startswith("k,t_us,")), None)
    fin_csv = next((i for i, v in enumerate(lineas)
                    if v.startswith("# LAB7 END;")), None)
    resumen = {"uart_bytes": len(bruto), "uart_fin": fin_csv is not None,
               "filas_uart": 0, "filas_flags_no_cero": None,
               "max_cpu_us": None, "Ts_median_us": None,
               "valores_mando_solicitado_mV": []}
    if inicio_csv is None:
        return resumen
    if fin_csv is None:
        fin_csv = len(lineas)
    contenido = "\n".join(lineas[inicio_csv:fin_csv]) + "\n"
    (carpeta / "psoc_uart.csv").write_text(contenido, encoding="utf-8")
    tabla = list(csv.DictReader(io.StringIO(contenido)))
    resumen["filas_uart"] = len(tabla)
    if not tabla:
        return resumen
    if not all(campo in tabla[0] for campo in CAMPOS_ESP):
        resumen["aviso_formato_uart"] = "Columnas del firmware distintas a las esperadas"
        return resumen
    try:
        flags = np.asarray([int(r["flags"]) for r in tabla])
        tiempos = np.asarray([int(r["intervalo_us"]) for r in tabla])
        cpu = np.asarray([int(r["cpu_us"]) for r in tabla])
        mando = np.asarray([int(r["u_solicitada_mV"]) for r in tabla])
        resumen.update(
            filas_flags_no_cero=int(np.count_nonzero(flags)),
            max_cpu_us=int(cpu.max()),
            Ts_median_us=float(np.median(tiempos[1:])) if len(tiempos)>1 else None,
            valores_mando_solicitado_mV=sorted(set(map(int,mando))),
            t_final_us=int(tabla[-1]["t_us"]),
        )
    except (ValueError, KeyError) as e:
        resumen["aviso_analisis_uart"] = str(e)
    return resumen


def generar_parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--port", default="COM4", help="Puerto serie PSoC (COM4)")
    p.add_argument("--baud", type=int, default=57600)
    p.add_argument("--resource", default=None, help="Recurso VISA Rigol (opcional)")
    p.add_argument("--label", default="ensayo_lab7")
    p.add_argument("--modo-esperado", choices=("ABIERTO", "MONITOR", "PREDICCION", "ACTUAL"),
                   default="ABIERTO")
    p.add_argument("--salida", type=Path, default=Path(__file__).resolve().parents[2] /
                   "Laboratorio_7" / "04_Ensayos" / "Capturas_Sincronizadas")
    p.add_argument("--escala-ch1", type=float, default=0.02,
                   help="Voltios/div CH1; 0.02 = 20 mV/div")
    p.add_argument("--escala-ch2", type=float, default=0.02)
    p.add_argument("--escala-tiempo", type=float, default=0.05,
                   help="Segundos/div; 0.05 = 50 ms/div")
    p.add_argument("--nivel-trigger", type=float, default=0.035,
                   help="Nivel absoluto en voltios; adaptar si cambia el offset")
    p.add_argument("--demora-armado", type=float, default=0.5,
                   help="Segundos después del aviso de inicio (debe ser < 3 s)")
    p.add_argument("--timeout", type=float, default=45,
                   help="Tiempo total esperando el ciclo PSoC")
    return p


def main(argv=None):
    args = generar_parser().parse_args(argv)
    if not (0 <= args.demora_armado < 2.5):
        print("ERROR: --demora-armado debe ser >=0 y <2.5s (firmware espera 3s).",
              file=sys.stderr)
        return 2
    if any(v<=0 for v in (args.escala_ch1,args.escala_ch2,args.escala_tiempo,args.timeout)):
        print("ERROR: escalas y timeout deben ser positivos.",file=sys.stderr)
        return 2

    etiqueta = re.sub(r"[^a-zA-Z0-9_-]+", "_", args.label).strip("_") or "lab7"
    sello = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    carpeta = args.salida.resolve() / f"{sello}_{etiqueta}"
    carpeta.mkdir(parents=True, exist_ok=False)
    meta = {"captura_local": datetime.now().astimezone().isoformat(timespec="seconds"),
            "modo_esperado": args.modo_esperado,
            "puerto": args.port, "baud": args.baud,
            "configuracion_rigol": {"ch1_V_div":args.escala_ch1,
                                   "ch2_V_div":args.escala_ch2,
                                   "tiempo_s_div":args.escala_tiempo,
                                   "trigger_V":args.nivel_trigger,
                                   "fuente_trigger":"CHAN1",
                                   "flanco":"POS", "sweep":"NORM",
                                   "trigger_forzado":False},
            "firmware_requiere_inicio_ms":3000}
    manager = scope = None
    bruto = b""
    inicio = time.perf_counter()
    try:
        print(f"Carpeta ensayo: {carpeta}", flush=True)
        print("Conectando RIGOL USB VISA...", flush=True)
        manager, scope, recurso = connect(args.resource)
        meta["recurso_rigol"] = recurso
        print("Configurando CH1=J5, CH2=J7, trigger ascendente CH1...",flush=True)
        configurar_rigol(scope,args)
        print(f"Abriendo UART {args.port} a {args.baud} 8N1...",flush=True)
        with serial.Serial(args.port,args.baud,timeout=0.1) as uart:
            uart.reset_input_buffer()
            bruto, anuncio, armado, fin, modo = leer_uart_y_armar(uart,scope,args)
        meta.update(anuncio_arranque=anuncio,rigol_armado=armado,
                    uart_fin_recibido=fin,modo_detectado=modo)
        meta["uart"] = guardar_uart(carpeta,bruto)
        print(f"UART: {meta['uart']['filas_uart']} filas; fin={fin}; "
              f"flags !=0: {meta['uart']['filas_flags_no_cero']}",flush=True)
        if not armado:
            meta["aviso"] = "Rigol NO fue armado: inicio UART no detectado a tiempo"
            raise RuntimeError(meta["aviso"])

        # No se fuerza el disparo: un registro sin flanco se conserva como diagnostico,
        # nunca se etiqueta como ensayo fisico valido.
        estado = scope.query(":TRIG:STAT?").strip()
        meta["estado_rigol_antes_stop"] = estado
        if estado != "STOP":
            print(f"ATENCION: Rigol estado {estado}, SIN trigger fisico confirmado; se detiene para diagnostico.",flush=True)
            scope.write(":STOP")
            meta["trigger_fisico_confirmado"] = False
        else:
            print("RIGOL: SINGLE terminó en STOP; se conserva el evento.",flush=True)
            meta["trigger_fisico_confirmado"] = True
        for canal in ("CHAN1","CHAN2"):
            t0 = time.perf_counter()
            print(f"Guardando {canal}...",flush=True)
            t, y, detalles = acquire_screen_waveform(scope,canal)
            save_waveform_csv(carpeta/f"{canal.lower()}.csv",t,y)
            meta.setdefault("formas_onda",{})[canal] = detalles
            if canal == "CHAN1":
                bajo = np.median(y[y <= np.quantile(y,0.25)])
                alto = np.median(y[y >= np.quantile(y,0.75)])
                meta["variacion_robusta_CH1_V"] = round(float(alto-bajo),6)
            print(f"{canal}: {len(t)} puntos en {time.perf_counter()-t0:.2f} s",flush=True)
        t0 = time.perf_counter()
        print("Guardando pantalla.png...",flush=True)
        save_screenshot(scope,carpeta/"pantalla.png")
        print(f"PNG guardado en {time.perf_counter()-t0:.2f} s",flush=True)
        meta["duracion_total_s"] = round(time.perf_counter()-inicio,3)
        meta["ensayo_valido_preliminar"] = bool(
            meta["trigger_fisico_confirmado"] and fin and modo==args.modo_esperado
            and meta["uart"]["filas_uart"] == 256
            and meta["uart"]["filas_flags_no_cero"] == 0
            and (modo!="ABIERTO" or meta["variacion_robusta_CH1_V"]>=0.01)
        )
        save_json(carpeta/"metadatos.json",meta)
        print(f"CAPTURA COMPLETA: {carpeta}",flush=True)
        print(f"VALIDACION PRELIMINAR: {meta['ensayo_valido_preliminar']}; "
              f"variacion robusta CH1={meta['variacion_robusta_CH1_V']*1000:.2f} mV",flush=True)
        if not meta["ensayo_valido_preliminar"]:
            print("AVISO: conservar como diagnostico; revisar modo, flags, pulso y trigger.",flush=True)
        return 0
    except (Exception, KeyboardInterrupt) as error:
        meta["error"] = str(error)
        print(f"ERROR ENSAYO: {error}",file=sys.stderr,flush=True)
        if bruto and not (carpeta/"psoc_uart.txt").exists():
            guardar_uart(carpeta,bruto)
        save_json(carpeta/"metadatos.json",meta)
        return 1
    finally:
        if scope is not None:
            try: scope.close()
            except Exception: pass
        if manager is not None:
            try: manager.close()
            except Exception: pass


if __name__ == "__main__":
    raise SystemExit(main())
