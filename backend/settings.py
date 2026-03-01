import os
from functools import lru_cache

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4-turbo", alias="OPENAI_MODEL")

    # Backend URLs / CORS
    allowed_origins: list[str] = Field(
        default_factory=lambda:[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://ai-pdf-chatbot.vercel.app",
        "https://ai-pdf-chatbot-rohanjain11.vercel.app",
    ],
        alias="ALLOWED_ORIGINS",
    )

    # Storage configuration
    upload_dir: str = Field("uploads", alias="UPLOAD_DIR")
    cache_dir: str = Field("cache", alias="CACHE_DIR")

    # PDF limits
    max_pdf_size_mb: int = Field(20, alias="MAX_PDF_SIZE_MB")
    max_pdf_pages: int = Field(200, alias="MAX_PDF_PAGES")

    # Retrieval / context limits
    faiss_k: int = Field(5, alias="FAISS_K")
    context_max_chars: int = Field(8000, alias="CONTEXT_MAX_CHARS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance so we don't re-parse env on every request."""
    # Ensure the env file is resolved relative to this file's directory when running from other CWDs
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        os.environ.setdefault("DOTENV_PATH", env_path)
    return Settings()

