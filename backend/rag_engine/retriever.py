from .embeddings import embed_text
from .vector_store import store
from .access_control import has_access


def add_documents(docs):
    embeddings = embed_text(docs)
    store.add_texts(docs, embeddings)

def retrieve(question, department, user_role, top_k=3):
    if not has_access(user_role, department):
        return None, "Access denied for this department"

    query_vec = embed_text(question)
    results = store.search(query_vec, top_k)
   
    # Department filter
    results = [r for r in results if r["department"].upper() == department.upper()]
    
    
    if not results:
        return [], "No relevant documents found"

    #  CALCULATE CONFIDENCE SCORE (avg similarity; 1 - normalized distance for relevance)
    avg_score = sum(r["score"] for r in results) / len(results)
    confidence = "high" if avg_score > 0.8 else "medium" if avg_score > 0.5 else "low"

    return results, confidence