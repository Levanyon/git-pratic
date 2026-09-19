# Sensor Log Analyzer

Küçük bir Python CLI projesi: CSV biçimindeki sıcaklık ve titreşim sensörü kayıtlarını analiz eder, özet istatistikler çıkarır ve belirlenen eşikleri aşan ölçümleri raporlar.

## Neler yapar?

- CSV sensör kayıtlarını okur.
- Sıcaklık ve titreşim için min / max / ortalama hesaplar.
- Sıcaklık veya titreşim eşiklerini aşan kayıtları anomali olarak işaretler.
- Tamamen Python standart kütüphanesiyle çalışır.
- `unittest` testleri ve GitHub Actions CI içerir.

## Kullanım

Python 3.10+ önerilir.

```bash
python sensor_analyzer.py sample_data.csv
```

Eşikleri değiştirmek için:

```bash
python sensor_analyzer.py sample_data.csv --temp-limit 75 --vibration-limit 5.0
```

## Örnek çıktı

```text
Sensor Log Summary
------------------
Readings: 6
Temperature: min=36.5 °C, max=78.2 °C, avg=48.5 °C
Vibration:   min=1.2 mm/s, max=5.1 mm/s, avg=2.6 mm/s

Anomalies: 2
- 2026-09-19T12:00:00 | temperature=78.2 °C
- 2026-09-19T12:10:00 | vibration=5.1 mm/s
```

## Test

```bash
python -m unittest discover -v
```

## Dosyalar

- `sensor_analyzer.py` — ana CLI ve analiz fonksiyonları
- `sample_data.csv` — örnek sensör verisi
- `test_sensor_analyzer.py` — birim testleri
- `.github/workflows/tests.yml` — GitHub Actions test iş akışı
- `.gitignore` — Python için temel hariç tutmalar

## Öğrenme hedefi

Bu mini proje; CSV okuma, veri doğrulama, `dataclass`, istatistik hesaplama, CLI argümanları, hata yönetimi, birim testi ve CI kullanımını birlikte pratik etmek için hazırlandı.
