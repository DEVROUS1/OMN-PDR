import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Guessed patterns for 2025 YKS Excel files
PATTERNS = [
    "https://dokuman.osym.gov.tr/pdfdokuman/2025/YKS/yerlestirme/MinMaxPuanlar_Tablo4.xlsx",
    "https://dokuman.osym.gov.tr/pdfdokuman/2025/YKS/yerlestirme/MinMaxPuanlar_Tablo3.xlsx",
    "https://dokuman.osym.gov.tr/pdfdokuman/2025/YKS/tablo4.xlsx",
    "https://dokuman.osym.gov.tr/pdfdokuman/2025/YKS/sayisal_bilgiler/tablo4.xlsx",
    "https://dokuman.osym.gov.tr/pdfdokuman/2025/YKS/YKS_Sayisal_Bilgiler_2025_Tablo4.xlsx"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def verify_links():
    for url in PATTERNS:
        try:
            print(f"Checking: {url}")
            # Use head request to be efficient
            response = requests.head(url, headers=HEADERS, verify=False, timeout=5)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"!!! FOUND VALID LINK: {url}")
        except Exception as e:
            print(f"Error checking {url}: {e}")

if __name__ == "__main__":
    verify_links()
