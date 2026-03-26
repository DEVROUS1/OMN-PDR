import requests
from bs4 import BeautifulSoup
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://kazanabilirsin.com/tum-muhendislik-bolumleri-taban-puanlari-basari-siralamalari/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def scrape_engineering():
    try:
        print(f"Scraping: {URL}")
        response = requests.get(URL, headers=HEADERS, verify=False, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Look for the table
        table = soup.find("table")
        if not table:
            print("No table found!")
            return
            
        rows = table.find_all("tr")
        print(f"Found {len(rows)} rows.")
        
        results = []
        # Column indices might vary, need to check headers
        headers = [th.text.strip().lower() for th in rows[0].find_all(["th", "td"])]
        print("Headers:", headers)
        
        # Mapping (heuristic)
        idx_uni = -1
        idx_dept = -1
        idx_puan = -1
        idx_sira = -1
        
        for i, h in enumerate(headers):
            if "üniversite" in h: idx_uni = i
            elif "bölüm" in h: idx_dept = i
            elif "puan" in h and "türü" not in h: idx_puan = i
            elif "sıra" in h: idx_sira = i
            
        for row in rows[1:11]: # Just first 10 for prototype
            cols = row.find_all("td")
            if len(cols) > max(idx_uni, idx_dept, idx_puan, idx_sira):
                data = {
                    "universite": cols[idx_uni].text.strip(),
                    "bolum": cols[idx_dept].text.strip(),
                    "puan": cols[idx_puan].text.strip(),
                    "siralama": cols[idx_sira].text.strip()
                }
                results.append(data)
                
        print("\nPrototype Results (First 10):")
        for r in results:
            print(r)
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_engineering()
