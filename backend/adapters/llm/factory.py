"""LLM provider factory — selects the concrete provider from settings."""

from __future__ import annotations

from backend.core.config import settings
from backend.core.ports.llm import LLMProvider


def get_llm_provider() -> LLMProvider:
    provider = settings.llm_provider.lower()
    if provider == "anthropic":
        from backend.adapters.llm.anthropic_provider import AnthropicProvider

        return AnthropicProvider()
    if provider == "gemini":
        from backend.adapters.llm.gemini_provider import GeminiProvider

        return GeminiProvider()
    if provider == "ollama":
        from backend.adapters.llm.ollama_provider import OllamaProvider

        return OllamaProvider()
    raise ValueError(f"Unknown LLM provider: {settings.llm_provider!r}")


def is_llm_configured() -> bool:
    """Whether the selected provider has the credentials it needs to run.

    Ollama is assumed reachable locally; hosted providers require their key.
    """
    provider = settings.llm_provider.lower()
    if provider == "anthropic":
        return bool(settings.anthropic_api_key)
    if provider == "gemini":
        return bool(settings.gemini_api_key)
    return provider == "ollama"
