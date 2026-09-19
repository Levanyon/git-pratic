import csv
import tempfile
import unittest
from pathlib import Path

from sensor_analyzer import (
    SensorReading,
    find_anomalies,
    load_readings,
    summarize,
)


class SensorAnalyzerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.readings = [
            SensorReading("2026-09-19T10:00:00", 40.0, 1.5),
            SensorReading("2026-09-19T10:10:00", 50.0, 2.5),
            SensorReading("2026-09-19T10:20:00", 80.0, 5.5),
        ]

    def test_summarize(self) -> None:
        result = summarize(self.readings)
        self.assertEqual(result["count"], 3)
        self.assertEqual(result["temperature_min"], 40.0)
        self.assertEqual(result["temperature_max"], 80.0)
        self.assertAlmostEqual(result["temperature_avg"], 56.6666666667)
        self.assertEqual(result["vibration_min"], 1.5)
        self.assertEqual(result["vibration_max"], 5.5)
        self.assertAlmostEqual(result["vibration_avg"], 3.1666666667)

    def test_empty_summary(self) -> None:
        result = summarize([])
        self.assertEqual(result["count"], 0)
        self.assertEqual(result["temperature_avg"], 0.0)
        self.assertEqual(result["vibration_avg"], 0.0)

    def test_find_anomalies(self) -> None:
        anomalies = find_anomalies(
            self.readings,
            temp_limit=70.0,
            vibration_limit=4.5,
        )
        self.assertEqual(len(anomalies), 1)
        reading, reasons = anomalies[0]
        self.assertEqual(reading.timestamp, "2026-09-19T10:20:00")
        self.assertEqual(len(reasons), 2)

    def test_load_readings(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "readings.csv"
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle)
                writer.writerow(["timestamp", "temperature_c", "vibration_mm_s"])
                writer.writerow(["2026-09-19T11:00:00", "42.5", "2.1"])

            loaded = load_readings(csv_path)

        self.assertEqual(
            loaded,
            [SensorReading("2026-09-19T11:00:00", 42.5, 2.1)],
        )

    def test_missing_column_raises(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_path = Path(temp_dir) / "bad.csv"
            csv_path.write_text(
                "timestamp,temperature_c\n2026-09-19T11:00:00,42.5\n",
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_readings(csv_path)


if __name__ == "__main__":
    unittest.main()
