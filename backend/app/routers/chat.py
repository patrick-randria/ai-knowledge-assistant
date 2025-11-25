# backend/app/routers/chat.py
from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import Response
from rag.rag_chain import RAGChain

router = APIRouter()

class Question(BaseModel):
    question: str

@router.post("/ask")
def ask(q: Question):
    res = RAGChain().answer_question(q.question)

    return Response(content=res, media_type="text/markdown")
