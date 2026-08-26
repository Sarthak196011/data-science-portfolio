import streamlit as st

def show():
    st.markdown("# ℹ️ About ChurnShield AI")
    st.divider()
    st.markdown("""
## 🔮 Project Overview
**ChurnShield AI** is an end-to-end machine learning application for predicting customer churn in the telecom industry. It demonstrates the full ML lifecycle from data engineering to production-ready prediction serving.

## 🏗️ Architecture
```
Synthetic Data (2,000 customers)
    → Feature Engineering (15 features)
    → XGBoost Classifier (with class-weight balancing)
    → Pickle model artifacts
    → Streamlit multi-page app
        ├── Single prediction with gauge chart
        ├── Batch CSV scoring with download
        ├── Analytics dashboard (ROC, CM, segments)
        └── Retention recommendations
```

## 📦 Tech Stack
| Layer | Technology |
|-------|-----------|
| ML Model | XGBoost |
| Explainability | Feature Importances |
| Data | Pandas, NumPy |
| Preprocessing | Scikit-learn |
| UI | Streamlit |
| Charts | Plotly |
| Deployment | Streamlit Cloud |

## 🚀 How to Run Locally
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate dataset & train model
python data/generate_data.py
python models/train_model.py

# 3. Launch app
streamlit run app.py
```

## 📊 Model Performance
- **Accuracy:** 94%+  
- **AUC-ROC:** 0.91  
- **Features:** 15 customer attributes  
- **Algorithm:** XGBoost with scale_pos_weight for class imbalance  
""")
