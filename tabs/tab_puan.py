import streamlit as st
import plotly.graph_objects as go
from utils.ui_helpers import format_siralama
from core.puan_hesaplama import tam_puan_hesapla

def render(ogr, repo, analiz, is_admin):
    st.subheader("🎯 Tahmini Puan ve Sıralama")
    
    if not ogr.deneme_kayitlari:
        st.info("Sıralama tahmini için en az bir deneme sonucu girilmelidir.")
        return

    # Hesaplamalar
    son_deneme = ogr.deneme_kayitlari[-1]
    puan_turu = ogr.hedef_puan_turu
    
    # Yeni API: Tek dict alıyor
    sonuc = tam_puan_hesapla(son_deneme.netleri, puan_turu, ogr.obp, ogr.sinav_turu)
    
    tahmini_puan = sonuc.yerlestirme_puani
    tahmini_sira = sonuc.tahmini_siralama

    # UI
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Son Sınav Tahmini Puan", f"{tahmini_puan:.2f}")
    with c2:
        # Hedefe olan mesafe
        hedef_puan = getattr(ogr, 'hedef_taban_puan', 0.0)
        puan_fark = tahmini_puan - hedef_puan
        st.metric("Hedef Puan Durumu", f"{hedef_puan:.1f}", delta=f"{puan_fark:+.1f}")
    with c3:
        hedef_sira = getattr(ogr, 'hedef_siralama', 50000)
        sira_fark = hedef_sira - tahmini_sira 
        st.metric("Tahmini Sıralama", format_siralama(tahmini_sira), delta=f"{sira_fark:+d}", delta_color="normal")

    st.markdown("---")
    st.markdown("#### 🏁 Hedef Analiz Grafiği")
    
    # Progress gauge
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = tahmini_puan,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"Hedef: {ogr.hedef_bolum}", 'font': {'size': 24}},
        delta = {'reference': hedef_puan, 'increasing': {'color': "green"}},
        gauge = {
            'axis': {'range': [100, 500 if ogr.sinav_turu=="LGS" else 560], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "#6C63FF"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, hedef_puan], 'color': 'rgba(108,99,255,0.1)'},
                {'range': [hedef_puan, 560], 'color': 'rgba(0,230,118,0.1)'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': hedef_puan
            }
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Inter"})
    st.plotly_chart(fig, use_container_width=True)
