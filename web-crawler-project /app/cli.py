from .crawler import Crawler
from .index import Index
from .search import SearchEngine

def run_cli():
    index = Index()
    crawler = Crawler()
    search_engine = SearchEngine(index)

    while True:
        cmd = input("\n> ").strip()

        if cmd.startswith("index"):
            parts = cmd.split(maxsplit=2)  # sadece ilk 3 parçayı al
            if len(parts) != 3:
                print("Usage: index <url> <depth>")
                continue
            _, url, depth = parts
            try:
                depth = int(depth)
            except ValueError:
                print("Depth must be an integer")
                continue
            crawler.start(url, depth, index)
            print("Indexing started...")

        elif cmd.startswith("search"):
            parts = cmd.split(maxsplit=1)
            if len(parts) != 2:
                print("Usage: search <query>")
                continue
            _, query = parts
            results = search_engine.search(query)
            for r in results[:10]:
                print(r)

        elif cmd == "status":
            print(f"Visited: {len(crawler.visited)}")
            print(f"Queue size: {crawler.queue.qsize()}")
            print(f"Indexed docs: {len(index.data)}")

        elif cmd == "exit":
            crawler.stop()
            print("Stopping...")
            break

        else:
            print("Commands:")
            print(" index <url> <depth>")
            print(" search <query>")
            print(" status")
            print(" exit")