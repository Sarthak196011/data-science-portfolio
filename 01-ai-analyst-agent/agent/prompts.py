"""Prompt templates for the DataGPT agent."""

SYSTEM_PROMPT = """You are DataGPT, a senior data analyst AI. 
You have access to an e-commerce sales dataset with 1,000 orders from 2023.
When given data summaries, provide sharp, concise business insights in 2-3 sentences.
Always highlight the most important number in bold markdown."""

DEMO_ANSWERS = {
    "default": "I analysed the dataset and found key patterns in your data. The results are visualized above — explore the chart for detailed breakdowns by segment.",
}

def build_prompt(question: str, context: str) -> str:
    return f"""Dataset context:
{context}

User question: {question}

Provide a data-driven insight in 2-3 sentences. Bold the key numbers."""
