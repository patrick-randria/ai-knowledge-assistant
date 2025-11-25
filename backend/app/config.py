# backend/app/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    HF_API_TOKEN: str = Field(..., env="HF_API_TOKEN")
    HF_CHAT_MODEL: str = Field("microsoft/Phi-3-mini-4k-instruct", env="HF_CHAT_MODEL")
    HF_EMBED_MODEL: str = Field("intfloat/e5-small", env="HF_EMBED_MODEL")  # adjust if needed

    QDRANT_HOST: str = Field("qdrant", env="QDRANT_HOST")
    QDRANT_PORT: int = Field(6333, env="QDRANT_PORT")
    QDRANT_COLLECTION: str = Field("docs", env="QDRANT_COLLECTION")

    PDF_STORAGE_DIR: str = Field("storage/pdfs", env="PDF_STORAGE_DIR")
    EMBED_DIM: int = Field(768, env="EMBED_DIM")  # set to embedding dim of chosen model

    APP_ORIGINS: str = Field("*", env="APP_ORIGINS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
