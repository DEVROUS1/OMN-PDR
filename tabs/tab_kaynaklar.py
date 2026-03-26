import streamlit as st
from models.konu_verileri import konu_listesi_getir, TYT_KONULARI, AYT_KONULARI

def render(ogr, repo, analiz, is_admin):
    st.subheader("📚 Kaynak Kitap ve Konu Takibi")
    st.markdown("Öğrencinin elindeki kitapları (yayınları) ekleyin ve kitaptaki konuları tamamladıkça buradan işaretleyin.")
    
    col_k1, col_k2 = st.columns([1, 2])
    with col_k1:
        st.markdown("#### ➕ Yeni Kaynak Ekle")
        k_marka = st.text_input("Kitap / Yayın Adı", placeholder="Örn: 345 Yayınları...", key="k_marka_tab")
        
        if ogr.sinav_turu == "LGS":
            bolum_listesi = ["LGS"]
            from models.konu_verileri import LGS_KONULARI
            ders_listesi = list(LGS_KONULARI.keys())
        else:
            bolum_listesi = ["TYT", "AYT"]
            k_bolum_secim = st.radio("Sınav Bölümü", bolum_listesi, horizontal=True, key="k_bolum_radio_tab")
            ders_listesi = list(TYT_KONULARI.keys()) if k_bolum_secim == "TYT" else list(AYT_KONULARI.keys())
            k_bolum = k_bolum_secim

        k_ders_secim = st.selectbox("Ders Seçin", ders_listesi, key="k_ders_listbox_tab")
        
        if st.button("✨ Kaynağı Kütüphaneye Ekle", use_container_width=True, type="primary", key="k_add_btn"):
            if k_marka.strip():
                final_bolum = "LGS" if ogr.sinav_turu == "LGS" else k_bolum
                ogr.kaynak_ekle(k_marka.strip(), k_ders_secim, final_bolum)
                repo.kaydet(ogr)
                st.success("✅ Kaynak eklendi!")
                st.rerun()

    with col_k2:
        st.markdown("#### 📖 Kaynaklarım ve İlerleme")
        if not hasattr(ogr, "kaynaklar") or not ogr.kaynaklar:
            st.info("🎯 Henüz bir kaynak kitap eklenmemiş.")
        else:
            for k in ogr.kaynaklar:
                with st.expander(f"📔 {k.ad} ({k.bolum} {k.ders})"):
                    konular = konu_listesi_getir(k.bolum, k.ders)
                    if konular:
                        tamamlanan_sayisi = len([c for c in k.tamamlanan_konular if c in konular])
                        toplam_sayisi = len(konular)
                        yuzde = (tamamlanan_sayisi / toplam_sayisi * 100) if toplam_sayisi > 0 else 0
                        
                        st.progress(yuzde / 100)
                        st.caption(f"Tamamlanan: {tamamlanan_sayisi}/{toplam_sayisi} (%{yuzde:.0f})")
                        
                        ck_cols = st.columns(2)
                        for i, konu in enumerate(konular):
                            target_ck_col = ck_cols[i % 2]
                            is_done = konu in k.tamamlanan_konular
                            with target_ck_col:
                                res = st.checkbox(konu, value=is_done, key=f"tab_check_{k.id}_{konu}")
                                if res != is_done:
                                    if res:
                                        if konu not in k.tamamlanan_konular: k.tamamlanan_konular.append(konu)
                                    else:
                                        if konu in k.tamamlanan_konular: k.tamamlanan_konular.remove(konu)
                                    repo.kaydet(ogr)
                                    st.rerun()

                    if st.button(f"🗑️ Sil", key=f"tab_del_{k.id}", type="secondary"):
                        ogr.kaynaklar.remove(k)
                        repo.kaydet(ogr)
                        st.rerun()
