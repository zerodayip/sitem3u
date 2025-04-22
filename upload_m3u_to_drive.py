import json
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Secret'tan gelen JSON'u dosyaya yaz
with open("client_secrets.json", "w") as f:
    f.write(os.environ["GOOGLE_CLIENT_SECRET_JSON"])

# Kimlik doğrulama
gauth = GoogleAuth()
gauth.LoadClientConfigFile("client_secrets.json")
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# playlist.m3u dosyasını Drive'a yükle
file = drive.CreateFile({'title': 'playlist.m3u'})
file.SetContentFile('playlist.m3u')
file.Upload()

# Paylaşılabilir yap
file.InsertPermission({
    'type': 'anyone',
    'value': 'anyone',
    'role': 'reader'
})

print(f"Yüklendi: https://drive.google.com/file/d/{file['id']}/view?usp=sharing")
