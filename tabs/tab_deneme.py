import streamlit as st
from datetime import date
from models.ogrenci_sinifi import DenemeKaydi
from core.puan_hesaplama import TYT_DERSLER, AYT_DERSLER, LGS_DERSLER, net_hesapla_yks, net_hesapla_lgs

def render(ogr, repo, analiz, is_admin):
    st.subheader("📝 Deneme Kaydı Ekle")
    
    with st.form("deneme_ekle_form"):
        tarih = st.date_input("Sınav Tarihi", date.today())
        puan_turu = st.radio("Puan Türü", ["TYT", "AYT"] if ogr.sinav_turu == "YKS" else ["LGS"], horizontal=True)
        
        ders_list = TYT_DERSLER if puan_turu == "TYT" else (AYT_DERSLER if puan_turu == "AYT" else LGS_DERSLER)
        
        c1, c2, c3 = st.columns(3)
        netler = {}
        for idx, ders in enumerate(ders_list):
            target_col = [c1, c2, c3][idx % 3]
            with target_col:
                st.markdown(f"**{ders}**")
                dogru = st.number_input(f"{ders} D", 0, 40, 0, key=f"d_{ders}")
                yanlis = st.number_input(f"{ders} Y", 0, 40, 0, key=f"y_{ders}")
                
                # Net hesapla
                if ogr.sinav_turu == "YKS":
                    net = net_hesapla_yks(dogru, yanlis)
                else:
                    net = net_hesapla_lgs(dogru, yanlis)
                netler[ders] = net
                
        st.markdown("---")
        cal_saat = st.slider("Önceki Gün Çalışma Saati", 0.0, 16.0, 6.0)
        stres = st.select_slider("Stres Seviyesi (1: Düşük, 10: Yüksek)", range(1, 11), 5)
        uyku = st.slider("Uyku Saati", 0.0, 12.0, 7.5)
        
        if st.form_submit_button("✅ Kaydet / Güncelle", use_container_width=True):
            yeni = DenemeKaydi(
                tarih=tarih,
                netleri=netler,
                calisma_saati=cal_saat,
                stres_puani=stres,
                uyku_saati=uyku
            )
            ogr.deneme_ekle(yeni)
            repo.kaydet(ogr)
            st.success("✅ Deneme başarıyla kaydedildi!")
            st.rerun()

    if ogr.deneme_kayitlari:
        st.markdown("#### 📋 Son Kayıtlar")
        for i, d in enumerate(reversed(ogr.deneme_kayitlari[-5:])):
            with st.expander(f"{d.tarih} | {sum(d.netleri.values()):.2f} Net"):
                st.write(d.netleri)
                if st.button("🗑️ Sil", key=f"del_d_{i}"):
                    ogr.deneme_kayitlari.remove(d)
                    repo.kaydet(ogr)
                    st.rerun()
