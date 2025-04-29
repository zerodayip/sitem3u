import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time

# Kanal Listesi URL'si
base_url = "https://canlitv.com/?sayfa={}"

# Kanal Detaylarını almak için fonksiyon
def get_channel_data(page):
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    kanal_listesi = soup.find(id="kanal-listesi")
    if kanal_listesi:
        kanal_items = kanal_listesi.find_all("div", class_="kanal")
        for kanal in kanal_items:
            kanal_ad = kanal.find("div", class_="kanal_ad")
            kanal_resim = kanal.find("div", class_="kanal_resim").find("img") if kanal.find("div", class_="kanal_resim") else None
            kanal_link = kanal.find("a", title=True)

            # Eğer kanal_ad ve kanal_link varsa işleme alalım
            if kanal_ad and kanal_link:
                kanal_ad_text = kanal_ad.text.strip()
                kanal_resim_url = "https://canlitv.com" + kanal_resim["src"] if kanal_resim else None
                kanal_url = "https://canlitv.com" + kanal_link["href"]

                # Verileri yazdır
                print(f"Kanal Adı: {kanal_ad_text}")
                print(f"Logo URL: {kanal_resim_url}")
                print(f"Kanal Linki: {kanal_url}")
                print("------")

# Paralel olarak işlemleri yapalım
def scrape_channels():
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Sayfa numaralarını 1'den 6'ya kadar paralel işle
        pages = [1, 2, 3, 4, 5, 6]
        executor.map(get_channel_data, pages)
    end_time = time.time()
    print(f"Veri çekme tamamlandı. Süre: {end_time - start_time:.2f} saniye")

if __name__ == "__main__":
    scrape_channels()
