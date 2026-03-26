import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://www.osym.gov.tr/TR,29486/2025-yks-yerlestirme-sonuclarina-iliskin-sayisal-bilgiler.html"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def extract_links():
    try:
        print(f"Fetching: {URL}")
        response = requests.get(URL, headers=HEADERS, verify=False, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        
        links = soup.find_all("a")
        print(f"Found {len(links)} links.")
        for a in links:
            href = a.get("href")
            text = a.text.strip()
            if href and ("xlsx" in href.lower() or "tablo" in text.lower() or "tablo" in href.lower()):
                print(f"LINK: {text} -> {href}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    extract_links()
