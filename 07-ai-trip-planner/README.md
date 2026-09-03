# VoyageAI Planner — Intelligent Itinerary & Travel Budget Platform ✈️

> **Personalized Day-by-Day Travel Plans with Flight/Hotel Estimation & Budget Variance Analytics.**

---

## 📌 Problem Solved
Planning a multi-day trip is tedious: travelers struggle to balance flight prices, accommodation tiers, daily activity sequencing, neighborhood logistics, and target budgets. VoyageAI solves this by automating the entire planning workflow: estimating logistics, curating neighborhood-optimized daily plans, comparing costs against a budget target, and allowing instant **single-day regenerations** without resetting the rest of the trip.

---

## 🚀 Key Features
- 📍 **Multi-Destination Intelligence**: Rich pre-loaded destination guides (Tokyo, Paris, Rome, New York, Bali) with categorized attractions.
- ✈️ **Flight & Hotel Cost Estimator**: Estimates lodging tiers (Budget, Boutique, Luxury) and airfare based on traveler count and duration.
- 📅 **Day-by-Day Clustered Itinerary**: Sequenced into Morning, Afternoon, and Evening activities with timing, ratings, and costs.
- 🔄 **Single-Day Regeneration**: Re-roll any single day's plan without modifying the other days.
- 💰 **Budget & Variance Breakdown**: Interactive Plotly Donut Chart comparing flights, lodging, dining, activities, and contingency buffers with over/under budget alerts.
- 📥 **Export Travel Guide**: Instant markdown download of the generated itinerary.

---

## 🛠️ Tech Stack
| Component | Technology |
|---|---|
| **Language** | Python 3.10+ |
| **Frontend UI** | Streamlit + Custom Travel Theme CSS |
| **Data Visualization** | Plotly Express & Plotly Graph Objects |
| **Data Structures** | Pandas, JSON |
| **APIs Supported** | Amadeus API (Flights/Hotels), Google Places API, OpenAI API |

---

## 💻 Quick Start & Run Locally
```bash
cd 07-ai-trip-planner
pip install -r requirements.txt
streamlit run app.py
```
App will open automatically at `http://localhost:8501`.

---

## 🌐 Deploy to Streamlit Community Cloud
1. Push this folder to GitHub.
2. Visit [share.streamlit.io](https://share.streamlit.io).
3. Set main file path to `07-ai-trip-planner/app.py`.
4. Click **Deploy**!
