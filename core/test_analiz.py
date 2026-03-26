
"""
OmniPDR – core/test_analiz.py
===================================
Test sonuçlarını yorumlayan ve kişiselleştirilmiş rapor üreten analiz motoru.
"""

def holland_analizi(skorlar: dict) -> dict:
    """
    Holland (RIASEC) puanlarına göre en baskın 3 tipi ve meslek önerilerini döndürür.
    """
    # Skorları büyükten küçüğe sırala
    sirali_tipler = sorted(skorlar.items(), key=lambda x: x[1], reverse=True)
    top_3 = sirali_tipler[:3]
    
    kod = "".join([t[0] for t in top_3])
    
    yorumlar = {
        "R": {
            "baslik": "GERÇEKÇİ (Realistic)",
            "ozellik": "Pratik, madde odaklı, kas gücü ve el becerisi gerektiren işleri seven.",
            "meslekler": ["Mühendislik (Makine, İnşaat)", "Mimarlık", "Veterinerlik", "Pilotluk", "Teknisyenlik", "Aşçılık", "Sporculuk"]
        },
        "I": {
            "baslik": "ARAŞTIRMACI (Investigative)",
            "ozellik": "Analitik, meraklı, problem çözen, bilimsel ve matematiksel konuları seven.",
            "meslekler": ["Tıp / Doktorluk", "Yazılım Mühendisliği", "Eczacılık", "Biolog / Genetik", "Psikoloji", "Akademisyenlik"]
        },
        "A": {
            "baslik": "SANATSAL (Artistic)",
            "ozellik": "Yaratıcı, hayal gücü geniş, estetik kaygısı olan ve özgür çalışmayı seven.",
            "meslekler": ["Grafik Tasarım", "Müzisyenlik", "Yazarlık / Gazetecilik", "İç Mimarlık", "Tiyatro / Oyunculuk", "Reklamcılık"]
        },
        "S": {
            "baslik": "SOSYAL (Social)",
            "ozellik": "Yardımsever, iletişimi güçlü, insanlarla çalışmayı ve öğretmeyi seven.",
            "meslekler": ["Öğretmenlik", "Psikolojik Danışmanlık", "Halkla İlişkiler", "Hemşirelik", "Sosyal Hizmetler", "İnsan Kaynakları"]
        },
        "E": {
            "baslik": "GİRİŞİMCİ (Enterprising)",
            "ozellik": "Lider, ikna kabiliyeti yüksek, hırslı ve organizasyon yeteneği olan.",
            "meslekler": ["Avukatlık", "İşletme / Yöneticilik", "Pazarlama / Satış", "Siyaset Bilimi", "Girişimcilik", "Turizm İşletmeciliği"]
        },
        "C": {
            "baslik": "GELENEKSEL (Conventional)",
            "ozellik": "Düzenli, planlı, veri ve rakamlarla çalışmayı seven, kurallara uyan.",
            "meslekler": ["Muhasebe", "Bankacılık", "Finans Uzmanlığı", "Kütüphanecilik", "İstatistik", "Memurluk"]
        }
    }

    rapor = []
    for tip, puan in top_3:
        bilgi = yorumlar.get(tip, {})
        rapor.append({
            "tip": bilgi.get("baslik"),
            "puan": puan,
            "yorum": bilgi.get("ozellik"),
            "oneriler": ", ".join(bilgi.get("meslekler", []))
        })

    return {
        "kod": kod,
        "detay": rapor,
        "genel_yorum": f"Sizin baskın Holland kodunuz: {kod}. Bu kod, {rapor[0]['tip']} özelliklerinizin en ön planda olduğunu gösterir."
    }

def coklu_zeka_analizi(skorlar: dict) -> dict:
    """
    Çoklu Zeka Envanteri sonuçlarını yorumlar.
    """
    sirali = sorted(skorlar.items(), key=lambda x: x[1], reverse=True)
    baskin_zeka = sirali[0]
    
    yorumlar = {
        "Sözel": "Kelimelerle aranız çok iyi. Okuma, yazma ve konuşma becerileriniz yüksek.",
        "Mantıksal": "Sayılar, neden-sonuç ilişkileri ve mantıksal örüntüler sizin alanınız.",
        "Görsel": "Dünyayı resimlerle algılıyorsunuz. Yön bulma ve tasarım yeteneğiniz güçlü.",
        "Müziksel": "Melodi ve ritimlere karşı çok duyarlısınız.",
        "Bedensel": "Hareket ederek öğreniyorsunuz. El becerileriniz veya sportif yönünüz kuvvetli.",
        "Sosyal": "İnsanlarla iletişim kurmakta ve grup çalışmalarında çok başarılısınız.",
        "İçsel": "Kendinizi çok iyi tanıyor, bağımsız çalışmayı ve düşünmeyi seviyorsunuz.",
        "Doğa": "Doğadaki canlıları, bitkileri ve olayları incelemekten keyif alıyorsunuz."
    }

    return {
        "baskin_tip": baskin_zeka[0],
        "puan": baskin_zeka[1],
        "yorum": yorumlar.get(baskin_zeka[0], "Bu zeka alanında potansiyeliniz yüksek."),
        "tum_sirala": sirali
    }

def sinav_kaygisi_analizi(toplam_puan: int, soru_sayisi: int) -> dict:
    """
    Sınav Kaygısı Ölçeği toplam puanına göre değerlendirme yapar.
    Genelde her soru 1-5 puan arasıdır. Max puan: soru_sayisi * 5.
    Burada 0-1 arası (Evet/Hayır) veya 1-5 puanlama varsayılabilir.
    Kullanıcı arayüzünde 1-5 Skala (Hiç - Her zaman) kullanacağız.
    """
    max_puan = soru_sayisi * 5
    yuzde = (toplam_puan / max_puan) * 100
    
    seviye = ""
    yorum = ""
    oneriler = []
    
    if yuzde < 20:
        seviye = "Düşük Kaygı"
        yorum = "Sınavlara karşı oldukça rahatsınız. Ancak biraz heyecan, motivasyon için gereklidir; tamamen kaygısız olmak dikkati düşürebilir."
    elif 20 <= yuzde < 45:
        seviye = "Orta (Sağlıklı) Kaygı"
        yorum = "Bu seviyedeki kaygı, sizi ders çalışmaya motive eden sağlıklı bir düzeydir. Performansınız için ideal seviyedesiniz."
    elif 45 <= yuzde < 70:
        seviye = "Yüksek Kaygı"
        yorum = "Kaygı düzeyiniz, potansiyelinizi göstermenizi engellemeye başlamış olabilir. Fiziksel belirtiler (kalp çarpıntısı vb.) yaşıyor olabilirsiniz."
        oneriler = ["Nefes egzersizleri yapın.", "Sınav öncesi uyku düzenine dikkat edin.", "Olumsuz iç konuşmaları ('Yapamayacağım') fark edip durdurun."]
    else:
        seviye = "Çok Yüksek (Panik) Düzey"
        yorum = "Sınav kaygısı günlük yaşamınızı ve başarınızı ciddi şekilde etkiliyor. Bir uzman desteği almanız faydalı olabilir."
        oneriler = ["Okul PDR servisine başvurun.", "Profesyonel psikolojik destek almayı değerlendirin.", "Gevşeme tekniklerini öğrenin."]
        
    return {
        "seviye": seviye,
        "yuzde": round(yuzde, 1),
        "yorum": yorum,
        "oneriler": oneriler
    }

def analiz_et(test_id: str, cevaplar: dict, soru_verileri: list) -> dict:
    """
    Genel analiz fonksiyonu.
    """
    try:
        # Puanlama
        toplam_puan = 0
        kategori_puanlari = {}
        
        for s_index, cevap_val in cevaplar.items():
            # ID'yi string veya int olarak eşleştir
            soru = next((s for s in soru_verileri if str(s.id) == str(s_index)), None)
            if not soru: continue
            
            puan = int(cevap_val)
            toplam_puan += puan
            
            if soru.kategori:
                kategori_puanlari[soru.kategori] = kategori_puanlari.get(soru.kategori, 0) + puan

        # Özelleştirilmiş Raporlama
        if test_id == "holland_ilgi":
            return holland_analizi(kategori_puanlari)
        elif test_id == "coklu_zeka":
            return coklu_zeka_analizi(kategori_puanlari)
        elif test_id == "sinav_kaygisi":
            return sinav_kaygisi_analizi(toplam_puan, len(soru_verileri))
        
        return {"toplam": toplam_puan, "kategori_dagilimi": kategori_puanlari}

    except Exception as e:
        return {"hata": str(e)}
