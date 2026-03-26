import streamlit as st
from datetime import date
import html as html_module

def render(ogr, repo, analiz, is_admin):
    st.subheader("📅 Haftalık Görev & Ödev Takibi")
    st.markdown("Öğrenciye mikro-hedefler atayın ve hafta boyunca programına uyup uymadığını kontrol edin.")
    
    col_g1, col_g2 = st.columns([1, 2])
    with col_g1:
        st.markdown("#### ➕ Yeni Ödev Ver")
        g_baslik = st.text_input("Görev/Ödev Kapsamı", placeholder="Örn: 200 Paragraf, Türev Fasikülü...")
        g_gunler = st.slider("Kaç Gün İçinde Bitecek?", 1, 30, 7)
        if st.button("📌 Görevi Ata", use_container_width=True, type="primary"):
            if g_baslik.strip():
                if not hasattr(ogr, "gorevler"):
                    ogr.gorevler = []
                ogr.gorev_ekle(g_baslik.strip(), hedefe_kalan_gun=g_gunler)
                repo.kaydet(ogr)
                st.success("✅ Ödev atandı!")
                st.rerun()
                
    with col_g2:
        st.markdown("#### 📋 Aktif Görevler")
        if not hasattr(ogr, "gorevler") or not ogr.gorevler:
            st.info("🎯 Henüz atanmış bir görev bulunmuyor.")
        else:
            bugun = date.today()
            aktif_gorevler = [g for g in ogr.gorevler if not g.tamamlandi_mi]
            tamamlanan_gorevler = [g for g in ogr.gorevler if g.tamamlandi_mi]
            
            if aktif_gorevler:
                for g in aktif_gorevler:
                    kalan_gun = (g.hedef_tarih - bugun).days
                    durum_renk = "green" if kalan_gun >= 3 else ("orange" if kalan_gun >= 0 else "red")
                    kalan_metin = f"Gecikti ({abs(kalan_gun)} gün)" if kalan_gun < 0 else f"{kalan_gun} gün kaldı"
                    
                    sc1, sc2, sc3 = st.columns([4, 2, 1])
                    with sc1:
                        st.markdown(f"**{html_module.escape(g.bashik)}**")
                        st.caption(f"Atandı: {g.olusturulma.isoformat()}")
                    with sc2:
                        st.markdown(f"<span style='color:{durum_renk}; font-weight:bold;'>{kalan_metin}</span>", unsafe_allow_html=True)
                    with sc3:
                        if st.button("✅ Yap", key=f"yap_{g.id}"):
                            g.tamamlandi_mi = True
                            repo.kaydet(ogr)
                            st.rerun()
                    st.markdown("---")
            else:
                st.success("Aktif tüm görevler bitirilmiş!")
                
            if tamamlanan_gorevler:
                with st.expander(f"📁 Biten Görevler ({len(tamamlanan_gorevler)})"):
                    for g in tamamlanan_gorevler:
                        st.markdown(f"~~{html_module.escape(g.bashik)}~~ (Hedef: {g.hedef_tarih.isoformat()})")
