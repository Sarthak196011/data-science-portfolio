"""
Train XGBoost churn model and save artifacts.
Run: python train_model.py
"""
import pandas as pd
import numpy as np
import pickle, os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report
import xgboost as xgb

# ── 1. Load data ─────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE, '..', 'data', 'telecom_churn.csv'))

# ── 2. Feature engineering ───────────────────────────────────────────────────
cat_cols = ['contract_type','internet_service','online_security',
            'tech_support','paperless_billing','gender','partner','dependents']
num_cols = ['tenure_months','monthly_charges','total_charges',
            'num_products','support_calls','payment_delays','senior_citizen']

encoders = {}
df_enc = df.copy()
for col in cat_cols:
    le = LabelEncoder()
    df_enc[col] = le.fit_transform(df[col])
    encoders[col] = le

feature_cols = num_cols + cat_cols
X = df_enc[feature_cols]
y = df_enc['churn']

# ── 3. Scale ─────────────────────────────────────────────────────────────────
scaler = StandardScaler()
X_scaled = X.copy()
X_scaled[num_cols] = scaler.fit_transform(X[num_cols])

# ── 4. Train / test split ─────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y)

# ── 5. Train XGBoost ──────────────────────────────────────────────────────────
model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    scale_pos_weight=(y==0).sum()/(y==1).sum(),
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42,
    verbosity=0
)
model.fit(X_train, y_train,
          eval_set=[(X_test, y_test)],
          verbose=False)

# ── 6. Evaluate ───────────────────────────────────────────────────────────────
y_pred  = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]
acc     = accuracy_score(y_test, y_pred)
auc     = roc_auc_score(y_test, y_proba)
print(f"\n[OK] Accuracy : {acc*100:.2f}%")
print(f"[OK] AUC-ROC  : {auc:.4f}")
print("\n" + classification_report(y_test, y_pred, target_names=['Retained','Churned']))

# ── 7. Save artifacts ─────────────────────────────────────────────────────────
models_dir = os.path.join(BASE, '..', 'models')
os.makedirs(models_dir, exist_ok=True)

artifacts = {
    'model':        model,
    'scaler':       scaler,
    'encoders':     encoders,
    'feature_cols': feature_cols,
    'num_cols':     num_cols,
    'cat_cols':     cat_cols,
}
with open(os.path.join(models_dir, 'churn_artifacts.pkl'), 'wb') as f:
    pickle.dump(artifacts, f)

# Save test data for dashboard
test_df = df.iloc[X_test.index].copy()
test_df['churn_proba'] = y_proba
test_df['predicted']   = y_pred
test_df.to_csv(os.path.join(models_dir, 'test_predictions.csv'), index=False)

print(f"\n[OK] Artifacts saved -> models/churn_artifacts.pkl")
print(f"[OK] Test predictions -> models/test_predictions.csv")
