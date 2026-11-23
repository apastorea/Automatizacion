"""Calibracion sincronizada PSoC--RIGOL para el Laboratorio 4.

Escucha el protocolo UART del modo LAB4_MODE_DMM_CALIBRATION y mide, para
cada nivel estable, el mando en CH1 (J8) y la salida de planta en CH2 (J7).
No programa el PSoC ni aplica niveles distintos de los definidos en firmware.
"""

from __future__ import annotations

import argparse
import csv
import re
import statistics
import time
from datetime import datetime
from pathlib import Path

import serial

from rigol_ds1202ze import connect, save_screenshot


POINT_RE = re.compile(
    r"# DMM point=(?P<point>\d+) requested_mV=(?P<requested>-?\d+) "
    r"applied_mV=(?P<applied>-?\d+) dac_p=(?P<dac_p>\d+) "
    r"dac_n=(?P<dac_n>\d+) hold_ms=(?P<hold_ms>\d+) "
    r"saturated=(?P<saturated>\d+)"
)

ADC_RE = re.compile(
    r"# DMM ADC point=(?P<point>\d+) samples=(?P<samples>\d+) "
    r"raw_avg_x1000=(?P<raw_avg_x1000>-?\d+) "
    r"adc_mean_uV=(?P<adc_mean_uV>-?\d+)"
)


def configure_scope(scope) -> None:
    """Configura ambos canales para niveles de hasta +/-0,25 V."""
    for channel in ("CHAN1", "CHAN2"):
        scope.write(f":{channel}:DISP ON")
        scope.write(f":{channel}:COUP DC")
        scope.write(f":{channel}:PROB 10")
        scope.write(f":{channel}:BWL 20M")
        scope.write(f":{channel}:SCAL 0.1")
        scope.write(f":{channel}:OFFS 0")
    scope.write(":TIM:SCAL 0.05")
    scope.write(":TIM:OFFS 0")
    scope.write(":TRIG:MODE EDGE")
    scope.write(":TRIG:EDGE:SOUR CHAN1")
    scope.write(":TRIG:EDGE:SLOP POS")
    scope.write(":TRIG:EDGE:LEV 0.025")
    scope.write(":TRIG:SWE AUTO")
    scope.write(":RUN")


def finite_measurement(scope, channel: str) -> float:
    value = float(scope.query(f":MEAS:ITEM? VAVG,{channel}"))
    if abs(value) > 1.0e20:
        raise RuntimeError(f"Lectura VAVG invalida en {channel}: {value}")
    return value


def measure_level(scope, settle_s: float, repetitions: int) -> dict[str, float]:
    time.sleep(settle_s)
    ch1: list[float] = []
    ch2: list[float] = []
    for _ in range(repetitions):
        ch1.append(finite_measurement(scope, "CHAN1"))
        ch2.append(finite_measurement(scope, "CHAN2"))
        time.sleep(0.35)
    return {
        "u_mean_V": statistics.fmean(ch1),
        "u_std_V": statistics.stdev(ch1) if len(ch1) > 1 else 0.0,
        "y_mean_V": statistics.fmean(ch2),
        "y_std_V": statistics.stdev(ch2) if len(ch2) > 1 else 0.0,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="COM4")
    parser.add_argument("--baud", type=int, default=57600)
    parser.add_argument("--timeout", type=float, default=360.0)
    parser.add_argument("--settle", type=float, default=3.0)
    parser.add_argument("--repetitions", type=int, default=5)
    parser.add_argument(
        "--stop-after-point",
        type=int,
        choices=range(1, 6),
        default=5,
        help="Finaliza despues del punto indicado; util para diagnostico de nodos.",
    )
    parser.add_argument("--label", default="calibracion_rigol")
    parser.add_argument("--resource")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    output_dir = root / "Matlab" / "Laboratorio 4" / "datos_experimentales"
    output_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_label = re.sub(r"[^A-Za-z0-9_-]+", "_", args.label).strip("_")
    csv_path = output_dir / f"lab4_{safe_label}_{stamp}.csv"
    image_dir = output_dir / f"lab4_{safe_label}_{stamp}_imagenes"
    image_dir.mkdir(parents=True, exist_ok=True)

    resource_manager, scope, resource_name = connect(args.resource)
    configure_scope(scope)
    rows: list[dict[str, object]] = []
    deadline = time.monotonic() + args.timeout
    armed = False

    print(f"RIGOL listo: {resource_name}", flush=True)
    print(
        "REGISTRADOR_LISTO: reinicie ahora el PSoC. "
        "Se aceptara solamente el modo LAB4 DMM.",
        flush=True,
    )

    try:
        with serial.Serial(args.port, args.baud, timeout=0.5) as uart:
            uart.reset_input_buffer()
            while time.monotonic() < deadline:
                raw = uart.readline()
                if not raw:
                    continue
                line = raw.decode("ascii", errors="ignore").strip()
                if line:
                    print(line, flush=True)
                if line.startswith("# LAB4 DMM:"):
                    armed = True
                    continue
                if line.startswith("# DMM point="):
                    if not armed:
                        print(
                            "IGNORADO: punto perteneciente a una secuencia iniciada "
                            "antes de abrir el registrador.",
                            flush=True,
                        )
                        continue
                    match = POINT_RE.fullmatch(line)
                    if match is None:
                        raise RuntimeError(f"Cabecera DMM no reconocida: {line}")
                    metadata = {key: int(value) for key, value in match.groupdict().items()}
                    if metadata["saturated"] != 0:
                        raise RuntimeError("El firmware informa saturacion durante la calibracion.")
                    measured = measure_level(scope, args.settle, args.repetitions)
                    row = {**metadata, **measured}
                    rows.append(row)
                    image_path = image_dir / f"punto_{metadata['point']}.png"
                    save_screenshot(scope, image_path)
                    print(
                        f"MEDIDO punto={metadata['point']} "
                        f"u={1e3 * measured['u_mean_V']:.3f} mV "
                        f"y={1e3 * measured['y_mean_V']:.3f} mV",
                        flush=True,
                    )
                    continue
                if line.startswith("# DMM ADC point="):
                    if not armed:
                        continue
                    match = ADC_RE.fullmatch(line)
                    if match is None:
                        raise RuntimeError(f"Lectura ADC DMM no reconocida: {line}")
                    adc_data = {key: int(value) for key, value in match.groupdict().items()}
                    if not rows or rows[-1]["point"] != adc_data["point"]:
                        raise RuntimeError("La lectura ADC no corresponde al ultimo punto medido.")
                    rows[-1]["adc_samples"] = adc_data["samples"]
                    rows[-1]["adc_raw_avg"] = adc_data["raw_avg_x1000"] / 1000.0
                    rows[-1]["adc_mean_V"] = adc_data["adc_mean_uV"] / 1.0e6
                    print(
                        f"ADC punto={adc_data['point']} "
                        f"raw={rows[-1]['adc_raw_avg']:.3f} "
                        f"Vadc={rows[-1]['adc_mean_V']:.6f} V",
                        flush=True,
                    )
                    if adc_data["point"] >= args.stop_after_point:
                        print(
                            "DIAGNOSTICO_COMPLETO: reinicie el PSoC para volver a cero.",
                            flush=True,
                        )
                        break
                    continue
                if line.startswith("# DMM END"):
                    break
            else:
                raise TimeoutError("No finalizo la secuencia DMM dentro del plazo.")
    finally:
        scope.close()
        resource_manager.close()

    if len(rows) != args.stop_after_point:
        raise RuntimeError(
            f"Se esperaban {args.stop_after_point} puntos DMM y se recibieron {len(rows)}."
        )

    fieldnames = [
        "point",
        "requested",
        "applied",
        "dac_p",
        "dac_n",
        "hold_ms",
        "saturated",
        "u_mean_V",
        "u_std_V",
        "y_mean_V",
        "y_std_V",
        "adc_samples",
        "adc_raw_avg",
        "adc_mean_V",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV={csv_path}", flush=True)
    print(f"IMAGENES={image_dir}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
