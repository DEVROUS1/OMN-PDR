
import json
import sys
import os

# Add scripts dir to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.kitapsec_scraper import scrape_url

URLS_TYT = [
    "https://www.kitapsec.com/blog/link-236.html", # Hub
    "https://www.kitapsec.com/blog/link-114.html", # TYT Matematik
    "https://www.kitapsec.com/blog/link-15.html",  # TYT Geometri
    "https://www.kitapsec.com/blog/link-17.html",  # TYT Fizik
]

URLS_AYT = [
    "https://www.kitapsec.com/blog/link-235.html", # Hub
    "https://www.kitapsec.com/blog/link-134.html", # AYT Matematik
    "https://www.kitapsec.com/blog/link-135.html", # AYT Geometri
    "https://www.kitapsec.com/blog/link-136.html", # AYT Fizik
]

# Mapping from Scraper Key to Model Key
TYT_MAPPING = {
    "Türkçe": "Türkçe",
    "Temel Matematik": "Temel Matematik",
    "Fizik": "Fizik",
    "Kimya": "Kimya",
    "Biyoloji": "Biyoloji",
    "Tarih": "Tarih",
    "Coğrafya": "Coğrafya",
    "Felsefe": "Felsefe", # TYT uses Felsefe, check if verified
    "Din Kültürü": "Din Kültürü",
    "Geometri": "Geometri_TEMP" # Will be merged
}

AYT_MAPPING = {
    "Matematik": "Matematik",
    "Fizik": "Fizik",
    "Kimya": "Kimya",
    "Biyoloji": "Biyoloji",
    "Edebiyat": "Edebiyat",
    "Geometri": "Geometri_TEMP" # Will be merged
    # Note: Tarih, Coğrafya, Felsefe, Din are NOT in current AYT model
}

def clean_key_name(k):
    return k.split('(')[0].strip()

def merge_datasets(urls, mapping):
    merged = {}
    geometri_data = {}
    
    for url in urls:
        print(f"Scraping {url}...")
        data = scrape_url(url)
        if not data: continue
        
        for k, v in data.items():
            clean_k = clean_key_name(k)
            
            # Map clean key to model key
            if clean_k in mapping:
                model_key = mapping[clean_k]
                
                if model_key == "Geometri_TEMP":
                    # Collect Geometri separately to merge later
                    if len(v['data']) > 0:
                        geometri_data.update(v['data'])
                else:
                    if model_key not in merged:
                        merged[model_key] = {}
                    
                    # Merge data (topics)
                    # If duplicate topics, overwrite (usually specific page > hub page)
                    if len(v['data']) > 0:
                         merged[model_key].update(v['data'])
            
            # Special handling for Felsefe in TYT which might be named differently?
            # Existing code for verify_and_merge handled this via checking 'clean_key'
            
    return merged, geometri_data

def update_model_file():
    print("--- DOING TYT ---")
    tyt_data, tyt_geo = merge_datasets(URLS_TYT, TYT_MAPPING)
    
    # Merge Geometri into Temel Matematik
    if "Temel Matematik" in tyt_data and tyt_geo:
        # Remove aggregate "Geometri" if exists
        if "Geometri" in tyt_data["Temel Matematik"]:
             del tyt_data["Temel Matematik"]["Geometri"]
        
        # Add detailed geometry topics
        tyt_data["Temel Matematik"].update(tyt_geo)
        print(f"Merged {len(tyt_geo)} Geometry topics into TYT Temel Matematik")
        
    print("--- DOING AYT ---")
    ayt_data, ayt_geo = merge_datasets(URLS_AYT, AYT_MAPPING)
    
    # Merge Geometri into Matematik
    if "Matematik" in ayt_data and ayt_geo:
        if "Geometri" in ayt_data["Matematik"]:
             del ayt_data["Matematik"]["Geometri"]
        
        ayt_data["Matematik"].update(ayt_geo)
        print(f"Merged {len(ayt_geo)} Geometry topics into AYT Matematik")

    # Generate Python Content
    content = '"""\nOmniPDR – models/soru_dagilimi.py\n===================================\nTYT ve AYT derslerine ait son 5 yılın (2021-2025) konu bazlı soru dağılımı verileri.\n2025 verileri, MEB müfredatı ve ÖSYM kazanımlarına dayalı projeksiyonlardır.\n"""\n\n'
    content += 'from typing import Dict, List\n\n'
    content += '# Yıllar sütunu: 2025, 2024, 2023, 2022, 2021, 2020\n'
    content += 'YILLAR = ["2025", "2024", "2023", "2022", "2021", "2020"]\n\n'
    
    content += 'TYT_DAGILIM: Dict[str, Dict[str, List[int]]] = ' + json.dumps(tyt_data, ensure_ascii=False, indent=4) + '\n\n'
    content += 'AYT_DAGILIM: Dict[str, Dict[str, List[int]]] = ' + json.dumps(ayt_data, ensure_ascii=False, indent=4) + '\n'
    
    # Write to file
    path = os.path.join(os.path.dirname(__file__), '..', 'models', 'soru_dagilimi.py')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Successfully updated {path}")

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    update_model_file()
