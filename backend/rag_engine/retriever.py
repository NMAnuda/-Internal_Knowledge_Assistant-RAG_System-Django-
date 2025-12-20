from .embeddings import embed_text
from .vector_store import store



def add_documents(docs):
    embeddings = embed_text(docs)
    store.add_texts(docs, embeddings)

def retrieve(question, top_k=3):
    query_vec = embed_text(question)
    docs = store.search(query_vec, top_k)
    return "\n".join(docs)