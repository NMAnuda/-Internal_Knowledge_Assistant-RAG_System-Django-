from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_answer(question, context):
    prompt = f"""
You are an internal company assistant.
Answer ONLY using the context below.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    print("genrated one",response)
    return response.choices[0].message.content
