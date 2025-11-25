# backend/app/rag/rag_chain.py
import asyncio
from rag.huggingface import HuggingFaceClient
from rag.vectorstore import VectorStore
from typing import List
from pathlib import Path
from config import settings
import uuid
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAGChain:

    def __init__(self):

        self.huggingface_client = HuggingFaceClient()
        
        self.embedding = self.huggingface_client.get_embedding()

        self.vector_store = VectorStore(self.embedding)

        self.ensure_dir(settings.PDF_STORAGE_DIR)
    
    def load_document(self, path: str) -> List[str]:
        loader = PyPDFLoader(path)
        documents = loader.load()
        return documents
    
    def split_documents(self, documents: List[str]) -> List[str]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=60,
            length_function=len,
            separators=["\n\n", "\n"]
        )
        all_splits = text_splitter.split_documents(documents=documents)
        return all_splits
    
    def embed_and_index(self, chunks: List[str]):
        return self.vector_store.upload_documents_to_index(chunks)
    
    def ensure_dir(self, path: str):
        Path(path).mkdir(parents=True, exist_ok=True)
    
    def save_pdf_bytes(self, file_bytes: bytes, filename: str = None) -> str:
        if not filename:
            filename = f"{uuid.uuid4()}.pdf"
        path = Path(settings.PDF_STORAGE_DIR) / filename
        with open(path, "wb") as f:
            f.write(file_bytes)
        return str(path)
    
    
    def retreive(self, question: str, top_k: int = 4):
        retrieved_docs = self.vector_store.get_vectorstore().similarity_search(
            question,
            k=top_k
        )
        return retrieved_docs
    
    ## RAG Pipelines
    def ingest_document(self, file_bytes: bytes, filename: str = None):
        path = self.save_pdf_bytes(file_bytes, filename)
        documents = self.load_document(path)
        chunks = self.split_documents(documents)
        self.embed_and_index(chunks)
        return {"status":"ok"}
    
    def answer_question(self, question: str):
        retrieved_docs = self.retreive(question)
        answer = self.huggingface_client.generate(
            question, retrieved_docs
        )
        return answer
