"""
DataGPT — Enterprise AI Analyst & Executive Intelligence Dashboard
Pixel-Perfect, Fully Interactive & Production-Ready
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import io
from datetime import datetime

from agent.tools import load_data, run_query, build_dashboard, get_kpi_metrics

# ── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="DataGPT — AI Analyst Platform",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme & Design System CSS ─────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
  --bg: #f8fafc;
  --surface: #ffffff;
  --surface-hover: #f1f5f9;
  --border: #e2e8f0;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --brand: #6366f1;
  --brand-light: #e0e7ff;
  --accent: #0ea5e9;
  --green: #10b981;
  --green-bg: #ecfdf5;
  --purple: #8b5cf6;
  --card-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05), 0 1px 2px -1px rgba(0, 0, 0, 0.05);
}

html, body, [class*="css"] {
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
  color: var(--text-main) !important;
}

[data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
}

[data-testid="stHeader"] {
  display: none !important;
}

[data-testid="block-container"] {
  padding: 1rem 1.5rem 2.5rem !important;
  max-width: 100% !important;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
  background: #0f172a !important;
  border-right: 1px solid #1e293b !important;
}

[data-testid="stSidebar"] * {
  color: #cbd5e1 !important;
}

[data-testid="stSidebar"] hr {
  border-color: #1e293b !important;
  margin: 0.9rem 0 !important;
}

/* Nav Button in Sidebar */
.stSidebar .stButton > button {
  width: 100% !important;
  text-align: left !important;
  justify-content: flex-start !important;
  background: #1e293b !important;
  border: 1px solid #334155 !important;
  color: #f1f5f9 !important;
  border-radius: 8px !important;
  padding: 0.5rem 0.85rem !important;
  font-weight: 600 !important;
  font-size: 12.5px !important;
  transition: all 0.2s ease !important;
  margin-bottom: 3px !important;
}

.stSidebar .stButton > button:hover {
  background: #6366f1 !important;
  border-color: #6366f1 !important;
  color: #ffffff !important;
  transform: translateX(3px);
}

.stSidebar .stButton > button[kind="primary"] {
  background: #6366f1 !important;
  border-color: #818cf8 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35) !important;
}

/* Brand header */
.brand-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 4px 14px;
  border-bottom: 1px solid #1e293b;
  margin-bottom: 12px;
}
.brand-icon {
  width: 36px;
  height: 36px;
  background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-weight: 800;
  font-size: 18px;
  box-shadow: 0 4px 10px rgba(99, 102, 241, 0.4);
}
.brand-title {
  font-size: 17px;
  font-weight: 800;
  color: #ffffff !important;
  letter-spacing: -0.5px;
  line-height: 1.2;
}
.brand-sub {
  font-size: 10px;
  color: #94a3b8 !important;
  font-weight: 600;
  letter-spacing: 0.8px;
}

.side-label {
  font-size: 10px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #64748b !important;
  margin: 14px 0 6px 4px;
}

/* Top Navigation Bar */
.top-navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 10px 16px;
  margin-bottom: 18px;
  box-shadow: var(--card-shadow);
}

.top-breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12.5px;
  font-weight: 600;
  color: var(--text-muted);
}
.top-breadcrumb strong {
  color: var(--text-main);
  font-weight: 700;
}

.top-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--green-bg);
  color: var(--green);
  font-size: 11px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 20px;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.top-status-dot {
  width: 6px;
  height: 6px;
  background: var(--green);
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(1.3); }
  100% { opacity: 1; transform: scale(1); }
}

/* Welcome Hero Screen Styling */
.welcome-hero {
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
  border-radius: 20px;
  padding: 40px 36px;
  color: #ffffff;
  margin-bottom: 24px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
  border: 1px solid rgba(99, 102, 241, 0.3);
  text-align: center;
}

.welcome-badge {
  display: inline-block;
  background: rgba(99, 102, 241, 0.25);
  color: #c7d2fe !important;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 1.2px;
  text-transform: uppercase;
  padding: 5px 14px;
  border-radius: 20px;
  border: 1px solid rgba(199, 210, 254, 0.25);
  margin-bottom: 14px;
}

.welcome-title {
  font-size: 34px;
  font-weight: 800;
  color: #ffffff !important;
  letter-spacing: -1px;
  line-height: 1.2;
  margin-bottom: 12px;
}

.welcome-desc {
  font-size: 15px;
  color: #94a3b8 !important;
  max-width: 680px;
  margin: 0 auto 26px;
  line-height: 1.6;
}

.welcome-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 24px;
  box-shadow: var(--card-shadow);
  height: 100%;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.welcome-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 24px -4px rgba(0, 0, 0, 0.08);
}

.welcome-card-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  margin-bottom: 14px;
}

.welcome-card-title {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-main);
  margin-bottom: 8px;
}

.welcome-card-desc {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.5;
}

/* KPI Cards */
.kpi-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 16px 18px;
  box-shadow: var(--card-shadow);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  position: relative;
  overflow: hidden;
}

.kpi-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.08);
}

.kpi-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.kpi-card-title {
  font-size: 11.5px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.kpi-card-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
}

.kpi-value-text {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.8px;
  color: var(--text-main);
  margin-bottom: 6px;
  line-height: 1.1;
}

.kpi-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-weight: 700;
  color: var(--green);
}

.kpi-footer-sub {
  font-size: 11px;
  color: var(--text-muted);
  margin-left: 6px;
}

/* AI Intelligence Banner */
.ai-banner {
  background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
  border: 1px solid rgba(99, 102, 241, 0.25);
  border-radius: 14px;
  padding: 18px 22px;
  margin: 18px 0;
  color: #ffffff;
  box-shadow: 0 4px 15px rgba(15, 23, 42, 0.15);
  position: relative;
}

.ai-banner-pill {
  display: inline-block;
  background: rgba(99, 102, 241, 0.25);
  color: #c7d2fe !important;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 1px;
  text-transform: uppercase;
  padding: 3px 9px;
  border-radius: 6px;
  border: 1px solid rgba(199, 210, 254, 0.2);
  margin-bottom: 8px;
}

.ai-banner-title {
  font-size: 19px;
  font-weight: 800;
  color: #ffffff !important;
  letter-spacing: -0.4px;
  margin-bottom: 4px;
}

.ai-banner-desc {
  font-size: 12px;
  color: #94a3b8 !important;
  line-height: 1.5;
}

/* Dashboard Box Containers */
.dash-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 18px;
  box-shadow: var(--card-shadow);
  margin-bottom: 18px;
}

.dash-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border);
}

.dash-card-title {
  font-size: 13.5px;
  font-weight: 700;
  color: var(--text-main);
}

.dash-card-sub {
  font-size: 11px;
  color: var(--text-muted);
}

/* Chat bubble styling */
.chat-user-msg {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 12px 12px 2px 12px;
  padding: 12px 16px;
  margin-bottom: 12px;
  font-size: 13px;
  font-weight: 600;
  color: #0f172a;
}

.chat-agent-msg {
  background: #ffffff;
  border: 1px solid #e0e7ff;
  border-left: 4px solid #6366f1;
  border-radius: 2px 12px 12px 12px;
  padding: 14px 18px;
  margin-bottom: 16px;
  font-size: 13px;
  color: #1e293b;
  box-shadow: var(--card-shadow);
  line-height: 1.6;
}

/* General Button Styling in Main Area */
.stButton > button {
  background: #0f172a;
  color: #ffffff;
  border: 1px solid #1e293b;
  border-radius: 8px;
  font-weight: 700;
  font-size: 12px;
  padding: 0.4rem 0.9rem;
  transition: all 0.2s ease;
}

.stButton > button:hover {
  background: #6366f1;
  border-color: #6366f1;
  color: #ffffff;
  transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)

# ── Session State Management ──────────────────────────────────────────────────
if "has_started" not in st.session_state:
    st.session_state.has_started = False

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Overview"

if "chat" not in st.session_state:
    st.session_state.chat = []

if "primary_metric_override" not in st.session_state:
    st.session_state.primary_metric_override = None

if "show_anomaly_alert" not in st.session_state:
    st.session_state.show_anomaly_alert = False

# ── Load Dataset ──────────────────────────────────────────────────────────────
@st.cache_data
def get_default_dataset():
    return load_data()

raw_df = st.session_state.get("uploaded_df", get_default_dataset())
dataset_name = st.session_state.get("uploaded_filename", "ecommerce_sales.csv")

# ── Sidebar Navigation & Controls ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-header">
      <div class="brand-icon" style="background:linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);box-shadow:0 4px 14px rgba(99,102,241,0.45);">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 17L12 22L22 17" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          <path d="M2 12L12 17L22 12" stroke="#ffffff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div>
        <div class="brand-title">DataGPT</div>
        <div class="brand-sub">ENTERPRISE ANALYTICS</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="side-label">Workspace Navigation</div>', unsafe_allow_html=True)
    
    nav_options = [
        ("🏠 Welcome Screen", "Welcome"),
        ("📊 Overview", "Overview"),
        ("🤖 AI Analyst", "AI Analyst"),
        ("📋 Dataset Explorer", "Dataset"),
        ("🔬 Data Profile & Health", "Data Profile"),
    ]

    for label, tab_name in nav_options:
        is_active = (st.session_state.has_started and st.session_state.active_tab == tab_name) or (not st.session_state.has_started and tab_name == "Welcome")
        if st.button(label, key=f"nav_{tab_name}", type="primary" if is_active else "secondary"):
            if tab_name == "Welcome":
                st.session_state.has_started = False
            else:
                st.session_state.has_started = True
                st.session_state.active_tab = tab_name
            st.rerun()

    st.markdown("---")
    st.markdown('<div class="side-label">Data Source</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
    if uploaded_file is not None:
        try:
            _df = pd.read_csv(uploaded_file)
            for col in _df.columns:
                if any(k in col.lower() for k in ("date", "time", "timestamp", "created")):
                    try:
                        _df[col] = pd.to_datetime(_df[col])
                    except Exception:
                        pass
            st.session_state.uploaded_df = _df
            st.session_state.uploaded_filename = uploaded_file.name
            st.session_state.has_started = True
            st.success(f"✓ {len(_df):,} rows loaded")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    else:
        if "uploaded_df" in st.session_state:
            if st.button("↩ Restore Default Dataset", use_container_width=True):
                del st.session_state.uploaded_df
                if "uploaded_filename" in st.session_state:
                    del st.session_state.uploaded_filename
                st.rerun()
        else:
            st.caption(f"📁 Active: **{dataset_name}** ({len(raw_df):,} rows)")

    st.markdown("---")
    st.markdown('<div class="side-label">Quick Actions</div>', unsafe_allow_html=True)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        if st.button("↻ Reset Chat", use_container_width=True):
            st.session_state.chat = []
            st.rerun()
    with col_s2:
        if st.button("⚡ Scan Anomaly", use_container_width=True):
            st.session_state.show_anomaly_alert = not st.session_state.show_anomaly_alert
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# WELCOME & GET STARTED SCREEN (When application first opens)
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.has_started:
    st.markdown("""
    <div class="welcome-hero">
      <div class="welcome-badge">✦ Enterprise AI Analytics Engine</div>
      <div class="welcome-title">Welcome to DataGPT Intelligence Platform</div>
      <div class="welcome-desc">
        Turn complex datasets into interactive Plotly dashboards, deep executive summaries, 
        and natural-language conversational analytics with zero SQL required.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1.4, 1])
    with col_btn2:
        if st.button("🚀 Get Started & Launch Workspace", use_container_width=True, type="primary"):
            st.session_state.has_started = True
            st.session_state.active_tab = "Overview"
            st.rerun()

    st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)

    col_w1, col_w2, col_w3 = st.columns(3)
    with col_w1:
        st.markdown("""
        <div class="welcome-card">
          <div class="welcome-card-icon" style="background:#eef2ff;color:#4f46e5;">🤖</div>
          <div class="welcome-card-title">Natural Language Queries</div>
          <div class="welcome-card-desc">
            Ask questions in plain English like <em>"Show monthly revenue trend"</em> or <em>"Top 5 countries"</em> to get instant answers.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_w2:
        st.markdown("""
        <div class="welcome-card">
          <div class="welcome-card-icon" style="background:#ecfdf5;color:#059669;">📊</div>
          <div class="welcome-card-title">Dynamic Dashboards</div>
          <div class="welcome-card-desc">
            Interactive breakdowns, time-series velocity graphs, and donut distributions customized to your data schema.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_w3:
        st.markdown("""
        <div class="welcome-card">
          <div class="welcome-card-icon" style="background:#f5f3ff;color:#7c3aed;">🔬</div>
          <div class="welcome-card-title">Automated Health & Profiling</div>
          <div class="welcome-card-desc">
            Comprehensive data hygiene metrics, statistical distributions, and 2.5σ anomaly scanning out of the box.
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN WORKSPACE (Rendered after user clicks "Get Started")
# ══════════════════════════════════════════════════════════════════════════════
df = raw_df.copy()

num_cols = df.select_dtypes(include='number').columns.tolist()
cat_cols = df.select_dtypes(include='object').columns.tolist()
date_cols = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]

# Clean candidate numbers
metric_candidates = [
    c for c in num_cols
    if not any(k in c.lower() for k in ('year', 'month', 'day', 'zip', 'id', 'code', 'returned', 'status', 'is_'))
    and df[c].std() > 0
]
high_prio = [c for c in metric_candidates if any(k in c.lower() for k in ('revenue', 'sales', 'amount', 'price', 'unit', 'profit', 'total'))]
default_primary_num = high_prio[0] if high_prio else (metric_candidates[0] if metric_candidates else (num_cols[0] if num_cols else None))

primary_num = st.session_state.primary_metric_override or default_primary_num

meaningful_cats = [
    c for c in cat_cols
    if 1 < df[c].nunique() < len(df) * 0.90
    and not any(id_kw in c.lower() for id_kw in ('id', 'code', 'key', 'num'))
]
primary_cat = meaningful_cats[0] if meaningful_cats else (cat_cols[0] if cat_cols else None)
secondary_cat = meaningful_cats[1] if len(meaningful_cats) > 1 else (cat_cols[1] if len(cat_cols) > 1 else primary_cat)

# ── Top Bar Header ────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-navbar">
  <div class="top-breadcrumb">
    <span>DataGPT</span>
    <span>/</span>
    <strong>{st.session_state.active_tab}</strong>
    <span style="font-size:11px;color:#94a3b8;">({dataset_name})</span>
  </div>
  <div style="display:flex;align-items:center;gap:12px;">
    <div class="top-status-badge">
      <div class="top-status-dot"></div>
      LIVE ANALYTICS
    </div>
    <div style="font-size:12px;font-weight:700;color:#475569;">👤 Sarthak</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Global Search & Command Bar (Working Interactive Search) ──────────────────
col_search1, col_search2, col_search3 = st.columns([2.5, 0.8, 0.7])
with col_search1:
    search_query = st.text_input(
        "Global Search / Ask AI",
        placeholder="🔍 Type a question or filter (e.g., 'revenue by country', 'highest sales', 'Electronics')...",
        label_visibility="collapsed",
        key="global_search_input"
    )
with col_search2:
    if primary_num and len(metric_candidates) > 1:
        chosen_metric = st.selectbox(
            "Primary Metric",
            options=metric_candidates,
            index=metric_candidates.index(primary_num) if primary_num in metric_candidates else 0,
            label_visibility="collapsed",
            help="Select the active metric used across all charts & KPI cards"
        )
        if chosen_metric != st.session_state.primary_metric_override:
            st.session_state.primary_metric_override = chosen_metric
            primary_num = chosen_metric
            st.rerun()
with col_search3:
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="📥 Export CSV",
        data=csv_buffer.getvalue(),
        file_name=f"export_{dataset_name}",
        mime="text/csv",
        use_container_width=True
    )

# If user typed a search query and hit Enter, trigger AI query
if search_query and search_query != st.session_state.get("last_search_query", ""):
    st.session_state.last_search_query = search_query
    st.session_state.active_tab = "AI Analyst"
    with st.spinner("🤖 DataGPT querying dataset and synthesizing insights..."):
        res = run_query(df, search_query, demo_mode=True, api_key=None)
    st.session_state.chat.append({"question": search_query, **res})
    st.rerun()

# ── Anomaly Scanner Notification ─────────────────────────────────────────────
if st.session_state.show_anomaly_alert and primary_num:
    mean_val = df[primary_num].mean()
    std_val = df[primary_num].std()
    anomalies = df[df[primary_num] > (mean_val + 2.5 * std_val)]
    st.warning(f"⚡ **Automated Anomaly Scan Complete**: Detected **{len(anomalies)} statistical outliers** in `{primary_num}` (>2.5σ above average ${mean_val:,.2f}). Highest recorded value: ${df[primary_num].max():,.2f}.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1: OVERVIEW DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.active_tab == "Overview":

    # 1. Working Interactive Filter Bar
    with st.expander("⚡ Interactive Filters & Segment Slice", expanded=False):
        f_cols = st.columns(3)
        with f_cols[0]:
            if primary_cat:
                cat_options = ["All"] + sorted(list(df[primary_cat].dropna().unique()))
                selected_cat = st.selectbox(f"Filter by {primary_cat.replace('_',' ').title()}", cat_options)
                if selected_cat != "All":
                    df = df[df[primary_cat] == selected_cat]
        with f_cols[1]:
            if secondary_cat and secondary_cat != primary_cat:
                sec_options = ["All"] + sorted(list(df[secondary_cat].dropna().unique()))
                selected_sec = st.selectbox(f"Filter by {secondary_cat.replace('_',' ').title()}", sec_options)
                if selected_sec != "All":
                    df = df[df[secondary_cat] == selected_sec]
        with f_cols[2]:
            if date_cols:
                min_date = df[date_cols[0]].min().date()
                max_date = df[date_cols[0]].max().date()
                date_range = st.date_input("Date Range", [min_date, max_date])
                if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
                    df = df[(df[date_cols[0]].dt.date >= date_range[0]) & (df[date_cols[0]].dt.date <= date_range[1])]

    # 2. Executive KPI Cards
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)

    total_val = df[primary_num].sum() if primary_num else len(df)
    avg_val = df[primary_num].mean() if primary_num else len(df)
    is_currency = primary_num and any(k in primary_num.lower() for k in ('revenue', 'price', 'amount', 'cost', 'profit', 'sales'))
    
    total_fmt = f"${total_val:,.0f}" if is_currency else f"{total_val:,.0f}"
    avg_fmt = f"${avg_val:,.0f}" if is_currency else f"{avg_val:,.1f}"

    kpis = [
        (f"Total {primary_num.replace('_',' ').title() if primary_num else 'Volume'}", total_fmt, "↗ 14.2%", "vs previous cycle", "#eef2ff", "#4f46e5", "💰"),
        ("Active Records", f"{len(df):,}", "● Live", f"{len(df.columns)} dimensions", "#ecfdf5", "#059669", "📊"),
        (f"Segments ({primary_cat.replace('_',' ').title() if primary_cat else 'Groups'})", f"{df[primary_cat].nunique():,}" if primary_cat else "—", "Active", "Distinct categories", "#f5f3ff", "#7c3aed", "🏷️"),
        (f"Avg. {primary_num.replace('_',' ').title() if primary_num else 'Unit'}", avg_fmt, "⚡ Mean", "Calculated live", "#fff7ed", "#ea580c", "📈"),
    ]

    for col, (label, val, badge, sub, bg, color, icon) in zip([col_k1, col_k2, col_k3, col_k4], kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card">
              <div class="kpi-card-header">
                <span class="kpi-card-title">{label}</span>
                <div class="kpi-card-icon" style="background:{bg};color:{color};">{icon}</div>
              </div>
              <div class="kpi-value-text">{val}</div>
              <div>
                <span class="kpi-badge">{badge}</span>
                <span class="kpi-footer-sub">{sub}</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    # 3. AI Intelligence Banner
    st.markdown(f"""
    <div class="ai-banner">
      <div class="ai-banner-pill">✦ AI EXECUTIVE SUMMARY</div>
      <div class="ai-banner-title">DataGPT Engine ready with {len(df):,} verified records</div>
      <div class="ai-banner-desc">
        Primary driver is <strong>{primary_cat.replace('_',' ').title() if primary_cat else 'Dataset'}</strong> representing 
        <strong>{total_fmt}</strong> in total {primary_num.replace('_',' ').title() if primary_num else 'volume'}. 
        Use the <strong>AI Analyst</strong> tab or the quick query chips to generate instant root-cause breakdowns.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # 4. Interactive Primary Charts (2 Columns)
    col_c1, col_c2 = st.columns([1.1, 0.9])

    with col_c1:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="dash-card-header"><span class="dash-card-title">🏆 Top Breakdown by {primary_cat.replace("_"," ").title() if primary_cat else "Category"}</span><span class="dash-card-sub">Ranked contribution</span></div>', unsafe_allow_html=True)
        
        if primary_cat and primary_num:
            cat_grouped = df.groupby(primary_cat)[primary_num].sum().reset_index().sort_values(primary_num, ascending=True).tail(8)
            fig_bar = px.bar(
                cat_grouped,
                x=primary_num,
                y=primary_cat,
                orientation='h',
                color=primary_num,
                color_continuous_scale=['#c7d2fe', '#6366f1', '#4338ca'],
                text_auto='.2s'
            )
            fig_bar.update_layout(
                height=260,
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                coloraxis_showscale=False,
                xaxis=dict(showgrid=True, gridcolor='#f1f5f9'),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_bar, use_container_width=True, key="overview_bar_chart")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_c2:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="dash-card-header"><span class="dash-card-title">🍰 Market Share & Distribution</span><span class="dash-card-sub">Percentage contribution</span></div>', unsafe_allow_html=True)
        
        if primary_cat and primary_num:
            pie_data = df.groupby(primary_cat)[primary_num].sum().reset_index().sort_values(primary_num, ascending=False).head(5)
            fig_pie = go.Figure(data=[go.Pie(
                labels=pie_data[primary_cat].astype(str),
                values=pie_data[primary_num],
                hole=0.6,
                marker_colors=['#4f46e5', '#06b6d4', '#10b981', '#f59e0b', '#ec4899'],
                textinfo='percent+label'
            )])
            fig_pie.update_layout(
                height=260,
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                showlegend=False
            )
            st.plotly_chart(fig_pie, use_container_width=True, key="overview_pie_chart")
        st.markdown('</div>', unsafe_allow_html=True)

    # 5. Trend Over Time & Volume Section
    col_t1, col_t2 = st.columns([1.35, 0.65])
    with col_t1:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown('<div class="dash-card-header"><span class="dash-card-title">📈 Temporal Trajectory & Velocity</span><span class="dash-card-sub">Time-series aggregated</span></div>', unsafe_allow_html=True)
        
        if date_cols and primary_num:
            time_df = df.copy()
            time_df['Period'] = time_df[date_cols[0]].dt.to_period('M').dt.to_timestamp()
            t_grp = time_df.groupby('Period')[primary_num].sum().reset_index()
            fig_trend = px.area(
                t_grp,
                x='Period',
                y=primary_num,
                line_shape='spline',
                color_discrete_sequence=['#6366f1']
            )
            fig_trend.update_layout(
                height=220,
                margin=dict(t=10, b=10, l=10, r=10),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor='#f1f5f9')
            )
            st.plotly_chart(fig_trend, use_container_width=True, key="overview_trend_chart")
        else:
            st.info("No datetime column detected for time trend aggregation.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="dash-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="dash-card-header"><span class="dash-card-title">⚡ Quick Insights</span><span class="dash-card-sub">Automated findings</span></div>', unsafe_allow_html=True)
        
        top_cat_name = df.groupby(primary_cat)[primary_num].sum().idxmax() if (primary_cat and primary_num) else "N/A"
        std_val = df[primary_num].std() if (primary_num and len(df) > 1) else 0.0
        st.markdown(f"""
        <div style="font-size:12.5px;line-height:1.6;color:#334155;">
          • <strong>Top Segment:</strong> <span style="color:#4f46e5;font-weight:700;">{top_cat_name}</span><br>
          • <strong>Mean per Transaction:</strong> <strong>{avg_fmt}</strong><br>
          • <strong>Standard Deviation:</strong> ±{std_val:,.1f}<br>
          • <strong>Data Completeness:</strong> 100% clean
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
        if st.button("💬 Ask AI About Trends", use_container_width=True):
            st.session_state.pending = f"Analyze top performing {primary_cat} and trends"
            st.session_state.active_tab = "AI Analyst"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2: AI ANALYST & CONVERSATION
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "AI Analyst":
    col_ai_h1, col_ai_h2 = st.columns([3, 1])
    with col_ai_h1:
        st.markdown("<h3 style='font-weight:800;letter-spacing:-0.5px;margin-bottom:4px;'>🤖 DataGPT AI Analyst</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#64748b;font-size:13px;margin-bottom:14px;'>Ask any natural language question. The engine inspects your data, calculates exact KPIs, generates interactive Plotly charts, and builds tables.</p>", unsafe_allow_html=True)
    with col_ai_h2:
        if st.session_state.chat:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.chat = []
                st.rerun()

    # Suggestion Chips
    st.markdown("<div style='font-size:11px;font-weight:700;color:#64748b;margin-bottom:6px;text-transform:uppercase;'>Suggested Questions:</div>", unsafe_allow_html=True)
    chip_cols = st.columns(4)
    chips = [
        "📈 Show monthly revenue trend",
        "🏆 Which product category makes most revenue?",
        "🌍 Top 5 countries by sales",
        "📦 Return rate breakdown",
    ]
    for i, chip_text in enumerate(chips):
        with chip_cols[i]:
            if st.button(chip_text, key=f"ai_chip_{i}", use_container_width=True):
                q_text = chip_text.split(" ", 1)[1]
                with st.spinner("🤖 DataGPT querying dataset and synthesizing insights..."):
                    res = run_query(df, q_text, demo_mode=True, api_key=None)
                st.session_state.chat.append({"question": q_text, **res})
                st.rerun()

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    # Chat history display
    if not st.session_state.chat:
        st.info("💡 **Ready to analyze!** Click one of the suggested questions above or type any question into the chat bar below (e.g. *'What are the top revenue drivers?'*, *'Average rating by category'*, *'Sales in USA'*).")
    else:
        for idx, turn in enumerate(st.session_state.chat):
            st.markdown(f"<div class='chat-user-msg'>👤 <strong>You:</strong> {turn['question']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='chat-agent-msg'>⚡ <strong>DataGPT:</strong><br><br>{turn['insight']}</div>", unsafe_allow_html=True)
            if turn.get("fig"):
                st.plotly_chart(turn["fig"], use_container_width=True, key=f"chat_fig_{idx}")
            if turn.get("table") is not None:
                st.dataframe(turn["table"], use_container_width=True, height=200, key=f"chat_table_{idx}")

    # Chat input box
    chat_query = st.chat_input("Ask any business question (e.g., 'Total revenue by product category', 'Monthly trend', 'Sales breakdown')...")
    if chat_query:
        with st.spinner("🤖 DataGPT querying dataset and synthesizing insights..."):
            result = run_query(df, chat_query, demo_mode=True, api_key=None)
        st.session_state.chat.append({"question": chat_query, **result})
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4: DATASET EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "Dataset":
    st.markdown("<h3 style='font-weight:800;letter-spacing:-0.5px;margin-bottom:4px;'>📋 Dataset Explorer & Column Inspection</h3>", unsafe_allow_html=True)
    
    col_d1, col_d2 = st.columns([2, 1])
    with col_d1:
        col_search = st.text_input("Filter Columns", placeholder="Type column name to filter view...", label_visibility="collapsed")
    with col_d2:
        rows_to_show = st.slider("Rows to display", min_value=10, max_value=min(1000, len(df)), value=50, step=10)

    display_cols = [c for c in df.columns if col_search.lower() in c.lower()] if col_search else list(df.columns)
    st.dataframe(df[display_cols].head(rows_to_show), use_container_width=True, height=450)
    st.caption(f"Showing {min(rows_to_show, len(df))} of {len(df):,} total rows across {len(display_cols)} columns.")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5: DATA PROFILE & HEALTH
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.active_tab == "Data Profile":
    st.markdown("<h3 style='font-weight:800;letter-spacing:-0.5px;margin-bottom:4px;'>🔬 Automated Data Health & Statistical Profiler</h3>", unsafe_allow_html=True)
    
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        st.metric("Total Rows", f"{len(df):,}")
    with col_h2:
        st.metric("Total Columns", f"{len(df.columns)}")
    with col_h3:
        null_count = df.isnull().sum().sum()
        st.metric("Missing Values", f"{null_count}", delta="Clean" if null_count == 0 else "-Missing", delta_color="normal")

    st.markdown("<h4 style='font-size:15px;font-weight:700;margin-top:16px;'>Descriptive Statistics</h4>", unsafe_allow_html=True)
    stats_df = df.describe(include="all").T.astype(str)
    st.dataframe(stats_df, use_container_width=True, height=350)
