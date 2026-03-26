import requests
import pandas as pd
import json
import io
import os

URL = "https://raw.githubusercontent.com/MorphaxTheDeveloper/yokatlas-dataset-2025/main/tum_bolumler.csv"
OUTPUT_JSON = os.path.join("data", "yokatlas_full.json")

def fetch_and_process():
    print(f"Downloading data from {URL}...")
    try:
        response = requests.get(URL)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to download data: {e}")
        return

    # Load CSV
    df = pd.read_csv(io.StringIO(response.text))
    print(f"Loaded {len(df)} rows from CSV.")
    
    # Identify latest year columns
    year_cols = [col for col in df.columns if col.startswith("puan")]
    years = [int(col.replace("puan", "")) for col in year_cols if col.replace("puan", "").isdigit()]
    
    if not years:
        print("Could not find year columns!")
        return
        
    latest_year = max(years)
    print(f"Latest year found in dataset: {latest_year}")
    
    # Map columns
    # Core mappings
    # universite -> Universite
    # isim -> Bolum
    # il -> Sehir
    # tur -> Puan Turu (Need normalization)
    # unitur -> Tur (Devlet/Vakif)
    # puan{YEAR} -> Taban Puan
    # sira{YEAR} -> Siralama
    # kontenjan{YEAR} -> Kontenjan
    # maxpuan{YEAR} -> Tavan Puan
    
    puan_col = f"puan{latest_year}"
    sira_col = f"sira{latest_year}"
    kont_col = f"kontenjan{latest_year}"
    maxpuan_col = f"maxpuan{latest_year}"
    
    records = []
    
    for _, row in df.iterrows():
        # Normalization
        pt = row.get("tur", "")
        if pt == "SAYISAL": pt = "SAY"
        elif pt == "EŞİT AĞIRLIK": pt = "EA"
        elif pt == "SÖZEL": pt = "SOZ"
        elif pt == "DİL": pt = "YDT"
        
        # Skip if puan_turu is not valid for our app (e.g. TYT might be separate or handled differently)
        # Actually app supports TYT too.
        
        # Unitur title case
        u_tur = str(row.get("unitur", "")).title()
        if "Devlet" in u_tur: u_tur = "Devlet"
        elif "Vakıf" in u_tur or "Vakif" in u_tur: u_tur = "Vakıf"
        elif "Kıbrıs" in u_tur: u_tur = "Kıbrıs"
        elif "Yabancı" in u_tur: u_tur = "Yabancı"
        
        # Extract metrics
        try:
            taban_puan = float(str(row.get(puan_col, 0)).replace(",", "."))
        except:
            taban_puan = 0.0
            
        try:
            tavan_puan = float(str(row.get(maxpuan_col, 0)).replace(",", "."))
        except:
            tavan_puan = 0.0
            
        try:
            siralama = int(float(str(row.get(sira_col, 0)).replace(",", ".")))
        except:
            siralama = 9999999
            
        try:
            kontenjan = int(float(str(row.get(kont_col, 0)).replace(",", ".")))
        except:
            kontenjan = 0
            
        record = {
            "universite": row.get("universite", "Bilinmiyor"),
            "bolum": row.get("isim", "Bilinmiyor"),
            "sehir": row.get("il", "Bilinmiyor"),
            "puan_turu": pt,
            "taban_puan": taban_puan,
            "tavan_puan": tavan_puan,
            "siralama": siralama,
            "kontenjan": kontenjan,
            "tur": u_tur
        }
        
        records.append(record)
        
    print(f"Processed {len(records)} records.")
    
    # Ensure data directory
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
        
    print(f"Saved to {OUTPUT_JSON}")

if __name__ == "__main__":
    fetch_and_process()
