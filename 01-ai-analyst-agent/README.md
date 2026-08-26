# DataGPT — AI Data Analyst Agent 🤖

> **Ask business questions, get instant charts + insights** | No SQL required

## Overview
Type any business question → the AI agent queries the e-commerce dataset, builds a Plotly chart, and writes a 3-sentence data-driven insight. Works in demo mode (no API key) or with OpenAI for richer analysis.

## Quick Start
```bash
pip install -r requirements.txt
streamlit run app.py
# Dataset auto-generated on first run
```

## Example Questions
- "Show monthly revenue trend"
- "Which product category makes the most revenue?"
- "Top 5 countries by sales"
- "What's the return rate by category?"

## Deploy to Streamlit Cloud
Push to GitHub → [share.streamlit.io](https://share.streamlit.io) → Connect → Deploy!

## Architecture
```
User Question → Intent Classification → Tool Selection
    → Pandas Query on E-Commerce Dataset (1,000 orders)
    → Plotly Chart Generation
    → GPT-4 / Demo Insight Narrative
    → Streamlit Chat UI
```
