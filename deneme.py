import requests
from bs4 import BeautifulSoup

url = "https://canlitv.com/?sayfa=1"
base_url = "https://canlitv.com"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

kanallar = soup.select("li.tv.fk_")

for kanal in kanallar:
    a_tag = kanal.find("a")
    if a_tag:
        kanal_adi = a_tag.text.strip()
        detay_url = base_url + a_tag.get("href")
        print(f"{kanal_adi} - {detay_url}")
