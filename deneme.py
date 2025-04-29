import requests
from bs4 import BeautifulSoup

# Manually visit each page (sayfa 1 to sayfa 6)
page_urls = [
    "https://canlitv.com/?sayfa=1",
    "https://canlitv.com/?sayfa=2",
    "https://canlitv.com/?sayfa=3",
    "https://canlitv.com/?sayfa=4",
    "https://canlitv.com/?sayfa=5",
    "https://canlitv.com/?sayfa=6"
]

# Loop through each URL to get data
for url in page_urls:
    print(f"Veri çekiliyor: {url}")
    
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Sayfa başarıyla yüklendi: {url}")
        
        # BeautifulSoup ile sayfa içeriğini parse ediyoruz
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Kanal listesine ait 'li' elemanlarını buluyoruz
        kanal_list = soup.find_all('li', class_='tv fk_')

        # Her bir kanal için bilgileri alıyoruz
        for kanal in kanal_list:
            # Kanal adı
            kanal_ad = kanal.find('a').text.strip()

            # Kanal linki
            kanal_link = kanal.find('a')['href']
            kanal_link = f"https://canlitv.com{kanal_link}"

            print(f"Kanal Adı: {kanal_ad}")
            print(f"Kanal Linki: {kanal_link}")
            print("-" * 40)

    else:
        print(f"Sayfa yüklenemedi: {url}")
