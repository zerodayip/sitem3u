import requests
from bs4 import BeautifulSoup

# 1'den 6'ya kadar olan sayfaları gezmek için
base_url = "https://canlitv.com/?sayfa="

# 1'den 6'ya kadar olan sayfa numaralarıyla döngü yapalım
for page_num in range(1, 7):
    url = base_url + str(page_num)
    
    # Sayfayı çekiyoruz
    response = requests.get(url)
    
    # Eğer sayfa başarılı bir şekilde geldiyse, verileri işleyelim
    if response.status_code == 200:
        print(f"Sayfa {page_num} başarıyla yüklendi!")
        
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
        print(f"Sayfa {page_num} yüklenemedi!")
