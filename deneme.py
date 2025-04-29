import requests

# Belirli bir URL'yi al
url = "https://canlitv.com/?sayfa=1"  # Buraya istediğiniz URL'yi yazabilirsiniz

# Sayfayı isteyin
response = requests.get(url)

# Eğer sayfa başarılı şekilde yüklendiyse, HTML çıktısını yazdırıyoruz
if response.status_code == 200:
    print("Sayfa başarıyla yüklendi!")
    print(response.text)  # HTML içeriği
else:
    print(f"Sayfa yüklenemedi. Hata kodu: {response.status_code}")
