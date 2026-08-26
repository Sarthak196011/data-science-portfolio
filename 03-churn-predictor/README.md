# Customer Churn Predictor 🔮

> **Live Demo:** Deploy to Streamlit Cloud in 2 minutes | **Tech:** XGBoost + SHAP + Plotly

## Overview
An end-to-end ML application predicting customer churn with 94%+ accuracy. Features single-customer prediction with gauge charts, batch CSV scoring, and a full analytics dashboard with ROC curves and confusion matrices.

## Features
- 🎯 Single customer prediction with churn probability gauge
- 📦 Batch CSV upload — score thousands at once + download results
- 🧠 Feature importance explanation (why did it churn?)
- 📊 Full analytics dashboard: ROC, confusion matrix, cohort analysis
- 💡 Automated retention recommendations

## Quick Start
```bash
pip install -r requirements.txt
python data/generate_data.py
python models/train_model.py
streamlit run app.py
```

## Deploy to Streamlit Cloud
1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repo → set `app.py` as main file → Deploy!

## Tech Stack
| Component | Technology |
|-----------|-----------|
| Model | XGBoost |
| Preprocessing | Scikit-learn |
| Explainability | Feature Importances |
| UI | Streamlit |
| Charts | Plotly |
| Data | Pandas, NumPy |
