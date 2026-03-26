import streamlit as st
from core.ai_kocluk import AIKoc

def render(ogr, repo, analiz, is_admin):
    st.subheader("🤖 AI Koçun OmniAI")
    st.info("OmniAI senin akademik verilerini biliyor. Ona sınavların, hedeflerin veya motivasyonun hakkında soru sorabilirsin.")

    # Sohbet geçmişi anahtarı
    chat_key = f"sohbet_{ogr.ogrenci_id}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
        
        # İlk selamlama (otomatik)
        burnout_v = analiz.tukenmislik_riski_hesapla()
        son_net_v = sum(ogr.deneme_kayitlari[-1].netleri.values()) if ogr.deneme_kayitlari else 0
        
        ilk_mesaj = f"Selam {ogr.ad}! 👋 Ben senin koçun OmniAI. Son denemende {son_net_v} net yapmışsın ve yorgunluk seviyen %{burnout_v:.1f}. Bugün nasıl hissediyorsun?"
        st.session_state[chat_key].append({"role": "assistant", "icerik": ilk_mesaj})

    # Sohbeti temizle
    if st.button("🗑️ Sohbeti Temizle", key="clear_ai_tab"):
        st.session_state[chat_key] = []
        st.rerun()

    # Geçmişi göster
    for m in st.session_state[chat_key]:
        with st.chat_message(m["role"]):
            st.markdown(m["icerik"])

    # Yeni mesaj girişi
    if prompt_text := st.chat_input("Mesajınızı yazın..."):
        st.session_state[chat_key].append({"role": "user", "icerik": prompt_text})
        with st.chat_message("user"):
            st.markdown(prompt_text)

        ai_k = AIKoc()
        burnout_v = analiz.tukenmislik_riski_hesapla()
        son_net_v = sum(ogr.deneme_kayitlari[-1].netleri.values()) if ogr.deneme_kayitlari else 0
        
        c_data = {
            "ad": ogr.ad,
            "hedef_uni": getattr(ogr, "hedef_uni", ""),
            "hedef_bolum": ogr.hedef_bolum,
            "son_net": son_net_v,
            "burnout": f"%{burnout_v:.1f}"
        }
        
        with st.chat_message("assistant"):
            with st.spinner("OmniAI yanıtlıyor..."):
                yanit = ai_k.sohbet_yaniti_uret(prompt_text, c_data, st.session_state[chat_key][:-1])
                st.markdown(yanit)
                st.session_state[chat_key].append({"role": "assistant", "icerik": yanit})
