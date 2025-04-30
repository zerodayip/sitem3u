import gzip
import shutil
import os

# Giriş ve çıkış dosyaları
input_file = 'logo.xml'
output_file = 'epg.xml.gz'

# GZ formatına dönüştürme
def compress_xml_to_gz(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"HATA: {input_path} bulunamadı.")
        return

    with open(input_path, 'rb') as f_in:
        with gzip.open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(f"{input_path} başarıyla {output_path} dosyasına dönüştürüldü.")

# Fonksiyonu çalıştır
compress_xml_to_gz(input_file, output_file)
