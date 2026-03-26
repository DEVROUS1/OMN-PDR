import streamlit as st
from core.yokatlas_verileri import bolum_ara, universite_oner
from utils.ui_helpers import format_siralama
from core.puan_hesaplama import tam_puan_hesapla, _siralama_tahmin

def render(ogr, repo, analiz, is_admin):
    st.subheader("🏛️ Üniversite & Bölüm Önerileri")
    
    if ogr.sinav_turu == "LGS":
        st.info("LGS için lise taban puanları yakında eklenecek. Şimdilik YKS odaklı çalışmaktadır.")
        return

    if not ogr.deneme_kayitlari:
        st.warning("Öneri alabilmek için en az 1 deneme sonucu girilmelidir.")
        return
        
    son_deneme = ogr.deneme_kayitlari[-1]
    p_turu = ogr.hedef_puan_turu
    sonuc = tam_puan_hesapla(son_deneme.netleri, p_turu, ogr.obp, ogr.sinav_turu)
    puan = sonuc.yerlestirme_puani
    sira = sonuc.tahmini_siralama
    
    st.markdown(f"**Güncel Sıralamanız:** `{format_siralama(sira)}` | **Puan Türü:** `{p_turu}`")
    st.markdown("---")

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        s_sehir = st.multiselect("Şehir Tercihi (Boş ise hepsi)", ["Ankara", "İstanbul", "İzmir", "Eskişehir", "Bursa", "Antalya"])
    with col_s2:
        s_bolum = st.text_input("Bölüm Ara (Örn: Bilgisayar, Hukuk...)", value=ogr.hedef_bolum if ogr.hedef_bolum != "Belirlenmedi" else "")

    if st.button("🔍 Uygun Programları Listele", use_container_width=True):
        öneriler = universite_oner(sira, p_turu, bolum_filtresi=s_bolum if s_bolum else None)
        
        if not öneriler:
            st.info("Kriterlere uygun sonuç bulunamadı. Lütfen filtreleri genişletin.")
        else:
            for uni in öneriler:
                # Durum belirle
                fark = sira - uni.siralama
                if fark < -20000: # Sıralaması bizden çok yukarda
                    durum, cls = "ZOR / ŞANS", "badge-sans"
                elif fark < 10000: # Yakın
                    durum, cls = "DENGELİ", "badge-dengeli"
                else:
                    durum, cls = "GÜVENLİ", "badge-guvenli"
                
                st.markdown(f"""
                <div class="uni-card">
                    <div style="display:flex; justify-content:space-between; align-items:start;">
                        <div>
                            <div class="uni-card-title">{uni.universite}</div>
                            <div class="uni-card-subtitle">{uni.bolum} ({uni.puan_turu})</div>
                        </div>
                        <div class="uni-card-badge {cls}">{durum}</div>
                    </div>
                    <div style="margin-top:12px; display:flex; gap:20px; font-size:0.85rem;">
                        <span style="color:var(--text-secondary);">Taban Sıralama: <b>{format_siralama(uni.siralama)}</b></span>
                        <span style="color:var(--text-secondary);">Taban Puan: <b>{uni.taban_puan}</b></span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
