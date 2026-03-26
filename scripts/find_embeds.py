import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://kazanabilirsin.com/bilgisayar-muhendisligi-2021-taban-puanlari-ve-basari-siralamasi/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def find_embedded_data():
    try:
        response = requests.get(URL, headers=HEADERS, verify=False, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Look for iframes
        iframes = soup.find_all("iframe")
        print(f"Found {len(iframes)} iframes.")
        for i in iframes:
            print(f"Iframe Source: {i.get('src')}")
            
        # Look for script tags that might contain JSON
        scripts = soup.find_all("script")
        print(f"Found {len(scripts)} scripts.")
        
        # Look for the "aşağıdaki tablodan" text parent
        target = soup.find(text=lambda t: "aşağıdaki tablodan" in t)
        if target:
            parent = target.parent
            print("Found target text parent tag:", parent.name)
            # Print next few siblings
            for sibling in parent.find_next_siblings()[:5]:
                print(f"Sibling: {sibling.name}, Class: {sibling.get('class')}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_embedded_data()
