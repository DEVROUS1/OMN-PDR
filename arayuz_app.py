"""
OmniPDR – arayuz_app.py (Modular Version)
=========================================
Ultra-Profesyonel PDR Öğrenci Takip Platformu
"""

import streamlit as st
import pandas as pd
import os
import streamlit_authenticator as stauth
import bcrypt
from dotenv import load_dotenv
from pathlib import Path

# Çevresel değişkenleri yükle
load_dotenv()

# Yerel modüller (Modeller ve Core)
from models.ogrenci_sinifi import Ogrenci, DenemeKaydi, HataKaydi, GorusmeNotu, Kaynak
from core.veritabani import OgrenciRepository
from core.analiz_motoru import AnalizMotoru
from core.yokatlas_verileri import BOLUM_VERILERI, benzersiz_bolumler
from core.bildirim import email_gonder

# SaaS Modu Kontrolü
IS_SAAS = os.getenv("SAAS_MODE", "false").lower() == "true"
if IS_SAAS:
    from core.supabase_veritabani import SupabaseOgrenciRepository as RemoteRepo
    from core.supabase_veritabani import SupabaseAuthRepository as RemoteAuth
    from core.veritabani import OgrenciRepository as LocalRepo
else:
    from core.veritabani import OgrenciRepository as LocalRepo

# UI Yardımcıları ve Sekmeler
from utils.ui_helpers import metric_card, format_siralama, geri_sayim_goster
from tabs import (
    tab_dashboard, tab_puan, tab_universite, tab_konu,
    tab_deneme, tab_tekrar, tab_pdr_notlari, tab_testler,
    tab_gorev, tab_ders_programi, tab_kaynaklar, tab_ai_koc
)

# ══════════════════════════════════════════════
# Sayfa Ayarları ve Stil
# ══════════════════════════════════════════════
st.set_page_config(
    page_title="OmniPDR – Öğrenci Takip Platformu",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS Yükle
css_path = Path(__file__).parent / "static" / "style.css"
if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ── Kimlik Doğrulama (Auth) ──
if IS_SAAS:
    auth_repo = RemoteAuth(RemoteRepo().supabase)
    credentials = auth_repo.kullanicilari_getir()
else:
    coach_user = os.getenv("COACH_USERNAME", "admin")
    coach_hash = os.getenv("COACH_PASSWORD_HASH", "")
    if not coach_hash:
        st.error("⚠️ Kritik Hata: .env dosyasında COACH_PASSWORD_HASH eksik.")
        st.stop()
    credentials = {"usernames": {coach_user: {"name": "Eğitim Koçu", "password": coach_hash}}}

authenticator = stauth.Authenticate(credentials, "omnipdr_session_cookie", "omnipdr_secret_key", cookie_expiry_days=30)

# Sign-up (Sadece SaaS ise)
if IS_SAAS:
    with st.expander("🆕 Yeni Hesap Oluştur"):
        n_email = st.text_input("E-posta")
        n_ad = st.text_input("Ad Soyad")
        n_sifre = st.text_input("Şifre", type="password")
        if st.button("Kayıt Ol"):
            h_sifre = bcrypt.hashpw(n_sifre.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            if auth_repo.uye_ekle(n_email, h_sifre, n_ad):
                st.success("Hesap oluşturuldu! Şimdi giriş yapabilirsiniz.")
                st.rerun()

authenticator.login(location='main')
authentication_status = st.session_state.get("authentication_status")
name = st.session_state.get("name")
username = st.session_state.get("username")

if authentication_status is False:
    st.error("Kullanıcı adı veya şifre hatalı.")
    st.stop()
elif authentication_status is None:
    st.warning("Lütfen Eğitim Koçu hesabı ile giriş yapın.")
    st.stop()

# ══════════════════════════════════════════════
# Sistem Başlatma
# ══════════════════════════════════════════════
def _get_repo():
    if IS_SAAS:
        return RemoteRepo()
    return LocalRepo()

repo = _get_repo()

def _state(key, default=None):
    if key not in st.session_state: st.session_state[key] = default
    return st.session_state[key]

_state("secili_ogrenci_id", None)

def get_secili_ogr():
    oid = st.session_state.get("secili_ogrenci_id")
    u_id = st.session_state.get("username") # SaaS için user_id
    if not oid: return None
    
    if IS_SAAS:
        return repo.getir_id_ile(oid, u_id)
    return repo.getir_id_ile(oid)

# Bildirim Yardımı (Ana Kodda Kalması Daha Uygun)
def notify_logic(ogrenciler, ebbinghaus=True, gorusme=True, dusus=True):
    from datetime import date
    bugun = date.today()
    bulgular = []
    for o in ogrenciler:
        if ebbinghaus:
            gecikenler = [h for h in o.hata_kayitlari if h.bekleyen_tekrar_sayisi > 0]
            if len(gecikenler) >= 5: bulgular.append(f"🔴 {o.ad}: {len(gecikenler)} bekleyen Ebbinghaus tekrarı var.")
        if gorusme:
            son_tarih = o.gorusme_notlari[-1].tarih if o.gorusme_notlari else None
            if not son_tarih or (bugun - son_tarih).days >= 7:
                 bulgular.append(f"🟠 {o.ad}: En son { (bugun-son_tarih).days if son_tarih else 'Hiç' } gün önce görüşülmüş.")
        if dusus and len(o.deneme_kayitlari) >= 3:
            sonlar = o.deneme_kayitlari[-3:]
            n3, n2, n1 = [sum(d.netleri.values()) for d in sonlar]
            if n3 > n2 > n1: bulgular.append(f"📉 {o.ad}: Son 3 sınavdır netleri düşüyor.")

    if bulgular and os.getenv("COACH_EMAIL"):
        email_gonder(f"OmniPDR Kritik Durum Özeti - {bugun.strftime('%d.%m.%Y')}", "\n".join(bulgular), os.getenv("COACH_EMAIL"))
    return bulgular

@st.cache_data(ttl=86400)
def auto_check(_ogrenciler): return notify_logic(_ogrenciler)

# ══════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🧠 OmniPDR")
    st.markdown("*Bireysel Eğitim Koçluğu*")
    aktif_rol = st.radio("Kullanıcı Profili", ["Eğitim Koçu (Admin)", "Öğrenci (Kiosk)"])
    is_admin = (aktif_rol == "Eğitim Koçu (Admin)")
    st.markdown("---")

    u_id = st.session_state.get("username")
    ogrenciler = repo.hepsini_getir(u_id) if IS_SAAS else repo.hepsini_getir()
    isimler = [o.ad for o in ogrenciler]
    if isimler:
        secim = st.selectbox("👤 Öğrenci Seç", isimler, key="sb_ogrenci")
        for o in ogrenciler:
            if o.ad == secim:
                st.session_state["secili_ogrenci_id"] = o.ogrenci_id
                break

    # Öğrenci İşlemleri (Admin) 
    if is_admin:
        with st.expander("➕ Yeni Öğrenci Ekle"):
            y_ad = st.text_input("Öğrenci Ad Soyad")
            y_hedef = st.text_input("Hedef Bölüm")
            y_tur = st.selectbox("Sınav Türü", ["YKS", "LGS"])
            if st.button("✅ Kaydet"):
                y_ogr = Ogrenci(ad=y_ad, hedef_bolum=y_hedef, sinav_turu=y_tur, user_id=st.session_state.get("username"))
                repo.kaydet(y_ogr)
                st.success(f"Başarılı! {y_ad} eklendi.")
                st.rerun()

    secili_ogr = get_secili_ogr()
    if is_admin and secili_ogr:
        with st.expander("✏️ Öğrenci Düzenle"):
            d_ad = st.text_input("Ad Soyad", secili_ogr.ad)
            d_tel = st.text_input("Veli Tel", getattr(secili_ogr, "veli_telefon", ""))
            if st.button("💾 Güncelle"):
                secili_ogr.ad = d_ad
                secili_ogr.veli_telefon = d_tel
                repo.kaydet(secili_ogr)
                st.rerun()
    elif is_admin and not secili_ogr:
        st.info("Düzenleme yapmak için bir öğrenci seçin.")

    auth_col1, auth_col2 = st.columns(2)
    authenticator.logout("🚪 Çıkış", "sidebar")

# ══════════════════════════════════════════════
# ANA İÇERİK
# ══════════════════════════════════════════════
ogr = get_secili_ogr()

if not ogr:
    st.markdown('<div class="hero-banner" style="text-align:center; padding:40px;"><h1>🎯 OmniPDR Koçluk Panosu</h1></div>', unsafe_allow_html=True)
    if not repo.hepsini_getir(): st.info("👈 Menüden yeni öğrenci ekleyin.")
    st.stop()

analiz = AnalizMotoru(ogr)

# SEKME TANIMLARI
sekme_isimleri = [
    "🏠 Dashboard", "🎯 Puan", "🏛️ Üniversite", "📚 Konu", 
    "📝 Deneme Ekle", "🔁 Tekrar", "📓 Notlar", "🧠 Testler",
    "📅 Görevler", "📅 Program", "📚 Kaynaklar", "🤖 AI Koçum"
]

sekmeler = st.tabs(sekme_isimleri)

# RENDER
with sekmeler[0]: tab_dashboard.render(ogr, repo, analiz, is_admin, ogrenciler, notify_logic, auto_check)
with sekmeler[1]: tab_puan.render(ogr, repo, analiz, is_admin)
with sekmeler[2]: tab_universite.render(ogr, repo, analiz, is_admin)
with sekmeler[3]: tab_konu.render(ogr, repo, analiz, is_admin)
with sekmeler[4]: tab_deneme.render(ogr, repo, analiz, is_admin)
with sekmeler[5]: tab_tekrar.render(ogr, repo, analiz, is_admin)
with sekmeler[6]: tab_pdr_notlari.render(ogr, repo, analiz, is_admin)
with sekmeler[7]: tab_testler.render(ogr, repo, analiz, is_admin)
with sekmeler[8]: tab_gorev.render(ogr, repo, analiz, is_admin)
with sekmeler[9]: tab_ders_programi.render(ogr, repo, analiz, is_admin)
with sekmeler[10]: tab_kaynaklar.render(ogr, repo, analiz, is_admin)
with sekmeler[11]: tab_ai_koc.render(ogr, repo, analiz, is_admin)
