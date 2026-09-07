"""Document loader — robust extraction for PDF, TXT, and DOCX without raw binary fallbacks."""
import io
import re
import zipfile
import xml.etree.ElementTree as ET
from typing import List

def extract_text_from_file(f) -> str:
    """Safely extract plain text from uploaded Streamlit file object."""
    try:
        f.seek(0)
    except Exception:
        pass
    data = f.read()
    ext = f.name.split('.')[-1].lower()

    if ext == "txt":
        return data.decode("utf-8", errors="ignore")

    elif ext == "docx":
        # 1. Try python-docx
        try:
            import docx
            doc = docx.Document(io.BytesIO(data))
            parts = []
            for p in doc.paragraphs:
                txt = p.text.strip()
                if txt:
                    parts.append(txt)
            for table in doc.tables:
                for row in table.rows:
                    row_txt = " | ".join(c.text.strip() for c in row.cells if c.text.strip())
                    if row_txt:
                        parts.append(row_txt)
            text = "\n\n".join(parts)
            if text.strip():
                return text
        except Exception:
            pass

        # 2. Native ZIP + XML fallback (standard library, zero external dependency)
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as zf:
                if 'word/document.xml' in zf.namelist():
                    xml_bytes = zf.read('word/document.xml')
                    tree = ET.fromstring(xml_bytes)
                    paragraphs = []
                    for elem in tree.iter():
                        if elem.tag.endswith('}p'):
                            texts = [t.text for t in elem.iter() if t.tag.endswith('}t') and t.text]
                            if texts:
                                line = "".join(texts).strip()
                                if line:
                                    paragraphs.append(line)
                    text = "\n\n".join(paragraphs)
                    if text.strip():
                        return text
        except Exception:
            pass

        return ""

    elif ext == "pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(data))
            pages_text = []
            for page in reader.pages:
                txt = page.extract_text()
                if txt and txt.strip():
                    pages_text.append(txt.strip())
            return "\n\n".join(pages_text)
        except Exception:
            pass
        return ""

    return ""

def load_documents(uploaded_files) -> List[dict]:
    """Load and chunk uploaded Streamlit file objects."""
    all_docs = []
    for f in uploaded_files:
        try:
            text = extract_text_from_file(f)
        except Exception as e:
            text = ""

        # Filter out accidental binary data
        if text.startswith("PK\x03\x04") or "\x00" in text[:100]:
            text = ""

        if text and text.strip():
            chunks = text_to_docs(text, source=f.name)
            all_docs.extend(chunks)

    return all_docs

def text_to_docs(text: str, source: str = "document", chunk_size: int = 500, overlap: int = 80) -> List[dict]:
    """Split text into clean, overlapping paragraph/word chunks."""
    # Normalize whitespace while preserving paragraphs
    text = re.sub(r'\r\n', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text.strip())
    
    # Split by paragraphs first for coherent chunking
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    chunks = []
    current_chunk = []
    current_words = 0
    
    for p in paragraphs:
        words = p.split()
        if not words:
            continue
            
        if current_words + len(words) > chunk_size and current_chunk:
            chunk_text = "\n\n".join(current_chunk)
            chunks.append({"text": chunk_text, "source": source, "chunk_id": len(chunks)})
            # Overlap: keep last paragraph if reasonable
            if len(current_chunk) > 1 and len(current_chunk[-1].split()) < overlap:
                current_chunk = [current_chunk[-1], p]
                current_words = len(current_chunk[0].split()) + len(words)
            else:
                current_chunk = [p]
                current_words = len(words)
        else:
            current_chunk.append(p)
            current_words += len(words)
            
    if current_chunk:
        chunk_text = "\n\n".join(current_chunk)
        chunks.append({"text": chunk_text, "source": source, "chunk_id": len(chunks)})

    # Fallback to word slicing if single giant paragraph
    if not chunks and text.strip():
        words = text.split()
        start = 0
        while start < len(words):
            end = min(start + chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append({"text": chunk, "source": source, "chunk_id": len(chunks)})
            start += max(1, chunk_size - overlap)

    return chunks
