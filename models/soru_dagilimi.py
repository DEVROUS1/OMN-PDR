"""
OmniPDR – models/soru_dagilimi.py
===================================
TYT ve AYT derslerine ait son 5 yılın (2021-2025) konu bazlı soru dağılımı verileri.
2025 verileri, MEB müfredatı ve ÖSYM kazanımlarına dayalı projeksiyonlardır.
"""

from typing import Dict, List

# Yıllar sütunu: 2025, 2024, 2023, 2022, 2021, 2020
YILLAR = ["2025", "2024", "2023", "2022", "2021", "2020"]

TYT_DAGILIM: Dict[str, Dict[str, List[int]]] = {
    "Türkçe": {
        "Ses Bilgisi": [
            0,
            0,
            1,
            0,
            1,
            0
        ],
        "Dil Bilgisi": [
            3,
            0,
            2,
            3,
            2,
            3
        ],
        "Noktalama İşaretleri": [
            2,
            2,
            2,
            2,
            2,
            2
        ],
        "Yazım Kuralları": [
            2,
            2,
            2,
            2,
            2,
            2
        ],
        "Anlatım Bozukluğu": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "Paragraf": [
            26,
            26,
            26,
            26,
            25,
            26
        ],
        "Cümlede Anlam": [
            3,
            5,
            4,
            3,
            3,
            6
        ],
        "Sözcükte Anlam": [
            4,
            5,
            3,
            4,
            5,
            1
        ]
    },
    "Fizik": {
        "Fizik Bilimine Giriş": [
            0,
            0,
            0,
            0,
            0,
            1
        ],
        "Madde Ve Özellikleri": [
            1,
            1,
            1,
            1,
            1,
            0
        ],
        "Sıvıların Kaldırma Kuvveti": [
            0,
            1,
            0,
            0,
            0,
            1
        ],
        "Basınç": [
            0,
            0,
            0,
            1,
            1,
            0
        ],
        "Isı, Sıcaklık ve Genleşme": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Hareket ve Kuvvet": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Dinamik": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "İş, Güç ve Enerji": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "Elektrostatik": [
            1,
            0,
            0,
            0,
            0,
            0
        ],
        "Elektrik Akımı ve Devreler": [
            0,
            0,
            2,
            0,
            0,
            1
        ],
        "Elektriksel Enerji ve Güç": [
            0,
            0,
            0,
            1,
            1,
            0
        ],
        "Optik": [
            1,
            1,
            2,
            1,
            1,
            1
        ],
        "Manyetizma": [
            1,
            1,
            0,
            0,
            0,
            0
        ],
        "Dalgalar": [
            1,
            1,
            0,
            1,
            1,
            1
        ]
    },
    "Kimya": {
        "SORU SAYISI": [
            7,
            7,
            7,
            7,
            7,
            7
        ],
        "Kimya Bilimi": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Atomun Yapısı": [
            1,
            1,
            0,
            0,
            0,
            1
        ],
        "Periyodik Tablo": [
            0,
            0,
            1,
            1,
            1,
            0
        ],
        "Maddenin Halleri": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Kimyasal Türler Arası Etkileşimler": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Kimyasal Hesaplamalar": [
            1,
            1,
            0,
            0,
            1,
            1
        ],
        "Kimyanın Temel Kanunları": [
            0,
            0,
            1,
            1,
            0,
            0
        ],
        "Asit, Baz ve Tuz": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Karışımlar": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Kimya Her Yerde": [
            0,
            0,
            0,
            0,
            0,
            0
        ]
    },
    "Biyoloji": {
        "SORU SAYISI": [
            6,
            6,
            6,
            6,
            6,
            6
        ],
        "Canlıların Ortak Özellikleri": [
            1,
            0,
            0,
            1,
            0,
            0
        ],
        "Canlıların Temel Bileşenleri": [
            0,
            1,
            1,
            0,
            1,
            1
        ],
        "Hücre ve Organelleri": [
            0,
            1,
            1,
            1,
            1,
            1
        ],
        "Madde Geçişleri": [
            1,
            0,
            0,
            0,
            0,
            0
        ],
        "Canlıların Sınıflandırılması": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Hücre Bölünmeleri ve Üreme": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Kalıtım": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Ekosistem Ekoloji": [
            0,
            1,
            1,
            1,
            1,
            1
        ],
        "Bitkiler Biyolojisi": [
            1,
            0,
            0,
            0,
            0,
            0
        ]
    },
    "Tarih": {
        "SORU SAYISI": [
            5,
            5,
            5,
            5,
            5,
            5
        ],
        "Tarih ve Zaman": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "İlk ve Orta Çağlarda Türk Dünyası": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "İslam Medeniyetinin Doğuşu": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "Türklerin İslamiyet'i Kabulü ve İlk Türk İslam Devletleri": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Beylikten Devlete Osmanlı": [
            1,
            0,
            0,
            1,
            0,
            0
        ],
        "Dünya Gücü Osmanlı": [
            0,
            1,
            0,
            0,
            0,
            0
        ],
        "Değişim Çağında Avrupa ve Osmanlı": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "Uluslararası İlişkilerde Denge Stratejisi (1774-1914)": [
            0,
            0,
            1,
            0,
            1,
            1
        ],
        "XX. Yüzyıl Başlarında Osmanlı Devleti ve Dünya": [
            0,
            0,
            0,
            0,
            0,
            1
        ],
        "Milli Mücadele": [
            1,
            1,
            2,
            1,
            1,
            1
        ],
        "Atatürkçülük ve Türk İnkılabı": [
            1,
            1,
            0,
            1,
            1,
            0
        ]
    },
    "Coğrafya": {
        "SORU SAYISI": [
            5,
            5,
            5,
            5,
            5,
            5
        ],
        "Doğa ve İnsan": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "Dünya'nın Şekli ve Hareketleri": [
            0,
            0,
            0,
            0,
            1,
            0
        ],
        "Coğrafi Konum": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "Harita Bilgisi": [
            1,
            1,
            0,
            1,
            0,
            1
        ],
        "Atmosfer ve Sıcaklık": [
            0,
            0,
            1,
            0,
            0,
            1
        ],
        "İklim Bilgisi": [
            1,
            1,
            1,
            1,
            1,
            0
        ],
        "İç ve Dış Kuvvetler": [
            0,
            0,
            0,
            1,
            1,
            1
        ],
        "Nüfus ve Yerleşme": [
            1,
            1,
            2,
            0,
            1,
            1
        ],
        "Türkiye'nin Yer Şekilleri": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "Ekonomik Faaliyetler": [
            0,
            0,
            0,
            1,
            0,
            0
        ],
        "Bölgeler": [
            1,
            1,
            0,
            0,
            1,
            1
        ],
        "Uluslararası Ulaşım Hatları": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "Doğal Afetler": [
            1,
            1,
            1,
            1,
            0,
            0
        ]
    },
    "Felsefe": {
        "SORU SAYISI": [
            5,
            5,
            5,
            5,
            5,
            5
        ],
        "Felsefenin Alanı": [
            0,
            1,
            2,
            1,
            2,
            0
        ],
        "Bilgi Felsefesi": [
            3,
            1,
            2,
            2,
            0,
            1
        ],
        "Bilim Felsefesi": [
            1,
            0,
            0,
            0,
            0,
            0
        ],
        "Varlık Felsefesi": [
            0,
            1,
            0,
            1,
            1,
            1
        ],
        "Ahlak Felsefesi": [
            1,
            1,
            1,
            1,
            0,
            2
        ],
        "Siyaset Felsefesi": [
            0,
            0,
            0,
            0,
            1,
            0
        ],
        "Din Felsefesi": [
            0,
            1,
            0,
            0,
            0,
            1
        ],
        "Sanat Felsefesi": [
            0,
            0,
            0,
            0,
            1,
            0
        ]
    },
    "Din Kültürü": {
        "Bilgi ve İnanç": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "İbadetler": [
            1,
            1,
            1,
            1,
            1,
            0
        ],
        "Ahlak ve Değerler": [
            1,
            1,
            1,
            1,
            1,
            1
        ],
        "Hz. Muhammed (S.A.V)": [
            1,
            1,
            0,
            0,
            0,
            1
        ],
        "Vahiy ve Akıl": [
            0,
            0,
            1,
            1,
            1,
            2
        ],
        "İslam Düşüncesinde Yorumlar, Mezhepler": [
            1,
            1,
            0,
            0,
            0,
            0
        ],
        "Din, Kültür ve Medeniyet": [
            0,
            0,
            1,
            1,
            1,
            0
        ]
    }
}

# Temel Matematik TYT dağılımı (soru_dagilimi formatında)
TYT_DAGILIM["Temel Matematik"] = {
    "Temel Kavramlar": [3, 3, 3, 3, 3, 1],
    "Sayı Basamakları": [2, 2, 1, 1, 2, 1],
    "Bölme-Bölünebilme": [1, 1, 1, 1, 1, 1],
    "EBOB-EKOK": [0, 0, 1, 0, 0, 1],
    "Rasyonel Sayılar": [1, 1, 2, 2, 1, 1],
    "Basit Eşitsizlikler": [1, 1, 1, 1, 2, 1],
    "Mutlak Değer": [1, 1, 1, 1, 1, 1],
    "Üslü Sayılar": [1, 1, 1, 1, 1, 1],
    "Köklü Sayılar": [1, 1, 1, 1, 1, 1],
    "Oran-Orantı": [1, 1, 1, 0, 1, 1],
    "Denklem Çözme": [1, 1, 1, 1, 1, 0],
    "Problemler": [8, 7, 8, 8, 8, 8],
    "Yüzde-Faiz": [2, 2, 2, 1, 1, 2],
    "Kümeler": [1, 1, 1, 1, 1, 1],
    "Fonksiyonlar": [1, 1, 2, 1, 1, 2],
    "Permütasyon-Kombinasyon": [0, 0, 1, 1, 0, 1],
    "Olasılık": [1, 1, 1, 1, 1, 1],
    "İstatistik": [1, 1, 1, 1, 1, 1],
    "Veri Yorumlama": [1, 1, 1, 0, 2, 1],
}

AYT_DAGILIM: Dict[str, Dict[str, List[int]]] = {
    "Matematik": {
        "SORU SAYISI": [
            29,
            32,
            32,
            32,
            32,
            30
        ],
        "Temel Kavramlar": [
            3,
            2,
            4,
            2,
            3,
            2
        ],
        "Sayı Basamakları": [
            0,
            1,
            0,
            0,
            0,
            3
        ],
        "Bölme ve Bölünebilme": [
            0,
            0,
            1,
            0,
            0,
            0
        ],
        "EBOB – EKOK": [
            0,
            0,
            0,
            1,
            1,
            0
        ],
        "Rasyonel Sayılar": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "Basit Eşitsizlikler": [
            0,
            1,
            1,
            0,
            1,
            1
        ],
        "Mutlak Değer": [
            0,
            0,
            1,
            0,
            0,
            1
        ],
        "Üslü Sayılar": [
            0,
            0,
            1,
            0,
            1,
            1
        ],
        "Köklü Sayılar": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "Çarpanlara Ayırma": [
            0,
            1,
            0,
            1,
            0,
            0
        ],
        "Oran Orantı": [
            0,
            0,
            0,
            0,
            0,
            0
        ],
        "Kümeler ve Kartezyen Çarpım": [
            1,
            1,
            1,
            1,
            1,
            2
        ],
        "Mantık": [
            1,
            1,
            1,
            1,
            1,
            0
        ],
        "Fonksiyonlar": [
            2,
            2,
            2,
            2,
            2,
            2
        ],
        "Polinomlar": [
            0,
            0,
            2,
            1,
            1,
            2
        ],
        "2.Dereceden Denklemler ve Eşitsizlikler": [
            1,
            1,
            2,
            2,
            1,
            1
        ],
        "Parabol": [
            0,
            1,
            1,
            0,
            1,
            1
        ],
        "Permütasyon-Kombinasyon-Olasılık – Binom": [
            3,
            3,
            3,
            3,
            2,
            3
        ],
        "Trigonometri": [
            5,
            5,
            5,
            4,
            5,
            4
        ],
        "Karmaşık Sayılar": [
            0,
            0,
            0,
            0,
            0,
            2
        ],
        "Logaritma": [
            2,
            1,
            3,
            2,
            1,
            3
        ],
        "Diziler": [
            2,
            1,
            2,
            1,
            1,
            2
        ],
        "Limit": [
            1,
            2,
            0,
            2,
            2,
            0
        ],
        "Türev": [
            5,
            3,
            0,
            4,
            3,
            0
        ],
        "İntegral": [
            3,
            5,
            0,
            4,
            4,
            0
        ],
        "TOPLAM": [
            9,
            9,
            9,
            9,
            10
        ],
        "Doğruda ve Üçgende Açı": [
            1,
            2,
            1,
            0,
            1
        ],
        "Özel Üçgenler": [
            0,
            0,
            0,
            0,
            2
        ],
        "Açıortay – Kenarortay": [
            0,
            0,
            0,
            0,
            0
        ],
        "Üçgende Alan Benzerlik": [
            0,
            1,
            0,
            0,
            0
        ],
        "Açı Kenar Bağıntıları": [
            0,
            0,
            0,
            0,
            0
        ],
        "Çokgenler": [
            0,
            0,
            0,
            0,
            1
        ],
        "Özel Dörtgenler": [
            0,
            1,
            0,
            0,
            0
        ],
        "Çember ve Daire": [
            2,
            2,
            2,
            3,
            2
        ],
        "Noktanın Analitiği": [
            1,
            1,
            1,
            2,
            1
        ],
        "Doğrunun Analitiği": [
            3,
            0,
            1,
            2,
            1
        ],
        "Dönüşüm Geometrisi": [
            0,
            0,
            1,
            0,
            1
        ],
        "Katı Cisimler": [
            1,
            1,
            2,
            1,
            1
        ],
        "Çemberin Analitiği": [
            1,
            0,
            1,
            1,
            0
        ]
    },
    "Edebiyat": {
        "SORU SAYISI": [
            24,
            24,
            24,
            24,
            24
        ],
        "Anlam Bilgisi": [
            6,
            6,
            6,
            3,
            6
        ],
        "Dil Bilgisi": [
            0,
            0,
            0,
            0,
            0
        ],
        "Metinlerin Sınıflandırılması": [
            1,
            1,
            0,
            0,
            0
        ],
        "Şiir Bilgisi": [
            2,
            3,
            3,
            2,
            3
        ],
        "Edebi Sanatlar": [
            2,
            1,
            2,
            2,
            1
        ],
        "İslamiyet Öncesi Türk Edebiyatı ve Geçiş Dönemi": [
            1,
            0,
            1,
            1,
            1
        ],
        "Halk Edebiyatı": [
            1,
            2,
            1,
            2,
            2
        ],
        "Divan Edebiyatı": [
            4,
            5,
            4,
            6,
            4
        ],
        "Tanzimat Edebiyatı": [
            1,
            1,
            1,
            2,
            1
        ],
        "Servet-İ Fünun Ve Fecr-İ Ati Edebiyatı": [
            1,
            1,
            1,
            1,
            2
        ],
        "Milli Edebiyat": [
            1,
            1,
            1,
            1,
            1
        ],
        "Cumhuriyet Dönemi Edebiyatı": [
            3,
            2,
            3,
            3,
            2
        ],
        "Batı Edebiyat Akımları": [
            1,
            1,
            1,
            1,
            1
        ]
    },
    "Fizik": {
        "SORU SAYISI": [
            14,
            14,
            14,
            14,
            14
        ],
        "Vektörler": [
            0,
            1,
            1,
            0,
            0
        ],
        "Bağıl Hareket": [
            1,
            1,
            0,
            0,
            1
        ],
        "Newton'un Hareket Yasaları": [
            1,
            1,
            1,
            0,
            1
        ],
        "Bir Boyutta Sabit İvmeli Hareket": [
            0,
            0,
            0,
            0,
            0
        ],
        "Atışlar": [
            1,
            0,
            0,
            1,
            1
        ],
        "İş, Güç ve Enerji II": [
            1,
            1,
            0,
            1,
            1
        ],
        "İtme ve Momentum": [
            1,
            1,
            1,
            0,
            1
        ],
        "Kuvvet, Tork ve Denge": [
            0,
            0,
            0,
            1,
            1
        ],
        "Kütle Merkezi": [
            0,
            0,
            0,
            0,
            0
        ],
        "Basit Makineler": [
            0,
            0,
            1,
            0,
            0
        ],
        "Elektrik Alan ve Potansiyel": [
            1,
            1,
            0,
            2,
            1
        ],
        "Paralel Levhalar ve Sığa": [
            0,
            0,
            0,
            0,
            0
        ],
        "Manyetik Alan ve Manyetik Kuvvet": [
            1,
            1,
            1,
            1,
            0
        ],
        "İndüksiyon, Alternatif Akım ve Transformatörler": [
            2,
            2,
            1,
            1,
            2
        ],
        "Çembersel Hareket": [
            0,
            1,
            1,
            1,
            2
        ],
        "Dönme, Yuvarlanma ve Açısal Momentum": [
            0,
            1,
            1,
            0,
            1
        ],
        "Kütle Çekim ve Kepler Yasaları": [
            0,
            1,
            0,
            1,
            0
        ],
        "Basit Harmonik Hareket": [
            1,
            1,
            1,
            1,
            1
        ],
        "Dalga Mekaniği ve Elektromanyetik Dalgalar": [
            1,
            1,
            1,
            1,
            1
        ],
        "Atom Modelleri": [
            0,
            0,
            0,
            0,
            0
        ],
        "Büyük Patlama ve Parçacık Fiziği": [
            0,
            0,
            1,
            0,
            0
        ],
        "Atom Fiziğine Giriş ve Radyoaktivite": [
            1,
            0,
            0,
            1,
            0
        ],
        "Özel Görelilik": [
            1,
            0,
            1,
            0,
            0
        ],
        "Kara Cisim Işıması": [
            0,
            0,
            0,
            0,
            0
        ],
        "Fotoelektrik Olay ve Compton Olayı": [
            1,
            0,
            1,
            1,
            0
        ],
        "Modern Fiziğin Teknolojideki Uygulamaları": [
            1,
            0,
            1,
            1,
            0
        ],
        "Hareket": [
            1,
            1,
            0,
            0,
            1
        ],
        "İş, Güç ve Enerji": [
            1,
            1,
            0,
            1,
            1
        ],
        "Kütle Çekim Merkezi ve Açısal Momentum": [
            0,
            0,
            0,
            0,
            0
        ],
        "Düzgün Çembersel Hareket": [
            0,
            1,
            1,
            1,
            2
        ],
        "Radyoaktivite": [
            0,
            0,
            0,
            1,
            0
        ]
    },
    "Kimya": {
        "SORU SAYISI": [
            13,
            13,
            13,
            13,
            13
        ],
        "Kimya Bilimi": [
            0,
            0,
            0,
            0,
            0
        ],
        "Atom ve Yapısı": [
            0,
            0,
            0,
            0,
            0
        ],
        "Periyodik Sistem": [
            0,
            0,
            0,
            1,
            0
        ],
        "Kimyasal Türler Arası Etkileşim": [
            0,
            0,
            0,
            0,
            0
        ],
        "Kimyasal Hesaplamalar": [
            0,
            0,
            0,
            0,
            0
        ],
        "Modern Atom Teorisi": [
            1,
            1,
            1,
            0,
            2
        ],
        "Gazlar": [
            1,
            2,
            1,
            1,
            1
        ],
        "Sıvı Çözeltiler": [
            2,
            2,
            2,
            2,
            2
        ],
        "Kimyasal Tepkimelerde Enerji": [
            1,
            1,
            1,
            1,
            1
        ],
        "Kimyasal Tepkimelerde Hız": [
            1,
            1,
            1,
            1,
            1
        ],
        "Kimyasal Tepkimelerde Denge": [
            1,
            2,
            1,
            1,
            1
        ],
        "Asit-Baz Dengesi": [
            1,
            0,
            0,
            1,
            1
        ],
        "Çözünürlük Dengesi": [
            0,
            0,
            1,
            0,
            0
        ],
        "Kimya ve Elektrik": [
            2,
            3,
            2,
            2,
            3
        ],
        "Organik Kimya": [
            3,
            1,
            3,
            3,
            1
        ]
    },
    "Biyoloji": {
        "SORU SAYISI": [
            13,
            13,
            13,
            13,
            13
        ],
        "Sinir Sistemi": [
            1,
            1,
            0,
            0,
            0
        ],
        "Endokrin Sistem": [
            1,
            2,
            0,
            1,
            1
        ],
        "Duyu Organları": [
            0,
            0,
            1,
            0,
            1
        ],
        "Destek ve Hareket Sistemi": [
            0,
            0,
            1,
            1,
            0
        ],
        "Sindirim Sistemi": [
            1,
            1,
            0,
            0,
            1
        ],
        "Dolaşım ve Bağışıklık Sistemi": [
            1,
            1,
            1,
            1,
            1
        ],
        "Solunum Sistemi": [
            1,
            1,
            1,
            1,
            1
        ],
        "Üriner Sistem": [
            0,
            1,
            0,
            0,
            1
        ],
        "Üreme Sistemi ve Embriyonik Gelişim": [
            0,
            0,
            1,
            0,
            0
        ],
        "Komünite ve Popülasyon Ekolojisi": [
            2,
            2,
            2,
            2,
            2
        ],
        "Nükleik Asitler": [
            0,
            0,
            0,
            0,
            1
        ],
        "Genetik Şifre ve Protein Sentezi": [
            2,
            1,
            2,
            2,
            2
        ],
        "Canlılık ve Enerji": [
            1,
            1,
            1,
            0,
            0
        ],
        "Fotosentez ve Kemosentez": [
            1,
            0,
            1,
            1,
            1
        ],
        "Hücresel Solunum": [
            0,
            1,
            0,
            1,
            1
        ],
        "Bitki Biyolojisi": [
            2,
            0,
            2,
            2,
            0
        ],
        "Canlılar ve Çevre": [
            0,
            1,
            0,
            1,
            0
        ]
    }
}

if __name__ == "__main__":
    print(f"TYT Konu Dağılımı: {len(TYT_DAGILIM)} ders bulundu.")
    for ders, konular in TYT_DAGILIM.items():
        print(f"  - {ders}: {len(konular)} konu")
        
    print(f"\nAYT Konu Dağılımı: {len(AYT_DAGILIM)} ders bulundu.")
    for ders, konular in AYT_DAGILIM.items():
        print(f"  - {ders}: {len(konular)} konu")
    
    print("\nVeri dosyası başarıyla yüklendi ve geçerli.")
