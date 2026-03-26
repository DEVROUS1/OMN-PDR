@echo off
:: Eğer kullanıcı Yönetici olarak çalıştırdıysa CWD System32 olabilir.
:: Scriptin bulunduğu dizine geçiş yapıyoruz.
cd /d "%~dp0"

chcp 65001 > nul
title OmniPDR Baslatiliyor...
echo.
echo ===================================================
echo   OmniPDR - PDR Ogrenci Takip Platformu
echo ===================================================
echo.
echo [BILGI] Uygulama baslatiliyor, lutfen bekleyin...
echo [BILGI] Verileriniz otomatik olarak bilgisayariniza kaydedilmektedir.
echo [BILGI] Internet baglantisi olmasa da calisabilirsiniz.
echo.

:: Sanal ortamdaki python'u doğrudan kullan
set PYTHON_EXE="%~dp0.venv\Scripts\python.exe"
set STREAMLIT_EXE="%~dp0.venv\Scripts\streamlit.exe"

:: IP Adresini Göster (Mobil Erişim İçin)
%PYTHON_EXE% scripts/show_ip.py
echo.

:: Streamlit'i başlat
start "OmniPDR Server" /min cmd /c "%PYTHON_EXE% -m streamlit run arayuz_app.py --server.headless true --server.port 8501 --server.address 0.0.0.0"

:: Sunucunun ayağa kalkması için biraz bekle
timeout /t 3 > nul

echo [BILGI] Arayuz yukleniyor...

:: Chrome varsa uygulama modunda aç (Adres çubuğu olmadan)
if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app=http://localhost:8501
) else if exist "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --app=http://localhost:8501
) else (
    :: Chrome yoksa varsayılan tarayıcıda aç
    start http://localhost:8501
)

echo.
echo [DURUM] Uygulama calisiyor!
echo [UYARI] Bu pencereyi kapatirsaniz uygulama durur.
echo [IPUCU] Uygulamayi tam ekran yapmak icin F11 tusuna basabilirsiniz.
echo.
echo [SECENEK] Uzaktan erisim (ngrok) baslatmak icin herhangi bir tusa basin...
pause > nul
start "OmniPDR Remote Tunnel" cmd /c "%PYTHON_EXE% scripts/remote_access.py"
