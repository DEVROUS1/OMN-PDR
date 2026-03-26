import socket
import qrcode
import sys

def get_local_ip():
    try:
        # Dummy connection to determine preferred interface
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def print_qr(url):
    qr = qrcode.QRCode(version=1, box_size=1, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)

if __name__ == "__main__":
    ip = get_local_ip()
    port = "8501"
    url = f"http://{ip}:{port}"
    
    print("\n" + "="*50)
    print("MOBIL ERISIM (TELEFON/TABLET)")
    print("="*50)
    print(f"Bilgisayariniz ve telefonunuz ayni Wi-Fi aginda olmalidir.")
    print(f"Telefonunuzun tarayicisina su adresi yazin:")
    print(f"\n   >>>  {url}  <<<\n")
    print("Veya mumkunse asagidaki QR kodu okutmayi deneyin (Terminal destegine bagli):")
    try:
        print_qr(url)
    except:
        pass
    print("="*50 + "\n")
