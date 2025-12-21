from .embeddings import embed_text
from .vector_store import store
from .access_control import has_access


def add_documents(docs):
    embeddings = embed_text(docs)
    store.add_texts(docs, embeddings)

def retrieve(question, department, user_role, top_k=3):
    if not has_access(user_role, department):
        print("has_acess",user_role,department)
        return None, "Access denied for this department"

    query_vec = embed_text(question)
    results = store.search(query_vec, top_k)

    # department filter
    results = [
        r for r in results
        if r["department"].upper() == department.upper()
    ]

    return results, None