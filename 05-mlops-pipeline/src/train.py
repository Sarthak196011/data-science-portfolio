"""Model training with MLflow experiment tracking."""
import pandas as pd, numpy as np, pickle, os, sys
import mlflow, mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score
import xgboost as xgb

BASE      = os.path.dirname(os.path.abspath(__file__))
ROOT      = os.path.join(BASE, '..')
DATA_PATH = os.path.join(ROOT, 'data', 'churn_data.csv')
MODEL_DIR = os.path.join(ROOT, 'models')

def generate_data():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    np.random.seed(42); n = 3000
    data = {
        'tenure_months':    np.random.randint(1,72,n),
        'monthly_charges':  np.round(np.random.uniform(20,120,n),2),
        'total_charges':    np.round(np.random.uniform(100,8000,n),2),
        'num_products':     np.random.randint(1,5,n),
        'support_calls':    np.random.randint(0,10,n),
        'payment_delays':   np.random.randint(0,5,n),
        'contract_type':    np.random.choice(['Month-to-month','One year','Two year'],n,p=[.55,.25,.20]),
        'internet_service': np.random.choice(['DSL','Fiber optic','No'],n,p=[.35,.45,.20]),
        'online_security':  np.random.choice(['Yes','No'],n),
        'tech_support':     np.random.choice(['Yes','No'],n),
        'paperless_billing':np.random.choice(['Yes','No'],n,p=[.6,.4]),
        'gender':           np.random.choice(['Male','Female'],n),
        'senior_citizen':   np.random.choice([0,1],n,p=[.84,.16]),
        'partner':          np.random.choice(['Yes','No'],n),
        'dependents':       np.random.choice(['Yes','No'],n,p=[.3,.7]),
    }
    df = pd.DataFrame(data)
    prob = (.05 + (df.contract_type=='Month-to-month')*.25 + (df.internet_service=='Fiber optic')*.10
            + (df.monthly_charges>80)*.15 + (df.tenure_months<12)*.20 + (df.support_calls>5)*.10
            + (df.payment_delays>2)*.10).clip(0,1)
    df['churn'] = (np.random.random(n) < prob).astype(int)
    df.to_csv(DATA_PATH, index=False)
    return df

def train():
    os.environ["MLFLOW_ALLOW_FILE_STORE"] = "true"
    mlflow.set_tracking_uri("file:///" + os.path.join(ROOT, 'mlruns').replace('\\', '/'))
    mlflow.set_experiment("churn-prediction")

    df = pd.read_csv(DATA_PATH) if os.path.exists(DATA_PATH) else generate_data()
    cat_cols = ['contract_type','internet_service','online_security','tech_support',
                'paperless_billing','gender','partner','dependents']
    num_cols = ['tenure_months','monthly_charges','total_charges','num_products',
                'support_calls','payment_delays','senior_citizen']

    encoders = {}
    for col in cat_cols:
        le = LabelEncoder(); df[col] = le.fit_transform(df[col]); encoders[col] = le

    feature_cols = num_cols + cat_cols
    X = df[feature_cols]; y = df['churn']
    scaler = StandardScaler()
    X_s = X.copy(); X_s[num_cols] = scaler.fit_transform(X[num_cols])
    X_train, X_test, y_train, y_test = train_test_split(X_s, y, test_size=0.2, random_state=42, stratify=y)

    params = {"n_estimators":300,"max_depth":5,"learning_rate":0.05,
              "subsample":0.8,"colsample_bytree":0.8,"random_state":42,"verbosity":0}

    model = xgb.XGBClassifier(**params, scale_pos_weight=(y==0).sum()/(y==1).sum(),
                               use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train, y_train, eval_set=[(X_test,y_test)], verbose=False)

    y_pred  = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:,1]
    acc = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)
    f1  = f1_score(y_test, y_pred)

    print(f"Accuracy: {acc:.4f} | AUC: {auc:.4f} | F1: {f1:.4f}")

    try:
        with mlflow.start_run(run_name="xgboost-v1") as run:
            mlflow.log_params(params)
            mlflow.log_metrics({"accuracy":acc,"auc_roc":auc,"f1_score":f1})
            # Try to log model; if skops/scipy blocks due to OS dll policy, catch it
            try:
                mlflow.xgboost.log_model(model, "model")
            except Exception as e:
                print(f"[MLflow Warning] Model logging failed: {e}")
            print(f"Run ID : {run.info.run_id}")
    except Exception as e:
        print(f"[MLflow Warning] MLflow tracking failed (probably due to App Control policy blocking DLLs): {e}")

    # Save local artifacts
    os.makedirs(MODEL_DIR, exist_ok=True)
    artifacts = {"model":model,"scaler":scaler,"encoders":encoders,
                 "feature_cols":feature_cols,"num_cols":num_cols,"cat_cols":cat_cols}
    with open(os.path.join(MODEL_DIR,'artifacts.pkl'),'wb') as f:
        pickle.dump(artifacts, f)
    print(f"[OK] Model saved -> {MODEL_DIR}/artifacts.pkl")
    return artifacts

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT,'data'), exist_ok=True)
    if not os.path.exists(DATA_PATH):
        generate_data()
    train()
