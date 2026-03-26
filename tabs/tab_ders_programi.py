import streamlit as st
from datetime import date

def render(ogr, repo, analiz, is_admin):
    st.subheader("📋 Etkileşimli Ders Programı Oluşturucu")
    st.markdown("Gönderdiğiniz haftalık program şablonunu (görselini) yükleyin ve öğrenci programını üzerine dijital olarak yazdırıp indirin.")

    sablon_dosya = st.file_uploader("Şablon Arka Planı Yükle (.png, .jpg)", type=["png", "jpg", "jpeg"])
    
    if sablon_dosya:
        dp_tarih = st.text_input("Tarih / Hafta Bilgisi", value=f"{date.today().strftime('%d.%m.%Y')} Haftası")
        st.markdown("#### Günlük Programları Giriniz")
        
        r1_c1, r1_c2, r1_c3, r1_c4 = st.columns(4)
        veri_dict = {"Tarih": dp_tarih}
        with r1_c1: veri_dict["Pazartesi"] = st.text_area("Pazartesi", height=120)
        with r1_c2: veri_dict["Salı"] = st.text_area("Salı", height=120)
        with r1_c3: veri_dict["Çarşamba"] = st.text_area("Çarşamba", height=120)
        with r1_c4: veri_dict["Perşembe"] = st.text_area("Perşembe", height=120)
        
        r2_c1, r2_c2, r2_c3, r2_c4 = st.columns(4)
        with r2_c1: veri_dict["Cuma"] = st.text_area("Cuma", height=120)
        with r2_c2: veri_dict["Cumartesi"] = st.text_area("Cumartesi", height=120)
        with r2_c3: veri_dict["Pazar"] = st.text_area("Pazar", height=120)
        
        if st.button("🚀 Programı Görsel Olarak Oluştur", use_container_width=True, type="primary"):
            try:
                from core.program_yazdirici import create_schedule_image
                sablon_bytes = sablon_dosya.getvalue()
                output_bytes = create_schedule_image(sablon_bytes, veri_dict)
                
                st.success("✅ Ders Programı başarıyla hazırlandı!")
                st.image(output_bytes, caption="Önizleme", use_container_width=True)
                
                st.download_button(
                    label="📥 Proramı Cihaza İndir (PNG)",
                    data=output_bytes,
                    file_name=f"Ders_Programi_{ogr.ad.replace(' ', '_')}.png",
                    mime="image/png",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Görsel oluşturulurken bir hata oluştu: {str(e)}")
    else:
        st.info("👉 Devam etmek için lütfen boş bir Ders Programı şablonu (resmi) yükleyin.")
