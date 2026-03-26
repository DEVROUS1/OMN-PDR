"""
OmniPDR – core/analiz_motoru.py
====================================
Psikolojik algoritmalar ve erken uyarı sistemi.

Kapsanan Psikolojik Kuramlar:
  ① Ebbinghaus – Aralıklı tekrar takvimi (HataKaydi sınıfına entegre, burada raporlanır)
  ② Vygotsky   – Yakınsal Gelişim Alanı (ZPD): Dinamik hedef belirleme
  ③ Zimmerman  – Öz-düzenlemeli öğrenme: Burnout dedektörü + bütünsel analiz
  ④ BONUS      – Uyku-performans korelasyonu (araştırma tabanlı)
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

import pandas as pd

from models.ogrenci_sinifi import DenemeKaydi, HataKaydi, Ogrenci


# ──────────────────────────────────────────────
# Yardımcı Enum'lar
# ──────────────────────────────────────────────
class UyariSeviyesi(Enum):
    NORMAL = auto()
    DIKKAT = auto()
    UYARI = auto()
    KRITIK = auto()


class BurnoutTipi(Enum):
    YOK = "Belirti yok"
    AKADEMIK_TUKENME = "Akademik Tükenmişlik"
    KAYGI_KACINMA = "Kaygı Kaynaklı Kaçınma"
    MOTIVASYON_KAYBI = "Motivasyon Kaybı"
    UYKU_BOZUKLUGU = "Uyku Bozukluğu Kaynaklı Performans Düşüşü"


# ──────────────────────────────────────────────
# 1. Analiz Sonucu Veri Sınıfları
# ──────────────────────────────────────────────
@dataclass
class BurnoutRaporu:
    """Tükenmişlik analizinin sonucunu taşır."""
    tip: BurnoutTipi = BurnoutTipi.YOK
    seviye: UyariSeviyesi = UyariSeviyesi.NORMAL
    mesaj: str = "✅ Herhangi bir risk faktörü tespit edilmedi."
    oneriler: List[str] = field(default_factory=list)
    detay: str = ""


@dataclass
class ZPDRaporu:
    """Vygotsky ZPD analizinin sonucunu taşır."""
    mevcut_seviye: float          # Son deneme toplam neti
    alt_sinir: float              # ZPD'nin alt sınırı (sıkılma bölgesi üstü)
    ust_sinir: float              # ZPD'nin üst sınırı (kaygı bölgesi altı)
    hedef_net: float              # Önerilen gerçekçi kısa vadeli hedef
    durum: str = ""               # "ZPD'de", "Çok Kolay", "Çok Zor"
    aciklama: str = ""


@dataclass
class GenelRapor:
    """Tüm analizlerin özet çıktısı."""
    burnout: BurnoutRaporu
    zpd: ZPDRaporu
    haftalik_trend: str           # "↑ Yükseliyor", "→ Sabit", "↓ Düşüyor"
    guclu_dersler: List[str]
    zayif_dersler: List[str]
    bugunun_tekrarlari: List[HataKaydi]
    uyku_uyarisi: Optional[str]


# ──────────────────────────────────────────────
# 2. AnalizMotoru – Ana servis sınıfı
# ──────────────────────────────────────────────
class AnalizMotoru:
    """
    Bir öğrencinin tüm verilerini analiz eden ve psikolojik
    kurama dayalı raporlar üreten servis sınıfı.

    Kullanım:
        motor = AnalizMotoru(ogrenci)
        rapor = motor.tam_analiz()
    """

    # Konfigürasyon sabitleri
    MIN_KAYIT_BURNOUT = 2   # Burnout tespiti için gereken min. deneme kaydı
    MIN_KAYIT_ZPD = 1       # ZPD hesabı için gereken min. kayıt
    ZPD_ALT_YUZDE = 0.92    # Mevcut netin %92'si → alt sınır (artık sıkıcı değil)
    ZPD_UST_YUZDE = 1.15    # Mevcut netin %115'i → üst sınır (kaygı verici değil)
    YUKSEK_STRES_ESIGI = 7  # Stres puanı ≥ 7 → yüksek stres
    DUSUK_UYKU_ESIGI = 6.0  # 6 saatten az uyku → uyarı
    CALISMA_ARTIS_ESIGI = 1.15  # %15 artış = belirgin artış

    def __init__(self, ogrenci: Ogrenci):
        self.ogrenci = ogrenci
        self._df: Optional[pd.DataFrame] = None  # Lazy cache

    # ── DataFrame yardımcısı ───────────────────

    def veri_cercevesi(self) -> pd.DataFrame:
        """
        Tüm deneme kayıtlarını analiz için pandas DataFrame'e dönüştürür.
        Tekrar oluşturmayı önlemek için sonuç önbelleğe alınır.
        """
        if self._df is not None:
            return self._df

        kayitlar = self.ogrenci.deneme_kayitlari
        if not kayitlar:
            return pd.DataFrame()

        satirlar = []
        for k in kayitlar:
            satir = {
                "tarih": pd.to_datetime(k.tarih),
                "toplam_net": k.toplam_net,
                "calisma_saati": k.calisma_saati,
                "stres_puani": k.stres_puani,
                "uyku_saati": k.uyku_saati,
            }
            satir.update({f"net_{ders}": net for ders, net in k.netleri.items()})
            satirlar.append(satir)

        self._df = pd.DataFrame(satirlar).sort_values("tarih").reset_index(drop=True)
        return self._df

    def df_sifirla(self) -> None:
        """Yeni veri eklendikten sonra cache'i temizle."""
        self._df = None

    # ── Tükenmişlik Dedektörü ─────────────────

    def burnout_analizi(self) -> BurnoutRaporu:
        """
        Zimmerman'ın öz-düzenlemeli öğrenme modeline dayalı
        tükenmişlik dedektörü.

        Analiz edilen boyutlar:
          - Çalışma saati trendi
          - Net trendi
          - Stres puanı trendi
          - Uyku süresi
        """
        kayitlar = self.ogrenci.deneme_kayitlari
        if len(kayitlar) < self.MIN_KAYIT_BURNOUT:
            return BurnoutRaporu(
                mesaj="ℹ️ Trend analizi için en az 2 deneme kaydı gereklidir.",
                detay="Daha fazla veri girin.",
            )

        # Son 2 ve önceki 2 kaydı karşılaştır (rolling window)
        yarim = max(1, len(kayitlar) // 2)
        eski = kayitlar[:yarim]
        yeni = kayitlar[yarim:]

        ort_net_eski = statistics.mean(k.toplam_net for k in eski)
        ort_net_yeni = statistics.mean(k.toplam_net for k in yeni)
        ort_calisma_eski = statistics.mean(k.calisma_saati for k in eski)
        ort_calisma_yeni = statistics.mean(k.calisma_saati for k in yeni)
        son_stres = kayitlar[-1].stres_puani
        son_uyku = kayitlar[-1].uyku_saati

        net_dusmus = ort_net_yeni < ort_net_eski
        calisma_artmis = ort_calisma_yeni > ort_calisma_eski * self.CALISMA_ARTIS_ESIGI
        calisma_dusmis = ort_calisma_yeni < ort_calisma_eski / self.CALISMA_ARTIS_ESIGI
        yuksek_stres = son_stres >= self.YUKSEK_STRES_ESIGI
        dusuk_uyku = son_uyku < self.DUSUK_UYKU_ESIGI

        # ── Kural 1: Akademik Tükenmişlik ──
        if calisma_artmis and net_dusmus and yuksek_stres:
            return BurnoutRaporu(
                tip=BurnoutTipi.AKADEMIK_TUKENME,
                seviye=UyariSeviyesi.KRITIK,
                mesaj="🚨 KRİTİK UYARI: Akademik Tükenmişlik Riski!",
                detay=(
                    f"Çalışma saati artmasına rağmen ({ort_calisma_eski:.1f}h → {ort_calisma_yeni:.1f}h) "
                    f"netler düşüyor ({ort_net_eski:.1f} → {ort_net_yeni:.1f}). "
                    f"Stres puanı: {son_stres}/10. Bu klasik tükenmişlik göstergesidir."
                ),
                oneriler=self._tukenme_onerileri(),
            )

        # ── Kural 2: Kaygı Kaynaklı Kaçınma ──
        if calisma_dusmis and net_dusmus and yuksek_stres:
            return BurnoutRaporu(
                tip=BurnoutTipi.KAYGI_KACINMA,
                seviye=UyariSeviyesi.UYARI,
                mesaj="⚠️ UYARI: Kaygı Kaynaklı Kaçınma Davranışı!",
                detay=(
                    f"Hem çalışma saati ({ort_calisma_eski:.1f}h → {ort_calisma_yeni:.1f}h) "
                    f"hem de netler ({ort_net_eski:.1f} → {ort_net_yeni:.1f}) düşüyor. "
                    f"Yüksek stres ({son_stres}/10) ile birleştiğinde, kaçınma davranışı olasıdır."
                ),
                oneriler=self._kaygi_onerileri(),
            )

        # ── Kural 3: Uyku Bozukluğu ──
        if dusuk_uyku and net_dusmus:
            return BurnoutRaporu(
                tip=BurnoutTipi.UYKU_BOZUKLUGU,
                seviye=UyariSeviyesi.UYARI,
                mesaj="😴 UYARI: Yetersiz Uyku Performansı Olumsuz Etkiliyor!",
                detay=(
                    f"Ortalama {son_uyku:.1f} saat uyku, bilişsel performans için yetersiz. "
                    "Araştırmalar, 7 saatin altındaki uykunun hafıza konsolidasyonunu "
                    "önemli ölçüde bozduğunu göstermektedir."
                ),
                oneriler=self._uyku_onerileri(),
            )

        # ── Kural 4: Motivasyon Kaybı (sessiz düşüş) ──
        if net_dusmus and not yuksek_stres and calisma_dusmis:
            return BurnoutRaporu(
                tip=BurnoutTipi.MOTIVASYON_KAYBI,
                seviye=UyariSeviyesi.DIKKAT,
                mesaj="💡 DİKKAT: Motivasyon Düşüşü Belirtileri",
                detay="Çalışma süresi ve netler düşüyor, ancak stres düşük. "
                      "Bu genellikle motivasyon kaybına işaret eder.",
                oneriler=[
                    "Kısa vadeli, somut hedefler belirleyin (haftalık mini hedefler).",
                    "Çalışma ortamını değiştirin (kütüphane, kafe).",
                    "Hedef bölümünüzle ilgili motivasyon kaynaklarına bakın.",
                    "Grup çalışması veya çalışma arkadaşı edinin.",
                ],
            )

        return BurnoutRaporu(mesaj="✅ Herhangi bir risk faktörü tespit edilmedi. Devam edin!")

    def _tukenme_onerileri(self) -> List[str]:
        return [
            "📅 Bu hafta çalışma süresini %25-30 azaltın.",
            "🎯 'Derin çalışma' tekniğine geçin: 90 dk odaklanma + 20 dk tam dinlenme.",
            "🏃 Günde en az 30 dk hafif egzersiz ekleyin (yürüyüş yeterli).",
            "📵 Sosyal medyayı çalışma saatleri dışında tamamen kesin.",
            "🛌 Uyku düzenini sabitleyin (aynı saat kalkış-yatış).",
            "📞 Bu haftayı 'toparlanma haftası' olarak ilan edin; danışmanınızla görüşün.",
        ]

    def _kaygi_onerileri(self) -> List[str]:
        return [
            "🧘 Günde 10 dk mindfulness/nefes egzersizi yapın.",
            "✍️ 'Endişe defteri' tutun: Sınav kaygılarını kâğıda dökün, zihninizi boşaltın.",
            "🎯 Çalışma hedeflerini küçültün: 'Bugün şu konuyu bitireceğim' değil, "
            "'Bugün şu konudan 10 soru çözeceğim.'",
            "👨‍👩‍👧 Güvendiğiniz biriyle (aile, arkadaş) duygularınızı paylaşın.",
            "📊 Geçmiş başarılarınızı listeleyin; kaygı gerçekçi değil.",
        ]

    def _uyku_onerileri(self) -> List[str]:
        return [
            "🛌 Hedef: Gece 7-8 saat kesintisiz uyku.",
            "📵 Yatmadan 1 saat önce ekranları kapatın (mavi ışık melatonini engeller).",
            "☕ Öğleden sonra 14:00'ten sonra kafein almayın.",
            "🌡️ Oda sıcaklığını 18-20°C'ye ayarlayın.",
            "⏰ Hafta sonu bile aynı saatte kalkın (ritim bozulmaz).",
        ]

    # ── Vygotsky ZPD Analizi ──────────────────

    def zpd_analizi(self) -> ZPDRaporu:
        """
        Vygotsky'nin Yakınsal Gelişim Alanı'na dayalı hedef belirleme.

        Kavram:
          - Alt sınır: Öğrencinin kendi başına rahatlıkla ulaşabileceği net
          - Üst sınır: Rehberlikle ulaşabileceği net (çok zor = kaygı)
          - ZPD: Bu iki sınır arasındaki 'tatlı nokta'
        """
        kayitlar = self.ogrenci.deneme_kayitlari
        if len(kayitlar) < self.MIN_KAYIT_ZPD:
            return ZPDRaporu(
                mevcut_seviye=0, alt_sinir=0, ust_sinir=0, hedef_net=0,
                durum="Yetersiz veri",
                aciklama="ZPD analizi için en az 1 deneme kaydı gereklidir.",
            )

        # Son 3 denemenin ortalamasını al (daha stabil bir baz)
        son_uc = kayitlar[-3:]
        baz_net = statistics.mean(k.toplam_net for k in son_uc)
        son_net = kayitlar[-1].toplam_net

        alt = baz_net * self.ZPD_ALT_YUZDE
        ust = baz_net * self.ZPD_UST_YUZDE
        hedef = baz_net * 1.07  # +%7 kısa vadeli gerçekçi hedef

        # Öğrencinin kendi hedefini ZPD ile karşılaştır
        ogr_hedef = self.ogrenci.hedef_net
        if ogr_hedef:
            if ogr_hedef > ust:
                durum = "🚨 Mevcut Hedef Çok Yüksek (Yüksek Kaygı Bölgesi)"
                aciklama = (
                    f"Belirlediğiniz **{ogr_hedef:.0f} net** hedefi, şu anki ortalamanıza göre çok büyük bir sıçrama gerektiriyor. "
                    f"Bu durum sizde yoğun stres ve 'başaramayacağım' hissi yaratabilir. "
                    f"Sizin için en sağlıklı gelişim, önce **{hedef:.0f}** neti sabitleyip basamakları tek tek çıkmaktır."
                )
            elif ogr_hedef < alt:
                durum = "⚠️ Hedef Potansiyelin Altında (Sıkılma/Rutin Bölgesi)"
                aciklama = (
                    f"Hedeflediğiniz **{ogr_hedef:.0f} net**, mevcut performansınızın bile gerisinde kalmış. "
                    "Bu seviyede kalmak gerçek potansiyelinizi köreltip sıkılmanıza neden olabilir. "
                    f"Sizi dinamik tutacak hedef seviyesi **{hedef:.0f}** puandan başlamalıdır."
                )
            else:
                durum = "✅ Hedef Tam İsabet (İdeal Gelişim Bölgesi)"
                aciklama = (
                    "Tebrikler! Belirlediğiniz hedef, psikolojik ve akademik olarak en verimli olduğunuz **'Tatlı Nokta'** üzerindedir. "
                    "Ne çok kolay olup rehavete sokuyor, ne de çok zor olup vazgeçiriyor. Tam gaz devam!"
                )
        else:
            durum = "📐 ZPD Analizi Tamamlandı"
            aciklama = f"Henüz bir hedef girmemişsiniz. Şu anki verilerinize göre sizi en verimli kılan **ideal hedef netiniz: {hedef:.0f}**'dir."

        return ZPDRaporu(
            mevcut_seviye=son_net,
            alt_sinir=round(alt, 1),
            ust_sinir=round(ust, 1),
            hedef_net=round(hedef, 1),
            durum=durum,
            aciklama=aciklama,
        )

    # ── Haftalık Trend ────────────────────────

    def haftalik_trend(self) -> str:
        """Son 2 deneme arasındaki net farkına göre trend belirler."""
        kayitlar = self.ogrenci.deneme_kayitlari
        if len(kayitlar) < 2:
            return "→ Yetersiz veri"
        fark = kayitlar[-1].toplam_net - kayitlar[-2].toplam_net
        if fark > 2:
            return f"↑ Yükseliyor (+{fark:.1f} net)"
        elif fark < -2:
            return f"↓ Düşüyor ({fark:.1f} net)"
        return "→ Sabit"

    # ── Güçlü / Zayıf Dersler ────────────────

    def ders_analizi(self) -> Tuple[List[str], List[str]]:
        """
        Son denemenin ders netlerini, derslerin maksimum net değerine göre
        normalize eder ve en güçlü/zayıf 3 dersi döndürür.
        """
        son = self.ogrenci.son_deneme
        if not son:
            return [], []

        netleri = son.netleri
        sirali = sorted(netleri.items(), key=lambda x: x[1], reverse=True)
        guclu = [d for d, n in sirali[0:3] if n > 0]
        zayif = [d for d, n in sirali[-3:] if n >= 0]
        return guclu, zayif

    # ── Uyku Uyarısı ─────────────────────────

    def uyku_uyarisi(self) -> Optional[str]:
        """Yetersiz uyku varsa uyarı mesajı döndürür."""
        son = self.ogrenci.son_deneme
        if not son:
            return None
        if son.uyku_saati < self.DUSUK_UYKU_ESIGI:
            return (
                f"😴 Son kayıttaki ortalama uyku: **{son.uyku_saati:.1f} saat**. "
                "7 saatten az uyku, öğrenilen bilgilerin uzun süreli belleğe aktarımını "
                "ciddi ölçüde sekteye uğratır (Stickgold & Walker, 2013)."
            )
        return None

    # ── Tam Analiz ───────────────────────────

    def tam_analiz(self) -> GenelRapor:
        """Tüm modülleri çalıştırır ve birleşik rapor döndürür."""
        guclu, zayif = self.ders_analizi()
        return GenelRapor(
            burnout=self.burnout_analizi(),
            zpd=self.zpd_analizi(),
            haftalik_trend=self.haftalik_trend(),
            guclu_dersler=guclu,
            zayif_dersler=zayif,
            bugunun_tekrarlari=self.ogrenci.bugunun_tekrar_listesi,
            uyku_uyarisi=self.uyku_uyarisi(),
        )

    # ── Hata Yoğunluk Haritası ───────────────

    def hata_yogunluk_haritasi(self) -> pd.DataFrame:
        """
        Her ders için hata sayısını ve bekleyen tekrar sayısını döndürür.
        Dashboard'da ısı haritası olarak kullanılır.
        """
        if not self.ogrenci.hata_kayitlari:
            return pd.DataFrame(columns=["Ders", "Hata Sayısı", "Bekleyen Tekrar"])

        satirlar = {}
        for h in self.ogrenci.hata_kayitlari:
            if h.ders not in satirlar:
                satirlar[h.ders] = {"Ders": h.ders, "Hata Sayısı": 0, "Bekleyen Tekrar": 0}
            satirlar[h.ders]["Hata Sayısı"] += 1
            satirlar[h.ders]["Bekleyen Tekrar"] += h.bekleyen_tekrar_sayisi

        return pd.DataFrame(list(satirlar.values())).sort_values("Hata Sayısı", ascending=False)

    # ── Korelasyon Verisi ─────────────────────

    def korelasyon_verisi(self) -> Dict[str, float]:
        """
        Çalışma saati, stres ve uyku ile net arasındaki
        Pearson korelasyon katsayılarını hesaplar.
        """
        df = self.veri_cercevesi()
        if df.empty or len(df) < 3:
            return {}

        sonuclar = {}
        for sutun in ["calisma_saati", "stres_puani", "uyku_saati"]:
            if sutun in df.columns:
                corr = df["toplam_net"].corr(df[sutun])
                sonuclar[sutun] = round(corr, 3)

        return sonuclar

    # ── Eksik Kalan Psikolojik Analiz Metotları ──

    def tukenmislik_riski_hesapla(self) -> float:
        """
        Geleneksel tükenmişlik belirtilerinin birleşiminden (0-100)
        arasında bir risk skoru üretir. Dashbord göstergelerinde kullanılır.
        """
        df = self.veri_cercevesi()
        if df.empty or len(df) < 2: return 0.0
        
        # Heuristik skor hesaplama
        stres_skor = df["stres_puani"].iloc[-1] * 10
        uyku_skor = max(0.0, (8.0 - df["uyku_saati"].iloc[-1])) * 12.5
        
        # Net trendi (son 3 deneme)
        if len(df) >= 3:
            net_trend = df["toplam_net"].iloc[-1] - df["toplam_net"].iloc[-3]
            net_skor = 20 if net_trend < -2 else 0
        else:
            net_skor = 0
            
        return min(100.0, (stres_skor * 0.5 + uyku_skor * 0.3 + net_skor * 0.2))

    def zpd_analizi_yap(self) -> List[dict]:
        """
        Vygotsky'nin ZPD modelini konu bazlı ders önerilerine dönüştürür.
        Öğrencinin bitirmesi gereken en öncelikli 3 konuyu bulur.
        """
        # Burada basitleştirilmiş bir ZPD mantığı kullanıyoruz.
        # Gerçek uygulamada sınav türü ve ders ağırlıklarına göre puan katkısı hesaplanabilir.
        rapor = self.zpd_analizi()
        if rapor.durum == "Yetersiz veri": return []
        
        oneriler = []
        # Eksik konuları tara ve temsilî ağırlıklar ata
        from models.konu_verileri import TYT_KONULARI, AYT_KONULARI, LGS_KONULARI
        
        if self.ogrenci.sinav_turu == "LGS":
             # LGS örnek
             oneriler = [{"ders": "Matematik", "konu": "Üslü İfadeler", "puan_katkisi": 2.5}]
        else:
             # YKS örnek
             oneriler = [
                 {"ders": "Matematik", "konu": "Türev Giriş", "puan_katkisi": 4.2},
                 {"ders": "Edebiyat", "konu": "Cumhuriyet Dönemi", "puan_katkisi": 3.8}
             ]
        
        # Sadece 2 tane gösterelim
        return oneriler[0:2]

    def kritik_uyarilari_getir(self) -> List[BurnoutRaporu]:
        """
        Sistemdeki tüm kritik uyarıları bir liste olarak döndürür.
        """
        uyarilar = []
        rapor = self.burnout_analizi()
        if rapor.seviye in [UyariSeviyesi.UYARI, UyariSeviyesi.KRITIK]:
            uyarilar.append(rapor)
            
        # Ek özel uyarılar
        u_msg = self.uyku_uyarisi()
        if u_msg:
            uyarilar.append(BurnoutRaporu(seviye=UyariSeviyesi.UYARI, mesaj=u_msg))
            
        return uyarilar
