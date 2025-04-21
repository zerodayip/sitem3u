import requests
from bs4 import BeautifulSoup

# Verilen URL
url = 'https://daddylive.mp/schedule/schedule.html'

# Sayfayı istek ile al
response = requests.get(url)

# Eğer istek başarılı ise (HTTP status 200)
if response.status_code == 200:
    # Sayfanın HTML içeriğini al
    html_content = response.text
    
    # HTML içeriğini işlemek için BeautifulSoup kullan
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # HTML içeriğini yazdır (isteğe bağlı, sadece kontrol için)
    print(soup.prettify())
else:
    print("Sayfa alınamadı:", response.status_code)
