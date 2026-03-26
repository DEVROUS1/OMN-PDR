"""
OmniPDR – core/supabase_veritabani.py (SaaS Sürümü)
===================================================
Supabase tabanlı bulut kalıcılık katmanı.
Her kullanıcı sadece kendi 'user_id'sine ait öğrencileri görür.
"""

import os
import json
from typing import List, Optional
from supabase import create_client, Client
from models.ogrenci_sinifi import Ogrenci
import bcrypt

class SupabaseAuthRepository:
    """Supabase üzerinden kullanıcı kimlik doğrulama verilerini yönetir."""
    def __init__(self, client: Client):
        self.supabase = client
        self.tablo = "uyeler"

    def kullanicilari_getir(self) -> dict:
        """Tüm kullanıcıları streamlit-authenticator formatında döndürür."""
        res = self.supabase.table(self.tablo).select("*").execute()
        credentials = {"usernames": {}}
        for row in res.data:
            credentials["usernames"][row["email"]] = {
                "name": row["ad_soyad"],
                "password": row["sifre_hash"]
            }
        return credentials

    def uye_ekle(self, email, sifre_hash, ad_soyad) -> bool:
        data = {"email": email, "sifre_hash": sifre_hash, "ad_soyad": ad_soyad}
        res = self.supabase.table(self.tablo).insert(data).execute()
        return len(res.data) > 0

class SupabaseOgrenciRepository:
    """
    Tüm öğrenci verilerini Supabase (PostgreSQL) üzerinde saklayan sınıf.
    SaaS (Multi-tenant) yapısını destekler.
    """

    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") # Veya KEY
        if not url or not key:
            raise ValueError("SUPABASE_URL ve SUPABASE_SERVICE_ROLE_KEY .env dosyasında eksik.")
        
        self.supabase: Client = create_client(url, key)
        self.tablo = "ogrenciler"

    def kaydet(self, ogrenci: Ogrenci) -> bool:
        """Yeni veya mevcut öğrenciyi Supabase'e kaydeder."""
        if not ogrenci.user_id:
            raise ValueError("SaaS modunda 'user_id' zorunludur.")

        data = {
            "id": ogrenci.ogrenci_id,
            "user_id": ogrenci.user_id,
            "ad": ogrenci.ad,
            "hedef_bolum": ogrenci.hedef_bolum,
            "sinav_turu": ogrenci.sinav_turu,
            "veri": ogrenci.to_dict()
        }

        # upsert: varsa güncelle, yoksa ekle
        res = self.supabase.table(self.tablo).upsert(data).execute()
        return len(res.data) > 0

    def getir_id_ile(self, ogrenci_id: str, user_id: str) -> Optional[Ogrenci]:
        res = self.supabase.table(self.tablo)\
            .select("*")\
            .eq("id", ogrenci_id)\
            .eq("user_id", user_id)\
            .execute()
        
        if res.data:
            return Ogrenci.from_dict(res.data[0]["veri"])
        return None

    def hepsini_getir(self, user_id: str) -> List[Ogrenci]:
        """Sadece ilgili kullanıcıya ait öğrencileri getirir."""
        res = self.supabase.table(self.tablo)\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()
        
        return [Ogrenci.from_dict(row["veri"]) for row in res.data]

    def sil(self, ogrenci_id: str, user_id: str) -> bool:
        res = self.supabase.table(self.tablo)\
            .delete()\
            .eq("id", ogrenci_id)\
            .eq("user_id", user_id)\
            .execute()
        return len(res.data) > 0

    @property
    def toplam_ogrenci(self) -> int:
        # Bu metot genel istatistik için (Admin paneli gerekirse)
        res = self.supabase.table(self.tablo).select("id", count="exact").execute()
        return res.count if res.count is not None else 0
