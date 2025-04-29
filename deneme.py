from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/117.0.0.0 Safari/537.36")

driver = webdriver.Chrome(options=options)

# Asıl sayfayı aç
driver.get("https://canlitv.com/trt1-canli")
time.sleep(5)

# iframe'i bul
try:
    iframe = driver.find_element("id", "Player")
    iframe_src = iframe.get_attribute("src")
    print(f"iframe src: {iframe_src}")
    
    # iframe içine git
    driver.get("https://canlitv.com" + iframe_src)
    time.sleep(5)

    # İçeriği al ve .m3u8 ara
    html = driver.page_source
    matches = re.findall(r'https?://[^\s"\']+\.m3u8', html)

    if matches:
        print("Bulunan .m3u8 bağlantıları:")
        for m in matches:
            print(m)
    else:
        print("Hiçbir .m3u8 bağlantısı bulunamadı.")

except Exception as e:
    print(f"Hata oluştu: {e}")

driver.quit()
