import requests
import re

def download_m3u(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.splitlines()
    return []

def parse_m3u(m3u_lines, force_group_title=None, include_group_titles=None):
    parsed_entries = []
    entry = []
    group_title = ""

    for line in m3u_lines:
        if line.startswith("#EXTINF"):
            if force_group_title:
                line = re.sub(r'group-title="[^"]+"', f'group-title="{force_group_title}"', line)
                if 'group-title' not in line:
                    line = line.replace("#EXTINF", f'#EXTINF group-title="{force_group_title}"', 1)

            match = re.search(r'group-title="([^"]+)"', line)
            group_title = match.group(1) if match else "ZZZ"

            if include_group_titles and group_title not in include_group_titles:
                entry = []
                continue

            entry = [line]

        elif line.startswith("#EXTVLCOPT") or line.startswith("http"):
            if entry:
                entry.append(line)
                if line.startswith("http"):
                    parsed_entries.append((group_title, entry))
                    entry.append("")
                    entry = []

    return parsed_entries

def merge_m3u(url1, url2, url3, url4, url5, kanal_url, output_file="playlist.m3u"):
    new_m3u = download_m3u(url3)
    gol_m3u = download_m3u(url1)
    programlar_m3u = download_m3u(url4)
    vavoo_m3u = download_m3u(url2)
    event_m3u = download_m3u(url5)
    kanal_m3u = download_m3u(kanal_url)

    include_only = [
        "GÜNLÜK SPOR AKIŞI",
        "GÜNLÜK SPOR AKIŞI 2",
        "GÜNLÜK DÜNYA SPORLARI",
        "SPOR YAYINLARI (MAC SAATİ)",
        "SPOR YAYINLARI",
        "BELGESEL YAYINLARI",
        "SİNEMA YAYINLARI",
        "BUGÜNÜN DİZİLERİ",
        "BUGÜNÜN FİLMLERİ",
        "BUGÜNÜN SPOR İÇERİKLERİ",
        "BUGÜNÜN BELGESELLERİ",
        "BUGÜNÜN HABER PROGRAMLARI",
        "HAFTANIN FUTBOL FİKSTÜRÜ",
        "HAFTANIN BASKETBOL FİKSTÜRÜ",
        "TURKEY",
        "GÜNLÜK DÜNYA KANALLARI"
    ]

    group_priority = {group: i for i, group in enumerate(include_only)}

    merged_content = ["#EXTM3U"]
    all_entries = []

    for m3u_list, force_group in [
        (new_m3u, None),
        (gol_m3u, None),
        (programlar_m3u, None),
        (vavoo_m3u, None),
        (event_m3u, None),
        (kanal_m3u, None)
    ]:
        if m3u_list and m3u_list[0].startswith("#EXTM3U"):
            m3u_list.pop(0)
        all_entries.extend(parse_m3u(m3u_list, force_group, include_only))

    all_entries.sort(key=lambda x: group_priority.get(x[0], 99))

    for _, entry in all_entries:
        merged_content.extend(entry)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_content))

# Çalıştırma
merge_m3u(
    "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/g/gol.m3u",
    "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/v/vavoo.m3u",
    "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/v/new_m3u.m3u",
    "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/v/programlar.m3u",
    "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/d/event.m3u",
    "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/d/kanal.m3u"
)
