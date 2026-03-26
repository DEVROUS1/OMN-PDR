import requests
from bs4 import BeautifulSoup

URL = "https://www.kariyer.net/universite-taban-puanlari"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

try:
    response = requests.get(URL, headers=HEADERS)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        print("\nPage Title:", soup.title.string.strip())
        
        # Try to find a data table or list
        # Look for table rows or list items
        print("\n--- HTML Snippet ---")
        print(soup.prettify()[:1000])
        
        # Specific check for potential data containers
        tables = soup.find_all("table")
        print(f"\nFound {len(tables)} tables.")
        
    else:
        print("Failed to retrieve content.")

except Exception as e:
    print(f"Error: {e}")
