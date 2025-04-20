from bs4 import BeautifulSoup

# HTML dosyasını oku
with open("schedule2.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Bütün satırları sırayla al
rows = soup.find("table").find_all("tr")

current_category = None
output_lines = []

# Satırları sırayla işle
for i, row in enumerate(rows):
    if "category-row" in row.get("class", []):
        current_category = row.get_text(strip=True)

    elif "event-row" in row.get("class", []):
        time = row.find("div", class_="event-time").get_text(strip=True)
        event_info = row.find("div", class_="event-info").get_text(strip=True)

        # Sonraki satır kanal bilgisi
        next_row = rows[i + 1] if i + 1 < len(rows) else None
        if next_row and "channel-row" in next_row.get("class", []):
            channel_link = next_row.find("a", class_="channel-button-small")
            if channel_link and "stream-" in channel_link["href"]:
                channel_id = channel_link["href"].split("stream-")[-1].split(".php")[0]
            else:
                channel_id = "N/A"
            channel_name = channel_link.get_text(strip=True) if channel_link else ""
        else:
            channel_id = "N/A"
            channel_name = ""

        # Event formatla
        full_event = f'{time} ({current_category}) {event_info}{channel_name}'

        # Listeye ekle
        output_lines.append(f'Channel_ID= "{channel_id}"')
        output_lines.append(f'Event= "{full_event}"\n')

# schedule2.txt dosyasına yaz
with open("schedule2.txt", "w", encoding="utf-8") as outfile:
    outfile.write("\n".join(output_lines))

print("schedule2.txt başarıyla oluşturuldu.")

