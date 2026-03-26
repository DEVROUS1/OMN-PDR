import streamlit as st
from datetime import datetime
import html as html_module

YKS_TARIH = datetime(2026, 6, 13)
LGS_TARIH = datetime(2026, 6, 7)

def geri_sayim_goster(sinav_turu="YKS"):
    hedef = YKS_TARIH if sinav_turu == "YKS" else LGS_TARIH
    bugun = datetime.now()
    fark = hedef - bugun

    if fark.days < 0:
        st.info(f"📅 {sinav_turu} 2026 tamamlandı!")
        return

    gun = fark.days
    saat = fark.seconds // 3600
    dakika = (fark.seconds % 3600) // 60

    cols = st.columns(3)
    with cols[0]:
        st.markdown(f"""
        <div class="countdown-box">
            <div class="countdown-number">{gun}</div>
            <div class="countdown-label">Gün</div>
        </div>""", unsafe_allow_html=True)
    with cols[1]:
        st.markdown(f"""
        <div class="countdown-box">
            <div class="countdown-number">{saat}</div>
            <div class="countdown-label">Saat</div>
        </div>""", unsafe_allow_html=True)
    with cols[2]:
        st.markdown(f"""
        <div class="countdown-box">
            <div class="countdown-number">{dakika}</div>
            <div class="countdown-label">Dakika</div>
        </div>""", unsafe_allow_html=True)

def metric_card(etiket, deger, renk="var(--gradient-1)"):
    escaped_deger = html_module.escape(str(deger))
    escaped_etiket = html_module.escape(str(etiket))
    return f"""
    <div class="metric-card">
        <div class="metric-value" style="background:{renk};-webkit-background-clip:text;-webkit-text-fill-color:transparent;">{escaped_deger}</div>
        <div class="metric-label">{escaped_etiket}</div>
    </div>"""

def format_siralama(s):
    if s is None:
        return "—"
    if s >= 1_000_000:
        return f"{s/1_000_000:.1f}M"
    if s >= 1_000:
        return f"{s/1_000:,.0f}K".replace(",", ".")
    return str(s)
