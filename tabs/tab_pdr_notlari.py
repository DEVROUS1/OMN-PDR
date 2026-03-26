import streamlit as st
import pandas as pd
from datetime import date
import urllib.parse
from models.ogrenci_sinifi import GorusmeNotu
from core.ai_kocluk import AIKoc
import html as html_module

def render(ogr, repo, analiz, is_admin):
    st.subheader("📓 PDR & Koçluk Notları")
    
    if is_admin:
        with st.form("gorusme_ekle_form"):
            st.markdown("#### 📝 Yeni Görüşme Notu Ekle")
            g_icerik = st.text_area("Görüşme Detayı", height=150, placeholder="Öğrencinin haftalık performansı, motivasyonu ve hedefleri...")
            g_deger = st.select_slider("Genel Değerlendirme", ["Kritik", "Zayıf", "Orta", "İyi", "Mükemmel"], "Orta")
            
            if st.form_submit_button("📁 Görüşmeyi Kaydet", use_container_width=True):
                if g_icerik.strip():
                    ogr.gorusme_ekle(
                        icerik=g_icerik.strip(),
                        degerlendirme=g_deger,
                        tarih=date.today()
                    )
                    repo.kaydet(ogr)
                    st.success("✅ Görüşme notu başarıyla arşivlendi!")
                    st.rerun()

    # Görüşme Geçmişi
    if ogr.gorusme_notlari:
        st.markdown("#### 🕒 Görüşme Arşivi")
        for i, n in enumerate(reversed(ogr.gorusme_notlari)):
            with st.expander(f"{n.tarih} | Değerlendirme: {n.degerlendirme}"):
                st.markdown(f"_{html_module.escape(n.icerik)}_")
                if is_admin:
                    if st.button("🗑️ Notu Sil", key=f"del_n_{i}"):
                        ogr.gorusme_notlari.remove(n)
                        repo.kaydet(ogr)
                        st.rerun()

    st.markdown("---")
    
    # AI Raporlama (Sadece Admin)
    if is_admin:
        st.markdown("#### 🤖 Yapay Zeka ile Veli Raporu Oluştur")
        st.caption("AI, son deneme sonuçlarını, konu ilerlemesini ve görüşme notlarını analiz ederek profesyonel bir veli bilgilendirme metni hazırlar.")
        
        if st.button("📑 Raporu Oluştur", use_container_width=True):
            with st.spinner("AI verileri analiz ediyor ve rapor hazırlıyor..."):
                ai = AIKoc()
                rapor_metni = ai.veli_raporu_olustur(ogr, analiz)
                st.session_state[f"rapor_{ogr.ogrenci_id}"] = rapor_metni
        
        rapor_key = f"rapor_{ogr.ogrenci_id}"
        if rapor_key in st.session_state:
            rapor_metni = st.session_state[rapor_key]
            st.markdown("---")
            st.markdown("##### 📄 Hazırlanan Veli Raporu")
            st.text_area("Rapor İçeriği (Kopyalayabilir veya Düzenleyebilirsiniz)", value=rapor_metni, height=400, key="rapor_editor")
            
            # WhatsApp Gönder
            v_tel = getattr(ogr, 'veli_telefon', '')
            if v_tel:
                # Telefonu temizle (wa.me formatı için)
                temiz_tel = "".join(filter(str.isdigit, v_tel))
                if temiz_tel.startswith("0") and not temiz_tel.startswith("00"):
                    temiz_tel = "90" + temiz_tel[1:len(temiz_tel)]
                if not temiz_tel.startswith("90") and not temiz_tel.startswith("00"):
                    temiz_tel = "90" + temiz_tel
                
                encoded_metin = urllib.parse.quote(rapor_metni)
                wa_url = f"https://wa.me/{temiz_tel}?text={encoded_metin}"
                
                st.success(f"📱 Veli Telefonu Kayıtlı: {v_tel}")
                st.link_button("📱 WhatsApp'ta Gönder", wa_url, use_container_width=True)
            else:
                st.warning("⚠️ Veli telefonu kayıtlı değil. Sidebar'daki 'Öğrenci Düzenle' bölümünden veli telefonunu ekleyerek bu özelliği kullanabilirsiniz.")
            
            # Download butonu (txt ve PDF)
            dc1, dc2 = st.columns(2)
            with dc1:
                st.download_button("📝 Metin (.txt) İndir", rapor_metni, file_name=f"veli_raporu_{ogr.ad}.txt", use_container_width=True)
            
            with dc2:
                try:
                    from core.pdf_rapor import PDFRaporcu
                    raporcu = PDFRaporcu()
                    pdf_bytes = raporcu.rapor_olustur(ogr, rapor_metni)
                    st.download_button("📄 PDF Raporu İndir", pdf_bytes, file_name=f"Kocluk_Raporu_{ogr.ad}.pdf", mime="application/pdf", use_container_width=True)
                except Exception as e:
                    st.warning(f"PDF hazırlanamadı: {e}")
