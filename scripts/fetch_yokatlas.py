
import json
import os
import time
import requests
from typing import List, Dict

# YÖK Atlas Official Endpoints (Reverse Engineered)
# These are the endpoints used by the wizard.
API_BASE = "https://yokatlas.yok.gov.tr"

def fetch_universities():
    """Fetches the list of universities."""
    # This is a placeholder. Without the library, we might need to parse the homepage.
    # However, let's try to use the library first.
    try:
        from yokatlas import YokAtlas
        yok = YokAtlas()
        print("Kütüphane kullanılıyor: yokatlas")
        return yok.universities()
    except ImportError:
        print("UYARI: 'yokatlas' kütüphanesi bulunamadı. Manuel mod devreye giriyor (Kısıtlı).")
        return []

def fetch_all_data():
    print("YÖK Atlas Veri Çekme İşlemi Başlatılıyor...")
    
    all_data = []
    
    # 1. Try using the library for bulk data
    try:
        from yokatlas import YokAtlas
        yok = YokAtlas()
        
        # Lisans Programları
        print("Lisans programları çekiliyor...")
        lisans_programs = yok.programs(level="lisans")
        print(f"{len(lisans_programs)} lisans programı bulundu.")
        all_data.extend(lisans_programs)
        
        # Önlisans Programları
        print("Önlisans programları çekiliyor...")
        onlisans_programs = yok.programs(level="onlisans")
        print(f"{len(onlisans_programs)} önlisans programı bulundu.")
        all_data.extend(onlisans_programs)
        
    except ImportError:
        print("Kütüphane yok, veri çekilemedi.")
        return
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return

    # Veriyi Kaydet
    output_path = "data/yokatlas_full.json"
    os.makedirs("data", exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"Toplam {len(all_data)} program verisi '{output_path}' dosyasına kaydedildi.")

if __name__ == "__main__":
    fetch_all_data()
