import json
import requests
import os
import sys
import re

OUTPUT_FILE_PATH = 'tvbahcesi/tvbahcesi.m3u'
COUNTRY_NAMES_PATH = 'tvbahcesi/countries.json'

def fetch_channels():
    base_url = "https://raw.githubusercontent.com/TVGarden/tv-garden-channel-list/main/channels/raw/countries"
    channels = []
    try:
        index_url = "https://api.github.com/repos/TVGarden/tv-garden-channel-list/contents/channels/raw/countries"
        response = requests.get(index_url)
        response.raise_for_status()

        files = response.json()
        country_files = [file['name'] for file in files if file['name'].endswith('.json')]
        for country_file in country_files:
            country_url = f"{base_url}/{country_file}"
            response = requests.get(country_url)
            response.raise_for_status()
            try:
                country_channels = response.json()
                if isinstance(country_channels, list):
                    channels.extend(country_channels)
            except json.JSONDecodeError as e:
                print(f"Error decoding {country_file}: {e}")
                continue
        return channels
    except requests.exceptions.RequestException as e:
        print(f"HTTP Hatası veya Ağ Hatası: {e}")
        return []
    except Exception as e:
        print(f"fetch_channels sırasında beklenmeyen hata: {e}")
        return []

def get_country_name(country_code):
    try:
        with open(COUNTRY_NAMES_PATH, 'r', encoding='utf-8') as f:
            country_names = json.load(f)
    except FileNotFoundError:
        print(f"Hata: countries.json dosyası bulunamadı: {COUNTRY_NAMES_PATH}. Varsayılan kullanılacak.")
        country_names = {}
    except json.JSONDecodeError as e:
        print(f"Error decoding countries.json: {e}. Varsayılan kullanılacak.")
        country_names = {}
    except Exception as e:
        print(f"get_country_name sırasında beklenmeyen hata: {e}")
        country_names = {}

    return country_names.get(country_code.lower(), country_code.upper())

def generate_m3u(channels):
    m3u_content = ["#EXTM3U"]
    for channel in channels:
        if 'iptv_urls' not in channel or not isinstance(channel['iptv_urls'], list) or \
           'name' not in channel or 'country' not in channel:
            print(f"Uyarı: Eksik veya yanlış formatta kanal verisi atlanıyor: {channel.get('name', 'Bilinmiyor')}")
            continue

        for index, url in enumerate(channel['iptv_urls']):
            if url and url.endswith('.m3u8'):
                channel_name = f"{channel['name']} ({index + 1})" if len(channel['iptv_urls']) > 1 else channel['name']
                country_code = channel['country'].lower()
                country_name = get_country_name(country_code)
                channel_id = re.sub(r'[^a-zA-Z0-9]+', '', channel_name).lower()
                lang_code = channel['country'].lower()

                m3u_content.append(
                    f"#EXTINF:-1 tvg-id=\"{channel_id}\" "
                    f"tvg-name=\"{channel_name}\" "
                    f"tvg-country=\"{country_code}\" "
                    f"tvg-language=\"{lang_code}\" "
                    f"group-title=\"{country_name}\",{channel_name}"
                )
                m3u_content.append(url)
    return '\n'.join(m3u_content)

if __name__ == '__main__':
    print("Kanallar getiriliyor...")
    channels = fetch_channels()

    if channels:
        print(f"Toplam {len(channels)} kanal getirildi.")
        print("M3U içeriği oluşturuluyor...")
        m3u_content = generate_m3u(channels)

        if m3u_content.strip() == "#EXTM3U":
            print("Uyarı: M3U içeriği oluşturulamadı veya boş.")
            sys.exit(1)
        else:
            output_dir = os.path.dirname(OUTPUT_FILE_PATH)
            try:
                os.makedirs(output_dir, exist_ok=True)
                with open(OUTPUT_FILE_PATH, 'w', encoding='utf-8') as f:
                    f.write(m3u_content)
                print(f"M3U file generated successfully at {OUTPUT_FILE_PATH}")
            except IOError as e:
                print(f"Dosya yazma hatası: {e}")
                sys.exit(1)
    else:
        print("Kanallar getirilemedi veya boş liste.")
        sys.exit(1)
