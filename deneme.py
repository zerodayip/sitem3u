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

# Kanal listesini bulalım
kanal_listesi = soup.find_all('div', {'class': 'kanal_ad'})

# Verileri yazdırıyoruz
if kanal_listesi:
    print("Kanal Adları:")
    for kanal in kanal_listesi:
        print(kanal.text.strip())  # Kanal adını yazdırıyoruz
else:
    print("Kanal adı bulunamadı!")

# Kanal resimlerinin URL'lerini alalım
kanal_resimleri = soup.find_all('div', {'class': 'kanal_resim'})

if kanal_resimleri:
    print("\nKanal Resimleri:")
    for resim in kanal_resimleri:
        img_tag = resim.find('img')
        if img_tag and 'src' in img_tag.attrs:
            resim_url = "https://canlitv.com" + img_tag.attrs['src']
            print(resim_url)
        else:
            print("Resim URL'si bulunamadı!")
else:
    print("Kanal resimleri bulunamadı!")

# Kanal linklerini alalım
kanal_linkleri = soup.find_all('a', {'title': True})

if kanal_linkleri:
    print("\nKanal Linkleri:")
    for link in kanal_linkleri:
        kanal_link = "https://canlitv.com" + link['href']
        print(kanal_link)
else:
    print("Kanal linkleri bulunamadı!")
