"""
VoyageAI Planner — Intelligent Itinerary & Travel Budget Platform
Run: streamlit run app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json
import os
import sys
import datetime

# Ensure project modules are importable
sys.path.insert(0, os.path.dirname(__file__))

from planner.flight_hotel_engine import estimate_travel_logistics
from planner.activity_curator import curate_activities, resolve_global_destination
from planner.itinerary_generator import generate_itinerary, regenerate_single_day
from planner.budget_analyzer import analyze_trip_budget

st.set_page_config(
    page_title="VoyageAI — Smart Travel Itinerary & Budget Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM: Dark Luxury Editorial / Travel Magazine
# Inspired by: Aman Resorts, Mr & Mrs Smith, Condé Nast Traveller,
#              Ritz-Carlton digital, premium hotel booking UIs
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Outfit:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', -apple-system, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background: linear-gradient(180deg, #0c1220 0%, #111827 50%, #0f172a 100%) !important;
    color: #e2e8f0 !important;
}

/* Dark luxury sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
    border-right: 1px solid rgba(245, 158, 11, 0.08) !important;
}
[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
}

/* Gold-accented hero */
.hero-banner {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 50%, #1a1a2e 100%);
    border: 1px solid rgba(245, 158, 11, 0.12);
    border-radius: 16px;
    padding: 30px 36px;
    color: #ffffff;
    margin-bottom: 24px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.3);
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0; left: 0;
    background: 
        linear-gradient(135deg, rgba(245, 158, 11, 0.04) 0%, transparent 40%),
        radial-gradient(ellipse at 90% 10%, rgba(245, 158, 11, 0.06) 0%, transparent 50%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.2), transparent);
}

/* Dark metric cards with gold accent */
.metric-card {
    background: linear-gradient(145deg, #1e293b 0%, #1a2236 100%);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 14px;
    padding: 20px 24px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(245, 158, 11, 0.3), transparent);
}
.metric-card:hover {
    border-color: rgba(245, 158, 11, 0.15);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    transform: translateY(-2px);
}

.metric-label {
    font-size: 11px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #64748b;
    margin-bottom: 8px;
    font-family: 'Outfit', sans-serif !important;
}
.metric-val {
    font-size: 28px;
    font-weight: 700;
    color: #f1f5f9;
    font-family: 'Cormorant Garamond', serif !important;
    letter-spacing: -0.02em;
}

/* Day header with gold left border */
.day-header {
    background: linear-gradient(145deg, #1e293b 0%, #1a2236 100%);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-left: 3px solid #f59e0b;
    border-radius: 12px;
    padding: 18px 24px;
    margin-top: 22px;
    margin-bottom: 14px;
}

/* Activity cards */
.activity-slot {
    background: linear-gradient(145deg, rgba(30, 41, 59, 0.9) 0%, rgba(26, 34, 54, 0.9) 100%);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 10px;
    transition: all 0.25s;
}
.activity-slot:hover {
    border-color: rgba(245, 158, 11, 0.12);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

/* Elegant tabs */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(30, 41, 59, 0.6) !important;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.06);
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    color: #64748b !important;
    font-weight: 500;
    font-size: 13px;
    letter-spacing: 0.02em;
}
.stTabs [aria-selected="true"] {
    color: #f59e0b !important;
    border-bottom-color: #f59e0b !important;
}

/* Gold-outlined buttons */
.stButton>button {
    background: transparent !important;
    color: #f59e0b !important;
    border: 1px solid rgba(245, 158, 11, 0.3) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    letter-spacing: 0.04em;
    padding: 8px 20px !important;
    transition: all 0.3s;
}
.stButton>button:hover {
    background: rgba(245, 158, 11, 0.08) !important;
    border-color: rgba(245, 158, 11, 0.5) !important;
    box-shadow: 0 0 20px rgba(245, 158, 11, 0.06);
}

/* Dark inputs */
.stTextInput>div>div>input {
    background: rgba(30, 41, 59, 0.8) !important;
    color: #e2e8f0 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px;
}
.stSelectbox>div>div {
    background: rgba(30, 41, 59, 0.8) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 10px;
}

/* Dark dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
}

/* Alert styling */
.stAlert {
    background: rgba(30, 41, 59, 0.6) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 12px !important;
}

/* Download button */
.stDownloadButton>button {
    background: rgba(245, 158, 11, 0.08) !important;
    color: #f59e0b !important;
    border: 1px solid rgba(245, 158, 11, 0.2) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Load Destination Catalog ──────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'destinations.json')
with open(DATA_PATH, 'r', encoding='utf-8') as f:
    catalog = json.load(f)

dest_dict = {f"{d['city']}, {d['country']}": d for d in catalog["destinations"]}

# ── Command Palette Header (macOS / Raycast Floating Bar Style) ───────────────
st.markdown("""
<div style='background:rgba(30, 41, 59, 0.75);backdrop-filter:blur(20px);border:1px solid rgba(245, 158, 11, 0.2);padding:14px 24px;border-radius:18px;margin-bottom:20px;display:flex;align-items:center;justify-content:space-between;box-shadow:0 8px 32px rgba(0,0,0,0.3);'>
    <div style='display:flex;align-items:center;gap:14px;'>
        <div style='background:linear-gradient(135deg,#f59e0b,#d97706);color:#0f172a;width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:900;'>⌘</div>
        <div>
            <div style='font-size:16px;font-weight:700;color:#f8fafc;font-family:Cormorant Garamond,serif;'>VoyageAI Command Studio — Global Any-Location Planner</div>
            <div style='font-size:10px;color:#94a3b8;letter-spacing:0.08em;text-transform:uppercase;'>Plan routes from ANY start location to ANY destination in the world</div>
        </div>
    </div>
    <div style='display:flex;align-items:center;gap:8px;'>
        <span style='background:rgba(245,158,11,0.15);color:#f59e0b;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;'>🌍 Global Route Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Callback functions for location quick chips ──────────────────────────────
if "origin_val" not in st.session_state:
    st.session_state.origin_val = "New York, USA"
if "dest_val" not in st.session_state:
    st.session_state.dest_val = "Tokyo, Japan"

def set_origin(val):
    st.session_state.origin_val = val

def set_dest(val):
    st.session_state.dest_val = val

# ── Floating Intake Control Palette with Start & End Locations ───────────────
with st.expander("🌍 Route Controls — Choose Start & End Locations Anywhere in the World", expanded=True):
    col_loc1, col_loc2 = st.columns(2)
    
    with col_loc1:
        st.markdown("**🛫 1. Start Location (Origin)**")
        origin_input = st.text_input(
            "Origin City / Country",
            value=st.session_state.origin_val,
            placeholder="Type any city/country (e.g. 'New York, USA', 'London, UK', 'Mumbai, India', 'Sydney')...",
            key="origin_text_input"
        )
        st.session_state.origin_val = origin_input
        st.caption("Quick selection:")
        chip_o1, chip_o2, chip_o3, chip_o4 = st.columns(4)
        chip_o1.button("🗽 New York", key="origin_ny", on_click=set_origin, args=("New York, USA",))
        chip_o2.button("🇬🇧 London", key="origin_lon", on_click=set_origin, args=("London, UK",))
        chip_o3.button("🇮🇳 Mumbai", key="origin_mum", on_click=set_origin, args=("Mumbai, India",))
        chip_o4.button("🇦🇺 Sydney", key="origin_syd", on_click=set_origin, args=("Sydney, Australia",))

    with col_loc2:
        st.markdown("**🛬 2. End Location (Destination)**")
        preset_dest = st.selectbox(
            "Select Catalog or Type Custom Destination",
            options=["-- Type Custom Place Below --"] + list(dest_dict.keys()),
            index=1 if st.session_state.dest_val in dest_dict else 0,
            key="preset_dest_select"
        )
        default_dest = preset_dest if preset_dest != "-- Type Custom Place Below --" else st.session_state.dest_val
        dest_input = st.text_input(
            "Destination City / Country",
            value=default_dest,
            placeholder="Type ANY place in the world (e.g. 'Kyoto, Japan', 'Barcelona, Spain', 'Bali, Indonesia')...",
            key="dest_text_input"
        )
        st.session_state.dest_val = dest_input
        st.caption("Quick selection:")
        chip_d1, chip_d2, chip_d3, chip_d4 = st.columns(4)
        chip_d1.button("🇯🇵 Tokyo", key="dest_tokyo", on_click=set_dest, args=("Tokyo, Japan",))
        chip_d2.button("🇫🇷 Paris", key="dest_paris", on_click=set_dest, args=("Paris, France",))
        chip_d3.button("🇮🇹 Rome", key="dest_rome", on_click=set_dest, args=("Rome, Italy",))
        chip_d4.button("🌴 Bali", key="dest_bali", on_click=set_dest, args=("Bali, Indonesia",))

    st.divider()

    c1, c2, c3, c4 = st.columns([1.5, 1.2, 1.2, 1.4])
    with c1:
        travelers = st.number_input("Travelers", min_value=1, max_value=10, value=2, step=1)
    with c2:
        days = st.number_input("Days", min_value=1, max_value=14, value=4, step=1)
    with c3:
        target_budget = st.number_input("Target Budget ($USD)", min_value=500, max_value=50000, value=3500, step=250)
    with c4:
        hotel_tier = st.selectbox("Lodging Tier", ["Budget (Hostels)", "Boutique (3-4★)", "Luxury (5★)"], index=1)
        clean_tier = "Budget" if "Budget" in hotel_tier else ("Luxury" if "Luxury" in hotel_tier else "Boutique")

    col_p1, col_p2 = st.columns([2, 3])
    with col_p1:
        pace = st.select_slider("Daily Pace", options=["Relaxed", "Balanced", "Action-Packed"], value="Balanced")
    with col_p2:
        interest_options = ["Culture", "Food", "Sightseeing", "Adventure", "Relaxation", "Nightlife"]
        selected_interests = st.multiselect("Primary Interests", interest_options, default=["Food", "Culture", "Sightseeing"])

# ── Global Destination & Route Resolution ──────────────────────────────────────
selected_dest = resolve_global_destination(dest_input, catalog["destinations"])

# ── Session State Management for Itinerary ────────────────────────────────────
session_key = f"itin_{selected_dest['id']}_{origin_input}_{days}_{clean_tier}_{pace}_{'_'.join(sorted(selected_interests))}"
if "active_itinerary" not in st.session_state or st.session_state.get("current_session_key") != session_key:
    candidate_acts = curate_activities(selected_dest, selected_interests, pace)
    fresh_itin = generate_itinerary(selected_dest, candidate_acts, days, travelers, pace)
    st.session_state.active_itinerary = fresh_itin
    st.session_state.current_session_key = session_key

logistics = estimate_travel_logistics(selected_dest, travelers, days - 1, clean_tier, origin=origin_input)
budget_summary = analyze_trip_budget(logistics, st.session_state.active_itinerary, float(target_budget), travelers)

st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)

# ── Floating Dock Navigation Bar (macOS Dock Style) ───────────────────────────
st.markdown("""
<style>
.dock-container {
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 20px;
    padding: 8px 16px;
    margin-bottom: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.4);
}
</style>
""", unsafe_allow_html=True)

dock_col1, dock_col2, dock_col3, dock_col4 = st.columns(4)
with dock_col1:
    btn_itin = st.button("🗺️ Itinerary Timeline", use_container_width=True)
with dock_col2:
    btn_budget = st.button("📊 Budget Analytics", use_container_width=True)
with dock_col3:
    btn_logistics = st.button("✈️ Flights & Lodging", use_container_width=True)
with dock_col4:
    btn_export = st.button("📥 Export Guide", use_container_width=True)

if "active_dock_tab" not in st.session_state:
    st.session_state.active_dock_tab = "Itinerary Timeline"

if btn_itin:
    st.session_state.active_dock_tab = "Itinerary Timeline"
elif btn_budget:
    st.session_state.active_dock_tab = "Budget Analytics"
elif btn_logistics:
    st.session_state.active_dock_tab = "Flights & Lodging"
elif btn_export:
    st.session_state.active_dock_tab = "Export Guide"

# ── Active Hero Banner ────────────────────────────────────────────────────────
st.markdown(f"""
<div class='hero-banner'>
    <div style='display:inline-block;background:rgba(245,158,11,0.12);color:#f59e0b;border:1px solid rgba(245,158,11,0.25);padding:4px 14px;border-radius:24px;font-size:11px;font-weight:600;margin-bottom:10px;letter-spacing:0.08em;text-transform:uppercase;'>
        ✈️ {origin_input} ➔ {selected_dest['city']}, {selected_dest['country']} · {days} Days · {travelers} Traveler(s)
    </div>
    <h1 style='margin:0 0 6px 0;font-size:28px;font-weight:700;font-family:Cormorant Garamond,serif;color:#f8fafc;'>
        {selected_dest['city']} Travel Expedition
    </h1>
    <p style='margin:0;font-size:13px;color:#94a3b8;max-width:750px;'>
        {selected_dest['tagline']}
    </p>
</div>
""", unsafe_allow_html=True)

# ── 4 Top KPI Metric Cards ────────────────────────────────────────────────────
kpi_cols = st.columns(4)

with kpi_cols[0]:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>💰 Total Estimated Cost</div>
        <div class='metric-val' style='color:#f59e0b;'>${budget_summary['grand_total']:,.2f}</div>
        <div style='font-size:11px;color:#64748b;'>${budget_summary['per_person_total']:,.2f} per person</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[1]:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>🎯 Target Budget</div>
        <div class='metric-val' style='color:#f1f5f9;'>${budget_summary['target_budget']:,.2f}</div>
        <div style='font-size:11px;color:#64748b;'>{travelers} travelers · {days} days</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[2]:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>📊 Budget Variance</div>
        <div class='metric-val' style='color:{budget_summary["status_color"]};'>
            {"+" if budget_summary["variance"] >= 0 else "-"}${abs(budget_summary["variance"]):,.0f}
        </div>
        <div style='font-size:11px;color:{budget_summary["status_color"]};font-weight:600;'>{budget_summary['status']}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[3]:
    total_acts = sum(len(d.get("activities", [])) for d in st.session_state.active_itinerary)
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>🎟️ Planned Experiences</div>
        <div class='metric-val' style='color:#fbbf24;'>{total_acts} <span style='font-size:14px;color:#64748b;font-weight:400;'>places</span></div>
        <div style='font-size:11px;color:#64748b;'>Pace: <strong style='color:#cbd5e1;'>{pace}</strong></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

# ── Dynamic Dock View Rendering ───────────────────────────────────────────────
current_tab = st.session_state.active_dock_tab

if current_tab == "Itinerary Timeline":
    st.markdown("<h3 style='font-weight:700;font-size:22px;margin-bottom:8px;font-family:Cormorant Garamond,serif;color:#f8fafc;'>🗺️ Day-by-Day Itinerary Canvas</h3>", unsafe_allow_html=True)
    for day in st.session_state.active_itinerary:
        d_num = day["day_num"]
        col_dh1, col_dh2 = st.columns([4, 1])
        with col_dh1:
            st.markdown(f"""
            <div class='day-header'>
                <div>
                    <strong style='font-size:18px;color:#f8fafc;font-family:Cormorant Garamond,serif;'>Day {d_num}: {day['theme']}</strong>
                    <div style='font-size:12px;color:#94a3b8;'>📍 {day['neighborhood']} · Est: <strong style='color:#f59e0b;'>${day['total_day_cost']:,.2f}</strong></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_dh2:
            st.markdown("<div style='margin-top:18px;'></div>", unsafe_allow_html=True)
            if st.button(f"🔄 Re-roll Day {d_num}", key=f"regen_btn_{d_num}", use_container_width=True):
                st.session_state.active_itinerary = regenerate_single_day(
                    selected_dest,
                    st.session_state.active_itinerary,
                    d_num,
                    travelers,
                    pace
                )
                st.rerun()

        st.markdown(f"<div style='font-size:13px;color:#cbd5e1;background:linear-gradient(145deg,rgba(30,41,59,0.8),rgba(26,34,54,0.8));border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:14px 18px;margin-bottom:12px;line-height:1.6;'>{day['narrative']}</div>", unsafe_allow_html=True)

        slot_cols = st.columns(len(day["activities"]))
        time_labels = ["🌅 Morning", "☀️ Afternoon", "🌙 Evening", "✨ Late Night"]
        for idx, act in enumerate(day["activities"]):
            with slot_cols[idx]:
                cost_val = act.get("cost_usd", 0)
                cost_text = "Free Admission" if cost_val == 0 else f"${cost_val:,.2f} per person"
                cost_color = "#10b981" if cost_val == 0 else "#f59e0b"
                
                st.markdown(f"""
                <div class='activity-slot'>
                    <div style='font-size:10px;font-weight:600;color:#f59e0b;text-transform:uppercase;letter-spacing:0.1em;'>{time_labels[idx]}</div>
                    <div style='font-weight:700;font-size:15px;color:#f8fafc;margin:4px 0;font-family:Cormorant Garamond,serif;'>{act['name']}</div>
                    <div style='font-size:11px;color:#64748b;margin-bottom:6px;'>
                        📍 {act.get('neighborhood','')} · ★ {act.get('rating',4.8)} · ⏱️ {act.get('duration_hours',2)}h
                    </div>
                    <div style='font-size:12px;color:#94a3b8;line-height:1.4;'>{act.get('desc','')}</div>
                    <div style='margin-top:8px;font-size:11px;font-weight:600;color:{cost_color};'>
                        {cost_text}
                    </div>
                </div>
                """, unsafe_allow_html=True)

elif current_tab == "Budget Analytics":
    st.markdown("<h3 style='font-weight:700;font-size:22px;margin-bottom:12px;font-family:Cormorant Garamond,serif;color:#f8fafc;'>📊 Budget Matrix & Money Saving Tips</h3>", unsafe_allow_html=True)
    col_b1, col_b2 = st.columns([1, 1], gap="medium")
    with col_b1:
        st.markdown("<h4 style='font-weight:700;font-size:16px;color:#f1f5f9;'>Cost Allocation Pie</h4>", unsafe_allow_html=True)
        df_b = budget_summary["breakdown_df"]
        fig_donut = px.pie(
            df_b,
            names="Category",
            values="Total ($)",
            hole=0.5,
            color_discrete_sequence=["#f59e0b", "#d97706", "#10b981", "#6366f1", "#64748b"]
        )
        fig_donut.update_traces(textinfo='percent+label')
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family='Outfit', color='#cbd5e1'),
            height=280,
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False
        )
        st.plotly_chart(fig_donut, use_container_width=True)
    with col_b2:
        st.markdown("<h4 style='font-weight:700;font-size:16px;color:#f1f5f9;'>💡 Money-Saving Tips</h4>", unsafe_allow_html=True)
        for tip in budget_summary["tips"]:
            st.markdown(f"<div style='font-size:13px;color:#94a3b8;margin-bottom:8px;'>• {tip}</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:14px;'></div>", unsafe_allow_html=True)
    st.dataframe(budget_summary["breakdown_df"], use_container_width=True, hide_index=True)

elif current_tab == "Flights & Lodging":
    st.markdown("<h3 style='font-weight:700;font-size:22px;margin-bottom:12px;font-family:Cormorant Garamond,serif;color:#f8fafc;'>✈️ Flights & Accommodation Estimator</h3>", unsafe_allow_html=True)
    col_l1, col_l2 = st.columns(2)
    with col_l1:
        st.markdown(f"""
        <div style='background:linear-gradient(145deg,#1e293b,#1a2236);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:22px;box-shadow:0 4px 16px rgba(0,0,0,0.2);'>
            <h5 style='font-weight:700;margin:0 0 10px 0;color:#f8fafc;font-family:Cormorant Garamond,serif;font-size:18px;'>✈️ Estimated Flights</h5>
            <div style='font-size:13px;color:#94a3b8;line-height:1.7;'>
                • Route: Major Hub ⇄ {selected_dest['city']} ({selected_dest['country']})<br>
                • Estimated roundtrip: <strong style='color:#f59e0b;'>${logistics['flight_per_person']:,.2f}</strong> / traveler<br>
                • Total for {travelers} travelers: <strong style='color:#f59e0b;'>${logistics['total_flights']:,.2f}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_l2:
        st.markdown(f"""
        <div style='background:linear-gradient(145deg,#1e293b,#1a2236);border:1px solid rgba(255,255,255,0.06);border-radius:14px;padding:22px;box-shadow:0 4px 16px rgba(0,0,0,0.2);'>
            <h5 style='font-weight:700;margin:0 0 10px 0;color:#f8fafc;font-family:Cormorant Garamond,serif;font-size:18px;'>🏨 Lodging ({clean_tier})</h5>
            <div style='font-size:13px;color:#94a3b8;line-height:1.7;'>
                • Accommodation Tier: <strong style='color:#cbd5e1;'>{clean_tier}</strong><br>
                • Nightly rate: <strong style='color:#f59e0b;'>${logistics['hotel_per_night']:,.2f}</strong> / room<br>
                • Rooms required: {logistics['rooms_needed']} room(s) for {days - 1} night(s)<br>
                • Total Lodging: <strong style='color:#f59e0b;'>${logistics['total_hotel']:,.2f}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif current_tab == "Export Guide":
    st.markdown("<h3 style='font-weight:700;font-size:22px;margin-bottom:12px;font-family:Cormorant Garamond,serif;color:#f8fafc;'>📥 Export Travel Guide</h3>", unsafe_allow_html=True)
    guide_text = f"# 🌍 VoyageAI Travel Blueprint: {selected_dest['city']}, {selected_dest['country']}\n\n"
    guide_text += f"- **Duration:** {days} Days ({days - 1} Nights)\n"
    guide_text += f"- **Travelers:** {travelers}\n"
    guide_text += f"- **Total Estimated Budget:** ${budget_summary['grand_total']:,.2f} (Target: ${target_budget:,.2f})\n"
    guide_text += f"- **Lodging Tier:** {clean_tier}\n\n"
    guide_text += "## 📅 Day-by-Day Itinerary\n\n"
    for day in st.session_state.active_itinerary:
        guide_text += f"### Day {day['day_num']}: {day['theme']} ({day['neighborhood']})\n"
        guide_text += f"{day['narrative']}\n\n"
        for act in day["activities"]:
            guide_text += f"- **{act['name']}** ({act.get('category','')}): {act.get('desc','')} — ${act.get('cost_usd',0):,.2f}\n"
        guide_text += "\n"
        
    st.text_area("Travel Guide Markdown Preview", guide_text, height=220)
    st.download_button(
        label="📥 Download Markdown Travel Guide",
        data=guide_text,
        file_name=f"voyageai_itinerary_{selected_dest['id']}_{days}days.md",
        mime="text/markdown",
        use_container_width=True
    )
