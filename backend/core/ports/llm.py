"""LLM provider port.

Any concrete provider (Anthropic/Claude, Ollama, ...) implements this
Protocol. ``structured`` is the primary path: it returns a validated Pydantic
model rather than raw text, so callers never parse JSON by hand.
"""

from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@runtime_checkable
class LLMProvider(Protocol):
    async def generate(self, prompt: str, system: str | None = None) -> str:
        """Return a free-text completion."""
        ...

    async def structured(
        self,
        prompt: str,
        response_model: type[T],
        system: str | None = None,
    ) -> T:
        """Return a validated instance of ``response_model``.

        Implementations should enforce the schema (e.g. via Instructor) and
        retry on validation failure.
        """
        ...
