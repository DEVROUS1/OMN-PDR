
import requests
import time

def check_urls():
    base_pattern = "https://www.kitapsec.com/blog/2026-tyt-konulari-ve-soru-dagilimi-{}.html"
    base_pattern_ayt = "https://www.kitapsec.com/blog/2026-ayt-konulari-ve-soru-dagilimi-{}.html"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Scan IDs to find titles
    print("Scanning IDs 210-240...")
    requests.packages.urllib3.disable_warnings()
    for i in range(210, 241):
        url = f"https://www.kitapsec.com/blog/link-{i}.html"
        try:
            r = requests.get(url, headers=headers, timeout=5, verify=False)
            if r.status_code == 200:
                # Extract title with regex to avoid bs4 if needed, or use bs4 if robust
                title_match = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
                if title_match:
                    title = title_match.group(1).strip()
                    # Print ALL titles to see what's there
                    print(f"ID {i}: {title}")
                    if "TYT" in title and "Soru" in title:
                        print(f"!!! POSSIBLE TYT MATCH: {url}")
                    if "AYT" in title and "Soru" in title:
                         print(f"!!! POSSIBLE AYT MATCH: {url}")
        except Exception as e:
            # print(f"Error on {i}: {e}")
            pass
            
        time.sleep(0.5)

if __name__ == "__main__":
    check_urls()
