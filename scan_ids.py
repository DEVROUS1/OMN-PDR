
import requests
import re
import time
import concurrent.futures

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def check_id(i):
    url = f"https://www.kitapsec.com/blog/link-{i}.html"
    try:
        r = requests.get(url, headers=HEADERS, timeout=5, verify=False)
        if r.status_code == 200:
            title_match = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE)
            if title_match:
                title = title_match.group(1).strip()
                if "Soru" in title and ("TYT" in title or "AYT" in title or "YKS" in title):
                    return f"MATCH ID {i}: {title} | {url}"
                # elif "Konu" in title:
                #    return f"Topic ID {i}: {title}"
    except:
        pass
    return None

def scan_range():
    requests.packages.urllib3.disable_warnings()
    print("Scanning IDs 150-350...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(check_id, i) for i in range(150, 350)]
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                print(result)

if __name__ == "__main__":
    scan_range()
