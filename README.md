# Internal Knowledge Assistant – RAG System (Django)

An AI-powered internal knowledge assistant built using Django REST Framework and Retrieval-Augmented Generation (RAG).
The system allows organizations to upload internal documents and enables employees to query company-specific knowledge securely and accurately using a self-hosted or external LLM.

## Core Features

* Upload internal documents (PDF / text-based)
* Intelligent document chunking
* Semantic search using FAISS vector database
* LLM-powered answer generation (self-hosted)
* Answers strictly grounded on internal documents (RAG)
* Department-based document filtering
* Context-aware responses

## Security & Reliability

* JWT Authentication
* Role-based access control
* Chat history & audit logging
* RAG failure handling (no hallucinations)
* Explainable responses with citations
* RAG evaluation metrics (backend)

## Tech Stack

### Backend

Python | Django | Django REST Framework | FAISS (Vector Search) | Self-Hosted LLM(qwen2) | JWT Authentication

### AI / NLP

Sentence Embeddings | Semantic Similarity Search | Retrieval-Augmented Generation (RAG)

### Frontend

Company Internal Knowledge Chatbot (Django + RAG)

### Tools & Libraries
* Document Processing: PyPDF2 (PDF extraction), Sentence Transformers (embeddings)
* Vector Store: FAISS (persistent indexing)
* Evaluation: NumPy, Matplotlib (metrics/plots)
* Deployment: Vercel (frontend), Heroku/Railway (backend)


## System Workflow

* Admin uploads document
* Document is chunked into smaller passages
* Embeddings are generated
* Stored in FAISS vector store
* User asks a question
* Relevant chunks are retrieved
* LLM generates answer only using retrieved context
* Response returned with confidence & citations

## Project Structure

  
    Company_Internal_Knowledge_Chatbot_-Django-RAG-/
    ├── backend/                          # Django backend (Python)
    │   ├── config/                       # Django settings & config
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   ├── accounts/                     # User auth & roles
    │   │   ├── urls.py     
    │   │   ├── models.py                 # Custom User, Role
    │   │   ├── serializers.py
    │   │   └── views.py                  # Register / Login
    │   ├── chat/                         # Chat & history APIs
    │   │   ├── models.py                 # ChatMessage
    │   │   ├── urls.py    
    │   │   ├── serializers.py
    │   │   └── views.py                  # Ask, History
    │   ├── documents/                    # Document upload & processing
    │   │   ├── models.py                 # Document
    │   │   ├── serializers.py
    │   │   ├── urls.py   
    │   │   └── views.py                  # Upload
    │   ├── rag_engine/                   # RAG core (non-Django)
    │   │   ├── access_control
    │   │   ├── loaders.py                # PDF / text loader
    │   │   ├── chunker.py                # Text chunking
    │   │   ├── embeddings.py             # SentenceTransformer
    │   │   ├── vector_store.py           # FAISS index
    │   │   ├── pipeline
    │   │   ├── retriever.py              # Search + access control
    │   │   └── generator.py              # Self-hosted
    │   ├── evaluation/                   # RAG evaluation
    │   │   └── eval_rag.py               # Precision / Recall / Faithfulness
    │   ├── manage.py
    │   ├── requirements.txt
    │   └── db.sqlite3                    # Development database
    ├── frontend-svelte/                  # SvelteKit frontend
    │   ├── src/
    │   │   ├── lib/
    │   │   │   └── auth.ts                # JWT store
    │   │   ├── routes/
    │   │   │   ├── login/+page.svelte     # Login UI
    │   │   │   ├── chat/+page.svelte      # Chat interface + history
    │   │   │   └── upload/+page.svelte    # Role-based document upload
    │   │   └── app.html                   # Root template
    │   ├── .env                           # VITE_BACKEND_URL
    │   ├── package.json
    │   └── svelte.config.js
    ├── README.md
    ├── .gitignore
    └── requirements.txt                  # Backend dependencies


## Backend Apps Breakdown

* accounts: JWT auth, custom User with roles (employee/hr/manager/admin).
* chat: Ask API (RAG query), history GET (paginated logs).
* documents: Upload API (ingest to FAISS with dept).
* rag_engine: Core RAG (load/chunk/embed/retrieve/generate/eval).

## Installation & Setup

Clone repo → cd backend.
python -m venv venv; source venv/bin/activate (Windows: venv\Scripts\activate).
pip install -r requirements.txt.
Copy .env.example to .env → Add SECRET_KEY, OPENAI_API_KEY.
python manage.py migrate.
python manage.py createsuperuser.
python manage.py runserver → localhost:8000.

cd frontend-svelte.
npm install.
Copy .env.example to .env → Add VITE_BACKEND_URL=http://localhost:8000.
npm run dev → localhost:5173.

## RAG Failure Handling & Explainability

Failure Handling

* No Docs: Returns "No relevant documents found" (low confidence).
* Access Denied: 403 + "Access denied for department" (role check).
* Low Relevance: Avg FAISS score <0.5 → "low" confidence + faithfulness eval <0.8 flags "verify sources".
* Hallucinations: LLM prompt: "Answer ONLY using context" + faithfulness score in history.
* Fallback: Broaden search to 'GENERAL' dept if role-specific fails.

Explainability

* Citations: Inline [1] in answers + list at bottom (doc_name + score).
* Confidence: "high/medium/low" from FAISS avg score (UI badge).
* Audit: History JSON with full Q/A/sources/confidence/timestamp (exportable).
* Eval: Backend script for precision@3 (1.00), recall (1.00), faithfulness (1.00) — plot saved as PNG.

## Evaluation Metrics

Run python evaluation/eval_rag.py:

* Precision@3: 1.00 (100% relevant top docs).
* Recall: 1.00 (All expected retrieved).
* Faithfulness: 1.00 (No hallucinations).

See evaluation/confidence_vs_faithfulness.png for correlation plot.

