from .loaders import load_pdf
from .chunker import chunk_text
from .embeddings import embed_text
from .vector_store import store

def ingest_document(file_path, doc_name, department):
    text = load_pdf(file_path)
    chunks = chunk_text(text)

    docs = []
    for chunk in chunks:
        docs.append({
            "content": chunk,
            "doc_name": doc_name,
            "department": department
        })

    embeddings = embed_text([d["content"] for d in docs])
    store.add_docs(docs, embeddings)
