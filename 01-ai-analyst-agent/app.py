"""
DataGPT — Fully Dynamic AI Analyst & Dashboard Generator
Robust Column Selection & Clean Plotly Chart Rendering (Fixes Blank Box & Slipped Donut Chart)
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

from agent.tools import load_data, run_query, build_dashboard, get_kpi_metrics

st.set_page_config(
    page_title="DataGPT — AI Analyst Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Clean CSS Injection ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
  color: #1e293b !important;
}

[data-testid="stAppViewContainer"] { background-color: #f8fafc !important; }
[data-testid="stHeader"] { display: none !important; }
[data-testid="block-container"] { padding: 1.5rem 2rem !important; max-width: 100% !important; }

/* Sidebar - Dark Navigation (#0f172a) */
[data-testid="stSidebar"] {
  background-color: #0f172a !important; border-right: none !important;
  box-shadow: 4px 0 24px rgba(0,0,0,0.12) !important;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] label {
  font-size: 11px !important; font-weight: 700 !important;
  color: #64748b !important; text-transform: uppercase !important;
  letter-spacing: 0.8px !important;
}
[data-testid="stSidebar"] input {
  background: #1e293b !important; border: 1px solid #334155 !important;
  color: #f8fafc !important; border-radius: 10px !important; font-size: 13px !important;
}
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
  background: rgba(255,255,255,0.03) !important;
  border: 1.5px dashed rgba(255,255,255,0.15) !important; border-radius: 12px !important;
}
[data-testid="stSidebar"] .stButton > button {
  background: #1e293b !important; border: 1px solid #334155 !important;
  color: #f1f5f9 !important; border-radius: 10px !important; font-weight: 600 !important;
  font-size: 13px !important; transition: all 0.2s !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: #2563eb !important; border-color: #2563eb !important; color: #ffffff !important;
}

/* Header Component */
.header-row {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 20px; background: #ffffff; padding: 16px 22px;
  border-radius: 18px; border: 1px solid #e2e8f0; box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}
.greeting-title {
  font-size: 22px; font-weight: 800; color: #0f172a; letter-spacing: -0.4px; margin: 0;
}
.greeting-sub { font-size: 12.5px; color: #64748b; margin-top: 2px; font-weight: 500; }
.hdr-badge {
  background: #eff6ff; border: 1px solid #bfdbfe; color: #2563eb;
  padding: 5px 12px; border-radius: 20px; font-size: 12px; font-weight: 600;
}

/* Top Row Cards - Fixed 175px Height for Perfect Alignment */
.top-card-box {
  background: #ffffff; border-radius: 20px; padding: 18px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02); border: 1px solid #f1f5f9;
  height: 175px; display: flex; flex-direction: column; justify-content: space-between;
  margin-bottom: 16px;
}
.card-header-sm {
  display: flex; justify-content: space-between; align-items: center;
  color: #475569; font-size: 13px; font-weight: 600;
}
.big-metric-sm {
  font-size: 30px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px;
  display: flex; align-items: center; gap: 8px; line-height: 1.1; margin: 4px 0;
}
.tag-pill {
  font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 12px;
  display: inline-flex; align-items: center; gap: 3px;
}
.tag-green { background: #dcfce7; color: #16a34a; }
.tag-blue { background: #e0f2fe; color: #0284c7; }

/* Segmented Bar Visualizer */
.segmented-bar {
  display: flex; gap: 4px; height: 20px; align-items: flex-end; margin-top: 6px;
}
.seg-block { flex: 1; height: 18px; border-radius: 3px; }
.seg-cyan { background: #00c8b3; }
.seg-blue { background: #2563eb; }
.seg-gray { background: #e2e8f0; }

/* Contacts Blue Card (Top Right - Fixed 175px Height) */
.top-contacts-card-blue {
  background: linear-gradient(160deg, #1e40af 0%, #2563eb 100%);
  border-radius: 20px; padding: 18px 20px; color: #ffffff !important;
  box-shadow: 0 8px 24px rgba(37, 99, 235, 0.28); height: 175px;
  display: flex; flex-direction: column; justify-content: space-between;
  margin-bottom: 16px;
}
.top-contacts-card-blue * { color: #ffffff !important; }

/* White Mini Bars inside Blue Card */
.chart-bars-white {
  display: flex; gap: 6px; height: 50px; align-items: flex-end; margin-top: 6px;
}
.bar-w {
  flex: 1; background: rgba(255,255,255,0.85); border-radius: 4px 4px 0 0;
}

/* Middle / Standard Cards */
.card-box {
  background: #ffffff; border-radius: 20px; padding: 18px 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02); border: 1px solid #f1f5f9;
  position: relative; margin-bottom: 16px;
}

/* Contact Item List */
.contact-row {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 0; border-bottom: 1px solid #f1f5f9; font-size: 13px;
}
.contact-row:last-child { border-bottom: none; }
.c-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 8px; }

/* Dark Widget */
.dark-widget {
  background: #18181b; border-radius: 20px; padding: 18px 20px; color: #ffffff !important;
  box-shadow: 0 8px 24px rgba(0,0,0,0.25);
}
.dark-widget * { color: #ffffff !important; }

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
  background: #ffffff !important; border-radius: 14px !important;
  padding: 5px !important; gap: 5px !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.03) !important;
  border: 1px solid #e2e8f0 !important; margin-bottom: 16px !important;
}
.stTabs [data-baseweb="tab"] {
  border-radius: 10px !important; padding: 8px 18px !important;
  font-weight: 600 !important; font-size: 13px !important; color: #64748b !important;
}
.stTabs [aria-selected="true"] {
  background: #2563eb !important; color: #ffffff !important;
}
.stTabs [data-baseweb="tab-panel"] {
  background: transparent !important; border: none !important; padding: 0 !important;
}

.stButton > button {
  background: #2563eb !important; color: white !important;
  font-weight: 600 !important; border-radius: 10px !important; padding: 8px 18px !important;
  border: none !important; transition: all 0.2s !important;
}
.stButton > button:hover {
  background: #1d4ed8 !important; transform: translateY(-1px) !important;
}
.user-bubble {
  background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 14px;
  padding: 12px 16px; margin: 8px 0; color: #1e3a8a; font-size: 13.5px;
}
.agent-bubble {
  background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
  padding: 12px 16px; margin: 8px 0; color: #0f172a; font-size: 13.5px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.02);
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar Navigation & File Upload ─────────────────────────────────────────
with st.sidebar:
    st.markdown("<h2 style='color:#fff;font-weight:800;font-size:22px;'>🤖 DataGPT</h2>", unsafe_allow_html=True)
    st.caption("AI Data Analyst Agent")
    st.divider()

    st.markdown("**📂 CSV Data Source**")
    uploaded_file = st.file_uploader("Upload custom CSV", type=["csv"], label_visibility="collapsed")
    if uploaded_file is not None:
        try:
            _df = pd.read_csv(uploaded_file)
            for col in _df.columns:
                if any(k in col.lower() for k in ("date", "time", "timestamp", "created")):
                    try: _df[col] = pd.to_datetime(_df[col])
                    except Exception: pass
            st.session_state.uploaded_df = _df
            st.session_state.uploaded_filename = uploaded_file.name
            st.success(f"✅ Loaded {len(_df):,} rows")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    else:
        if "uploaded_df" in st.session_state:
            del st.session_state.uploaded_df
        st.caption("Using default e-commerce dataset")

    st.divider()
    st.markdown("**🔑 API Key Settings**")
    openai_key = st.text_input("OpenAI Key", type="password", placeholder="sk-...", label_visibility="collapsed")
    demo_mode = not bool(openai_key)
    if demo_mode:
        st.info("🎭 Demo Mode Active")


    st.divider()
    if st.button("🔄 Reset Conversation", use_container_width=True):
        st.session_state.chat = []
        st.rerun()

# ── Load Active Dataset ───────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

df = st.session_state.get("uploaded_df", get_data())

if "chat" not in st.session_state:
    st.session_state.chat = []

# ── Dynamic Clean Header Bar ──────────────────────────────────────────────────
dataset_name = st.session_state.get("uploaded_filename", "ecommerce_sales.csv")
total_rows = len(df)
total_cols = len(df.columns)

st.markdown(f"""
<div class="header-row">
  <div>
    <h1 class="greeting-title">🤖 DataGPT Analytics Dashboard</h1>
    <div class="greeting-sub">Active Dataset: <b>{dataset_name}</b> &nbsp;•&nbsp; {total_rows:,} rows &nbsp;•&nbsp; {total_cols} columns</div>
  </div>
  <div class="hdr-badge">
    ⚡ Live Sync & Auto-Calculated
  </div>
</div>
""", unsafe_allow_html=True)

# ── Main Tabs ─────────────────────────────────────────────────────────────────
tab_dash, tab_ai, tab_preview, tab_stats = st.tabs([
    "🎛️ Dynamic Dashboard",
    "💬 AI Analyst Assistant",
    "📋 Dataset Preview",
    "📊 Data Profile & Stats"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1: 🎛️ 100% DYNAMIC DASHBOARD GENERATED FROM USER DATASET
# ══════════════════════════════════════════════════════════════════════════════
with tab_dash:

    # ── Robust Smart Column Selection Heuristics ─────────────────────────────
    all_num_cols = df.select_dtypes(include='number').columns.tolist()
    all_cat_cols = df.select_dtypes(include='object').columns.tolist()
    date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]

    # Exclude year/date/ID/index columns from being chosen as primary numerical metric
    metric_num_candidates = [
        c for c in all_num_cols 
        if not any(k in c.lower() for k in ('year', 'date', 'month', 'day', 'zip', 'code', 'id', 'returned', 'status', 'is_'))
        and df[c].std() > 0
    ]
    # Prioritize revenue/sales/amount/units
    high_priority_num = [c for c in metric_num_candidates if any(k in c.lower() for k in ('revenue', 'sales', 'amount', 'unit', 'price', 'quantity', 'qty', 'cost', 'profit', 'total'))]
    
    if high_priority_num:
        primary_num = high_priority_num[0]
    elif metric_num_candidates:
        primary_num = metric_num_candidates[0]
    elif all_num_cols:
        primary_num = all_num_cols[0]
    else:
        primary_num = None

    secondary_num = [c for c in metric_num_candidates if c != primary_num]
    secondary_num = secondary_num[0] if secondary_num else primary_num

    # Filter out categories with 1 unique value or unique values > 90% rows
    meaningful_cat_cols = [
        c for c in all_cat_cols 
        if 1 < df[c].nunique() < len(df) * 0.85
        and not any(id_kw in c.lower() for id_kw in ('id', 'code', 'num', 'key'))
    ]
    primary_cat = meaningful_cat_cols[0] if meaningful_cat_cols else (all_cat_cols[0] if all_cat_cols else None)

    # 1. Top Row: 3 Fixed Height Cards
    col_t1, col_t2, col_t3 = st.columns([1.1, 1.1, 0.9])

    with col_t1:
        if 'is_returned' in df.columns:
            succ_rate = (1 - df['is_returned'].mean()) * 100
            label_text = "Success Rate"
            val_text = f"{succ_rate:.1f}%"
            pending_text = f"{(100-succ_rate):.1f}% returned"
        elif primary_num:
            val = df[primary_num].sum()
            label_text = f"Total {primary_num.replace('_',' ').title()}"
            val_text = f"${val:,.0f}" if 'rev' in primary_num or 'price' in primary_num else f"{val:,.0f}"
            pending_text = f"Avg: {df[primary_num].mean():,.1f}"
        else:
            label_text = "Total Records"
            val_text = f"{len(df):,}"
            pending_text = f"{len(df.columns)} columns"

        st.markdown(f"""
        <div class="top-card-box">
          <div class="card-header-sm">
            <span>{label_text}</span>
            <span>:::</span>
          </div>
          <div class="big-metric-sm">
            {val_text}
            <span class="tag-pill tag-green">↗ Active</span>
            <span style="font-size:11px;color:#94a3b8;font-weight:500;margin-left:auto;">{pending_text}</span>
          </div>
          <div class="segmented-bar">
            <div class="seg-block seg-cyan"></div>
            <div class="seg-block seg-cyan"></div>
            <div class="seg-block seg-cyan"></div>
            <div class="seg-block seg-cyan"></div>
            <div class="seg-block seg-cyan"></div>
            <div class="seg-block seg-cyan"></div>
            <div class="seg-block seg-cyan"></div>
            <div class="seg-block seg-cyan"></div>
            <div class="seg-block seg-blue"></div>
            <div class="seg-block seg-gray"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_t2:
        if primary_cat:
            cat_count = df[primary_cat].nunique()
            cat_label = f"Unique {primary_cat.replace('_',' ').title()}"
        else:
            cat_count = len(df.columns)
            cat_label = "Total Attributes"

        st.markdown(f"""
        <div class="top-card-box">
          <div class="card-header-sm">
            <span>{cat_label}</span>
            <span>:::</span>
          </div>
          <div class="big-metric-sm">
            {cat_count}
            <span class="tag-pill tag-blue">Active Categories</span>
          </div>
          <div style="display:flex;gap:4px;height:18px;align-items:flex-end;margin-top:8px;">
            <div style="flex:1;height:12px;background:#3b82f6;border-radius:3px;"></div>
            <div style="flex:1;height:16px;background:#3b82f6;border-radius:3px;"></div>
            <div style="flex:1;height:14px;background:#3b82f6;border-radius:3px;"></div>
            <div style="flex:1;height:18px;background:#3b82f6;border-radius:3px;"></div>
            <div style="flex:1;height:15px;background:#3b82f6;border-radius:3px;"></div>
            <div style="flex:1;height:10px;background:#3b82f6;border-radius:3px;"></div>
            <div style="flex:1;height:16px;background:#3b82f6;border-radius:3px;"></div>
            <div style="flex:1;height:12px;background:#e2e8f0;border-radius:3px;"></div>
            <div style="flex:1;height:14px;background:#e2e8f0;border-radius:3px;"></div>
            <div style="flex:1;height:10px;background:#e2e8f0;border-radius:3px;"></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_t3:
        if primary_num:
            num_sum = df[primary_num].sum()
            num_fmt = f"${num_sum:,.0f}" if ('revenue' in primary_num or 'price' in primary_num) else f"{num_sum:,.0f}"
            lbl_title = primary_num.replace('_',' ').title()
        else:
            num_fmt = f"{len(df):,}"
            lbl_title = "Total Rows"

        if date_cols and primary_num:
            d_df = df.set_index(date_cols[0]).resample('ME')[primary_num].sum().head(7)
            bars = [int(v/d_df.max()*40)+10 if d_df.max()>0 else 20 for v in d_df.values]
            while len(bars) < 7: bars.append(20)
        else:
            bars = [25, 40, 28, 35, 45, 30, 50]

        bars_html = "".join([f'<div class="bar-w" style="height:{h}px;"></div>' for h in bars[:6]])
        bars_html += f'<div class="bar-w" style="height:{bars[6] if len(bars)>6 else 50}px;background:#ffffff;box-shadow:0 0 8px rgba(255,255,255,0.8);"></div>'

        st.markdown(f"""
        <div class="top-contacts-card-blue">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span style="font-size:13px;font-weight:600;">{lbl_title} Overview</span>
            <span style="opacity:0.7;">:::</span>
          </div>
          <div>
            <div style="font-size:28px;font-weight:800;line-height:1;">{num_fmt}</div>
            <div style="font-size:11px;opacity:0.85;margin-top:2px;">Calculated from {len(df):,} records</div>
          </div>
          <div class="chart-bars-white">
            {bars_html}
          </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. Middle Row: Top Category Breakdown & Donut Chart
    col_m1, col_m2 = st.columns([1.1, 0.9])

    with col_m1:
        rows_list = []
        if primary_cat and primary_num:
            top_grp = df.groupby(primary_cat)[primary_num].sum().reset_index().sort_values(primary_num, ascending=False).head(4)
            tot = df[primary_num].sum()
            colors = ['#00c8b3', '#2563eb', '#93c5fd', '#64748b']
            for i, (_, row) in enumerate(top_grp.iterrows()):
                pct = (row[primary_num] / tot * 100) if tot > 0 else 0
                val_str = f"${row[primary_num]:,.0f}" if ('revenue' in primary_num or 'price' in primary_num) else f"{row[primary_num]:,.0f}"
                c_name = str(row[primary_cat])[:25]
                c_color = colors[i % len(colors)]
                rows_list.append(f'<div class="contact-row"><div><span class="c-dot" style="background:{c_color};"></span><b>{c_name}</b></div><div><span style="color:#94a3b8;margin-right:12px;">{pct:.1f}%</span><b>{val_str}</b></div></div>')
            rows_html = "".join(rows_list)
        else:
            rows_html = f"<div style='padding:14px;color:#94a3b8;font-size:13px;'>Dataset loaded with {len(df)} records.</div>"

        cat_header_title = primary_cat.replace('_',' ').title() if primary_cat else 'Group'
        st.markdown(f"""
        <div class="card-box" style="height:250px;">
          <div class="card-header">
            <span>Top Breakdown by {cat_header_title}</span>
            <span style="font-size:12px;color:#94a3b8;">Sorted ∨</span>
          </div>
          {rows_html}
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        # Donut Chart - Rendered inside container cleanly
        if primary_cat and primary_num:
            pie_df = df.groupby(primary_cat)[primary_num].sum().reset_index().head(5)
            fig_donut = go.Figure(data=[go.Pie(
                labels=pie_df[primary_cat].astype(str),
                values=pie_df[primary_num],
                hole=.68,
                marker_colors=['#18181b', '#00c8b3', '#2563eb', '#3b82f6', '#93c5fd'],
                textinfo='percent', hoverinfo='label+value+percent'
            )])
        else:
            fig_donut = go.Figure(data=[go.Pie(labels=['Data A', 'Data B', 'Data C'], values=[40,30,30], hole=.68)])

        chart_title = primary_num.replace("_"," ").title() if primary_num else "Share"
        fig_donut.update_layout(
            title=dict(text=f"<b>{chart_title} Share</b>", font=dict(family="Plus Jakarta Sans", size=13, color="#475569")),
            showlegend=True, margin=dict(t=35, b=10, l=10, r=10), height=240,
            paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02, font=dict(family='Plus Jakarta Sans', size=11, color='#475569'))
        )
        st.plotly_chart(fig_donut, use_container_width=True, key="clean_dynamic_donut_fixed")

    # 3. Bottom Row: Stacked Bar & Dark Widget
    col_b1, col_b2 = st.columns([1.35, 0.65])

    with col_b1:
        if date_cols and primary_num:
            t_df = df.copy()
            t_df['Month'] = t_df[date_cols[0]].dt.strftime('%b')
            t_df['Month_num'] = t_df[date_cols[0]].dt.month
            m_grp = t_df.groupby(['Month_num', 'Month'])[primary_num].sum().reset_index().sort_values('Month_num')

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(x=m_grp['Month'], y=m_grp[primary_num], name=primary_num.title(), marker_color='#3b82f6'))
            if secondary_num and secondary_num != primary_num:
                m_grp2 = t_df.groupby(['Month_num', 'Month'])[secondary_num].sum().reset_index().sort_values('Month_num')
                fig_bar.add_trace(go.Bar(x=m_grp2['Month'], y=m_grp2[secondary_num], name=secondary_num.title(), marker_color='#93c5fd'))
        elif primary_cat and primary_num:
            c_grp = df.groupby(primary_cat)[primary_num].sum().reset_index().head(10)
            fig_bar = go.Figure(data=[go.Bar(x=c_grp[primary_cat], y=c_grp[primary_num], marker_color='#3b82f6')])
        else:
            fig_bar = go.Figure(data=[go.Bar(x=['A','B','C'], y=[10,20,30], marker_color='#3b82f6')])

        fig_bar.update_layout(
            title=dict(text="<b>Trend & Breakdown</b>", font=dict(family="Plus Jakarta Sans", size=13, color="#475569")),
            barmode='stack', height=240, margin=dict(t=35, b=20, l=20, r=10),
            showlegend=False, paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
            xaxis=dict(showgrid=False, tickfont=dict(family='Plus Jakarta Sans', size=10, color='#94a3b8')),
            yaxis=dict(showgrid=True, gridcolor='#f1f5f9', tickfont=dict(family='Plus Jakarta Sans', size=10, color='#94a3b8'))
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="clean_dynamic_bar_fixed")

    with col_b2:
        avg_val = df[primary_num].mean() if primary_num else len(df)
        avg_fmt = f"${avg_val:,.0f}" if (primary_num and ('rev' in primary_num or 'price' in primary_num)) else f"{avg_val:,.1f}"
        metric_name = primary_num.replace('_',' ').title() if primary_num else 'Metric'

        st.markdown(f"""
        <div class="card-box" style="padding:14px 18px;margin-bottom:12px;">
          <div class="card-header" style="margin-bottom:4px;">
            <span>Average {metric_name}</span>
            <span>:::</span>
          </div>
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
              <span style="font-size:24px;font-weight:800;color:#0f172a;">{avg_fmt}</span>
              <span style="font-size:11px;color:#94a3b8;margin-left:6px;">Average / row</span>
            </div>
            <div style="width:28px;height:28px;border-radius:50%;background:#0f172a;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;cursor:pointer;">+</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        if date_cols and primary_num:
            a_df = df.set_index(date_cols[0]).resample('D')[primary_num].sum().reset_index().head(30)
            a_x, a_y = a_df[date_cols[0]].dt.strftime('%d %b'), a_df[primary_num]
        elif primary_num:
            a_x, a_y = list(range(1, 15)), df[primary_num].head(14).values
        else:
            a_x, a_y = [1, 2, 3, 4], [10, 25, 15, 30]

        fig_area = go.Figure(data=[go.Scatter(
            x=list(a_x), y=list(a_y), mode='lines', fill='tozeroy',
            line=dict(color='#ffffff', width=2), fillcolor='rgba(255,255,255,0.08)'
        )])
        fig_area.update_layout(
            height=65, margin=dict(t=5, b=15, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, tickfont=dict(family='Plus Jakarta Sans', size=9, color='#94a3b8')),
            yaxis=dict(showgrid=False, showticklabels=False)
        )

        vol_name = primary_num.replace("_"," ").title() if primary_num else "Volume"
        st.markdown('<div class="dark-widget">', unsafe_allow_html=True)
        st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;"><span style="font-size:12px;font-weight:600;color:#cbd5e1;">Total {vol_name}</span><span style="font-size:11px;color:#94a3b8;">Dataset ∨</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:26px;font-weight:800;line-height:1;">{num_fmt}</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:10.5px;color:#94a3b8;margin-top:2px;">Calculated live &nbsp;<span class="tag-pill tag-green" style="background:rgba(34,197,94,0.2);color:#4ade80;">↗ Live</span></div>', unsafe_allow_html=True)
        st.plotly_chart(fig_area, use_container_width=True, key="clean_dynamic_dark_area_fixed")
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. Auto-Generated Charts Section
    st.markdown("<h4 style='margin-top:20px;margin-bottom:12px;font-weight:700;'>📊 Additional Auto-Generated Visualizations</h4>", unsafe_allow_html=True)
    try:
        raw_figs = build_dashboard(df)
        if raw_figs:
            d_cols = st.columns(2)
            for i, (name, fig) in enumerate(raw_figs):
                with d_cols[i % 2]:
                    st.plotly_chart(fig, use_container_width=True, key=f"clean_auto_dash_fig_fixed_{i}")
    except Exception as e:
        st.error(f"Dashboard generator error: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2: 💬 AI ANALYST ASSISTANT
# ══════════════════════════════════════════════════════════════════════════════
with tab_ai:
    st.markdown("<h3 style='margin-bottom:12px;font-weight:700;'>🤖 Ask DataGPT AI Agent</h3>", unsafe_allow_html=True)
    
    suggestions = [
        "📈 Show monthly revenue trend",
        "🏆 Which product category makes most revenue?",
        "🌍 Top 5 countries by sales",
        "📦 Refund rate by category",
    ]
    q_cols = st.columns(4)
    for i, sug in enumerate(suggestions):
        with q_cols[i]:
            if st.button(sug, key=f"clean_ai_sug_fixed_{i}", use_container_width=True):
                st.session_state.pending = sug.split(" ", 1)[1]
                st.rerun()

    for idx, turn in enumerate(st.session_state.chat):
        st.markdown(f"<div class='user-bubble'>👤 <strong>You:</strong> {turn['question']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='agent-bubble'>🤖 <strong>DataGPT:</strong> {turn['insight']}</div>", unsafe_allow_html=True)
        if turn.get("fig"):
            st.plotly_chart(turn["fig"], use_container_width=True, key=f"clean_chat_fig_fixed_{idx}")
        if turn.get("table") is not None:
            st.dataframe(turn["table"], use_container_width=True, height=200, key=f"clean_chat_tbl_fixed_{idx}")

    question = st.chat_input("Ask a business question about your data...")
    if hasattr(st.session_state, "pending"):
        question = st.session_state.pending
        del st.session_state.pending

    if question:
        with st.spinner("🤖 DataGPT analyzing data..."):
            result = run_query(df, question, demo_mode=demo_mode, api_key=openai_key or None)
        st.session_state.chat.append({"question": question, **result})
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3: 📋 DATASET PREVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab_preview:
    st.dataframe(df.head(50), use_container_width=True, height=450)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4: 📊 DATA PROFILE & STATS
# ══════════════════════════════════════════════════════════════════════════════
with tab_stats:
    st.markdown("#### Automated Data Profile")
    stats_df = df.describe(include="all").T.fillna("-")
    st.dataframe(stats_df, use_container_width=True, height=300)
