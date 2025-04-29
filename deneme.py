import requests

# Sayfa numarasını 1 yapalım
base_url = "https://canlitv.com/?sayfa=1"  # Sayfa 1

# Sayfa yükleniyor
response = requests.get(base_url)

# HTML içeriğini yazdıralım
print(response.text)  # Sayfanın tam HTML içeriği
