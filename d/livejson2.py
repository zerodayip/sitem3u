from playwright.sync_api import sync_playwright
import os
import json
from datetime import datetime
import re
from bs4 import BeautifulSoup

def html_to_json(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    result = {}

    # Tarihi al
    date_div = soup.find('div', class_='entry-content')
    if not date_div:
        print("UYARI: Tarih içeriği bulunamadı!")
        return {}

    date_text_match = re.search(r'(\w+\s\d{2}th\s\w+\s\d{4})', date_div.get_text())
    if not date_text_match:
        print("UYARI: Tarih formatı çözümlenemedi!")
        return {}

    current_date = date_text_match.group(1)
    result[current_date] = {}

    # Kategori (örneğin "TV Shows")
    category_tag = soup.find('h2', string=re.compile(r'TV Shows', re.IGNORECASE))
    current_category = category_tag.get_text().strip() + "</span>" if category_tag else "TV Shows</span>"
    result[current_date][current_category] = []

    # Etkinlikleri işle
    for strong in soup.find_all('strong'):
        full_text = strong.get_text(" ", strip=True)
        time_match = re.match(r'^(\d{2}:\d{2})', full_text)

        if not time_match:
            continue

        event_time = time_match.group(1)
        event_info = full_text[len(event_time):].strip()

        # Kanal bilgilerini al
        channels = []
        links = strong.find_all('a', href=True)

        for link in links:
            href = link['href']
            channel_id_match = re.search(r'stream-(\d+)\.php', href)
            if channel_id_match:
                channel_id = channel_id_match.group(1)
                channel_name = link.get_text(strip=True)
                channel_name = re.sub(r'\s*\(CH-\d+\)$', '', channel_name)

                channels.append({
                    "channel_name": channel_name,
                    "channel_id": channel_id
                })

        # Kanal ismini etkinlik adından ayır
        event_info = re.sub(r'\s*\(CH-\d+\)', '', event_info)

        event_data = {
            "time": event_time,
            "event": event_info,
            "channels": channels
        }

        result[current_date][current_category].append(event_data)

    return result

def modify_json_file(json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    current_month = datetime.now().strftime("%B")

    for date in list(data.keys()):
        match = re.match(r"(\w+\s\d+)(st|nd|rd|th)\s(\w+)\s(\d{4})", date)
        if match:
            day_part = match.group(1)
            suffix = match.group(2)
            original_month = match.group(3)
            year_part = match.group(4)
            new_date = f"{day_part}{suffix} {original_month} {year_part}"
            data[new_date] = data.pop(date)

    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"JSON dosyası güncellendi ve kaydedildi: {json_file_path}")

def extract_schedule_container():
    url = "https://daddylivehd1.click/"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_output = os.path.join(script_dir, "schedule.json")

    print(f"{url} sayfasına erişiliyor, içerik çekiliyor...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            print("Sayfaya gidiliyor...")
            page.goto(url)
            print("Sayfanın yüklenmesi bekleniyor...")
            page.wait_for_timeout(10000)

            # Yeni yapı: div.entry-content içeriğini al
            schedule_content = page.evaluate("""() => {
                const container = document.querySelector('div.entry-content');
                return container ? container.parentElement.outerHTML : '';
            }""")

            if not schedule_content:
                print("UYARI: entry-content bulunamadı ya da boş!")
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
