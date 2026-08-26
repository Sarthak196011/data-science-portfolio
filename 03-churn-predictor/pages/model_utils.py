"""Shared model loader — cached across pages."""
import pickle, os
import streamlit as st

MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'churn_artifacts.pkl')

@st.cache_resource(show_spinner="Loading model…")
def load_artifacts():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

def predict_churn(artifacts, input_dict):
    import pandas as pd
    model    = artifacts['model']
    scaler   = artifacts['scaler']
    encoders = artifacts['encoders']
    feat     = artifacts['feature_cols']
    num_cols = artifacts['num_cols']
    cat_cols = artifacts['cat_cols']

    row = pd.DataFrame([input_dict])
    for col in cat_cols:
        row[col] = encoders[col].transform(row[col])
    row[num_cols] = scaler.transform(row[num_cols])
    proba = model.predict_proba(row[feat])[0][1]
    return proba
