"""LLM provider factory — selects the concrete provider from settings."""

from __future__ import annotations

from backend.core.config import settings
from backend.core.ports.llm import LLMProvider


def get_llm_provider() -> LLMProvider:
    provider = settings.llm_provider.lower()
    if provider == "anthropic":
        from backend.adapters.llm.anthropic_provider import AnthropicProvider

        return AnthropicProvider()
    if provider == "ollama":
        from backend.adapters.llm.ollama_provider import OllamaProvider

        return OllamaProvider()
    raise ValueError(f"Unknown LLM provider: {settings.llm_provider!r}")
