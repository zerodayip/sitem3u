import httpx

url = "https://daddylive.mp/schedule/schedule.html"
output_file = "schedule.html"

# httpx ile HTTP isteği gönderiyoruz
with httpx.Client() as client:
    response = client.get(url)
    
    if response.status_code == 200:
        # HTML içeriğini kaydediyoruz
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"{output_file} başarıyla kaydedildi.")
        
        # HTML içeriğini ekrana yazdırıyoruz
        print("\nHTML İçeriği:")
        print(response.text[:1000])  # İlk 1000 karakteri ekrana yazdırıyoruz
    else:
        print(f"İstek başarısız oldu. Hata kodu: {response.status_code}")
