import faiss
import numpy as np
import os
import pickle

BASE_DIR = os.path.dirname(__file__)
INDEX_PATH = os.path.join(BASE_DIR, "faiss.index")
TEXTS_PATH = os.path.join(BASE_DIR, "texts.pkl")


class VectorStore:
    def __init__(self, dim=384):
        self.dim = dim
        self.index = None
        self.texts = []

        self.load()

    def load(self):
        if os.path.exists(INDEX_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            with open(TEXTS_PATH, "rb") as f:
                self.texts = pickle.load(f)
            print("FAISS loaded from disk")
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            print("New FAISS index created")

    def save(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(TEXTS_PATH, "wb") as f:
            pickle.dump(self.texts, f)

    def add_texts(self, texts, embeddings):
        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)
        self.texts.extend(texts)
        self.save()

        print("Saved FAISS. Total vectors:", self.index.ntotal)

    def search(self, query_vec, top_k=3):
        if self.index.ntotal == 0:
            print("FAISS index empty")
            return []

        query_vec = np.array(query_vec).astype("float32").reshape(1, -1)
        D, I = self.index.search(query_vec, top_k)

        return [self.texts[i] for i in I[0] if i < len(self.texts)]


store = VectorStore()
