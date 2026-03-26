import os
import shutil
import sys
from pyngrok import ngrok, conf, installer

def fix_ngrok():
    print("="*50)
    print("NGROK ONARIM ARACI")
    print("="*50)

    # 1. Kill existing processes
    print("[1/4] Eski tüneller kapatılıyor...")
    try:
        ngrok.kill()
    except:
        pass
    
    # 2. Clear config
    print("[2/4] Yapılandırma sıfırlanıyor...")
    config_path = conf.get_default().config_path
    if config_path and os.path.exists(config_path):
        try:
            os.remove(config_path)
            print("   - Eski ayar dosyası silindi.")
        except Exception as e:
            print(f"   - Uyarı: Dosya silinemedi ({e})")
            
    # 3. Set Token
    print("[3/4] Token yeniden tanımlanıyor...")
    token = "39t4UbMXBHCF3Ma1a8jhPe2Uv54_3ZnwtvYXLjqJqVnjNrNeN"
    try:
        ngrok.set_auth_token(token)
        print("   - Token başarıyla kaydedildi.")
    except Exception as e:
        print(f"   - HATA: Token kaydedilemedi ({e})")

    # 4. Test connection
    print("[4/4] Bağlantı testi yapılıyor...")
    try:
        # Force a new config path to avoid permissions issues if any
        conf.get_default().monitor_thread = False
        
        url = ngrok.connect(8501, "http").public_url
        print(f"\n[BASARILI] Tünel açıldı: {url}")
        print("Sorun çözüldü! Lütfen bu pencereyi kapatıp 'baslat.bat'ı çalıştırın.")
    except Exception as e:
        print(f"\n[HATA] Tünel hala açılamıyor: {e}")
        print("Lütfen internet bağlantınızı kontrol edin veya güvenlik duvarını kapatıp deneyin.")

    input("\nÇıkış için Enter'a basın...")

if __name__ == "__main__":
    fix_ngrok()
