from .loaders import load_pdf
from .chunker import chunk_text
from .embeddings import embed_text
from .vector_store import store

def ingest_document(file_path):
    text = load_pdf(file_path)
    chunks = chunk_text(text)
    embeddings = embed_text(chunks)
    store.add_texts(chunks,embeddings)
