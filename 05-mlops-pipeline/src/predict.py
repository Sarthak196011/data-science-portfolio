"""Inference utilities for the MLOps API."""
import pickle, os, numpy as np, pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__),'..','models','artifacts.pkl')

def load_model():
    if not os.path.exists(MODEL_PATH):
        from src.train import train
        return train()
    with open(MODEL_PATH,'rb') as f:
        return pickle.load(f)

def _encode_and_scale(artifacts, row_dict):
    encoders = artifacts['encoders']; scaler = artifacts['scaler']
    num_cols = artifacts['num_cols']; cat_cols = artifacts['cat_cols']
    feat     = artifacts['feature_cols']
    row = pd.DataFrame([row_dict])
    for col in cat_cols:
        try:
            row[col] = encoders[col].transform(row[col])
        except ValueError:
            row[col] = 0
    row[num_cols] = scaler.transform(row[num_cols])
    return row[feat]

def predict_single(artifacts, row_dict):
    X     = _encode_and_scale(artifacts, row_dict)
    proba = float(artifacts['model'].predict_proba(X)[0][1])
    pred  = proba > 0.5
    risk  = "High" if proba > 0.6 else "Medium" if proba > 0.35 else "Low"
    importances = artifacts['model'].feature_importances_
    feat_names  = artifacts['feature_cols']
    top_idx     = np.argsort(importances)[::-1][:3]
    top_factors = [feat_names[i].replace('_',' ').title() for i in top_idx]
    return {"probability": round(proba,4), "predicted": bool(pred), "risk_level": risk, "top_factors": top_factors}

def predict_batch(artifacts, rows):
    return [{"customer_index": i, **predict_single(artifacts, row)} for i, row in enumerate(rows)]
