from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştırır
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# WebDriver'ı başlatıyoruz
service = Service('/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Hedef URL'yi açıyoruz
url = 'https://daddylive.mp/schedule/schedule.html'
driver.get(url)

# Sayfanın dinamik olarak yüklenmesi için beklemek
time.sleep(5)

# HTML içeriğini alıyoruz
html_content = driver.page_source

# Sayfanın HTML içeriğini yazdırıyoruz
print(html_content)

# WebDriver'ı kapatıyoruz
driver.quit()
