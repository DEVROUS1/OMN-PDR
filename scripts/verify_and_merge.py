
import json
import sys
import os

# Add scripts dir to path to import scraper
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.kitapsec_scraper import scrape_url, TYT_URL, AYT_URL

# Target keys in models/soru_dagilimi.py
TYT_KEYS = ["Türkçe", "Temel Matematik", "Fizik", "Kimya", "Biyoloji", "Tarih", "Coğrafya", "Felsefe", "Din Kültürü"]
AYT_KEYS = ["Matematik", "Fizik", "Kimya", "Biyoloji", "Edebiyat"]

def merge_data():
    print("Scraping TYT...")
    tyt_data = scrape_url(TYT_URL)
    print("Scraping AYT...")
    ayt_data = scrape_url(AYT_URL)
    
    if not tyt_data:
        print("CRITICAL: Failed to scrape TYT data")
        return
    if not ayt_data:
        print("CRITICAL: Failed to scrape AYT data")
        return

    # Prepare new data structure
    new_tyt = {}
    new_ayt = {}
    
    print("\n--- TYT MAPPING ANALYSIS ---")
    found_tyt_keys = []
    for key, val in tyt_data.items():
        # Clean key names (remove (1), (2) suffixes)
        clean_key = key.split('(')[0].strip()
        print(f"Scraped Key: '{key}' -> Clean: '{clean_key}' - Data Count: {len(val['data'])}")
        
        if clean_key in TYT_KEYS:
            # Check if likely valid data
            if len(val['data']) > 0:
                new_tyt[clean_key] = val['data']
                found_tyt_keys.append(clean_key)
        
        # Special handling for "Coğrafya" which might be named differently
        if clean_key == "Felsefe" and "Felsefe" in TYT_KEYS:
             new_tyt["Felsefe"] = val['data']
             found_tyt_keys.append("Felsefe")
             
        if "Bilinmeyen" in key:
            topics = list(val['data'].keys())[:5]
            print(f"!!! UNKNOWN CONTENT ({key}): {topics}")

    print(f"Missing TYT Keys: {set(TYT_KEYS) - set(found_tyt_keys)}")

    print("\n--- AYT MAPPING ANALYSIS ---")
    found_ayt_keys = []
    # AYT subjects might be in the AYT page OR TYT page (sometimes they are mixed or scraped incorrectly)
    # But checking AYT data specifically
    for key, val in ayt_data.items():
        clean_key = key.split('(')[0].strip()
        print(f"Scraped Key: '{key}' -> Clean: '{clean_key}' - Data Count: {len(val['data'])}")
        
        if clean_key in AYT_KEYS:
             if len(val['data']) > 0:
                new_ayt[clean_key] = val['data']
                found_ayt_keys.append(clean_key)
        
        if clean_key == "Türkçe":
             print(f"!!! SUSPICIOUS AYT TÜRKÇE TOPICS: {list(val['data'].keys())[:5]}")
    
    print(f"Missing AYT Keys: {set(AYT_KEYS) - set(found_ayt_keys)}")

    # Check validity
    if len(found_tyt_keys) < len(TYT_KEYS) * 0.5: # At least 50%
        print("WARNING: Low match rate for TYT.")
    
    if len(found_ayt_keys) < len(AYT_KEYS) * 0.5:
        print("WARNING: Low match rate for AYT.")

    return new_tyt, new_ayt

if __name__ == "__main__":
    merge_data()
