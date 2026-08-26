# DocMind — RAG Chatbot 💬

> **Chat with any document using AI** | Deploy free on Streamlit Cloud

## Overview
Upload PDFs, DOCX, or TXT files and ask questions in natural language. Answers come with source citations. Uses free HuggingFace sentence-transformers for embeddings — no API cost. Optionally plug in an OpenAI key for GPT-4 powered answers.

## Features
- 📂 Upload PDF, TXT, DOCX (multiple files)
- 💬 Natural language Q&A with source citations
- 🆓 Works without API key (free HuggingFace embeddings)
- 🤖 GPT-4 powered answers with OpenAI key
- 📄 Pre-loaded sample annual report for instant demo

## Quick Start
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud
1. Push to GitHub
2. Connect at [share.streamlit.io](https://share.streamlit.io)
3. Main file: `app.py` → Deploy!

## Architecture
```
Upload Document → Text Extraction → Chunking (500 words, 80 overlap)
    → Sentence-Transformer Embeddings → FAISS/Cosine Similarity Search
    → Top-K Chunks Retrieved → GPT-4 or Demo Answer with Citations
```
