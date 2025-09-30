from .embeddings_index import load_index_and_docs
from sentence_transformers import SentenceTransformer
import numpy as np

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class Searcher:
    def __init__(self):
        self.index, self.docs = load_index_and_docs()
        self.model = SentenceTransformer(MODEL_NAME)

    def query(self, text, top_k=5):
        q_emb = self.model.encode([text], convert_to_numpy=True)
        D, I = self.index.search(q_emb, top_k)
        results = []
        for idx, dist in zip(I[0], D[0]):
            if idx < 0:
                continue
            doc = self.docs[idx].item() if hasattr(self.docs[idx], "item") else self.docs[idx]
            summary = {
                "score": float(dist),
                "source": doc["source"],
                "page": doc["page"],
                "chunk_id": doc["chunk_id"],
                "snippet": doc["text"][:400],
                "metadata": doc.get("metadata", {})
            }
            results.append(summary)
        return results

if __name__ == "__main__":
    s = Searcher()
    res = s.query("arrest in mavelikkara", top_k=3)
    import pprint; pprint.pprint(res)
