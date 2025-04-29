import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import time

# PHP sayfasından veriyi almak için fonksiyon
def get_php_data(channel_url):
    try:
        response = requests.get(channel_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # PHP sayfasındaki veri, örneğin başlık, içerik veya başka bir veri
        php_data = soup.find('div', {'class': 'some-class'})  # Bu kısmı değiştirin
        if php_data:
            return php_data.text.strip()
        else:
            return "Veri Bulunamadı"
    except Exception as e:
        return f"Hata: {e}"

# Kanal verilerini almak için fonksiyon
def get_channel_data(page_number):
    url = f'https://canlitv.com/?sayfa={page_number}'
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        kanal_listesi = soup.find('div', {'id': 'kanal-listesi'})
        if kanal_listesi:
            channels = kanal_listesi.find_all('div', {'class': 'kanal'})

            channel_data = []
            for channel in channels:
                kanal_ad = channel.find('div', {'class': 'kanal_ad'}).text.strip()
                kanal_resim = 'https://canlitv.com' + channel.find('div', {'class': 'kanal_resim'}).find('img')['src']
                kanal_link = 'https://canlitv.com' + channel.find('a')['href']

                # PHP verisini almak için ilgili URL'yi çağırıyoruz
                php_data = get_php_data(kanal_link)

                channel_data.append({
                    'kanal_ad': kanal_ad,
                    'kanal_resim': kanal_resim,
                    'kanal_link': kanal_link,
                    'php_data': php_data  # PHP verisini ekliyoruz
                })

            return channel_data
        else:
            return []

    except Exception as e:
        return f"Hata: {e}"

# Sayfa numaralarını paralel şekilde işlemek için fonksiyon
def scrape_all_pages(start_page, end_page):
    with ThreadPoolExecutor(max_workers=50) as executor:
        results = executor.map(get_channel_data, range(start_page, end_page + 1))
    
    all_channels = []
    for result in results:
        all_channels.extend(result)

    return all_channels

# Ana fonksiyon
def main():
    start_time = time.time()

    # Sayfaları 1'den 6'ya kadar çekiyoruz
    all_data = scrape_all_pages(1, 6)

    for channel in all_data:
        print(f"Kanal Adı: {channel['kanal_ad']}")
        print(f"Kanal Resim: {channel['kanal_resim']}")
        print(f"Kanal Link: {channel['kanal_link']}")
        print(f"PHP Verisi: {channel['php_data']}")
        print('----------------------------')

    print(f"İşlem Süresi: {time.time() - start_time:.2f} saniye")

if __name__ == "__main__":
    main()
