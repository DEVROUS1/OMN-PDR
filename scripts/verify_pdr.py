
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from models.test_verileri import tum_testleri_getir
from core.test_analiz import analiz_et

def verify_pdr():
    print("="*50)
    print("PDR MODÜLÜ DOĞRULAMA TESTİ")
    print("="*50)

    # 1. Test Verilerini Yükle
    print("[1/2] Testler yükleniyor...")
    try:
        testler = tum_testleri_getir()
        print(f"   - {len(testler)} test bulundu.")
        for t in testler:
            print(f"   - {t.ad} ({len(t.sorular)} soru)")
    except Exception as e:
        print(f"   - HATA: Veri yüklenemedi ({e})")
        return

    # 2. Analiz Motorunu Test Et
    print("\n[2/2] Analiz motoru test ediliyor...")
    
    # Holland Testi Simülasyonu
    holland = next(t for t in testler if t.id == "holland_ilgi")
    cevaplar_holland = {str(s.id): "1" for s in holland.sorular} # Hepsi "Fark Etmez"
    try:
        sonuc = analiz_et("holland_ilgi", cevaplar_holland, holland.sorular)
        print(f"   - Holland Analizi: BAŞARILI (Kod: {sonuc.get('kod')})")
    except Exception as e:
        print(f"   - Holland Analizi: HATA ({e})")

    # Sınav Kaygısı Simülasyonu
    kaygi = next(t for t in testler if t.id == "sinav_kaygisi")
    cevaplar_kaygi = {str(s.id): "3" for s in kaygi.sorular} # Orta seviye
    try:
        sonuc = analiz_et("sinav_kaygisi", cevaplar_kaygi, kaygi.sorular)
        print(f"   - Kaygı Analizi: BAŞARILI (Seviye: {sonuc.get('seviye')})")
    except Exception as e:
        print(f"   - Kaygı Analizi: HATA ({e})")

    print("\n" + "="*50)
    print("TEST TAMAMLANDI")

if __name__ == "__main__":
    verify_pdr()
