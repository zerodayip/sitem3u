from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    m3u8_links = []

    def handle_request(request):
        if ".m3u8" in request.url:
            m3u8_links.append(request.url)

    # Ağ trafiğini dinlemeye başla
    page.on("request", handle_request)

    # Sayfayı aç
    page.goto("https://canlitv.com/trt1-canli")

    # Iframe'i seç
    iframe = page.frame(name="Player")  # Burada iframe'in 'name' veya 'id' özelliklerine göre seçiyoruz

    # Eğer iframe'deki video öğesini bulabilirsen, buradaki oynatma işlemini tetikleyebilirsin:
    # iframe.click('button#play-button')  # Eğer bir play butonu varsa bunu tetikle

    # Yavaşça bekleyerek tüm medya kaynaklarının yüklenmesini sağla
    page.wait_for_timeout(10000)  # Sayfa yüklendikten sonra 10 saniye bekle

    # Bulunan m3u8 bağlantılarını yazdır
    if m3u8_links:
        print("Bulunan m3u8 bağlantıları:")
        for url in set(m3u8_links):
            print(url)
    else:
        print("Herhangi bir m3u8 bağlantısı bulunamadı.")

    browser.close()
