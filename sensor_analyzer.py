from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable


@dataclass(frozen=True)
class SensorReading:
    timestamp: str
    temperature_c: float
    vibration_mm_s: float


def load_readings(path: str | Path) -> list[SensorReading]:
    """Load sensor readings from a CSV file and validate required columns."""
    required = {"timestamp", "temperature_c", "vibration_mm_s"}
    readings: list[SensorReading] = []

    with Path(path).open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        missing = required - fieldnames
        if missing:
            raise ValueError(
                "Missing required column(s): " + ", ".join(sorted(missing))
            )

        for line_number, row in enumerate(reader, start=2):
            try:
                readings.append(
                    SensorReading(
                        timestamp=(row["timestamp"] or "").strip(),
                        temperature_c=float(row["temperature_c"]),
                        vibration_mm_s=float(row["vibration_mm_s"]),
                    )
                )
            except (TypeError, ValueError) as exc:
                raise ValueError(
                    f"Invalid sensor data on CSV line {line_number}."
                ) from exc

    return readings


def summarize(readings: Iterable[SensorReading]) -> dict[str, float | int]:
    items = list(readings)
    if not items:
        return {
            "count": 0,
            "temperature_min": 0.0,
            "temperature_max": 0.0,
            "temperature_avg": 0.0,
            "vibration_min": 0.0,
            "vibration_max": 0.0,
            "vibration_avg": 0.0,
        }

    temperatures = [item.temperature_c for item in items]
    vibrations = [item.vibration_mm_s for item in items]

    return {
        "count": len(items),
        "temperature_min": min(temperatures),
        "temperature_max": max(temperatures),
        "temperature_avg": mean(temperatures),
        "vibration_min": min(vibrations),
        "vibration_max": max(vibrations),
        "vibration_avg": mean(vibrations),
    }


def find_anomalies(
    readings: Iterable[SensorReading],
    temp_limit: float = 70.0,
    vibration_limit: float = 4.5,
) -> list[tuple[SensorReading, list[str]]]:
    anomalies: list[tuple[SensorReading, list[str]]] = []

    for reading in readings:
        reasons: list[str] = []
        if reading.temperature_c > temp_limit:
            reasons.append(f"temperature={reading.temperature_c:.1f} °C")
        if reading.vibration_mm_s > vibration_limit:
            reasons.append(f"vibration={reading.vibration_mm_s:.1f} mm/s")
        if reasons:
            anomalies.append((reading, reasons))

    return anomalies


def format_report(
    summary: dict[str, float | int],
    anomalies: list[tuple[SensorReading, list[str]]],
) -> str:
    lines = [
        "Sensor Log Summary",
        "------------------",
        f"Readings: {summary['count']}",
        (
            "Temperature: "
            f"min={summary['temperature_min']:.1f} °C, "
            f"max={summary['temperature_max']:.1f} °C, "
            f"avg={summary['temperature_avg']:.1f} °C"
        ),
        (
            "Vibration:   "
            f"min={summary['vibration_min']:.1f} mm/s, "
            f"max={summary['vibration_max']:.1f} mm/s, "
            f"avg={summary['vibration_avg']:.1f} mm/s"
        ),
        "",
        f"Anomalies: {len(anomalies)}",
    ]

    for reading, reasons in anomalies:
        lines.append(f"- {reading.timestamp} | " + ", ".join(reasons))

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Analyze temperature and vibration sensor logs from CSV."
    )
    parser.add_argument("csv_file", help="Path to the sensor CSV file.")
    parser.add_argument(
        "--temp-limit",
        type=float,
        default=70.0,
        help="Temperature anomaly threshold in °C (default: 70).",
    )
    parser.add_argument(
        "--vibration-limit",
        type=float,
        default=4.5,
        help="Vibration anomaly threshold in mm/s (default: 4.5).",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    readings = load_readings(args.csv_file)
    summary = summarize(readings)
    anomalies = find_anomalies(
        readings,
        temp_limit=args.temp_limit,
        vibration_limit=args.vibration_limit,
    )
    print(format_report(summary, anomalies))


if __name__ == "__main__":
    main()
