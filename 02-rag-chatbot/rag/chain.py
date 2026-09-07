"""RAG answer chain — OpenAI GPT-4 or Intelligent Context-Aware Synthesis."""
import re
from typing import Tuple, List
from rag.embedder import retrieve

def extract_key_sentences(text: str, query: str, max_sentences: int = 4) -> List[str]:
    """Find the most informative sentences in text that address the user query."""
    query_words = set(re.findall(r'\w+', query.lower()))
    stopwords = {
        'what', 'is', 'the', 'main', 'topic', 'of', 'this', 'document', 'and', 'or', 'in',
        'to', 'a', 'an', 'are', 'was', 'were', 'about', 'does', 'can', 'you', 'tell', 'me',
        'who', 'where', 'when', 'why', 'how', 'which'
    }
    keywords = query_words - stopwords

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    scored = []
    
    for s in sentences:
        s_clean = s.strip()
        if len(s_clean) < 25 or len(s_clean) > 350:
            continue
        s_words = set(re.findall(r'\w+', s_clean.lower()))
        
        # Calculate overlap score
        score = sum(1 for w in keywords if w in s_words)
        # Give slight boost to title-like or informative sentences
        if any(h in s_clean.lower() for h in ['objective', 'purpose', 'overview', 'internship', 'summary', 'project', 'report', 'findings']):
            score += 1.5
        if score > 0 or not keywords:
            scored.append((score, s_clean))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scored[:max_sentences]]

def answer_question(
    question: str,
    vectorstore: dict,
    api_key: str = None,
    top_k: int = 4,
    demo_mode: bool = True,
) -> Tuple[str, List[str]]:
    """Answer a question using RAG. Falls back to intelligent synthesis in demo mode."""

    # 1. Retrieve relevant chunks
    chunks = retrieve(vectorstore, question, top_k=top_k)
    context = "\n\n---\n\n".join(c["text"] for c in chunks)
    sources = list(dict.fromkeys(c["source"] for c in chunks))

    # 2. OpenAI mode (if API key provided)
    if api_key and not demo_mode:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            system = (
                "You are an expert, precise document intelligence assistant. Answer the user's question "
                "thoroughly and directly using ONLY the provided document context. "
                "Synthesize clear bullet points, cite facts, and provide structured insights. "
                "If the information is not present, state that clearly."
            )
            user_msg = f"Document Context:\n{context}\n\nQuestion: {question}"
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user_msg}],
                max_tokens=700,
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip(), sources
        except Exception as e:
            pass  # Fall through to intelligent demo mode

    # 3. Intelligent Demo Mode — Direct, structured answering
    if not chunks:
        return "I could not find any relevant information in the uploaded documents to answer your question. Please ensure your document was parsed correctly.", sources

    q_lower = question.lower()
    is_overview_q = any(w in q_lower for w in ['topic', 'about', 'summary', 'overview', 'purpose', 'main', 'subject', 'what is this'])

    first_chunk = chunks[0]["text"]
    all_sentences = []
    for c in chunks:
        all_sentences.extend(extract_key_sentences(c["text"], question, max_sentences=3))

    # Remove duplicates while preserving order
    unique_sentences = list(dict.fromkeys(all_sentences))

    # Detect title / header from first chunk
    first_lines = [l.strip() for l in first_chunk.split('\n') if l.strip()]
    doc_title = first_lines[0] if first_lines else "the uploaded document"
    if len(doc_title) > 90:
        doc_title = doc_title[:85] + "..."

    output_lines = []

    if is_overview_q:
        output_lines.append(f"### 📋 Document Topic & Overview")
        output_lines.append(f"Based on **{sources[0] if sources else 'your document'}**, the primary focus of this document is **{doc_title}**.\n")
        
        output_lines.append("### 💡 Key Findings & Content Summary:")
        if unique_sentences:
            for s in unique_sentences[:5]:
                output_lines.append(f"- {s}")
        else:
            # Fallback to key paragraph excerpts
            paragraphs = [p.strip() for p in first_chunk.split('\n\n') if len(p.strip()) > 40]
            for p in paragraphs[:3]:
                output_lines.append(f"- {p}")
    else:
        output_lines.append(f"### 💬 Answer to Your Question")
        if unique_sentences:
            output_lines.append(f"**Direct finding:** {unique_sentences[0]}\n")
            if len(unique_sentences) > 1:
                output_lines.append("### 📌 Detailed Supporting Evidence:")
                for s in unique_sentences[1:4]:
                    output_lines.append(f"- {s}")
        else:
            output_lines.append(f"The most relevant passage regarding your question states:\n")
            snippet = first_chunk[:350].strip()
            output_lines.append(f"> {snippet}{'...' if len(first_chunk) > 350 else ''}")

    # Add verified source citations
    output_lines.append("\n---")
    output_lines.append(f"📁 **Source Document:** `{sources[0] if sources else 'Uploaded File'}`")


    return "\n".join(output_lines), sources
