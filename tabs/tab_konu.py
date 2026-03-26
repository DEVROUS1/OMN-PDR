import streamlit as st
from models.konu_verileri import konu_listesi_getir, tum_dersler, TYT_KONULARI, AYT_KONULARI, LGS_KONULARI

def render(ogr, repo, analiz, is_admin):
    st.subheader("📚 Konu Tamamlama Takibi")
    
    if ogr.sinav_turu == "LGS":
        dersler = list(LGS_KONULARI.keys())
        sinav_bolumleri = ["LGS"]
    else:
        sinav_bolumleri = ["TYT", "AYT"]
        
    for bolum in sinav_bolumleri:
        st.markdown(f"#### 🏷️ {bolum} Konuları")
        
        ders_list = list(TYT_KONULARI.keys()) if bolum == "TYT" else list(AYT_KONULARI.keys())
        if bolum == "LGS": ders_list = list(LGS_KONULARI.keys())
        
        cols = st.columns(3)
        for idx, ders in enumerate(ders_list):
            target_col = cols[idx % 3]
            with target_col:
                konular = konu_listesi_getir(bolum, ders)
                # Tamamlanma oranı
                total = len(konular)
                done = sum(1 for k in konular if ogr.konu_tamamlandi_mi(bolum, ders, k))
                oran = (done / total) if total > 0 else 0
                
                with st.expander(f"{ders} (%{int(oran*100)})"):
                    # Ana Progress
                    st.progress(oran)
                    
                    for k_adi in konular:
                        is_ok = ogr.konu_tamamlandi_mi(bolum, ders, k_adi)
                        check = st.checkbox(k_adi, value=is_ok, key=f"kb_{bolum}_{ders}_{k_adi}")
                        if check != is_ok:
                            ogr.konu_ilerlemesi_guncelle(bolum, ders, k_adi, check)
                            repo.kaydet(ogr)
                            st.rerun()
        st.markdown("---")

    # ZPD Analizi (Yakınsal Gelişim Alanı)
    st.markdown("#### 🚀 ZPD: Odaklanman Gereken Konular")
    oneriler = analiz.zpd_analizi_yap()
    if oneriler:
        for oneri in oneriler:
            st.warning(f"**{oneri['ders']}**: {oneri['konu']} (Bu konuyu bitirmen +{oneri['puan_katkisi']:.1f} puan kazandırabilir)")
    else:
        st.success("Tebrikler! Belirlediğin net hedeflerine göre tüm kritik konuları tamamlamış görünüyorsun.")
