import requests

# Sayfa URL'sini belirt
url = "https://canlitv.com/?sayfa=1"

# Sayfanın HTML içeriğini almak
response = requests.get(url)

# Sayfa başarılı bir şekilde alındıysa HTML içeriğini yazdır
if response.status_code == 200:
    print(response.text)
else:
    print("Sayfa alınamadı, HTTP Durum Kodu:", response.status_code)
