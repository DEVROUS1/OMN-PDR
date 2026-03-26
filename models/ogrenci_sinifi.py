"""
OmniPDR – models/ogrenci_sinifi.py
=====================================
Veri modelleri ve OOP sınıfları.

Psikolojik Temel:
  - Zimmerman'ın Öz-Düzenlemeli Öğrenmesi: Öğrenci yalnızca akademik
    değil; uyku, stres ve çalışma saati gibi bütünsel verilerle takip edilir.
  - Ebbinghaus'un Aralıklı Tekrarı: Her hata kaydı, tekrar takvimi
    üretecek metadata ile saklanır.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


# ──────────────────────────────────────────────
# 1. YKS/LGS Ders Adları (sabit değerler)
# ──────────────────────────────────────────────
DERSLER_YKS = ["Türkçe", "Matematik", "Fizik", "Kimya", "Biyoloji",
               "Tarih", "Coğrafya", "Felsefe", "Din", "Yabancı Dil"]
DERSLER_LGS = ["Türkçe", "Matematik", "Fen Bilimleri",
               "T.C. İnkılap Tarihi", "Din Kültürü", "İngilizce"]


def _short_id() -> str:
    """Benzersiz kısa kimlik oluşturur (16'lık sistemde)."""
    val = uuid.uuid4().hex
    return str(val[0:8])


# ──────────────────────────────────────────────
# 2. GörüşmeNotu – Tarih damgalı PDR notları
# ──────────────────────────────────────────────
@dataclass
class GorusmeNotu:
    """
    Tek bir psikolojik danışma görüşmesini temsil eder.
    Her not; tarih, içerik ve danışmanın kısa değerlendirmesini içerir.
    """
    tarih: date
    icerik: str
    degerlendirme: Optional[str] = None  # Danışman yorumu
    duygu_modu: int = 3 # 1 (Kötü) - 5 (Çok İyi) arası koçluk duygu durumu
    id: str = field(default_factory=_short_id)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "tarih": self.tarih.isoformat(),
            "icerik": self.icerik,
            "degerlendirme": self.degerlendirme,
            "duygu_modu": self.duygu_modu,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "GorusmeNotu":
        v_id = d.get("id")
        if not v_id: v_id = _short_id()
        return cls(
            tarih=date.fromisoformat(d["tarih"]),
            icerik=d["icerik"],
            degerlendirme=d.get("degerlendirme"),
            duygu_modu=d.get("duygu_modu", 3),
            id=str(v_id),
        )


# ──────────────────────────────────────────────
# 3. HataKaydi – Ebbinghaus aralıklı tekrar birimi
# ──────────────────────────────────────────────
@dataclass
class HataKaydi:
    """
    Bir öğrencinin yanlış yaptığı tek bir konuyu/soruyu temsil eder.
    Ebbinghaus'un eğrisine göre tekrar tarihleri otomatik hesaplanır:
      → 1., 3., 7., 21. ve 30. günler.
    """
    ders: str
    konu: str
    hata_tarihi: date
    kaynak: str = "" # Hatanın çıktığı yayın/kitap
    id: str = field(default_factory=_short_id)
    # Tekrar tarihleri algoritma tarafından doldurulur
    tekrar_tarihleri: List[date] = field(default_factory=list)
    tamamlanan_tekrarlar: List[date] = field(default_factory=list)

    # Ebbinghaus aralık gün sayıları
    ARALIK_GUNLER: tuple = field(default=(1, 3, 7, 21, 30), init=False, repr=False)

    def __post_init__(self):
        if not self.tekrar_tarihleri:
            self._tekrar_takvimi_olustur()

    def _tekrar_takvimi_olustur(self):
        """Hata tarihinden itibaren 5 tekrar günü hesaplar."""
        from datetime import timedelta
        self.tekrar_tarihleri = [
            self.hata_tarihi + timedelta(days=g)
            for g in self.ARALIK_GUNLER
        ]

    @property
    def bugunun_tekrari_var_mi(self) -> bool:
        """Bugün herhangi bir planlı tekrar günü mü?"""
        bugun = date.today()
        return any(
            t == bugun and t not in self.tamamlanan_tekrarlar
            for t in self.tekrar_tarihleri
        )

    @property
    def bekleyen_tekrar_sayisi(self) -> int:
        """Henüz tamamlanmamış, tarihi geçmiş veya bugünkü tekrarlar."""
        bugun = date.today()
        return sum(
            1 for t in self.tekrar_tarihleri
            if t <= bugun and t not in self.tamamlanan_tekrarlar
        )

    def tekrar_tamamla(self, tarih: Optional[date] = None):
        """Bir tekrar seansını tamamlandı olarak işaretle."""
        tarih = tarih or date.today()
        if tarih not in self.tamamlanan_tekrarlar:
            self.tamamlanan_tekrarlar.append(tarih)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ders": self.ders,
            "konu": self.konu,
            "kaynak": self.kaynak,
            "hata_tarihi": self.hata_tarihi.isoformat(),
            "tekrar_tarihleri": [t.isoformat() for t in self.tekrar_tarihleri],
            "tamamlanan_tekrarlar": [t.isoformat() for t in self.tamamlanan_tekrarlar],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "HataKaydi":
        v_id = d.get("id")
        if not v_id: v_id = _short_id()
        obj = cls(
            ders=d["ders"],
            konu=d["konu"],
            kaynak=d.get("kaynak", ""),
            hata_tarihi=date.fromisoformat(d["hata_tarihi"]),
            id=str(v_id),
        )
        obj.tekrar_tarihleri = [date.fromisoformat(t) for t in d.get("tekrar_tarihleri", [])]
        obj.tamamlanan_tekrarlar = [date.fromisoformat(t) for t in d.get("tamamlanan_tekrarlar", [])]
        return obj


# ──────────────────────────────────────────────
# 4. DenemeKaydi – Haftalık sınav verisi
# ──────────────────────────────────────────────
@dataclass
class DenemeKaydi:
    """
    Bir deneme sınavının tüm verilerini barındırır.
    Akademik performans + bütünsel (uyku, stres, çalışma) verisi bir arada.
    """
    tarih: date
    netleri: dict          # {"Türkçe": 28.5, "Matematik": 22.0, ...}
    calisma_saati: float   # O haftaki toplam çalışma saati
    stres_puani: int       # 1–10 arası öznel stres skoru
    uyku_saati: float      # Günlük ortalama uyku süresi (saat)
    notlar: str = ""       # Serbest metin notlar

    @property
    def toplam_net(self) -> float:
        return sum(self.netleri.values())

    def to_dict(self) -> dict:
        return {
            "tarih": self.tarih.isoformat(),
            "netleri": self.netleri,
            "calisma_saati": self.calisma_saati,
            "stres_puani": self.stres_puani,
            "uyku_saati": self.uyku_saati,
            "notlar": self.notlar,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "DenemeKaydi":
        return cls(
            tarih=date.fromisoformat(d["tarih"]),
            netleri=d["netleri"],
            calisma_saati=d["calisma_saati"],
            stres_puani=d["stres_puani"],
            uyku_saati=d.get("uyku_saati", 7.0),
            notlar=d.get("notlar", ""),
        )


@dataclass
class OgrenciGorevi:
    """Bireysel koçlukta öğrenciye verilen haftalık ödev veya görevleri takip eder."""
    id: str
    bashik: str
    hedef_tarih: date
    tamamlandi_mi: bool = False
    olusturulma: date = date.today()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "bashik": self.bashik,
            "hedef_tarih": self.hedef_tarih.isoformat(),
            "tamamlandi_mi": self.tamamlandi_mi,
            "olusturulma": self.olusturulma.isoformat(),
        }

    @classmethod
    def from_dict(cls, d: dict) -> "OgrenciGorevi":
        v_id = d.get("id")
        if not v_id: v_id = _short_id()
        try:
            return cls(
                id=str(v_id),
                bashik=d["bashik"],
                hedef_tarih=date.fromisoformat(d["hedef_tarih"]),
                tamamlandi_mi=d.get("tamamlandi_mi", False),
                olusturulma=date.fromisoformat(d.get("olusturulma", date.today().isoformat())),
            )
        except Exception:
            # Geriye dönük veya hatalı kayıtlarda kurtarma
            return cls(id=str(v_id), bashik=str(d.get("bashik", "Bilinmeyen Görev")), hedef_tarih=date.today())


@dataclass
class Kaynak:
    """Öğrencinin sahip olduğu bir kitabı/kaynağı ve içindeki ilerlemesini temsil eder."""
    id: str
    ad: str
    ders: str
    bolum: str  # TYT, AYT veya LGS
    tamamlanan_konular: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "ad": self.ad,
            "ders": self.ders,
            "bolum": self.bolum,
            "tamamlanan_konular": self.tamamlanan_konular
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Kaynak":
        v_id = d.get("id")
        if not v_id: v_id = _short_id()
        return cls(
            id=str(v_id),
            ad=str(d["ad"]),
            ders=str(d["ders"]),
            bolum=str(d.get("bolum", "TYT")),
            tamamlanan_konular=d.get("tamamlanan_konular", [])
        )

# ──────────────────────────────────────────────
# 5. Ogrenci – Ana domain sınıfı
# ──────────────────────────────────────────────
class Ogrenci:
    """
    Sistemdeki her öğrenciyi temsil eden merkezi sınıf.
    Bireysel koçluk, CRM, akademik performans ve görevleri tek noktada toplar.
    """

    def __init__(
        self,
        ad: str,
        hedef_bolum: str,
        sinav_turu: str = "YKS",   # "YKS" veya "LGS"
        hedef_net: Optional[float] = None,
        ogrenci_id: Optional[str] = None,
        obp: float = 0.0,
        hedef_puan_turu: str = "SAY",
        hedef_siralama: Optional[int] = None,
        # Yeni Kişisel Bilgiler
        telefon: str = "",
        email: str = "",
        veli_adi: str = "",
        veli_telefon: str = "",
        hedef_uni: str = "",
        hedef_taban_puan: Optional[float] = None,
        hedef_siralama_yok: Optional[int] = None,
        user_id: Optional[str] = None, # SaaS için kullanıcı kimliği
    ):
        u_id = ogrenci_id or _short_id()
        self.ogrenci_id: str = str(u_id)
        self.user_id: Optional[str] = user_id
        self.ad: str = ad
        self.hedef_bolum: str = hedef_bolum
        self.sinav_turu: str = sinav_turu
        self.hedef_net: Optional[float] = hedef_net
        self.obp: float = obp
        self.hedef_puan_turu: str = hedef_puan_turu
        self.hedef_siralama: Optional[int] = hedef_siralama
        
        # Kişisel detaylar
        self.telefon = telefon
        self.email = email
        self.veli_adi = veli_adi
        self.veli_telefon = veli_telefon
        self.okul = okul
        self.sinif = sinif
        
        self.hedef_uni = hedef_uni
        self.hedef_taban_puan = hedef_taban_puan
        self.hedef_siralama_yok = hedef_siralama_yok
        
        self.kayit_tarihi: date = date.today()

        # Alt koleksiyonlar
        self.deneme_kayitlari: List[DenemeKaydi] = []
        self.hata_kayitlari: List[HataKaydi] = []
        self.gorusme_notlari: List[GorusmeNotu] = []
        self.gorevler: List[OgrenciGorevi] = []  # Bireysel koçluk için ödev/görev listesi
        self.konu_ilerlemeleri: dict = {}
        self.test_sonuclari: dict = {} # {test_id: {tarih, skor, sonuc_detayi}}
        self.kaynaklar: List[Kaynak] = []

    def __post_init__(self):
        """Eski verilerde eksik olabilecek yeni alanları tamamlar."""
        if not hasattr(self, "hedef_uni"): self.hedef_uni = ""
        if not hasattr(self, "hedef_taban_puan"): self.hedef_taban_puan = None
        if not hasattr(self, "hedef_siralama_yok"): self.hedef_siralama_yok = None
        if not hasattr(self, "okul"): self.okul = ""
        if not hasattr(self, "veli_adi"): self.veli_adi = ""
        if not hasattr(self, "okul"): self.okul = ""
        if not hasattr(self, "veli_telefon"): self.veli_telefon = getattr(self, "veli_tel", "")
        if not hasattr(self, "telefon"): self.telefon = ""
        if not hasattr(self, "sinif"): self.sinif = ""
        if not hasattr(self, "email"): self.email = ""
        if not hasattr(self, "gorevler"): self.gorevler = []
        if not hasattr(self, "kaynaklar"): self.kaynaklar = []

    # ── Veri ekleme yardımcıları ──────────────────

    def deneme_ekle(self, kayit: DenemeKaydi) -> None:
        """Yeni bir deneme kaydı ekler (tarihe göre sıralı tutar)."""
        self.deneme_kayitlari.append(kayit)
        self.deneme_kayitlari.sort(key=lambda d: d.tarih)

    def hata_ekle(self, ders: str, konu: str, tarih: Optional[date] = None) -> HataKaydi:
        """
        Yeni bir konu hatası ekler ve otomatik olarak Ebbinghaus
        takvimi oluşturur.
        """
        kayit = HataKaydi(ders=ders, konu=konu, hata_tarihi=tarih or date.today())
        self.hata_kayitlari.append(kayit)
        return kayit

    def gorusme_ekle(self, icerik: str, degerlendirme: Optional[str] = None, duygu_modu: int = 3, tarih: Optional[date] = None):
        """Öğrencinin profilinde yeni bir PDR veya Koçluk notu oluşturur."""
        notumuz = GorusmeNotu(
            tarih=tarih or date.today(),
            icerik=icerik,
            degerlendirme=degerlendirme,
            duygu_modu=duygu_modu,
        )
        self.gorusme_notlari.append(notumuz)
        self.gorusme_notlari.sort(key=lambda n: n.tarih)
        
    def gorev_ekle(self, bashik: str, hedefe_kalan_gun: int = 7) -> OgrenciGorevi:
        from datetime import timedelta
        g = OgrenciGorevi(id=str(uuid.uuid4())[0:8], bashik=bashik, hedef_tarih=date.today() + timedelta(days=hedefe_kalan_gun))
        self.gorevler.append(g)
        return g

    def kaynak_ekle(self, ad: str, ders: str, bolum: str = "TYT") -> Kaynak:
        """Yeni bir kaynak kitap ekler."""
        k = Kaynak(id=_short_id(), ad=ad, ders=ders, bolum=bolum)
        self.kaynaklar.append(k)
        return k

    def konu_ilerlemesi_guncelle(self, bolum: str, ders: str, konu: str, tamamlandi: bool):
        """Konu tamamlama durumunu günceller."""
        if bolum not in self.konu_ilerlemeleri:
            self.konu_ilerlemeleri[bolum] = {}
        if ders not in self.konu_ilerlemeleri[bolum]:
            self.konu_ilerlemeleri[bolum][ders] = {}
        self.konu_ilerlemeleri[bolum][ders][konu] = tamamlandi

    def konu_tamamlandi_mi(self, bolum: str, ders: str, konu: str) -> bool:
        """Belirli bir konunun tamamlanıp tamamlanmadığını döndürür."""
        try:
            return self.konu_ilerlemeleri[bolum][ders][konu]
        except (KeyError, TypeError):
            return False
        
    def test_sonucu_ekle(self, test_id: str, sonuc_verisi: dict):
        """PDR test sonucunu kaydeder."""
        if test_id not in self.test_sonuclari:
            self.test_sonuclari[test_id] = []
        self.test_sonuclari[test_id].append(sonuc_verisi)

    # ── Hesaplama özellikleri ──────────────────

    @property
    def son_deneme(self) -> Optional[DenemeKaydi]:
        return self.deneme_kayitlari[-1] if self.deneme_kayitlari else None

    @property
    def bugunun_tekrar_listesi(self) -> List[HataKaydi]:
        """Bugün tekrar edilmesi gereken konular."""
        return [h for h in self.hata_kayitlari if h.bugunun_tekrari_var_mi]

    @property
    def bekleyen_tekrar_sayisi(self) -> int:
        return sum(h.bekleyen_tekrar_sayisi for h in self.hata_kayitlari)

    @property
    def dersler(self) -> List[str]:
        """Sınav türüne göre ders listesi."""
        return DERSLER_YKS if self.sinav_turu == "YKS" else DERSLER_LGS

    # ── Serileştirme ──────────────────────────

    def to_dict(self) -> dict:
        return {
            "ogrenci_id": self.ogrenci_id,
            "ad": self.ad,
            "hedef_bolum": self.hedef_bolum,
            "sinav_turu": self.sinav_turu,
            "hedef_net": self.hedef_net,
            "obp": self.obp,
            "hedef_puan_turu": self.hedef_puan_turu,
            "hedef_siralama": self.hedef_siralama,
            "user_id": self.user_id,
            # Yeni alanlar
            "telefon": self.telefon,
            "email": self.email,
            "veli_adi": self.veli_adi,
            "veli_telefon": self.veli_telefon,
            "okul": self.okul,
            "sinif": self.sinif,
            "hedef_uni": self.hedef_uni,
            "hedef_taban_puan": self.hedef_taban_puan,
            "hedef_siralama_yok": self.hedef_siralama_yok,
            
            "kayit_tarihi": self.kayit_tarihi.isoformat(),
            "deneme_kayitlari": [d.to_dict() for d in self.deneme_kayitlari],
            "hata_kayitlari": [h.to_dict() for h in self.hata_kayitlari],
            "gorusme_notlari": [g.to_dict() for g in self.gorusme_notlari],
            "gorevler": [g.to_dict() for g in getattr(self, "gorevler", [])],
            "konu_ilerlemeleri": self.konu_ilerlemeleri,
            "test_sonuclari": self.test_sonuclari,
            "kaynaklar": [k.to_dict() for k in self.kaynaklar],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Ogrenci":
        ogr = cls(
            ad=d["ad"],
            hedef_bolum=d["hedef_bolum"],
            sinav_turu=d.get("sinav_turu", "YKS"),
            hedef_net=d.get("hedef_net"),
            ogrenci_id=d.get("ogrenci_id"),
            obp=d.get("obp", 0.0),
            hedef_puan_turu=d.get("hedef_puan_turu", "SAY"),
            hedef_siralama=d.get("hedef_siralama"),
            # Yeni alanlar (geriye dönük uyumluluk için .get)
            telefon=d.get("telefon", ""),
            email=d.get("email", ""),
            veli_adi=d.get("veli_adi", ""),
            veli_telefon=str(d.get("veli_telefon", d.get("veli_tel", ""))),
            okul=d.get("okul", ""),
            sinif=d.get("sinif", ""),
            hedef_uni=d.get("hedef_uni", ""),
            hedef_taban_puan=d.get("hedef_taban_puan"),
            hedef_siralama_yok=d.get("hedef_siralama_yok"),
            user_id=d.get("user_id"),
        )
        ogr.kayit_tarihi = date.fromisoformat(d.get("kayit_tarihi", date.today().isoformat()))        # Alt listeler doldurulur
        ogr.deneme_kayitlari = [DenemeKaydi.from_dict(dk) for dk in d.get("deneme_kayitlari", [])]
        ogr.hata_kayitlari = [HataKaydi.from_dict(hk) for hk in d.get("hata_kayitlari", [])]
        ogr.gorusme_notlari = [GorusmeNotu.from_dict(gn) for gn in d.get("gorusme_notlari", [])]
        ogr.gorevler = [OgrenciGorevi.from_dict(g) for g in d.get("gorevler", [])]
        ogr.konu_ilerlemeleri = d.get("konu_ilerlemeleri", {})
        ogr.test_sonuclari = d.get("test_sonuclari", {})
        ogr.kaynaklar = [Kaynak.from_dict(k) for k in d.get("kaynaklar", [])]
        
        return ogr

    def __repr__(self) -> str:
        return f"<Ogrenci '{self.ad}' | {self.sinav_turu} | {len(self.deneme_kayitlari)} deneme>"
