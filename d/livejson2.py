from playwright.sync_api import sync_playwright

def view_html_from_site():
    url = "https://daddylivehd1.click/"

    print(f"Sayfaya erişiliyor: {url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            page.goto(url)
            print("Sayfa yükleniyor, bekleniyor...")
            page.wait_for_timeout(10000)  # 10 saniye bekle

            html_content = page.evaluate("""() => document.body.innerHTML""")

            print("\n--- HTML İçeriği Başlangıcı ---\n")
            print(html_content)
            print("\n--- HTML İçeriği Sonu ---\n")

        except Exception as e:
            print(f"Hata oluştu: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    view_html_from_site()
