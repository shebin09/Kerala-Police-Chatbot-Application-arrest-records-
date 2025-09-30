import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from pathlib import Path
from .config import EMBEDDING_MODEL, FAISS_INDEX_FILE, DOCS_FILE
import os

def build_embeddings_and_index(chunks_iterable, model_name=EMBEDDING_MODEL):
    """
    chunks_iterable: iterable/list of chunk dicts (with 'text' field)
    saves FAISS index and documents numpy
    """
    model = SentenceTransformer(model_name)
    texts = [c["text"] for c in chunks_iterable]
    # keep full chunk objects as docs
    docs = chunks_iterable
    if not texts:
        raise ValueError("No texts to embed")
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings, dtype='float32'))
    Path(FAISS_INDEX_FILE).parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(FAISS_INDEX_FILE))
    np.save(str(DOCS_FILE), np.array(docs, dtype=object))
    print(f"Saved FAISS index to {FAISS_INDEX_FILE} and docs to {DOCS_FILE}")

def load_index_and_docs():
    idx = faiss.read_index(str(FAISS_INDEX_FILE))
    docs = np.load(str(DOCS_FILE), allow_pickle=True)
    return idx, docs
