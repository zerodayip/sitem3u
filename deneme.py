from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

# Otomatik driver kurulumu
chromedriver_autoinstaller.install()

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)
browser.get("https://canlitv.com/trt1-canli")

# Tüm sayfa kaynaklarını al
html = browser.page_source

# m3u8 var mı diye kontrol et
if ".m3u8" in html:
    print("Sayfa kaynağında m3u8 bulundu!")
    start = html.find("http")
    end = html.find(".m3u8") + 5
    print("M3U8 bağlantısı:", html[start:end])
else:
    print("Sayfa kaynağında m3u8 bulunamadı.")

browser.quit()
