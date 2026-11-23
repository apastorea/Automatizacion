"""Captura un bloque finito LAB4 emitido por el PSoC mediante UART."""

from __future__ import annotations

import argparse
import re
import time
from datetime import datetime
from pathlib import Path

import serial


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", default="COM4")
    parser.add_argument("--baud", type=int, default=57600)
    parser.add_argument("--timeout", type=float, default=60.0)
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output_dir = root / "Matlab" / "Laboratorio 4" / "datos_experimentales"
    output_dir.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + args.timeout
    received = ""

    print(
        f"UART_LISTA: {args.port} a {args.baud} 8N1. Reinicie ahora el PSoC.",
        flush=True,
    )
    with serial.Serial(args.port, args.baud, timeout=0.2) as uart:
        uart.reset_input_buffer()
        while time.monotonic() < deadline:
            waiting = uart.in_waiting
            if waiting:
                received += uart.read(waiting).decode("ascii", errors="ignore")
                match = re.search(
                    r"(?s)(# LAB4 mode=.*?# END;[^\r\n]*(?:\r?\n)?)",
                    received,
                )
                if match:
                    capture = match.group(1)
                    break
            time.sleep(0.01)
        else:
            raise TimeoutError("No se recibio una captura LAB4 completa.")

    mode_match = re.search(r"mode_name=([A-Z_]+)", capture)
    ref_match = re.search(r"reference=([A-Z_]+)", capture)
    mode = mode_match.group(1).lower() if mode_match else "desconocido"
    reference = ref_match.group(1).lower() if ref_match else "desconocida"
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    output_path = output_dir / f"lab4_{mode}_{reference}_{stamp}.csv"
    header = (
        f"# HOST ground_verified=1 captured_at={stamp} "
        f"port={args.port} baud={args.baud}\n"
    )
    output_path.write_text(header + capture, encoding="utf-8")
    print(f"CAPTURA={output_path}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
