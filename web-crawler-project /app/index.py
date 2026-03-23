# app/index.py
import threading
import re
import os

class Index:
    def __init__(self):
        self.data = {}         
        self.lock = threading.Lock()

    def tokenize(self, text):
        """Metni kelimelere ayırır ve küçük harfe çevirir"""
        return re.findall(r"\w+", text.lower())

    def add_document(self, url, html, origin, depth):
        """Yeni bir dokümanı index'e ekler"""
        tokens = self.tokenize(html)
        with self.lock:
            self.data[url] = {
                "content": html,   
                "tokens": tokens,
                "origin": origin,
                "depth": depth
            }

    def save_to_file(self, filepath="data/storage/p.data"):
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with self.lock:
            with open(filepath, "w", encoding="utf-8") as f:
                for url, doc in self.data.items():
                    words = doc["content"].split()
                    word_counts = {}
                    for w in words:
                        w_clean = w.lower().strip(".,!?:;()[]{}\"'")
                        if w_clean:
                            word_counts[w_clean] = word_counts.get(w_clean, 0) + 1
                    for word, freq in word_counts.items():
                        line = f"{word} {url} {doc['origin']} {doc['depth']} {freq}\n"
                        f.write(line)
        print(f"[INFO] Index saved to {filepath}")