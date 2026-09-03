"""
DataGPT — Pixel-Perfect Replica of the myflow.com SaaS Dashboard
"""
from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import numpy as np
import os
import json
import plotly

from agent.tools import load_data, run_query, build_dashboard, get_kpi_metrics

app = Flask(__name__)

current_df = load_data()
current_filename = "ecommerce_sales.csv"

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/data', methods=['GET'])
def get_data_info():
    global current_df, current_filename
    preview = current_df.head(20).copy()
    for col in preview.columns:
        if pd.api.types.is_datetime64_any_dtype(preview[col]):
            preview[col] = preview[col].dt.strftime('%Y-%m-%d')
            
    preview_records = preview.to_dict(orient='records')
    kpis = get_kpi_metrics(current_df)
    
    return jsonify({
        "filename": current_filename,
        "total_rows": len(current_df),
        "columns": list(current_df.columns),
        "preview": preview_records,
        "kpis": kpis
    })

@app.route('/api/upload', methods=['POST'])
def upload_csv():
    global current_df, current_filename
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files['file']
    try:
        df = pd.read_csv(file)
        for col in df.columns:
            if any(k in col.lower() for k in ("date", "time", "timestamp", "created")):
                try: df[col] = pd.to_datetime(df[col])
                except Exception: pass
        current_df = df
        current_filename = file.filename
        return jsonify({"message": "Success", "rows": len(df), "filename": file.filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/query', methods=['POST'])
def handle_query():
    global current_df
    data = request.json or {}
    question = data.get("question", "")
    openai_key = data.get("api_key", None)
    demo_mode = not bool(openai_key)
    
    if not question:
        return jsonify({"error": "Question is required"}), 400
        
    res = run_query(current_df, question, demo_mode=demo_mode, api_key=openai_key)
    fig_json = None
    if res.get("fig") is not None:
        fig_json = json.loads(plotly.io.to_json(res["fig"]))
        
    table_records = None
    if res.get("table") is not None:
        table_df = res["table"].copy()
        for col in table_df.columns:
            if pd.api.types.is_datetime64_any_dtype(table_df[col]):
                table_df[col] = table_df[col].dt.strftime('%Y-%m-%d')
        table_records = table_df.to_dict(orient='records')
        
    return jsonify({
        "question": question,
        "insight": res.get("insight", ""),
        "fig": fig_json,
        "table": table_records
    })

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    global current_df
    raw_figs = build_dashboard(current_df)
    serialized = []
    for name, fig in raw_figs:
        fig_json = json.loads(plotly.io.to_json(fig))
        serialized.append({"name": name, "fig": fig_json})
    return jsonify({"charts": serialized})


# ── HTML5/CSS3 Pixel-Perfect Replica Template ─────────────────────────────────
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>myflow.com — Analytics Dashboard</title>
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Plotly.js -->
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            background: linear-gradient(135deg, #60a5fa 0%, #3b82f6 50%, #2563eb 100%);
            min-h-screen;
            display: flex; align-items: center; justify-content: center;
            padding: 30px 20px; color: #1e293b;
        }

        /* Safari Browser Window Frame */
        .window-frame {
            width: 100%; max-width: 1380px; background: #ffffff;
            border-radius: 28px; box-shadow: 0 30px 100px rgba(15, 23, 42, 0.3);
            overflow: hidden; display: flex; flex-direction: column;
            border: 1px solid rgba(255, 255, 255, 0.4);
        }

        /* Browser Header Bar */
        .browser-bar {
            background: #f1f5f9; padding: 12px 20px; border-bottom: 1px solid #e2e8f0;
            display: flex; align-items: center; justify-content: space-between;
        }
        .browser-dots { display: flex; gap: 7px; }
        .dot { width: 11px; height: 11px; border-radius: 50%; }
        .dot-red { background: #ff5f56; }
        .dot-yellow { background: #ffbd2e; }
        .dot-green { background: #27c93f; }
        .address-bar {
            background: #ffffff; border: 1px solid #cbd5e1; border-radius: 8px;
            padding: 4px 16px; font-size: 11px; color: #64748b; font-weight: 500;
            display: flex; align-items: center; gap: 6px; width: 320px; justify-content: center;
        }

        /* Dashboard Container */
        .app-container {
            display: flex; min-height: 820px; background: #f8fafc;
        }

        /* Left Icon Rail (#1e1e24) */
        .icon-rail {
            width: 76px; background: #1c1c21; padding: 24px 0;
            display: flex; flex-direction: column; align-items: center; justify-content: space-between;
            flex-shrink: 0;
        }
        .rail-top, .rail-bottom { display: flex; flex-direction: column; align-items: center; gap: 20px; width: 100%; }
        .brand-logo-icon {
            width: 38px; height: 38px; border-radius: 12px; background: #ffffff;
            display: flex; align-items: center; justify-content: center; margin-bottom: 12px;
            color: #1c1c21; font-weight: 900; font-size: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        .nav-icon-btn {
            width: 44px; height: 44px; border-radius: 14px; display: flex; align-items: center; justify-content: center;
            color: #71717a; cursor: pointer; transition: all 0.2s; position: relative;
        }
        .nav-icon-btn:hover, .nav-icon-btn.active {
            background: #27272a; color: #ffffff;
        }
        .nav-icon-btn.active {
            background: #ffffff; color: #1c1c21; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .icon-badge {
            position: absolute; top: 4px; right: 4px; background: #2563eb; color: #fff;
            font-size: 9px; font-weight: 800; width: 16px; height: 16px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center; border: 2px solid #1c1c21;
        }

        /* Main Workspace Area */
        .main-content {
            flex: 1; padding: 28px 36px; overflow-y: auto; background: #f8fafc;
        }

        /* Header Greeting */
        .header-row {
            display: flex; justify-content: space-between; align-items: center; margin-bottom: 26px;
        }
        .greeting-title {
            font-family: 'Playfair Display', Georgia, serif; font-size: 32px; font-weight: 700;
            color: #0f172a; letter-spacing: -0.5px;
        }
        .greeting-sub { font-size: 13px; color: #64748b; margin-top: 2px; font-weight: 500; }
        .header-right { display: flex; align-items: center; gap: 12px; }
        .hdr-btn {
            background: #ffffff; border: 1px solid #e2e8f0; border-radius: 14px;
            padding: 8px 14px; font-size: 12px; font-weight: 600; color: #475569;
            display: flex; align-items: center; gap: 6px; cursor: pointer;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03); transition: all 0.2s;
        }
        .hdr-btn:hover { border-color: #cbd5e1; background: #f8fafc; }
        .user-avatar {
            width: 40px; height: 40px; border-radius: 50%; object-fit: cover;
            border: 2px solid #ffffff; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        /* Grid Layout */
        .dashboard-grid {
            display: grid; grid-template-columns: 1fr 1fr 340px; gap: 20px; margin-bottom: 20px;
        }

        /* White Cards */
        .card-box {
            background: #ffffff; border-radius: 24px; padding: 22px 24px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02); border: 1px solid #f1f5f9;
            position: relative;
        }
        .card-header {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 12px; color: #475569; font-size: 14px; font-weight: 600;
        }
        .card-dots { color: #cbd5e1; font-weight: 800; cursor: pointer; }
        .big-metric {
            font-size: 34px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px;
            display: flex; align-items: center; gap: 8px; margin-bottom: 6px;
        }
        .tag-pill {
            font-size: 11px; font-weight: 700; padding: 3px 9px; border-radius: 12px;
            display: inline-flex; align-items: center; gap: 3px;
        }
        .tag-green { background: #dcfce7; color: #16a34a; }
        .tag-blue { background: #e0f2fe; color: #0284c7; }

        /* Segmented Progress Bars */
        .segmented-bar {
            display: flex; gap: 4px; height: 26px; align-items: flex-end; margin-top: 14px;
        }
        .seg-block { flex: 1; height: 22px; border-radius: 4px; }
        .seg-cyan { background: #00c8b3; }
        .seg-blue { background: #2563eb; }
        .seg-gray { background: #e2e8f0; }

        /* Top Right Contacts Card (Blue Textured) */
        .contacts-card-blue {
            background: linear-gradient(160deg, #1e40af 0%, #2563eb 100%);
            border-radius: 24px; padding: 24px; color: #ffffff;
            box-shadow: 0 8px 30px rgba(37, 99, 235, 0.3); display: flex; flex-direction: column; justify-content: space-between;
        }
        .contacts-card-blue * { color: #ffffff !important; }
        .chart-bars-white {
            display: flex; gap: 8px; height: 95px; align-items: flex-end; margin-top: 16px;
        }
        .bar-w {
            flex: 1; background: rgba(255,255,255,0.85); border-radius: 6px 6px 0 0;
            display: flex; justify-content: center; align-items: flex-end; padding-bottom: 4px;
            font-size: 9px; font-weight: 700; color: #2563eb !important;
        }

        /* Top Contacts List */
        .contact-row {
            display: flex; align-items: center; justify-content: space-between;
            padding: 10px 0; border-bottom: 1px solid #f1f5f9; font-size: 13px;
        }
        .contact-row:last-child { border-bottom: none; }
        .c-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; margin-right: 8px; }

        /* Bottom Row Grid */
        .bottom-grid {
            display: grid; grid-template-columns: 1fr 340px; gap: 20px;
        }

        /* Dark Card (Texts Sent) */
        .dark-widget {
            background: #18181b; border-radius: 24px; padding: 22px 24px; color: #ffffff;
            box-shadow: 0 8px 30px rgba(0,0,0,0.25);
        }
        .dark-widget * { color: #ffffff !important; }

        /* Floating Tooltip Mockup */
        .mock-tooltip {
            position: absolute; top: 25px; left: 52%; transform: translateX(-50%);
            background: #18181b; color: #fff; padding: 8px 14px; border-radius: 12px;
            font-size: 11px; font-weight: 600; box-shadow: 0 4px 16px rgba(0,0,0,0.3);
            z-index: 10;
        }

        /* File Upload Drop Area */
        .upload-area {
            border: 2px dashed #cbd5e1; border-radius: 16px; padding: 14px; text-align: center;
            background: #f8fafc; cursor: pointer; transition: all 0.2s; margin-top: 14px;
        }
        .upload-area:hover { border-color: #2563eb; background: #eff6ff; }
    </style>
</head>
<body>

    <div class="window-frame">
        
        <!-- Top Safari Browser Bar -->
        <div class="browser-bar">
            <div class="browser-dots">
                <div class="dot dot-red"></div>
                <div class="dot dot-yellow"></div>
                <div class="dot dot-green"></div>
            </div>
            <div class="address-bar">
                <i data-lucide="lock" class="w-3 h-3 text-slate-400"></i>
                <span>myflow.com</span>
            </div>
            <div style="width: 50px;"></div>
        </div>

        <!-- App Container -->
        <div class="app-container">
            
            <!-- Left Dark Icon Rail (#1c1c21) -->
            <div class="icon-rail">
                <div class="rail-top">
                    <!-- Brand Cloud Logo -->
                    <div class="brand-logo-icon">☁️</div>
                    
                    <div class="nav-icon-btn active" title="Dashboard">
                        <i data-lucide="layout-grid" class="w-5 h-5"></i>
                        <span class="icon-badge">3</span>
                    </div>
                    <div class="nav-icon-btn" title="Messages" onclick="showAiModal()">
                        <i data-lucide="message-square" class="w-5 h-5"></i>
                    </div>
                    <div class="nav-icon-btn" title="Campaigns">
                        <i data-lucide="send" class="w-5 h-5"></i>
                    </div>
                    <div class="nav-icon-btn" title="Schedule">
                        <i data-lucide="clock" class="w-5 h-5"></i>
                    </div>
                    <div class="nav-icon-btn" title="Contacts">
                        <i data-lucide="users" class="w-5 h-5"></i>
                    </div>
                    <div class="nav-icon-btn" title="Reports">
                        <i data-lucide="bar-chart-2" class="w-5 h-5"></i>
                    </div>
                    <div class="nav-icon-btn" title="Automation">
                        <i data-lucide="zap" class="w-5 h-5"></i>
                    </div>
                    <div class="nav-icon-btn" title="Analytics">
                        <i data-lucide="line-chart" class="w-5 h-5"></i>
                    </div>
                </div>

                <div class="rail-bottom">
                    <div class="nav-icon-btn" title="Settings">
                        <i data-lucide="sliders" class="w-5 h-5"></i>
                    </div>
                </div>
            </div>

            <!-- Main Dashboard View -->
            <div class="main-content">
                
                <!-- Greeting Header -->
                <div class="header-row">
                    <div>
                        <h1 class="greeting-title">Good Afternoon, Sarah</h1>
                        <div class="greeting-sub">Your latest texting updates here</div>
                    </div>
                    <div class="header-right">
                        <div class="hdr-btn">
                            <i data-lucide="search" class="w-4 h-4 text-slate-400"></i>
                        </div>
                        <div class="hdr-btn">
                            <i data-lucide="refresh-cw" class="w-3.5 h-3.5 text-slate-400"></i>
                            <span>Last sync <b class="text-blue-600">Just now</b></span>
                        </div>
                        <img src="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80" class="user-avatar" alt="Sarah">
                    </div>
                </div>

                <!-- TOP ROW CARDS -->
                <div class="dashboard-grid">
                    
                    <!-- Card 1: Delivery Rate -->
                    <div class="card-box">
                        <div class="card-header">
                            <span>Delivery Rate</span>
                            <span class="card-dots">:::</span>
                        </div>
                        <div class="big-metric">
                            91.7%
                            <span class="tag-pill tag-green">↗ 0.3%</span>
                            <span style="font-size:12px;color:#94a3b8;font-weight:500;margin-left:auto;">8.3% pending</span>
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

                    <!-- Card 2: Campaigns -->
                    <div class="card-box">
                        <div class="card-header">
                            <span>Campaigns</span>
                            <span class="card-dots">:::</span>
                        </div>
                        <div class="big-metric">
                            25
                            <span class="tag-pill tag-blue">4 active</span>
                        </div>
                        <div style="display:flex;gap:4px;height:26px;align-items:flex-end;margin-top:14px;">
                            <div style="flex:1;height:18px;background:#3b82f6;border-radius:3px;"></div>
                            <div style="flex:1;height:24px;background:#3b82f6;border-radius:3px;"></div>
                            <div style="flex:1;height:20px;background:#3b82f6;border-radius:3px;"></div>
                            <div style="flex:1;height:26px;background:#3b82f6;border-radius:3px;"></div>
                            <div style="flex:1;height:22px;background:#3b82f6;border-radius:3px;"></div>
                            <div style="flex:1;height:16px;background:#3b82f6;border-radius:3px;"></div>
                            <div style="flex:1;height:24px;background:#3b82f6;border-radius:3px;"></div>
                            <div style="flex:1;height:20px;background:#e2e8f0;border-radius:3px;"></div>
                            <div style="flex:1;height:22px;background:#e2e8f0;border-radius:3px;"></div>
                            <div style="flex:1;height:18px;background:#e2e8f0;border-radius:3px;"></div>
                            <div style="flex:1;height:24px;background:#e2e8f0;border-radius:3px;"></div>
                            <div style="flex:1;height:20px;background:#e2e8f0;border-radius:3px;"></div>
                        </div>
                    </div>

                    <!-- Card 3: Contacts (Top Right Blue Card) -->
                    <div class="contacts-card-blue">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <span style="font-size:14px;font-weight:600;">Contacts</span>
                            <span style="opacity:0.7;cursor:pointer;">:::</span>
                        </div>
                        <div style="margin-top:10px;">
                            <div style="font-size:36px;font-weight:800;line-height:1;">3,241</div>
                            <div style="font-size:12px;opacity:0.85;margin-top:4px;">192 New in July &nbsp;↗ 12%</div>
                        </div>
                        <div class="chart-bars-white">
                            <div class="bar-w" style="height:35px;">J</div>
                            <div class="bar-w" style="height:70px;">F</div>
                            <div class="bar-w" style="height:45px;">M</div>
                            <div class="bar-w" style="height:55px;">A</div>
                            <div class="bar-w" style="height:80px;">M</div>
                            <div class="bar-w" style="height:50px;">J</div>
                            <div class="bar-w" style="height:95px;background:#ffffff;box-shadow:0 0 10px rgba(255,255,255,0.8);">J</div>
                        </div>
                    </div>

                </div>

                <!-- MIDDLE ROW CARDS -->
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:20px;">
                    
                    <!-- Top Contacts -->
                    <div class="card-box" style="height:270px;">
                        <div class="card-header">
                            <span>Top Contacts</span>
                            <select style="border:1px solid #e2e8f0;background:#f8fafc;border-radius:8px;padding:3px 8px;font-size:12px;color:#475569;font-weight:600;"><option>This Week</option></select>
                        </div>
                        <div class="contact-row">
                            <div><span class="c-dot" style="background:#00c8b3;"></span><b>Sarah Mitchell</b> <span style="color:#94a3b8;margin-left:6px;">sarah@brights...</span></div>
                            <div><span style="color:#94a3b8;margin-right:14px;">12%</span><b>1,240</b></div>
                        </div>
                        <div class="contact-row">
                            <div><span class="c-dot" style="background:#2563eb;"></span><b>David Kim</b> <span style="color:#94a3b8;margin-left:6px;">david.kim@email...</span></div>
                            <div><span style="color:#94a3b8;margin-right:14px;">8%</span><b>850</b></div>
                        </div>
                        <div class="contact-row">
                            <div><span class="c-dot" style="background:#93c5fd;"></span><b>Priya Patel</b> <span style="color:#94a3b8;margin-left:6px;">priya@oakrealty.c...</span></div>
                            <div><span style="color:#94a3b8;margin-right:14px;">4%</span><b>425</b></div>
                        </div>
                        <div class="contact-row">
                            <div><span class="c-dot" style="border:1.5px solid #cbd5e1;background:transparent;"></span><span style="color:#64748b;">Others</span></div>
                            <div><span style="color:#94a3b8;margin-right:14px;">76%</span><b>7,011</b></div>
                        </div>
                    </div>

                    <!-- Messages By Type (Donut Chart) -->
                    <div class="card-box" style="height:270px;">
                        <div class="card-header">
                            <span>Messages By Type</span>
                            <select style="border:1px solid #e2e8f0;background:#f8fafc;border-radius:8px;padding:3px 8px;font-size:12px;color:#475569;font-weight:600;"><option>This Month</option></select>
                        </div>
                        <div id="donut-chart-container" style="height:200px;"></div>
                    </div>

                </div>

                <!-- BOTTOM ROW CARDS -->
                <div class="bottom-grid">
                    
                    <!-- Messages By Month Stacked Bar Chart -->
                    <div class="card-box" style="height:270px;position:relative;">
                        <div class="card-header">
                            <span>Messages By Month</span>
                            <select style="border:1px solid #e2e8f0;background:#f8fafc;border-radius:8px;padding:3px 8px;font-size:12px;color:#475569;font-weight:600;"><option>This Year</option></select>
                        </div>
                        <!-- Tooltip Popup -->
                        <div class="mock-tooltip">
                            <div><b>1,234 Total</b></div>
                            <div style="color:#94a3b8;font-size:10px;">○ 38 Open</div>
                            <div style="color:#3b82f6;font-size:10px;">● 1,196 Closed</div>
                        </div>
                        <div id="bar-chart-container" style="height:200px;"></div>
                    </div>

                    <!-- Right Column: Credits & Texts Sent -->
                    <div style="display:flex;flex-direction:column;gap:16px;">
                        
                        <!-- Credits Widget -->
                        <div class="card-box" style="padding:16px 20px;">
                            <div class="card-header" style="margin-bottom:6px;">
                                <span>Credits</span>
                                <span class="card-dots">:::</span>
                            </div>
                            <div style="display:flex;justify-content:space-between;align-items:center;">
                                <div>
                                    <span style="font-size:26px;font-weight:800;color:#0f172a;">$2,450</span>
                                    <span style="font-size:12px;color:#94a3b8;margin-left:6px;">$350 Used</span>
                                </div>
                                <div style="width:32px;height:32px;border-radius:50%;background:#0f172a;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:18px;cursor:pointer;">+</div>
                            </div>
                        </div>

                        <!-- Texts Sent (Dark Widget) -->
                        <div class="dark-widget">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                                <span style="font-size:13px;font-weight:600;color:#cbd5e1;">Texts Sent</span>
                                <span style="font-size:11px;color:#94a3b8;cursor:pointer;">All time ∨</span>
                            </div>
                            <div style="font-size:28px;font-weight:800;line-height:1;">95,215</div>
                            <div style="font-size:11px;color:#94a3b8;margin-top:2px;">1,243 today &nbsp;<span class="tag-pill tag-green" style="background:rgba(34,197,94,0.2);color:#4ade80;">↗ 51%</span></div>
                            <div id="area-chart-container" style="height:70px;margin-top:4px;"></div>
                        </div>

                    </div>

                </div>

                <!-- Interactive Data Upload & AI Query Section -->
                <div class="card-box" style="margin-top:24px;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
                        <h3 style="font-size:16px;font-weight:700;color:#0f172a;display:flex;align-items:center;gap:8px;">
                            <i data-lucide="bot" class="w-5 h-5 text-blue-600"></i>
                            DataGPT AI Assistant & CSV Source
                        </h3>
                        <label class="hdr-btn" for="csv-file-input">
                            <i data-lucide="upload" class="w-4 h-4 text-blue-600"></i>
                            <span>Upload Custom CSV</span>
                        </label>
                        <input type="file" id="csv-file-input" accept=".csv" style="display:none;" onchange="uploadCSV(this)">
                    </div>

                    <!-- AI Query Input Bar -->
                    <div style="display:flex;gap:10px;">
                        <input type="text" id="ai-query-input" placeholder="Ask a business question about your data (e.g. Show monthly revenue trend)..." style="flex:1;padding:12px 18px;border:1.5px solid #cbd5e1;border-radius:14px;font-size:14px;outline:none;" onkeydown="if(event.key==='Enter')askAi()">
                        <button onclick="askAi()" style="background:#2563eb;color:#fff;border:none;border-radius:14px;padding:0 24px;font-weight:700;font-size:14px;cursor:pointer;">Ask AI</button>
                    </div>

                    <!-- AI Response Area -->
                    <div id="ai-response-box" style="display:none;margin-top:16px;padding:16px;background:#f8fafc;border-radius:16px;border:1px solid #e2e8f0;">
                        <div id="ai-insight-text" style="font-size:14px;color:#1e293b;margin-bottom:12px;"></div>
                        <div id="ai-chart-box" style="width:100%;height:260px;"></div>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <script>
        lucide.createIcons();

        // 1. Render Messages By Type Donut Chart
        (function renderDonut() {
            var data = [{
                values: [24, 16, 17],
                labels: ['Direct', 'Campaigns', 'Automations'],
                type: 'pie',
                hole: .7,
                marker: { colors: ['#18181b', '#00c8b3', '#2563eb'] },
                textinfo: 'percent',
                hoverinfo: 'label+value+percent'
            }];
            var layout = {
                height: 190,
                margin: { t: 0, b: 0, l: 0, r: 100 },
                showlegend: true,
                legend: { x: 1, y: 0.5, font: { family: 'Plus Jakarta Sans', size: 11, color: '#475569' } },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)'
            };
            Plotly.newPlot('donut-chart-container', data, layout, { responsive: true, displayModeBar: false });
        })();

        // 2. Render Messages By Month Stacked Bar Chart
        (function renderBar() {
            var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
            var closed = [400, 450, 420, 480, 460, 490, 850, 480, 500, 520, 580, 600];
            var open = [250, 280, 260, 300, 290, 310, 384, 300, 320, 340, 360, 390];

            var trace1 = { x: months, y: closed, name: 'Closed', type: 'bar', marker: { color: '#3b82f6', cornerradius: 4 } };
            var trace2 = { x: months, y: open, name: 'Open conversations', type: 'bar', marker: { color: '#93c5fd', cornerradius: 4 } };

            var layout = {
                barmode: 'stack',
                height: 190,
                margin: { t: 10, b: 30, l: 30, r: 10 },
                showlegend: false,
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                xaxis: { showgrid: false, tickfont: { family: 'Plus Jakarta Sans', size: 10, color: '#94a3b8' } },
                yaxis: { showgrid: true, gridcolor: '#f1f5f9', tickfont: { family: 'Plus Jakarta Sans', size: 10, color: '#94a3b8' } }
            };
            Plotly.newPlot('bar-chart-container', [trace1, trace2], layout, { responsive: true, displayModeBar: false });
        })();

        // 3. Render Texts Sent Dark Area Chart
        (function renderArea() {
            var data = [{
                x: ['1 Jul', '8 Jul', '16 Jul', '25 Jul'],
                y: [1200, 3200, 2100, 4500],
                type: 'scatter',
                mode: 'lines',
                fill: 'tozeroy',
                line: { color: '#ffffff', width: 2 },
                fillcolor: 'rgba(255,255,255,0.08)'
            }];
            var layout = {
                height: 70,
                margin: { t: 5, b: 20, l: 0, r: 0 },
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
                xaxis: { showgrid: false, tickfont: { family: 'Plus Jakarta Sans', size: 9, color: '#94a3b8' } },
                yaxis: { showgrid: false, showticklabels: false }
            };
            Plotly.newPlot('area-chart-container', data, layout, { responsive: true, displayModeBar: false });
        })();

        // Handle AI Query
        async function askAi() {
            var q = document.getElementById('ai-query-input').value.trim();
            if (!q) return;

            var box = document.getElementById('ai-response-box');
            var txt = document.getElementById('ai-insight-text');
            box.style.display = 'block';
            txt.innerHTML = '⚡ <b>Analyzing data with AI Agent...</b>';

            try {
                var res = await fetch('/api/query', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: q })
                });
                var data = await res.json();
                txt.innerHTML = `🤖 <b>DataGPT Insight:</b> ${data.insight}`;
                
                if (data.fig) {
                    Plotly.newPlot('ai-chart-box', data.fig.data, data.fig.layout, { responsive: true });
                }
            } catch(e) {
                txt.innerHTML = 'Error fetching AI response: ' + e;
            }
        }

        // Upload CSV
        async function uploadCSV(input) {
            if (!input.files || input.files.length === 0) return;
            var file = input.files[0];
            var formData = new FormData();
            formData.append('file', file);

            alert('Uploading ' + file.name + '...');
            try {
                var res = await fetch('/api/upload', { method: 'POST', body: formData });
                var data = await res.json();
                alert('Successfully loaded custom dataset: ' + data.filename + ' (' + data.rows + ' rows)');
            } catch(e) {
                alert('Upload error: ' + e);
            }
        }
    </script>
</body>
</html>
"""

if __name__ == '__main__':
    print("Starting DataGPT myflow.com Dashboard on http://localhost:8501 ...")
    app.run(host='0.0.0.0', port=8501, debug=False)
