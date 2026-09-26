"""Embedder factory (singleton to avoid reloading the model)."""

from __future__ import annotations

from functools import lru_cache

from backend.adapters.embeddings.fastembed_embedder import FastEmbedEmbedder
from backend.core.ports.embedder import Embedder


@lru_cache(maxsize=1)
def get_embedder() -> Embedder:
    return FastEmbedEmbedder()
