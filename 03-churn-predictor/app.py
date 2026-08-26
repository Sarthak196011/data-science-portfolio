"""
Customer Churn Predictor — Main Streamlit App
Run: streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="ChurnShield AI — Customer Churn Predictor",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject custom CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #05050f 0%, #0a0a1a 100%);
}
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.03) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
.metric-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    transition: 0.3s;
}
.metric-card:hover { border-color: rgba(0,212,255,0.4); }
.metric-val { font-size: 2rem; font-weight: 800; color: #00d4ff; }
.metric-lbl { font-size: 0.8rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 0.1em; }
.churn-high   { background: rgba(239,68,68,0.15); border: 1px solid rgba(239,68,68,0.4); border-radius:10px; padding:16px; }
.churn-low    { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.4); border-radius:10px; padding:16px; }
.stButton>button {
    background: linear-gradient(135deg,#00d4ff,#8b5cf6) !important;
    color: white !important; font-weight: 700 !important;
    border: none !important; border-radius: 50px !important;
    padding: 12px 32px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar Navigation ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔮 ChurnShield AI")
    st.markdown("*Customer Churn Prediction Platform*")
    st.divider()
    page = st.radio("Navigate", ["🏠 Home","🎯 Predict Single","📦 Batch Predict","📊 Analytics Dashboard","ℹ️ About"])
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
