import requests

url = "https://vavoo.to/channels"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print(response.text)
else:
    print(f"Sayfa alınamadı. Durum kodu: {response.status_code}")
