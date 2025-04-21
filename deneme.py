import requests

url = "https://daddylive.mp/schedule/schedule.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # Hata varsa fırlatır

    with open("schedule.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    print("schedule.html başarıyla kaydedildi.")
except Exception as e:
    print("Hata oluştu:", e)

