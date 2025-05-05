from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
import json

def extract_html():
    url = "https://daddylivehd1.click/"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(10000)  # 10 saniye bekle
        html = page.content()
        browser.close()
        return html

def html_to_json(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    result = {}

    # 1. Tarih başlığını al (örneğin "Monday 05th May 2025 – Schedule Time UK GMT")
    date_tag = soup.find('div', class_='entry-content')
    if date_tag:
        # Tarih bilgisi <h2><strong>...</strong></h2> içinde yer alıyor
        date_text = date_tag.find('h2').find('strong').get_text(strip=True)
        result[date_text] = {}
        print(f"Tarih Bilgisi: {date_text}")  # Tarih bilgisini yazdıralım
    else:
        print("Tarih bilgisi bulunamadı.")
        return {}

    current_category = None

    # 2. Kategorileri ve etkinlikleri işle
    for tag in soup.find_all(['h2', 'p']):
        if tag.name == 'h2' and tag.find('strong'):
            current_category = tag.get_text(strip=True)
            result[date_text][current_category] = []

        elif tag.name == 'p':
            strong_tags = tag.find_all('strong')
            for st in strong_tags:
                full_text = st.get_text(" ", strip=True)
                time_match = re.match(r'^(\d{2}:\d{2})\s+(.*)', full_text)
                if not time_match:
                    continue

                time = time_match.group(1)
                event_text = time_match.group(2)

                channels = []
                for a in st.find_all('a'):
                    href = a.get('href', '')
                    ch_id_match = re.search(r'stream-(\d+)\.php', href)
                    ch_id = ch_id_match.group(1) if ch_id_match else ""
                    ch_name = re.sub(r'\s*\(CH-\d+\)$', '', a.get_text(strip=True))
                    if ch_id:
                        channels.append({
                            "channel_name": ch_name,
                            "channel_id": ch_id
                        })

                result[date_text][current_category].append({
                    "time": time,
                    "event": event_text,
                    "channels": channels
                })

    return result

def save_json(data, filename="schedule.json"):
    # JSON verisini belirtilen dosyaya kaydet
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"JSON verisi '{filename}' dosyasına kaydedildi.")

if __name__ == "__main__":
    # HTML içeriğini al
    html_content = extract_html()

    # HTML'den JSON verisi oluştur
    data = html_to_json(html_content)

    # JSON çıktısını kaydet
    if data:
        save_json(data, "schedule.json")
    else:
        print("Veri oluşturulamadı.")
