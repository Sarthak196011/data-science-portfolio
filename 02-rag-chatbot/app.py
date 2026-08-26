"""
RAG Chatbot — app.py
Streamlit chat interface for querying uploaded documents.
Run: streamlit run app.py
"""
import streamlit as st
import os

st.set_page_config(
    page_title="DocMind — RAG Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg,#05050f,#0a0a1a); }
[data-testid="stSidebar"] { background: rgba(255,255,255,0.03) !important; border-right: 1px solid rgba(255,255,255,0.08) !important; }
.chat-msg-user { background: rgba(0,212,255,0.1); border: 1px solid rgba(0,212,255,0.2); border-radius:12px; padding:14px; margin:8px 0; }
.chat-msg-bot  { background: rgba(139,92,246,0.1); border: 1px solid rgba(139,92,246,0.2); border-radius:12px; padding:14px; margin:8px 0; }
.source-badge  { background: rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:6px; padding:4px 10px; font-size:0.78rem; color:#10b981; display:inline-block; margin:3px; }
.stButton>button { background: linear-gradient(135deg,#00d4ff,#8b5cf6) !important; color:white !important; font-weight:700 !important; border:none !important; border-radius:50px !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💬 DocMind RAG")
    st.markdown("*Chat with your documents using AI*")
    st.divider()

    st.markdown("### 📂 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF, TXT, or DOCX files",
        type=["pdf","txt","docx"],
        accept_multiple_files=True,
        help="Your documents are processed locally — nothing is stored on external servers."
    )

    openai_key = st.text_input("OpenAI API Key (optional)", type="password",
                               placeholder="sk-... (leave blank for demo mode)")
    st.caption("🔒 Keys are never stored or logged.")

    st.divider()
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.session_state.vectorstore = None
        st.rerun()

    st.markdown("**Settings**")
    top_k    = st.slider("Sources to retrieve (k)", 2, 8, 4)
    use_demo = not bool(openai_key)
    if use_demo:
        st.info("🎭 Demo mode — realistic mock responses without an API key.")

# ── Session state ──────────────────────────────────────────────────────────────
if "messages"    not in st.session_state: st.session_state.messages    = []
if "vectorstore" not in st.session_state: st.session_state.vectorstore = None
if "doc_names"   not in st.session_state: st.session_state.doc_names   = []

# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("# 💬 DocMind — Chat With Your Documents")
st.markdown("Upload documents, then ask questions. AI answers with citations from your files.")
st.divider()

# ── Document processing ───────────────────────────────────────────────────────
from rag.loader import load_documents
from rag.embedder import build_vectorstore
from rag.chain import answer_question

if uploaded_files:
    new_names = [f.name for f in uploaded_files]
    if new_names != st.session_state.doc_names:
        with st.spinner("📚 Processing documents…"):
            docs = load_documents(uploaded_files)
            if docs:
                st.session_state.vectorstore = build_vectorstore(docs)
                st.session_state.doc_names   = new_names
                st.success(f"✅ Indexed {len(docs)} chunks from {len(uploaded_files)} file(s)")
            else:
                st.error("Could not extract text from the uploaded files.")
else:
    # Auto-load sample doc
    sample_path = os.path.join(os.path.dirname(__file__), 'sample_docs', 'sample_report.txt')
    if os.path.exists(sample_path) and st.session_state.vectorstore is None:
        with st.spinner("📚 Loading sample document…"):
            with open(sample_path, 'r', encoding='utf-8') as f:
                text = f.read()
            from rag.loader import text_to_docs
            docs = text_to_docs(text, source="sample_report.txt")
            st.session_state.vectorstore = build_vectorstore(docs)
            st.session_state.doc_names   = ["sample_report.txt"]
        st.info("📄 Sample document loaded. Upload your own files to replace it.")

# ── Chat history ───────────────────────────────────────────────────────────────
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"""<div class='chat-msg-user'>
            <strong>🧑 You:</strong><br>{msg['content']}</div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class='chat-msg-bot'>
            <strong>🤖 DocMind:</strong><br>{msg['content']}</div>""", unsafe_allow_html=True)
            if msg.get("sources"):
                for src in msg["sources"]:
                    st.markdown(f"<span class='source-badge'>📄 {src}</span>", unsafe_allow_html=True)

# ── Suggested questions ────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("### 💡 Try asking:")
    q_cols = st.columns(3)
    suggestions = [
        "What is the main topic of this document?",
        "Summarize the key findings",
        "What are the recommendations?",
        "List the most important statistics mentioned",
        "What problems does this document address?",
        "What conclusions are drawn?",
    ]
    for i, (col, q) in enumerate(zip(q_cols * 2, suggestions)):
        if col.button(q, key=f"sug_{i}"):
            st.session_state.pending_q = q
            st.rerun()

# ── Input ─────────────────────────────────────────────────────────────────────
question = st.chat_input("Ask anything about your documents…")
if hasattr(st.session_state, 'pending_q'):
    question = st.session_state.pending_q
    del st.session_state.pending_q

if question:
    st.session_state.messages.append({"role":"user","content":question})

    if st.session_state.vectorstore is None:
        answer = "Please upload a document first so I can answer questions about it."
        sources = []
    else:
        with st.spinner("🔍 Searching documents…"):
            answer, sources = answer_question(
                question,
                st.session_state.vectorstore,
                api_key=openai_key if openai_key else None,
                top_k=top_k,
                demo_mode=use_demo,
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })
    st.rerun()
