from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-agent=Mozilla/5.0")

driver = webdriver.Chrome(options=options)

# 1. Ana sayfaya git (cookie, token vs. için)
driver.get("https://daddylive.mp/")
time.sleep(10)

# 2. JSON verisinin üretildiği URL'ye git
driver.get("https://daddylive.mp/schedule/schedule-generated.php")
time.sleep(2)

# 3. İçeriği yazdır
print(driver.page_source)

driver.quit()
