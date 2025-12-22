from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question, context, sources, confidence):
    # Number sources for citations
    numbered_sources = {i+1: src["doc_name"] for i, src in enumerate(sources)}

    prompt = f"""
You are an internal company assistant. Answer ONLY using the context below.
Be concise and accurate. If confidence is low, note it.

Context (with citations):
{context}

Confidence: {confidence}

Question: {question}

Format your answer with inline citations like [1] after relevant sentences.
At the end, list sources: [1] {list(numbered_sources.values())[0]}, etc.
If low confidence, say: "This is based on limited data — verify with original docs."
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
