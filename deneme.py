from datetime import datetime, timezone

# origin.txt dosyasından URL'yi oku
with open("d/origin.txt", "r", encoding="utf-8") as f:
    origin_url = f.read().strip()

# schedule_son.txt dosyasından verileri oku
schedule_entries = []

with open("d/schedule_son.txt", "r", encoding="utf-8") as f:
    lines = f.read().strip().split("\n\n")

    for line in lines:
        entry = {}
        for item in line.split("\n"):
            if item.startswith("Channel_Name="):
                entry["Channel_Name"] = item.split('=')[1].strip().strip('"')
            elif item.startswith("Channel_server="):
                entry["Channel_server"] = item.split('=')[1].strip().strip('"')
            elif item.startswith("Event="):
                entry["Event"] = item.split('=')[1].strip().strip('"')
        if entry:
            schedule_entries.append(entry)

# Şu anki saat alınır ve UTC olarak dakikası sıfırlanır
current_time = datetime.now(timezone.utc)
today_date = current_time.date()

# Geçici temp_schedule.txt dosyasını oluşturma
with open("d/temp_schedule.txt", "w", encoding="utf-8") as temp_file:
    for entry in schedule_entries:
        channel_name = entry["Channel_Name"]
        channel_server = entry["Channel_server"]
        event = entry["Event"]

        try:
            event_time_str = event.strip().split()[0]  # Örn: "19:00"
            event_time_obj = datetime.strptime(event_time_str, "%H:%M").replace(
                year=today_date.year,
                month=today_date.month,
                day=today_date.day,
                tzinfo=timezone.utc
            )

            # Etkinlik saati şu anki saatten büyükse yaz
            if event_time_obj > current_time:
                temp_file.write(f'Channel_Name={channel_name}\n')
                temp_file.write(f'Channel_server={channel_server}\n')
                temp_file.write(f'Event={event}\n\n')

        except Exception as e:
            print(f"Hatalı etkinlik saati: {event} — Hata: {e}")

# Temp dosyasındaki verilerle event.txt dosyasını oluşturma
with open("d/event.txt", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n\n")

    with open("d/temp_schedule.txt", "r", encoding="utf-8") as temp_file:
        temp_lines = temp_file.read().strip().split("\n\n")

        for line in temp_lines:
            entry = {}
            for item in line.split("\n"):
                if item.startswith("Channel_Name="):
                    entry["Channel_Name"] = item.split('=')[1].strip().strip('"')
                elif item.startswith("Channel_server="):
                    entry["Channel_server"] = item.split('=')[1].strip().strip('"')
                elif item.startswith("Event="):
                    entry["Event"] = item.split('=')[1].strip().strip('"')

            if entry:
                channel_name = entry["Channel_Name"]
                channel_server = entry["Channel_server"]
                event = entry["Event"]

                f.write(f'#EXTINF:-1 tvg-id="{event}" tvg-logo="{channel_server}" group-title="GÜNLÜK DÜNYA SPORLARI",{event}\n')
                f.write(f'#EXTVLCOPT:http-origin={origin_url}\n')
                f.write(f'#EXTVLCOPT:http-referrer={origin_url}\n')
                f.write(f'#EXTVLCOPT:http-user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1\n')
                f.write(f'https://{channel_server}top1.newkso.ru/{channel_server}/premium{channel_name}/mono.m3u8\n\n')

print("event.txt başarıyla oluşturuldu.")
