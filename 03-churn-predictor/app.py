"""
Customer Churn Predictor — Main Streamlit App
Run: streamlit run app.py
"""
import streamlit as st
import os

st.set_page_config(
    page_title="ChurnShield AI — Customer Churn Predictor",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; color: #0f172a !important; }

[data-testid="stAppViewContainer"] {
    background-color: #f8fafc !important;
}
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
}
.metric-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 2px 4px -2px rgba(0,0,0,0.05);
}
.metric-card:hover { border-color: #cbd5e1; }
.metric-val { font-size: 2.2rem; font-weight: 800; color: #0ea5e9; }
.metric-lbl { font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; }
.churn-high   { background: #fef2f2; border: 1px solid #fecaca; border-radius:10px; padding:16px; color: #991b1b; }
.churn-low    { background: #f0fdf4; border: 1px solid #bbf7d0; border-radius:10px; padding:16px; color: #166534; }
.stButton>button {
    background: #0ea5e9 !important;
    color: white !important; font-weight: 600 !important;
    border: none !important; border-radius: 6px !important;
    padding: 10px 24px !important;
    transition: 0.2s;
}
.stButton>button:hover {
    background: #0284c7 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.image(os.path.join(os.path.dirname(__file__), "images", "churn_3d_bridge.jpg"), use_container_width=True)
    st.markdown("## 🔮 ChurnShield AI")
    st.markdown("*Customer Churn Prediction Platform*")
    st.divider()
    page = st.radio("Navigate", ["🏠 Home","🎯 Predict Single","📦 Batch Predict","📊 Analytics Dashboard","ℹ️ About"])
    st.divider()
    
    openai_key = st.text_input("OpenAI API Key (optional)", type="password", placeholder="sk-...")
    st.session_state.openai_key = openai_key
    st.divider()
    
    st.markdown("**Model Info**")
    st.markdown("- Algorithm: XGBoost")
    st.markdown("- Features: 15")
    st.markdown("- Dataset: 2,000 customers")

# ── Page routing ──────────────────────────────────────────────────────────────
if page == "🏠 Home":
    from pages.home import show; show()
elif page == "🎯 Predict Single":
    from pages.predict import show; show()
elif page == "📦 Batch Predict":
    from pages.batch import show; show()
elif page == "📊 Analytics Dashboard":
    from pages.dashboard import show; show()
elif page == "ℹ️ About":
    from pages.about import show; show()
