import requests
from bs4 import BeautifulSoup

# Web sayfasının URL'si
url = "https://canlitv.com/?sayfa=1"

# Sayfayı almak için GET isteği gönderiyoruz
response = requests.get(url)
if response.status_code == 200:
    print("Sayfa başarıyla yüklendi!")
else:
    print("Sayfa yüklenemedi!")
    exit()

# BeautifulSoup ile sayfayı parse ediyoruz
soup = BeautifulSoup(response.content, "html.parser")

# Kanal listesini bulalım (kanal-listesi içindeki a etiketleri)
kanal_listeleri = soup.find_all('a', {'title': True})

# Kanal adı, resim URL ve linki almak
kanal_adlari = []
kanal_resimleri = []
kanal_linkleri = []

for kanal in kanal_listeleri:
    # Kanal adını alalım
    kanal_ad_div = kanal.find('div', {'class': 'kanal_ad'})
    if kanal_ad_div:
        kanal_ad = kanal_ad_div.text.strip()
        kanal_adlari.append(kanal_ad)
    else:
        kanal_adlari.append('Kanal adı bulunamadı')

    # Kanal resminin URL'sini alalım
    kanal_resim_div = kanal.find('div', {'class': 'kanal_resim'})
    if kanal_resim_div:
        kanal_resim = kanal_resim_div.find('img')['src']
        kanal_resim_url = "https://canlitv.com" + kanal_resim
        kanal_resimleri.append(kanal_resim_url)
    else:
        kanal_resimleri.append('Resim bulunamadı')

    # Kanal linkini alalım
    kanal_link = kanal.get('href')
    if kanal_link:
        kanal_linkleri.append("https://canlitv.com" + kanal_link)
    else:
        kanal_linkleri.append('Link bulunamadı')

# Verileri yazdıralım
if kanal_adlari and kanal_resimleri and kanal_linkleri:
    print("Kanal Adları:")
    for kanal_ad in kanal_adlari:
        print(kanal_ad)
    
    print("\nKanal Resimleri:")
    for kanal_resim in kanal_resimleri:
        print(kanal_resim)

    print("\nKanal Linkleri:")
    for kanal_link in kanal_linkleri:
        print(kanal_link)
else:
    print("Veri çekilemedi!")
