"""Captura sincronizada UART + RIGOL de un ensayo dinámico LAB4."""

from __future__ import annotations

import argparse
import re
import time
from datetime import datetime
from pathlib import Path

import serial

from rigol_ds1202ze import (
    acquire_screen_waveform,
    connect,
    instrument_metadata,
    save_json,
    save_screenshot,
    save_waveform_csv,
)


def configure_scope(
    scope, ch1_scale: float, ch2_scale: float,
    time_scale: float, trigger_level: float, trigger_source: str,
) -> None:
    for channel, scale in (("CHAN1", ch1_scale), ("CHAN2", ch2_scale)):
        scope.write(f":{channel}:DISP ON")
        scope.write(f":{channel}:COUP DC")
        scope.write(f":{channel}:PROB 10")
        scope.write(f":{channel}:BWL 20M")
        scope.write(f":{channel}:SCAL {scale}")
        scope.write(f":{channel}:OFFS 0")
    scope.write(f":TIM:SCAL {time_scale}")
    scope.write(":TIM:OFFS 0")
    # Alta resolucion promedia las muestras internas de cada intervalo de
    # pantalla y evita que impulsos de pocos microsegundos oculten la
    # dinamica lenta de la planta.
    scope.write(":ACQ:TYPE HRES")
    scope.write(":TRIG:MODE EDGE")
    # La fuente se selecciona desde la linea de comandos. CH2 permite medir
    # directamente la respuesta; CH1 resulta mas robusto cuando el cambio de
    # mando es inmediato y la salida de la planta tarda en cruzar el umbral.
    scope.write(f":TRIG:EDGE:SOUR {trigger_source}")
    scope.write(":TRIG:EDGE:SLOP POS")
    scope.write(f":TRIG:EDGE:LEV {trigger_level}")
    scope.write(":TRIG:SWE NORM")
    # Se arma despues de recibir por UART el mensaje de arranque del PSoC.
    # Asi el transitorio electrico del RESET no dispara antes del escalon.
    scope.write(":STOP")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="COM4")
    parser.add_argument("--baud", type=int, default=57600)
    parser.add_argument("--timeout", type=float, default=90.0)
    parser.add_argument("--label", default="ensayo")
    parser.add_argument("--resource")
    parser.add_argument("--ch1-scale", type=float, default=0.05)
    parser.add_argument("--ch2-scale", type=float, default=0.02)
    parser.add_argument("--time-scale", type=float, default=0.01)
    parser.add_argument("--trigger-level", type=float, default=0.03)
    parser.add_argument(
        "--trigger-source", choices=("CHAN1", "CHAN2"), default="CHAN2",
    )
    parser.add_argument(
        "--force-trigger", action="store_true",
        help=(
            "Fuerza el disparo inmediatamente despues de armar. Util para "
            "ensayos cuyo instante se conoce y contienen impulsos espurios."
        ),
    )
    parser.add_argument(
        "--continuous-stop-delay", type=float,
        help=(
            "Ejecuta el RIGOL en AUTO desde el anuncio de arranque y lo "
            "detiene tras este retardo. Evita depender de un trigger."
        ),
    )
    parser.add_argument(
        "--arm-delay", type=float, default=2.5,
        help=(
            "Retardo desde el anuncio de arranque del PSoC hasta armar "
            "el RIGOL. Debe ser menor que LAB4_START_DELAY_MS."
        ),
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    destination = root / "Matlab" / "Laboratorio 4" / "datos_experimentales"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    label = re.sub(r"[^A-Za-z0-9_-]+", "_", args.label).strip("_") or "ensayo"
    folder = destination / f"lab4_{label}_{stamp}"
    folder.mkdir(parents=True, exist_ok=False)

    manager, scope, resource_name = connect(args.resource)
    try:
        scope.timeout = 60_000
        configure_scope(
            scope, args.ch1_scale, args.ch2_scale,
            args.time_scale, args.trigger_level, args.trigger_source,
        )
        print(
            f"ENSAYO_LISTO: RIGOL={resource_name}; UART={args.port}. "
            "Reinicie ahora el PSoC.",
            flush=True,
        )
        deadline = time.monotonic() + args.timeout
        received = ""
        scope_armed = False
        arm_at = None
        stop_at = None
        scope_stopped = False
        with serial.Serial(args.port, args.baud, timeout=0.2) as uart:
            uart.reset_input_buffer()
            while time.monotonic() < deadline:
                waiting = uart.in_waiting
                if waiting:
                    received += uart.read(waiting).decode("ascii", errors="ignore")
                    if (
                        not scope_armed and arm_at is None
                        and "# LAB4: mode=" in received
                    ):
                        if args.continuous_stop_delay is not None:
                            scope.write(":TRIG:SWE AUTO")
                            scope.write(":RUN")
                            scope_armed = True
                            stop_at = (
                                time.monotonic()
                                + args.continuous_stop_delay
                            )
                            print(
                                "RIGOL_CONTINUO: adquisición AUTO iniciada.",
                                flush=True,
                            )
                        else:
                            arm_at = time.monotonic() + args.arm_delay
                    match = re.search(
                        r"(?s)(# LAB4 mode=.*?# END;[^\r\n]*(?:\r?\n)?)",
                        received,
                    )
                    if match:
                        capture = match.group(1)
                        break
                if stop_at is not None and time.monotonic() >= stop_at:
                    scope.write(":STOP")
                    scope_stopped = True
                    stop_at = None
                    print("RIGOL_STOP_TEMPORIZADO: captura detenida.", flush=True)
                if (
                    not scope_armed and arm_at is not None
                    and time.monotonic() >= arm_at
                ):
                    scope.write(":SING")
                    scope_armed = True
                    if args.force_trigger:
                        time.sleep(0.02)
                        scope.write(":TFOR")
                    time.sleep(0.05)
                    trigger_state = scope.query(":TRIG:STAT?").strip()
                    print(
                        "RIGOL_ARMADO: esperando el evento aplicado; "
                        f"estado={trigger_state}.",
                        flush=True,
                    )
                time.sleep(0.01)
            else:
                raise TimeoutError("No se recibio una captura LAB4 completa.")

        if not scope_armed:
            raise RuntimeError("No se recibio el anuncio de arranque para armar el RIGOL.")

        if not scope_stopped:
            time.sleep(0.5)
        trigger_state_before_stop = scope.query(":TRIG:STAT?").strip()
        print(
            f"RIGOL_ESTADO_ANTES_STOP={trigger_state_before_stop}",
            flush=True,
        )
        scope.write(":STOP")
        uart_path = folder / "psoc_uart.csv"
        uart_path.write_text(
            f"# HOST ground_verified=1 captured_at={stamp} "
            f"port={args.port} baud={args.baud}\n" + capture,
            encoding="utf-8",
        )
        save_screenshot(scope, folder / "pantalla.png")
        metadata = instrument_metadata(scope, resource_name)
        waveform_info = {}
        for channel in ("CHAN1", "CHAN2"):
            time_s, voltage_v, info = acquire_screen_waveform(scope, channel)
            save_waveform_csv(folder / f"{channel.lower()}.csv", time_s, voltage_v)
            waveform_info[channel] = info
        metadata["waveforms"] = waveform_info
        save_json(folder / "metadatos.json", metadata)
        print(f"CAPTURA={folder}", flush=True)
        return 0
    finally:
        scope.close()
        manager.close()


if __name__ == "__main__":
    raise SystemExit(main())
