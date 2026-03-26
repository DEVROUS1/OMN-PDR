
import requests
from bs4 import BeautifulSoup
import re

def find_urls():
    base_url = "https://www.kitapsec.com/blog/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Try first 3 pages
    for page in range(1, 4):
        url = f"{base_url}?sayfa={page}" if page > 1 else base_url
        print(f"Scanning {url}...")
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Failed to fetch page {page}: {response.status_code}")
                continue
                
            soup = BeautifulSoup(response.content, 'html.parser')
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link['href']
                text = link.get_text().strip()
                
                # Check for TYT, AYT, YKS in text or href
                if any(x in text.upper() or x in href.upper() for x in ["TYT", "AYT", "YKS", "KONU"]):
                     # Refine to likely blog posts (usually contain 'konulari' or 'soru-dagilimi')
                    if "blog" in href or "soru" in href or "konu" in href.lower():
                        print(f"Found: {text}")
                        print(f"URL: {href}")
                        print("-" * 20)
        
        except Exception as e:
            print(f"Error on page {page}: {e}")
                


if __name__ == "__main__":
    find_urls()
