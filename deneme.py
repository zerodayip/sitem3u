from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument("--user-agent=Mozilla/5.0")

driver = webdriver.Chrome(options=options)

try:
    # Ana sayfaya git
    driver.get("https://daddylive.mp/")
    
    # Extra Schedule butonunun yüklenmesini bekle (bu sayfanın JS'lerinin yüklenmesini tetikliyor)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Extra Schedule')]"))
    )

    # Beklemenin ardından veriye git
    driver.get("https://daddylive.mp/schedule/schedule-generated.php")
    time.sleep(2)

    print(driver.page_source)

finally:
    driver.quit()
