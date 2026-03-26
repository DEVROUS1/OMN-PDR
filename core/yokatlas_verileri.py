"""
OmniPDR – core/yokatlas_verileri.py
=======================================
YÖK Atlas veri seti – yokatlas_full.json'dan dinamik yükleme.

6.37 MB'lık gerçek veri setini okuyarak binlerce bölümü
filtreleme ve öneri sistemine sunar. Veri bulunamazsa
gömülü fallback seti kullanılır.

Resmi güncel veriler için: https://yokatlas.yok.gov.tr
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

# Streamlit cache (opsiyonel – Streamlit yoksa sessizce geç)
try:
    import streamlit as st
    _HAS_STREAMLIT = True
except ImportError:
    _HAS_STREAMLIT = False


@dataclass
class BolumBilgisi:
    """Bir üniversite bölümünü temsil eder."""
    universite: str
    bolum: str
    sehir: str
    puan_turu: str          # SAY, EA, SOZ, TYT, YDT
    taban_puan: float       # taban puanı
    tavan_puan: float       # tavan puanı
    siralama: int           # başarı sıralaması
    kontenjan: int          # Toplam kontenjan
    tur: str = "Devlet"     # Devlet / Vakıf


@dataclass
class LiseBilgisi:
    """Bir liseyi temsil eder (LGS için)."""
    okul_adi: str
    sehir: str
    okul_turu: str
    taban_puan: float
    yuzdelik_dilim: float
    kontenjan: int


LGS_LISELERI = [
    LiseBilgisi("Galatasaray Lisesi", "İstanbul", "Anadolu Lisesi", 494.5, 0.04, 100),
    LiseBilgisi("İstanbul Erkek Lisesi", "İstanbul", "Anadolu Lisesi", 493.5, 0.05, 120),
    LiseBilgisi("Kabataş Erkek Lisesi", "İstanbul", "Anadolu Lisesi", 492.0, 0.07, 150),
    LiseBilgisi("Ankara Fen Lisesi", "Ankara", "Fen Lisesi", 490.8, 0.10, 120),
    LiseBilgisi("İzmir Fen Lisesi", "İzmir", "Fen Lisesi", 488.5, 0.15, 90),
    LiseBilgisi("Bursa Nilüfer IMKB Fen Lisesi", "Bursa", "Fen Lisesi", 485.4, 0.25, 120),
    LiseBilgisi("Atatürk Anadolu Lisesi", "Ankara", "Anadolu Lisesi", 481.2, 0.50, 180),
    LiseBilgisi("Kadıköy Anadolu Lisesi", "İstanbul", "Anadolu Lisesi", 478.1, 0.70, 200),
    LiseBilgisi("Cağaloğlu Anadolu Lisesi", "İstanbul", "Anadolu Lisesi", 475.0, 0.85, 150),
    LiseBilgisi("Antalya Yusuf Ziya Öner Fen L", "Antalya", "Fen Lisesi", 468.2, 1.50, 120),
    LiseBilgisi("Adana Fen Lisesi", "Adana", "Fen Lisesi", 465.0, 1.80, 120),
    LiseBilgisi("Karşıyaka Anadolu Lisesi", "İzmir", "Anadolu Lisesi", 450.0, 3.50, 150),
    LiseBilgisi("Gazi Anadolu Lisesi", "Ankara", "Anadolu Lisesi", 445.0, 4.00, 180),
    LiseBilgisi("Ahmet Erdem Anadolu Lisesi", "Bursa", "Anadolu Lisesi", 440.0, 4.50, 150),
    LiseBilgisi("Süleyman Demirel Fen Lisesi", "Afyon", "Fen Lisesi", 435.0, 5.00, 90),
    LiseBilgisi("Mehmet Niyazi Altuğ And L", "İstanbul", "Anadolu Lisesi", 430.0, 5.50, 180),
    LiseBilgisi("Cihat Kora Anadolu Lisesi", "İzmir", "Anadolu Lisesi", 420.0, 7.00, 150),
]

def lise_ara(puan: float = None, sehir: str = None) -> List[LiseBilgisi]:
    sonuc = LGS_LISELERI.copy()
    if sehir and sehir != "Tümü":
        sonuc = [l for l in sonuc if l.sehir.lower() == sehir.lower()]
    if puan is not None:
        sonuc = sorted(sonuc, key=lambda x: abs(x.taban_puan - puan))
    return sonuc

def lise_benzersiz_sehirler() -> List[str]:
    return sorted(list(set(l.sehir for l in LGS_LISELERI)))


# ──────────────────────────────────────────────
# JSON Veri Yükleme
# ──────────────────────────────────────────────
_JSON_YOL = Path(__file__).parent.parent / "data" / "yokatlas_full.json"


def _json_yukle() -> List[BolumBilgisi]:
    """
    yokatlas_full.json dosyasından tüm bölüm verilerini yükler.
    Dosya bulunamazsa gömülü fallback setini döndürür.
    """
    if _JSON_YOL.exists():
        try:
            with open(_JSON_YOL, "r", encoding="utf-8") as f:
                ham = json.load(f)
            sonuc = []
            for kayit in ham:
                try:
                    sonuc.append(BolumBilgisi(
                        universite=str(kayit.get("universite", "") or ""),
                        bolum=str(kayit.get("bolum", "") or ""),
                        sehir=str(kayit.get("sehir", "") or ""),
                        puan_turu=str(kayit.get("puan_turu", "") or ""),
                        taban_puan=float(kayit.get("taban_puan", 0) or 0),
                        tavan_puan=float(kayit.get("tavan_puan", 0) or 0),
                        siralama=int(kayit.get("siralama", 0) or 0),
                        kontenjan=int(kayit.get("kontenjan", 0) or 0),
                        tur=str(kayit.get("tur", "Devlet") or "Devlet"),
                    ))
                except (ValueError, TypeError):
                    continue  # Bozuk kayıtları atla
            if sonuc:
                return sonuc
        except (json.JSONDecodeError, IOError):
            pass  # Dosya bozuksa fallback'e düş

    # Fallback: Gömülü minimum veri seti
    return _FALLBACK_VERILERI()


def _FALLBACK_VERILERI() -> List[BolumBilgisi]:
    """JSON yüklenemezse kullanılacak minimum veri seti."""
    return [
        BolumBilgisi("Hacettepe Üniversitesi", "Tıp", "Ankara", "SAY", 489.2, 498.5, 748, 350),
        BolumBilgisi("İstanbul Üniversitesi", "Tıp", "İstanbul", "SAY", 486.1, 497.8, 1100, 450),
        BolumBilgisi("ODTÜ", "Bilgisayar Mühendisliği", "Ankara", "SAY", 478.9, 496.1, 3800, 180),
        BolumBilgisi("Boğaziçi Üniversitesi", "Bilgisayar Mühendisliği", "İstanbul", "SAY", 482.3, 497.2, 2400, 120),
        BolumBilgisi("İTÜ", "Bilgisayar Mühendisliği", "İstanbul", "SAY", 475.6, 493.8, 5500, 180),
        BolumBilgisi("Ankara Üniversitesi", "Hukuk", "Ankara", "EA", 442.5, 468.3, 12000, 450),
        BolumBilgisi("İstanbul Üniversitesi", "Hukuk", "İstanbul", "EA", 445.8, 472.1, 10000, 500),
        BolumBilgisi("Koç Üniversitesi", "Tıp", "İstanbul", "SAY", 485.5, 497.8, 1300, 100, "Vakıf"),
    ]


# Streamlit cache ile veriyi tek sefer yükle
if _HAS_STREAMLIT:
    @st.cache_data(ttl=3600, show_spinner=False)
    def _yukle_cached() -> List[dict]:
        """Veriyi dict listesi olarak cache'le (dataclass cache'lenemez)."""
        veriler = _json_yukle()
        return [
            {
                "universite": b.universite, "bolum": b.bolum, "sehir": b.sehir,
                "puan_turu": b.puan_turu, "taban_puan": b.taban_puan,
                "tavan_puan": b.tavan_puan, "siralama": b.siralama,
                "kontenjan": b.kontenjan, "tur": b.tur,
            }
            for b in veriler
        ]

    def _verileri_getir() -> List[BolumBilgisi]:
        return [BolumBilgisi(**d) for d in _yukle_cached()]
else:
    # Streamlit olmadan çalışma (test, script)
    _CACHE = None

    def _verileri_getir() -> List[BolumBilgisi]:
        global _CACHE
        if _CACHE is None:
            _CACHE = _json_yukle()
        return _CACHE


# Geriye dönük uyumluluk: BOLUM_VERILERI referansı
@property
def _lazy_bolum_verileri():
    return _verileri_getir()


# BOLUM_VERILERI artık fonksiyon çağrısı ile çalışır
def _get_bolum_verileri() -> List[BolumBilgisi]:
    return _verileri_getir()


# Geriye dönük uyumluluk için modül seviyesinde referans
# İlk erişimde lazy load yapılır
class _LazyList:
    """Modül seviyesinde lazy loading sağlayan wrapper."""
    def __init__(self):
        self._data = None

    def _ensure_loaded(self):
        if self._data is None:
            self._data = _verileri_getir()

    def __iter__(self):
        self._ensure_loaded()
        return iter(self._data)

    def __len__(self):
        self._ensure_loaded()
        return len(self._data)

    def __getitem__(self, idx):
        self._ensure_loaded()
        return self._data[idx]

    def copy(self):
        self._ensure_loaded()
        return self._data.copy()


BOLUM_VERILERI = _LazyList()


# ──────────────────────────────────────────────
# Arama ve Filtreleme Fonksiyonları
# ──────────────────────────────────────────────
def bolum_ara(
    puan_turu: Optional[str] = None,
    min_puan: Optional[float] = None,
    max_puan: Optional[float] = None,
    sehir: Optional[str] = None,
    bolum_adi: Optional[str] = None,
    tur: Optional[str] = None,
    limit: int = 200,
) -> List[BolumBilgisi]:
    """Kriterlere göre bölüm arar. Performans için limit parametresi eklendi."""
    sonuclar = list(BOLUM_VERILERI)

    if puan_turu:
        sonuclar = [b for b in sonuclar if b.puan_turu == puan_turu]
    if min_puan is not None:
        sonuclar = [b for b in sonuclar if b.taban_puan >= min_puan]
    if max_puan is not None:
        sonuclar = [b for b in sonuclar if b.taban_puan <= max_puan]
    if sehir:
        sonuclar = [b for b in sonuclar if sehir.lower() in b.sehir.lower()]
    if bolum_adi:
        sonuclar = [b for b in sonuclar if bolum_adi.lower() in b.bolum.lower()]
    if tur:
        sonuclar = [b for b in sonuclar if b.tur == tur]

    sonuclar = sorted(sonuclar, key=lambda b: b.taban_puan, reverse=True)
    return sonuclar[:limit]


def universite_oner(
    puan: float,
    puan_turu: str,
    tolerans: float = 20.0,
) -> Dict[str, List[BolumBilgisi]]:
    """
    Puana göre üniversite önerileri.
    3 kategori: Güvenli, Dengeli, Şans
    """
    tum = bolum_ara(puan_turu=puan_turu, limit=5000)

    guvenli = [b for b in tum if b.taban_puan <= puan - tolerans / 2][:10]
    dengeli = [b for b in tum if abs(b.taban_puan - puan) <= tolerans / 2][:10]
    sans = [b for b in tum if puan < b.taban_puan <= puan + tolerans][:10]

    return {
        "guvenli": sorted(guvenli, key=lambda b: b.taban_puan, reverse=True),
        "dengeli": sorted(dengeli, key=lambda b: b.taban_puan, reverse=True),
        "sans": sorted(sans, key=lambda b: b.taban_puan),
    }


def benzersiz_sehirler() -> List[str]:
    """Verideki tüm şehirleri döndürür."""
    return sorted(set(b.sehir for b in BOLUM_VERILERI))


def benzersiz_bolumler() -> List[str]:
    """Verideki tüm bölüm adlarını döndürür."""
    return sorted(set(b.bolum for b in BOLUM_VERILERI))


def benzersiz_universiteler() -> List[str]:
    """Verideki tüm üniversite adlarını döndürür."""
    return sorted(set(b.universite for b in BOLUM_VERILERI))


def veri_sayisi() -> int:
    """Yüklenen toplam bölüm sayısını döndürür."""
    return len(BOLUM_VERILERI)
