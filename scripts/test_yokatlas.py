
try:
    from yokatlas import YokAtlas
    print("yokatlas kutuphanesi basariyla yuklendi.")
except ImportError:
    print("yokatlas kutuphanesi yuklenemedi!")
    exit(1)

def test_yokatlas():
    print("YOK Atlas API Testi Basliyor...")
    yok = YokAtlas()
    
    # Ornek: Lisans programlari
    print("Lisans programlari cekiliyor (ilk 5)...")
    try:
        programs = yok.programs(level="lisans")
        print(f"Toplam {len(programs)} program bulundu.")
        for p in programs[:1]:
            print(f"- {p}")
            # Anahtarları ve örnek değerleri görelim
            if hasattr(p, '__dict__'):
                print(p.__dict__)
            else:
                print(p)
    except Exception as e:
        print(f"HATA: {e}")

if __name__ == "__main__":
    test_yokatlas()
