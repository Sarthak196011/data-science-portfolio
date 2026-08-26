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
html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg,#05050f,#0a0a1a); }
[data-testid="stSidebar"] { background: rgba(255,255,255,0.03) !important; border-right: 1px solid rgba(255,255,255,0.08) !important; }
.user-bubble { background: rgba(0,212,255,0.08); border:1px solid rgba(0,212,255,0.2); border-radius:14px; padding:14px 18px; margin:10px 0; }
.agent-bubble { background: rgba(139,92,246,0.08); border:1px solid rgba(139,92,246,0.2); border-radius:14px; padding:14px 18px; margin:10px 0; }
.insight-box { background: rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.25); border-radius:10px; padding:14px; margin-top:10px; }
.stButton>button { background: linear-gradient(135deg,#00d4ff,#8b5cf6) !important; color:white !important; font-weight:700 !important; border:none !important; border-radius:50px !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 DataGPT")
    st.markdown("*AI-Powered Data Analyst Agent*")
    st.divider()

    openai_key = st.text_input("OpenAI API Key (optional)", type="password", placeholder="sk-...")
    st.caption("Leave blank for demo mode with pre-generated insights.")
    demo_mode = not bool(openai_key)
    if demo_mode:
        st.info("🎭 Demo mode active")
    st.divider()

    st.markdown("**📊 Dataset Info**")
    st.markdown("- 1,000 e-commerce orders")
    st.markdown("- 12 features")
    st.markdown("- Jan 2023 – Dec 2023")
    st.divider()

    if st.button("🔄 Reset Conversation"):
        st.session_state.chat = []
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

# ── Dataset preview ────────────────────────────────────────────────────────────
with st.expander("📋 View Dataset (E-Commerce Orders 2023)"):
    st.dataframe(df.head(20), use_container_width=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Orders",   f"{len(df):,}")
    c2.metric("Total Revenue",  f"${df['revenue'].sum():,.0f}")
    c3.metric("Avg Order Value",f"${df['revenue'].mean():.0f}")
    c4.metric("Products",       df['product_category'].nunique())

# ── Suggested questions ────────────────────────────────────────────────────────
st.markdown("### 💡 Quick Questions")
suggestions = [
    "📈 Show monthly revenue trend",
    "🏆 Which product category makes most revenue?",
    "🌍 Top 5 countries by sales",
    "👥 What's the average order value by customer segment?",
    "📦 Show orders by payment method",
    "🔄 What is the refund rate by category?",
]
cols = st.columns(3)
for i, (col, sug) in enumerate(zip(cols * 2, suggestions)):
    if col.button(sug, key=f"q{i}"):
        st.session_state.pending = sug.split(" ",1)[1]
        st.rerun()

st.divider()

# ── Chat history ───────────────────────────────────────────────────────────────
for turn in st.session_state.chat:
    st.markdown(f"<div class='user-bubble'>🧑 <strong>You:</strong> {turn['question']}</div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='agent-bubble'>🤖 <strong>DataGPT:</strong> {turn['insight']}</div>",
                unsafe_allow_html=True)
    if turn.get("fig"):
        st.plotly_chart(turn["fig"], use_container_width=True)
    if turn.get("table") is not None:
        st.dataframe(turn["table"], use_container_width=True, height=200)

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
