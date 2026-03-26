import sys
from pyngrok import ngrok, conf

def set_token():
    token = "39t4UbMXBHCF3Ma1a8jhPe2Uv54_3ZnwtvYXLjqJqVnjNrNeN"
    print(f"Token ayarlaniyor: {token[:5]}...")
    
    try:
        ngrok.set_auth_token(token)
        print("BASARILI: Ngrok token kaydedildi!")
    except Exception as e:
        print(f"HATA: Token ayarlanamadi: {e}")

if __name__ == "__main__":
    set_token()
