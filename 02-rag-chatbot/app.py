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
html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; color: #37352f !important; }
[data-testid="stAppViewContainer"] { background-color: #fcfcfc !important; }
[data-testid="stSidebar"] { background-color: #f7f7f7 !important; border-right: 1px solid #edece9 !important; }
.chat-msg-user { background-color: #f1f1f0; border: none; border-radius: 12px; padding: 14px; margin: 10px 0; color: #37352f; }
.chat-msg-bot  { background-color: #fdf6e2; border: 1px solid #f5ebd0; border-radius: 12px; padding: 14px; margin: 10px 0; color: #37352f; }
.source-badge  { background-color: #e2f5ec; border: 1px solid #bcead3; border-radius: 6px; padding: 4px 10px; font-size: 0.78rem; color: #0f7b47; display: inline-block; margin: 3px; font-weight: 600; }
.stButton>button { background: #df7b00 !important; color: white !important; font-weight: 600 !important; border: none !important; border-radius: 6px !important; padding: 8px 20px !important; transition: 0.2s; }
.stButton>button:hover { background: #c66c00 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image(os.path.join(os.path.dirname(__file__), "images", "rag_3d_library.jpg"), use_container_width=True)
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
    st.markdown("**🗣️ Language Settings**")
    chat_lang = st.selectbox("Select Chat Language", ["English", "Spanish", "French", "Hindi", "German"])

    st.divider()
    st.markdown("**💾 Session Manager**")
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}
    
    if st.button("💾 Save Current Chat"):
        if st.session_state.messages:
            s_name = f"Session {len(st.session_state.sessions) + 1} ({len(st.session_state.messages)} turns)"
            st.session_state.sessions[s_name] = st.session_state.messages.copy()
            st.session_state.messages = []
            st.success(f"Saved: {s_name}")
            st.rerun()
        else:
            st.warning("Chat is empty, nothing to save.")

    if st.session_state.sessions:
        load_s = st.selectbox("📂 Load Saved Chat", ["Select session..."] + list(st.session_state.sessions.keys()))
        if load_s != "Select session...":
            st.session_state.messages = st.session_state.sessions[load_s].copy()
            st.success(f"Loaded: {load_s}")
            st.rerun()

    st.divider()
    if st.button("🗑️ Clear Active Chat"):
        st.session_state.messages = []
        st.session_state.vectorstore = None
        st.rerun()

    st.markdown("**Settings**")
    top_k    = st.slider("Sources to retrieve (k)", 2, 8, 4)
    use_demo = not bool(openai_key)
    if use_demo:
        st.info("🎭 Demo mode active.")

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

# ── Translation Helper ─────────────────────────────────────────────────────────
def translate_text(text: str, target_lang: str, api_key: str = None) -> str:
    if target_lang == "English":
        return text
    if not api_key:
        mocks = {
            "Spanish": f"[Spanish Translation] {text}",
            "French": f"[French Translation] {text}",
            "Hindi": f"[Hindi Translation] {text}",
            "German": f"[German Translation] {text}",
        }
        return mocks.get(target_lang, f"[{target_lang}] {text}")
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"Translate the following text to {target_lang}. Return ONLY the direct translation, no extra notes."},
                {"role": "user", "content": text}
            ],
            max_tokens=400, temperature=0.2
        )
        return resp.choices[0].message.content
    except Exception:
        return f"[{target_lang}] {text}"

def translate_to_english(text: str, source_lang: str, api_key: str = None) -> str:
    if source_lang == "English":
        return text
    if not api_key:
        return text # fallback to english directly in mock
    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Translate the following text to English. Return ONLY the direct translation, no extra notes."},
                {"role": "user", "content": text}
            ],
            max_tokens=400, temperature=0.2
        )
        return resp.choices[0].message.content
    except Exception:
        return text

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
            # Translate query to English if needed
            eng_question = translate_to_english(question, chat_lang, openai_key if openai_key else None)
            
            answer, sources = answer_question(
                eng_question,
                st.session_state.vectorstore,
                api_key=openai_key if openai_key else None,
                top_k=top_k,
                demo_mode=use_demo,
            )
            
            # Translate answer back to user's selected language
            if chat_lang != "English":
                answer = translate_text(answer, chat_lang, openai_key if openai_key else None)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })
    st.rerun()
