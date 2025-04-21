from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests

# Headless Chrome ayarları
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Ana sayfaya git
driver.get("https://daddylive.mp")

# 10 saniye bekle
time.sleep(10)

# Sonra JSON verisini requests ile al
session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

url = "https://daddylive.mp/schedule/schedule-generated.php"
response = session.get(url)
print(response.text)

driver.quit()
