# backend/app/main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.chat import router as chat_router
from routers.ingest import router as ingest_router
from routers.health import router as health_router

app = FastAPI(title="AI Knowledge Assistant", version="0.1.0")

# CORS - allow from frontend dev by default
origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != [""] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(ingest_router, prefix="/ingest", tags=["ingest"])
app.include_router(ingest_router, prefix="/documents", tags=["documents"])
app.include_router(health_router, prefix="/health", tags=["health"])
