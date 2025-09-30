import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import faiss, numpy as np, pandas as pd, torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from src.config import INDEX_DIR, FAISS_INDEX_FILE, DOCS_FILE

# =====================
# Load Index + Model
# =====================
@st.cache_resource
def load_index_and_model():
    index = faiss.read_index(str(FAISS_INDEX_FILE))
    docs = np.load(str(DOCS_FILE), allow_pickle=True)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return index, docs, model

index, docs, model = load_index_and_model()

# =====================
# Helper: MMR for diverse results
# =====================
def mmr(query_embedding, doc_embeddings, doc_ids, top_k=5, diversity=0.7):
    query_embedding = torch.tensor(query_embedding)
    doc_embeddings = torch.tensor(doc_embeddings)

    sim_query_doc = cos_sim(query_embedding, doc_embeddings)[0]
    sim_doc_doc = cos_sim(doc_embeddings, doc_embeddings)

    selected, candidates = [], list(range(len(doc_ids)))

    while len(selected) < top_k and candidates:
        if not selected:
            idx = int(torch.argmax(sim_query_doc))
            selected.append(idx)
            candidates.remove(idx)
        else:
            remaining = torch.tensor(candidates)
            sim_to_query = sim_query_doc[remaining]
            sim_to_selected = sim_doc_doc[remaining][:, selected].max(dim=1).values
            mmr_scores = diversity * sim_to_query - (1 - diversity) * sim_to_selected
            idx = candidates[int(torch.argmax(mmr_scores))]
            selected.append(idx)
            candidates.remove(idx)

    return [doc_ids[i] for i in selected]

# =====================
# Query Function
# =====================
def query_dataframe(q, k=5):
    q_emb = model.encode([q], convert_to_numpy=True)

    # Search more candidates from FAISS
    D, I = index.search(q_emb, 30)
    candidate_indices = I[0]

    # Recompute embeddings for candidates
    candidate_texts = [docs[i].item()["text"] if hasattr(docs[i], "item") else docs[i]["text"] 
                       for i in candidate_indices]
    candidate_embeds = model.encode(candidate_texts, convert_to_numpy=True)

    # Apply MMR
    selected_ids = mmr(q_emb, candidate_embeds, candidate_indices, top_k=k)

    # Collect results
    results = []
    for idx in selected_ids:
        doc = docs[idx].item() if hasattr(docs[idx], "item") else docs[idx]
        snippet = doc["text"][:200].replace("\n"," ")
        meta = doc.get("metadata", {})
        results.append({
            "Date": meta.get("date"),
            "Snippet": snippet,
            "Source": doc["source"],
            "Page": doc["page"],
            "Accused Person":meta.get("accused"),
            "Place of incident":meta.get("place"),
            "Sections Involved":meta.get('sections')
        })

    # Deduplicate
    df = pd.DataFrame(results).drop_duplicates(subset=["Snippet"])
    return df


# =====================
# Streamlit UI
# =====================
st.set_page_config(page_title="Arrest Records Assistant", layout="wide")
st.title("🔎 Kerala Police — Arrest Records Assistant")

query = st.text_input("Enter a query (e.g., 'Mavelikkara arrest 2021'):")

if query:
    st.write(f"### Results for: *{query}*")
    df = query_dataframe(query, k=5)
    st.dataframe(df, use_container_width=True)
