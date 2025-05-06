from playwright.sync_api import sync_playwright
import os
import json
from datetime import datetime
import re
from bs4 import BeautifulSoup

def html_to_json(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    result = {}

    # Tarih bilgisi <h2><strong>Tuesday 06th May 2025 – Schedule Time UK GMT</strong></h2>
    date_header = soup.find('h2', string=re.compile(r'\w+ \d{2}(st|nd|rd|th) \w+ \d{4}', re.IGNORECASE))
    if not date_header:
        print("UYARI: Tarih bilgisi bulunamadı!")
        return {}

    date_text = date_header.get_text(strip=True).split('–')[0].strip()
    result[date_text] = {}

    # Kategori (örneğin "TV Shows")
    category_header = soup.find('h2', string=re.compile(r'TV Shows', re.IGNORECASE))
    if not category_header:
        print("UYARI: Kategori başlığı bulunamadı!")
        return result

    category = category_header.get_text(strip=True)
    result[date_text][category] = []

    # Etkinlikler: kategori başlığından sonraki <strong> etiketleri
    strong_tags = category_header.find_all_next('strong')
    for tag in strong_tags:
        raw_text = tag.get_text(" ", strip=True)
        match = re.match(r"(\d{2}:\d{2})\s+(.*?)(?=(https?|$))", raw_text)
        if not match:
            continue

        event_time = match.group(1)
        event_info = match.group(2).strip()

        # Linklerdeki kanal bilgilerini çek
        channels = []
        for a in tag.find_all('a', href=True):
            href = a['href']
            name = a.get_text(strip=True)
            id_match = re.search(r'stream-(\d+)\.php', href)
            if id_match:
                channel_id = id_match.group(1)
                clean_name = re.sub(r'\s*\(CH-\d+\)$', '', name)
                channels.append({
                    "channel_name": clean_name,
                    "channel_id": channel_id
                })

        result[date_text][category].append({
            "time": event_time,
            "event": event_info,
            "channels": channels
        })

    return result


def modify_json_file(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    current_month = datetime.now().strftime("%B")

    for date in list(data.keys()):
        match = re.match(r"(\w+\s\d+)(st|nd|rd|th)\s(\d{4})", date)
        if match:
            day_part = match.group(1)
            suffix = match.group(2)
            year_part = match.group(3)
            new_date = f"{day_part}{suffix} {current_month} {year_part}"
            data[new_date] = data.pop(date)

    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"JSON dosyası güncellendi ve kaydedildi: {json_file_path}")

def extract_schedule_container():
    url = "https://daddylive.dad/"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_output = os.path.join(script_dir, "schedule.json")

    print(f"{url} sayfasına erişiliyor, ana program içeriği çekiliyor...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print("Sayfaya gidiliyor...")
            page.goto(url)
            print("Sayfanın tam yüklenmesi bekleniyor...")
            page.wait_for_timeout(10000)  # 10 saniye

            schedule_content = page.evaluate("""() => {
                const container = document.getElementById('main-schedule-container');
                return container ? container.outerHTML : '';
            }""")

            if not schedule_content:
                print("UYARI: main-schedule-container bulunamadı ya da boş!")
                return False

            print("HTML içerik JSON formatına dönüştürülüyor...")
            json_data = html_to_json(schedule_content)

            with open(json_output, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=4, ensure_ascii=False)

            print(f"JSON verileri kaydedildi: {json_output}")

            modify_json_file(json_output)
            browser.close()
            return True

        except Exception as e:
            print(f"HATA: {str(e)}")
            return False

if __name__ == "__main__":
    success = extract_schedule_container()
    if not success:
        exit(1)
