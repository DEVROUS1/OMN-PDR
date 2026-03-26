import urllib.request
import urllib.parse
import json

data_dict = {
    'postname': 'yks-hesapla',
    'isyerlesme': 0,
    'diplomapuani': 80.0,
    'tyt-t': 30, 'tyt-s': 15, 'tyt-m': 30, 'tyt-f': 15,
    'ayt-mat': 30, 'ayt-fizik': 10, 'ayt-kimya': 10, 'ayt-biyoloji': 10,
    'ayt-edebiyat': 0, 'ayt-tarih1': 0, 'ayt-cografya1': 0,
    'ayt-tarih2': 0, 'ayt-cografya2': 0, 'ayt-felsefe': 0, 'ayt-din': 0, 'ayt-dil': 0
}
data = urllib.parse.urlencode(data_dict).encode('utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://vepuan.com',
    'Referer': 'https://vepuan.com/yks-puan-hesaplama/'
}

req = urllib.request.Request('https://vepuan.com/hesapla.php', data=data, headers=headers)
try:
    resp = urllib.request.urlopen(req, timeout=3).read().decode('utf-8')
    print("Length:", len(resp))
    print("Content:", resp[:200])
except Exception as e:
    print("Error:", e)
