
import os
import json
from bs4 import BeautifulSoup
import glob

# Hedef dosya
OUTPUT_JSON = "data/yokatlas_full.json"
INPUT_DIR = "data/yokatlas_html"

def parse_html_file(filepath):
    """
    YÖK Atlas HTML dosyasını parse eder.
    Genelde tablo ID'si 'mydata' olur.
    """
    print(f"İşleniyor: {filepath}")
    
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content, "lxml")
    
    # Tabloyu bul
    table = soup.find("table", {"id": "mydata"})
    if not table:
        print(f"UYARI: '{filepath}' içinde tablo bulunamadı. Lütfen sayfayı doğru kaydettiğinizden emin olun.")
        return []
        
    data = []
    
    # Satırları gez (tbody varsa oradan, yoksa direkt tr'lerden)
    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")
    
    for row in rows:
        cols = row.find_all("td")
        if not cols or len(cols) < 8:
            continue
            
        try:
            # Sütun İndeksleri (Tahmini - YÖK Atlas Standardı)
            # 0: Kod, 1: Üni Adı, 2: Fakülte, 3: Bölüm, 4: Puan Türü, 5: Kont., 6: Yer., 7: Taban Puan, 8: Başarı Sırası
            # Ancak bazen farklı olabilir. Metin bazlı analiz daha güvenli.
            
            # Üniversite ve Şehir ayıklama
            uni_cell = cols[1].get_text(strip=True)
            sehir = ""
            if "(" in uni_cell and ")" in uni_cell:
                parts = uni_cell.rsplit("(", 1)
                uni_adi = parts[0].strip()
                sehir = parts[1].replace(")", "").strip()
            else:
                uni_adi = uni_cell
            
            bolum_adi = cols[3].get_text(strip=True)
            puan_turu = cols[4].get_text(strip=True)
            
            # Kontenjan
            kont_text = cols[5].get_text(strip=True)
            kontenjan = int(kont_text.split("+")[0]) if "+" in kont_text else int(kont_text) if kont_text.isdigit() else 0
            
            # Taban Puan
            puan_text = cols[7].get_text(strip=True).replace(",", ".")
            taban_puan = float(puan_text) if puan_text != "---" and puan_text != "Dolmadı" else 0.0
            
            # Sıralama
            sira_text = cols[8].get_text(strip=True).replace(".", "")
            if sira_text.isdigit():
                 siralama = int(sira_text)
            else:
                 siralama = 9999999  # Dolmadı veya veri yok
                 
            # Ekle
            item = {
                "universite": uni_adi,
                "sehir": sehir,
                "bolum": bolum_adi,
                "puan_turu": puan_turu,
                "kontenjan": kontenjan,
                "taban_puan": taban_puan,
                "siralama": siralama,
                "tur": "Devlet" if "Vakıf" not in uni_adi and "Kıbrıs" not in uni_adi else "Vakıf" # Basit varsayım
            }
            data.append(item)
            
        except Exception as e:
            print(f"Satır hatası: {e}")
            continue
            
    return data

def main():
    if not os.path.exists(INPUT_DIR):
        print(f"Klasör bulunamadı: {INPUT_DIR}")
        return

    all_programs = []
    files = glob.glob(os.path.join(INPUT_DIR, "*.html"))
    files.extend(glob.glob(os.path.join(INPUT_DIR, "*.htm")))
    
    if not files:
        print("Klasörde HTML dosyası bulunamadı!")
        return

    print(f"{len(files)} dosya bulundu.")
    
    for f in files:
        programs = parse_html_file(f)
        all_programs.extend(programs)
        
    print(f"Toplam {len(all_programs)} program verisi işlendi.")
    
    # Kaydet
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_programs, f, ensure_ascii=False, indent=2)
        
    print(f"Veriler '{OUTPUT_JSON}' dosyasına başarıyla kaydedildi.")

if __name__ == "__main__":
    main()
