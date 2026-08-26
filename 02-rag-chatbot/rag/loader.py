"""Document loader — supports PDF, TXT, DOCX."""
import re
from typing import List

def load_documents(uploaded_files) -> List[dict]:
    """Load and chunk uploaded Streamlit file objects."""
    all_docs = []
    for f in uploaded_files:
        ext  = f.name.split('.')[-1].lower()
        text = ""
        try:
            if ext == "txt":
                text = f.read().decode("utf-8", errors="ignore")
            elif ext == "pdf":
                import io
                try:
                    import pypdf
                    reader = pypdf.PdfReader(io.BytesIO(f.read()))
                    text   = "\n".join(p.extract_text() or "" for p in reader.pages)
                except ImportError:
                    text = f.read().decode("utf-8", errors="ignore")
            elif ext == "docx":
                import io
                try:
                    from docx import Document
                    doc  = Document(io.BytesIO(f.read()))
                    text = "\n".join(p.text for p in doc.paragraphs)
                except ImportError:
                    text = f.read().decode("utf-8", errors="ignore")
        except Exception:
            continue

        if text.strip():
            chunks = text_to_docs(text, source=f.name)
            all_docs.extend(chunks)

    return all_docs


def text_to_docs(text: str, source: str = "document", chunk_size: int = 500, overlap: int = 80) -> List[dict]:
    """Split text into overlapping chunks."""
    text   = re.sub(r'\n{3,}', '\n\n', text.strip())
    words  = text.split()
    chunks = []
    start  = 0
    while start < len(words):
        end   = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append({"text": chunk, "source": source, "chunk_id": len(chunks)})
        start += chunk_size - overlap
    return chunks
