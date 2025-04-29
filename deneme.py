import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

base_url = "https://canlitv.com"
sayfa_url = base_url + "/?sayfa={}"

def sayfa_isle(sayfa):
    try:
        response = requests.get(sayfa_url.format(sayfa), timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        kanallar = soup.select("li.tv.fk_")

        sonuc = [f"{a.text.strip()} - {base_url + a.get('href')}"
                 for kanal in kanallar if (a := kanal.find("a"))]
        return f"\n--- Sayfa {sayfa} ---\n" + "\n".join(sonuc)
    except Exception as e:
        return f"\n--- Sayfa {sayfa} ---\nHata: {e}"

with ThreadPoolExecutor(max_workers=6) as executor:
    results = executor.map(sayfa_isle, range(1, 7))

for r in results:
    print(r)
