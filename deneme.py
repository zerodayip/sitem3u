from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")

# ChromeDriver'ı otomatik olarak indirmek ve çalıştırmak
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

url = 'https://daddylive.mp/schedule/schedule.html'
driver.get(url)

# Sayfanın HTML içeriğini almak
html_content = driver.page_source
print(html_content)

driver.quit()
