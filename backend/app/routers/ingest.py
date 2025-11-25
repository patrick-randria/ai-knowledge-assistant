# backend/app/routers/ingest.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from rag.rag_chain import RAGChain

router = APIRouter()

@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    content = await file.read()

    RAGChain().ingest_document(file_bytes=content, filename=file.filename)
    return {"status":"ingested"}

@router.get("/documents")
def list_indexed_documents(limit: int = 10):
    documents = RAGChain().vector_store.list_indexed_documents(limit=limit)
    return documents
