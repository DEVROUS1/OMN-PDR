import sys
import os
import json
from dataclasses import asdict

# Add project root to sys.path to import from core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from core.yokatlas_verileri import BOLUM_VERILERI
except ImportError as e:
    print(f"Error importing core.yokatlas_verileri: {e}")
    sys.exit(1)

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'exported_universities.json')

def main():
    print("Exporting university data...")
    
    # Convert dataclass objects to dictionaries
    data = [asdict(bolum) for bolum in BOLUM_VERILERI]
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully exported {len(data)} records to {os.path.abspath(OUTPUT_FILE)}")

if __name__ == "__main__":
    main()
