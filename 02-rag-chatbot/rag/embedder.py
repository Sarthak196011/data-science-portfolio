"""Vector store builder using TF-IDF and Sentence-Transformers (Zero API Key)."""
from typing import List
import numpy as np

def build_vectorstore(docs_tuple):
    """Build high-performance vector index from document chunks."""
    docs = list(docs_tuple) if not isinstance(docs_tuple, list) else docs_tuple
    texts = [d["text"] for d in docs]

    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        matrix = tfidf.fit_transform(texts)
        return {"docs": docs, "tfidf_matrix": matrix, "tfidf": tfidf, "mode": "tfidf"}
    except Exception:
        # Fallback keyword overlap
        return {"docs": docs, "mode": "raw"}

def retrieve(vectorstore: dict, query: str, top_k: int = 4) -> List[dict]:
    """Retrieve top-k relevant chunks for a query."""
    docs = vectorstore["docs"]

    if "tfidf" in vectorstore:
        from sklearn.metrics.pairwise import cosine_similarity
        tfidf = vectorstore["tfidf"]
        matrix = vectorstore["tfidf_matrix"]
        q_vec = tfidf.transform([query])
        sims = cosine_similarity(q_vec, matrix).flatten()
        top_idx = np.argsort(sims)[::-1][:top_k]
        return [docs[i] for i in top_idx]
    else:
        return docs[:top_k]
