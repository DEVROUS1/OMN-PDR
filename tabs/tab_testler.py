import streamlit as st
import math
import pandas as pd
import plotly.express as px
import subprocess
import sys
from models.test_verileri import tum_testleri_getir

def render(ogr, repo, analiz, is_admin):
    st.subheader("🧠 Akademik PDR Testleri & Analiz")
    st.markdown("Kendinizi daha iyi tanımanız ve gelişiminizi takip etmeniz için bilimsel envanterler.")
    
    testler = tum_testleri_getir()
    secilen_test_adi = st.selectbox("Test Seçiniz", [t.ad for t in testler])
    secilen_test = next((t for t in testler if t.ad == secilen_test_adi), None)
    
    if secilen_test:
        st.info(f"ℹ️ **{secilen_test.aciklama}**")
        st.markdown("---")
        
        # Session state ile cevapları sakla
        cevap_key = f"cevaplar_{secilen_test.id}_{ogr.ogrenci_id}"
        if cevap_key not in st.session_state:
            st.session_state[cevap_key] = {}
            
        cevaplar = st.session_state[cevap_key]
        
        # Sayfalama
        SORU_PER_PAGE = 10
        total_pages = math.ceil(len(secilen_test.sorular) / SORU_PER_PAGE)
        
        page_key = f"page_{secilen_test.id}_{ogr.ogrenci_id}"
        if page_key not in st.session_state:
            st.session_state[page_key] = 1
            
        current_page = st.session_state[page_key]
        
        # İlerleme
        doluluk = len(cevaplar) / len(secilen_test.sorular)
        st.progress(doluluk, text=f"Tamamlanma: %{int(doluluk*100)}")
        
        # Soruları Getir
        start_idx = (current_page - 1) * SORU_PER_PAGE
        end_idx = min(start_idx + SORU_PER_PAGE, len(secilen_test.sorular))
        page_sorular = secilen_test.sorular[start_idx:end_idx]
        
        with st.form(key=f"form_{secilen_test.id}_{current_page}"):
            st.markdown(f"**Sayfa {current_page} / {total_pages}**")
            
            for soru in page_sorular:
                st.markdown(f"**{soru.id}. {soru.metin}**")
                val = cevaplar.get(str(soru.id), 3 if secilen_test.id == "sinav_kaygisi" else 0)
                
                if secilen_test.id == "sinav_kaygisi":
                     yeni_val = st.slider(f"Soru {soru.id}", 1, 5, int(val), key=f"q_{secilen_test.id}_{soru.id}", label_visibility="collapsed")
                elif secilen_test.id == "holland_ilgi":
                     opts = ["Hoşlanmam (0)", "Fark Etmez (1)", "Hoşlanırım (2)"]
                     idx = int(val)
                     secim = st.radio(f"Soru {soru.id}", opts, index=idx, horizontal=True, key=f"q_{secilen_test.id}_{soru.id}", label_visibility="collapsed")
                     yeni_val = opts.index(secim)
                else:
                     yeni_val = st.slider(f"Soru {soru.id}", 1, 5, int(val), key=f"q_{secilen_test.id}_{soru.id}", label_visibility="collapsed")
                
                cevaplar[str(soru.id)] = yeni_val

            col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
            with col_btn1:
                if current_page > 1:
                    if st.form_submit_button("⬅️ Önceki"):
                         st.session_state[page_key] -= 1
                         st.rerun()
            with col_btn3:
                if current_page < total_pages:
                    if st.form_submit_button("Sonraki ➡️"):
                         st.session_state[page_key] += 1
                         st.rerun()
                else:
                    if st.form_submit_button("✅ Testi Bitir"):
                         if len(cevaplar) < len(secilen_test.sorular):
                              st.warning("Eksik sorular var!")
                         else:
                              from core.test_analiz import analiz_et
                              sonuc = analiz_et(secilen_test.id, cevaplar, secilen_test.sorular)
                              st.session_state[f"sonuc_{secilen_test.id}_{ogr.ogrenci_id}"] = sonuc
                              st.rerun()

        # Sonuç Gösterimi
        sonuc_key = f"sonuc_{secilen_test.id}_{ogr.ogrenci_id}"
        if sonuc_key in st.session_state:
            sonuc = st.session_state[sonuc_key]
            st.markdown("---")
            st.success("🎉 Analiz Tamamlandı!")
            
            if secilen_test.id == "holland_ilgi":
                st.subheader(f"🏷️ Mesleki Kodunuz: **{sonuc['kod']}**")
                st.write(sonuc["genel_yorum"])
                for item in sonuc["detay"]:
                    with st.expander(f"🔹 {item['tip']} ({item['puan']} Puan)"):
                        st.markdown(f"_{item['yorum']}_")
                        st.markdown(f"**Önerilen Meslekler:** {item['oneriler']}")
                        
            elif secilen_test.id == "coklu_zeka":
                st.subheader(f"🧠 Baskın Zeka: **{sonuc['baskin_tip']}**")
                st.info(sonuc["yorum"])
                data = dict(sonuc["tum_sirala"])
                df_radar = pd.DataFrame(dict(r=list(data.values()), theta=list(data.keys())))
                fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True)
                fig.update_layout(template="plotly_dark", height=400)
                st.plotly_chart(fig, use_container_width=True)
                
            elif secilen_test.id == "sinav_kaygisi":
                st.subheader(f"Seviye: **{sonuc['seviye']}** (%{sonuc['yuzde']})")
                st.write(sonuc["yorum"])
                if sonuc["oneriler"]:
                    st.warning("💡 **Öneriler:**")
                    for oneri in sonuc["oneriler"]: st.markdown(f"- {oneri}")
