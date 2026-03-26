import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

URL = "https://kazanabilirsin.com/universitelerin-guncel-taban-puanlari-ve-basari-siralamalari-yokatlas-osym/"
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
        
        # Check for list of links to 4-year departments
        links = soup.find_all("a")
        
        # Filter for likely department links
        dept_links = []
        for a in links:
            href = str(a.get("href", ""))
            text = a.text.strip()
            # Keywords often used in URLs for departments
            if "taban-puanlari" in href and "yillik" not in href: # Try to avoid general yearly lists if possible, or maybe catch them
                 dept_links.append({"text": text, "href": href})
        
        print(f"Found {len(dept_links)} potential department links.")
        for l in dept_links[:10]:
            print(f"- {l['text']}: {l['href']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect()
