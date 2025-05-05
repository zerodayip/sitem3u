from bs4 import BeautifulSoup
import json

# HTML dosyasını aç ve içeriği oku
with open("live.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# BeautifulSoup ile HTML'yi parse et
soup = BeautifulSoup(html_content, "html.parser")

# Verileri saklayacağımız ana sözlük
data = {}

# Tarih bilgisi (örnek: Sunday 04th May May 2025)
schedule_date = "Sunday 04th May May 2025 - Schedule Time UK GMT"
data[schedule_date] = {}

# Tüm 'h2' başlıklarını bul ve ilgili içerikleri JSON formatında topla
sections = soup.find_all('h2')

for section in sections:
    section_name = section.get_text(strip=True)
    
    # Eğer başlık altında içerik varsa, ilgili içerikleri al
    section_content = []
    
    # Bu başlık altında bulunan tüm içerikleri al
    content_paragraph = section.find_next('p')
    if content_paragraph:
        entries = content_paragraph.find_all('strong')
        for entry in entries:
            show_info = entry.get_text(strip=True)
            time = show_info.split(" ")[0]  # ilk kelime saati alır
            event = " ".join(show_info.split(" ")[1:])  # geri kalanı etkinlik adı
            link = entry.find('a')['href'] if entry.find('a') else None

            # Kanal bilgilerini çıkaralım
            channel_info = []
            if link:
                channel_name = entry.find('a').get_text(strip=True)
                channel_id = link.split("-")[-1].split(".")[0]  # Linkten kanal ID'sini alıyoruz
                channel_info.append({
                    "channel_name": channel_name,
                    "channel_id": channel_id
                })

            section_content.append({
                "time": time,
                "event": event,
                "channels": channel_info
            })

    # Eğer içerik varsa, o bölümü JSON'a ekleyelim
    if section_content:
        data[schedule_date][section_name] = section_content

# JSON formatında çıktıyı yazdır
json_output = json.dumps(data, indent=4)
print(json_output)

# JSON'u bir dosyaya kaydedelim
with open("schedule_output.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_output)
