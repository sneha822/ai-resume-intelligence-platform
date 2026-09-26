"""CPU-friendly embeddings via fastembed (ONNX runtime, no PyTorch).

Model download happens lazily on first use and is cached by fastembed, so
importing this module is cheap. Runs comfortably on a CPU-only laptop.
"""

from __future__ import annotations

import asyncio
from functools import lru_cache
from typing import TYPE_CHECKING

from backend.core.config import settings

if TYPE_CHECKING:
    from fastembed import TextEmbedding


@lru_cache(maxsize=2)
def _load_model(model_name: str) -> TextEmbedding:
    from fastembed import TextEmbedding

    return TextEmbedding(model_name=model_name)


class FastEmbedEmbedder:
    """Implements the ``Embedder`` port."""

    def __init__(self, model_name: str | None = None, dim: int | None = None) -> None:
        self._model_name = model_name or settings.embedding_model
        self._dim = dim or settings.embedding_dim

    @property
    def dimension(self) -> int:
        return self._dim

    def _embed_sync(self, texts: list[str]) -> list[list[float]]:
        model = _load_model(self._model_name)
        return [vector.tolist() for vector in model.embed(texts)]

    async def embed(self, text: str) -> list[float]:
        result = await self.embed_batch([text])
        return result[0]

    async def embed_batch(self, texts: list[str]) -> list[list[float]]:
        # fastembed is synchronous/CPU-bound; run off the event loop.
        return await asyncio.to_thread(self._embed_sync, texts)
