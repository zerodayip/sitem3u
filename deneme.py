from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Headless Chrome ayarlarını yapıyoruz
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# ChromeDriver'ı başlatıyoruz
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options,
    seleniumwire_options={}
)

# Sayfayı açıyoruz
driver.get("https://daddylive.mp/schedule")

# Sayfa tamamen yüklenene kadar bekliyoruz
time.sleep(5)

# İstekleri kontrol ediyoruz
for request in driver.requests:
    if request.response and "schedule-generated.php" in request.url:
        # JSON verisini almak
        json_data = request.response.body.decode("utf-8")
        print("Alınan JSON Verisi:")
        print(json_data)
        break

# Tarayıcıyı kapatıyoruz
driver.quit()
