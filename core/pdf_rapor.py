import os
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfbase
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.linecharts import HorizontalLineChart

class PDFRaporcu:
    def __init__(self):
        self.font_name = self._font_kaydet()
        self.styles = getSampleStyleSheet()
        self._stilleri_olustur()

    def _font_kaydet(self):
        # Türkçe karakter desteği için sistem fontlarını kontrol et
        paths = [
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\tahoma.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "DejaVuSans.ttf"
        ]
        for p in paths:
            if os.path.exists(p):
                pdfbase.registerFont(TTFont('TurkceFont', p))
                return 'TurkceFont'
        return 'Helvetica'

    def _stilleri_olustur(self):
        self.styles.add(ParagraphStyle(
            name='AnaBaslik',
            fontName=self.font_name,
            fontSize=22,
            alignment=1,
            spaceAfter=25,
            textColor=colors.HexColor("#1a1d29")
        ))
        self.styles.add(ParagraphStyle(
            name='KisimBaslik',
            fontName=self.font_name,
            fontSize=14,
            spaceBefore=15,
            spaceAfter=10,
            textColor=colors.HexColor("#1a1d29"),
            borderPadding=5,
            borderWidth=0,
            leftIndent=0
        ))
        self.styles.add(ParagraphStyle(
            name='GovdeMetin',
            fontName=self.font_name,
            fontSize=10,
            leading=12,
            textColor=colors.black
        ))

    def rapor_olustur(self, ogr, ai_notu=""):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=50, bottomMargin=50)
        elements = []

        # 1. Başlık ve Logo Placeholder
        d = Drawing(100, 40)
        d.add(Rect(0, 0, 100, 40, fillColor=colors.HexColor("#f0f0f0")))
        d.add(String(25, 15, "OmniPDR", fontName=self.font_name, fontSize=12, fillColor=colors.grey))
        elements.append(d)
        elements.append(Spacer(1, 10))
        
        elements.append(Paragraph(f"Bireysel Koçluk & PDR Değerlendirme Raporu", self.styles['AnaBaslik']))
        elements.append(Paragraph(f"<b>Öğrenci:</b> {ogr.ad}", self.styles['GovdeMetin']))
        elements.append(Paragraph(f"<b>Tarih:</b> {datetime.now().strftime('%d.%m.%Y')}", self.styles['GovdeMetin']))
        elements.append(Spacer(1, 20))

        # 2. Öğrenci Profili
        elements.append(Paragraph("👤 Öğrenci Profili", self.styles['KisimBaslik']))
        p_data = [
            ["Okul:", ogr.okul],
            ["Hedef:", f"{getattr(ogr, 'hedef_uni', '')} / {ogr.hedef_bolum}"],
            ["Sınav Türü:", f"{ogr.sinav_turu} ({ogr.hedef_puan_turu})"]
        ]
        t_p = Table(p_data, colWidths=[100, 350])
        t_p.setStyle(TableStyle([
            ('FONTNAME', (0,0), (-1,-1), self.font_name),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        elements.append(t_p)

        # 3. Son Denemeler Tablosu
        elements.append(Paragraph("📊 Son Deneme Performansları", self.styles['KisimBaslik']))
        denemeler = ogr.deneme_kayitlari[-5:]
        if denemeler:
            d_data = [["Tarih", "Toplam Net"]]
            # En son sınavın derslerini de sütun olarak ekleyelim (varsa)
            main_subjects = list(denemeler[-1].netleri.keys())[:4] # İlk 4 dersi gösterelim
            d_data[0].extend(main_subjects)
            
            for d in reversed(denemeler):
                row = [d.tarih.strftime('%d.%m'), f"{sum(d.netleri.values()):.1f}"]
                for s in main_subjects:
                    row.append(f"{d.netleri.get(s, 0.0):.1f}")
                d_data.append(row)
            
            t_d = Table(d_data)
            t_d.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1a1d29")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f5f5f5")),
                ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
            ]))
            elements.append(t_d)
            
            # Grafiği Ekle
            elements.append(Spacer(1, 15))
            elements.append(self._grafik_olustur(denemeler))
        else:
            elements.append(Paragraph("Henüz deneme kaydı girilmemiş.", self.styles['GovdeMetin']))

        # 4. Konu ve Tekrar Durumu
        elements.append(Paragraph("📚 Gelişim ve Tekrar Durumu", self.styles['KisimBaslik']))
        
        # Konu Özeti
        lesson_stats = {}
        for k in ogr.konu_ilerlemeleri:
            lesson_stats[k.ders] = lesson_stats.get(k.ders, 0) + (1 if k.tamamlandi_mi else 0)
        
        c_cols = []
        for d, sayi in list(lesson_stats.items())[:6]: # İlk 6 ders
            c_cols.append(f"<b>{d}:</b> {sayi} konu tamam")
        
        elements.append(Paragraph(" • ".join(c_cols), self.styles['GovdeMetin']))
        
        # Bekleyen Tekrarlar
        eksikler = [h.konu for h in ogr.hata_kayitlari if h.bekleyen_tekrar_sayisi > 0]
        if eksikler:
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(f"<b>⚠️ Bekleyen Ebbinghaus Tekrarları:</b> {', '.join(eksikler[:10])}", self.styles['GovdeMetin']))

        # 5. Görüşme Notları
        if ogr.gorusme_notlari:
            elements.append(Paragraph("📓 Danışman Gözlemleri", self.styles['KisimBaslik']))
            son = ogr.gorusme_notlari[-1]
            mod_metin = {1:"Çok Düşük", 2:"Düşük", 3:"Normal", 4:"İyi", 5:"Çok İyi"}.get(son.duygu_modu, "Normal")
            elements.append(Paragraph(f"<b>Son Görüşme ({son.tarih.strftime('%d.%m.%Y')}):</b> {son.icerik}", self.styles['GovdeMetin']))
            elements.append(Paragraph(f"<b>Motivasyon Modu:</b> {mod_metin}", self.styles['GovdeMetin']))

        # 6. AI Değerlendirmesi
        if ai_notu:
            elements.append(Paragraph("🤖 Yapay Zeka Koç Değerlendirmesi", self.styles['KisimBaslik']))
            # Markdown temizliği (basit)
            temiz_not = ai_notu.replace("**", "").replace("#", "")
            elements.append(Paragraph(temiz_not, self.styles['GovdeMetin']))

        # PDF oluştur
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

    def _grafik_olustur(self, denemeler):
        drawing = Drawing(400, 150)
        data = [tuple(sum(d.netleri.values()) for d in denemeler)]
        
        lp = HorizontalLineChart()
        lp.x = 20
        lp.y = 20
        lp.height = 100
        lp.width = 350
        lp.data = data
        lp.joinedLines = 1
        lp.lines[0].strokeColor = colors.HexColor("#1a1d29")
        lp.lines[0].strokeWidth = 2
        lp.fillColor = colors.HexColor("#f5f5f5")
        
        # Eksen Ayarları
        lp.categoryAxis.categoryNames = [d.tarih.strftime('%d.%m') for d in denemeler]
        lp.categoryAxis.labels.fontName = self.font_name
        lp.categoryAxis.labels.fontSize = 7
        lp.valueAxis.labels.fontName = self.font_name
        lp.valueAxis.labels.fontSize = 7
        
        drawing.add(lp)
        return drawing
