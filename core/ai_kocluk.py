import os
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class AIKoc:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.client = None
        if self.api_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                print("Groq yüklenemedi:", e)

    def yorum_uret(self, ogrenci_verisi: Dict[str, Any]) -> str:
        if not self.client:
            return "⚠️ AI servisi başlatılamadı. GROQ_API_KEY yüklü değil veya groq paketi kurulamadı."
        
        prompt = f"""Eğitim koçu olarak öğrencini değerlendir. Samimi, açık, veri odaklı ve motive edici ol!
Lütfen asla genel geçer tavsiyeler verme. Verilen netleri, çalışma saatini, stres düzeyini analiz ederek mantıklı ve somut çıkarımlar (Örn. 'uykun düşük olduğu için matematik netlerin sapmış olabilir' gibi teşhisler) yap. Ebbinghaus tekrar konularına mutlaka kısaca atıfta bulun.
Öğrenciye tam adıyla değil ismiyle (Örn: Sevgili Ahmet) hitap et. Doğrudan ona konuşan bir mektup tarzında yaz. Paragrafları rahat okunur yap. En fazla 180 kelime kullan.
Ekstra hiçbir sistem metni kullanma, direkt cevaba gir.

ÖĞRENCİ BİLGİLERİ:
Adı: {ogrenci_verisi.get('ad')}
Hedef Üniversite/Bölüm: {ogrenci_verisi.get('hedef_uni', 'Belirtilmedi')} - {ogrenci_verisi.get('hedef_bolum')}
Son Girdiği Denemelerin Notları ve Toplam Netleri: {ogrenci_verisi.get('denemeler', [])}
Son Haftaki Stres Düzeyi (10 Üzerinden, 10 çok stresli): {ogrenci_verisi.get('stres')}
Son Haftaki Ortalama Uyku Saati: {ogrenci_verisi.get('uyku')}
Son Haftaki Çalışma Süresi (Saat): {ogrenci_verisi.get('calisma_saati')}
Aralıklı Tekrar (Ebbinghaus) Bekleyen Eksik Konuları: {ogrenci_verisi.get('hatalar', [])}
"""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Sen çok yetenekli, saygın, veri analizi yapabilen ve empati kuran harika bir PDR uzmanısın. Türk eğitim ve YKS/LGS sınav sistemini kusursuz biliyorsun. Türkçeyi mükemmel kullanıyorsun ve emoji kullanmayı seviyorsun."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                max_tokens=800
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"❌ AI Yanıt Üretirken Hata Oluştu: {str(e)}"

    def veli_raporu_uret(self, ogrenci_verisi: Dict[str, Any]) -> str:
        if not self.client:
            return "⚠️ AI servisi başlatılamadı. GROQ_API_KEY yüklü değil."
            
        prompt = f"""Bir eğitim kurumu PDR (Rehberlik) servisi olarak, öğrencimizin velisine yönelik profesyonel, güven veren ve nazik bir haftalık/aylık değerlendirme raporu yaz.
Veliyi endişelendirmeden (ancak eksikleri de gizlemeden) durum analizi yap. Net değişimlerini, hedefine ne kadar yakın olduğunu ve bizim Ebbinghaus tekrar sistemiyle onun zayıf konularını nasıl kapattığımızı kısaca anlat.
WhatsApp üzerinden veliye gönderilebilecek kıvamda, kibar bir dille yaz (Örn: "Sayın Velimiz, Ahmet'in bu haftaki..."). En fazla 150 kelime kullan, rahat okunur paragraflara böl.

ÖĞRENCİ BİLGİLERİ:
Adı: {ogrenci_verisi.get('ad')}
Hedef: {ogrenci_verisi.get('hedef_uni', 'Belirtilmedi')} - {ogrenci_verisi.get('hedef_bolum')}
Son Girdiği Deneme Netleri: {ogrenci_verisi.get('denemeler', [])}
Son Haftaki Stres (10 Üzerinden, 10 çok stresli): {ogrenci_verisi.get('stres')}
Son Haftaki Uyku Ortalama: {ogrenci_verisi.get('uyku')}
Ebbinghaus Tekrar Sistemiyle Takip Ettiğimiz Eksikleri: {ogrenci_verisi.get('hatalar', [])}
"""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "Sen çok saygın, kurumsal bir dille konuşan deneyimli bir Eğitim Koordinatörü ve PDR uzmanısın. Velilere aşırı uzun olmayan, güven verici mesajlar atıyorsun."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=600
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"❌ Veli Raporu Üretilirken Hata Oluştu: {str(e)}"
    def sohbet_yaniti_uret(self, mesaj: str, ogrenci_verisi: Dict[str, Any], gecmis: List[Dict[str, str]]) -> str:
        if not self.client:
            return "⚠️ AI servisi başlatılamadı. GROQ_API_KEY yüklü değil."
            
        sys_prompt = f"""Sen öğrencilere birebir koçluk yapan, onları çok iyi tanıyan, samimi, zeki ve motive edici bir AI Koçsun. 
Senin adın 'OmniAI'. Şu an karşındaki öğrencinin tüm verilerine vakıfsın.

ÖĞRENCİ VERİLERİ (Context):
- İsim: {ogrenci_verisi.get('ad')}
- Hedef: {ogrenci_verisi.get('hedef_uni', '')} / {ogrenci_verisi.get('hedef_bolum', '')}
- Son Deneme Neti: {ogrenci_verisi.get('son_net', 'Henüz girilmemiş')}
- Burnout Seviyesi: {ogrenci_verisi.get('burnout', 'Normal')}

KURALLAR:
1. Kısa ve öz konuş (max 120 kelime).
2. Kesinlikle genel tavsiye verme, öğrencinin verilerine (net, hedef vb.) atıfta bulun.
3. Motivasyonu daima yüksek tut ama gerçekçi ol.
4. Emoji kullanmayı unutma.
5. Sadece Türkçe konuş.
"""
        messages = [{"role": "system", "content": sys_prompt}]
        
        # Geçmişi ekle
        for g in gecmis:
            messages.append({
                "role": g["role"],
                "content": g["icerik"]
            })
            
        # Yeni mesajı ekle
        messages.append({"role": "user", "content": mesaj})
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=600
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"❌ Sohbet Hatası: {str(e)}"
