import threading
from queue import Queue
from urllib.request import urlopen
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for (key, value) in attrs:
                if key == "href":
                    self.links.append(value)

class Crawler:
    def __init__(self, max_queue_size=1000, worker_count=5):
        self.visited = set()
        self.visited_lock = threading.Lock()
        self.queue = Queue(maxsize=max_queue_size)
        self.worker_count = worker_count
        self.running = False

    def fetch(self, url):
        try:
            with urlopen(url, timeout=5) as response:
                return response.read().decode("utf-8", errors="ignore")
        except:
            return ""

    def extract_links(self, html, base_url):
        parser = LinkParser()
        parser.feed(html)
        links = []
        for link in parser.links:
            absolute = urljoin(base_url, link)
            if urlparse(absolute).scheme in ("http", "https"):
                links.append(absolute)
        return links

    def worker(self, indexer):
        while self.running:
            try:
                url, origin, depth, max_depth = self.queue.get(timeout=1)
            except:
                continue

            if depth > max_depth:
                self.queue.task_done()
                continue

            with self.visited_lock:
                if url in self.visited:
                    self.queue.task_done()
                    continue
                self.visited.add(url)

            html = self.fetch(url)
            indexer.add_document(url, html, origin, depth)

            links = self.extract_links(html, url)
            for link in links:
                try:
                    self.queue.put((link, origin, depth + 1, max_depth), timeout=1)
                except:
                    pass

            self.queue.task_done()

    def start(self, origin, max_depth, indexer):
        self.running = True
        self.queue.put((origin, origin, 0, max_depth))

        threads = []
        for _ in range(self.worker_count):
            t = threading.Thread(target=self.worker, args=(indexer,))
            t.daemon = True
            t.start()
            threads.append(t)

        return threads

    def stop(self):
        self.running = False
