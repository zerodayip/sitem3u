from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options,
    seleniumwire_options={}
)

driver.get("https://daddylive.mp/schedule")
time.sleep(5)

for request in driver.requests:
    if request.response and "schedule-generated.php" in request.url:
        print("JSON VERİSİ:")
        print(request.response.body.decode("utf-8"))
        break

driver.quit()
