"""Application configuration via pydantic-settings.

Values are read from environment variables (or a local ``.env`` file). See
``.env.example`` for the full list.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App ---
    app_name: str = "AI Resume Intelligence Platform"
    environment: str = Field(default="development")
    debug: bool = Field(default=True)

    # --- Database (Postgres + pgvector) ---
    database_url: str = Field(default="postgresql+psycopg://airi:airi@localhost:5432/airi")

    # --- Redis / Celery ---
    redis_url: str = Field(default="redis://localhost:6379/0")
    celery_broker_url: str = Field(default="redis://localhost:6379/0")
    celery_result_backend: str = Field(default="redis://localhost:6379/1")

    # --- LLM ---
    llm_provider: str = Field(default="anthropic")  # "anthropic" | "ollama"
    llm_model: str = Field(default="claude-sonnet-5")
    anthropic_api_key: str = Field(default="")
    ollama_model: str = Field(default="llama3.2")

    # --- Embeddings / retrieval ---
    # CPU-friendly ONNX embeddings via fastembed (no torch). 768-dim.
    embedding_model: str = Field(default="BAAI/bge-base-en-v1.5")
    embedding_dim: int = Field(default=768)


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()


settings = get_settings()
