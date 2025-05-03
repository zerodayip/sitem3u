import requests
from bs4 import BeautifulSoup
import re

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


def extract_m3u8_from_url(url, referer):
    try:
        headers = {"Referer": referer, "User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        m3u8_links = re.findall(r'https?://[^\s"\']+\.m3u8', r.text)
        return m3u8_links[0] if m3u8_links else None
    except Exception as e:
        print(f"m3u8 extraction failed for {url}: {e}")
        return None


def fetch_events():
    base_url = "https://topembed.pw"
    items = []

    # İlk sayfa (spor etkinlikleri)
    response = requests.get(f"{base_url}?all")
    soup = BeautifulSoup(response.text, "html.parser")

    for game in soup.select("div.bg-white"):
        title1 = game.select_one("div.font-bold").text.strip()
        title2 = game.select_one("div.mb-2").text.replace("Info: ", "").strip()

        # Lig belirleme
        league = "Other"
        for key, value in LEAGUE_MAPPING.items():
            if key in title2:
                league = value
                break

        links = []
        for channel in game.select("div.mb-4 > div > input"):
            link = channel.get("value")
            if link and link.startswith("https"):
                m3u8 = extract_m3u8_from_url(link, referer=base_url)
                links.append({"page": link, "m3u8": m3u8})

        items.append({
            "title": f"{title1} - {title2}",
            "league": league,
            "links": links
        })

    # İkinci sayfa (TV yayınları)
    response = requests.get(f"{base_url}?show_tv=true")
    soup = BeautifulSoup(response.text, "html.parser")

    for row in soup.select("tbody > tr"):
        title = row.select_one("td").text.strip()
        link = row.select_one("input").get("value")
        m3u8 = extract_m3u8_from_url(link, referer=base_url)
        items.append({
            "title": title,
            "league": "TV",
            "links": [{"page": link, "m3u8": m3u8}]
        })

    return items


# Kullanım
if __name__ == "__main__":
    events = fetch_events()
    for event in events:
        print(f"{event['league']}: {event['title']}")
        for link in event['links']:
            print(f"  Sayfa Linki: {link['page']}")
            print(f"  m3u8 Linki:  {link['m3u8']}")
        print()
