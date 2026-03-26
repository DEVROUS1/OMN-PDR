import requests

URL = "https://raw.githubusercontent.com/MorphaxTheDeveloper/yokatlas-dataset-2025/main/tum_bolumler.csv"

try:
    response = requests.get(URL, stream=True)
    response.raise_for_status()
    
    # Read first 4KB
    content = next(response.iter_content(chunk_size=4096)).decode('utf-8', errors='ignore')
    lines = content.splitlines()
    print("Headers:", lines[0])
    if len(lines) > 1:
        print("Row 1:", lines[1])
except Exception as e:
    print(f"Error: {e}")
