import json
import numpy as np
import sys
import os
from pathlib import Path
from dotenv import load_dotenv  


load_dotenv()


if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env! Add it and retry.")


sys.path.append(str(Path(__file__).parent.parent))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup() 

from rag_engine.generator import client, generate_answer
from rag_engine.retriever import retrieve
from django.contrib.auth import get_user_model

User = get_user_model()


with open('evaluation/test_queries.json', 'r') as f:
    test_queries = json.load(f)

def evaluate_rag(test_queries, user_role='admin', k=3):
    results = []
    for q in test_queries:
        dummy_user = User.objects.first()
        docs, confidence = retrieve(q['query'], q['department'], user_role, top_k=k)
   
     
        answer = ""
        if not docs:
            precision = 0
            recall = 0
            faithfulness = 0
        else:
            relevant_retrieved = sum(1 for d in docs if d['doc_name'] in q['expected_relevant_docs'])
            precision = relevant_retrieved / k
            total_expected = len(q['expected_relevant_docs'])
            recall = min(1.0, relevant_retrieved / total_expected) if total_expected > 0 else 0

            context = "\n".join([d['content'] for d in docs])
            answer = generate_answer(q['query'], context, docs, confidence)

            faithfulness_prompt = f"""
            Rate how faithful this answer is to the context (0-1, where 1=fully grounded, no hallucinations).
            Answer: {answer}
            Context: {context}
            Respond ONLY with a number like "0.85".
            """
            faithfulness_resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": faithfulness_prompt}],
                temperature=0
            )
            faithfulness_str = faithfulness_resp.choices[0].message.content.strip()
            try:
                faithfulness = float(faithfulness_str)
            except ValueError:
                faithfulness = 0.5

        results.append({
            'query': q['query'],
            'precision': precision,
            'recall': recall,
            'faithfulness': faithfulness,
            'confidence': confidence,
            'answer': answer
        })

   
    avg_precision = np.mean([r['precision'] for r in results])
    avg_recall = np.mean([r['recall'] for r in results])
    avg_faithfulness = np.mean([r['faithfulness'] for r in results])

    print(f"Avg Precision@{k}: {avg_precision:.2f}")
    print(f"Avg Recall: {avg_recall:.2f}")
    print(f"Avg Faithfulness: {avg_faithfulness:.2f}")

  
    import matplotlib.pyplot as plt
    confidences = [1 if r['confidence'] == 'high' else 0.5 if r['confidence'] == 'medium' else 0 for r in results]
    faithfulnesses = [r['faithfulness'] for r in results]
    plt.scatter(confidences, faithfulnesses)
    plt.xlabel('Confidence')
    plt.ylabel('Faithfulness')
    plt.title('Confidence vs. Faithfulness')
    plt.savefig('evaluation/confidence_vs_faithfulness.png')
    plt.show()

    return results

if __name__ == "__main__":
    eval_results = evaluate_rag(test_queries)
    with open('evaluation/eval_results.json', 'w') as f:
        json.dump(eval_results, f, indent=2)
    print("Eval complete! Check eval_results.json and plot.")