import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
from utils.ui_helpers import metric_card, format_siralama, geri_sayim_goster
import html as html_module

def render(ogr, repo, analiz, is_admin, tum_ogrenciler=None, notify_func=None, auto_notify_func=None):
    # Admin Bildirim Bölümü
    if is_admin and tum_ogrenciler and notify_func:
        with st.expander("🔔 Bildirim Ayarları & Manuel Kontrol"):
            st.info("Kritik eşikleri aşan öğrenciler için e-posta bildirimi alabilirsiniz.")
            c_ebb = st.checkbox("Geciken Ebbinghaus tekrarı >= 5 olanları bildir", value=True)
            c_gorus = st.checkbox("Son 7 gündür görüşülmeyenleri bildir", value=True)
            c_dusus = st.checkbox("3 sınav üst üste net düşenleri bildir", value=True)
            
            sc_c1, sc_c2 = st.columns(2)
            with sc_c1:
                if st.button("🚀 Şimdi Kontrol Et ve Bildirim Gönder", use_container_width=True):
                    with st.spinner("Kontrol ediliyor..."):
                        sonuc = notify_func(tum_ogrenciler, c_ebb, c_gorus, c_dusus)
                        if sonuc:
                            st.success(f"Bildirim e-postası gönderildi! ({len(sonuc)} uyarı)")
                            for s in sonuc: st.write(s)
                        else:
                            st.info("Kriterlere uyan kritik durum bulunamadı.")
            
            with sc_c2:
                auto_on = st.toggle("Uygulama açılışında günlük kontrol", value=False)
                if auto_on and auto_notify_func:
                    auto_notify_func(tum_ogrenciler)
                    st.caption("✅ Günlük kontrol aktif. Son 24 saat içinde bildirim gönderildiyse tekrar gönderilmez.")

    # Geri sayım
    geri_sayim_goster(ogr.sinav_turu)
    st.markdown("<br>", unsafe_allow_html=True)

    # Üst metrikler
    deneme_sayisi = len(ogr.deneme_kayitlari)
    if deneme_sayisi > 0:
        son_deneme = ogr.deneme_kayitlari[-1]
        son_toplam_net = sum(son_deneme.netleri.values())
        ortalama_net = sum(
            sum(d.netleri.values()) for d in ogr.deneme_kayitlari
        ) / deneme_sayisi

        # Trend hesapla
        if deneme_sayisi >= 2:
            onceki_net = sum(ogr.deneme_kayitlari[-2].netleri.values())
            trend = son_toplam_net - onceki_net
            trend_icon = "📈" if trend > 0 else ("📉" if trend < 0 else "➡️")
            trend_metin = f"{trend_icon} {abs(trend):.1f}"
        else:
            trend_metin = "Veri bekleniyor"

        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(metric_card("Son Toplam Net", f"{son_toplam_net:.2f}"), unsafe_allow_html=True)
        with m2: st.markdown(metric_card("Gelişim Trendi", trend_metin, renk="var(--gradient-2)"), unsafe_allow_html=True)
        with m3: st.markdown(metric_card("Genel Net Ort.", f"{ortalama_net:.2f}", renk="var(--gradient-3)"), unsafe_allow_html=True)
        with m4: st.markdown(metric_card("Diploma Notu (OBP)", f"{ogr.obp:.1f}", renk="var(--gradient-3)"), unsafe_allow_html=True)

    # Orta Panel: Analiz ve Grafik
    col_l, col_r = st.columns([2, 1])

    with col_l:
        st.markdown("#### 📉 Net Gelişim Analizi")
        if deneme_sayisi > 0:
            df_net = pd.DataFrame([
                {"Tarih": d.tarih, "Net": sum(d.netleri.values())}
                for d in ogr.deneme_kayitlari
            ])
            fig = px.line(df_net, x="Tarih", y="Net", markers=True)
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color="#9AA0A6",
                margin=dict(l=0, r=0, t=20, b=0),
                height=300,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="#2d3250"),
                template="plotly_dark"
            )
            fig.update_traces(line_color="#6C63FF", line_width=3, marker=dict(size=8, color="#00D2FF"))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Grafik için en az 1 deneme kaydı gerekli.")

    with col_r:
        st.markdown("#### 🧠 Durum Özeti")
        burnout = analiz.tukenmislik_riski_hesapla()
        risk_renk = "green" if burnout < 30 else ("orange" if burnout < 60 else "red")
        
        st.markdown(f"""
        <div style="background:var(--bg-card); padding:20px; border-radius:16px; border:1px solid var(--border-color);">
            <div style="color:var(--text-secondary); font-size:0.8rem; text-transform:uppercase; letter-spacing:1px;">Burnout (Yorgunluk) Riski</div>
            <div style="font-size:2rem; font-weight:800; color:{risk_renk}; margin:10px 0;">%{burnout:.1f}</div>
            <div style="height:8px; background:var(--bg-hover); border-radius:4px; overflow:hidden;">
                <div style="width:{burnout}%; height:100%; background:{risk_renk};"></div>
            </div>
            <p style="font-size:0.85rem; color:var(--text-secondary); margin-top:15px;">
                {analiz.kritik_uyarilari_getir()[0].mesaj if analiz.kritik_uyarilari_getir() else "Her şey yolunda görünüyor. Tempo istikrarlı."}
            </p>
        </div>
        """, unsafe_allow_html=True)
