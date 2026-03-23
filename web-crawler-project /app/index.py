import threading
import re

class Index:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def tokenize(self, text):
        return re.findall(r"\w+", text.lower())

    def add_document(self, url, html, origin, depth):
        tokens = self.tokenize(html)
        with self.lock:
            self.data[url] = {
                "tokens": tokens,
                "origin": origin,
                "depth": depth
            }
