#  Kerala Police Arrest Records AI Assistant

##  Project Overview
The Kerala Police maintains thousands of arrest records in **unstructured PDF documents**.  
Searching these records manually is slow, error-prone, and sensitive due to **personally identifiable information (PII)**.  

This project builds an **AI-powered semantic search assistant** that:
- Extracts text from 5,000+ arrest record PDFs (with OCR fallback).
- Redacts sensitive PII (names, Aadhaar, addresses, dates).
- Parses structured metadata (Case No, Date, IPC Sections).
- Splits text into searchable chunks.
- Creates vector embeddings using **SentenceTransformers**.
- Stores them in a **FAISS index** for fast retrieval.
- Provides an interactive **Streamlit UI** for querying arrest records.

---


## ⚙️ Installation
Clone repo and install dependencies:
```bash
git clone https://github.com/shebin09/Kerala-Police-Chatbot-Application-arrest-records-
cd arrest-records-ai
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```
▶️ Usage
1. Add PDFs
Place your arrest record PDFs inside:

```bash
data/raw_pdfs/
```
2. Ingest PDFs
Run extraction, redaction, and chunking:


```python
python -m scripts.ingest_pdfs
```
3. Build Index
Generate embeddings and FAISS index:


```python
python -m scripts.build_index
```
4. Run App
Launch Streamlit search assistant:


```python
streamlit run src/app_streamlit.py
```
## Features
* Semantic Search → query by natural language.

* OCR Support → handles scanned PDFs.

* PII Redaction → anonymizes sensitive info.

* FAISS Indexing → fast vector retrieval.

* Interactive UI → user-friendly query interface.

## Progress
* Dataset obtained (5000+ arrest record PDFs)

* Preprocessing + PII Redaction

* Exploratory Data Analysis (EDA)

* Embeddings + FAISS Indexing

* Streamlit UI 

* LLM Summarization (future work → RAG pipeline)

## Tech Stack
* Python 3.10+

* pdfplumber, pytesseract (OCR)

* spaCy (NER for PII redaction)

* SentenceTransformers (all-MiniLM-L6-v2)

* FAISS (vector search)

* Streamlit (UI)

## Future Enhancements
* Integrate LLM summarization for full RAG pipeline.

* Add multilingual support (Malayalam) via Bhashini API.

* Extend metadata extraction for IPC Sections, Police Stations, Districts.

* Deploy as a secure web service for Kerala Police officials.
