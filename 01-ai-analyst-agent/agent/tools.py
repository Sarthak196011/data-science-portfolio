"""Agent tools: data loader, query executor, chart builder."""
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os, re

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'ecommerce_sales.csv')

def load_data() -> pd.DataFrame:
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH, parse_dates=['order_date'])
    return _generate_data()

def _generate_data() -> pd.DataFrame:
    np.random.seed(42)
    n = 1000
    dates     = pd.date_range('2023-01-01','2023-12-31', periods=n)
    cats      = ['Electronics','Clothing','Home & Kitchen','Books','Sports','Beauty']
    countries = ['USA','UK','Germany','India','Canada','Australia','France']
    segments  = ['Consumer','Corporate','Home Office']
    payments  = ['Credit Card','PayPal','Bank Transfer','Crypto']

    df = pd.DataFrame({
        'order_id':          [f'ORD{i:05d}' for i in range(n)],
        'order_date':        np.random.choice(dates, n),
        'customer_id':       [f'CUST{np.random.randint(1,300):04d}' for _ in range(n)],
        'product_category':  np.random.choice(cats, n, p=[0.28,0.22,0.18,0.12,0.12,0.08]),
        'country':           np.random.choice(countries, n, p=[0.35,0.15,0.12,0.14,0.10,0.08,0.06]),
        'customer_segment':  np.random.choice(segments, n, p=[0.52,0.33,0.15]),
        'payment_method':    np.random.choice(payments, n, p=[0.55,0.25,0.15,0.05]),
        'units_sold':        np.random.randint(1, 20, n),
        'unit_price':        np.round(np.random.uniform(9.99, 499.99, n), 2),
        'discount_pct':      np.random.choice([0,5,10,15,20], n, p=[0.4,0.2,0.2,0.1,0.1]),
        'is_returned':       np.random.choice([0,1], n, p=[0.88,0.12]),
        'rating':            np.round(np.random.uniform(2.5, 5.0, n), 1),
    })
    df['revenue'] = np.round(df['units_sold'] * df['unit_price'] * (1 - df['discount_pct']/100), 2)
    df.sort_values('order_date', inplace=True)
    df.to_csv(DATA_PATH, index=False)
    return df


def run_query(df: pd.DataFrame, question: str, demo_mode: bool = True, api_key: str = None) -> dict:
    """Route question to the right tool and return {insight, fig, table}."""
    q = question.lower()
    fig = None
    table = None

    # ── Route to chart tools ───────────────────────────────────────────────────
    if any(w in q for w in ['monthly','trend','over time','by month','time']):
        fig, data = _monthly_revenue(df)
        insight = _insight(question, data, demo_mode, api_key,
            f"Monthly revenue peaked in {data.loc[data.revenue.idxmax(),'month_label']} at ${data.revenue.max():,.0f}. "
            f"Total 2023 revenue was ${data.revenue.sum():,.0f}. "
            f"The best quarter was Q{data.groupby(data.month.apply(lambda x: (x-1)//3+1)).revenue.sum().idxmax()}.")

    elif any(w in q for w in ['category','product','categories']):
        fig, data = _by_category(df)
        top = data.iloc[0]
        insight = _insight(question, data, demo_mode, api_key,
            f"The top performing category is **{top['product_category']}** with ${top['revenue']:,.0f} revenue "
            f"({top['revenue']/data.revenue.sum()*100:.1f}% of total). "
            f"**{data.iloc[-1]['product_category']}** has the lowest sales at ${data.iloc[-1]['revenue']:,.0f}.")

    elif any(w in q for w in ['country','countries','region','geographic','top 5','top5']):
        fig, data = _by_country(df)
        insight = _insight(question, data, demo_mode, api_key,
            f"**{data.iloc[0]['country']}** leads with ${data.iloc[0]['revenue']:,.0f} revenue. "
            f"The top 3 countries account for {data.head(3).revenue.sum()/data.revenue.sum()*100:.0f}% of total revenue.")
        table = data.head(7)

    elif any(w in q for w in ['segment','customer type','consumer','corporate']):
        fig, data = _by_segment(df)
        insight = _insight(question, data, demo_mode, api_key,
            f"The **{data.iloc[0]['customer_segment']}** segment drives the most revenue at ${data.iloc[0]['revenue']:,.0f}. "
            f"Average order value differs significantly: Consumer ${df[df.customer_segment=='Consumer'].revenue.mean():.0f} "
            f"vs Corporate ${df[df.customer_segment=='Corporate'].revenue.mean():.0f}.")

    elif any(w in q for w in ['payment','method','credit','paypal']):
        fig, data = _by_payment(df)
        insight = _insight(question, data, demo_mode, api_key,
            f"**{data.iloc[0]['payment_method']}** is the most used payment method ({data.iloc[0]['pct']:.0f}% of orders). "
            f"Crypto payments, while smallest in volume, may indicate a tech-savvy customer segment.")

    elif any(w in q for w in ['refund','return','returned']):
        fig, data = _refund_rate(df)
        insight = _insight(question, data, demo_mode, api_key,
            f"Overall return rate is {df.is_returned.mean()*100:.1f}%. "
            f"**{data.iloc[-1]['product_category']}** has the highest return rate at {data.iloc[-1]['return_rate']*100:.1f}%.")

    elif any(w in q for w in ['3d', 'scatter', 'multivariate', 'cluster', '3d chart']):
        fig = px.scatter_3d(
            df, x='units_sold', y='revenue', z='rating',
            color='product_category',
            title='3D Product Performance (Units Sold vs Revenue vs Rating)',
            labels={'units_sold': 'Units Sold', 'revenue': 'Revenue ($)', 'rating': 'Customer Rating'},
            color_discrete_sequence=['#6366f1','#10b981','#3b82f6','#ec4899','#f59e0b','#ef4444']
        )
        fig.update_layout(
            scene = dict(
                xaxis = dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,0,0,0.05)", showbackground=True),
                yaxis = dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,0,0,0.05)", showbackground=True),
                zaxis = dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="rgba(0,0,0,0.05)", showbackground=True),
            ),
            margin=dict(l=0, r=0, b=0, t=40),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c2825')
        )
        insight = "Here is an interactive **3D Scatter Plot** showing units sold (X), revenue (Y), and customer rating (Z) colored by product category. You can drag and scroll to rotate the 3D model."

    else:
        # Fallback: show revenue overview
        fig, data = _monthly_revenue(df)
        insight = (f"Great question! I analysed the e-commerce dataset (1,000 orders) for you. "
                   f"Total 2023 revenue: **${df.revenue.sum():,.0f}** across {df.country.nunique()} countries "
                   f"and {df.product_category.nunique()} product categories. "
                   f"Average order value: **${df.revenue.mean():.0f}**. Try asking about trends, categories, or countries!")

    return {"insight": insight, "fig": fig, "table": table}


# ── Chart generators ──────────────────────────────────────────────────────────
_LAYOUT = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0.015)', font=dict(color='#2c2825'), height=380)

def _monthly_revenue(df):
    df2 = df.copy()
    df2['month'] = df2['order_date'].dt.month
    df2['month_label'] = df2['order_date'].dt.strftime('%b')
    data = df2.groupby(['month','month_label'])['revenue'].sum().reset_index().sort_values('month')
    fig = px.area(data, x='month_label', y='revenue', title='Monthly Revenue 2023',
                  color_discrete_sequence=['#6366f1'])
    fig.update_traces(fill='tozeroy', fillcolor='rgba(99,102,241,0.08)')
    fig.update_layout(**_LAYOUT)
    return fig, data

def _by_category(df):
    data = df.groupby('product_category')['revenue'].sum().reset_index().sort_values('revenue',ascending=False)
    fig  = px.bar(data, x='product_category', y='revenue', title='Revenue by Product Category',
                  color='revenue', color_continuous_scale='Purples')
    fig.update_layout(**_LAYOUT)
    return fig, data

def _by_country(df):
    data = df.groupby('country')['revenue'].sum().reset_index().sort_values('revenue',ascending=False)
    fig  = px.bar(data, x='revenue', y='country', orientation='h', title='Revenue by Country',
                  color='revenue', color_continuous_scale='Sunset')
    fig.update_layout(**_LAYOUT)
    return fig, data

def _by_segment(df):
    data = df.groupby('customer_segment').agg(revenue=('revenue','sum'), orders=('order_id','count')).reset_index()
    fig  = px.pie(data, names='customer_segment', values='revenue', title='Revenue by Customer Segment',
                  color_discrete_sequence=['#6366f1','#f43f5e','#10b981'])
    fig.update_layout(**_LAYOUT)
    return fig, data

def _by_payment(df):
    data = df.groupby('payment_method').size().reset_index(name='orders')
    data['pct'] = data['orders']/data['orders'].sum()*100
    fig  = px.pie(data, names='payment_method', values='orders', title='Orders by Payment Method',
                  color_discrete_sequence=['#6366f1','#f43f5e','#10b981','#f59e0b'])
    fig.update_layout(**_LAYOUT)
    return fig, data

def _refund_rate(df):
    data = df.groupby('product_category').agg(
        return_rate=('is_returned','mean'), orders=('order_id','count')).reset_index()
    fig  = px.bar(data.sort_values('return_rate'), x='return_rate', y='product_category',
                  orientation='h', title='Return Rate by Category',
                  color='return_rate', color_continuous_scale='RdYlGn_r')
    fig.update_layout(**_LAYOUT)
    return fig, data


def _insight(question, data, demo_mode, api_key, fallback):
    if not demo_mode and api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            resp   = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"You are a senior data analyst. Give a concise 3-sentence insight with key numbers. Use markdown bold for numbers."},
                    {"role":"user","content":f"Question: {question}\nData summary:\n{data.to_string(index=False)}"},
                ],
                max_tokens=200, temperature=0.3,
            )
            return resp.choices[0].message.content
        except Exception:
            pass
    return fallback
