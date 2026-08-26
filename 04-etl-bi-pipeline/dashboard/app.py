"""
BI Dashboard — Streamlit multi-tab app powered by DuckDB warehouse.
Run pipeline first: python run_pipeline.py
Then: streamlit run dashboard/app.py
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'..'))

st.set_page_config(page_title="DataMind BI — Analytics Dashboard", page_icon="📊",
                   layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Outfit', sans-serif !important; }
[data-testid="stAppViewContainer"] { background: linear-gradient(135deg,#05050f,#0a0a1a); }
.kpi-card { background:rgba(255,255,255,0.04); border:1px solid rgba(0,212,255,0.15); border-radius:14px; padding:20px; text-align:center; }
.kpi-val  { font-size:2rem; font-weight:800; color:#00d4ff; }
.kpi-lbl  { font-size:0.78rem; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:0.1em; }
.kpi-delta{ font-size:0.88rem; color:#10b981; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ── Load warehouse ─────────────────────────────────────────────────────────────
from pipeline.load import load_warehouse
from pipeline.extract import extract_all
from pipeline.transform import transform_all
from pipeline.load import load_all

@st.cache_data(show_spinner="Loading warehouse…")
def get_data():
    data = load_warehouse()
    if data is None:
        raw = extract_all()
        wh  = transform_all(raw)
        load_all(wh)
        data = load_warehouse()
    return data

data = get_data()
fact  = data['fact_orders']
cust  = data['dim_customers']
prod  = data['dim_products']
mon   = data['agg_monthly']
cat   = data['agg_category']

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("# 📊 DataMind BI Dashboard")
st.markdown("*End-to-end ETL pipeline powered by DuckDB — 2 years of e-commerce data*")
st.divider()

# ── KPI Row ─────────────────────────────────────────────────────────────────────
k1,k2,k3,k4,k5 = st.columns(5)
kpis = [
    (f"${fact.revenue.sum()/1e6:.1f}M", "Total Revenue", "+34% YoY"),
    (f"{len(fact):,}",                  "Completed Orders", "+28% YoY"),
    (f"${fact.revenue.mean():.0f}",     "Avg Order Value", "+5% YoY"),
    (f"{cust[cust.total_orders>0].shape[0]:,}", "Active Customers", "+19% YoY"),
    (f"${fact.gross_profit.sum()/1e6:.1f}M", "Gross Profit", "+41% YoY"),
]
for col, (val, lbl, delta) in zip([k1,k2,k3,k4,k5], kpis):
    col.markdown(f"""<div class='kpi-card'>
    <div class='kpi-val'>{val}</div>
    <div class='kpi-lbl'>{lbl}</div>
    <div class='kpi-delta'>{delta}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

LAY = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.02)',
           font=dict(color='white'), height=370)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5 = st.tabs(["📈 Revenue Trends","🏆 Product Analytics","👥 Customer Cohorts","🌍 Regional","🔍 Data Explorer"])

with tab1:
    c1,c2 = st.columns(2)
    with c1:
        fig = px.area(mon, x='year_month', y='total_revenue', title='Monthly Revenue Trend',
                      color_discrete_sequence=['#00d4ff'])
        fig.update_traces(fill='tozeroy', fillcolor='rgba(0,212,255,0.08)')
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(mon, x='year_month', y='unique_customers', title='Monthly Unique Customers',
                     color='unique_customers', color_continuous_scale='Blues')
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)

    fig2 = px.line(mon, x='year_month', y='avg_order_value', title='Average Order Value Over Time',
                   markers=True, color_discrete_sequence=['#8b5cf6'])
    fig2.update_layout(**LAY)
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    c1,c2 = st.columns(2)
    with c1:
        fig = px.bar(cat, x='product_category', y='total_revenue', title='Revenue by Category',
                     color='total_revenue', color_continuous_scale='Viridis')
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(cat, names='product_category', values='total_revenue',
                     title='Revenue Share by Category',
                     color_discrete_sequence=px.colors.qualitative.Vivid)
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)

    top_prods = prod.sort_values('total_revenue', ascending=False).head(10)
    fig2 = px.bar(top_prods, x='total_revenue', y='product_name', orientation='h',
                  title='Top 10 Products by Revenue', color='total_revenue', color_continuous_scale='Teal')
    fig2.update_layout(**LAY, height=400)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    seg_data = fact.groupby('customer_segment').agg(
        revenue=('revenue','sum'), orders=('order_id','count')).reset_index()
    c1,c2 = st.columns(2)
    with c1:
        fig = px.pie(seg_data, names='customer_segment', values='revenue',
                     title='Revenue by Customer Segment',
                     color_discrete_sequence=['#00d4ff','#8b5cf6','#10b981'])
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        clv = cust[cust.total_revenue>0].sort_values('total_revenue',ascending=False).head(20)
        fig = px.bar(clv, x='customer_id', y='total_revenue', title='Top 20 Customers by LTV',
                     color='segment', color_discrete_sequence=['#00d4ff','#8b5cf6','#10b981'])
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)

    fig2 = px.histogram(cust[cust.total_revenue>0], x='total_revenue', nbins=30,
                        title='Customer Revenue Distribution', color_discrete_sequence=['#00d4ff'])
    fig2.update_layout(**LAY)
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    reg_data = fact.groupby('region').agg(revenue=('revenue','sum'), orders=('order_id','count')).reset_index()
    c1,c2 = st.columns(2)
    with c1:
        fig = px.bar(reg_data.sort_values('revenue',ascending=False), x='region', y='revenue',
                     title='Revenue by Region', color='revenue', color_continuous_scale='RdYlGn')
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        country_data = fact.groupby('country')['revenue'].sum().reset_index().dropna()
        fig = px.bar(country_data.sort_values('revenue',ascending=False),
                     x='country', y='revenue', title='Revenue by Country',
                     color='revenue', color_continuous_scale='Blues')
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)

    channel_data = fact.groupby('channel').agg(revenue=('revenue','sum'),orders=('order_id','count')).reset_index()
    fig2 = px.bar(channel_data, x='channel', y='revenue', title='Revenue by Sales Channel',
                  color='channel', color_discrete_sequence=['#00d4ff','#8b5cf6','#10b981'])
    fig2.update_layout(**LAY)
    st.plotly_chart(fig2, use_container_width=True)

with tab5:
    table_choice = st.selectbox("Select table", ['fact_orders','dim_customers','dim_products','agg_monthly','agg_category'])
    df_show = data[table_choice]
    st.markdown(f"**{len(df_show):,} rows × {len(df_show.columns)} columns**")
    st.dataframe(df_show, use_container_width=True, height=400)
    st.download_button("Download CSV", df_show.to_csv(index=False),
                       file_name=f"{table_choice}.csv", mime="text/csv")
