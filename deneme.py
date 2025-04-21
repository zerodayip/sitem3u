import requests

url = "https://daddylive.mp/schedule/schedule-generated.json"  # Dilersen diğer domainleri de deneyebilirsin
try:
    response = requests.get(url, timeout=10)
    data = response.json()
    print(data)
except Exception as e:
    print("Hata oluştu:", e)
