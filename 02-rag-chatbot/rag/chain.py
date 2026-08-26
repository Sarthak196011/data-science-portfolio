"""RAG answer chain — OpenAI or intelligent demo mode."""
from typing import Tuple, List
from rag.embedder import retrieve

DEMO_RESPONSES = [
    "Based on the document, {context_snippet} This indicates that the core focus is on providing structured information about the topic at hand.",
    "According to the retrieved sections, {context_snippet} The document provides detailed guidance on this subject matter.",
    "From the document content: {context_snippet} This passage highlights the key aspects relevant to your question.",
    "The document addresses this by stating: {context_snippet} This suggests a systematic approach to the topic.",
]

def answer_question(
    question: str,
    vectorstore: dict,
    api_key: str = None,
    top_k: int = 4,
    demo_mode: bool = True,
) -> Tuple[str, List[str]]:
    """Answer a question using RAG. Falls back to demo mode if no API key."""

    # ── 1. Retrieve relevant chunks ────────────────────────────────────────────
    chunks  = retrieve(vectorstore, question, top_k=top_k)
    context = "\n\n---\n\n".join(c["text"] for c in chunks)
    sources = list(dict.fromkeys(c["source"] for c in chunks))  # deduplicated

    # ── 2. OpenAI mode ─────────────────────────────────────────────────────────
    if api_key and not demo_mode:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            system = (
                "You are a precise document assistant. Answer ONLY based on the provided context. "
                "If the answer is not in the context, say so honestly. Be concise and cite relevant facts."
            )
            user_msg = f"Context from documents:\n{context}\n\nQuestion: {question}"
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"system","content":system},{"role":"user","content":user_msg}],
                max_tokens=600,
                temperature=0.2,
            )
            return resp.choices[0].message.content.strip(), sources
        except Exception as e:
            pass  # fall through to demo mode

    # ── 3. Demo mode — intelligent context-based response ─────────────────────
    import random, re
    snippet = chunks[0]["text"][:300].strip() if chunks else ""
    snippet = re.sub(r'\s+', ' ', snippet)

    # Build a contextual answer from the retrieved text
    answer_parts = [
        f"📄 **Based on your document**, here's what I found relevant to your question:\n\n",
        f"> {snippet}{'...' if len(chunks[0]['text']) > 300 else ''}\n\n",
    ]

    # Add follow-up sentences from other chunks
    if len(chunks) > 1:
        answer_parts.append("**Additional relevant context:**\n")
        for chunk in chunks[1:3]:
            mini = chunk['text'][:150].strip()
            answer_parts.append(f"- {mini}...\n")

    answer_parts.append(
        f"\n\n---\n*🎭 Demo mode active — add an OpenAI API key in the sidebar for full GPT-4 powered answers with deeper analysis.*"
    )

    return "".join(answer_parts), sources
