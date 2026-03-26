import requests

SITES = [
    "https://www.basarisiralamalari.com/4-yillik-bolumlerin-taban-puanlari-ve-basari-siralamalari/",
    "https://kazanabilirsin.com/universite-taban-puanlari/"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def check_site(url):
    try:
        print(f"Checking {url}...")
        response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Accessible!")
            return True
        else:
            print("Failed.")
    except Exception as e:
        print(f"Error: {e}")
    return False

if __name__ == "__main__":
    for site in SITES:
        check_site(site)
        print("-" * 20)
