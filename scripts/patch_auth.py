import sys
import os

filepath = r'c:\Users\BilnetPc\Desktop\OmniPDR\arayuz_app.py'
if not os.path.exists(filepath):
    print(f"File not found: {filepath}")
    sys.exit(1)

with open(filepath, 'rb') as f:
    content = f.read()

# 1. Replace st.set_page_config block with Auth block
start_marker = b'st.set_page_config('
end_marker = b')'

start_index = content.find(start_marker)
if start_index == -1:
    print("Could not find st.set_page_config")
else:
    end_index = content.find(end_marker, start_index)
    if end_index != -1:
        actual_end = end_index + 1
        if content[actual_end:actual_end+2] == b'\r\n':
            actual_end += 2
        elif content[actual_end:actual_end+1] == b'\n':
            actual_end += 1

        new_auth_block = b"""st.set_page_config(
    page_title="OmniPDR \xe2\x80\x93 \xc3\x96\xc4\x9frenci Takip Platformu",
    page_icon="\xf0\x9f\xa7\xa0",
    layout="wide",
    initial_sidebar_state="expanded",
)

# \xe2\x94\x80\xe2\x94\x80 Kimlik Do\xc4\x9frulama (Auth) \xe2\x94\x80\xe2\x94\x80
coach_user = os.getenv("COACH_USERNAME", "admin")
coach_hash = os.getenv("COACH_PASSWORD_HASH", "")

if not coach_hash:
    st.error("\xe2\x9a\xa0\xef\xb8\x8f Kritik Hata: .env dosyas\xc4\xb1nda COACH_PASSWORD_HASH eksik. Uygulama ba\xc5\x9flat\xc4\xb1lam\xc4\xb1yor.")
    st.info("L\xc3\xbctfen .env dosyas\xc4\xb1na COACH_PASSWORD_HASH de\xc4\x9fi\xc5\x9fkenini (bcrypt) ekleyin.")
    st.stop()

credentials = {
    "usernames": {
        coach_user: {
            "name": "E\xc4\x9fitim Ko\xc3\xa7u",
            "password": coach_hash
        }
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "omnipdr_session_cookie",
    "omnipdr_secret_key",
    cookie_expiry_days=30
)

# Login Formu (Ana Ekran)
name, authentication_status, username = authenticator.login("OmniPDR - Ko\xc3\xa7 Giri\xc5\x9fi", "main")

if authentication_status is False:
    st.error("Kullan\xc4\xb1c\xc4\xb1 ad\xc4\xb1 veya \xc5\x9fifre hatal\xc4\xb1.")
    st.stop()
elif authentication_status is None:
    st.warning("L\xc3\xbctfen E\xc4\x9fitim Ko\xc3\xa7u hesab\xc4\xb1 ile giri\xc5\x9f yap\xc4\xb1n.")
    # API Anahtar\xc4\xb1 Kontrol\xc3\xbc (Giri\xc5\x9f yap\xc4\xb1lmasa da bilgilendirme)
    if not os.getenv("GROQ_API_KEY"):
        st.info("\xe2\x84\xb9\xef\xb8\x8f Yapay Zeka (Groq) anahtar\xc4\xb1 eksik. Sistem \xc3\xa7evrimd\xc4\xb1\xc5\x9f\xc4\xb1 modda \xc3\xa7al\xc4\xb1\xc5\x9facakt\xc4\xb1r.")
    st.stop()
"""
        if b'\r\n' in content: 
            new_auth_block = new_auth_block.replace(b'\n', b'\r\n')
        content = content[:start_index] + new_auth_block + content[actual_end:]

# 2. Add logout to sidebar
sidebar_marker = b'st.caption("v3.0.0 \xe2\x80\xa2 Ultra-Profesyonel")'
sidebar_index = content.find(sidebar_marker)
if sidebar_index == -1:
    print("Could not find sidebar caption marker")
else:
    insert_pos = sidebar_index + len(sidebar_marker)
    if content[insert_pos:insert_pos+2] == b'\r\n':
        insert_pos += 2
    elif content[insert_pos:insert_pos+1] == b'\n':
        insert_pos += 1
    
    logout_code = b'    st.markdown("---")\n    authenticator.logout("\xf0\x9f\x9a\xaa Sistemden G\xc3\xbcvenli \xc3\x87\xc4\xb1k\xc4\xb1\xc5\x9f", "sidebar")\n'
    if b'\r\n' in content:
        logout_code = logout_code.replace(b'\n', b'\r\n')
    
    content = content[:insert_pos] + logout_code + content[insert_pos:]

with open(filepath, 'wb') as f:
    f.write(content)

print("✅ Authentication and Logout successfully integrated via patch script.")
