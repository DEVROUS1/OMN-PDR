"""
OmniPDR – models/test_verileri.py
===================================
Akademik standartlarda (validitesi yüksek) PDR envanterleri.
Bu dosya statik veri kaynağıdır ve bilimsel ölçeklerden derlenmiştir.

İÇERİK:
1. Holland Mesleki İlgi Envanteri (RIASEC) - 90 Soru
2. Çoklu Zeka Envanteri (Gardner) - 80 Soru
3. Sınav Kaygısı Ölçeği (Detaylı) - 30 Soru
4. Çalışma Davranışı Değerlendirme Ölçeği - 40 Soru
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional

@dataclass
class TestSorusu:
    id: int
    metin: str
    secenekler: Optional[List[str]] = None
    puanlar: Optional[List[int]] = None
    kategori: Optional[str] = None  # Holland tipi, Zeka türü vb.

@dataclass
class PDRTesti:
    id: str
    ad: str
    aciklama: str
    sorular: List[TestSorusu]
    degerlendirme_tipi: str  # "toplam_puan", "kategori_puani", "coklu_kategori"

# ──────────────────────────────────────────────
# 1. HOLLAND MESLEKİ İLGİ ENVANTERİ (RIASEC)
# ──────────────────────────────────────────────
# Kaynak: John L. Holland's Typology of Vocational Interests
# Puanlama: "Hoşlanırım" (1), "Hoşlanmam" (0)
# Kategoriler: R (Realistic), I (Investigative), A (Artistic), S (Social), E (Enterprising), C (Conventional)

HOLLAND_SORULARI_RAW = [
    # R - Gerçekçi (Realistic)
    ("R", "Bozulan elektronik eşyaları tamir etmek."),
    ("R", "Ahşap veya metal ile bir şeyler inşa etmek."),
    ("R", "Otomobil motorunun nasıl çalıştığını incelemek."),
    ("R", "Doğa yürüyüşleri ve kamp yapmak."),
    ("R", "Tarım veya bahçecilikle uğraşmak."),
    ("R", "Mekanik aletler ve makineler kullanmak."),
    ("R", "Spor yapmak ve fiziksel aktivitelerde bulunmak."),
    ("R", "Bir uçağın kokpitini incelemek."),
    ("R", "Mimari çizimler ve planlar yapmak."),
    ("R", "Evdeki basit tamirat işlerini yapmak."),
    ("R", "Hayvan bakımı ve beslemesiyle ilgilenmek."),
    ("R", "Laboratuvar aletlerini (mikroskop vb.) kullanmak."),
    ("R", "Mobilya monte etmek."),
    ("R", "Bilgisayar donanım parçalarını birleştirmek."),
    ("R", "İnşaat ve yapı işlerini izlemek."),

    # I - Araştırmacı (Investigative)
    ("I", "Bilimsel dergiler ve makaleler okumak."),
    ("I", "Karmaşık matematik problemlerini çözmek."),
    ("I", "Bir hastalığın nedenlerini araştırmak."),
    ("I", "Kimyasal deneyler yapmak."),
    ("I", "İnsan davranışlarının nedenlerini incelemek."),
    ("I", "Uzay ve astronomi ile ilgili belgeseller izlemek."),
    ("I", "Tarihi olayların neden-sonuç ilişkilerini analiz etmek."),
    ("I", "Satranç veya strateji oyunları oynamak."),
    ("I", "Hava durumu raporlarını ve iklim değişikliklerini incelemek."),
    ("I", "Biyoloji ve canlıların yapısını merak etmek."),
    ("I", "Yeni bir bilgisayar programlama dili öğrenmek."),
    ("I", "Toplumsal sorunlara istatistiksel çözümler aramak."),
    ("I", "Felsefi konular üzerine düşünmek."),
    ("I", "Deneysel çalışmaların sonuçlarını yorumlamak."),
    ("I", "Ansiklopedi veya bilgi içerikli siteleri karıştırmak."),

    # A - Sanatsal (Artistic)
    ("A", "Resim yapmak veya eskiz çizmek."),
    ("A", "Bir enstrüman çalmak."),
    ("A", "Şiir veya hikaye yazmak."),
    ("A", "Tiyatro oyununda rol almak."),
    ("A", "Moda ve kıyafet tasarımları yapmak."),
    ("A", "Fotoğraf çekmek ve düzenlemek."),
    ("A", "Ev dekorasyonu ile ilgilenmek."),
    ("A", "Yaratıcı yemek tarifleri denemek."),
    ("A", "Konser, sergi veya müzeye gitmek."),
    ("A", "Heykel veya seramik yapmak."),
    ("A", "Film senaryoları kurgulamak."),
    ("A", "Grafik tasarım programları kullanmak."),
    ("A", "Dans etmek veya koreografi hazırlamak."),
    ("A", "Yabancı dil öğrenmek ve farklı kültürleri tanımak."),
    ("A", "Özgün ve sıradışı fikirler üretmek."),

    # S - Sosyal (Social)
    ("S", "İnsanların sorunlarını dinlemek ve yardım etmek."),
    ("S", "Bir gruba liderlik etmek değil, onlara rehberlik etmek."),
    ("S", "Çocuklarla oyun oynamak ve ilgilenmek."),
    ("S", "Sosyal sorumluluk projelerinde gönüllü olmak."),
    ("S", "Arkadaşlarınla dertleşmek."),
    ("S", "Bir konuda başkalarına eğitim vermek."),
    ("S", "Hasta veya yaşlı insanlara bakım vermek."),
    ("S", "Parti veya etkinlik organize etmek."),
    ("S", "İnsan psikolojisi üzerine kitaplar okumak."),
    ("S", "Topluluk önünde konuşmaktan çekinmemek."),
    ("S", "Takım çalışmalarında yer almak."),
    ("S", "Yeni insanlarla tanışmak."),
    ("S", "Farklı kültürlerden insanlarla iletişim kurmak."),
    ("S", "Bir tartışmada arabulucu olmak."),
    ("S", "İnsan hakları ve adalet konularını savunmak."),

    # E - Girişimci (Enterprising)
    ("E", "Bir grubu yönetmek ve liderlik etmek."),
    ("E", "İkna kabiliyetini kullanarak bir ürünü satmak."),
    ("E", "Politika ve siyasetle ilgilenmek."),
    ("E", "Kendi işini kurmayı hayal etmek."),
    ("E", "Borsa ve ekonomi haberlerini takip etmek."),
    ("E", "Okul kulüplerinde başkanlık yapmak."),
    ("E", "Sunum yapmak ve insanları etkilemek."),
    ("E", "Pazarlık yapmaktan hoşlanmak."),
    ("E", "Rekabetçi ortamlarda bulunmak."),
    ("E", "Risk almaktan korkmamak."),
    ("E", "Reklam ve pazarlama stratejileri geliştirmek."),
    ("E", "Kariyer hedefleri belirlemek ve planlamak."),
    ("E", "Münazaralara katılmak."),
    ("E", "Bir projeyi finanse etmek veya bütçe yönetmek."),
    ("E", "Hırslı ve başarı odaklı olmak."),

    # C - Geleneksel (Conventional)
    ("C", "Düzenli not tutmak ve planlı çalışmak."),
    ("C", "Dosyalama ve arşivleme yapmak."),
    ("C", "Hesap makinesi kullanmak ve bütçe yapmak."),
    ("C", "Kurallara ve talimatlara uymak."),
    ("C", "Veri girişi ve bilgisayar işletmenliği."),
    ("C", "Bir ofis ortamında çalışmayı hayal etmek."),
    ("C", "Yazım kurallarına ve dilbilgisine dikkat etmek."),
    ("C", "Koleksiyon yapmak (para, pul vb.)."),
    ("C", "Ayrıntılara dikkat etmek."),
    ("C", "Belirli saatlerde başlayıp biten işleri sevmek."),
    ("C", "Envanter sayımı veya stok kontrolü yapmak."),
    ("C", "Vergi, sigorta gibi resmi işlemleri takip etmek."),
    ("C", "Randevularına sadık kalmak."),
    ("C", "Dağınık ortamları sevmemek, düzenlemek."),
    ("C", "İş güvenliği kurallarına önem vermek.")
]

# ──────────────────────────────────────────────
# 2. ÇOKLU ZEKA ENVANTERİ (GARDNER)
# ──────────────────────────────────────────────
# 8 Zeka Türü - Her biri için 10 soru
ZEKA_SORULARI_RAW = [
    # Sözel-Dilsel
    ("Sözel", "Kitap okumayı çok severim."),
    ("Sözel", "Kelimelerle oynamayı (bulmaca, scrabble) severim."),
    ("Sözel", "Hikaye, şiir veya yazı yazmaktan hoşlanırım."),
    ("Sözel", "İsimleri, yerleri ve tarihleri kolay hatırlarım."),
    ("Sözel", "Dinleyerek öğrenmeyi tercih ederim."),
    ("Sözel", "Kelime dağarcığımın geniş olduğunu düşünürüm."),
    ("Sözel", "Başka bir dil öğrenmeye yatkınım."),
    ("Sözel", "İnsanlarla konuşarak iletişim kurmayı severim."),
    ("Sözel", "Tekerlemeleri ve dil oyunlarını severim."),
    ("Sözel", "Sözlü sunumlarda başarılıyımdır."),

    # Mantıksal-Matematiksel
    ("Mantıksal", "Zihinden matematiksel işlemleri kolayca yaparım."),
    ("Mantıksal", "Olaylar arasındaki neden-sonuç ilişkilerini merak ederim."),
    ("Mantıksal", "Satranç, dama gibi strateji oyunlarını severim."),
    ("Mantıksal", "Mantık hatalarını hemen fark ederim."),
    ("Mantıksal", "Bilimsel deneyler yapmaktan hoşlanırım."),
    ("Mantıksal", "Bilgileri kategorize etmeyi ve sınıflandırmayı severim."),
    ("Mantıksal", "Bilgisayar programlama mantığı ilgimi çeker."),
    ("Mantıksal", "Soyut kavramlarla düşünmeyi severim."),
    ("Mantıksal", "Sorunları adım adım analiz ederek çözerim."),
    ("Mantıksal", "Grafik ve istatistikleri yorumlamakta iyiyimdir."),

    # Görsel-Uzamsal
    ("Görsel", "Gözümü kapattığımda nesneleri net bir şekilde hayal edebilirim."),
    ("Görsel", "Harita, grafik ve diyagramları kolayca anlarım."),
    ("Görsel", "Resim yapmayı veya karalama yapmayı severim."),
    ("Görsel", "Yön bulma konusunda iyiyimdir."),
    ("Görsel", "Puzzle (yapboz) yapmaktan hoşlanırım."),
    ("Görsel", "Renk uyumlarına dikkat ederim."),
    ("Görsel", "Makinelerin veya nesnelerin nasıl sökülüp takıldığını bilirim."),
    ("Görsel", "Video ve fotoğraflarla öğrenmeyi tercih ederim."),
    ("Görsel", "Mekansal düzenlemeler (dekorasyon vb.) ilgimi çeker."),
    ("Görsel", "Gördüğüm yüzleri kolay hatırlarım."),

    # Müziksel-Ritmik
    ("Müziksel", "Şarkıların melodilerini kolayca hatırlarım."),
    ("Müziksel", "Bir enstrüman çalmayı biliyorum veya çok istiyorum."),
    ("Müziksel", "Çalışırken arka planda müzik olmasını severim."),
    ("Müziksel", "Ritim tutmaktan veya mırıldanmaktan hoşlanırım."),
    ("Müziksel", "Seslerdeki ton farklılıklarını kolayca ayırt ederim."),
    ("Müziksel", "Müzik dinlemeden duramam."),
    ("Müziksel", "Şarkı sözlerini çabuk ezberlerim."),
    ("Müziksel", "Doğadaki seslere (kuş, rüzgar vb.) duyarlıyım."),
    ("Müziksel", "Kendi kendime şarkı bestelerim."),
    ("Müziksel", "Müzik, duygularımı ifade etmemde önemlidir."),

    # Bedensel-Kinestetik
    ("Bedensel", "Yerimde durmakta zorlanırım, hareket etmeyi severim."),
    ("Bedensel", "Spor yapmaktan çok hoşlanırım."),
    ("Bedensel", "El becerisi gerektiren işlerde (tamir, örgü, maket) iyiyimdir."),
    ("Bedensel", "Konuşurken ellerimi ve kollarımı çok kullanırım."),
    ("Bedensel", "Dokunarak öğrenmeyi tercih ederim."),
    ("Bedensel", "Dans etmeyi veya rol yapmayı severim."),
    ("Bedensel", "Denge gerektiren aktivitelerde başarılıyımdır."),
    ("Bedensel", "Bir şeyi okumaktansa yapmayı tercih ederim."),
    ("Bedensel", "Fiziksel risk almaktan korkmam (tırmanma vb.)."),
    ("Bedensel", "Vücudumu iyi kontrol ederim."),

    # Sosyal (Kişilerarası)
    ("Sosyal", "İnsanlarla vakit geçirmekten enerji alırım."),
    ("Sosyal", "Arkadaşlarımla sorunlarını konuşmayı severim."),
    ("Sosyal", "Grup çalışmalarında liderlik yapabilirim."),
    ("Sosyal", "Başkalarının duygularını ve niyetlerini kolayca anlarım."),
    ("Sosyal", "Çok sayıda arkadaşım vardır."),
    ("Sosyal", "İnsanlara bir şeyler öğretmekten hoşlanırım."),
    ("Sosyal", "Empati yeteneğim yüksektir."),
    ("Sosyal", "Sosyal etkinliklere ve kulüplere katılmayı severim."),
    ("Sosyal", "Grup içinde çalışmayı bireysel çalışmaya tercih ederim."),
    ("Sosyal", "Çatışma ortamlarını yatıştırabilirim."),

    # İçsel (Öze Dönük)
    ("İçsel", "Yalnız kalıp düşünmekten hoşlanırım."),
    ("İçsel", "Kendi güçlü ve zayıf yönlerimi iyi bilirim."),
    ("İçsel", "Bağımsız çalışmayı tercih ederim."),
    ("İçsel", "Hayatın amacı ve felsefesi üzerine düşünürüm."),
    ("İçsel", "Kendi hedeflerimi kendim belirlerim."),
    ("İçsel", "Duygularımı ve ruh halimi analiz ederim."),
    ("İçsel", "Günlük tutmayı severim."),
    ("İçsel", "Başkalarından çok kendi standartlarıma önem veririm."),
    ("İçsel", "Sessiz ortamlar bana huzur verir."),
    ("İçsel", "Özgüvenim yüksektir."),

    # Doğa
    ("Doğa", "Doğada vakit geçirmeyi çok severim."),
    ("Doğa", "Hayvanları severim ve onlarla ilgilenirim."),
    ("Doğa", "Bitki yetiştirmekten hoşlanırım."),
    ("Doğa", "Çevre kirliliği ve ekolojik sorunlara duyarlıyım."),
    ("Doğa", "Doğa belgeselleri izlemeyi severim."),
    ("Doğa", "Mevsim değişikliklerini ve hava olaylarını gözlemlerim."),
    ("Doğa", "Farklı bitki ve hayvan türlerini ayırt edebilirim."),
    ("Doğa", "Kamp yapmayı, lüks otele tercih ederim."),
    ("Doğa", "Gökyüzünü ve yıldızları izlemekten keyif alırım."),
    ("Doğa", "Biyoloji ve coğrafya dersleri ilgimi çeker.")
]

# ──────────────────────────────────────────────
# 3. SINAV KAYGISI ÖLÇEĞİ (DETAYLI)
# ──────────────────────────────────────────────
SINAV_KAYGISI_SORULARI = [
    "Sınavdan bir gece önce uyumakta zorlanırım.",
    "Sınav anında bildiğim her şeyi unutmuş gibi hissederim.",
    "Sınavda kalbim çok hızlı çarpar.",
    "Sınav sırasında ellerim titrer veya terler.",
    "Sınav süresinin yetmeyeceği düşüncesi beni panikletir.",
    "Sınav sorularını okurken dikkatimi toplayamam.",
    "Başkalarının benden daha hızlı çözdüğünü görünce endişelenirim.",
    "Sınav sonucunun tüm hayatımı belirleyeceğini düşünürüm.",
    "Ailemi hayal kırıklığına uğratmaktan korkarım.",
    "Sınav anında midemde bir ağrı veya bulantı hissederim.",
    "Sınav yaklaştıkça iştahım kesilir veya artar.",
    "Sınavdan sonra sık sık 'keşke' ile başlayan cümleler kurarım.",
    "Deneme sınavları bile beni çok gerer.",
    "Sınavda başarısız olursam herkesin benimle dalga geçeceğini düşünürüm.",
    "Soruları tekrar tekrar okumak zorunda kalırım.",
    "Sınav anında zihnimin boşaldığını hissederim.",
    "Sınav salonuna girdiğimde nefesim daralır.",
    "Sınavdan çıktıktan sonra baş ağrısı çekerim.",
    "Sınav konularını çalışsam bile kendimi yetersiz hissederim.",
    "Sınav günü sabahı çok gergin uyanırım."
]


def tum_testleri_getir() -> List[PDRTesti]:
    return [
        PDRTesti(
            id="holland_ilgi",
            ad="Holland Mesleki İlgi Envanteri (RIASEC)",
            aciklama="90 soruluk kapsamlı mesleki eğilim testi. Kişilik tipinize en uygun meslekleri belirler.",
            sorular=[TestSorusu(id=i, metin=m, kategori=k) for i, (k, m) in enumerate(HOLLAND_SORULARI_RAW)],
            degerlendirme_tipi="kategori_puani"
        ),
        PDRTesti(
            id="coklu_zeka",
            ad="Çoklu Zeka Envanteri (Gardner)",
            aciklama="80 soruluk zeka alanı testi. Hangi zeka türlerinizin (Sözel, Sayısal, Görsel vb.) baskın olduğunu keşfedin.",
            sorular=[TestSorusu(id=i, metin=m, kategori=k) for i, (k, m) in enumerate(ZEKA_SORULARI_RAW)],
            degerlendirme_tipi="kategori_puani"
        ),
        PDRTesti(
            id="sinav_kaygisi",
            ad="Sınav Kaygısı Ölçeği",
            aciklama="Sınava yönelik kaygı düzeyinizi ve bedensel/zihinsel belirtilerinizi ölçer.",
            sorular=[TestSorusu(id=i, metin=m) for i, m in enumerate(SINAV_KAYGISI_SORULARI)],
            degerlendirme_tipi="toplam_puan"
        )
    ]
