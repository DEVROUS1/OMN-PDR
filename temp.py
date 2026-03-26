import urllib.request
import re
import json

try:
    req = urllib.request.Request(
        'https://vepuan.com/yks-puan-hesaplama/',
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    
    scripts = re.findall(r'<script.*src=["\']([^"\']+)["\']', html)
    print("Found scripts:", scripts)
    for s in scripts:
        if 'puan' in s.lower() or 'hesapla' in s.lower() or 'assets' in s.lower():
            if not s.startswith('http'):
                url = 'https://vepuan.com' + s
            else:
                url = s
            print(f"Downloading {url}...")
            js_req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            js = urllib.request.urlopen(js_req).read().decode('utf-8')
            with open(s.split('/')[-1].split('?')[0], 'w', encoding='utf-8') as f:
                f.write(js)
except Exception as e:
    print(e)
