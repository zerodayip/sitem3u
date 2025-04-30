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

    # Sayfada JSON varsa düz metin olarak çek
    raw_text = soup.get_text().strip()
    data = json.loads(raw_text)

    with open("data.txt", "w", encoding="utf-8") as file:
        for item in data:
            country = item.get("country", "")
            channel_id = item.get("id", "")
            channel_name = item.get("name", "").split(" (")[0]
            url_line = f"https://vavoo.to/play/{channel_id}/index.m3u8"

            file.write(f'Country = "{country}"\n')
            file.write(f'Channel_Name = "{channel_name}"\n')
            file.write(f'URL = "{url_line}"\n\n')

    print("Veriler başarıyla data.txt dosyasına yazıldı.")

except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
    print(f"Bir hata oluştu: {e}")
