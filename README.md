# AI Knowledge Assistant  
LangChain + RAG + FastAPI + React + Hugging Face + Qdrant

This project implements a complete Retrieval-Augmented Generation (RAG) system.  
It uses LangChain for orchestration, Hugging Face for LLMs and embeddings, Qdrant for vector search, FastAPI for the backend, and React for the frontend.


## Features

### Retrieval-Augmented Generation (RAG)
- PDF ingestion through file upload  
- Text extraction and chunking  
- Semantic search using Qdrant  
- Context injection into the LLM prompt  

### Hugging Face Inference
- Wraps a Hugging Face chat model  
- Executes retrieval steps before synthesizing an answer  
- Produces grounded, context-aware responses  

### Backend (FastAPI)
- `/ingest/upload`: PDF ingestion 
- `/ingest/documents`: Listing indexed documents
- `/ask`: RAG + answer 
- Modular components (LLM client, embedder, vector store, agent logic)  

### Frontend (React)
- Chat interface  
- PDF upload  
- API communication via a simple client wrapper  

### Infrastructure
- Docker Compose for local deployment  
- Runs backend, frontend, and Qdrant together  
- Compatible with low-cost VPS hosting


## Quickstart

### 1. Clone the repository

```bash
git clone https://github.com/patrick-randria/ai-knowledge-assistant
cd ai-knowledge-assistant
```

### 2. Environment variables

Create a file at:

```
backend/.env
```

with the following content:

```
HF_API_TOKEN=your_huggingface_key
HF_MODEL=openai/gpt-oss-120b:fastest
HF_EMBED_MODEL=intfloat/e5-small
QDRANT_HOST=qdrant
QDRANT_PORT=6333
QDRANT_COLLECTION=docs
EMBED_DIM=384
ALLOWED_ORIGINS=*
```

Make sure the `EMBED_DIM` value matches the embedding model you choose.

### 3. Start the stack

```bash
docker-compose up --build
```

Services:

- Frontend: http://localhost:3000  
- Backend: http://localhost:8000  
- Qdrant UI: http://localhost:6333/dashboard  


## How It Works

1. A PDF is uploaded to the backend  
2. Text is extracted and chunked  
3. Chunks are embedded using Hugging Face  
4. Embeddings are stored in Qdrant  
5. A query triggers a retrieval + synthesis pipeline using LangChain  


## Recommended Models

LLMs:
- microsoft/Phi-3-mini-4k-instruct
- google/gemma-2b-it
- mistralai/Mistral-7B-Instruct-v0.3

Embeddings:
- intfloat/e5-small (384 dim)  
- intfloat/e5-base (768 dim)  
- sentence-transformers/all-MiniLM-L6-v2 (384 dim)


## Deployment Notes

A low-cost VPS (2GB RAM minimum recommended) is sufficient for this stack, since all LLM inference happens through Hugging Face’s hosted API.

To expose the application publicly:
- serve the React build through Nginx  
- reverse-proxy the FastAPI backend  
- use Certbot for HTTPS  

---

## Author

Patrick R. | Python Developer  

GitHub: https://github.com/patrick-randria

Forks welcome.

---

## License

MIT License
