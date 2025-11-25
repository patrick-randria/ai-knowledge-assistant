# backend/app/routers/health.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
def ping():
    return {"status": "ok"}
