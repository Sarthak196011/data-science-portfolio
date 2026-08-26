import pandas as pd
import numpy as np
import os

np.random.seed(42)
n = 2000

data = {
    'customer_id':      [f'CUST{i:04d}' for i in range(n)],
    'tenure_months':    np.random.randint(1, 72, n),
    'monthly_charges':  np.round(np.random.uniform(20, 120, n), 2),
    'total_charges':    np.round(np.random.uniform(100, 8000, n), 2),
    'num_products':     np.random.randint(1, 5, n),
    'support_calls':    np.random.randint(0, 10, n),
    'payment_delays':   np.random.randint(0, 5, n),
    'contract_type':    np.random.choice(['Month-to-month','One year','Two year'], n, p=[0.55,0.25,0.20]),
    'internet_service': np.random.choice(['DSL','Fiber optic','No'], n, p=[0.35,0.45,0.20]),
    'online_security':  np.random.choice(['Yes','No'], n),
    'tech_support':     np.random.choice(['Yes','No'], n),
    'paperless_billing':np.random.choice(['Yes','No'], n, p=[0.6,0.4]),
    'gender':           np.random.choice(['Male','Female'], n),
    'senior_citizen':   np.random.choice([0,1], n, p=[0.84,0.16]),
    'partner':          np.random.choice(['Yes','No'], n),
    'dependents':       np.random.choice(['Yes','No'], n, p=[0.3,0.7]),
}

df = pd.DataFrame(data)

churn_prob = (
    0.05
    + (df['contract_type']=='Month-to-month').astype(float) * 0.25
    + (df['internet_service']=='Fiber optic').astype(float) * 0.10
    + (df['monthly_charges'] > 80).astype(float) * 0.15
    + (df['tenure_months'] < 12).astype(float) * 0.20
    + (df['support_calls'] > 5).astype(float) * 0.10
    + (df['payment_delays'] > 2).astype(float) * 0.10
    + (df['online_security'] == 'No').astype(float) * 0.05
).clip(0, 1)

df['churn'] = (np.random.random(n) < churn_prob).astype(int)

out = r'C:\Users\sarthak\.gemini\antigravity-ide\scratch\03-churn-predictor\data\telecom_churn.csv'
df.to_csv(out, index=False)
print(f"Saved {len(df)} rows | Churn rate: {df.churn.mean()*100:.1f}%")
