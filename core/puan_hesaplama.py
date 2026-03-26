"""
OmniPDR – core/puan_hesaplama.py
====================================
Türk eğitim sistemi puan hesaplama motoru.

Kapsanan Sınavlar:
  ① TYT – Temel Yeterlilik Testi (120 soru, 4 yanlış = 1 doğru)
  ② AYT – Alan Yeterlilik Testleri (80 soru, SAY/EA/SÖZ)
  ③ LGS – Liseye Geçiş Sınavı (90 soru, 3 yanlış = 1 doğru)

Yerleştirme Puanı = TYT × 0.40 + AYT × 0.60 + OBP × 0.12
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any


# ──────────────────────────────────────────────
# Sabitler
# ──────────────────────────────────────────────

# TYT test yapısı
TYT_DERSLER = {
    "Türkçe":            {"soru_sayisi": 40, "katsayi": 3.3},
    "Temel Matematik":   {"soru_sayisi": 40, "katsayi": 3.3},
    "Tarih":             {"soru_sayisi": 5, "katsayi": 3.4},
    "Coğrafya":          {"soru_sayisi": 5, "katsayi": 3.4},
    "Felsefe":           {"soru_sayisi": 5, "katsayi": 3.4},
    "Din Kültürü":       {"soru_sayisi": 5, "katsayi": 3.4},
    "Fizik":             {"soru_sayisi": 7, "katsayi": 3.4},
    "Kimya":             {"soru_sayisi": 7, "katsayi": 3.4},
    "Biyoloji":          {"soru_sayisi": 6, "katsayi": 3.4},
}
TYT_BASLANGIC = 100.0
TYT_MAKSIMUM = 500.0

# AYT test yapısı ve puan türü katsayıları
AYT_DERSLER = {
    "Matematik":    {"soru_sayisi": 40},
    "Fizik":        {"soru_sayisi": 14},
    "Kimya":        {"soru_sayisi": 13},
    "Biyoloji":     {"soru_sayisi": 13},
    "Edebiyat":     {"soru_sayisi": 24},
    "Tarih-1":      {"soru_sayisi": 10},
    "Coğrafya-1":   {"soru_sayisi": 6},
    "Tarih-2":      {"soru_sayisi": 11},
    "Coğrafya-2":   {"soru_sayisi": 11},
    "Felsefe":      {"soru_sayisi": 12},
    "Din":          {"soru_sayisi": 6},
}

# AYT puan türü ağırlıkları (yaklaşık katsayılar)
AYT_PUAN_KATSAYILARI = {
    "SAY": {
        "Matematik": 3.0, "Fizik": 2.85, "Kimya": 3.07, "Biyoloji": 3.07,
        "Edebiyat": 0.0, "Tarih-1": 0.0, "Coğrafya-1": 0.0,
        "Tarih-2": 0.0, "Coğrafya-2": 0.0, "Felsefe": 0.0, "Din": 0.0,
    },
    "EA": {
        "Matematik": 3.0, "Fizik": 0.0, "Kimya": 0.0, "Biyoloji": 0.0,
        "Edebiyat": 3.0, "Tarih-1": 2.8, "Coğrafya-1": 3.33,
        "Tarih-2": 0.0, "Coğrafya-2": 0.0, "Felsefe": 0.0, "Din": 0.0,
    },
    "SOZ": {
        "Matematik": 0.0, "Fizik": 0.0, "Kimya": 0.0, "Biyoloji": 0.0,
        "Edebiyat": 3.0, "Tarih-1": 2.8, "Coğrafya-1": 3.33,
        "Tarih-2": 2.91, "Coğrafya-2": 2.91, "Felsefe": 2.5, "Din": 3.33,
    },
}

# LGS test yapısı
LGS_DERSLER = {
    "Türkçe":               {"soru_sayisi": 20, "agirlik": 4},
    "Matematik":            {"soru_sayisi": 20, "agirlik": 4},
    "Fen Bilimleri":        {"soru_sayisi": 20, "agirlik": 4},
    "T.C. İnkılap Tarihi":  {"soru_sayisi": 10, "agirlik": 1},
    "Din Kültürü":          {"soru_sayisi": 10, "agirlik": 1},
    "İngilizce":            {"soru_sayisi": 10, "agirlik": 1},
}
LGS_MAKSIMUM = 500.0

# Tahmini sıralama tabloları (yaklaşık değerler, 2024 verileri baz alınmıştır)
TYT_SIRALAMA_TABLOSU = [
    (500, 1), (490, 100), (480, 500), (470, 1500), (460, 3000),
    (450, 5500), (440, 9000), (430, 14000), (420, 20000), (410, 28000),
    (400, 38000), (390, 50000), (380, 65000), (370, 82000), (360, 102000),
    (350, 125000), (340, 152000), (330, 183000), (320, 218000), (310, 258000),
    (300, 303000), (290, 353000), (280, 410000), (270, 473000), (260, 543000),
    (250, 620000), (240, 705000), (230, 798000), (220, 900000), (210, 1012000),
    (200, 1135000), (150, 2000000), (100, 3500000),
]

SAY_SIRALAMA_TABLOSU = [
    (500, 1), (490, 50), (480, 200), (470, 600), (460, 1500),
    (450, 3000), (440, 5500), (430, 9000), (420, 14000), (410, 20000),
    (400, 28000), (390, 38000), (380, 50000), (370, 65000), (360, 82000),
    (350, 102000), (340, 125000), (330, 152000), (320, 183000), (310, 218000),
    (300, 260000), (280, 360000), (260, 500000), (240, 680000), (200, 1200000),
]

EA_SIRALAMA_TABLOSU = [
    (500, 1), (490, 30), (480, 150), (470, 500), (460, 1200),
    (450, 2500), (440, 4500), (430, 7500), (420, 12000), (410, 18000),
    (400, 25000), (390, 34000), (380, 45000), (370, 58000), (360, 73000),
    (350, 90000), (340, 110000), (330, 135000), (320, 163000), (310, 195000),
    (300, 230000), (280, 320000), (260, 440000), (240, 600000), (200, 1000000),
]

SOZ_SIRALAMA_TABLOSU = [
    (500, 1), (490, 20), (480, 100), (470, 350), (460, 900),
    (450, 2000), (440, 3800), (430, 6500), (420, 10000), (410, 15000),
    (400, 22000), (390, 30000), (380, 40000), (370, 52000), (360, 66000),
    (350, 82000), (340, 100000), (330, 122000), (320, 148000), (310, 178000),
    (300, 212000), (280, 295000), (260, 400000), (240, 540000), (200, 900000),
]

LGS_SIRALAMA_TABLOSU = [
    (500, 1), (495, 100), (490, 500), (485, 1000), (480, 2000),
    (475, 3500), (470, 5000), (460, 10000), (450, 18000), (440, 28000),
    (430, 40000), (420, 55000), (410, 72000), (400, 92000), (380, 140000),
    (360, 200000), (340, 270000), (320, 350000), (300, 440000),
    (280, 540000), (260, 650000), (240, 770000), (200, 1000000),
]


# ──────────────────────────────────────────────
# Sonuç Veri Sınıfları
# ──────────────────────────────────────────────
@dataclass
class PuanSonucu:
    """Puan hesaplama sonucu."""
    ham_puan: float
    yerlestirme_puani: float  # OBP dahil
    puan_turu: str
    tahmini_siralama: int
    detay: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LGSSonucu:
    """LGS puan hesaplama sonucu."""
    puan: float
    tahmini_siralama: int
    tahmini_yuzdelik: float
    ders_puanlari: Dict[str, float] = field(default_factory=dict)


# ──────────────────────────────────────────────
# Hesaplama Fonksiyonları
# ──────────────────────────────────────────────
def net_hesapla_yks(dogru: int, yanlis: int) -> float:
    """YKS net hesaplama: 4 yanlış = 1 doğruyu götürür."""
    return max(0.0, dogru - yanlis / 4)


def net_hesapla_lgs(dogru: int, yanlis: int) -> float:
    """LGS net hesaplama: 3 yanlış = 1 doğruyu götürür."""
    return max(0.0, dogru - yanlis / 3)


def tyt_puan_hesapla(netleri: Dict[str, float]) -> float:
    """
    TYT puanı hesaplar.
    netleri: {"Türkçe": 30, "Temel Matematik": 25, "Sosyal Bilimler": 15, "Fen Bilimleri": 12}
    """
    puan = TYT_BASLANGIC
    for ders, bilgi in TYT_DERSLER.items():
        net = netleri.get(ders, 0.0)
        puan += net * bilgi["katsayi"]
    return min(puan, TYT_MAKSIMUM)


def ayt_puan_hesapla(netleri: Dict[str, float], puan_turu: str = "SAY") -> float:
    """
    AYT puanı hesaplar.
    puan_turu: "SAY", "EA", "SOZ"
    """
    katsayilar = AYT_PUAN_KATSAYILARI.get(puan_turu, AYT_PUAN_KATSAYILARI["SAY"])
    puan = 100.0  # AYT başlangıç
    for ders, katsayi in katsayilar.items():
        net = netleri.get(ders, 0.0)
        puan += net * katsayi
    return min(puan, TYT_MAKSIMUM)


def yerlestirme_puani_hesapla(
    tyt_puani: float,
    ayt_puani: float,
    obp: float = 0.0,
) -> float:
    """
    YKS yerleştirme puanı.
    Formül: TYT × 0.40 + AYT × 0.60 + OBP × 0.6
    OBP: Ortaöğretim Başarı Puanı (diploma notu, max 100)
    OBP katkısı max 60 puan (100 * 0.6).
    """
    obp_katki = min(obp * 0.6, 60.0)
    return tyt_puani * 0.40 + ayt_puani * 0.60 + obp_katki


def lgs_puan_hesapla(netleri: Dict[str, float]) -> LGSSonucu:
    """
    LGS puanı hesaplar (0-500 arası).
    Ağırlıklar: Türkçe/Mat/Fen = 4, İnkılap/Din/İng = 1
    """
    toplam_agirlikli = 0.0
    max_agirlikli = 0.0
    ders_puanlari = {}

    for ders, bilgi in LGS_DERSLER.items():
        net = netleri.get(ders, 0.0)
        agirlikli_net = net * bilgi["agirlik"]
        max_net = bilgi["soru_sayisi"] * bilgi["agirlik"]
        toplam_agirlikli += agirlikli_net
        max_agirlikli += max_net
        ders_puanlari[ders] = round(
            (net / bilgi["soru_sayisi"]) * 100, 1
        ) if bilgi["soru_sayisi"] > 0 else 0.0

    puan = (toplam_agirlikli / max_agirlikli) * LGS_MAKSIMUM if max_agirlikli > 0 else 0.0
    siralama = _siralama_tahmin(puan, LGS_SIRALAMA_TABLOSU)
    # Yaklaşık 1.1 milyon aday
    yuzdelik = max(0.01, min(100.0, (siralama / 1_100_000) * 100))

    return LGSSonucu(
        puan=round(puan, 2),
        tahmini_siralama=siralama,
        tahmini_yuzdelik=round(yuzdelik, 2),
        ders_puanlari=ders_puanlari,
    )


def _siralama_tahmin(puan: float, tablo: list) -> int:
    """Puan tablosuna göre linear interpolation ile sıralama tahmini."""
    if not tablo:
        return 0

    # Tablonun en yüksek puanından büyükse
    if puan >= tablo[0][0]:
        return tablo[0][1]

    # Tablonun en düşük puanından küçükse
    if puan <= tablo[-1][0]:
        return tablo[-1][1]

    # Linear interpolation
    for i in range(len(tablo) - 1):
        ust_puan, ust_siralama = tablo[i]
        alt_puan, alt_siralama = tablo[i + 1]
        if ust_puan >= puan >= alt_puan:
            oran = (ust_puan - puan) / (ust_puan - alt_puan) if ust_puan != alt_puan else 0
            return int(ust_siralama + oran * (alt_siralama - ust_siralama))

    return tablo[-1][1]


_VEPUAN_CACHE = {}

def _vepuan_api_get(tyt_netleri: Dict[str, float], ayt_netleri: Dict[str, float], obp: float, puan_turu: str) -> Optional[PuanSonucu]:
    try:
        cache_key = (frozenset(tyt_netleri.items()), frozenset(ayt_netleri.items()), obp, puan_turu)
        if cache_key in _VEPUAN_CACHE:
            return _VEPUAN_CACHE[cache_key]
            
        import urllib.request
        import urllib.parse
        import json
        
        data_dict = {
            'postname': 'tyt-hesapla',
            'isyerlesme': 0,
            'diplomapuani': max(50.0, min(100.0, obp)) if obp > 0 else 0,
            'tyt-t': tyt_netleri.get("Türkçe", 0),
            'tyt-s': sum(tyt_netleri.get(d, 0) for d in ["Tarih", "Coğrafya", "Felsefe", "Din Kültürü"]),
            'tyt-m': tyt_netleri.get("Temel Matematik", 0),
            'tyt-f': sum(tyt_netleri.get(d, 0) for d in ["Fizik", "Kimya", "Biyoloji"]),
            'ayt-mat': ayt_netleri.get("Matematik", 0),
            'ayt-fizik': ayt_netleri.get("Fizik", 0),
            'ayt-kimya': ayt_netleri.get("Kimya", 0),
            'ayt-biyoloji': ayt_netleri.get("Biyoloji", 0),
            'ayt-edebiyat': ayt_netleri.get("Edebiyat", 0),
            'ayt-tarih1': ayt_netleri.get("Tarih-1", 0),
            'ayt-cografya1': ayt_netleri.get("Coğrafya-1", 0),
            'ayt-tarih2': ayt_netleri.get("Tarih-2", 0),
            'ayt-cografya2': ayt_netleri.get("Coğrafya-2", 0),
            'ayt-felsefe': ayt_netleri.get("Felsefe", 0),
            'ayt-din': ayt_netleri.get("Din", 0),
            'ayt-dil': ayt_netleri.get("Yabancı Dil", 0)
        }
        data = urllib.parse.urlencode({k: v if v != 0 else "" for k, v in data_dict.items()}).encode('utf-8')
        req = urllib.request.Request('https://vepuan.com/hesapla.php', data=data, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'https://vepuan.com/'
        })
        resp = urllib.request.urlopen(req, timeout=3).read().decode('utf-8')
        rjson = json.loads(resp)
        year_data = rjson.get("2024") or rjson.get("2025") or list(rjson.values())[0]

        pt_map = {"SAY": "sayisal", "EA": "esit", "SOZ": "sozel", "TYT": "tyt"}
        prefix = pt_map.get(puan_turu, "sayisal")
        
        if prefix == "tyt":
            ham = float(year_data.get("ham", 0))
            yerlestirme = float(year_data.get("yerlestirme", 0))
            sira = int(year_data.get("tyt-yerlestirme-siralama", 0))
        else:
            ham = float(year_data.get(f"{prefix}-ham-puan", 0))
            yerlestirme = float(year_data.get(f"{prefix}-yerlestirme-puan", 0))
            sira = int(year_data.get(f"{prefix}-yerlestirme-siralama", 0))
            
        sonuc = PuanSonucu(
            ham_puan=round(ham, 2),
            yerlestirme_puani=round(yerlestirme, 2),
            puan_turu=puan_turu,
            tahmini_siralama=sira,
            detay={
                "TYT Puanı": round(float(year_data.get("yerlestirme", 0)), 2),
                "YKS Puanı": round(yerlestirme, 2),
                "OBP Katkısı": round(yerlestirme - ham, 2),
                "Yerleştirme Puanı": round(yerlestirme, 2),
                "Kaynak": "VePuan YKS (Aktif)"
            }
        )
        
        _VEPUAN_CACHE[cache_key] = sonuc
        return sonuc
    except Exception:
        return None

def tam_puan_hesapla(
    netleri: Dict[str, float],
    puan_turu: str = "SAY",
    obp: float = 0.0,
    sinav_turu: str = "YKS"
) -> PuanSonucu:
    """Tüm puanları hesaplayıp tek sonuç döndürür."""
    # 1. LGS ise farklı mantık
    if sinav_turu == "LGS":
        lgs = lgs_puan_hesapla(netleri)
        return PuanSonucu(
            ham_puan=lgs.puan, 
            yerlestirme_puani=lgs.puan, 
            puan_turu="LGS", 
            tahmini_siralama=lgs.tahmini_siralama,
            detay=lgs.ders_puanlari
        )

    # 2. YKS için API veya Fallback
    # API tyt ve ayt netlerini ayrı bekliyor ama bizde tek dict var
    # Aslında _vepuan_api_get içindeki get()'ler dict içinde varsa çalışır.
    api_sonucu = _vepuan_api_get(netleri, netleri, obp, puan_turu)
    if api_sonucu:
        return api_sonucu
    
    # fallback
    tyt = tyt_puan_hesapla(netleri)
    ayt = ayt_puan_hesapla(netleri, puan_turu)
    yerlestirme = yerlestirme_puani_hesapla(tyt, ayt, obp)

    siralama_tablolari = {
        "SAY": SAY_SIRALAMA_TABLOSU,
        "EA": EA_SIRALAMA_TABLOSU,
        "SOZ": SOZ_SIRALAMA_TABLOSU,
    }
    tablo = siralama_tablolari.get(puan_turu, SAY_SIRALAMA_TABLOSU)
    siralama = _siralama_tahmin(yerlestirme, tablo)

    return PuanSonucu(
        ham_puan=round(ayt, 2),
        yerlestirme_puani=round(yerlestirme, 2),
        puan_turu=puan_turu,
        tahmini_siralama=siralama,
        detay={
            "TYT Puanı": round(tyt, 2),
            "AYT Puanı": round(ayt, 2),
            "OBP Katkısı": round(min(obp * 0.6, 60.0), 2),
            "Yerleştirme Puanı": round(yerlestirme, 2),
            "Kaynak": "Çevrimdışı (Tahmini)"
        },
    )


# ──────────────────────────────────────────────
# Hedef Analizi
# ──────────────────────────────────────────────
def hedef_net_farki(
    mevcut_netleri: Dict[str, float],
    hedef_siralama: int,
    sinav_turu: str = "YKS",
    puan_turu: str = "SAY",
) -> Dict[str, float]:
    """
    Hedefe ulaşmak için her derste kaç net artması gerektiğini tahmin eder.
    Basit lineer yaklaşım kullanır.
    """
    if sinav_turu == "LGS":
        mevcut = lgs_puan_hesapla(mevcut_netleri)
        mevcut_puan = mevcut.puan
        # Hedef puana ulaşmak için gereken puan farkı
        hedef_puan = _puan_from_siralama(hedef_siralama, LGS_SIRALAMA_TABLOSU)
        puan_farki = hedef_puan - mevcut_puan
        if puan_farki <= 0:
            return {}
        # Eşit dağıt
        ders_sayisi = len(mevcut_netleri)
        if ders_sayisi == 0:
            return {}
        net_artis = puan_farki / ders_sayisi / 4  # yaklaşık
        return {d: round(net_artis, 1) for d in mevcut_netleri}

    return {}


def _puan_from_siralama(siralama: int, tablo: list) -> float:
    """Sıralamadan puan tahmin eder (ters interpolation)."""
    if siralama <= tablo[0][1]:
        return tablo[0][0]
    if siralama >= tablo[-1][1]:
        return tablo[-1][0]

    for i in range(len(tablo) - 1):
        ust_puan, ust_sir = tablo[i]
        alt_puan, alt_sir = tablo[i + 1]
        if ust_sir <= siralama <= alt_sir:
            oran = (siralama - ust_sir) / (alt_sir - ust_sir) if alt_sir != ust_sir else 0
            return ust_puan - oran * (ust_puan - alt_puan)

    return tablo[-1][0]
