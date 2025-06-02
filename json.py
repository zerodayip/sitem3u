import json
import re

def parse_m3u_to_json(m3u_path, category_key, output_path):
    with open(m3u_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    channels = {}
    categories = {category_key: category_key.upper()}
    idx = 1000
    i = 0

    while i < len(lines):
        if lines[i].startswith("#EXTINF"):
            title_match = re.search(r',(.+)', lines[i])
            logo_match = re.search(r'tvg-logo="(.*?)"', lines[i])
            title = title_match.group(1).strip() if title_match else f"Channel {idx}"
            logo = logo_match.group(1).strip() if logo_match else ""
            url = lines[i + 1].strip() if (i + 1) < len(lines) else ""
            if url.startswith("http"):
                channels[str(idx)] = {
                    "name": title,
                    "icon": logo,
                    "url": url,
                    "category_id": category_key
                }
                idx += 1
            i += 2
        else:
            i += 1

    with open(output_path, "w", encoding="utf-8") as out:
        json.dump({"channels": channels, "categories": categories}, out, ensure_ascii=False, indent=2)

# Kullanım örneği:
# parse_m3u_to_json("r/main.m3u", "filmler", "r/vod.json")        # Filmler için
# parse_m3u_to_json("r/turkey_temp.m3u", "canli", "r/channels.json")  # Canlı yayınlar için
