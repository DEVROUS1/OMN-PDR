import streamlit as st
from datetime import date
from models.ogrenci_sinifi import HataKaydi

def render(ogr, repo, analiz, is_admin):
    st.subheader("🔁 Ebbinghaus Tekrar Takibi")
    st.markdown("Hatalı çözdüğün veya zorlandığın soruları buraya ekle. Sistem bilimsel unutma eğrisine (1, 7, 30 gün) göre seni uyaracaktır.")

    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### ➕ Hatalı Soru Ekle")
        with st.form("hata_ekle"):
            h_marka = st.text_input("Kitap/Yayın", placeholder="345 Yayınları...")
            h_konu = st.text_input("Soru Konusu", placeholder="Üslü Sayılar...")
            h_ders = st.selectbox("Ders", ["Türkçe", "Matematik", "Fen", "Sosyal", "Geometri"])
            if st.form_submit_button("📌 Takibe Al", use_container_width=True):
                if h_marka and h_konu:
                    ogr.hata_ekle(h_ders, h_konu, tarih=date.today())
                    # Kaynak bilgisini de set edelim (hata_ekle içinde yoksa manuel veya helper güncellemesiyle)
                    ogr.hata_kayitlari[-1].kaynak = h_marka
                    repo.kaydet(ogr)
                    st.success("✅ Eklendi! İlk tekrar yarın seni bekliyor.")
                    st.rerun()

    with col2:
        st.markdown("#### 📅 Tekrar Bekleyenler")
        bekleyenler = [h for h in ogr.hata_kayitlari if h.bekleyen_tekrar_sayisi > 0]
        
        if not bekleyenler:
            st.success("Tebrikler! Şu an bekleyen bir tekrarın yok. Yeni hatalar ekleyerek gelişimini sürdür.")
        else:
            bugun = date.today()
            for i, h in enumerate(bekleyenler):
                yol = h.tekrar_durumu_getir(bugun)
                renk = "green" if "Hazır" in yol else "gray"
                
                with st.expander(f"📖 {h.ders}: {h.konu} ({h.kaynak})"):
                    st.markdown(f"**Atandığı Tarih:** {h.tarih.isoformat()}")
                    st.markdown(f"**Tekrar Durumu:** <span style='color:{renk}; font-weight:bold;'>{yol}</span>", unsafe_allow_html=True)
                    st.caption(f"Kalan Tekrar Sayısı: {h.bekleyen_tekrar_sayisi}")
                    
                    if "Hazır" in yol:
                        if st.button("✅ Tekrar Ettim", key=f"btn_h_{i}"):
                            h.tekrar_onayla()
                            repo.kaydet(ogr)
                            st.success("Harika! Bir sonraki tekrar planlandı.")
                            st.rerun()
                    
                    if st.button("🗑️ Kaydı Sil", key=f"del_h_{i}", type="secondary"):
                        ogr.hata_kayitlari.remove(h)
                        repo.kaydet(ogr)
                        st.rerun()
