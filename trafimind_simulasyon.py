"""
TrafiMind -- Trafik Akisi Simulasyonu
======================================
Proje  : Yapay Zeka Destekli Dinamik Trafik Isigi Kontrol Sistemi
Yarisma: TUBITAK 2204-B Ortaokul Bolge Finali 2026
Ogrenciler: Fatih Samet Ozkur | Ilhan Zayif

Model
-----
Karsilastirilan deger: ARA YOL bekleme suresi

  Sabit sistem : Ara yol her zaman 25 sn yesil alir -> arac 25 sn bekler.
  TrafiMind    : Ara yol T = 5+(n*2) sn yesil alir (5<=T<=25)
                 n=0 ise faz atlanir -> bekleme = 0 sn

Yontem
------
- 4 senaryo: Sabah pik, Gunduz normal, Aksam pik, Gece sakin
- Toplam 1200 dongu, RANDOM_SEED=2024 (tekrarlanabilir)
"""

import random
import statistics

RANDOM_SEED       = 2024
SABIT_ARAYOL_SURE = 25
T_MIN             = 5
T_MAX             = 25
T_BASE            = 5
T_PER_VEHICLE     = 2

def hesapla_T(n):
    if n == 0:
        return 0
    return max(T_MIN, min(T_MAX, T_BASE + n * T_PER_VEHICLE))

SENARYOLAR = {
    "Sabah Pik  (07:30-09:00)": {"n_aralik": (6, 12), "dongu": 180},
    "Gunduz     (10:00-16:00)": {"n_aralik": (2,  7), "dongu": 360},
    "Aksam Pik  (17:00-19:00)": {"n_aralik": (7, 12), "dongu": 180},
    "Gece Sakin (22:00-06:00)": {"n_aralik": (0,  3), "dongu": 480},
}

def simulasyonu_calistir(verbose=True):
    rng = random.Random(RANDOM_SEED)
    tum_sabit, tum_dinamik = [], []
    sonuclar = {}

    if verbose:
        print("=" * 60)
        print("TrafiMind -- Trafik Akisi Simulasyonu")
        print("Karsilastirma: ARA YOL bekleme suresi")
        print("=" * 60)

    for ad, p in SENARYOLAR.items():
        sabit_list, dinamik_list = [], []
        faz_atlama = 0

        for _ in range(p["dongu"]):
            n  = rng.randint(*p["n_aralik"])
            fw = float(SABIT_ARAYOL_SURE)
            dw = float(hesapla_T(n))
            sabit_list.append(fw)
            dinamik_list.append(dw)
            tum_sabit.append(fw)
            tum_dinamik.append(dw)
            if n == 0:
                faz_atlama += 1

        ort_s   = statistics.mean(sabit_list)
        ort_d   = statistics.mean(dinamik_list)
        azalma  = (ort_s - ort_d) / ort_s * 100
        faz_pct = faz_atlama / p["dongu"] * 100

        sonuclar[ad] = {
            "dongu": p["dongu"],
            "ort_sabit_sn": round(ort_s, 1),
            "ort_dinamik_sn": round(ort_d, 1),
            "azalma_yuzde": round(azalma, 1),
            "faz_atlama_pct": round(faz_pct, 1),
        }

        if verbose:
            print(f"\n{ad}")
            print(f"  Dongu     : {p['dongu']}")
            print(f"  n araligi : {p['n_aralik'][0]}-{p['n_aralik'][1]} arac")
            print(f"  Sabit     : {ort_s:.1f} sn  (hep sabit)")
            print(f"  TrafiMind : {ort_d:.1f} sn")
            print(f"  Azalma    : -%{azalma:.1f}")
            if faz_pct > 0:
                print(f"  Faz atla  : %{faz_pct:.1f} dongu")

    genel_s      = statistics.mean(tum_sabit)
    genel_d      = statistics.mean(tum_dinamik)
    genel_azalma = (genel_s - genel_d) / genel_s * 100
    std_d        = statistics.stdev(tum_dinamik)
    toplam       = sum(p["dongu"] for p in SENARYOLAR.values())

    sonuclar["GENEL"] = {
        "dongu": toplam,
        "ort_sabit_sn": round(genel_s, 1),
        "ort_dinamik_sn": round(genel_d, 1),
        "std_dinamik": round(std_d, 1),
        "azalma_yuzde": round(genel_azalma, 1),
    }

    if verbose:
        print("\n" + "=" * 60)
        print(f"GENEL SONUC  ({toplam} dongu, 4 senaryo)")
        print("=" * 60)
        print(f"  Sabit sistem : {genel_s:.1f} sn  (her zaman 25 sn)")
        print(f"  TrafiMind    : {genel_d:.1f} sn  (+/-{std_d:.1f})")
        print(f"  Azalma       : -%{genel_azalma:.1f}")

    return sonuclar

def T_tablosu_yazdir():
    print("\nT Formulü -- T = 5 + (n x 2)")
    print("-" * 42)
    print(f"{'n':>5}  {'Hesap':>13}  {'T':>5}  {'Durum':>10}")
    print("-" * 42)
    for n in [0, 1, 3, 5, 8, 10, 11, 12]:
        T = hesapla_T(n)
        if n == 0:
            hesap, durum = "Faz atla", "FAZ ATLA"
        else:
            ham = T_BASE + n * T_PER_VEHICLE
            hesap = f"5+({n}x2)={ham}"
            durum = "Ust sinir" if ham > T_MAX else "Normal"
        print(f"{n:>5}  {hesap:>13}  {T:>4} sn  {durum:>10}")
    print("-" * 42)

if __name__ == "__main__":
    sonuclar = simulasyonu_calistir(verbose=True)
    T_tablosu_yazdir()
    g = sonuclar["GENEL"]
    print(f"\nSonuc: {g['dongu']} dongude ara yol bekleme")
    print(f"  Sabit: {g['ort_sabit_sn']} sn  ->  TrafiMind: {g['ort_dinamik_sn']} sn  (-%{g['azalma_yuzde']})")
