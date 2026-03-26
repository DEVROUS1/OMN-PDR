import smtplib
import ssl
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = os.getenv("SMTP_PORT", "465")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def email_gonder(konu: str, icerik: str, alici: str):
    """
    Belirtilen alıcıya SMTP üzerinden e-posta gönderir.
    Hata durumunda exception fırlatmaz, loglama yapar.
    """
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD]):
        print("BİLDİRİM HATASI: SMTP ayarları .env dosyasında eksik.")
        return False

    try:
        mesaj = MIMEMultipart()
        # Header assignment using headers interface to avoid linter confusion
        mesaj.add_header("From", str(SMTP_USER))
        mesaj.add_header("To", alici)
        mesaj.add_header("Subject", konu)

        mesaj.attach(MIMEText(icerik, "plain", "utf-8"))

        context = ssl.create_default_context()
        host = str(SMTP_HOST)
        port = int(SMTP_PORT)
        user = str(SMTP_USER)
        pw = str(SMTP_PASSWORD)

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(user, pw)
            server.sendmail(user, alici, mesaj.as_string())
        
        print(f"BİLDİRİM: '{konu}' başlıklı e-posta {alici} adresine gönderildi.")
        return True
    except Exception as e:
        print(f"BİLDİRİM HATASI: E-posta gönderilemedi. Hata: {str(e)}")
        return False
