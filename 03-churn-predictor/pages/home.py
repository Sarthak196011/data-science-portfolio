import streamlit as st

def show():
    st.markdown("# 🔮 ChurnShield AI")
    st.markdown("### *Predict Customer Churn Before It Happens*")
    st.divider()

    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("94%+", "Model Accuracy"),
        ("0.91", "AUC-ROC Score"),
        ("2,000", "Training Customers"),
        ("15", "Features Used"),
    ]
    for col, (val, lbl) in zip([col1,col2,col3,col4], metrics):
        col.markdown(f"""
        <div class='metric-card'>
          <div class='metric-val'>{val}</div>
          <div class='metric-lbl'>{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("## How It Works")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 1️⃣ Input Customer Data")
        st.markdown("Enter customer attributes like tenure, contract type, monthly charges and service usage.")
    with c2:
        st.markdown("### 2️⃣ AI Prediction")
        st.markdown("XGBoost model analyses 15 features to output a churn probability score from 0–100%.")
    with c3:
        st.markdown("### 3️⃣ SHAP Explanation")
        st.markdown("See exactly **why** the model flagged the customer — ranked by feature contribution.")

    st.divider()
    st.markdown("## 🚀 Get Started")
    col_a, col_b = st.columns(2)
    col_a.info("👈 Use the sidebar to navigate to **Predict Single** for a single customer prediction")
    col_b.info("📦 Use **Batch Predict** to upload a CSV and score thousands of customers at once")
