"""Embedding provider port."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class Embedder(Protocol):
    @property
    def dimension(self) -> int:
        """Dimensionality of the produced vectors (must match the DB column)."""
        ...

    async def embed(self, text: str) -> list[float]:
        """Embed a single piece of text."""
        ...

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed many texts; order of the result matches the input."""
        ...
