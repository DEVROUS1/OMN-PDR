
import requests
from bs4 import BeautifulSoup
import re
import json
import sys

# Placeholder URLs - to be updated
TYT_URL = "https://www.kitapsec.com/blog/link-236.html"
AYT_URL = "https://www.kitapsec.com/blog/link-235.html"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def clean_text(text):
    return text.strip().replace('\xa0', ' ').replace('’', "'").replace('`', "'")

def parse_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find tables
    tables = soup.find_all('table')
    if not tables:
        print("No tables found!")
        return {}

    # This part is generic and needs to be adapted to the specific table structure of the target page
    # usually the first row is headers (Years)
    # columns[0] is Topic, columns[1:] are counts per year
    
    all_tables_data = {}
    
    for table in tables:
        # Try to find the preceding heading (h2, h3, strong, etc.) to identify the subject
        # This is heuristics-based. 
        # For now, let's just collect all tables that look like data tables.
        
        rows = table.find_all('tr')
        if not rows:
            continue
            
        # Find the header row (containing years)
        header_row_index = -1
        years = []
        
        # Check first 5 rows for years
        for i in range(min(5, len(rows))):
            cells = rows[i].find_all(['th', 'td'])
            current_headers = [clean_text(cell.get_text()) for cell in cells]
            
            current_years = []
            for h in current_headers:
                if re.match(r'202[0-9]', h):
                    current_years.append(h)
            
            if len(current_years) >= 3: # At least 3 years to be valid
                years = current_years
                header_row_index = i
                break
        
        if header_row_index == -1:
            # print(f"Skipping table with headers: {[clean_text(c.get_text()) for c in rows[0].find_all(['th', 'td'])]}")
            continue

        # print(f"Found table with years: {years}")
        
        data = {}
        # Iterate over data rows starting AFTER the header row
        for row in rows[header_row_index+1:]:
            cells = row.find_all('td')
            if not cells:
                continue
            
            # First cell is usually the topic
            topic = clean_text(cells[0].get_text())
            
            # Skip rows that are likely headers repeated or totals
            if "Soru Sayısı" in topic or "KONULAR" in topic.upper():
                 continue

            counts = []
            for cell in cells[1:]:
                val = clean_text(cell.get_text())
                # Handle empty or non-numeric
                if val == '-' or val == '' or val == '?':
                    counts.append(0)
                else:
                    try:
                        counts.append(int(val))
                    except:
                        counts.append(0) 
            
            # Ensure we match the number of years found
            # Sometimes colspan makes this tricky, but assume simple structure for now
            if len(counts) >= len(years):
                data[topic] = counts[:len(years)]
        
        # We need a key for this table. 
        # Attempt to find a subject name from the topics
        subject_name = "Bilinmeyen Ders"
        keys = list(data.keys())
        all_topics_str = " ".join(keys).lower()
        
        if keys:
            # Order matters! Specific subjects first.
            
            # Fen Bilimleri (Strict Keywords)
            if any(k in all_topics_str for k in ["fizik bilimine giriş", "optik", "kaldırma kuvveti", "dinamik", "manyetizma", "atışlar", "itme ve momentum", "dairesel hareket", "modern fizik", "newton", "kepler", "fotoelektrik", "bağıl hareket"]):
                subject_name = "Fizik"
            elif any(k in all_topics_str for k in ["kimya bilimi", "periyodik sistem", "gazlar", "sıvı çözeltiler", "kimyasal türler", "elektrokimya", "organik kimya", "hidrokarbonlar", "tepkimelerde hız", "tepkimelerde denge", "kimyasal hesaplamalar"]): 
                subject_name = "Kimya"
            elif any(k in all_topics_str for k in ["sinir sistemi", "endokrin", "duyu organları", "solunum sistemi", "dolaşım", "boşaltım", "üreme", "komünite", "fotosentez", "kemosentez", "protein sentezi", "kalıtım", "hücre bölünmeleri"]): 
                subject_name = "Biyoloji"
                
            # Matematik / Geometri
            elif any(k in all_topics_str for k in ["türev", "integral", "logaritma", "trigonometri", "diziler", "polinomlar", "fonksiyonlar", "parabol", "ikinci dereceden", "karmaşık sayılar", "eşitsizlikler"]): 
                subject_name = "Matematik" # AYT Mat
            elif any(k in all_topics_str for k in ["problemler", "sayı basamakları", "rasyonel sayılar", "üslü sayılar", "köklü sayılar", "mutlak değer", "çarpanlara ayırma", "oran orantı", "ebob"]):
                subject_name = "Temel Matematik" # TYT Mat
            elif any(k in all_topics_str for k in ["üçgen", "dörtgen", "çember", "katı cisimler", "analitik geometri", "doğruda açı", "yamuk", "eşkenar", "prizma", "piramit"]):
                subject_name = "Geometri"
            
            # Coğrafya
            elif any(k in all_topics_str for k in ["coğrafi", "harita", "iklim", "dünya'nın şekli", "yerleşme", "nüfus", "yer şekilleri", "bölgeler", "doğal afetler"]): 
                subject_name = "Coğrafya"
                
            # Edebiyat / Türkçe
            elif any(k in all_topics_str for k in ["tanzimat", "servet-i fünun", "divan edebiyatı", "halk edebiyatı", "şiir bilgisi", "edebi akımlar", "cumhuriyet dönemi"]): 
                subject_name = "Edebiyat"
            elif any(k in all_topics_str for k in ["ses bilgisi", "yazım kuralları", "noktalama", "paragraf", "cümlede anlam", "sözcükte anlam", "anlatım bozukluğu", "dil bilgisi", "fiiller", "sözcük türleri"]): 
                subject_name = "Türkçe"
                
            # Sosyal Bilimler
            elif any(k in all_topics_str for k in ["felsefe", "mantık", "klasik mantık", "psikoloji", "sosyoloji"]) and "integral" not in all_topics_str: 
                subject_name = "Felsefe"
            elif any(k in all_topics_str for k in ["allah", "ibadet", "hz. muhammed", "vahiy", "kuran", "mezhep", "din kültürü", "islam ve bilim"]): 
                subject_name = "Din Kültürü"
            elif any(k in all_topics_str for k in ["tarih ve zaman", "ilk çağ", "osmanlı", "inkılap", "beylik", "türk dünyası", "milli mücadele", "islam tarihi"]): 
                subject_name = "Tarih"
        
        # Determine if it's TYT or AYT based on content if possible, but usually rely on the page URL context
        # For now, just store with the detected name.
        
        if subject_name != "Bilinmeyen Ders":
             print(f"DEBUG: Classified as '{subject_name}' based on topics: {all_topics_str[:50]}...")

        # If we have duplicate subject names (e.g. multiple tables for same subject?), append index
        original_name = subject_name
        counter = 1
        while subject_name in all_tables_data:
            counter += 1
            subject_name = f"{original_name} ({counter})"
            
        all_tables_data[subject_name] = {
            "years": years,
            "data": data
        }
        
    return all_tables_data

def scrape_url(url):
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        response.raise_for_status()
        return parse_table(response.content)
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to scrape")
    args = parser.parse_args()
    
    target_url = args.url if args.url else TYT_URL
    
    if not target_url:
        print("Please provide a URL using --url")
        sys.exit(1)
        
    requests.packages.urllib3.disable_warnings() 
    data = scrape_url(target_url)
    if data:
        print(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print("Failed to extract data.")
