"""
OmniPDR – core/veritabani.py (SQLite Sürümü)
===========================================
SQLite tabanlı yüksek performanslı kalıcılık katmanı.
Model genişlediğinde tablo şeması JSON veri kolonu sayesinde bozulmaz.
"""

import sqlite3
import json
import os
import threading
from pathlib import Path
from typing import List, Optional, Dict
from datetime import date, datetime, timedelta

from models.ogrenci_sinifi import Ogrenci

# ──────────────────────────────────────────────
# Veritabanı Yolları
# ──────────────────────────────────────────────
_ROOT = Path(__file__).parent.parent
_DB_YOL = _ROOT / "data" / "ogrenciler.db"
_ESKI_JSON_YOL = _ROOT / "data" / "ogrenciler.json"


class OgrenciRepository:
    """
    Tüm öğrenci verilerini SQLite veritabanında saklayan ve yöneten sınıf.
    API dış dünyayla (Streamlit) uyumludur.
    """

    def __init__(self, db_yolu: Path = _DB_YOL):
        self.db_yolu = db_yolu
        self.db_yolu.parent.mkdir(parents=True, exist_ok=True)
        
        # Thread-safe bağlantı yönetimi
        self._lock = threading.Lock()
        self.conn = sqlite3.connect(str(self.db_yolu), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        
        self._tablo_hazirla()
        self._migrasyon_kontrol()

    def _tablo_hazirla(self):
        """Tabloları oluşturur."""
        with self._lock:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS ogrenciler (
                    id TEXT PRIMARY KEY,
                    veri TEXT NOT NULL
                )
            """)
            self.conn.commit()

    def _migrasyon_kontrol(self):
        """Eğer eski JSON dosyası varsa ve DB boşsa aktarır."""
        if _ESKI_JSON_YOL.exists():
            with self._lock:
                cursor = self.conn.execute("SELECT COUNT(*) FROM ogrenciler")
                if cursor.fetchone()[0] == 0:
                    print(f"MİGRASYON: {_ESKI_JSON_YOL.name} verileri SQLite'a taşınıyor...")
                    try:
                        with open(_ESKI_JSON_YOL, "r", encoding="utf-8") as f:
                            ham = json.load(f)
                        
                        for ogr_dict in ham.get("ogrenciler", []):
                            oid = ogr_dict.get("ogrenci_id")
                            self.conn.execute(
                                "INSERT OR REPLACE INTO ogrenciler (id, veri) VALUES (?, ?)",
                                (oid, json.dumps(ogr_dict, ensure_ascii=False))
                            )
                        self.conn.commit()
                        print("MİGRASYON: Başarıyla tamamlandı.")
                        # Eski dosyayı bozmamak için silmiyoruz, kullanıcıya bırakıyoruz.
                    except Exception as e:
                        print(f"MİGRASYON HATASI: {e}")

    # ── Genel CRUD operasyonları ───────────────

    def kaydet(self, ogrenci: Ogrenci) -> None:
        """Yeni veya mevcut öğrenciyi kaydeder/günceller."""
        self._otomatik_yedekle()
        with self._lock:
            self.conn.execute(
                "INSERT OR REPLACE INTO ogrenciler (id, veri) VALUES (?, ?)",
                (ogrenci.ogrenci_id, json.dumps(ogrenci.to_dict(), ensure_ascii=False))
            )
            self.conn.commit()

    def getir_id_ile(self, ogrenci_id: str) -> Optional[Ogrenci]:
        with self._lock:
            cursor = self.conn.execute("SELECT veri FROM ogrenciler WHERE id = ?", (ogrenci_id,))
            row = cursor.fetchone()
            if row:
                return Ogrenci.from_dict(json.loads(row["veri"]))
        return None

    def getir_ad_ile(self, ad: str) -> Optional[Ogrenci]:
        with self._lock:
            cursor = self.conn.execute("SELECT veri FROM ogrenciler")
            for row in cursor:
                ogr_data = json.loads(row["veri"])
                if ogr_data.get("ad", "").lower() == ad.lower():
                    return Ogrenci.from_dict(ogr_data)
        return None

    def hepsini_getir(self) -> List[Ogrenci]:
        ogrenciler = []
        with self._lock:
            cursor = self.conn.execute("SELECT veri FROM ogrenciler")
            for row in cursor:
                ogrenciler.append(Ogrenci.from_dict(json.loads(row["veri"])))
        return ogrenciler

    def sil(self, ogrenci_id: str) -> bool:
        with self._lock:
            cursor = self.conn.execute("DELETE FROM ogrenciler WHERE id = ?", (ogrenci_id,))
            self.conn.commit()
            return cursor.rowcount > 0

    # ── Yedekleme ve Bakım ──────────────────────

    def _otomatik_yedekle(self):
        """SQLite Backup API ile güvenli yedekleme yapar."""
        backup_dir = self.db_yolu.parent / "backups"
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        bugun = date.today().isoformat()
        yedek_db_yolu = backup_dir / f"ogrenciler_{bugun}.db"
        
        if yedek_db_yolu.exists():
            return

        with self._lock:
            try:
                dest = sqlite3.connect(str(yedek_db_yolu))
                with dest:
                    self.conn.backup(dest)
                dest.close()
                
                # Eski yedekleri temizle (30 günden eski)
                self._temizle_eski_yedekler(backup_dir)
            except Exception as e:
                print(f"YEDEKLEME HATASI: {e}")

    def _temizle_eski_yedekler(self, backup_dir: Path):
        sinir = datetime.now() - timedelta(days=30)
        for f in backup_dir.glob("ogrenciler_*.db"):
            try:
                t_str = f.stem.split("_")[1]
                if datetime.fromisoformat(t_str) < sinir:
                    f.unlink()
            except: pass

    def yedekleri_listele(self) -> List[str]:
        backup_dir = self.db_yolu.parent / "backups"
        if not backup_dir.exists(): return []
        return sorted([f.name for f in backup_dir.glob("ogrenciler_*.db")], reverse=True)

    def yedekten_geri_yukle(self, yedek_adi: str) -> bool:
        """Yedek DB'yi ana DB üzerine yazar."""
        yedek_yolu = self.db_yolu.parent / "backups" / yedek_adi
        if not yedek_yolu.exists(): return False
        
        with self._lock:
            try:
                source = sqlite3.connect(str(yedek_yolu))
                with self.conn:
                    source.backup(self.conn)
                source.close()
                return True
            except Exception as e:
                print(f"GERİ YÜKLEME HATASI: {e}")
                return False

    @property
    def toplam_ogrenci(self) -> int:
        with self._lock:
            cursor = self.conn.execute("SELECT COUNT(*) FROM ogrenciler")
            return cursor.fetchone()[0]

    def __del__(self):
        try:
            self.conn.close()
        except: pass

    def __repr__(self) -> str:
        return f"<OgrenciRepository (SQLite): {self.toplam_ogrenci} ogrenci>"
