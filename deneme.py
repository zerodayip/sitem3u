from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    m3u8_links = []

    def handle_request(request):
        if ".m3u8" in request.url:
            m3u8_links.append(request.url)

    page.on("request", handle_request)

    # Örnek kanal sayfası
    print("Sayfa yükleniyor...")
    page.goto("https://canlitv.com/trt1-canli")
    page.wait_for_timeout(5000)

    # Bağlantılar
    if m3u8_links:
        print("Bulunan m3u8 bağlantıları:")
        for url in set(m3u8_links):
            print(url)
    else:
        print("Herhangi bir m3u8 bağlantısı bulunamadı.")

    browser.close()
