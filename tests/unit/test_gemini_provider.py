"""Gemini provider selection + configuration checks (no network)."""

from __future__ import annotations

import pytest

from backend.adapters.llm.factory import get_llm_provider, is_llm_configured
from backend.adapters.llm.gemini_provider import GeminiProvider
from backend.core.config import settings


def test_gemini_provider_implements_port_surface() -> None:
    for method in ("generate", "structured", "stream"):
        assert callable(getattr(GeminiProvider, method))


@pytest.mark.parametrize(
    ("provider", "anthropic_key", "gemini_key", "expected"),
    [
        ("anthropic", "sk-x", "", True),
        ("anthropic", "", "", False),
        ("gemini", "", "g-x", True),
        ("gemini", "", "", False),
        ("ollama", "", "", True),
        ("unknown", "", "", False),
    ],
)
def test_is_llm_configured(
    monkeypatch: pytest.MonkeyPatch,
    provider: str,
    anthropic_key: str,
    gemini_key: str,
    expected: bool,
) -> None:
    monkeypatch.setattr(settings, "llm_provider", provider)
    monkeypatch.setattr(settings, "anthropic_api_key", anthropic_key)
    monkeypatch.setattr(settings, "gemini_api_key", gemini_key)
    assert is_llm_configured() is expected


def test_factory_selects_gemini(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "llm_provider", "gemini")
    monkeypatch.setattr(settings, "gemini_api_key", "test-key")
    provider = get_llm_provider()
    assert isinstance(provider, GeminiProvider)
