import requests
from bs4 import BeautifulSoup

# Sayfa URL'lerini tek tek yazalım
urls = [
    "https://canlitv.com/?sayfa=1",
    "https://canlitv.com/?sayfa=2",
    "https://canlitv.com/?sayfa=3",
    "https://canlitv.com/?sayfa=4",
    "https://canlitv.com/?sayfa=5",
    "https://canlitv.com/?sayfa=6"
]

# Her sayfayı tek tek gezerek verileri çekelim
for url in urls:
    # Sayfayı çekiyoruz
    response = requests.get(url)
    
    # Eğer sayfa başarılı bir şekilde geldiyse, verileri işleyelim
    if response.status_code == 200:
        print(f"Sayfa başarıyla yüklendi: {url}")
        
        # HTML'yi BeautifulSoup ile parse edelim
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Kanal linklerini bulmak için tüm <a> etiketlerine bakacağız
        kanal_links = soup.find_all('a', title=True)  # title attribute'u olan <a> etiketleri

        # Kanal bilgilerini alalım
        for kanal in kanal_links:
            kanal_ad = kanal.text.strip()  # Kanal adı
            kanal_url = "https://canlitv.com" + kanal['href']  # Kanal URL'si

            # Kanal bilgilerini ekrana yazdıralım
            print(f"Kanal Adı: {kanal_ad}")
            print(f"Kanal URL: {kanal_url}")
            print("-" * 50)
    
    else:
        print(f"Sayfa yüklenemedi: {url}")
