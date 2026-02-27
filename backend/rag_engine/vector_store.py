import faiss
import numpy as np
import os
import pickle

BASE_DIR = os.path.dirname(__file__)
INDEX_PATH = os.path.join(BASE_DIR, "faiss.index")
DOCS_PATH = os.path.join(BASE_DIR, "docs.pkl")


class VectorStore:
    def __init__(self, dim=384):
        self.dim = dim
        self.index = None
        self.docs = []
        self.load()

    def load(self):
        if os.path.exists(INDEX_PATH) and os.path.exists(DOCS_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            with open(DOCS_PATH, "rb") as f:
                self.docs = pickle.load(f)
            # detect whether index uses inner-product (IP) metric or L2
            try:
                self.use_ip = (self.index.metric_type == faiss.METRIC_INNER_PRODUCT)
            except Exception:
                # fallback: inspect class name
                self.use_ip = 'IndexFlatIP' in type(self.index).__name__

            print(f"FAISS + docs loaded from disk (metric={'IP' if self.use_ip else 'L2'})")
        else:
            # Use inner-product index and normalize vectors so inner product == cosine similarity
            self.index = faiss.IndexFlatIP(self.dim)
            self.use_ip = True
            self.docs = []
            print("New FAISS index created (Inner Product - cosine similarity)")

    def save(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(DOCS_PATH, "wb") as f:
            pickle.dump(self.docs, f)

    def add_docs(self, docs, embeddings):
        embeddings = np.array(embeddings).astype("float32")
        # If using inner-product (for cosine), normalize vectors before adding
        if getattr(self, 'use_ip', False):
            faiss.normalize_L2(embeddings)

        self.index.add(embeddings)
        self.docs.extend(docs)
        self.save()
        print("Saved FAISS. Total vectors:", self.index.ntotal)

    def search(self, query_vec, top_k=3):
        if self.index.ntotal == 0:
            print("FAISS index empty")
            return []

        query_vec = np.array(query_vec).astype("float32").reshape(1, -1)
        # Normalize query when using inner-product index so inner product == cosine
        if getattr(self, 'use_ip', False):
            faiss.normalize_L2(query_vec)

        D, I = self.index.search(query_vec, top_k)

        results = []
        for idx, i in enumerate(I[0]):
            if i < len(self.docs):
                # If index is inner-product, D contains similarity (higher better, range approx [-1,1])
                score = float(D[0][idx])
                # If it's an L2 index (older data), convert distance to a similarity-like score in (0,1]
                if not getattr(self, 'use_ip', False):
                    # smaller distance -> higher similarity; use 1/(1+dist) to map to (0,1]
                    score = 1.0 / (1.0 + score)

                results.append({
                    "content": self.docs[i]["content"],
                    "doc_name": self.docs[i]["doc_name"],
                    "department": self.docs[i]["department"],
                    "score": score
                })

        return results


store = VectorStore()
# matching both techniques (L2 and cosine )to maintain backward‑compatibility while moving forward with cosine for better semantic retrieval.