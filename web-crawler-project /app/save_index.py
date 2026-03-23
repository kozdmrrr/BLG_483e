from app.index import Index

# Index sınıfını başlatıyoruz
index = Index()

# 1. Kayıt: 'python' kelimesi 3 kez geçiyor, derinlik 1
# Beklenen skor: (3 * 10) + 1000 - (1 * 5) = 1025
index.add_document(
    "https://www.python.org", 
    "python python python programming language official site", 
    "https://www.python.org", 
    1
)

# 2. Kayıt: 'python' kelimesi 1 kez geçiyor, derinlik 2
# Beklenen skor: (1 * 10) + 1000 - (2 * 5) = 1000
index.add_document(
    "https://docs.python.org", 
    "python documentation guide reference", 
    "https://docs.python.org", 
    2
)

# 3. Kayıt: 'python' kelimesi 5 kez geçiyor, derinlik 3
# Beklenen skor: (5 * 10) + 1000 - (3 * 5) = 1035 (En yüksek bu çıkmalı!)
index.add_document(
    "https://www.python.org/community/", 
    "python python python python python community events and people", 
    "https://www.python.org/community/", 
    3
)

# Verileri dosyaya kaydediyoruz
index.save_to_file("data/storage/p.data")

print("Veriler başarıyla farklı değerlerle kaydedildi!")
print("Şimdi 'p.data' dosyasını kontrol edebilirsin.")