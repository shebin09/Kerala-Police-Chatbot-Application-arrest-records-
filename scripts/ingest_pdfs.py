"""
Usage:
python scripts/ingest_pdfs.py
"""
import os
import json
from pathlib import Path
from tqdm import tqdm
from src.pdf_extract import extract_text_pdf
from src.pii_redact import find_spans, redact
from src.metadata_parse import parse_metadata
from src.chunker import chunks_from_pages
from src.io_utils import append_jsonl, write_jsonl
from src.config import RAW_PDF_DIR, PROCESSED_DIR, CHUNKS_FILE, META_FILE

def process_pdf_file(path):
    filename = Path(path).name
    out_meta = {"filename": filename}
    extracted = extract_text_pdf(path)
    pages = extracted["pages"]
    full_text = extracted["full_text"]
    # filter: only process if this looks like arrest record — simple heuristic:
    if "arrest" not in full_text.lower() and "arrested" not in full_text.lower() and "u/s" not in full_text.lower():
        # optionally skip non-arrest documents
        return None, None

    meta = parse_metadata(full_text)
    out_meta.update(meta)
    out_meta["raw_text_excerpt"] = full_text[:500]

    # PII detection + redact per page
    redacted_pages = []
    for p in pages:
        spans = find_spans(p["text"])
        red_text = redact(p["text"], spans)
        redacted_pages.append({"page_no": p["page_no"], "text": red_text})

    # chunk into pieces
    chunk_objs = chunks_from_pages(redacted_pages, filename, out_meta)
    return out_meta, chunk_objs

def main():
    in_dir = Path(RAW_PDF_DIR)
    all_metas = []
    # make sure empty files are not processed
    if not in_dir.exists():
        print("No raw pdf dir found:", in_dir)
        return

    # remove previous files
    if CHUNKS_FILE.exists(): CHUNKS_FILE.unlink()
    if META_FILE.exists(): META_FILE.unlink()

    for pdf in tqdm(list(in_dir.glob("*.pdf"))):
        meta, chunks = process_pdf_file(pdf)
        if meta is None:
            # skipped
            continue
        append_jsonl(META_FILE, meta)
        for c in chunks:
            append_jsonl(CHUNKS_FILE, c)

    print("Ingest complete. Chunks and metadata saved to processed folder.")

if __name__ == "__main__":
    main()
