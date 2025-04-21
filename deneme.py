from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome ayarları
options = Options()
options.add_argument("--headless")  # Tarayıcıyı arka planda açmak için
options.add_argument("--disable-gpu")  # GPU hızlandırmasını devre dışı bırak
options.add_argument("--no-sandbox")  # Sandbox'u devre dışı bırak (Linux için gerekli olabilir)
options.add_argument("window-size=1200x600")  # Tarayıcı pencere boyutunu belirle (yükleme hızını etkileyebilir)
options.add_argument("--disable-dev-shm-usage")  # Paylaşılan bellek kullanımını devre dışı bırak

# ChromeDriver'ı otomatik olarak indirip Service ile başlat
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    # Siteye git
    driver.get("https://daddylive.mp/")

    # WebDriverWait ile butonun tıklanabilir hale gelmesini bekleyin
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#header > header > div > strong > nav > a:nth-child(3)")))

    # CSS Selector ile üçüncü bağlantıya tıklama
    driver.find_element(By.CSS_SELECTOR, "#header > header > div > strong > nav > a:nth-child(3)").click()

    # main-schedule-container div'inin yüklenmesini bekleyin
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "main-schedule-container")))

    # main-schedule-container div'ini al
    main_schedule_container = driver.find_element(By.ID, "main-schedule-container")
    
    # İçeriği HTML olarak al
    html = main_schedule_container.get_attribute("outerHTML")

    # HTML içeriğini dosyaya kaydet
    with open("output_schedule2.html", "w", encoding="utf-8") as file:
        file.write(html)
        print("HTML kaydedildi: output_schedule.html")

finally:
    driver.quit()
