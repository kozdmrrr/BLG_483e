class SearchEngine:
    def __init__(self, index):
        self.index = index

    def search(self, query):
        query_tokens = query.lower().split()
        results = []

        with self.index.lock:
            for url, doc in self.index.data.items():
                score = sum(doc["tokens"].count(t) for t in query_tokens)
                if score > 0:
                    results.append((url, doc["origin"], doc["depth"], score))

        results.sort(key=lambda x: x[3], reverse=True)
        return [(r[0], r[1], r[2]) for r in results]
