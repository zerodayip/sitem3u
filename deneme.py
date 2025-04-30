import requests
from bs4 import BeautifulSoup
import json

url = "https://vavoo.to/channels"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Sayfada sadece JSON varsa veya düz metin içinde JSON varsa:
    raw_text = soup.get_text()
    
    # Başındaki boşlukları sil
    raw_text = raw_text.strip()
    
    # JSON verisini yükle
    data = json.loads(raw_text)

    with open("data.txt", "w", encoding="utf-8") as file:
        for item in data:
            country = item.get("country", "")
            channel_id = item.get("id", "")
            channel_name = item.get("name", "").split(" (")[0]
            file.write(f'Country="{country}"\n')
            file.write(f'Channel="{channel_id}"\n')
            file.write(f'Channel_Name="{channel_name}"\n\n')

    print("Veriler başarıyla data.txt dosyasına kaydedildi.")

except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
    print(f"Bir hata oluştu: {e}")
