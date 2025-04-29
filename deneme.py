import requests
from bs4 import BeautifulSoup

# Sayfa numarasını 1'den 6'ya kadar döngü ile artırıyoruz
for page_num in range(1, 7):
    url = f"https://canlitv.com/?sayfa={page_num}"

    # Sayfayı alıyoruz
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Sayfa {page_num} başarıyla yüklendi!\n")

        # Sayfa içeriğini BeautifulSoup ile parse ediyoruz
        soup = BeautifulSoup(response.text, 'html.parser')

        # Kanal listesine ait div'i alıyoruz
        kanal_list = soup.find_all('li', class_='tv fk_')

        # Her kanal için bilgi alıyoruz
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
        print(f"Sayfa {page_num} yüklenemedi!")
