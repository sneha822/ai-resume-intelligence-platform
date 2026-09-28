"""Application configuration via pydantic-settings.

Values are read from environment variables (or a local ``.env`` file). See
``.env.example`` for the full list.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import AliasChoices, Field
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

    # --- Ingestion mode ---
    # "async" enqueues to Celery (needs a worker + Redis); "sync" runs the pipeline
    # inline in the request (no worker/Redis needed — good for free hosting).
    ingest_mode: str = Field(default="async")

    # --- LLM ---
    llm_provider: str = Field(default="anthropic")  # "anthropic" | "gemini" | "ollama"
    llm_model: str = Field(default="claude-sonnet-5")
    anthropic_api_key: str = Field(default="")
    ollama_model: str = Field(default="llama3.2")
    # Gemini (accepts GEMINI_API_KEY or GOOGLE_API_KEY)
    gemini_api_key: str = Field(
        default="",
        validation_alias=AliasChoices("GEMINI_API_KEY", "GOOGLE_API_KEY"),
    )
    gemini_model: str = Field(default="gemini-3.8-flash")

    # --- Embeddings / retrieval ---
    # CPU-friendly ONNX embeddings via fastembed (no torch). 768-dim.
    embedding_model: str = Field(default="BAAI/bge-base-en-v1.5")
    embedding_dim: int = Field(default=768)

    # --- Observability (OpenTelemetry) ---
    otel_enabled: bool = Field(default=False)
    otel_service_name: str = Field(default="airi-backend")
    # e.g. http://localhost:4318 (Phoenix / OTLP collector). Empty = no OTLP export.
    otel_exporter_otlp_endpoint: str = Field(default="")
    otel_console_export: bool = Field(default=False)


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()


settings = get_settings()
