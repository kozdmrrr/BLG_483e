from app.index import Index

index = Index()
index.add_document("https://example.com", "Content of example.com", "https://example.com", 1)
index.add_document("https://example.org", "Content of example.org", "https://example.org", 1)
index.add_document("https://example.net", "Content of example.net", "https://example.net", 1)

# Storage dosyasını oluştur
index.save_to_file("data/storage/p.data")
print("Storage file created: data/storage/p.data")

# Eklenen URL’leri terminale yazdır
for url, doc in index.data.items():
    print(f"{url} -> {len(doc['tokens'])} tokens")