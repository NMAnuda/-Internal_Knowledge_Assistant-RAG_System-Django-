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
            print("FAISS + docs loaded from disk")
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.docs = []
            print("New FAISS index created")

    def save(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(DOCS_PATH, "wb") as f:
            pickle.dump(self.docs, f)

    def add_docs(self, docs, embeddings):
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.docs.extend(docs)
        self.save()
        print("Saved FAISS. Total vectors:", self.index.ntotal)

    def search(self, query_vec, top_k=3):
        if self.index.ntotal == 0:
            print("FAISS index empty")
            return []

        query_vec = np.array(query_vec).astype("float32").reshape(1, -1)
        D, I = self.index.search(query_vec, top_k)

        results = []
        for idx, i in enumerate(I[0]):
            if i < len(self.docs):
                results.append({
                    "content": self.docs[i]["content"],
                    "doc_name": self.docs[i]["doc_name"],
                    "department": self.docs[i]["department"],
                    "score": float(D[0][idx])
                })

        return results


store = VectorStore()
