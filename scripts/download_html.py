
import requests

url = "https://yokatlas.yok.gov.tr/tercih-sihirbazi-t4.php?p=say"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://yokatlas.yok.gov.tr/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
}

try:
    print(f"Downloading {url}...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    with open("yokatlas_sample.html", "w", encoding="utf-8") as f:
        f.write(response.text)
    
    print("Download complete. Saved to 'yokatlas_sample.html'.")
    print(f"Content length: {len(response.text)} bytes")
    
except Exception as e:
    print(f"Error: {e}")
