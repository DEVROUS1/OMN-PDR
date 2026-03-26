
import sys
import time
from pyngrok import ngrok, conf
import os

def start_ngrok():
    print("\n" + "="*50)
    print("UZAKTAN ERISIM (INTERNET UZERINDEN)")
    print("="*50)
    
    # Check for auth token in environment or config
    # If not present, we can try to start, but likely will fail or be limited
    # We will just try to connect
    
    try:
        # Close any existing tunnels
        ngrok.kill()
        
        # Connect to port 8501
        # If user has an authtoken, they should run: ngrok config add-authtoken <token>
        # But we will try anonymous first if possible (though ngrok usually requires it now)
        
        # Determine if we have a token
        config_path = conf.get_default().config_path
        if config_path and not os.path.exists(config_path):
             print("[BILGI] Ngrok yapılandırması bulunamadı.")
        
        # Try to connect with region fallback
        regions = ["eu", "us", "in", "sa", "ap", "au"]
        tunnel = None
        
        for region in regions:
            print(f"[BILGI] '{region}' bölgesi deneniyor...")
            try:
                conf.get_default().region = region
                tunnel = ngrok.connect(8501)
                print(f"[BASARILI] Bağlantı '{region}' üzerinden kuruldu!")
                break
            except Exception as e:
                print(f"   - Başarısız: {e}")
                time.sleep(1)
        
        if not tunnel:
            print("\n[KRITIK HATA] Hiçbir bölgeden bağlantı kurulamadı.")
            print("Görünüşe göre internet ağınız (MEB, Kurumsal veya Güvenlik Duvarı)")
            print("Ngrok tünel bağlantılarını engelliyor.")
            print("Mobil veriden (Hotspot) bağlanmayı deneyebilirsiniz.")
            raise Exception("Tüm bölgeler engellendi.")

        public_url = tunnel.public_url

        public_url = tunnel.public_url
        
        print(f"[BASARILI] Uygulamanız şu an internete açık!")
        print(f"Aşağıdaki adresi telefonunuza gönderin:")
        print(f"\n   >>>  {public_url}  <<<\n")
        print("(Bu pencere açık kaldığı sürece erişim devam eder)")
        print("="*50 + "\n")
        
        # Keep alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Tünel kapatılıyor...")
            ngrok.disconnect(public_url)
            ngrok.kill()

    except Exception as e:
        if "authtoken" in str(e).lower() or "authentication" in str(e).lower():
            print("\n[!] Ngrok AuthToken eksik veya hatalı.")
            token = input("Lütfen ngrok AuthToken'ınızı buraya yapıştırın: ").strip()
            if token:
                os.system(f"ngrok config add-authtoken {token}")
                print("[TAMAM] Token kaydedildi. Lütfen uygulamayı yeniden başlatın.")
            else:
                print("[İPTAL] Token girilmedi.")
        else:
            print(f"\n[HATA] Ngrok başlatılamadı: {e}")
        
        print("-" * 30)
        print("Yardım için: https://dashboard.ngrok.com")
        input("\nKapatmak için Enter'a basın...")

if __name__ == "__main__":
    start_ngrok()
