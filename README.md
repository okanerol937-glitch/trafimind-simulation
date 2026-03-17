# trafimind-simulation
Araç yoğunluğuna göre bekleme süresini azaltan yapay zekâ destekli dinamik trafik ışığı simülasyonu.

# TrafiMind — Trafik Akışı Simülasyonu 🚦

Bu repo, **TrafiMind: Yapay Zekâ Destekli Dinamik Trafik Işığı Kontrol Sistemi** projesi kapsamında geliştirilen simülasyon kodunu içerir.

## 📌 Amaç
Sabit zamanlı trafik ışığı sistemi ile TrafiMind dinamik algoritmasını karşılaştırmak:

- Ortalama bekleme süresi
- Trafik verimliliği

---

## ⚙️ Algoritma

TrafiMind yeşil süreyi şu şekilde hesaplar:

T = 5 + (n × 2)

Kısıtlar:
- 5 ≤ T ≤ 25 saniye
- n = araç sayısı
- n = 0 → faz atlanır (bekleme yok)

---

## 🧪 Simülasyon

Simülasyon şu senaryoları içerir:
- Sabah pik saat
- Gündüz normal trafik
- Akşam pik saat
- Gece düşük trafik

Toplam 1200 döngü çalıştırılmıştır.

---

## ▶️ Çalıştırma

```bash
pip install -r requirements.txt
python trafimind_simulasyon.py
