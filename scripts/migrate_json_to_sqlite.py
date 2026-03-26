import json
import sqlite3
import os
import sys
from pathlib import Path

# Proje kök dizini
ROOT = Path(__file__).parent.parent
JSON_YOL = ROOT / "data" / "ogrenciler.json"
DB_YOL = ROOT / "data" / "ogrenciler.db"

def migrate():
    print("🚀 OmniPDR JSON -> SQLite Migrasyonu Başlatıldı...")
    
    if not JSON_YOL.exists():
        print(f"❌ HATA: Kaynak JSON dosyası bulunamadı: {JSON_YOL}")
        return

    # Veriyi oku
    try:
        with open(JSON_YOL, "r", encoding="utf-8") as f:
            ham = json.load(f)
        ogrenciler = ham.get("ogrenciler", [])
        print(f"📂 JSON dosyasında {len(ogrenciler)} öğrenci bulundu.")
    except Exception as e:
        print(f"❌ HATA: JSON okunamadı: {e}")
        return

    # SQLite'a bağlan
    try:
        DB_YOL.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_YOL))
        cursor = conn.cursor()
        
        # Tablo oluştur
        cursor.execute("CREATE TABLE IF NOT EXISTS ogrenciler (id TEXT PRIMARY KEY, veri TEXT)")
        
        # Aktar
        basarili = 0
        for ogr in ogrenciler:
            oid = ogr.get("ogrenci_id")
            if not oid: continue
            
            cursor.execute(
                "INSERT OR REPLACE INTO ogrenciler (id, veri) VALUES (?, ?)",
                (oid, json.dumps(ogr, ensure_ascii=False))
            )
            basarili += 1
            
        conn.commit()
        conn.close()
        print(f"✅ Başarıyla {basarili} öğrenci SQLite veritabanına aktarıldı.")
        print(f"📁 Konum: {DB_YOL}")
        
    except Exception as e:
        print(f"❌ HATA: SQLite aktarımı sırasında hata: {e}")

if __name__ == "__main__":
    migrate()
