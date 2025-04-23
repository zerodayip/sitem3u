import time
import hashlib
import random
import os
from datetime import datetime

# Token üretimi için fonksiyon
def generate_token(secret_key, expiration_days):
    # Geçerlilik süresi ve geçici bir zaman damgası oluşturuluyor
    expiration_timestamp = int(time.time()) + (expiration_days * 86400)  # Gün cinsinden, saniyeye çevriliyor
    
    # Token'ı oluşturmak için hash kullanıyoruz
    raw_token = f"{secret_key}{expiration_timestamp}"
    token = hashlib.sha256(raw_token.encode()).hexdigest()
    
    return token, expiration_timestamp

# Token'in geçerliliğini kontrol etme
def is_token_valid(token, expiration_timestamp):
    current_timestamp = int(time.time())
    if current_timestamp > expiration_timestamp:
        return False  # Token süresi dolmuş
    return True  # Token geçerli

# Random 5 sayı ile secret_key oluştur
def generate_random_secret_key():
    return ''.join(random.choices('0123456789', k=5))  # 5 basamaktan oluşan random sayı

# M3U dosyasına tokenli link eklemek ve IP kontrolü
def add_token_info_to_file(name, token_link, expiration_timestamp, file_path='token.txt'):
    expire_date = datetime.utcfromtimestamp(expiration_timestamp).strftime('%Y-%m-%d %H:%M:%S')  # Expire tarihi formatlıyoruz
    
    # Dosyaya yazma
    with open(file_path, 'w') as f:
        f.write(f"NAME= {name}\n")
        f.write(f"TOKEN LINK= {token_link}\n")
        f.write(f"EXPIRE DATE= {expire_date}\n")

# Örnek kullanım
expiration_days = 1  # Geçerlilik süresi 1 gün
base_url = "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/playlist.m3u"
name = "MURAT DUYMAZ"  # Dinamik olarak buraya istediğiniz ismi yazabilirsiniz
m3u_url = "https://raw.githubusercontent.com/MDuymazz/sitem3u/refs/heads/main/playlist.m3u"  # M3U dosyasının URL'si

# Secret Key oluştur
secret_key = generate_random_secret_key()

# Token oluştur
token, expiration_timestamp = generate_token(secret_key, expiration_days)

# Token linki oluştur
token_link = f"{base_url}?token={token}"

# Token bilgilerini dosyaya kaydet
add_token_info_to_file(name, token_link, expiration_timestamp)

print("Token ve bilgi dosyaya kaydedildi.")

