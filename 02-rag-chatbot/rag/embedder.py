"""Vector store builder using sentence-transformers + FAISS (free, no API key)."""
from typing import List
import numpy as np
import streamlit as st

@st.cache_resource(show_spinner="🔢 Building embeddings…")
def build_vectorstore(docs_tuple):
    """Build FAISS index from document chunks."""
    docs = list(docs_tuple) if not isinstance(docs_tuple, list) else docs_tuple
    try:
        from sentence_transformers import SentenceTransformer
        model  = SentenceTransformer('all-MiniLM-L6-v2')
        texts  = [d["text"] for d in docs]
        embeds = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        return {"docs": docs, "embeddings": embeds, "model": model}
    except Exception:
        # Ultra-lightweight fallback: TF-IDF similarity
        from sklearn.feature_extraction.text import TfidfVectorizer
        texts  = [d["text"] for d in docs]
        tfidf  = TfidfVectorizer(max_features=5000, stop_words='english')
        matrix = tfidf.fit_transform(texts)
        return {"docs": docs, "tfidf_matrix": matrix, "tfidf": tfidf, "mode": "tfidf"}


def retrieve(vectorstore: dict, query: str, top_k: int = 4) -> List[dict]:
    """Retrieve top-k relevant chunks for a query."""
    docs = vectorstore["docs"]

    if "model" in vectorstore:
        # Sentence-transformer retrieval
        model      = vectorstore["model"]
        embeddings = vectorstore["embeddings"]
        q_emb      = model.encode([query], convert_to_numpy=True)
        # Cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        q_norm = np.linalg.norm(q_emb)
        sims   = (embeddings @ q_emb.T).flatten() / (norms.flatten() * q_norm + 1e-9)
        top_idx = np.argsort(sims)[::-1][:top_k]
        return [docs[i] for i in top_idx]

    else:
        # TF-IDF fallback
        from sklearn.metrics.pairwise import cosine_similarity
        tfidf  = vectorstore["tfidf"]
        matrix = vectorstore["tfidf_matrix"]
        q_vec  = tfidf.transform([query])
        sims   = cosine_similarity(q_vec, matrix).flatten()
        top_idx = np.argsort(sims)[::-1][:top_k]
        return [docs[i] for i in top_idx]
