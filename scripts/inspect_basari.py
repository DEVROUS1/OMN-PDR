import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://www.basarisiralamalari.com/category/basari-siralamalari/4-yillik-bolumler-taban-puanlari/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def inspect():
    try:
        response = requests.get(URL, headers=HEADERS, verify=False, timeout=10)
        print(f"Status: {response.status_code}")
        
        soup = BeautifulSoup(response.content, "html.parser")
        print("Title:", soup.title.string.strip())
        
        # Check for tables
        tables = soup.find_all("table")
        print(f"Found {len(tables)} tables.")
        
        # Look for article headings or post titles
        # Usually inside <h2> or <h3> tags in WordPress sites
        headings = soup.find_all(["h2", "h3"])
        print(f"Found {len(headings)} headings.")
        
        post_links = []
        for h in headings:
            a = h.find("a")
            if a:
                post_links.append({"text": a.text.strip(), "href": a.get("href")})
        
        if not post_links:
            # Fallback: look for generic links that might be posts (long paths)
            all_links = soup.find_all("a")
            for a in all_links:
                href = str(a.get("href", ""))
                if "basarisiralamalari.com/" in href and "/category/" not in href and href.count("/") > 3:
                     # Avoid very short specific links
                     if len(href) > 40: 
                        post_links.append({"text": a.text.strip(), "href": href})

        print(f"Found {len(post_links)} potential post links.")
        for p in post_links[:10]:
            print(f"- {p['text']}: {p['href']}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
