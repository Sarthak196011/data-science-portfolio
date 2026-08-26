"""Extract: generate and load raw CSV data."""
import pandas as pd
import numpy as np
import os

RAW_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')

def extract_all():
    os.makedirs(RAW_DIR, exist_ok=True)
    return {
        'orders':    _load_or_generate_orders(),
        'customers': _load_or_generate_customers(),
        'products':  _load_or_generate_products(),
    }

def _load_or_generate_orders():
    path = os.path.join(RAW_DIR, 'orders.csv')
    if os.path.exists(path):
        return pd.read_csv(path, parse_dates=['order_date'])
    np.random.seed(42)
    n = 5000
    cats = ['Electronics','Clothing','Home & Kitchen','Books','Sports','Beauty']
    df = pd.DataFrame({
        'order_id':    [f'ORD{i:06d}' for i in range(n)],
        'customer_id': [f'CUST{np.random.randint(1,500):04d}' for _ in range(n)],
        'product_id':  [f'PROD{np.random.randint(1,200):04d}' for _ in range(n)],
        'order_date':  pd.date_range('2022-01-01','2023-12-31',periods=n),
        'quantity':    np.random.randint(1, 15, n),
        'unit_price':  np.round(np.random.uniform(10, 500, n), 2),
        'discount':    np.random.choice([0,.05,.10,.15,.20], n, p=[.4,.2,.2,.1,.1]),
        'status':      np.random.choice(['Completed','Returned','Pending'], n, p=[.88,.08,.04]),
        'channel':     np.random.choice(['Web','Mobile','In-Store'], n, p=[.5,.35,.15]),
        'region':      np.random.choice(['North','South','East','West','International'], n, p=[.25,.2,.2,.2,.15]),
    })
    df['revenue'] = np.round(df['quantity']*df['unit_price']*(1-df['discount']),2)
    df.to_csv(path, index=False)
    return df

def _load_or_generate_customers():
    path = os.path.join(RAW_DIR, 'customers.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    np.random.seed(10)
    n = 499
    df = pd.DataFrame({
        'customer_id':  [f'CUST{i+1:04d}' for i in range(n)],
        'name':         [f'Customer {i+1}' for i in range(n)],
        'segment':      np.random.choice(['Consumer','Corporate','Home Office'], n, p=[.52,.33,.15]),
        'country':      np.random.choice(['USA','UK','Germany','India','Canada','Australia'], n, p=[.35,.15,.12,.18,.10,.10]),
        'signup_year':  np.random.randint(2018, 2024, n),
        'lifetime_value':np.round(np.random.exponential(1200, n), 2),
    })
    df.to_csv(path, index=False)
    return df

def _load_or_generate_products():
    path = os.path.join(RAW_DIR, 'products.csv')
    if os.path.exists(path):
        return pd.read_csv(path)
    np.random.seed(20)
    n = 199
    cats = ['Electronics','Clothing','Home & Kitchen','Books','Sports','Beauty']
    df = pd.DataFrame({
        'product_id':  [f'PROD{i+1:04d}' for i in range(n)],
        'product_name':[f'Product {i+1}' for i in range(n)],
        'category':    np.random.choice(cats, n, p=[.28,.22,.18,.12,.12,.08]),
        'cost_price':  np.round(np.random.uniform(5, 200, n), 2),
        'list_price':  np.round(np.random.uniform(10, 500, n), 2),
        'supplier':    np.random.choice(['SupplierA','SupplierB','SupplierC','SupplierD'], n),
    })
    df.to_csv(path, index=False)
    return df
