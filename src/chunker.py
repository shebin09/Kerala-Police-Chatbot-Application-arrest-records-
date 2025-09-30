from typing import List, Dict
from .config import CHUNK_SIZE_WORDS, CHUNK_OVERLAP

def chunk_text(text: str, chunk_size=CHUNK_SIZE_WORDS, overlap=CHUNK_OVERLAP):
    tokens = text.split()
    chunks = []
    if len(tokens) <= chunk_size:
        return [{"chunk_id": 0, "text": text}]
    
    i = 0
    chunk_id = 0
    while i < len(tokens):
        seg = tokens[i:i+chunk_size]
        chunks.append({"chunk_id": chunk_id, "text": " ".join(seg)})
        chunk_id += 1
        i += chunk_size - overlap
    return chunks

def chunks_from_pages(pages: List[Dict], filename: str, meta: Dict):
    out = []
    for p in pages:
        page_no = p["page_no"]
        raw_text = p["text"]
        chs = chunk_text(raw_text)
        for c in chs:
            out.append({
                "id": f"{filename}::p{page_no}::c{c['chunk_id']}",
                "source": filename,
                "page": page_no,
                "chunk_id": c["chunk_id"],
                "text": c["text"],
                "metadata": meta
            })
    return out
