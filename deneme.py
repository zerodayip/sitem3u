import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# Sayfa numarasını alacak fonksiyon
def sayfa_isle(sayfa):
    base_url = "https://canlitv.com/?sayfa="  # Base URL
    sayfa_url = f"{base_url}{sayfa}"  # Sayfa numarasını URL'ye ekleyerek dinamik URL oluşturuyoruz
    
    # Sayfa yükleniyor
    print(f"Sayfa {sayfa} yükleniyor: {sayfa_url}")
    response = requests.get(sayfa_url)

    # HTML içeriğini parse ediyoruz
    soup = BeautifulSoup(response.content, 'html.parser')

    # Kanal listesi bulundu
    kanal_listesi = soup.find('ul')  # Kanal listesi burada 'ul' etiketinde
    if kanal_listesi:
        # Kanalları döngüyle alıyoruz
        kanallar = kanal_listesi.find_all('li')
        for kanal in kanallar:
            kanal_ad = kanal.find('a').text.strip()  # Kanal adı
            kanal_link = f"https://canlitv.com{kanal.find('a')['href']}"  # Kanal linki
            print(f"Kanal: {kanal_ad}, Link: {kanal_link}")

# Paralel çalışmak için ThreadPoolExecutor kullanıyoruz
with ThreadPoolExecutor(max_workers=6) as executor:
    # 1'den 6'ya kadar olan sayfaları paralel olarak işliyoruz
    executor.map(sayfa_isle, range(1, 7))  # range(1, 7) ile sayfa numarasını 1'den 6'ya kadar alıyoruz
