import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import re
from concurrent.futures import ThreadPoolExecutor

LEAGUE_MAPPING = {
    "NBA": "NBA", "NFL": "NFL", "NHL": "NHL", "MLB": "MLB",
    "NCAA F": "NCAAF", "NCAA B": "NCAAB", "Soccer": "Soccer",
    "UFC": "UFC", "Boxing": "Boxing", "WWE": "WWE", "MMA": "MMA",
    "Tennis": "Tennis", "Golf": "Golf", "Rugby": "Rugby", "Cricket": "Cricket",
    "NASCAR": "NASCAR", "F1": "F1", "MotoGP": "MotoGP", "IndyCar": "IndyCar",
    "Supercross": "Supercross", "Darts": "Darts", "Snooker": "Snooker",
    "Table Tennis": "Table Tennis", "Volleyball": "Volleyball",
    "Handball": "Handball", "Basketball": "Basketball", "Hockey": "Hockey",
    "Baseball": "Baseball", "Football": "Soccer"
}

base_url = "https://topembed.pw"

def extract_m3u8_from_embed_page(embed_url):
    m3u8_links = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Tarayıcıyı başlat
        page = browser.new_page()

        # Referer ve User-Agent gibi başlıkları ayarla
        page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": embed_url
        })

        # Sayfayı yükle
        page.goto(embed_url)

        # Ağ trafiğini izleyerek m3u8 linklerini bul
        def handle_route(route, request):
            # Ağ isteklerini kontrol et
            if '.m3u8' in request.url:
                m3u8_links.append(request.url)

        # Ağ trafiği dinleme
        page.on('route', handle_route)

        # Sayfa yüklenene kadar bekle (max 30 saniye)
        page.wait_for_load_state('load')

        # Tarayıcıyı kapat
        browser.close()

    return m3u8_links

def fetch_events():
    items = []

    # Spor etkinlikleri
    r = requests.get(f"{base_url}?all")
    soup = BeautifulSoup(r.text, "html.parser")
    all_link_objs = []

    for game in soup.select("div.bg-white"):
        title1 = game.select_one("div.font-bold").text.strip()
        title2 = game.select_one("div.mb-2").text.replace("Info: ", "").strip()
        league = next((v for k, v in LEAGUE_MAPPING.items() if k in title2), "Other")
        title = f"{title1} - {title2}"

        links = []
        for input_el in game.select("div.mb-4 > div > input"):
            url = input_el.get("value")
            if url and url.startswith("https"):
                link_obj = {"page": url, "m3u8": None}
                links.append(link_obj)
                all_link_objs.append(link_obj)

        items.append({"title": title, "league": league, "links": links})

    # TV yayınları
    r = requests.get(f"{base_url}?show_tv=true")
    soup = BeautifulSoup(r.text, "html.parser")

    for row in soup.select("tbody > tr"):
        title = row.select_one("td").text.strip()
        url = row.select_one("input").get("value")
        link_obj = {"page": url, "m3u8": None}
        items.append({"title": title, "league": "TV", "links": [link_obj]})
        all_link_objs.append(link_obj)

    # 50 iş parçacığı ile m3u8 tarama (Playwright ile)
    updated_links = []
    with ThreadPoolExecutor(max_workers=50) as executor:
        updated_links = list(executor.map(extract_m3u8_from_embed_page, [link["page"] for link in all_link_objs]))

    # Güncellenen m3u8'leri eşleştir
    idx = 0
    for item in items:
        for i in range(len(item["links"])):
            if updated_links[idx]:
                item["links"][i]["m3u8"] = updated_links[idx][0] if updated_links[idx] else None
            idx += 1

    return items


# ÇALIŞTIR
if __name__ == "__main__":
    events = fetch_events()
    for event in events:
        print(f"{event['league']}: {event['title']}")
        for link in event['links']:
            print(f"  Sayfa: {link['page']}")
            print(f"  m3u8 : {link['m3u8']}")
        print()
