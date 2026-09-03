# DealSense AI — Price Comparison & Deal Intelligence Platform 🏷️

> **Shop Smarter. Spot Fake Sales. Verify Deals.** | Multi-Retailer Price Aggregator with 90-Day Statistical Tracking & 0–100 Deal Score.

---

## 📌 Problem Solved
E-commerce retailers frequently display inflated "Original Prices" / MSRPs to create artificial urgency for fake discounts. DealSense aggregates multi-store pricing across Amazon, Best Buy, Walmart, B&H, Target, and eBay, analyzes 90-day price movements, flags artificial markdowns, and generates a mathematically grounded **Deal Score (0–100)**.

---

## 🚀 Key Features
- 🔍 **Multi-Store Price Aggregation**: Compares total prices (including shipping) across top retailers in real time.
- 📉 **90-Day Historical Price Analysis**: Tracks 90-day medians, all-time lows, and price volatility.
- 🎯 **Authentic Deal Score (0–100)**: Evaluates current discount vs historical median (50%), competitor price spread (30%), and merchant trust (20%).
- ⚠️ **Fake Sale Detector**: Flags inflated list prices that falsely claim large discounts.
- ⭐ **Value vs Trust Matrix**: Plotly scatter chart balancing total price against customer review confidence.
- 📥 **Export Reports**: Instant CSV download of price comparisons.

---

## 🛠️ Architecture & Tech Stack
| Component | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Frontend UI** | Streamlit + Custom Glassmorphism CSS |
| **Data Visualization** | Plotly Express & Plotly Graph Objects |
| **Data Processing** | Pandas, NumPy |
| **APIs Supported** | Google Shopping API (via SerpAPI), OpenAI API |

---

## 💻 Quick Start & Run Locally
```bash
cd 06-price-comparison-shopper
pip install -r requirements.txt
streamlit run app.py
```
App will open automatically at `http://localhost:8501`.

---

## 🌐 Deploy to Streamlit Community Cloud
1. Push this folder to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io).
3. Select repo and set main file path to `06-price-comparison-shopper/app.py`.
4. Click **Deploy**!
