# cli.py
import threading
from app.index import Index

def print_index(index):
    print("\n--- Indexed Documents ---")
    with index.lock:
        for url, doc in index.data.items():
            token_count = len(doc.get("tokens", []))
            print(f"{url} -> {token_count} tokens")
    print("------------------------\n")

def run_cli():
    index = Index()
    queue = []
    visited = set()

    def index_url(url, depth):
        if url in visited:
            return
        visited.add(url)
        index.add_document(url, f"Content of {url}", url, depth)
        print(f"Indexed {url} with depth {depth}")

    print("> Simple Web Crawler CLI")
    while True:
        try:
            command_line = input("> ").strip()
            if not command_line:
                continue
            parts = command_line.split()
            command = parts[0].lower()

            if command == "index" and len(parts) >= 3:
                url = parts[1]
                depth = int(parts[2])
                threading.Thread(target=index_url, args=(url, depth)).start()
                print("Indexing started in background...")

            elif command == "status":
                print(f"Visited: {len(visited)}")
                print(f"Queue size: {len(queue)}")
                print(f"Indexed docs: {len(index.data)}")

            elif command == "list_index":
                print_index(index)

            elif command == "exit":
                print("Stopping...")
                break

            else:
                print("Unknown command. Use: index <url> <depth>, status, list_index, exit")

        except Exception as e:
            print(f"Error: {e}")