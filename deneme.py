from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import time

# ChromeDriver'ı otomatik indirip kur
chromedriver_autoinstaller.install()

# Tarayıcı ayarları
options = Options()
options.add_argument("--headless")  # Tarayıcıyı görünmeden çalıştır
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Tarayıcıyı başlat
browser = webdriver.Chrome(options=options)
browser.get("https://canlitv.com/trt1-canli")

# Sayfanın tam yüklenmesi için bekle (isteğe bağlı artırılabilir)
time.sleep(5)

# iframe içindeki player sayfasını bul
try:
    iframe = browser.find_element("id", "Player")
    iframe_src = iframe.get_attribute("src")
    print(f"[iframe src] {iframe_src}")
except Exception as e:
    print("[iframe bulunamadı]", e)
    iframe_src = None

# iframe varsa içeriğini ayrıca aç ve m3u8 ara
if iframe_src:
    if not iframe_src.startswith("http"):
        iframe_src = "https://canlitv.com" + iframe_src
    browser.get(iframe_src)
    time.sleep(5)

    html = browser.page_source
    if ".m3u8" in html:
        start = html.find("http")
        end = html.find(".m3u8") + 5
        print("[m3u8 bulundu]", html[start:end])
    else:
        print("[iframe içinde m3u8 bulunamadı]")
else:
    print("[iframe bulunamadı veya geçersiz]")

browser.quit()
