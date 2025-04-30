import re

# Dosya yolları
input_file = "v/data.txt"
output_file = "v/vavoo.m3u"
logos_file = "v/logo.txt"
temp_turkey_file = "v/turkey_temp.m3u"  # Turkey geçici dosyası

# Logo eşleşmeleri için sözlük (tam eşleşme için)
logo_dict = {}
with open(logos_file, "r", encoding="utf-8") as logo_file:
    for line in logo_file:
        if '=' in line:
            names_part, logo_file_name = line.strip().split('=', 1)
            channel_names = [name.strip().upper() for name in names_part.split(',')]
            for name in channel_names:
                logo_dict[name] = logo_file_name.strip()

# Logo bulma fonksiyonu (tam eşleşme)
def find_logo(channel_name, logo_dict):
    return logo_dict.get(channel_name.strip().upper(), "")

# Kanal verisi listesi
channels = []

# Kanal verisini oku
with open(input_file, "r", encoding="utf-8") as file:
    country = channel_name = url = None

    for line in file:
        if line.startswith("Country = "):
            country = line.split('=')[1].strip().strip('"')
        elif line.startswith("Channel_Name = "):
            channel_name = line.split('=')[1].strip().strip('"')
            channel_name = re.sub(r"\(.*?\)", "", channel_name).strip()
        elif line.startswith("URL = "):
            url = line.split('=')[1].strip().strip('"')

            if country and channel_name and url:
                channels.append((country, channel_name, url))
                country = channel_name = url = None

# Kanalları sıralama (ilk 14 karaktere göre alfabetik)
channels.sort(key=lambda x: x[1][:14].upper())

# Gruplar
priority_groups = ["SPOR YAYINLARI", "BELGESEL YAYINLARI", "SİNEMA YAYINLARI", "TURKEY"]
priority_channels = []
other_channels = []
turkey_channels = []

# Kanal satırlarını oluştur
for country, channel_name, url in channels:
    clean_channel_name = channel_name.replace('"', '')
    logo = find_logo(clean_channel_name, logo_dict)

    if country.upper() == "TURKEY":
        # Grup başlığını belirle
        if "TABII" in channel_name.upper() or "SPOR" in channel_name.upper() or "EXXEN" in channel_name.upper():
            group_title = "SPOR YAYINLARI"
        elif any(keyword in channel_name.upper() for keyword in ["BELGESEL", "DOKÜMANTER", "NATGEO", "DISCOVERY", "GEOGRAPHIC", "WILD"]):
            group_title = "BELGESEL YAYINLARI"
        elif any(keyword in channel_name.upper() for keyword in ["SİNEMA", "MOVIE", "FILM"]):
            group_title = "SİNEMA YAYINLARI"
        else:
            group_title = "TURKEY"

        turkey_channels.append(f"""#EXTINF:-1 tvg-id="None" tvg-name="{clean_channel_name.upper()}" tvg-logo="{logo}" group-title="{group_title}", {clean_channel_name.upper()}
#EXTVLCOPT:http-user-agent=VAVOO/1.0
#EXTVLCOPT:http-referrer=https://vavoo.to/
{url}\n
""")
    else:
        group_title = country.upper()
        m3u_content = f"""#EXTINF:-1 tvg-id="None" tvg-name="{clean_channel_name.upper()}" tvg-logo="{logo}" group-title="{group_title}", {clean_channel_name.upper()}
#EXTVLCOPT:http-user-agent=VAVOO/1.0
#EXTVLCOPT:http-referrer=https://vavoo.to/
{url}\n
"""
        if group_title in priority_groups:
            priority_channels.append(m3u_content)
        else:
            other_channels.append(m3u_content)

# Turkey geçici dosyasını başlıksız oluştur
with open(temp_turkey_file, "w", encoding="utf-8") as temp_file:
    temp_file.writelines(turkey_channels)

# Ana M3U dosyasını oluştur
with open(output_file, "w", encoding="utf-8") as output:
    output.write("#EXTM3U\n\n\n")
    output.writelines(priority_channels)

    with open(temp_turkey_file, "r", encoding="utf-8") as temp_file:
        output.writelines(temp_file.readlines())

    output.writelines(other_channels)

print(f"{output_file} başarıyla oluşturuldu. Gereksiz #EXTM3U satırı kaldırıldı.")
