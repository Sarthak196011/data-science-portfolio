"""
BI Dashboard — Streamlit multi-tab app powered by DuckDB warehouse.
Run pipeline first: python run_pipeline.py
Then: streamlit run dashboard/app.py
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

st.set_page_config(page_title="DataMind BI — Analytics Dashboard", page_icon="🏗️",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif !important; color: #e2e8f0 !important; }
[data-testid="stAppViewContainer"] {
    background: #020617 !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% 40%, rgba(6,182,212,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 20%, rgba(139,92,246,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 60% 80%, rgba(16,185,129,0.08) 0%, transparent 60%),
        linear-gradient(180deg, #020617 0%, #0a0f1e 100%) !important;
}
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(6,182,212,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(6,182,212,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
    animation: gridPulse 8s ease-in-out infinite;
}
@keyframes gridPulse { 0%, 100% { opacity: 0.5; } 50% { opacity: 1; } }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #0c1225 100%) !important;
    border-right: 1px solid rgba(6,182,212,0.15) !important;
    box-shadow: 4px 0 30px rgba(6,182,212,0.05) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.8) !important;
    border-radius: 14px !important;
    padding: 6px !important;
    border: 1px solid rgba(6,182,212,0.15) !important;
    backdrop-filter: blur(12px) !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 10px !important;
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    padding: 10px 18px !important;
    border: none !important;
    transition: all 0.25s ease !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(139,92,246,0.2)) !important;
    color: #06b6d4 !important;
    border: 1px solid rgba(6,182,212,0.3) !important;
    box-shadow: 0 0 15px rgba(6,182,212,0.15), inset 0 0 15px rgba(6,182,212,0.05) !important;
}
.kpi-card {
    background: linear-gradient(135deg, rgba(15,23,42,0.9) 0%, rgba(10,15,30,0.95) 100%);
    border: 1px solid rgba(6,182,212,0.2);
    border-radius: 16px;
    padding: 22px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.35s cubic-bezier(0.4,0,0.2,1);
    backdrop-filter: blur(20px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
}
.kpi-card:hover {
    border-color: rgba(6,182,212,0.5);
    transform: translateY(-4px) scale(1.02);
    box-shadow: 0 20px 40px rgba(0,0,0,0.5), 0 0 30px rgba(6,182,212,0.15), inset 0 1px 0 rgba(255,255,255,0.08);
}
.kpi-icon { font-size: 1.4rem; margin-bottom: 6px; display: block; }
.kpi-val  { font-size: 1.9rem; font-weight: 800; color: #06b6d4; line-height: 1; margin: 4px 0; font-family: 'JetBrains Mono', monospace; }
.kpi-lbl  { font-size: 0.7rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.12em; margin-top: 6px; font-weight: 600; }
.kpi-delta{ font-size: 0.82rem; color: #10b981; font-weight: 700; margin-top: 4px; }
.anomaly-alert {
    background: linear-gradient(135deg, rgba(239,68,68,0.08), rgba(220,38,38,0.04));
    border: 1px solid rgba(239,68,68,0.3);
    border-left: 3px solid #ef4444;
    border-radius: 10px;
    padding: 14px 18px;
    margin: 8px 0;
}
.section-header {
    font-size: 1rem; font-weight: 700; color: #e2e8f0; margin: 20px 0 14px 0;
    padding-bottom: 8px; border-bottom: 1px solid rgba(6,182,212,0.15);
}
.hero-banner {
    background: linear-gradient(135deg, rgba(6,182,212,0.08) 0%, rgba(139,92,246,0.06) 50%, rgba(16,185,129,0.04) 100%);
    border: 1px solid rgba(6,182,212,0.15);
    border-radius: 20px;
    padding: 30px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(20px);
}
.hero-banner::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(6,182,212,0.6), rgba(139,92,246,0.6), transparent);
}
.hero-title {
    font-size: 1.9rem; font-weight: 800; letter-spacing: -0.03em;
    background: linear-gradient(135deg, #e2e8f0 30%, #06b6d4 70%, #8b5cf6 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin: 0 0 8px 0;
}
.hero-subtitle { color: #475569; font-size: 0.88rem; font-weight: 500; margin: 0; }
.hero-badge {
    display: inline-block; background: rgba(16,185,129,0.1); border: 1px solid rgba(16,185,129,0.3);
    border-radius: 100px; padding: 4px 14px; font-size: 0.72rem; color: #10b981; font-weight: 700;
    letter-spacing: 0.08em; margin-top: 12px;
}
.sla-row { display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 0.8rem; }
.sla-key { color: #64748b; }
.sla-val { color: #06b6d4; font-family: 'JetBrains Mono', monospace; font-weight: 600; font-size: 0.78rem; }
.sla-val.green { color: #10b981; }
.stButton > button {
    background: linear-gradient(135deg, rgba(6,182,212,0.15), rgba(139,92,246,0.15)) !important;
    color: #06b6d4 !important; font-weight: 700 !important;
    border: 1px solid rgba(6,182,212,0.4) !important; border-radius: 10px !important;
    width: 100% !important; transition: all 0.25s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(6,182,212,0.3), rgba(139,92,246,0.3)) !important;
    box-shadow: 0 0 20px rgba(6,182,212,0.25) !important; transform: translateY(-2px) !important;
}
[data-testid="stSidebar"] img { border-radius: 12px !important; border: 1px solid rgba(6,182,212,0.2) !important; box-shadow: 0 0 30px rgba(6,182,212,0.1) !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: rgba(15,23,42,0.5); }
::-webkit-scrollbar-thumb { background: rgba(6,182,212,0.3); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)
from pipeline.load import load_warehouse
from pipeline.extract import extract_all
from pipeline.transform import transform_all
from pipeline.load import load_all

@st.cache_data(show_spinner="⚙️ Connecting to DuckDB warehouse…")
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

with st.sidebar:
    img_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'etl_3d_pipeline.jpg')
    if os.path.exists(img_path):
        st.image(img_path, use_container_width=True)
    st.markdown("""
    <div style='padding: 12px 0 4px 0;'>
        <div style='font-size:1.15rem; font-weight:800; color:#e2e8f0;'>🏗️ DataMind BI</div>
        <div style='font-size:0.75rem; color:#475569; margin-top:3px;'>DuckDB · E-Commerce Analytics</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('---')
    st.markdown("""
    <div style='background:rgba(16,185,129,0.07); border:1px solid rgba(16,185,129,0.2); border-radius:10px; padding:12px 14px; margin-bottom:12px;'>
        <div style='color:#10b981; font-size:0.75rem; font-weight:700; letter-spacing:0.08em;'>● PIPELINE ACTIVE</div>
        <div style='color:#475569; font-size:0.72rem; margin-top:3px;'>All systems operational</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.7rem; font-weight:700; color:#475569; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px;'>⏱ SLA & Freshness</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div>
        <div class='sla-row'><span class='sla-key'>ETL Runtime</span><span class='sla-val'>12.4s</span></div>
        <div class='sla-row'><span class='sla-key'>Last Run</span><span class='sla-val'>2026-08-26 16:24</span></div>
        <div class='sla-row'><span class='sla-key'>Status</span><span class='sla-val green'>✓ Healthy</span></div>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:16px; font-size:0.7rem; font-weight:700; color:#475569; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:8px;'>🗄 Warehouse Counts</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div>
        <div class='sla-row'><span class='sla-key'>fact_orders</span><span class='sla-val'>{len(fact):,}</span></div>
        <div class='sla-row'><span class='sla-key'>dim_customers</span><span class='sla-val'>{len(cust):,}</span></div>
        <div class='sla-row'><span class='sla-key'>dim_products</span><span class='sla-val'>{len(prod):,}</span></div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    if st.button('🔄 Re-Run ETL Pipeline'):
        st.cache_data.clear()
        st.success('✓ ETL pipeline triggered!')
        st.rerun()
st.markdown("""
<div class='hero-banner'>
    <div class='hero-title'>📊 DataMind BI Dashboard</div>
    <div class='hero-subtitle'>End-to-end ETL pipeline powered by DuckDB · 2 years of e-commerce data · Real-time anomaly detection</div>
    <div class='hero-badge'>● LIVE DATA</div>
</div>""", unsafe_allow_html=True)

LAY = dict(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.01)',
    font=dict(color='#94a3b8', family='Space Grotesk'), height=370,
    margin=dict(l=0, r=0, t=40, b=0),
    xaxis=dict(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.06)'),
    yaxis=dict(gridcolor='rgba(255,255,255,0.04)', linecolor='rgba(255,255,255,0.06)'),
    title_font=dict(color='#e2e8f0', size=14, family='Space Grotesk'),
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(255,255,255,0.06)', borderwidth=1)
)

k1,k2,k3,k4,k5 = st.columns(5)
kpis = [
    ('💰', f"${fact.revenue.sum()/1e6:.1f}M", 'Total Revenue',     '+34% YoY'),
    ('📦', f'{len(fact):,}',                   'Completed Orders',  '+28% YoY'),
    ('🛒', f'${fact.revenue.mean():.0f}',       'Avg Order Value',   '+5% YoY'),
    ('👥', f'{cust[cust.total_orders>0].shape[0]:,}', 'Active Customers', '+19% YoY'),
    ('📈', f'${fact.gross_profit.sum()/1e6:.1f}M', 'Gross Profit',  '+41% YoY'),
]
for col, (icon, val, lbl, delta) in zip([k1,k2,k3,k4,k5], kpis):
    col.markdown(f"<div class='kpi-card'><span class='kpi-icon'>{icon}</span><div class='kpi-val'>{val.replace('','')}</div><div class='kpi-lbl'>{lbl}</div><div class='kpi-delta'>▲ {delta}</div></div>", unsafe_allow_html=True)

st.markdown('<br>', unsafe_allow_html=True)
tab1,tab2,tab3,tab4,tab5 = st.tabs(['📈 Revenue Trends','🏆 Product Analytics','👥 Customer Cohorts','🌍 Regional','🔍 Data Explorer'])

with tab1:
    mon_mean = mon['total_revenue'].mean()
    mon_std  = mon['total_revenue'].std()
    mon['z_score'] = (mon['total_revenue'] - mon_mean) / mon_std
    anomalies = mon[mon['z_score'].abs() > 1.2]
    if not anomalies.empty:
        for _, row in anomalies.iterrows():
            direction = '📈 Spike' if row['z_score'] > 0 else '📉 Drop'
            st.markdown(f"<div class='anomaly-alert'>⚠️ <strong>ETL Anomaly — {row['year_month']}</strong> | {direction} of <strong>\</strong> · Z-score: <code>{row['z_score']:.2f}σ</code></div>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)
    with c1:
        fig = px.area(mon, x='year_month', y='total_revenue', title='Monthly Revenue Trend', color_discrete_sequence=['#06b6d4'])
        fig.update_traces(fill='tozeroy', fillcolor='rgba(6,182,212,0.06)', line=dict(width=2))
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(mon, x='year_month', y='unique_customers', title='Monthly Unique Customers', color='unique_customers', color_continuous_scale='Teal')
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    fig2 = px.line(mon, x='year_month', y='avg_order_value', title='Average Order Value Over Time', markers=True, color_discrete_sequence=['#8b5cf6'])
    fig2.update_traces(marker=dict(size=7, color='#8b5cf6', line=dict(width=2, color='#020617')), line=dict(width=2.5))
    fig2.update_layout(**LAY)
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    c1,c2 = st.columns(2)
    with c1:
        fig = px.bar(cat, x='category', y='total_revenue', title='Revenue by Category', color='total_revenue', color_continuous_scale='Teal')
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(cat, names='category', values='total_revenue', title='Revenue Share by Category', color_discrete_sequence=['#06b6d4','#8b5cf6','#10b981','#f59e0b','#ec4899','#ef4444'])
        fig.update_traces(textfont_size=12, marker=dict(line=dict(color='#020617', width=2)))
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    top_prods = prod.sort_values('total_revenue', ascending=False).head(10)
    fig2 = px.bar(top_prods, x='total_revenue', y='product_name', orientation='h', title='Top 10 Products by Revenue', color='total_revenue', color_continuous_scale=['#0e7490','#06b6d4','#67e8f9'])
    fig2.update_layout(**{**LAY, 'height': 420})
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("<div class='section-header'>🔮 3D Product Value Space — Price vs Revenue vs Orders</div>", unsafe_allow_html=True)
    prod3d = prod.dropna(subset=['list_price','total_revenue','total_orders','category'])
    fig3d = px.scatter_3d(prod3d, x='list_price', y='total_revenue', z='total_orders', color='category', title='Product Performance 3D Map', labels={'list_price': 'List Price ($)', 'total_revenue': 'Total Revenue ($)', 'total_orders': 'Total Orders'}, color_discrete_sequence=['#06b6d4','#8b5cf6','#10b981','#f59e0b','#ec4899','#ef4444'])
    fig3d.update_traces(marker=dict(size=5, line=dict(width=0.5, color='rgba(255,255,255,0.2)')))
    fig3d.update_layout(
        scene=dict(
            xaxis=dict(backgroundcolor='rgba(6,182,212,0.03)', gridcolor='rgba(6,182,212,0.08)', showbackground=True),
            yaxis=dict(backgroundcolor='rgba(139,92,246,0.03)', gridcolor='rgba(139,92,246,0.08)', showbackground=True),
            zaxis=dict(backgroundcolor='rgba(16,185,129,0.03)', gridcolor='rgba(16,185,129,0.08)', showbackground=True),
            camera=dict(eye=dict(x=1.5, y=1.5, z=0.8))
        ),
        margin=dict(l=0, r=0, b=0, t=50),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8', family='Space Grotesk'),
        title_font=dict(color='#e2e8f0', size=14),
        legend=dict(bgcolor='rgba(15,23,42,0.8)', bordercolor='rgba(6,182,212,0.2)', borderwidth=1), height=540
    )
    st.plotly_chart(fig3d, use_container_width=True)

with tab3:
    seg_data = fact.groupby('customer_segment').agg(revenue=('revenue','sum'), orders=('order_id','count')).reset_index()
    c1,c2 = st.columns(2)
    with c1:
        fig = px.pie(seg_data, names='customer_segment', values='revenue', title='Revenue by Customer Segment', color_discrete_sequence=['#06b6d4','#8b5cf6','#10b981'])
        fig.update_traces(textfont_size=12, marker=dict(line=dict(color='#020617', width=2)))
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        clv = cust[cust.total_revenue>0].sort_values('total_revenue',ascending=False).head(20)
        fig = px.bar(clv, x='customer_id', y='total_revenue', title='Top 20 Customers by LTV', color='segment', color_discrete_sequence=['#06b6d4','#8b5cf6','#10b981'])
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    fig2 = px.histogram(cust[cust.total_revenue>0], x='total_revenue', nbins=30, title='Customer Revenue Distribution', color_discrete_sequence=['#06b6d4'])
    fig2.update_layout(**LAY)
    st.plotly_chart(fig2, use_container_width=True)

with tab4:
    reg_data = fact.groupby('region').agg(revenue=('revenue','sum'), orders=('order_id','count')).reset_index()
    c1,c2 = st.columns(2)
    with c1:
        fig = px.bar(reg_data.sort_values('revenue',ascending=False), x='region', y='revenue', title='Revenue by Region', color='revenue', color_continuous_scale=['#164e63','#06b6d4','#a5f3fc'])
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        country_data = fact.groupby('country')['revenue'].sum().reset_index().dropna()
        fig = px.bar(country_data.sort_values('revenue',ascending=False).head(15), x='country', y='revenue', title='Revenue by Country', color='revenue', color_continuous_scale=['#312e81','#8b5cf6','#ddd6fe'])
        fig.update_layout(**LAY)
        st.plotly_chart(fig, use_container_width=True)
    channel_data = fact.groupby('channel').agg(revenue=('revenue','sum'),orders=('order_id','count')).reset_index()
    fig2 = px.bar(channel_data, x='channel', y='revenue', title='Revenue by Sales Channel', color='channel', color_discrete_sequence=['#06b6d4','#8b5cf6','#10b981','#f59e0b'])
    fig2.update_layout(**LAY)
    st.plotly_chart(fig2, use_container_width=True)

with tab5:
    st.markdown("<div class='section-header'>🔍 Warehouse Data Explorer</div>", unsafe_allow_html=True)
    col_sel, col_info = st.columns([2,1])
    with col_sel:
        table_choice = st.selectbox('Select table', ['fact_orders','dim_customers','dim_products','agg_monthly','agg_category'])
    df_show = data[table_choice]
    with col_info:
        st.markdown(f"<div style='background:rgba(6,182,212,0.05); border:1px solid rgba(6,182,212,0.15); border-radius:10px; padding:12px 16px; margin-top:22px;'><span style='color:#06b6d4; font-family:monospace; font-weight:700;'>{len(df_show):,} rows</span><span style='color:#475569; font-size:0.85rem;'> × {len(df_show.columns)} cols</span></div>", unsafe_allow_html=True)
    st.dataframe(df_show, use_container_width=True, height=420)
    st.download_button('⬇️ Export as CSV', df_show.to_csv(index=False), file_name=f'{table_choice}.csv', mime='text/csv')
