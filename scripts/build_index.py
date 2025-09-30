"""
Usage:
python scripts/build_index.py
"""
import json
from pathlib import Path
from src.io_utils import read_jsonl
from src.embeddings_index import build_embeddings_and_index
from src.config import CHUNKS_FILE

def main():
    chunks = [c for c in read_jsonl(CHUNKS_FILE)]
    if not chunks:
        print("No chunks found. Run ingest first.")
        return
    build_embeddings_and_index(chunks)
    print("Index build finished.")

if __name__ == "__main__":
    main()
