"""
DealSense AI — Price Comparison & Deal Intelligence Platform
Run: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io
import os
import sys

# Ensure project modules are importable
sys.path.insert(0, os.path.dirname(__file__))

from engine.scraper_api import load_catalog, search_products
from engine.deal_analyzer import analyze_deal
from engine.value_ranker import compute_value_scores

st.set_page_config(
    page_title="DealSense AI — Smart Price Comparison & Deal Score",
    page_icon="🏷️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM: Apple "Liquid Glass" / Bento Grid
# Inspired by: Apple WWDC 2025 Liquid Glass, iOS 26 frosted panels, 
#              Vercel dashboard, Linear app, Raycast
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background: linear-gradient(165deg, #f0f0f5 0%, #e8e6f0 30%, #f2eff8 60%, #edf0f7 100%) !important;
    color: #1a1a2e !important;
}

/* Frosted sidebar */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.55) !important;
    backdrop-filter: blur(24px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.5) !important;
}

/* Liquid Glass hero */
.hero-banner {
    background: linear-gradient(135deg, 
        rgba(99, 102, 241, 0.88) 0%, 
        rgba(139, 92, 246, 0.85) 35%, 
        rgba(168, 85, 247, 0.82) 70%, 
        rgba(192, 132, 252, 0.80) 100%);
    backdrop-filter: blur(20px) saturate(150%);
    -webkit-backdrop-filter: blur(20px) saturate(150%);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 20px;
    padding: 28px 34px;
    color: #ffffff;
    margin-bottom: 24px;
    box-shadow: 
        0 8px 32px rgba(99, 102, 241, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.2),
        inset 0 -1px 0 rgba(0, 0, 0, 0.05);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(ellipse at 30% 20%, rgba(255,255,255,0.12) 0%, transparent 50%);
    pointer-events: none;
}

/* Frosted glass metric pills (Bento tiles) */
.metric-pill {
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(16px) saturate(150%);
    -webkit-backdrop-filter: blur(16px) saturate(150%);
    border: 1px solid rgba(255, 255, 255, 0.6);
    border-radius: 16px;
    padding: 18px 22px;
    box-shadow: 
        0 2px 8px rgba(0, 0, 0, 0.03),
        0 8px 24px rgba(0, 0, 0, 0.04),
        inset 0 1px 0 rgba(255, 255, 255, 0.8);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.metric-pill:hover {
    transform: translateY(-2px);
    box-shadow: 
        0 4px 12px rgba(0, 0, 0, 0.06),
        0 12px 32px rgba(99, 102, 241, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.9);
    border-color: rgba(99, 102, 241, 0.2);
}

.metric-label {
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6b7280;
    margin-bottom: 6px;
}
.metric-value {
    font-size: 28px;
    font-weight: 800;
    color: #1a1a2e;
    letter-spacing: -0.02em;
}

.deal-badge-hero {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* Tabs — pill style */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.5) !important;
    backdrop-filter: blur(12px);
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.5);
    padding: 4px;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #6b7280 !important;
    font-weight: 600;
    border-radius: 10px;
    font-size: 13px;
}
.stTabs [aria-selected="true"] {
    color: #4f46e5 !important;
    background: rgba(255, 255, 255, 0.8) !important;
    border-bottom-color: transparent !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}

/* Rounded buttons */
.stButton>button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 20px !important;
    box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}
.stButton>button:hover {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
    transform: translateY(-1px);
}

/* Rounded inputs */
.stTextInput>div>div>input {
    background: rgba(255, 255, 255, 0.7) !important;
    backdrop-filter: blur(8px);
    color: #1a1a2e !important;
    border: 1px solid rgba(0, 0, 0, 0.06) !important;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.stTextInput>div>div>input:focus {
    border-color: rgba(99, 102, 241, 0.4) !important;
    box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.08);
}
.stSelectbox>div>div {
    background: rgba(255, 255, 255, 0.7) !important;
    border: 1px solid rgba(0, 0, 0, 0.06) !important;
    border-radius: 12px;
}

/* Frosted dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0, 0, 0, 0.06);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* Alert boxes */
.stAlert {
    background: rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0, 0, 0, 0.06) !important;
    border-radius: 14px !important;
}

.store-card {
    background: rgba(255, 255, 255, 0.6);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(0, 0, 0, 0.05);
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 8px;
}

/* Download button */
.stDownloadButton>button {
    background: rgba(255, 255, 255, 0.7) !important;
    color: #4f46e5 !important;
    border: 1px solid rgba(99, 102, 241, 0.2) !important;
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ── State Initialization ──────────────────────────────────────────────────────
if "selected_product_id" not in st.session_state:
    st.session_state.selected_product_id = "sony-wh1000xm5"
if "search_input" not in st.session_state:
    st.session_state.search_input = ""

catalog = load_catalog()
all_products = catalog.get("products", [])

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='display:flex;align-items:center;gap:10px;margin-bottom:12px;'>
        <div style='background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white;width:40px;height:40px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 4px 12px rgba(99,102,241,0.25);'>🏷️</div>
        <div>
            <h3 style='margin:0;font-size:18px;font-weight:800;color:#1a1a2e;letter-spacing:-0.3px;'>DealSense AI</h3>
            <p style='margin:0;font-size:11px;color:#9ca3af;font-weight:500;'>Smart Price Intelligence</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    st.markdown("**🔍 Browse Featured Categories**")
    cat_filter = st.selectbox("Category", ["All Categories"] + catalog.get("categories", []), label_visibility="collapsed")
    
    filtered_list = all_products
    if cat_filter != "All Categories":
        filtered_list = [p for p in all_products if p["category"] == cat_filter]

    st.markdown("**📦 Select Catalog Product**")
    product_options = {p["id"]: p["name"] for p in filtered_list}
    if product_options:
        curr_id = st.session_state.selected_product_id if st.session_state.selected_product_id in product_options else list(product_options.keys())[0]
        selected_id = st.selectbox(
            "Product",
            options=list(product_options.keys()),
            format_func=lambda x: product_options[x],
            index=list(product_options.keys()).index(curr_id),
            label_visibility="collapsed"
        )
        if selected_id != st.session_state.selected_product_id:
            st.session_state.selected_product_id = selected_id
            st.rerun()

    st.divider()
    st.markdown("**⚙️ Live API Connection (Optional)**")
    serpapi_key = st.text_input("SerpAPI Key (Google Shopping)", type="password", placeholder="Optional sk-...")
    openai_key = st.text_input("OpenAI Key (Narratives)", type="password", placeholder="Optional sk-...")
    
    st.divider()
    st.markdown("<p style='font-size:11px;color:#9ca3af;'>DealSense uses 90-day price tracking to verify deals and compute Deal Scores (0–100).</p>", unsafe_allow_html=True)

# ── Split-Screen Studio Workspace Layout (3-Pane Studio) ──────────────────────
col_canvas, col_inspector = st.columns([1.7, 1.0], gap="large")

with col_canvas:
    # ── STUDIO CANVAS: Top Search Bar & Chips ────────────────────────────────
    st.markdown("""
    <div style='background:rgba(255,255,255,0.7);backdrop-filter:blur(16px);border:1px solid rgba(0,0,0,0.06);padding:18px 24px;border-radius:18px;margin-bottom:18px;box-shadow:0 2px 8px rgba(0,0,0,0.03);'>
        <div style='font-size:11px;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;'>Studio Workspace // Active Search Canvas</div>
        <h2 style='margin:0 0 10px 0;font-size:24px;font-weight:800;letter-spacing:-0.5px;color:#1a1a2e;'>Price Intelligence Studio</h2>
        <p style='margin:0;font-size:13px;color:#6b7280;'>Search products or select items from the sidebar workspace to initiate deep deal verification.</p>
    </div>
    """, unsafe_allow_html=True)

    col_s1, col_s2 = st.columns([4, 1])
    with col_s1:
        search_query = st.text_input(
            "Search any product...",
            placeholder="Type any product (e.g., 'Sony WH-1000XM5', 'MacBook Pro M3', 'LG OLED TV')...",
            label_visibility="collapsed"
        )
    with col_s2:
        search_btn = st.button("🔍 Search Studio", use_container_width=True)

    # Suggestion Chips
    chip_cols = st.columns(5)
    chips = [
        ("🎧 Sony WH-1000XM5", "sony-wh1000xm5"),
        ("💻 MacBook Air M3", "apple-macbook-air-m3"),
        ("📺 LG 65\" OLED C3", "lg-c3-65-oled-tv"),
        ("📱 Galaxy S24 Ultra", "samsung-galaxy-s24-ultra"),
        ("⌚ Watch Ultra 2", "apple-watch-ultra-2")
    ]
    for i, (label, pid) in enumerate(chips):
        with chip_cols[i]:
            if st.button(label, key=f"chip_{i}", use_container_width=True):
                st.session_state.selected_product_id = pid
                st.session_state.search_input = ""
                st.rerun()

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    # ── Fetch Active Product Data ─────────────────────────────────────────────
    active_product = None
    if search_query and (search_btn or search_query != st.session_state.search_input):
        st.session_state.search_input = search_query
        results = search_products(search_query, serpapi_key=serpapi_key)
        if results:
            active_product = results[0]
    else:
        matched = [p for p in all_products if p["id"] == st.session_state.selected_product_id]
        if matched:
            active_product = matched[0]
        elif all_products:
            active_product = all_products[0]

    if not active_product:
        st.warning("No product selected. Please choose a product or perform a search.")
        st.stop()

    analysis = analyze_deal(active_product)
    scored_stores = compute_value_scores(active_product.get("stores", []))

    # ── CANVAS VISUALIZERS: 90-Day Price Trend & Retailer Bar Chart ───────────
    st.markdown("<h4 style='font-size:16px;font-weight:700;margin-bottom:6px;color:#1a1a2e;'>📈 90-Day Price Movement Canvas</h4>", unsafe_allow_html=True)
    hist_df = analysis["history_df"]
    if not hist_df.empty:
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Scatter(
            x=hist_df["Date"],
            y=hist_df["Price"],
            mode='lines+markers',
            name='Historical Price ($)',
            line=dict(color='#6366f1', width=3),
            marker=dict(size=6, color='#4f46e5')
        ))
        fig_hist.add_hline(
            y=analysis["median_90d"],
            line_dash="dash",
            line_color="#f59e0b",
            annotation_text=f"Median: ${analysis['median_90d']:,.0f}",
            annotation_position="bottom right"
        )
        fig_hist.add_hline(
            y=analysis["lowest_90d"],
            line_dash="dot",
            line_color="#10b981",
            annotation_text=f"90D Low: ${analysis['lowest_90d']:,.0f}",
            annotation_position="top left"
        )
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.4)',
            font=dict(family='Inter', color='#374151'),
            height=310,
            margin=dict(t=25, b=25, l=20, r=20),
            yaxis_title="Price ($USD)",
            xaxis_title="Timeline",
            xaxis=dict(gridcolor='rgba(0,0,0,0.04)'),
            yaxis=dict(gridcolor='rgba(0,0,0,0.04)')
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("<h4 style='font-size:16px;font-weight:700;margin-top:18px;margin-bottom:6px;color:#1a1a2e;'>📊 Cross-Retailer Price Breakdown</h4>", unsafe_allow_html=True)
    comp_data = analysis["comparison_df"].copy()
    fig_bar = px.bar(
        comp_data,
        x="Retailer",
        y="Total ($)",
        text="Total ($)",
        color="Total ($)",
        color_continuous_scale=["#10b981", "#6366f1", "#ef4444"],
    )
    fig_bar.update_traces(texttemplate='$%{text:,.2f}', textposition='outside')
    fig_bar.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.4)',
        font=dict(family='Inter', color='#374151'),
        height=280,
        margin=dict(t=25, b=25, l=20, r=20),
        coloraxis_showscale=False,
        xaxis=dict(gridcolor='rgba(0,0,0,0.04)'),
        yaxis=dict(gridcolor='rgba(0,0,0,0.04)')
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Value Matrix Scatter Plot
    st.markdown("<h4 style='font-size:16px;font-weight:700;margin-top:18px;margin-bottom:6px;color:#1a1a2e;'>⭐ Store Rating vs Total Cost Matrix</h4>", unsafe_allow_html=True)
    val_df = pd.DataFrame(scored_stores)
    if not val_df.empty:
        fig_scatter = px.scatter(
            val_df,
            x="total_cost",
            y="rating",
            size="value_score",
            color="store",
            hover_name="store",
            text="store",
            labels={"total_cost": "Total Cost ($)", "rating": "Store Rating (out of 5)"}
        )
        fig_scatter.update_traces(textposition='top center')
        fig_scatter.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(255,255,255,0.4)',
            font=dict(family='Inter', color='#374151'),
            height=280,
            margin=dict(t=25, b=25, l=20, r=20),
            xaxis=dict(gridcolor='rgba(0,0,0,0.04)'),
            yaxis=dict(gridcolor='rgba(0,0,0,0.04)')
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

with col_inspector:
    # ── STUDIO INSPECTOR PANEL ────────────────────────────────────────────────
    st.markdown("<div style='font-size:11px;font-weight:700;color:#6366f1;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:4px;'>Inspector Panel</div>", unsafe_allow_html=True)
    
    # Active Product Title & Category Badge
    st.markdown(f"<div style='font-size:11px;font-weight:600;color:#6366f1;text-transform:uppercase;letter-spacing:0.06em;'>{active_product.get('category','Product')} · {active_product.get('brand','')}</div>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='font-weight:800;letter-spacing:-0.5px;margin:2px 0 4px 0;color:#1a1a2e;font-size:20px;'>{active_product['name']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color:#6b7280;font-size:12px;margin-bottom:14px;'>{active_product.get('specs','')}</p>", unsafe_allow_html=True)

    # Executive Verdict Badge Card
    st.markdown(f"""
    <div style='background:{analysis["verdict_color"]}12;border:1px solid {analysis["verdict_color"]}30;padding:14px 18px;border-radius:14px;margin-bottom:16px;text-align:center;'>
        <div style='font-size:10px;font-weight:600;color:#6b7280;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:2px;'>Deal Verification</div>
        <div style='font-size:16px;font-weight:800;color:{analysis["verdict_color"]};margin-bottom:2px;'>{analysis["verdict_badge"]}</div>
        <div style='font-size:12px;color:#374151;'>Suggested: <strong style="color:#4f46e5;">{analysis["action"]}</strong></div>
    </div>
    """, unsafe_allow_html=True)

    if analysis["is_fake_deal"]:
        st.error(analysis["explanation"])
    else:
        st.info(f"🤖 {analysis['explanation']}")

    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)

    # Stacked Metric Cards
    st.markdown(f"""
    <div class='metric-pill' style='margin-bottom:8px;'>
        <div class='metric-label'>💰 Best Online Price</div>
        <div class='metric-value' style='color:#059669;'>${analysis['best_price']:,.2f}</div>
        <div style='font-size:11px;color:#6b7280;'>at <strong>{analysis['best_store']}</strong></div>
    </div>
    <div class='metric-pill' style='margin-bottom:8px;'>
        <div class='metric-label'>📉 90-Day Low / Median</div>
        <div class='metric-value'>${analysis['lowest_90d']:,.0f} <span style='font-size:13px;font-weight:500;color:#9ca3af;'>/ ${analysis['median_90d']:,.0f}</span></div>
        <div style='font-size:11px;color:{"#059669" if analysis["discount_vs_median_pct"] > 0 else "#dc2626"};font-weight:600;'>
            {"↓" if analysis["discount_vs_median_pct"] > 0 else "↑"} {abs(analysis['discount_vs_median_pct'])}% vs 90-day avg
        </div>
    </div>
    <div class='metric-pill' style='margin-bottom:8px;'>
        <div class='metric-label'>🎯 Deal Score</div>
        <div class='metric-value' style='color:#6366f1;'>{analysis['deal_score']} <span style='font-size:13px;font-weight:500;color:#9ca3af;'>/ 100</span></div>
        <div style='font-size:11px;color:#6b7280;'>Verified Price Integrity</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

    # Live Purchase Links
    st.markdown("<h4 style='font-size:15px;font-weight:700;margin-bottom:10px;color:#1a1a2e;'>🛒 Store Links</h4>", unsafe_allow_html=True)
    for s in active_product.get("stores", []):
        total_val = s["price"] + s.get("shipping", 0.0)
        is_best = (s["store"] == analysis["best_store"])
        border_c = "#10b981" if is_best else "#e2e8f0"
        bg_c = "rgba(99,102,241,0.04)" if is_best else "rgba(255,255,255,0.6)"
        best_tag = "<span style='background:linear-gradient(135deg,#6366f1,#8b5cf6);color:white;font-size:9px;padding:2px 8px;border-radius:6px;margin-left:4px;font-weight:600;'>BEST</span>" if is_best else ""
        price_color = "#059669" if is_best else "#1a1a2e"
        store_url = s.get("url", "#")
        
        st.markdown(f"""
        <div style='background:{bg_c};backdrop-filter:blur(12px);border:1px solid {border_c};border-radius:12px;padding:12px 14px;margin-bottom:8px;display:flex;justify-content:space-between;align-items:center;'>
            <div>
                <div style='font-weight:700;font-size:13px;color:#1a1a2e;'>{s['store']} {best_tag}</div>
                <div style='font-size:10px;color:#6b7280;'>★ {s.get('rating',4.5)} ({s.get('reviews',100):,} reviews)</div>
            </div>
            <div style='text-align:right;'>
                <div style='font-size:16px;font-weight:800;color:{price_color};'>${total_val:,.2f}</div>
                <a href='{store_url}' target='_blank' style='font-size:10px;color:#6366f1;text-decoration:none;font-weight:600;'>Visit ↗</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Export Drawer
    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    with st.expander("📋 Export & Raw Data"):
        st.dataframe(analysis["comparison_df"], use_container_width=True, hide_index=True)
        csv_buf = io.StringIO()
        analysis["comparison_df"].to_csv(csv_buf, index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_buf.getvalue(),
            file_name=f"price_comparison_{active_product['id']}.csv",
            mime="text/csv",
            use_container_width=True
        )

