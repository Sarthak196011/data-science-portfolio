"""FastAPI Backend Server for DocMind 3D Knowledge Retrieval Engine."""
import os
import sys
import shutil
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rag.loader import load_documents
from rag.embedder import build_vectorstore, retrieve
from rag.chain import answer_question

app = FastAPI(
    title="DocMind 3D — Neural Document Intelligence API",
    description="High-precision local RAG engine with 3D latent vector retrieval.",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global in-memory storage for active document vector stores
GLOBAL_STORE = {
    "vectorstore": None,
    "doc_names": [],
    "total_chunks": 0,
    "status": "ready"
}

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 4
    api_key: Optional[str] = ""

class MockUploadedFile:
    def __init__(self, name: str, data: bytes):
        self.name = name
        self._data = data
    def getbuffer(self):
        return self._data
    def read(self):
        return self._data

@app.get("/api/health")
async def health():
    return {
        "status": "online",
        "service": "DocMind Neural 3D RAG",
        "indexed_docs": GLOBAL_STORE["doc_names"],
        "total_chunks": GLOBAL_STORE["total_chunks"]
    }

@app.post("/api/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided.")

    mock_files = []
    for f in files:
        content = await f.read()
        mock_files.append(MockUploadedFile(f.filename, content))

    try:
        chunks = load_documents(mock_files)
        if not chunks:
            raise HTTPException(status_code=400, detail="No readable text could be extracted.")

        vstore = build_vectorstore(tuple(chunks))
        GLOBAL_STORE["vectorstore"] = vstore
        GLOBAL_STORE["doc_names"] = [f.filename for f in files]
        GLOBAL_STORE["total_chunks"] = len(chunks)

        return {
            "success": True,
            "message": f"Successfully indexed {len(files)} document(s) into {len(chunks)} neural chunks.",
            "doc_names": GLOBAL_STORE["doc_names"],
            "total_chunks": len(chunks)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing error: {str(e)}")

@app.get("/api/sample")
async def load_sample():
    sample_path = os.path.join(os.path.dirname(__file__), "sample_docs", "sample_report.txt")
    if not os.path.exists(sample_path):
        raise HTTPException(status_code=404, detail="Sample report not found.")

    with open(sample_path, "rb") as f:
        data = f.read()

    mock_file = MockUploadedFile("sample_report.txt", data)
    chunks = load_documents([mock_file])
    vstore = build_vectorstore(tuple(chunks))
    GLOBAL_STORE["vectorstore"] = vstore
    GLOBAL_STORE["doc_names"] = ["sample_report.txt"]
    GLOBAL_STORE["total_chunks"] = len(chunks)

    return {
        "success": True,
        "message": "Loaded enterprise sample document (Autonomous AI Systems & Ethics Whitepaper).",
        "doc_names": ["sample_report.txt"],
        "total_chunks": len(chunks)
    }

@app.post("/api/query")
async def query_documents(payload: QueryRequest):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Auto-load sample if no vectorstore present
    if GLOBAL_STORE["vectorstore"] is None:
        sample_path = os.path.join(os.path.dirname(__file__), "sample_docs", "sample_report.txt")
        if os.path.exists(sample_path):
            with open(sample_path, "rb") as f:
                mock_file = MockUploadedFile("sample_report.txt", f.read())
            chunks = load_documents([mock_file])
            GLOBAL_STORE["vectorstore"] = build_vectorstore(tuple(chunks))
            GLOBAL_STORE["doc_names"] = ["sample_report.txt"]
            GLOBAL_STORE["total_chunks"] = len(chunks)

    vstore = GLOBAL_STORE["vectorstore"]
    if vstore is None:
        raise HTTPException(status_code=400, detail="No documents indexed. Please upload a document first.")

    try:
        answer, sources = answer_question(
            question=payload.query,
            vectorstore=vstore,
            api_key=payload.api_key or os.environ.get("OPENAI_API_KEY", ""),
            top_k=payload.top_k or 4,
            demo_mode=not bool(payload.api_key or os.environ.get("OPENAI_API_KEY", ""))
        )

        # Retrieve raw chunks for citation verification
        relevant_chunks = retrieve(vstore, payload.query, top_k=payload.top_k or 4)
        snippets = [{"source": c.get("source", "Doc"), "text": c.get("text", "")[:280]} for c in relevant_chunks]

        return {
            "answer": answer,
            "sources": sources,
            "snippets": snippets,
            "docs_searched": GLOBAL_STORE["doc_names"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution error: {str(e)}")

# Mount static frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8502, reload=True)
