import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
RAW_PDF_DIR = DATA_DIR / "raw_pdfs"
PROCESSED_DIR = DATA_DIR / "processed"
INDEX_DIR = DATA_DIR / "index"

# file names
CHUNKS_FILE = PROCESSED_DIR / "chunks.jsonl"
META_FILE = PROCESSED_DIR / "metadata.jsonl"
FAISS_INDEX_FILE = INDEX_DIR / "faiss_index.bin"
DOCS_FILE = INDEX_DIR / "documents.npy"

# extraction options
OCR_LANG = "eng"  # change if you have MAL or other
OCR_CONFIDENCE_THRESHOLD = 0.0

# chunking
CHUNK_SIZE_WORDS = 350
CHUNK_OVERLAP = 50

# embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOP_K = 5

# create dirs
for d in [RAW_PDF_DIR, PROCESSED_DIR, INDEX_DIR]:
    d.mkdir(parents=True, exist_ok=True)
