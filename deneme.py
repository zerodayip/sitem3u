import chromedriver_binary_auto
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Chrome seçeneklerini ayarlayın
chrome_options = Options()
chrome_options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştırmak için

# ChromeDriver servisini başlatın
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

# Web sayfasını açın
driver.get("https://daddylive.mp/schedule/schedule.html")

# Sayfa kaynağını alın
html_content = driver.page_source
print(html_content)

# Tarayıcıyı kapatın
driver.quit()
