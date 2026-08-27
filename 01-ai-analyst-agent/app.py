"""
AI Data Analyst Agent — app.py
Ask business questions in natural language and get instant charts + insights.
Run: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="DataGPT — AI Analyst Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; color: #2c2825 !important; }
[data-testid="stAppViewContainer"] { background-color: #fbfaf7 !important; }
[data-testid="stSidebar"] { background-color: #f4f1ea !important; border-right: 1px solid #e5dfd3 !important; }
.user-bubble { background-color: #f0ebe4; border: 1px solid #dfd8cb; border-radius: 16px; padding: 14px 18px; margin: 12px 0; color: #2c2825; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
.agent-bubble { background-color: #f5f3ff; border: 1px solid #e0dbff; border-radius: 16px; padding: 14px 18px; margin: 12px 0; color: #2c2825; box-shadow: 0 2px 5px rgba(0,0,0,0.02); }
.stButton>button { background: #6366f1 !important; color: white !important; font-weight: 600 !important; border: none !important; border-radius: 8px !important; padding: 8px 24px !important; transition: 0.2s; }
.stButton>button:hover { background: #4f46e5 !important; transform: translateY(-1px); }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.image("images/agent_3d_brain.jpg", use_container_width=True)
    st.markdown("## 🤖 DataGPT")
    st.markdown("*AI-Powered Data Analyst Agent*")
    st.divider()

    openai_key = st.text_input("OpenAI API Key (optional)", type="password", placeholder="sk-...")
    st.caption("Leave blank for demo mode with pre-generated insights.")
    demo_mode = not bool(openai_key)
    if demo_mode:
        st.info("🎭 Demo mode active")
    st.divider()

    # Voice Query Input
    audio_file = st.audio_input("🎙️ Speak your question")
    if audio_file is not None:
        audio_bytes = audio_file.read()
        if "last_audio" not in st.session_state or st.session_state.last_audio != audio_bytes:
            st.session_state.last_audio = audio_bytes
            if not demo_mode:
                try:
                    import openai
                    client = openai.OpenAI(api_key=openai_key)
                    with open("temp_audio.wav", "wb") as f:
                        f.write(audio_bytes)
                    with open("temp_audio.wav", "rb") as f:
                        transcript = client.audio.transcriptions.create(
                            model="whisper-1",
                            file=f
                        )
                    st.session_state.pending = transcript.text
                    import os
                    os.remove("temp_audio.wav")
                except Exception as e:
                    st.error(f"Voice transcription error: {str(e)}")
            else:
                st.session_state.pending = "Show monthly revenue trend"
            st.rerun()

    st.divider()
    st.markdown("**📊 Actions**")
    if st.button("📊 Show Data Profile Report"):
        st.session_state.show_profile = True
        st.rerun()

    if st.button("🔄 Reset Conversation"):
        st.session_state.chat = []
        if "show_profile" in st.session_state:
            del st.session_state.show_profile
        st.rerun()

# ── Load data ──────────────────────────────────────────────────────────────────
from agent.tools import load_data, run_query
from agent.prompts import build_prompt, DEMO_ANSWERS

@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── Session state ──────────────────────────────────────────────────────────────
if "chat" not in st.session_state:
    st.session_state.chat = []

# ── Main UI ────────────────────────────────────────────────────────────────────
st.markdown("# 🤖 DataGPT — Ask Your Data Anything")
st.markdown("Type a business question below. The AI agent will query the dataset, build a chart, and write insights.")
st.divider()

# ── Dataset preview & profiling ────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📋 Dataset Preview", "📊 Data Profile & Stats"])

with tab1:
    st.dataframe(df.head(20), use_container_width=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Orders",   f"{len(df):,}")
    c2.metric("Total Revenue",  f"${df['revenue'].sum():,.0f}")
    c3.metric("Avg Order Value",f"${df['revenue'].mean():.0f}")
    c4.metric("Products",       df['product_category'].nunique())

with tab2:
    st.markdown("### 📊 Automated Statistical Profile")
    stats_df = df.describe(include='all').T.fillna('-')
    st.dataframe(stats_df, use_container_width=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Null Value Counts:**")
        nulls = df.isnull().sum().reset_index()
        nulls.columns = ["Column", "Null Count"]
        st.dataframe(nulls, use_container_width=True, height=220)
    with col_b:
        st.markdown("**Data Types & Unique Values:**")
        uniques = pd.DataFrame({
            "Dtype": df.dtypes.astype(str),
            "Uniques": df.nunique()
        })
        st.dataframe(uniques, use_container_width=True, height=220)

# ── Suggested questions ────────────────────────────────────────────────────────
st.markdown("### 💡 Quick Questions")
suggestions = [
    "📈 Show monthly revenue trend",
    "🏆 Which product category makes most revenue?",
    "🔮 Show 3D Sales Scatter",
    "🌍 Top 5 countries by sales",
    "👥 What's the average order value by customer segment?",
    "🔄 What is the refund rate by category?",
]
cols = st.columns(3)
for i, (col, sug) in enumerate(zip(cols * 2, suggestions)):
    if col.button(sug, key=f"q{i}"):
        st.session_state.pending = sug.split(" ",1)[1]
        st.rerun()

st.divider()

# ── Chat history ───────────────────────────────────────────────────────────────
for idx, turn in enumerate(st.session_state.chat):
    st.markdown(f"<div class='user-bubble'>🧑 <strong>You:</strong> {turn['question']}</div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='agent-bubble'>🤖 <strong>DataGPT:</strong> {turn['insight']}</div>",
                unsafe_allow_html=True)
    if turn.get("fig"):
        st.plotly_chart(turn["fig"], use_container_width=True, key=f"chart_{idx}")
    if turn.get("table") is not None:
        st.dataframe(turn["table"], use_container_width=True, height=200, key=f"table_{idx}")

# ── Question input ─────────────────────────────────────────────────────────────
question = st.chat_input("Ask a business question about your data…")
if hasattr(st.session_state, "pending"):
    question = st.session_state.pending
    del st.session_state.pending

if question:
    with st.spinner("🧠 Agent analysing data…"):
        result = run_query(df, question, demo_mode=demo_mode, api_key=openai_key or None)
    st.session_state.chat.append({"question": question, **result})
    st.rerun()
